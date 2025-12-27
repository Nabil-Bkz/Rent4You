from django.contrib import admin
from .models import Reclamation, Rapport, EtatVehicule


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('id', 'locataire', 'agence', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'agence')
    search_fields = ('locataire__user__email',)


@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_rapport', 'locataire', 'vehicule', 'created_at')
    list_filter = ('type_rapport', 'created_at')
    search_fields = ('locataire__user__email', 'vehicule__matricule')


@admin.register(EtatVehicule)
class EtatVehiculeAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicule', 'etat_general', 'garagiste', 'created_at')
    list_filter = ('etat_general', 'created_at')
    search_fields = ('vehicule__matricule',)

