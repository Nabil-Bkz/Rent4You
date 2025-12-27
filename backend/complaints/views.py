from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Reclamation, Rapport, EtatVehicule
from .serializers import ReclamationSerializer, RapportSerializer, EtatVehiculeSerializer
from core.permissions import IsLocataire, IsProprietaireAgence, IsGaragiste
from core.response import APIResponse
from core.email_service import EmailService
from core.notifications import NotificationService
from core.file_service import FileService


class ReclamationViewSet(viewsets.ModelViewSet):
    """Reclamation ViewSet"""
    queryset = Reclamation.objects.all()
    serializer_class = ReclamationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsLocataire()]
        elif self.action in ['update', 'partial_update']:
            return [IsProprietaireAgence()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        complaint = serializer.save(locataire=self.request.user.locataire)
        
        # Send email notification to agency owner
        try:
            if complaint.agence.proprietaires.exists():
                owner = complaint.agence.proprietaires.first()
                EmailService.send_complaint_received(
                    complaint,
                    owner.user.email
                )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email: {str(e)}")
        
        # Create in-app notification
        try:
            NotificationService.notify_complaint_received(complaint)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence])
    def resolve(self, request, pk=None):
        """Resolve a complaint"""
        reclamation = self.get_object()
        reponse = request.data.get('reponse', '')
        
        reclamation.status = 'RESOLVED'
        reclamation.reponse = reponse
        reclamation.traite_par = request.user.proprietaire_agence
        reclamation.traite_at = timezone.now()
        reclamation.save()
        
        # Create in-app notification
        try:
            NotificationService.notify_complaint_resolved(reclamation)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
        
        return APIResponse.success(
            data=ReclamationSerializer(reclamation).data,
            message="Complaint resolved successfully."
        )


class RapportViewSet(viewsets.ModelViewSet):
    """Rapport ViewSet"""
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsLocataire]
    
    def create(self, request, *args, **kwargs):
        """Create report with image upload support"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        images = []
        
        # Handle image uploads if provided
        if 'images' in request.FILES:
            uploaded_files = request.FILES.getlist('images')
            for uploaded_file in uploaded_files:
                try:
                    file_path = FileService.upload_image(
                        uploaded_file,
                        upload_path='reports/',
                        prefix='report'
                    )
                    # Get full URL
                    if file_path:
                        images.append(request.build_absolute_uri(f'/media/{file_path}'))
                except ValueError as e:
                    # Log error but continue with other images
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to upload image: {str(e)}")
        
        # Save report with images
        report = serializer.save(locataire=request.user.locataire, images=images)
        
        headers = self.get_success_headers(serializer.data)
        return APIResponse.created(
            data=serializer.data,
            message="Report created successfully."
        )


class EtatVehiculeViewSet(viewsets.ModelViewSet):
    """Etat vehicule ViewSet"""
    queryset = EtatVehicule.objects.all()
    serializer_class = EtatVehiculeSerializer
    permission_classes = [IsGaragiste]
    
    def perform_create(self, serializer):
        serializer.save(garagiste=self.request.user.garagiste)

