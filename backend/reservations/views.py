from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Reservation
from .serializers import ReservationSerializer
from core.permissions import IsLocataire, IsSecretaireAgence, IsAgencyStaff
from core.response import APIResponse
from core.email_service import EmailService
from core.notifications import NotificationService


class ReservationViewSet(viewsets.ModelViewSet):
    """Reservation ViewSet"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsLocataire()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsSecretaireAgence() | IsLocataire()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Locataires can only see their own reservations
        if hasattr(self.request.user, 'locataire'):
            queryset = queryset.filter(locataire=self.request.user.locataire)
        
        # Agency staff can see reservations for their agency's vehicles
        elif hasattr(self.request.user, 'proprietaire_agence'):
            agence = self.request.user.proprietaire_agence.agence
            queryset = queryset.filter(vehicule__agence=agence)
        elif hasattr(self.request.user, 'secretaire_agence'):
            agence = self.request.user.secretaire_agence.agence
            queryset = queryset.filter(vehicule__agence=agence)
        elif hasattr(self.request.user, 'admin_agence'):
            agence = self.request.user.admin_agence.agence
            queryset = queryset.filter(vehicule__agence=agence)
        
        return queryset
    
    def perform_create(self, serializer):
        # Ensure user is a locataire
        if not hasattr(self.request.user, 'locataire'):
            return Response(
                {"error": "Only renters can create reservations."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reservation = serializer.save(locataire=self.request.user.locataire)
        
        # Create in-app notification for pending reservation
        try:
            NotificationService.create_notification(
                user=reservation.locataire.user,
                notification_type='RESERVATION_CONFIRMED',
                title='Réservation créée',
                message=f'Votre réservation #{reservation.id} a été créée et est en attente de confirmation.',
                related_object_type='reservation',
                related_object_id=reservation.id
            )
        except Exception as e:
            # Log error but don't fail the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
    
    @action(detail=True, methods=['post'], permission_classes=[IsSecretaireAgence])
    def confirm(self, request, pk=None):
        """Confirm a reservation"""
        reservation = self.get_object()
        if reservation.status != 'PENDING':
            return APIResponse.error(
                message="Only pending reservations can be confirmed.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'CONFIRMED'
        reservation.save()
        
        # Send email notification
        try:
            EmailService.send_reservation_confirmation(
                reservation,
                reservation.locataire.user.email
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email: {str(e)}")
        
        # Create in-app notification
        try:
            NotificationService.notify_reservation_confirmed(reservation)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
        
        return APIResponse.success(
            data=ReservationSerializer(reservation).data,
            message="Reservation confirmed successfully."
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsLocataire | IsSecretaireAgence])
    def cancel(self, request, pk=None):
        """Cancel a reservation"""
        reservation = self.get_object()
        if reservation.status in ['COMPLETED', 'CANCELLED']:
            return APIResponse.error(
                message="Cannot cancel a completed or already cancelled reservation.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        reservation.status = 'CANCELLED'
        reservation.save()
        
        # Send email notification
        try:
            EmailService.send_reservation_cancellation(
                reservation,
                reservation.locataire.user.email
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send email: {str(e)}")
        
        # Create in-app notification
        try:
            NotificationService.notify_reservation_cancelled(reservation)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create notification: {str(e)}")
        
        return APIResponse.success(
            data=ReservationSerializer(reservation).data,
            message="Reservation cancelled successfully."
        )
    
    @action(detail=True, methods=['get'], permission_classes=[IsLocataire])
    def invoice(self, request, pk=None):
        """Get invoice for a reservation"""
        reservation = self.get_object()
        
        # Calculate invoice details
        # The prix field already includes the final price after promo discount
        rental_price = float(reservation.prix_original) if reservation.prix_original else float(reservation.prix)
        promo_discount = float(reservation.reduction) if reservation.reduction else 0.0
        # Agency fee is typically a percentage (e.g., 10%) of rental price
        # For now, we'll use 0 or calculate based on a standard rate
        agency_fee_percentage = 0.10  # 10% agency fee
        agency_fee = rental_price * agency_fee_percentage
        subtotal = rental_price - promo_discount
        total = subtotal + agency_fee
        
        invoice_data = {
            'reservation_id': reservation.id,
            'vehicle': {
                'matricule': reservation.vehicule.matricule,
                'marque': reservation.vehicule.marque,
                'model': reservation.vehicule.model,
            },
            'agency': {
                'nom': reservation.vehicule.agence.nom_agence,
                'email': reservation.vehicule.agence.email_agence,
            },
            'renter': {
                'name': f"{reservation.locataire.user.first_name} {reservation.locataire.user.last_name}",
                'email': reservation.locataire.user.email,
            },
            'dates': {
                'start': reservation.date_debut.isoformat(),
                'end': reservation.date_fin.isoformat(),
            },
            'pricing': {
                'rental_price': rental_price,
                'agency_fee': round(agency_fee, 2),
                'promo_discount': promo_discount,
                'subtotal': round(subtotal, 2),
                'total': round(total, 2),
            },
            'promo_code': reservation.code_promo.code if reservation.code_promo else None,
            'created_at': reservation.created_at.isoformat(),
        }
        
        return APIResponse.success(
            data=invoice_data,
            message="Invoice retrieved successfully."
        )

