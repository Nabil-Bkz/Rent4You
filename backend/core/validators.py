"""
Advanced validation utilities
"""
import re
from typing import Optional, Tuple
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class AdvancedValidators:
    """Advanced validation functions"""
    
    @staticmethod
    def validate_phone_number(phone: str) -> Tuple[bool, Optional[str]]:
        """
        Validate phone number (international format)
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Remove spaces and dashes
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # International format: + followed by 1-15 digits
        pattern = r'^\+?[1-9]\d{1,14}$'
        
        if not re.match(pattern, phone):
            return False, "Numéro de téléphone invalide. Format attendu: +212XXXXXXXXX"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email address
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "Adresse email invalide"
        
        return True, None
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        if len(password) < 8:
            errors.append("au moins 8 caractères")
        
        if not re.search(r'[A-Z]', password):
            errors.append("au moins une majuscule")
        
        if not re.search(r'[a-z]', password):
            errors.append("au moins une minuscule")
        
        if not re.search(r'\d', password):
            errors.append("au moins un chiffre")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("au moins un caractère spécial")
        
        if errors:
            return False, f"Le mot de passe doit contenir: {', '.join(errors)}"
        
        return True, None
    
    @staticmethod
    def validate_date_range(start_date, end_date) -> Tuple[bool, Optional[str]]:
        """
        Validate date range
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if start_date >= end_date:
            return False, "La date de fin doit être postérieure à la date de début"
        
        return True, None
    
    @staticmethod
    def validate_price(price: float, min_price: float = 0) -> Tuple[bool, Optional[str]]:
        """
        Validate price
        
        Args:
            price: Price to validate
            min_price: Minimum price
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if price < min_price:
            return False, f"Le prix doit être supérieur ou égal à {min_price}"
        
        if price > 1000000:  # Reasonable max
            return False, "Le prix est trop élevé"
        
        return True, None
    
    @staticmethod
    def validate_matricule(matricule: str) -> Tuple[bool, Optional[str]]:
        """
        Validate vehicle license plate (Moroccan format)
        
        Args:
            matricule: License plate to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Moroccan format: 12345-A-12 or similar
        pattern = r'^[0-9]{1,5}-[A-Z]{1,2}-[0-9]{1,3}$'
        
        if not re.match(pattern, matricule):
            return False, "Format de matricule invalide. Format attendu: 12345-A-12"
        
        return True, None


class CustomDjangoValidator:
    """Django-compatible validators"""
    
    @staticmethod
    def phone_validator(value: str):
        """Django validator for phone number"""
        is_valid, error = AdvancedValidators.validate_phone_number(value)
        if not is_valid:
            raise ValidationError(error)
    
    @staticmethod
    def password_validator(value: str):
        """Django validator for password strength"""
        is_valid, error = AdvancedValidators.validate_password_strength(value)
        if not is_valid:
            raise ValidationError(error)
    
    @staticmethod
    def matricule_validator(value: str):
        """Django validator for license plate"""
        is_valid, error = AdvancedValidators.validate_matricule(value)
        if not is_valid:
            raise ValidationError(error)

