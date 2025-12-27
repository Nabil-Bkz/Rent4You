from django.contrib import admin
from .models import User, Administrateur, ProprietaireAgence, SecretaireAgence, Garagiste, Locataire, AdminAgence


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')


@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(ProprietaireAgence)
class ProprietaireAgenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'agence')


@admin.register(SecretaireAgence)
class SecretaireAgenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'agence')


@admin.register(Garagiste)
class GaragisteAdmin(admin.ModelAdmin):
    list_display = ('user', 'agence')


@admin.register(Locataire)
class LocataireAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_banned')
    filter_horizontal = ('banned_from_agencies',)


@admin.register(AdminAgence)
class AdminAgenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'agence')

