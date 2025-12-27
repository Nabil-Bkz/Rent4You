"""
Standardized API response utilities
"""
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, Optional


class APIResponse:
    """Utility class for standardized API responses"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: Optional[str] = None,
        status_code: int = status.HTTP_200_OK
    ) -> Response:
        """
        Create a successful response
        
        Args:
            data: Response data
            message: Optional success message
            status_code: HTTP status code
            
        Returns:
            Response object
        """
        response_data: Dict[str, Any] = {
            'success': True,
        }
        
        if message:
            response_data['message'] = message
        
        if data is not None:
            response_data['data'] = data
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(
        message: str,
        errors: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """
        Create an error response
        
        Args:
            message: Error message
            errors: Optional detailed errors
            status_code: HTTP status code
            
        Returns:
            Response object
        """
        response_data: Dict[str, Any] = {
            'success': False,
            'message': message,
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(
        data: Any = None,
        message: Optional[str] = None
    ) -> Response:
        """
        Create a 201 Created response
        
        Args:
            data: Response data
            message: Optional success message
            
        Returns:
            Response object
        """
        return APIResponse.success(data=data, message=message, status_code=status.HTTP_201_CREATED)
    
    @staticmethod
    def not_found(message: str = "Resource not found.") -> Response:
        """
        Create a 404 Not Found response
        
        Args:
            message: Error message
            
        Returns:
            Response object
        """
        return APIResponse.error(message=message, status_code=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def forbidden(message: str = "You do not have permission to perform this action.") -> Response:
        """
        Create a 403 Forbidden response
        
        Args:
            message: Error message
            
        Returns:
            Response object
        """
        return APIResponse.error(message=message, status_code=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def unauthorized(message: str = "Authentication credentials were not provided.") -> Response:
        """
        Create a 401 Unauthorized response
        
        Args:
            message: Error message
            
        Returns:
            Response object
        """
        return APIResponse.error(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

