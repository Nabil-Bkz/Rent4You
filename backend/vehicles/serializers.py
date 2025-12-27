from rest_framework import serializers
from .models import Vehicule, Depot, PrixHistorique
from agencies.serializers import AgenceSerializer


class DepotSerializer(serializers.ModelSerializer):
    """Depot serializer"""
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = Depot
        fields = ['id', 'adress_dpt', 'capacite_dpt', 'agence', 'agence_nom', 
                'is_active', 'created_at']
        read_only_fields = ['created_at']


class VehiculeSerializer(serializers.ModelSerializer):
    """Vehicule serializer"""
    image_url = serializers.SerializerMethodField()
    etat_display = serializers.CharField(source='get_etat_vehicule_display', read_only=True)
    categorie_display = serializers.CharField(source='get_categorie_vehicule_display', read_only=True)
    depot_adress = serializers.CharField(source='depot.adress_dpt', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = Vehicule
        fields = ['id', 'matricule', 'marque', 'model', 'prix_heure', 'prix_jour',
                'description', 'etat_vehicule', 'etat_display', 'disponibilite',
                'categorie_vehicule', 'categorie_display', 'depot', 'depot_adress',
                'agence', 'agence_nom', 'img_vhl', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.img_vhl:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.img_vhl.url)
        return None


class PrixHistoriqueSerializer(serializers.ModelSerializer):
    """Prix historique serializer"""
    vehicule_matricule = serializers.CharField(source='vehicule.matricule', read_only=True)
    modifie_par_email = serializers.EmailField(source='modifie_par.email', read_only=True)
    
    class Meta:
        model = PrixHistorique
        fields = ['id', 'vehicule', 'vehicule_matricule', 'ancien_prix_jour', 
                'nouveau_prix_jour', 'ancien_prix_heure', 'nouveau_prix_heure',
                'modifie_par', 'modifie_par_email', 'created_at']
        read_only_fields = ['created_at']

