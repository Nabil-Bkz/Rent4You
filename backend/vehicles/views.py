from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vehicule, Depot, PrixHistorique
from .serializers import VehiculeSerializer, DepotSerializer, PrixHistoriqueSerializer
from core.permissions import IsAgencyStaff, IsProprietaireAgence, IsAdminAgence
from core.response import APIResponse
from .services import VehicleService
from core.file_service import FileService


class VehiculeViewSet(viewsets.ModelViewSet):
    """Vehicule ViewSet"""
    queryset = Vehicule.objects.all()
    serializer_class = VehiculeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['matricule', 'marque', 'model', 'description']
    ordering_fields = ['prix_jour', 'prix_heure', 'created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAgencyStaff()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        """Create vehicle with file upload support"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Handle image upload if provided
        if 'img_vhl' in request.FILES:
            try:
                uploaded_file = request.FILES['img_vhl']
                file_path = FileService.upload_image(
                    uploaded_file,
                    upload_path='vehicles/',
                    prefix='vehicle'
                )
                serializer.validated_data['img_vhl'] = file_path
            except ValueError as e:
                return APIResponse.error(
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return APIResponse.created(
            data=serializer.data,
            message="Vehicle created successfully."
        )
    
    def update(self, request, *args, **kwargs):
        """Update vehicle with file upload support"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Handle image upload if provided
        if 'img_vhl' in request.FILES:
            try:
                uploaded_file = request.FILES['img_vhl']
                # Delete old image if exists
                if instance.img_vhl:
                    FileService.delete_file(instance.img_vhl.name)
                
                file_path = FileService.upload_image(
                    uploaded_file,
                    upload_path='vehicles/',
                    prefix='vehicle'
                )
                serializer.validated_data['img_vhl'] = file_path
            except ValueError as e:
                return APIResponse.error(
                    message=str(e),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        
        self.perform_update(serializer)
        return APIResponse.success(
            data=serializer.data,
            message="Vehicle updated successfully."
        )
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Extract filters from query params
        filters = {
            'disponibilite': self.request.query_params.get('disponibilite'),
            'categorie': self.request.query_params.get('categorie'),
            'agence': self.request.query_params.get('agence'),
            'depot': self.request.query_params.get('depot'),
            'prix_min': self.request.query_params.get('prix_min'),
            'prix_max': self.request.query_params.get('prix_max'),
        }
        
        # Convert disponibilite to boolean if provided
        if filters['disponibilite'] is not None:
            filters['disponibilite'] = filters['disponibilite'].lower() == 'true'
        
        return VehicleService.filter_vehicles(queryset, filters)
    
    @action(detail=True, methods=['post'], permission_classes=[IsProprietaireAgence])
    def update_price(self, request, pk=None):
        """Update vehicle price and create history"""
        try:
            vehicule = self.get_object()
            nouveau_prix_jour = request.data.get('prix_jour')
            nouveau_prix_heure = request.data.get('prix_heure')
            
            result = VehicleService.update_price(
                vehicule,
                prix_jour=nouveau_prix_jour,
                prix_heure=nouveau_prix_heure,
                user=request.user
            )
            
            return APIResponse.success(
                data=result,
                message="Price updated successfully."
            )
        except Exception as e:
            status_code = getattr(e, 'status_code', status.HTTP_400_BAD_REQUEST)
            return APIResponse.error(
                message=str(e),
                status_code=status_code
            )


class DepotViewSet(viewsets.ModelViewSet):
    """Depot ViewSet"""
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer
    permission_classes = [IsAgencyStaff]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by agency if user is agency staff
        from core.utils import get_user_agency
        agency = get_user_agency(self.request.user)
        if agency:
            queryset = queryset.filter(agence=agency)
        return queryset

