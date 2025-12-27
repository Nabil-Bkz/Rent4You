"""
Views for statistics
"""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.statistics_service import StatisticsService
from core.response import APIResponse
from core.permissions import IsAdministrateur, IsProprietaireAgence, IsAgencyStaff
from datetime import datetime


class StatisticsView(APIView):
    """View for getting statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get statistics based on user role"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        start_date_obj = datetime.fromisoformat(start_date) if start_date else None
        end_date_obj = datetime.fromisoformat(end_date) if end_date else None
        
        # System admin gets system statistics
        if IsAdministrateur().has_permission(request, self):
            stats = StatisticsService.get_system_statistics(start_date_obj, end_date_obj)
            return APIResponse.success(data=stats)
        
        # Agency owner/staff gets agency statistics
        if IsAgencyStaff().has_permission(request, self):
            from core.utils import get_user_agency
            agency = get_user_agency(request.user)
            if agency:
                stats = StatisticsService.get_agency_statistics(
                    agency.id,
                    start_date_obj,
                    end_date_obj
                )
                return APIResponse.success(data=stats)
        
        # Regular user gets their own statistics
        stats = StatisticsService.get_user_statistics(request.user.id)
        return APIResponse.success(data=stats)


class ExportStatisticsView(APIView):
    """View for exporting statistics"""
    permission_classes = [IsAuthenticated, IsAgencyStaff]
    
    def get(self, request):
        """Export statistics to Excel"""
        from core.utils import get_user_agency
        from core.export_service import ExportService
        from reservations.models import Reservation
        
        agency = get_user_agency(request.user)
        if not agency:
            return APIResponse.error(
                message="Agence non trouvée.",
                status_code=400
            )
        
        format_type = request.query_params.get('format', 'excel')
        
        # Get reservations for agency
        reservations = Reservation.objects.filter(vehicule__agence=agency)
        
        if format_type == 'excel':
            return ExportService.export_reservations_to_excel(
                reservations,
                filename=f'reservations_agence_{agency.id}.xlsx'
            )
        elif format_type == 'pdf':
            return ExportService.export_reservations_to_pdf(
                reservations,
                filename=f'reservations_agence_{agency.id}.pdf'
            )
        
        return APIResponse.error(
            message="Format non supporté. Utilisez 'excel' ou 'pdf'.",
            status_code=400
        )

