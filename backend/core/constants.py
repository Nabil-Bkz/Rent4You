"""
Application-wide constants
"""

# User Roles
class UserRoles:
    ADMIN = 'ADMIN'
    OWNER = 'OWNER'
    SECRETARY = 'SECRETARY'
    MECHANIC = 'MECHANIC'
    RENTER = 'RENTER'
    AGENCY_ADMIN = 'AGENCY_ADMIN'
    VISITOR = 'VISITOR'
    
    CHOICES = [
        (ADMIN, 'Administrateur'),
        (OWNER, 'Propriétaire Agence'),
        (SECRETARY, 'Secrétaire Agence'),
        (MECHANIC, 'Garagiste'),
        (RENTER, 'Locataire'),
        (AGENCY_ADMIN, 'Administrateur Agence'),
        (VISITOR, 'Visiteur'),
    ]


# Vehicle States
class VehicleStates:
    INTRUSION = 'intrusion'
    EN_PANNE = 'enPanne'
    PROCHAINEMENT_DISPONIBLE = 'prochainementDisponible'
    EN_MARCHE = 'enMarche'
    EN_ARRET = 'enArret'
    
    CHOICES = [
        (INTRUSION, 'Intrusion'),
        (EN_PANNE, 'En Panne'),
        (PROCHAINEMENT_DISPONIBLE, 'Prochainement Disponible'),
        (EN_MARCHE, 'En Marche'),
        (EN_ARRET, 'En Arrêt'),
    ]


# Vehicle Categories
class VehicleCategories:
    PETITES = 'Petites'
    MOYENNES = 'Moyennes'
    LARGES = 'Larges'
    PREMIUM = 'Premium'
    MONOSPACES = 'Monospaces'
    SUV = 'SUV'
    
    CHOICES = [
        (PETITES, 'Petites'),
        (MOYENNES, 'Moyennes'),
        (LARGES, 'Larges'),
        (PREMIUM, 'Premium'),
        (MONOSPACES, 'Monospaces'),
        (SUV, 'SUV'),
    ]


# Reservation Status
class ReservationStatus:
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    CHOICES = [
        (PENDING, 'En attente'),
        (CONFIRMED, 'Confirmée'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Terminée'),
        (CANCELLED, 'Annulée'),
    ]
    
    ACTIVE_STATUSES = [PENDING, CONFIRMED, ACTIVE]


# Contract Status
class ContractStatus:
    DRAFT = 'DRAFT'
    PENDING_SIGNATURE = 'PENDING_SIGNATURE'
    SIGNED = 'SIGNED'
    CANCELLED = 'CANCELLED'
    
    CHOICES = [
        (DRAFT, 'Brouillon'),
        (PENDING_SIGNATURE, 'En attente de signature'),
        (SIGNED, 'Signé'),
        (CANCELLED, 'Annulé'),
    ]


# Partnership Request Status
class PartnershipStatus:
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    
    CHOICES = [
        (PENDING, 'En attente'),
        (APPROVED, 'Approuvée'),
        (REJECTED, 'Rejetée'),
    ]


# Error Messages
class ErrorMessages:
    INVALID_CREDENTIALS = "Invalid credentials."
    USER_DISABLED = "User account is disabled."
    EMAIL_PASSWORD_REQUIRED = "Email and password are required."
    VEHICLE_HAS_ACTIVE_RESERVATIONS = "Cannot modify price for a vehicle with active reservations."
    PRICE_REQUIRED = "At least one price must be provided."
    PERMISSION_DENIED = "You do not have permission to perform this action."
    NOT_FOUND = "Resource not found."
    VALIDATION_ERROR = "Validation error occurred."


# Success Messages
class SuccessMessages:
    PASSWORD_UPDATED = "Password updated successfully."
    PROFILE_UPDATED = "Profile updated successfully."
    RESERVATION_CREATED = "Reservation created successfully."
    RESERVATION_CONFIRMED = "Reservation confirmed successfully."
    RESERVATION_CANCELLED = "Reservation cancelled successfully."
    CONTRACT_SIGNED = "Contract signed successfully."
    COMPLAINT_RESOLVED = "Complaint resolved successfully."

