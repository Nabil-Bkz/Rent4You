from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Locataire
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserUpdateSerializer,
    PasswordChangeSerializer, LocataireSerializer
)
from core.permissions import IsAdministrateur, IsProprietaireAgence, IsSecretaireAgence
from core.response import APIResponse
from core.constants import SuccessMessages
from .services import AuthService, UserService


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet for CRUD operations"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrateur]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        try:
            result = UserService.get_user_profile(request.user)
            return APIResponse.success(data=result)
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        try:
            result = UserService.update_user_profile(request.user, request.data)
            return APIResponse.success(
                data=result,
                message=SuccessMessages.PROFILE_UPDATED
            )
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        try:
            serializer = PasswordChangeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            AuthService.change_password(
                request.user,
                serializer.validated_data['old_password'],
                serializer.validated_data['new_password']
            )
            
            return APIResponse.success(message=SuccessMessages.PASSWORD_UPDATED)
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class RegisterView(generics.CreateAPIView):
    """User registration view"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            result = AuthService.register(request.data)
            
            # Send welcome email
            try:
                from core.email_service import EmailService
                user_data = result.get('user', {})
                EmailService.send_welcome_email(
                    user_data.get('email', ''),
                    user_data.get('username', 'User')
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send welcome email: {str(e)}")
            
            return APIResponse.created(
                data=result,
                message="User registered successfully."
            )
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """User login view"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            result = AuthService.login(email, password)
            return APIResponse.success(
                data=result,
                message="Login successful."
            )
        except Exception as e:
            status_code = getattr(e, 'status_code', status.HTTP_400_BAD_REQUEST)
            return APIResponse.error(
                message=str(e),
                status_code=status_code
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class LocataireViewSet(viewsets.ReadOnlyModelViewSet):
    """Locataire ViewSet for viewing and managing tenants"""
    queryset = Locataire.objects.all()
    serializer_class = LocataireSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['ban', 'unban', 'ban_from_agency', 'unban_from_agency']:
            return [IsProprietaireAgence() | IsSecretaireAgence()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Agency staff can only see tenants related to their agency
        if hasattr(self.request.user, 'proprietaire_agence'):
            agence = self.request.user.proprietaire_agence.agence
            # Get tenants who have reservations with this agency's vehicles
            from reservations.models import Reservation
            tenant_ids = Reservation.objects.filter(
                vehicule__agence=agence
            ).values_list('locataire_id', flat=True).distinct()
            queryset = queryset.filter(id__in=tenant_ids)
        elif hasattr(self.request.user, 'secretaire_agence'):
            agence = self.request.user.secretaire_agence.agence
            from reservations.models import Reservation
            tenant_ids = Reservation.objects.filter(
                vehicule__agence=agence
            ).values_list('locataire_id', flat=True).distinct()
            queryset = queryset.filter(id__in=tenant_ids)
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence | IsSecretaireAgence])
    def ban(self, request, pk=None):
        """Ban a tenant globally"""
        locataire = self.get_object()
        locataire.is_banned = True
        locataire.save()
        
        return APIResponse.success(
            message=f"Tenant {locataire.user.email} has been banned."
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence | IsSecretaireAgence])
    def unban(self, request, pk=None):
        """Unban a tenant globally"""
        locataire = self.get_object()
        locataire.is_banned = False
        locataire.save()
        
        return APIResponse.success(
            message=f"Tenant {locataire.user.email} has been unbanned."
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence | IsSecretaireAgence])
    def ban_from_agency(self, request, pk=None):
        """Ban a tenant from a specific agency"""
        locataire = self.get_object()
        
        # Get agency from user
        if hasattr(request.user, 'proprietaire_agence'):
            agence = request.user.proprietaire_agence.agence
        elif hasattr(request.user, 'secretaire_agence'):
            agence = request.user.secretaire_agence.agence
        else:
            return APIResponse.error(
                message="You must be agency staff to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        locataire.banned_from_agencies.add(agence)
        
        return APIResponse.success(
            message=f"Tenant {locataire.user.email} has been banned from {agence.nom_agence}."
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence | IsSecretaireAgence])
    def unban_from_agency(self, request, pk=None):
        """Unban a tenant from a specific agency"""
        locataire = self.get_object()
        
        # Get agency from user
        if hasattr(request.user, 'proprietaire_agence'):
            agence = request.user.proprietaire_agence.agence
        elif hasattr(request.user, 'secretaire_agence'):
            agence = request.user.secretaire_agence.agence
        else:
            return APIResponse.error(
                message="You must be agency staff to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        locataire.banned_from_agencies.remove(agence)
        
        return APIResponse.success(
            message=f"Tenant {locataire.user.email} has been unbanned from {agence.nom_agence}."
        )

