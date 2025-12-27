"""
Business logic services for accounts app
"""
from typing import Dict, Any, Optional
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import InvalidCredentialsError, UserDisabledError
from core.utils import get_tokens_for_user, get_user_role_profile
from core.response import APIResponse
from core.constants import ErrorMessages

User = get_user_model()


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def login(email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user and return tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user, profile, and tokens
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
            UserDisabledError: If user account is disabled
        """
        if not email or not password:
            raise InvalidCredentialsError(ErrorMessages.EMAIL_PASSWORD_REQUIRED)
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise InvalidCredentialsError(ErrorMessages.INVALID_CREDENTIALS)
        
        if not user.is_active:
            raise UserDisabledError(ErrorMessages.USER_DISABLED)
        
        tokens = get_tokens_for_user(user)
        profile = get_user_role_profile(user)
        
        from accounts.serializers import UserSerializer
        return {
            'user': UserSerializer(user).data,
            'profile': profile,
            'tokens': tokens,
        }
    
    @staticmethod
    def register(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Dictionary with user and tokens
        """
        from accounts.serializers import UserRegistrationSerializer, UserSerializer
        
        serializer = UserRegistrationSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        tokens = get_tokens_for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'tokens': tokens,
        }
    
    @staticmethod
    def change_password(user, old_password: str, new_password: str) -> None:
        """
        Change user password
        
        Args:
            user: User instance
            old_password: Current password
            new_password: New password
            
        Raises:
            ValidationError: If old password is incorrect
        """
        if not user.check_password(old_password):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"old_password": "Wrong password."})
        
        user.set_password(new_password)
        user.save()


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def get_user_profile(user) -> Dict[str, Any]:
        """
        Get user profile with role-specific data
        
        Args:
            user: User instance
            
        Returns:
            Dictionary with user profile data
        """
        from accounts.serializers import UserSerializer
        profile = get_user_role_profile(user)
        
        return {
            'user': UserSerializer(user).data,
            'profile': profile,
        }
    
    @staticmethod
    def update_user_profile(user, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            user: User instance
            data: Update data
            
        Returns:
            Updated user data
        """
        from accounts.serializers import UserUpdateSerializer
        
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data

