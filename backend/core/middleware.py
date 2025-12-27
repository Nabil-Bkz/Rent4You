import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware for logging API requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log request
        logger.info(f"{request.method} {request.path} - User: {getattr(request.user, 'email', 'Anonymous')}")
        
        response = self.get_response(request)
        
        # Log response
        logger.info(f"Response: {response.status_code}")
        
        return response

