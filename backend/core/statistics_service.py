"""
Statistics and analytics service
"""
from typing import Dict, Any, List
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal


class StatisticsService:
    """Service for generating statistics and analytics"""
    
    @staticmethod
    def get_agency_statistics(agence_id: int, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """
        Get statistics for an agency
        
        Args:
            agence_id: Agency ID
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Dictionary with statistics
        """
        from vehicles.models import Vehicule
        from reservations.models import Reservation
        from accounts.models import Locataire
        
        # Date filter
        date_filter = Q()
        if start_date:
            date_filter &= Q(created_at__gte=start_date)
        if end_date:
            date_filter &= Q(created_at__lte=end_date)
        
        # Vehicle statistics
        vehicles = Vehicule.objects.filter(agence_id=agence_id)
        total_vehicles = vehicles.count()
        available_vehicles = vehicles.filter(disponibilite=True).count()
        
        # Reservation statistics
        reservations = Reservation.objects.filter(
            vehicule__agence_id=agence_id
        ).filter(date_filter) if date_filter else Reservation.objects.filter(vehicule__agence_id=agence_id)
        
        total_reservations = reservations.count()
        confirmed_reservations = reservations.filter(status='CONFIRMED').count()
        active_reservations = reservations.filter(status='ACTIVE').count()
        completed_reservations = reservations.filter(status='COMPLETED').count()
        cancelled_reservations = reservations.filter(status='CANCELLED').count()
        
        # Revenue statistics
        revenue_data = reservations.filter(status__in=['CONFIRMED', 'ACTIVE', 'COMPLETED']).aggregate(
            total_revenue=Sum('prix'),
            average_price=Avg('prix'),
            total_reservations=Count('id')
        )
        
        total_revenue = revenue_data['total_revenue'] or Decimal('0')
        average_price = revenue_data['average_price'] or Decimal('0')
        
        # Customer statistics
        unique_customers = reservations.values('locataire').distinct().count()
        
        # Recent reservations (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_reservations = reservations.filter(created_at__gte=thirty_days_ago).count()
        
        return {
            'vehicles': {
                'total': total_vehicles,
                'available': available_vehicles,
                'unavailable': total_vehicles - available_vehicles,
            },
            'reservations': {
                'total': total_reservations,
                'confirmed': confirmed_reservations,
                'active': active_reservations,
                'completed': completed_reservations,
                'cancelled': cancelled_reservations,
                'recent_30_days': recent_reservations,
            },
            'revenue': {
                'total': float(total_revenue),
                'average': float(average_price),
            },
            'customers': {
                'unique': unique_customers,
            },
        }
    
    @staticmethod
    def get_system_statistics(start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """
        Get system-wide statistics
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            
        Returns:
            Dictionary with system statistics
        """
        from agencies.models import Agence
        from vehicles.models import Vehicule
        from reservations.models import Reservation
        from accounts.models import User, Locataire
        
        # Date filter
        date_filter = Q()
        if start_date:
            date_filter &= Q(created_at__gte=start_date)
        if end_date:
            date_filter &= Q(created_at__lte=end_date)
        
        # Basic counts
        total_agencies = Agence.objects.filter(is_active=True).count()
        total_vehicles = Vehicule.objects.count()
        total_users = User.objects.filter(is_active=True).count()
        total_renters = Locataire.objects.count()
        
        # Reservation statistics
        reservations = Reservation.objects.filter(date_filter) if date_filter else Reservation.objects.all()
        total_reservations = reservations.count()
        
        revenue_data = reservations.filter(status__in=['CONFIRMED', 'ACTIVE', 'COMPLETED']).aggregate(
            total_revenue=Sum('prix'),
            average_price=Avg('prix')
        )
        
        total_revenue = revenue_data['total_revenue'] or Decimal('0')
        average_price = revenue_data['average_price'] or Decimal('0')
        
        # Monthly statistics (last 12 months)
        monthly_stats = []
        for i in range(12):
            month_start = timezone.now() - timedelta(days=30 * (i + 1))
            month_end = timezone.now() - timedelta(days=30 * i)
            month_reservations = Reservation.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            )
            month_revenue = month_reservations.filter(
                status__in=['CONFIRMED', 'ACTIVE', 'COMPLETED']
            ).aggregate(total=Sum('prix'))['total'] or Decimal('0')
            
            monthly_stats.append({
                'month': month_start.strftime('%Y-%m'),
                'reservations': month_reservations.count(),
                'revenue': float(month_revenue),
            })
        
        monthly_stats.reverse()  # Oldest to newest
        
        return {
            'overview': {
                'agencies': total_agencies,
                'vehicles': total_vehicles,
                'users': total_users,
                'renters': total_renters,
            },
            'reservations': {
                'total': total_reservations,
            },
            'revenue': {
                'total': float(total_revenue),
                'average': float(average_price),
            },
            'monthly_stats': monthly_stats,
        }
    
    @staticmethod
    def get_user_statistics(user_id: int) -> Dict[str, Any]:
        """
        Get statistics for a user (renter)
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user statistics
        """
        from accounts.models import Locataire
        from reservations.models import Reservation
        
        try:
            locataire = Locataire.objects.get(user_id=user_id)
        except Locataire.DoesNotExist:
            return {}
        
        reservations = Reservation.objects.filter(locataire=locataire)
        
        total_reservations = reservations.count()
        active_reservations = reservations.filter(status__in=['PENDING', 'CONFIRMED', 'ACTIVE']).count()
        completed_reservations = reservations.filter(status='COMPLETED').count()
        
        total_spent = reservations.filter(status__in=['CONFIRMED', 'ACTIVE', 'COMPLETED']).aggregate(
            total=Sum('prix')
        )['total'] or Decimal('0')
        
        return {
            'reservations': {
                'total': total_reservations,
                'active': active_reservations,
                'completed': completed_reservations,
            },
            'spending': {
                'total': float(total_spent),
            },
        }

