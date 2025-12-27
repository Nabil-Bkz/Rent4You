from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CodePromo
from .serializers import CodePromoSerializer
from core.permissions import IsAdminAgence, IsLocataire


class CodePromoViewSet(viewsets.ModelViewSet):
    """Code promo ViewSet"""
    queryset = CodePromo.objects.all()
    serializer_class = CodePromoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminAgence()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.admin_agence)
    
    @action(detail=False, methods=['get'], permission_classes=[IsLocataire])
    def validate(self, request):
        """Validate a promo code"""
        code = request.query_params.get('code')
        if not code:
            return Response(
                {"error": "Code parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            code_promo = CodePromo.objects.get(code=code)
            is_valid = code_promo.is_valid()
            return Response({
                'valid': is_valid,
                'code': code_promo.code,
                'discount_percentage': code_promo.discount_percentage,
                'message': 'Code is valid' if is_valid else 'Code is invalid or expired'
            })
        except CodePromo.DoesNotExist:
            return Response(
                {"error": "Promo code not found."},
                status=status.HTTP_404_NOT_FOUND
            )

