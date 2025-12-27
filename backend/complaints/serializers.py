from rest_framework import serializers
from .models import Reclamation, Rapport, EtatVehicule


class ReclamationSerializer(serializers.ModelSerializer):
    """Reclamation serializer"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    locataire_email = serializers.EmailField(source='locataire.user.email', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = Reclamation
        fields = ['id', 'contenu_reclamation', 'status', 'status_display', 'locataire',
                'locataire_email', 'agence', 'agence_nom', 'reservation', 'traite_par',
                'traite_at', 'reponse', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'traite_par', 'traite_at']


class RapportSerializer(serializers.ModelSerializer):
    """Rapport serializer"""
    type_display = serializers.CharField(source='get_type_rapport_display', read_only=True)
    locataire_email = serializers.EmailField(source='locataire.user.email', read_only=True)
    vehicule_matricule = serializers.CharField(source='vehicule.matricule', read_only=True)
    
    class Meta:
        model = Rapport
        fields = ['id', 'description', 'type_rapport', 'type_display', 'images',
                'locataire', 'locataire_email', 'agence', 'reservation', 'vehicule',
                'vehicule_matricule', 'created_at']
        read_only_fields = ['created_at']


class EtatVehiculeSerializer(serializers.ModelSerializer):
    """Etat vehicule serializer"""
    etat_display = serializers.CharField(source='get_etat_general_display', read_only=True)
    vehicule_matricule = serializers.CharField(source='vehicule.matricule', read_only=True)
    garagiste_email = serializers.EmailField(source='garagiste.user.email', read_only=True)
    
    class Meta:
        model = EtatVehicule
        fields = ['id', 'etat_general', 'etat_display', 'description', 'kilometrage',
                'notes', 'vehicule', 'vehicule_matricule', 'garagiste', 'garagiste_email',
                'created_at']
        read_only_fields = ['created_at']

