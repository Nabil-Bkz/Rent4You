"""
Utility functions for the application
"""
from typing import Optional, Dict, Any
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .constants import UserRoles

User = get_user_model()


def get_tokens_for_user(user) -> Dict[str, str]:
    """
    Generate JWT tokens for a user
    
    Args:
        user: User instance
        
    Returns:
        Dictionary with 'access' and 'refresh' tokens
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_role_profile(user) -> Optional[Dict[str, Any]]:
    """
    Get role-specific profile data for a user
    
    Args:
        user: User instance
        
    Returns:
        Dictionary with profile data or None
    """
    if hasattr(user, 'administrateur'):
        from accounts.serializers import AdministrateurSerializer
        return AdministrateurSerializer(user.administrateur).data
    elif hasattr(user, 'proprietaire_agence'):
        from accounts.serializers import ProprietaireAgenceSerializer
        return ProprietaireAgenceSerializer(user.proprietaire_agence).data
    elif hasattr(user, 'secretaire_agence'):
        from accounts.serializers import SecretaireAgenceSerializer
        return SecretaireAgenceSerializer(user.secretaire_agence).data
    elif hasattr(user, 'garagiste'):
        from accounts.serializers import GaragisteSerializer
        return GaragisteSerializer(user.garagiste).data
    elif hasattr(user, 'locataire'):
        from accounts.serializers import LocataireSerializer
        return LocataireSerializer(user.locataire).data
    elif hasattr(user, 'admin_agence'):
        from accounts.serializers import AdminAgenceSerializer
        return AdminAgenceSerializer(user.admin_agence).data
    return None


def get_user_agency(user):
    """
    Get the agency associated with a user (if any)
    
    Args:
        user: User instance
        
    Returns:
        Agency instance or None
    """
    if hasattr(user, 'proprietaire_agence') and user.proprietaire_agence.agence:
        return user.proprietaire_agence.agence
    elif hasattr(user, 'secretaire_agence') and user.secretaire_agence.agence:
        return user.secretaire_agence.agence
    elif hasattr(user, 'admin_agence') and user.admin_agence.agence:
        return user.admin_agence.agence
    elif hasattr(user, 'garagiste') and user.garagiste.agence:
        return user.garagiste.agence
    return None


def is_agency_staff(user) -> bool:
    """
    Check if user is any type of agency staff
    
    Args:
        user: User instance
        
    Returns:
        True if user is agency staff, False otherwise
    """
    return (
        hasattr(user, 'proprietaire_agence') or
        hasattr(user, 'secretaire_agence') or
        hasattr(user, 'admin_agence') or
        hasattr(user, 'garagiste')
    )


def calculate_reservation_price(vehicule, date_debut, date_fin, code_promo=None) -> Dict[str, Any]:
    """
    Calculate reservation price based on dates and promo code
    
    Args:
        vehicule: Vehicle instance
        date_debut: Start date
        date_fin: End date
        code_promo: Optional promo code
        
    Returns:
        Dictionary with prix, prix_original, and reduction
    """
    from datetime import timedelta
    
    days = (date_fin - date_debut).days + 1
    prix_original = float(vehicule.prix_jour) * days
    
    reduction = 0
    if code_promo and code_promo.is_valid():
        reduction = (prix_original * code_promo.discount_percentage) / 100
    
    prix = prix_original - reduction
    
    return {
        'prix': prix,
        'prix_original': prix_original,
        'reduction': reduction,
    }

