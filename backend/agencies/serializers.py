from rest_framework import serializers
from .models import Agence, DemandePartenariat, DemandeCompteAdmin
from accounts.serializers import UserSerializer


class AgenceSerializer(serializers.ModelSerializer):
    """Agence serializer"""
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Agence
        fields = ['id', 'nom_agence', 'siege_agence', 'num_contact', 'email_agence',
                'nmbr_succursales', 'nmbr_flotte', 'logo_agence', 'logo_url', 
                'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_logo_url(self, obj):
        if obj.logo_agence:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo_agence.url)
        return None


class DemandePartenariatSerializer(serializers.ModelSerializer):
    """Demande partenariat serializer"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewed_by_email = serializers.EmailField(source='reviewed_by.user.email', read_only=True)
    
    class Meta:
        model = DemandePartenariat
        fields = ['id', 'nom_prop', 'prenom_prop', 'ddn_prop', 'email_prop', 'phone_prop',
                'nom_agence', 'siege_agence', 'logo_agence', 'num_contact', 'email_agence',
                'nmbr_succursales', 'nmbr_flotte', 'status', 'status_display', 
                'reviewed_by', 'reviewed_by_email', 'reviewed_at', 'created_at']
        read_only_fields = ['status', 'reviewed_by', 'reviewed_at', 'created_at']


class DemandeCompteAdminSerializer(serializers.ModelSerializer):
    """Demande compte admin serializer"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    requested_by_email = serializers.EmailField(source='requested_by.user.email', read_only=True)
    reviewed_by_email = serializers.EmailField(source='reviewed_by.user.email', read_only=True)
    
    class Meta:
        model = DemandeCompteAdmin
        fields = ['id', 'nom_admin', 'prenom_admin', 'ddn_admin', 'email_admin', 'phone_admin',
                'agence', 'agence_nom', 'requested_by', 'requested_by_email', 'status', 
                'status_display', 'reviewed_by', 'reviewed_by_email', 'reviewed_at', 'created_at']
        read_only_fields = ['requested_by', 'status', 'reviewed_by', 'reviewed_at', 'created_at']

