from django.db import models
from django.core.validators import MinValueValidator


class Depot(models.Model):
    """Dépôt model - Vehicle Depot/Storage"""
    adress_dpt = models.TextField()
    capacite_dpt = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='depots')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'depots'
        verbose_name = 'Dépôt'
        verbose_name_plural = 'Dépôts'
    
    def __str__(self):
        return f"{self.adress_dpt} ({self.agence.nom_agence})"


class Vehicule(models.Model):
    """Véhicule model - Vehicle"""
    ETAT_CHOICES = [
        ('intrusion', 'Intrusion'),
        ('enPanne', 'En Panne'),
        ('prochainementDisponible', 'Prochainement Disponible'),
        ('enMarche', 'En Marche'),
        ('enArret', 'En Arrêt'),
    ]
    
    CATEGORIE_CHOICES = [
        ('Petites', 'Petites'),
        ('Moyennes', 'Moyennes'),
        ('Larges', 'Larges'),
        ('Premium', 'Premium'),
        ('Monospaces', 'Monospaces'),
        ('SUV', 'SUV'),
    ]
    
    matricule = models.CharField(max_length=50, unique=True)
    marque = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    prix_heure = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    prix_jour = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    etat_vehicule = models.CharField(max_length=50, choices=ETAT_CHOICES, default='enMarche')
    disponibilite = models.BooleanField(default=True)
    categorie_vehicule = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT, related_name='vehicules', null=True, blank=True)
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='vehicules')
    img_vhl = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vehicules'
        verbose_name = 'Véhicule'
        verbose_name_plural = 'Véhicules'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.marque} {self.model} ({self.matricule})"
    
    @property
    def imageURL(self):
        try:
            url = self.img_vhl.url
        except:
            url = ''
        return url


class PrixHistorique(models.Model):
    """Prix Historique model - Price History for vehicles"""
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='prix_history')
    ancien_prix_jour = models.DecimalField(max_digits=10, decimal_places=2)
    nouveau_prix_jour = models.DecimalField(max_digits=10, decimal_places=2)
    ancien_prix_heure = models.DecimalField(max_digits=10, decimal_places=2)
    nouveau_prix_heure = models.DecimalField(max_digits=10, decimal_places=2)
    modifie_par = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prix_historique'
        verbose_name = 'Prix Historique'
        verbose_name_plural = 'Prix Historiques'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Price change for {self.vehicule.matricule}"

