from django.contrib import admin
from .models import Agence, DemandePartenariat, DemandeCompteAdmin


@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    list_display = ('nom_agence', 'email_agence', 'nmbr_flotte', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('nom_agence', 'email_agence')


@admin.register(DemandePartenariat)
class DemandePartenariatAdmin(admin.ModelAdmin):
    list_display = ('nom_agence', 'email_prop', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('nom_agence', 'email_prop', 'email_agence')


@admin.register(DemandeCompteAdmin)
class DemandeCompteAdminAdmin(admin.ModelAdmin):
    list_display = ('email_admin', 'agence', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'agence')
    search_fields = ('email_admin', 'nom_admin', 'prenom_admin')

