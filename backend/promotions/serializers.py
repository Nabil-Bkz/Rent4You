from rest_framework import serializers
from .models import CodePromo


class CodePromoSerializer(serializers.ModelSerializer):
    """Code promo serializer"""
    is_valid_field = serializers.SerializerMethodField()
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.user.email', read_only=True)
    
    class Meta:
        model = CodePromo
        fields = ['id', 'code', 'discount_percentage', 'max_uses', 'current_uses',
                'valid_from', 'valid_until', 'is_active', 'is_valid_field', 'agence',
                'agence_nom', 'created_by', 'created_by_email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'current_uses', 'created_by']
    
    def get_is_valid_field(self, obj):
        return obj.is_valid()

