from django.contrib import admin
from .models import CodePromo


@admin.register(CodePromo)
class CodePromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'agence', 'is_active', 'current_uses', 'max_uses', 'valid_until')
    list_filter = ('is_active', 'agence', 'created_at')
    search_fields = ('code',)
    readonly_fields = ('current_uses',)

