from rest_framework import permissions


class IsAdministrateur(permissions.BasePermission):
    """Permission check for Administrateur role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'administrateur')
        )


class IsProprietaireAgence(permissions.BasePermission):
    """Permission check for Propriétaire Agence role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'proprietaire_agence')
        )


class IsSecretaireAgence(permissions.BasePermission):
    """Permission check for Secrétaire Agence role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'secretaire_agence')
        )


class IsGaragiste(permissions.BasePermission):
    """Permission check for Garagiste role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'garagiste')
        )


class IsLocataire(permissions.BasePermission):
    """Permission check for Locataire role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'locataire')
        )


class IsAdminAgence(permissions.BasePermission):
    """Permission check for Admin Agence role"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'admin_agence')
        )


class IsAgencyStaff(permissions.BasePermission):
    """Permission check for any agency staff (Owner, Secretary, Admin, Mechanic)"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            hasattr(request.user, 'proprietaire_agence') or
            hasattr(request.user, 'secretaire_agence') or
            hasattr(request.user, 'admin_agence') or
            hasattr(request.user, 'garagiste')
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission check: Owner can edit, others can only read"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

