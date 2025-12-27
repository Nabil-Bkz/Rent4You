"""
In-app notification system
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    """In-app notification model"""
    TYPE_CHOICES = [
        ('RESERVATION_CONFIRMED', 'Réservation confirmée'),
        ('RESERVATION_CANCELLED', 'Réservation annulée'),
        ('CONTRACT_READY', 'Contrat prêt'),
        ('COMPLAINT_RECEIVED', 'Réclamation reçue'),
        ('COMPLAINT_RESOLVED', 'Réclamation résolue'),
        ('PAYMENT_RECEIVED', 'Paiement reçu'),
        ('VEHICLE_AVAILABLE', 'Véhicule disponible'),
        ('SYSTEM', 'Système'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_object_type = models.CharField(max_length=50, null=True, blank=True)  # e.g., 'reservation', 'contract'
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class NotificationService:
    """Service for creating and managing notifications"""
    
    @staticmethod
    def create_notification(
        user: User,
        notification_type: str,
        title: str,
        message: str,
        related_object_type: str = None,
        related_object_id: int = None
    ) -> Notification:
        """
        Create a new notification
        
        Args:
            user: User to notify
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            related_object_type: Type of related object
            related_object_id: ID of related object
            
        Returns:
            Created notification
        """
        return Notification.objects.create(
            user=user,
            type=notification_type,
            title=title,
            message=message,
            related_object_type=related_object_type,
            related_object_id=related_object_id
        )
    
    @staticmethod
    def notify_reservation_confirmed(reservation) -> Notification:
        """Create notification for reservation confirmation"""
        return NotificationService.create_notification(
            user=reservation.locataire.user,
            notification_type='RESERVATION_CONFIRMED',
            title='Réservation confirmée',
            message=f'Votre réservation #{reservation.id} a été confirmée.',
            related_object_type='reservation',
            related_object_id=reservation.id
        )
    
    @staticmethod
    def notify_reservation_cancelled(reservation) -> Notification:
        """Create notification for reservation cancellation"""
        return NotificationService.create_notification(
            user=reservation.locataire.user,
            notification_type='RESERVATION_CANCELLED',
            title='Réservation annulée',
            message=f'Votre réservation #{reservation.id} a été annulée.',
            related_object_type='reservation',
            related_object_id=reservation.id
        )
    
    @staticmethod
    def notify_contract_ready(contract) -> Notification:
        """Create notification for contract ready"""
        return NotificationService.create_notification(
            user=contract.reservation.locataire.user,
            notification_type='CONTRACT_READY',
            title='Contrat prêt à signer',
            message=f'Votre contrat pour la réservation #{contract.reservation.id} est prêt à être signé.',
            related_object_type='contract',
            related_object_id=contract.id
        )
    
    @staticmethod
    def notify_complaint_received(complaint) -> Notification:
        """Create notification for complaint received"""
        # Notify agency owner
        if complaint.agence.proprietaires.exists():
            owner = complaint.agence.proprietaires.first().user
            return NotificationService.create_notification(
                user=owner,
                notification_type='COMPLAINT_RECEIVED',
                title='Nouvelle réclamation',
                message=f'Une nouvelle réclamation #{complaint.id} a été reçue.',
                related_object_type='complaint',
                related_object_id=complaint.id
            )
        return None
    
    @staticmethod
    def notify_complaint_resolved(complaint) -> Notification:
        """Create notification for complaint resolved"""
        return NotificationService.create_notification(
            user=complaint.locataire.user,
            notification_type='COMPLAINT_RESOLVED',
            title='Réclamation résolue',
            message=f'Votre réclamation #{complaint.id} a été résolue.',
            related_object_type='complaint',
            related_object_id=complaint.id
        )
    
    @staticmethod
    def get_user_notifications(user: User, unread_only: bool = False, limit: int = None):
        """Get notifications for a user"""
        notifications = Notification.objects.filter(user=user)
        if unread_only:
            notifications = notifications.filter(is_read=False)
        if limit:
            notifications = notifications[:limit]
        return notifications
    
    @staticmethod
    def mark_all_as_read(user: User) -> int:
        """Mark all notifications as read for a user"""
        return Notification.objects.filter(user=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
    
    @staticmethod
    def get_unread_count(user: User) -> int:
        """Get count of unread notifications"""
        return Notification.objects.filter(user=user, is_read=False).count()

