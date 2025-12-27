from rest_framework import serializers
from .models import Reservation
from accounts.serializers import UserSerializer
from vehicles.serializers import VehiculeSerializer


class ReservationSerializer(serializers.ModelSerializer):
    """Reservation serializer"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    locataire_email = serializers.EmailField(source='locataire.user.email', read_only=True)
    locataire_name = serializers.SerializerMethodField()
    vehicule_details = VehiculeSerializer(source='vehicule', read_only=True)
    code_promo_code = serializers.CharField(source='code_promo.code', read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'date_debut', 'date_fin', 'prix', 'prix_original', 'reduction',
                'status', 'status_display', 'locataire', 'locataire_email', 'locataire_name',
                'vehicule', 'vehicule_details', 'code_promo', 'code_promo_code',
                'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_locataire_name(self, obj):
        return f"{obj.locataire.user.first_name} {obj.locataire.user.last_name}"

