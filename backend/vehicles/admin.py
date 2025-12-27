from django.contrib import admin
from .models import Depot, Vehicule, PrixHistorique


@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ('adress_dpt', 'agence', 'capacite_dpt', 'is_active')
    list_filter = ('is_active', 'agence')
    search_fields = ('adress_dpt',)


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'marque', 'model', 'categorie_vehicule', 'etat_vehicule', 'disponibilite', 'agence')
    list_filter = ('categorie_vehicule', 'etat_vehicule', 'disponibilite', 'agence')
    search_fields = ('matricule', 'marque', 'model')


@admin.register(PrixHistorique)
class PrixHistoriqueAdmin(admin.ModelAdmin):
    list_display = ('vehicule', 'ancien_prix_jour', 'nouveau_prix_jour', 'modifie_par', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('vehicule__matricule',)

