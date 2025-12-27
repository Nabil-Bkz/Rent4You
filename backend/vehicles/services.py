"""
Business logic services for vehicles app
"""
from typing import Dict, Any, Optional
from django.db.models import Q
from core.exceptions import BusinessLogicError, VehicleHasActiveReservationsError
from core.constants import ErrorMessages, ReservationStatus
from core.utils import get_user_agency


class VehicleService:
    """Service for vehicle operations"""
    
    @staticmethod
    def can_modify_price(vehicule, user) -> bool:
        """
        Check if vehicle price can be modified
        
        Args:
            vehicule: Vehicle instance
            user: User instance
            
        Returns:
            True if price can be modified, False otherwise
        """
        from reservations.models import Reservation
        
        # Check if vehicle has active reservations
        active_reservations = Reservation.objects.filter(
            vehicule=vehicule,
            status__in=ReservationStatus.ACTIVE_STATUSES
        )
        
        if active_reservations.exists():
            return False
        
        return True
    
    @staticmethod
    def update_price(vehicule, prix_jour: Optional[float] = None, 
                     prix_heure: Optional[float] = None, user=None) -> Dict[str, Any]:
        """
        Update vehicle price and create history
        
        Args:
            vehicule: Vehicle instance
            prix_jour: New daily price
            prix_heure: New hourly price
            user: User making the change
            
        Returns:
            Updated vehicle data
            
        Raises:
            VehicleHasActiveReservationsError: If vehicle has active reservations
        """
        if not VehicleService.can_modify_price(vehicule, user):
            raise VehicleHasActiveReservationsError(ErrorMessages.VEHICLE_HAS_ACTIVE_RESERVATIONS)
        
        if not prix_jour and not prix_heure:
            raise BusinessLogicError(ErrorMessages.PRICE_REQUIRED)
        
        from vehicles.models import PrixHistorique
        
        # Create price history
        PrixHistorique.objects.create(
            vehicule=vehicule,
            ancien_prix_jour=vehicule.prix_jour,
            nouveau_prix_jour=prix_jour or vehicule.prix_jour,
            ancien_prix_heure=vehicule.prix_heure,
            nouveau_prix_heure=prix_heure or vehicule.prix_heure,
            modifie_par=user
        )
        
        # Update vehicle price
        if prix_jour:
            vehicule.prix_jour = prix_jour
        if prix_heure:
            vehicule.prix_heure = prix_heure
        vehicule.save()
        
        from vehicles.serializers import VehiculeSerializer
        return VehiculeSerializer(vehicule).data
    
    @staticmethod
    def filter_vehicles(queryset, filters: Dict[str, Any]):
        """
        Apply filters to vehicle queryset
        
        Args:
            queryset: Vehicle queryset
            filters: Dictionary of filters
            
        Returns:
            Filtered queryset
        """
        # Filter by availability
        if 'disponibilite' in filters and filters['disponibilite'] is not None:
            queryset = queryset.filter(disponibilite=filters['disponibilite'])
        
        # Filter by category
        if 'categorie' in filters and filters['categorie']:
            queryset = queryset.filter(categorie_vehicule=filters['categorie'])
        
        # Filter by agency
        if 'agence' in filters and filters['agence']:
            queryset = queryset.filter(agence_id=filters['agence'])
        
        # Filter by depot
        if 'depot' in filters and filters['depot']:
            queryset = queryset.filter(depot_id=filters['depot'])
        
        # Filter by price range
        if 'prix_min' in filters and filters['prix_min']:
            queryset = queryset.filter(prix_jour__gte=filters['prix_min'])
        if 'prix_max' in filters and filters['prix_max']:
            queryset = queryset.filter(prix_jour__lte=filters['prix_max'])
        
        return queryset

