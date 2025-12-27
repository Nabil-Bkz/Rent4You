# Rent4You Backend API

Django REST API backend for the Rent4You car rental management system.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create `.env` file in the backend directory and configure:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   DB_PORT=5432
   ```
   
   **Important**: Replace all placeholder values with your actual credentials. Never commit the `.env` file.

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login
- `GET /api/accounts/users/me/` - Get current user
- `PUT /api/accounts/users/update_profile/` - Update profile
- `POST /api/accounts/users/change_password/` - Change password
- `GET /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Vehicles
- `GET /api/vehicles/vehicules/` - List vehicles
  - Query params: `disponibilite`, `categorie`, `agence`, `depot`, `prix_min`, `prix_max`
- `POST /api/vehicles/vehicules/` - Create vehicle (agency staff)
- `GET /api/vehicles/vehicules/{id}/` - Get vehicle
- `PUT /api/vehicles/vehicules/{id}/` - Update vehicle
- `POST /api/vehicles/vehicules/{id}/update_price/` - Update price (owner)

### Reservations
- `GET /api/reservations/reservations/` - List reservations
- `POST /api/reservations/reservations/` - Create reservation (renter)
- `GET /api/reservations/reservations/{id}/` - Get reservation
- `POST /api/reservations/reservations/{id}/confirm/` - Confirm (secretary)
- `POST /api/reservations/reservations/{id}/cancel/` - Cancel

### Agencies
- `GET /api/agencies/agences/` - List agencies
- `POST /api/agencies/agences/` - Create agency (admin)
- `GET /api/agencies/agences/{id}/` - Get agency
- `POST /api/agencies/partenariats/` - Create partnership request
- `POST /api/agencies/partenariats/{id}/approve/` - Approve (admin)
- `POST /api/agencies/partenariats/{id}/reject/` - Reject (admin)

### Contracts
- `GET /api/contracts/contrats/` - List contracts
- `POST /api/contracts/contrats/` - Create contract (secretary)
- `POST /api/contracts/contrats/{id}/sign/` - Sign contract (renter)

### Complaints
- `GET /api/complaints/reclamations/` - List complaints
- `POST /api/complaints/reclamations/` - Create complaint (renter)
- `POST /api/complaints/reclamations/{id}/resolve/` - Resolve (owner)
- `POST /api/complaints/rapports/` - Create report (renter)
- `POST /api/complaints/etats-vehicules/` - Create vehicle state (mechanic)

### Promotions
- `GET /api/promotions/codes-promo/` - List promo codes
- `POST /api/promotions/codes-promo/` - Create promo code (agency admin)
- `GET /api/promotions/codes-promo/validate/?code=XXX` - Validate code

## Permissions

- **IsAdministrateur**: System administrators
- **IsProprietaireAgence**: Agency owners
- **IsSecretaireAgence**: Agency secretaries
- **IsGaragiste**: Mechanics
- **IsLocataire**: Renters
- **IsAdminAgence**: Agency administrators
- **IsAgencyStaff**: Any agency staff member

## Models

### User Roles
- `User` - Base user model
- `Administrateur` - System administrator
- `ProprietaireAgence` - Agency owner
- `SecretaireAgence` - Agency secretary
- `Garagiste` - Mechanic
- `Locataire` - Renter
- `AdminAgence` - Agency administrator

### Core Models
- `Agence` - Rental agency
- `Vehicule` - Vehicle
- `Depot` - Vehicle depot
- `Reservation` - Reservation
- `ContratLocation` - Rental contract
- `Reclamation` - Complaint
- `Rapport` - Report (accident/issue)
- `EtatVehicule` - Vehicle state (by mechanic)
- `CodePromo` - Promo code
- `DemandePartenariat` - Partnership request
- `DemandeCompteAdmin` - Admin account request

## Development

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Production

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Set up static file serving
4. Use environment variables for secrets
5. Configure database connection
6. Run migrations

