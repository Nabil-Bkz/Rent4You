"""
Rate limiting middleware
"""
import time
from collections import defaultdict
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status


class RateLimiter:
    """Simple rate limiter using cache"""
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
    
    def is_allowed(self, key: str) -> tuple[bool, dict]:
        """
        Check if request is allowed
        
        Args:
            key: Unique identifier (usually IP or user ID)
            
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        now = time.time()
        minute_key = f"rate_limit_minute_{key}"
        hour_key = f"rate_limit_hour_{key}"
        
        # Get current counts
        minute_count = cache.get(minute_key, 0)
        hour_count = cache.get(hour_key, 0)
        
        # Check limits
        minute_allowed = minute_count < self.requests_per_minute
        hour_allowed = hour_count < self.requests_per_hour
        
        is_allowed = minute_allowed and hour_allowed
        
        if is_allowed:
            # Increment counters
            cache.set(minute_key, minute_count + 1, 60)  # Expire in 60 seconds
            cache.set(hour_key, hour_count + 1, 3600)  # Expire in 1 hour
        
        rate_limit_info = {
            'limit_per_minute': self.requests_per_minute,
            'limit_per_hour': self.requests_per_hour,
            'remaining_minute': max(0, self.requests_per_minute - minute_count - 1) if is_allowed else 0,
            'remaining_hour': max(0, self.requests_per_hour - hour_count - 1) if is_allowed else 0,
            'reset_minute': int(now) + 60,
            'reset_hour': int(now) + 3600,
        }
        
        return is_allowed, rate_limit_info


class RateLimitMiddleware:
    """Middleware for rate limiting"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limiter = RateLimiter(
            requests_per_minute=60,
            requests_per_hour=1000
        )
        # Exclude these paths from rate limiting
        self.excluded_paths = ['/admin/', '/static/', '/media/', '/api/auth/token/']
    
    def __call__(self, request):
        # Skip rate limiting for excluded paths
        if any(request.path.startswith(path) for path in self.excluded_paths):
            return self.get_response(request)
        
        # Get identifier (IP address or user ID)
        identifier = self.get_identifier(request)
        
        # Check rate limit
        is_allowed, rate_limit_info = self.rate_limiter.is_allowed(identifier)
        
        if not is_allowed:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Rate limit exceeded. Please try again later.',
                    'rate_limit': rate_limit_info
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        response = self.get_response(request)
        
        # Add rate limit headers
        response['X-RateLimit-Limit-Minute'] = str(rate_limit_info['limit_per_minute'])
        response['X-RateLimit-Limit-Hour'] = str(rate_limit_info['limit_per_hour'])
        response['X-RateLimit-Remaining-Minute'] = str(rate_limit_info['remaining_minute'])
        response['X-RateLimit-Remaining-Hour'] = str(rate_limit_info['remaining_hour'])
        response['X-RateLimit-Reset-Minute'] = str(rate_limit_info['reset_minute'])
        response['X-RateLimit-Reset-Hour'] = str(rate_limit_info['reset_hour'])
        
        return response
    
    def get_identifier(self, request) -> str:
        """Get unique identifier for rate limiting"""
        # Use authenticated user ID if available
        if request.user.is_authenticated:
            return f"user_{request.user.id}"
        
        # Otherwise use IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        return f"ip_{ip}"

