from typing import Any, Optional, Dict, List
import json
import pickle
import asyncio
import logging
from datetime import datetime, timedelta
import hashlib
import os
from abc import ABC, abstractmethod

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

from ..core.config import settings

logger = logging.getLogger(__name__)

class CacheBackend(ABC):
    """Interfaz abstracta para backends de caché"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        pass

class RedisCache(CacheBackend):
    """Backend de caché usando Redis"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = None
        self._connected = False
    
    async def connect(self):
        """Conecta al servidor Redis"""
        try:
            if not REDIS_AVAILABLE:
                raise ImportError("Redis not available")
            
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Probar conexión
            await self.redis_client.ping()
            self._connected = True
            logger.info("Redis cache connected successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._connected = False
            raise
    
    async def disconnect(self):
        """Desconecta del servidor Redis"""
        if self.redis_client:
            await self.redis_client.close()
            self._connected = False
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if not self._connected:
            return None
        
        try:
            value = await self.redis_client.get(key)
            if value is None:
                return None
            
            # Intentar deserializar JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
                
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Establece un valor en el caché"""
        if not self._connected:
            return False
        
        try:
            # Serializar valor
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False)
            else:
                serialized_value = str(value)
            
            # Establecer valor con expiración opcional
            if expire:
                await self.redis_client.setex(key, expire, serialized_value)
            else:
                await self.redis_client.set(key, serialized_value)
            
            return True
            
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        if not self._connected:
            return False
        
        try:
            result = await self.redis_client.delete(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        if not self._connected:
            return False
        
        try:
            result = await self.redis_client.exists(key)
            return result > 0
            
        except Exception as e:
            logger.error(f"Redis exists error for key {key}: {e}")
            return False
    
    async def clear(self) -> bool:
        """Limpia todo el caché"""
        if not self._connected:
            return False
        
        try:
            await self.redis_client.flushdb()
            return True
            
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché Redis"""
        if not self._connected:
            return {"connected": False}
        
        try:
            info = await self.redis_client.info()
            return {
                "connected": True,
                "used_memory": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
            
        except Exception as e:
            logger.error(f"Redis stats error: {e}")
            return {"connected": False, "error": str(e)}

class MemoryCache(CacheBackend):
    """Backend de caché en memoria"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_times: Dict[str, datetime] = {}
        self.max_size = 1000  # Máximo número de elementos
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Verificar expiración
        if entry.get("expires_at") and datetime.utcnow() > entry["expires_at"]:
            await self.delete(key)
            return None
        
        # Actualizar tiempo de acceso
        self.access_times[key] = datetime.utcnow()
        
        return entry["value"]
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Establece un valor en el caché"""
        try:
            # Calcular tiempo de expiración
            expires_at = None
            if expire:
                expires_at = datetime.utcnow() + timedelta(seconds=expire)
            
            # Limpiar caché si está lleno
            if len(self.cache) >= self.max_size:
                await self._evict_oldest()
            
            # Establecer valor
            self.cache[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": datetime.utcnow()
            }
            
            self.access_times[key] = datetime.utcnow()
            return True
            
        except Exception as e:
            logger.error(f"Memory cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
            return True
            
        except Exception as e:
            logger.error(f"Memory cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        if key not in self.cache:
            return False
        
        entry = self.cache[key]
        
        # Verificar expiración
        if entry.get("expires_at") and datetime.utcnow() > entry["expires_at"]:
            await self.delete(key)
            return False
        
        return True
    
    async def clear(self) -> bool:
        """Limpia todo el caché"""
        try:
            self.cache.clear()
            self.access_times.clear()
            return True
            
        except Exception as e:
            logger.error(f"Memory cache clear error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché en memoria"""
        try:
            total_size = len(self.cache)
            expired_count = 0
            
            # Contar elementos expirados
            current_time = datetime.utcnow()
            for entry in self.cache.values():
                if entry.get("expires_at") and current_time > entry["expires_at"]:
                    expired_count += 1
            
            return {
                "type": "memory",
                "total_keys": total_size,
                "expired_keys": expired_count,
                "max_size": self.max_size,
                "usage_percentage": (total_size / self.max_size) * 100
            }
            
        except Exception as e:
            logger.error(f"Memory cache stats error: {e}")
            return {"type": "memory", "error": str(e)}
    
    async def _evict_oldest(self):
        """Elimina el elemento más antiguo del caché"""
        if not self.access_times:
            return
        
        # Encontrar la clave con el tiempo de acceso más antiguo
        oldest_key = min(self.access_times.keys(), 
                        key=lambda k: self.access_times[k])
        
        await self.delete(oldest_key)

class FileCache(CacheBackend):
    """Backend de caché basado en archivos"""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Obtiene la ruta del archivo para una clave"""
        # Crear hash seguro para el nombre del archivo
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.cache")
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        file_path = self._get_file_path(key)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            
            # Verificar expiración
            if data.get("expires_at") and datetime.utcnow() > data["expires_at"]:
                await self.delete(key)
                return None
            
            return data["value"]
            
        except Exception as e:
            logger.error(f"File cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Establece un valor en el caché"""
        file_path = self._get_file_path(key)
        
        try:
            # Calcular tiempo de expiración
            expires_at = None
            if expire:
                expires_at = datetime.utcnow() + timedelta(seconds=expire)
            
            # Preparar datos
            data = {
                "value": value,
                "expires_at": expires_at,
                "created_at": datetime.utcnow()
            }
            
            # Escribir archivo
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            return True
            
        except Exception as e:
            logger.error(f"File cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        file_path = self._get_file_path(key)
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
            
        except Exception as e:
            logger.error(f"File cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        file_path = self._get_file_path(key)
        
        if not os.path.exists(file_path):
            return False
        
        # Verificar si no ha expirado
        value = await self.get(key)
        return value is not None
    
    async def clear(self) -> bool:
        """Limpia todo el caché"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    file_path = os.path.join(self.cache_dir, filename)
                    os.remove(file_path)
            return True
            
        except Exception as e:
            logger.error(f"File cache clear error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché de archivos"""
        try:
            cache_files = [f for f in os.listdir(self.cache_dir) 
                          if f.endswith('.cache')]
            
            total_size = 0
            expired_count = 0
            
            for filename in cache_files:
                file_path = os.path.join(self.cache_dir, filename)
                total_size += os.path.getsize(file_path)
                
                # Verificar si está expirado
                try:
                    with open(file_path, 'rb') as f:
                        data = pickle.load(f)
                    
                    if (data.get("expires_at") and 
                        datetime.utcnow() > data["expires_at"]):
                        expired_count += 1
                        
                except Exception:
                    expired_count += 1  # Archivo corrupto
            
            return {
                "type": "file",
                "total_files": len(cache_files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "expired_files": expired_count,
                "cache_directory": self.cache_dir
            }
            
        except Exception as e:
            logger.error(f"File cache stats error: {e}")
            return {"type": "file", "error": str(e)}

class CacheManager:
    """Gestor principal de caché con múltiples backends"""
    
    def __init__(self):
        self.backend: Optional[CacheBackend] = None
        self.fallback_backend: Optional[CacheBackend] = None
        self._initialized = False
    
    async def initialize(self):
        """Inicializa el gestor de caché"""
        try:
            # Intentar usar Redis si está disponible
            if REDIS_AVAILABLE and hasattr(settings, 'REDIS_URL') and settings.REDIS_URL:
                try:
                    redis_cache = RedisCache(settings.REDIS_URL)
                    await redis_cache.connect()
                    self.backend = redis_cache
                    logger.info("Using Redis cache backend")
                except Exception as e:
                    logger.warning(f"Redis cache failed, falling back to memory: {e}")
            
            # Fallback a caché en memoria
            if not self.backend:
                self.backend = MemoryCache()
                logger.info("Using memory cache backend")
            
            # Configurar fallback a caché de archivos
            cache_dir = getattr(settings, 'CACHE_DIR', './cache')
            self.fallback_backend = FileCache(cache_dir)
            
            self._initialized = True
            logger.info("Cache manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize cache manager: {e}")
            # Usar caché en memoria como último recurso
            self.backend = MemoryCache()
            self._initialized = True
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Intentar con backend principal
            value = await self.backend.get(key)
            if value is not None:
                return value
            
            # Intentar con fallback si está disponible
            if self.fallback_backend:
                return await self.fallback_backend.get(key)
            
            return None
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Establece un valor en el caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Intentar con backend principal
            success = await self.backend.set(key, value, expire)
            
            # También guardar en fallback para redundancia
            if self.fallback_backend:
                await self.fallback_backend.set(key, value, expire)
            
            return success
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Eliminar de ambos backends
            success1 = await self.backend.delete(key)
            success2 = True
            
            if self.fallback_backend:
                success2 = await self.fallback_backend.delete(key)
            
            return success1 or success2
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe en el caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Verificar en backend principal
            exists = await self.backend.exists(key)
            if exists:
                return True
            
            # Verificar en fallback
            if self.fallback_backend:
                return await self.fallback_backend.exists(key)
            
            return False
            
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    async def clear(self) -> bool:
        """Limpia todo el caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Limpiar ambos backends
            success1 = await self.backend.clear()
            success2 = True
            
            if self.fallback_backend:
                success2 = await self.fallback_backend.clear()
            
            return success1 and success2
            
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del caché"""
        if not self._initialized:
            await self.initialize()
        
        try:
            stats = {
                "primary_backend": await self.backend.get_stats(),
                "initialized": self._initialized
            }
            
            if self.fallback_backend:
                stats["fallback_backend"] = await self.fallback_backend.get_stats()
            
            return stats
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"error": str(e)}
    
    async def cleanup_expired(self) -> int:
        """Limpia elementos expirados del caché"""
        # Esta funcionalidad se puede implementar para backends específicos
        # Por ahora, retorna 0
        return 0

# Instancia global del gestor de caché
cache_manager = CacheManager()

# Funciones de conveniencia
async def get_cache(key: str) -> Optional[Any]:
    """Función de conveniencia para obtener del caché"""
    return await cache_manager.get(key)

async def set_cache(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """Función de conveniencia para establecer en el caché"""
    return await cache_manager.set(key, value, expire)

async def delete_cache(key: str) -> bool:
    """Función de conveniencia para eliminar del caché"""
    return await cache_manager.delete(key)

async def exists_cache(key: str) -> bool:
    """Función de conveniencia para verificar existencia en el caché"""
    return await cache_manager.exists(key)

async def clear_cache() -> bool:
    """Función de conveniencia para limpiar el caché"""
    return await cache_manager.clear()

async def get_cache_stats() -> Dict[str, Any]:
    """Función de conveniencia para obtener estadísticas del caché"""
    return await cache_manager.get_stats()