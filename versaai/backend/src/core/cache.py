"""Redis Cache Configuration for VersaAI"""

import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from typing import Optional
import os
import json
from datetime import datetime, timedelta


class CacheManager:
    """Gestión centralizada de caché Redis"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.cache_ttl = int(os.getenv("REDIS_CACHE_TTL", 3600))
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
    async def init_cache(self):
        """Inicializar conexión Redis y FastAPI Cache"""
        try:
            # Configurar cliente Redis
            self.redis_client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", 20))
            )
            
            # Probar conexión
            await self.redis_client.ping()
            
            # Configurar FastAPI Cache
            FastAPICache.init(
                RedisBackend(self.redis_client),
                prefix="versaai-cache"
            )
            
            print("✅ Redis Cache inicializado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando Redis Cache: {e}")
            return False
    
    async def set_cache(self, key: str, value: any, ttl: Optional[int] = None) -> bool:
        """Guardar valor en caché"""
        try:
            if not self.redis_client:
                return False
                
            ttl = ttl or self.cache_ttl
            serialized_value = json.dumps(value, default=str)
            
            await self.redis_client.setex(
                f"versaai:{key}",
                ttl,
                serialized_value
            )
            return True
            
        except Exception as e:
            print(f"Error guardando en caché {key}: {e}")
            return False
    
    async def get_cache(self, key: str) -> Optional[any]:
        """Obtener valor del caché"""
        try:
            if not self.redis_client:
                return None
                
            cached_value = await self.redis_client.get(f"versaai:{key}")
            
            if cached_value:
                return json.loads(cached_value)
            return None
            
        except Exception as e:
            print(f"Error obteniendo del caché {key}: {e}")
            return None
    
    async def delete_cache(self, key: str) -> bool:
        """Eliminar valor del caché"""
        try:
            if not self.redis_client:
                return False
                
            result = await self.redis_client.delete(f"versaai:{key}")
            return result > 0
            
        except Exception as e:
            print(f"Error eliminando del caché {key}: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Limpiar caché por patrón"""
        try:
            if not self.redis_client:
                return 0
                
            keys = await self.redis_client.keys(f"versaai:{pattern}*")
            if keys:
                return await self.redis_client.delete(*keys)
            return 0
            
        except Exception as e:
            print(f"Error limpiando caché con patrón {pattern}: {e}")
            return 0
    
    async def get_cache_stats(self) -> dict:
        """Obtener estadísticas del caché"""
        try:
            if not self.redis_client:
                return {"status": "disconnected"}
                
            info = await self.redis_client.info()
            
            return {
                "status": "connected",
                "used_memory": info.get("used_memory_human", "N/A"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Instancia global del gestor de caché
cache_manager = CacheManager()


# Decorador para caché automático
def cache_response(ttl: int = 3600, key_prefix: str = ""):
    """Decorador para cachear respuestas de endpoints"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generar clave de caché
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Intentar obtener del caché
            cached_result = await cache_manager.get_cache(cache_key)
            if cached_result:
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            await cache_manager.set_cache(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator