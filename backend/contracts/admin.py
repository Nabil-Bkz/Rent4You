from django.contrib import admin
from .models import ContratLocation


@admin.register(ContratLocation)
class ContratLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation', 'status', 'signed_at', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reservation__id',)

