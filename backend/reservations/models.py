from django.db import models
from django.core.validators import MinValueValidator


class Reservation(models.Model):
    """Réservation model - Reservation"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Terminée'),
        ('CANCELLED', 'Annulée'),
    ]
    
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    locataire = models.ForeignKey('accounts.Locataire', on_delete=models.CASCADE, related_name='reservations')
    vehicule = models.ForeignKey('vehicles.Vehicule', on_delete=models.CASCADE, related_name='reservations')
    
    code_promo = models.ForeignKey('promotions.CodePromo', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    prix_original = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reservations'
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reservation {self.id} - {self.locataire.user.email} - {self.vehicule.matricule}"
    
    def save(self, *args, **kwargs):
        if not self.prix_original:
            self.prix_original = self.prix
        if self.code_promo and self.code_promo.is_valid():
            self.reduction = (self.prix_original * self.code_promo.discount_percentage) / 100
            self.prix = self.prix_original - self.reduction
        super().save(*args, **kwargs)

