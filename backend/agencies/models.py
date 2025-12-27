from django.db import models
from django.core.validators import MinValueValidator


class Agence(models.Model):
    """Agence model - Rental Agency"""
    nom_agence = models.CharField(max_length=255)
    siege_agence = models.TextField()
    num_contact = models.CharField(max_length=20)
    email_agence = models.EmailField(unique=True)
    nmbr_succursales = models.PositiveIntegerField(default=0)
    nmbr_flotte = models.PositiveIntegerField(default=0)
    logo_agence = models.ImageField(upload_to='agencies/logos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agences'
        verbose_name = 'Agence'
        verbose_name_plural = 'Agences'
    
    def __str__(self):
        return self.nom_agence


class DemandePartenariat(models.Model):
    """Demande de partenariat model - Partnership Request"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Rejetée'),
    ]
    
    # Propriétaire information
    nom_prop = models.CharField(max_length=255)
    prenom_prop = models.CharField(max_length=255)
    ddn_prop = models.DateField()
    email_prop = models.EmailField()
    phone_prop = models.CharField(max_length=20)
    password = models.TextField()  # Will be hashed on approval
    
    # Agence information
    nom_agence = models.CharField(max_length=255)
    siege_agence = models.TextField()
    logo_agence = models.ImageField(upload_to='partnerships/logos/', null=True, blank=True)
    num_contact = models.CharField(max_length=20)
    email_agence = models.EmailField()
    nmbr_succursales = models.PositiveIntegerField(default=0)
    nmbr_flotte = models.PositiveIntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey('accounts.Administrateur', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'demandes_partenariat'
        verbose_name = 'Demande Partenariat'
        verbose_name_plural = 'Demandes Partenariat'
    
    def __str__(self):
        return f"Partnership: {self.nom_agence} - {self.get_status_display()}"


class DemandeCompteAdmin(models.Model):
    """Demande de compte administrateur model - Admin Account Request"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Rejetée'),
    ]
    
    nom_admin = models.CharField(max_length=255)
    prenom_admin = models.CharField(max_length=255)
    ddn_admin = models.DateField()
    email_admin = models.EmailField()
    phone_admin = models.CharField(max_length=20)
    password = models.TextField()  # Will be hashed on approval
    
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='demandes_admin')
    requested_by = models.ForeignKey('accounts.ProprietaireAgence', on_delete=models.CASCADE, related_name='demandes_admin')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey('accounts.Administrateur', on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'demandes_compte_admin'
        verbose_name = 'Demande Compte Admin'
        verbose_name_plural = 'Demandes Compte Admin'
    
    def __str__(self):
        return f"Admin Request: {self.email_admin} - {self.get_status_display()}"

