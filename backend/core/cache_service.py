"""
Caching service utilities
"""
from functools import wraps
from django.core.cache import cache
from typing import Callable, Any, Optional
import hashlib
import json


class CacheService:
    """Service for caching operations"""
    
    DEFAULT_TIMEOUT = 300  # 5 minutes
    
    @staticmethod
    def get_cache_key(prefix: str, *args, **kwargs) -> str:
        """
        Generate cache key from prefix and arguments
        
        Args:
            prefix: Cache key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Cache key string
        """
        # Create a hash of arguments
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()[:8]
        return f"{prefix}:{key_hash}"
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get value from cache
        
        Args:
            key: Cache key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        return cache.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any, timeout: int = None) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            timeout: Cache timeout in seconds
            
        Returns:
            True if successful
        """
        timeout = timeout or CacheService.DEFAULT_TIMEOUT
        return cache.set(key, value, timeout)
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        return cache.delete(key)
    
    @staticmethod
    def clear_pattern(pattern: str) -> int:
        """
        Clear all keys matching pattern (requires Redis)
        
        Args:
            pattern: Pattern to match (e.g., 'user:*')
            
        Returns:
            Number of keys deleted
        """
        try:
            # This works with Redis backend
            if hasattr(cache, 'delete_pattern'):
                return cache.delete_pattern(pattern)
            else:
                # Fallback: clear all (not ideal)
                cache.clear()
                return 0
        except:
            return 0
    
    @staticmethod
    def cached(timeout: int = None, key_prefix: str = None):
        """
        Decorator for caching function results
        
        Args:
            timeout: Cache timeout in seconds
            key_prefix: Prefix for cache key
            
        Usage:
            @CacheService.cached(timeout=300, key_prefix='user_stats')
            def get_user_stats(user_id):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                prefix = key_prefix or f"{func.__module__}.{func.__name__}"
                cache_key = CacheService.get_cache_key(prefix, *args, **kwargs)
                
                # Try to get from cache
                cached_value = CacheService.get(cache_key)
                if cached_value is not None:
                    return cached_value
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Store in cache
                CacheService.set(cache_key, result, timeout)
                
                return result
            return wrapper
        return decorator


def invalidate_cache_pattern(pattern: str):
    """Invalidate cache by pattern"""
    return CacheService.clear_pattern(pattern)

