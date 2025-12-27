from rest_framework import serializers
from .models import ContratLocation
from reservations.serializers import ReservationSerializer


class ContratLocationSerializer(serializers.ModelSerializer):
    """Contrat location serializer"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reservation_details = ReservationSerializer(source='reservation', read_only=True)
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ContratLocation
        fields = ['id', 'reservation', 'reservation_details', 'pdf_file', 'pdf_url',
                'status', 'status_display', 'signed_at', 'signature_locataire',
                'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'signed_at']
    
    def get_pdf_url(self, obj):
        if obj.pdf_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.pdf_file.url)
        return None

