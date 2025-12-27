from django.db import models


class Reclamation(models.Model):
    """Réclamation model - Complaint"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('IN_PROGRESS', 'En cours'),
        ('RESOLVED', 'Résolue'),
        ('REJECTED', 'Rejetée'),
    ]
    
    contenu_reclamation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    locataire = models.ForeignKey('accounts.Locataire', on_delete=models.CASCADE, related_name='reclamations')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='reclamations')
    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.SET_NULL, null=True, blank=True, related_name='reclamations')
    
    traite_par = models.ForeignKey('accounts.ProprietaireAgence', on_delete=models.SET_NULL, null=True, blank=True, related_name='reclamations_traitees')
    traite_at = models.DateTimeField(null=True, blank=True)
    reponse = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reclamations'
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Réclamations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reclamation {self.id} - {self.locataire.user.email}"


class Rapport(models.Model):
    """Rapport model - Report (for accidents/issues)"""
    TYPE_CHOICES = [
        ('ACCIDENT', 'Accident'),
        ('PANNE', 'Panne'),
        ('AUTRE', 'Autre problème'),
    ]
    
    description = models.TextField()
    type_rapport = models.CharField(max_length=20, choices=TYPE_CHOICES, default='AUTRE')
    images = models.JSONField(default=list, blank=True)  # Array of image URLs
    
    locataire = models.ForeignKey('accounts.Locataire', on_delete=models.CASCADE, related_name='rapports')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='rapports')
    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, related_name='rapports')
    vehicule = models.ForeignKey('vehicles.Vehicule', on_delete=models.CASCADE, related_name='rapports')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rapports'
        verbose_name = 'Rapport'
        verbose_name_plural = 'Rapports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rapport {self.id} - {self.get_type_rapport_display()}"


class EtatVehicule(models.Model):
    """État véhicule model - Vehicle State Report (by mechanic)"""
    ETAT_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('BON', 'Bon'),
        ('MOYEN', 'Moyen'),
        ('MAUVAIS', 'Mauvais'),
        ('CRITIQUE', 'Critique'),
    ]
    
    etat_general = models.CharField(max_length=20, choices=ETAT_CHOICES)
    description = models.TextField()
    kilometrage = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    vehicule = models.ForeignKey('vehicles.Vehicule', on_delete=models.CASCADE, related_name='etats')
    garagiste = models.ForeignKey('accounts.Garagiste', on_delete=models.CASCADE, related_name='etats_vehicules')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'etats_vehicule'
        verbose_name = 'État Véhicule'
        verbose_name_plural = 'États Véhicule'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"État {self.vehicule.matricule} - {self.get_etat_general_display()}"

