from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'locataire', 'vehicule', 'date_debut', 'date_fin', 'status', 'prix', 'created_at')
    list_filter = ('status', 'date_debut', 'date_fin', 'created_at')
    search_fields = ('locataire__user__email', 'vehicule__matricule')
    date_hierarchy = 'created_at'

