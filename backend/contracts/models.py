from django.db import models


class ContratLocation(models.Model):
    """Contrat de location model - Rental Contract"""
    STATUS_CHOICES = [
        ('DRAFT', 'Brouillon'),
        ('PENDING_SIGNATURE', 'En attente de signature'),
        ('SIGNED', 'Signé'),
        ('CANCELLED', 'Annulé'),
    ]
    
    reservation = models.OneToOneField('reservations.Reservation', on_delete=models.CASCADE, related_name='contrat')
    pdf_file = models.FileField(upload_to='contracts/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    signed_at = models.DateTimeField(null=True, blank=True)
    signature_locataire = models.TextField(null=True, blank=True)  # Base64 signature image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contrats_location'
        verbose_name = 'Contrat Location'
        verbose_name_plural = 'Contrats Location'
    
    def __str__(self):
        return f"Contract for Reservation {self.reservation.id}"

