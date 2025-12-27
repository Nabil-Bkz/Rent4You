from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom User model extending AbstractUser"""
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('OWNER', 'Propriétaire Agence'),
        ('SECRETARY', 'Secrétaire Agence'),
        ('MECHANIC', 'Garagiste'),
        ('RENTER', 'Locataire'),
        ('AGENCY_ADMIN', 'Administrateur Agence'),
        ('VISITOR', 'Visiteur'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VISITOR')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class Administrateur(models.Model):
    """Administrateur model - System Administrator"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrateur')
    
    class Meta:
        db_table = 'administrateurs'
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'
    
    def __str__(self):
        return f"Admin: {self.user.email}"


class ProprietaireAgence(models.Model):
    """Propriétaire de l'agence model - Agency Owner"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='proprietaire_agence')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='proprietaires', null=True, blank=True)
    
    class Meta:
        db_table = 'proprietaires_agence'
        verbose_name = 'Propriétaire Agence'
        verbose_name_plural = 'Propriétaires Agence'
    
    def __str__(self):
        return f"Owner: {self.user.email}"


class SecretaireAgence(models.Model):
    """Secrétaire de l'agence model - Agency Secretary"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='secretaire_agence')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='secretaires', null=True, blank=True)
    
    class Meta:
        db_table = 'secretaires_agence'
        verbose_name = 'Secrétaire Agence'
        verbose_name_plural = 'Secrétaires Agence'
    
    def __str__(self):
        return f"Secretary: {self.user.email}"


class Garagiste(models.Model):
    """Garagiste model - Mechanic"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='garagiste')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='garagistes', null=True, blank=True)
    
    class Meta:
        db_table = 'garagistes'
        verbose_name = 'Garagiste'
        verbose_name_plural = 'Garagistes'
    
    def __str__(self):
        return f"Mechanic: {self.user.email}"


class Locataire(models.Model):
    """Locataire model - Renter/Tenant"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='locataire')
    is_banned = models.BooleanField(default=False)
    banned_from_agencies = models.ManyToManyField('agencies.Agence', related_name='banned_locataires', blank=True)
    
    class Meta:
        db_table = 'locataires'
        verbose_name = 'Locataire'
        verbose_name_plural = 'Locataires'
    
    def __str__(self):
        return f"Renter: {self.user.email}"


class AdminAgence(models.Model):
    """Administrateur de l'agence model - Agency Administrator"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_agence')
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='admins_agence', null=True, blank=True)
    
    class Meta:
        db_table = 'admins_agence'
        verbose_name = 'Admin Agence'
        verbose_name_plural = 'Admins Agence'
    
    def __str__(self):
        return f"Agency Admin: {self.user.email}"

