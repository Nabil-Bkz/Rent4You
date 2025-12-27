from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Agence, DemandePartenariat, DemandeCompteAdmin
from .serializers import AgenceSerializer, DemandePartenariatSerializer, DemandeCompteAdminSerializer
from accounts.models import User, ProprietaireAgence, AdminAgence
from core.permissions import IsAdministrateur, IsProprietaireAgence, IsAdminAgence


class AgenceViewSet(viewsets.ModelViewSet):
    """Agence ViewSet"""
    queryset = Agence.objects.all()
    serializer_class = AgenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdministrateur()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active agencies"""
        agencies = Agence.objects.filter(is_active=True)
        serializer = self.get_serializer(agencies, many=True)
        return Response(serializer.data)


class DemandePartenariatViewSet(viewsets.ModelViewSet):
    """Demande partenariat ViewSet"""
    queryset = DemandePartenariat.objects.all()
    serializer_class = DemandePartenariatSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated()]  # Anyone can create partnership request
        return [IsAdministrateur()]  # Only admin can view/approve/reject
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrateur])
    def approve(self, request, pk=None):
        """Approve partnership request"""
        demande = self.get_object()
        if demande.status != 'PENDING':
            return Response(
                {"error": "This request has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user for owner
        user = User.objects.create_user(
            email=demande.email_prop,
            username=demande.email_prop,
            first_name=demande.prenom_prop,
            last_name=demande.nom_prop,
            phone=demande.phone_prop,
            date_of_birth=demande.ddn_prop,
            role='OWNER',
            password=make_password(demande.password)
        )
        
        # Create agency
        agence = Agence.objects.create(
            nom_agence=demande.nom_agence,
            siege_agence=demande.siege_agence,
            num_contact=demande.num_contact,
            email_agence=demande.email_agence,
            nmbr_succursales=demande.nmbr_succursales,
            nmbr_flotte=demande.nmbr_flotte,
            logo_agence=demande.logo_agence
        )
        
        # Create owner profile
        ProprietaireAgence.objects.create(user=user, agence=agence)
        
        # Update demande
        demande.status = 'APPROVED'
        demande.reviewed_by = request.user.administrateur
        demande.reviewed_at = timezone.now()
        demande.save()
        
        # Send email notification
        try:
            EmailService.send_partnership_approved(
                demande,
                user.email
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email: {str(e)}")
        
        # Send welcome email
        try:
            EmailService.send_welcome_email(
                user.email,
                f"{user.first_name} {user.last_name}"
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send welcome email: {str(e)}")
        
        return Response({"message": "Partnership request approved successfully."})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrateur])
    def reject(self, request, pk=None):
        """Reject partnership request"""
        demande = self.get_object()
        if demande.status != 'PENDING':
            return Response(
                {"error": "This request has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        demande.status = 'REJECTED'
        demande.reviewed_by = request.user.administrateur
        demande.reviewed_at = timezone.now()
        demande.save()
        
        return Response({"message": "Partnership request rejected."})


class DemandeCompteAdminViewSet(viewsets.ModelViewSet):
    """Demande compte admin ViewSet"""
    queryset = DemandeCompteAdmin.objects.all()
    serializer_class = DemandeCompteAdminSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsProprietaireAgence()]
        return [IsAdministrateur()]
    
    def perform_create(self, serializer):
        # Get owner's agency
        owner = self.request.user.proprietaire_agence
        serializer.save(requested_by=owner, agence=owner.agence)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrateur])
    def approve(self, request, pk=None):
        """Approve admin account request"""
        demande = self.get_object()
        if demande.status != 'PENDING':
            return Response(
                {"error": "This request has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            email=demande.email_admin,
            username=demande.email_admin,
            first_name=demande.prenom_admin,
            last_name=demande.nom_admin,
            phone=demande.phone_admin,
            date_of_birth=demande.ddn_admin,
            role='AGENCY_ADMIN',
            password=make_password(demande.password)
        )
        
        # Create admin profile
        AdminAgence.objects.create(user=user, agence=demande.agence)
        
        # Update demande
        demande.status = 'APPROVED'
        demande.reviewed_by = request.user.administrateur
        demande.reviewed_at = timezone.now()
        demande.save()
        
        return Response({"message": "Admin account request approved successfully."})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrateur])
    def reject(self, request, pk=None):
        """Reject admin account request"""
        demande = self.get_object()
        if demande.status != 'PENDING':
            return Response(
                {"error": "This request has already been processed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        demande.status = 'REJECTED'
        demande.reviewed_by = request.user.administrateur
        demande.reviewed_at = timezone.now()
        demande.save()
        
        return Response({"message": "Admin account request rejected."})

