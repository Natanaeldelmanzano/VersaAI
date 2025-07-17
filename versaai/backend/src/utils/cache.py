from typing import Any, Optional, Dict, List
import asyncio
import json
import pickle
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        self.cache_dir = Path(settings.DATA_DIR or './data') / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._initialize_redis()
    
    def _initialize_redis(self):
        """
        Initialize Redis connection if available
        """
        if not REDIS_AVAILABLE:
            logger.info("Redis not available, using memory and file cache")
            return
        
        try:
            redis_url = settings.REDIS_URL or 'redis://localhost:6379'
            self.redis_client = redis.from_url(
                redis_url,
                encoding='utf-8',
                decode_responses=True
            )
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Redis: {str(e)}")
            self.redis_client = None
    
    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache
        """
        try:
            # Try Redis first
            if self.redis_client:
                value = await self._get_from_redis(key)
                if value is not None:
                    return value
            
            # Try memory cache
            if key in self.memory_cache:
                cache_item = self.memory_cache[key]
                if not self._is_expired(cache_item):
                    return cache_item['value']
                else:
                    del self.memory_cache[key]
            
            # Try file cache
            value = await self._get_from_file(key)
            if value is not None:
                return value
            
            return default
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {str(e)}")
            return default
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with optional expiration
        """
        try:
            success = False
            
            # Set in Redis
            if self.redis_client:
                success = await self._set_in_redis(key, value, expire)
            
            # Set in memory cache
            expire_time = None
            if expire:
                expire_time = datetime.utcnow() + timedelta(seconds=expire)
            
            self.memory_cache[key] = {
                'value': value,
                'expire_time': expire_time,
                'created_at': datetime.utcnow()
            }
            
            # Set in file cache for persistence
            await self._set_in_file(key, value, expire_time)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache
        """
        try:
            # Delete from Redis
            if self.redis_client:
                await self.redis_client.delete(key)
            
            # Delete from memory
            if key in self.memory_cache:
                del self.memory_cache[key]
            
            # Delete from file
            await self._delete_from_file(key)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {str(e)}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache
        """
        try:
            # Check Redis
            if self.redis_client:
                exists = await self.redis_client.exists(key)
                if exists:
                    return True
            
            # Check memory
            if key in self.memory_cache:
                cache_item = self.memory_cache[key]
                if not self._is_expired(cache_item):
                    return True
                else:
                    del self.memory_cache[key]
            
            # Check file
            return await self._exists_in_file(key)
            
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {str(e)}")
            return False
    
    async def clear(self, pattern: Optional[str] = None) -> bool:
        """
        Clear cache entries, optionally by pattern
        """
        try:
            # Clear Redis
            if self.redis_client:
                if pattern:
                    keys = await self.redis_client.keys(pattern)
                    if keys:
                        await self.redis_client.delete(*keys)
                else:
                    await self.redis_client.flushdb()
            
            # Clear memory
            if pattern:
                import fnmatch
                keys_to_delete = [
                    key for key in self.memory_cache.keys()
                    if fnmatch.fnmatch(key, pattern)
                ]
                for key in keys_to_delete:
                    del self.memory_cache[key]
            else:
                self.memory_cache.clear()
            
            # Clear file cache
            await self._clear_file_cache(pattern)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        """
        try:
            stats = {
                'memory_cache_size': len(self.memory_cache),
                'redis_available': self.redis_client is not None,
                'file_cache_dir': str(self.cache_dir)
            }
            
            # Redis stats
            if self.redis_client:
                try:
                    redis_info = await self.redis_client.info('memory')
                    stats['redis_memory_usage'] = redis_info.get('used_memory_human', 'unknown')
                    stats['redis_keys'] = await self.redis_client.dbsize()
                except Exception as e:
                    stats['redis_error'] = str(e)
            
            # File cache stats
            file_cache_files = list(self.cache_dir.glob('*.cache'))
            stats['file_cache_files'] = len(file_cache_files)
            
            total_size = sum(f.stat().st_size for f in file_cache_files)
            stats['file_cache_size'] = f"{total_size / 1024 / 1024:.2f} MB"
            
            return stats
            
        except Exception as e:
            logger.error(f"Cache stats error: {str(e)}")
            return {'error': str(e)}
    
    async def _get_from_redis(self, key: str) -> Any:
        """
        Get value from Redis
        """
        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Redis get error: {str(e)}")
            return None
    
    async def _set_in_redis(self, key: str, value: Any, expire: Optional[int]) -> bool:
        """
        Set value in Redis
        """
        try:
            serialized_value = json.dumps(value, default=str)
            if expire:
                await self.redis_client.setex(key, expire, serialized_value)
            else:
                await self.redis_client.set(key, serialized_value)
            return True
        except Exception as e:
            logger.warning(f"Redis set error: {str(e)}")
            return False
    
    async def _get_from_file(self, key: str) -> Any:
        """
        Get value from file cache
        """
        try:
            file_path = self.cache_dir / f"{self._hash_key(key)}.cache"
            if not file_path.exists():
                return None
            
            with open(file_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check expiration
            if cache_data.get('expire_time'):
                if datetime.utcnow() > cache_data['expire_time']:
                    file_path.unlink()  # Delete expired file
                    return None
            
            return cache_data['value']
            
        except Exception as e:
            logger.warning(f"File cache get error: {str(e)}")
            return None
    
    async def _set_in_file(self, key: str, value: Any, expire_time: Optional[datetime]):
        """
        Set value in file cache
        """
        try:
            file_path = self.cache_dir / f"{self._hash_key(key)}.cache"
            cache_data = {
                'value': value,
                'expire_time': expire_time,
                'created_at': datetime.utcnow(),
                'key': key
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(cache_data, f)
                
        except Exception as e:
            logger.warning(f"File cache set error: {str(e)}")
    
    async def _delete_from_file(self, key: str):
        """
        Delete value from file cache
        """
        try:
            file_path = self.cache_dir / f"{self._hash_key(key)}.cache"
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            logger.warning(f"File cache delete error: {str(e)}")
    
    async def _exists_in_file(self, key: str) -> bool:
        """
        Check if key exists in file cache
        """
        try:
            file_path = self.cache_dir / f"{self._hash_key(key)}.cache"
            if not file_path.exists():
                return False
            
            # Check if expired
            with open(file_path, 'rb') as f:
                cache_data = pickle.load(f)
            
            if cache_data.get('expire_time'):
                if datetime.utcnow() > cache_data['expire_time']:
                    file_path.unlink()
                    return False
            
            return True
            
        except Exception as e:
            logger.warning(f"File cache exists error: {str(e)}")
            return False
    
    async def _clear_file_cache(self, pattern: Optional[str] = None):
        """
        Clear file cache
        """
        try:
            if pattern:
                # Load each file to check the original key
                for file_path in self.cache_dir.glob('*.cache'):
                    try:
                        with open(file_path, 'rb') as f:
                            cache_data = pickle.load(f)
                        
                        import fnmatch
                        if fnmatch.fnmatch(cache_data.get('key', ''), pattern):
                            file_path.unlink()
                    except Exception:
                        continue
            else:
                # Clear all cache files
                for file_path in self.cache_dir.glob('*.cache'):
                    file_path.unlink()
                    
        except Exception as e:
            logger.warning(f"File cache clear error: {str(e)}")
    
    def _hash_key(self, key: str) -> str:
        """
        Create a hash of the key for file naming
        """
        return hashlib.md5(key.encode()).hexdigest()
    
    def _is_expired(self, cache_item: Dict[str, Any]) -> bool:
        """
        Check if cache item is expired
        """
        expire_time = cache_item.get('expire_time')
        if expire_time is None:
            return False
        return datetime.utcnow() > expire_time
    
    async def cleanup_expired(self):
        """
        Clean up expired cache entries
        """
        try:
            # Clean memory cache
            expired_keys = [
                key for key, item in self.memory_cache.items()
                if self._is_expired(item)
            ]
            for key in expired_keys:
                del self.memory_cache[key]
            
            # Clean file cache
            for file_path in self.cache_dir.glob('*.cache'):
                try:
                    with open(file_path, 'rb') as f:
                        cache_data = pickle.load(f)
                    
                    if cache_data.get('expire_time'):
                        if datetime.utcnow() > cache_data['expire_time']:
                            file_path.unlink()
                except Exception:
                    continue
            
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
            
        except Exception as e:
            logger.error(f"Cache cleanup error: {str(e)}")

# Global cache manager instance
cache_manager = CacheManager()

# Convenience functions
async def get_cache(key: str, default: Any = None) -> Any:
    """Get value from cache"""
    return await cache_manager.get(key, default)

async def set_cache(key: str, value: Any, expire: Optional[int] = None) -> bool:
    """Set value in cache"""
    return await cache_manager.set(key, value, expire)

async def delete_cache(key: str) -> bool:
    """Delete value from cache"""
    return await cache_manager.delete(key)

async def clear_cache(pattern: Optional[str] = None) -> bool:
    """Clear cache entries"""
    return await cache_manager.clear(pattern)