from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import ContratLocation
from .serializers import ContratLocationSerializer
from core.permissions import IsSecretaireAgence, IsLocataire
from core.response import APIResponse
from core.email_service import EmailService
from core.notifications import NotificationService


class ContratLocationViewSet(viewsets.ModelViewSet):
    """Contrat location ViewSet"""
    queryset = ContratLocation.objects.all()
    serializer_class = ContratLocationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsSecretaireAgence()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create contract and send notifications"""
        contract = serializer.save()
        
        # Send email notification
        try:
            EmailService.send_contract_ready(
                contract,
                contract.reservation.locataire.user.email
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email: {str(e)}")
        
        # Create in-app notification
        try:
            NotificationService.notify_contract_ready(contract)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
    
    @action(detail=True, methods=['post'], permission_classes=[IsLocataire])
    def sign(self, request, pk=None):
        """Sign contract"""
        contrat = self.get_object()
        signature = request.data.get('signature')
        
        if not signature:
            return APIResponse.error(
                message="Signature is required.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        contrat.signature_locataire = signature
        contrat.status = 'SIGNED'
        contrat.signed_at = timezone.now()
        contrat.save()
        
        return APIResponse.success(
            data=ContratLocationSerializer(contrat).data,
            message="Contract signed successfully."
        )

