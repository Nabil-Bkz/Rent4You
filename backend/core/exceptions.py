"""
Custom exceptions for the application
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):
    """Base exception for all API exceptions"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code:
            self.status_code = status_code
        super().__init__(detail, code)


class ValidationError(BaseAPIException):
    """Custom validation error"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Validation error occurred.'


class NotFoundError(BaseAPIException):
    """Resource not found error"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'


class PermissionDeniedError(BaseAPIException):
    """Permission denied error"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'


class UnauthorizedError(BaseAPIException):
    """Unauthorized error"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication credentials were not provided.'


class BusinessLogicError(BaseAPIException):
    """Business logic violation error"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Business logic violation.'


class VehicleHasActiveReservationsError(BusinessLogicError):
    """Vehicle has active reservations error"""
    default_detail = 'Cannot modify price for a vehicle with active reservations.'


class InvalidCredentialsError(UnauthorizedError):
    """Invalid credentials error"""
    default_detail = 'Invalid credentials.'


class UserDisabledError(UnauthorizedError):
    """User account disabled error"""
    default_detail = 'User account is disabled.'

