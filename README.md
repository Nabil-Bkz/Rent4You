# Rent4You - Professional Car Rental Management System

A comprehensive, professional car rental management system built with Django REST API backend and Next.js frontend, featuring role-based access control for multiple user types.

## 🚀 Features

### User Roles & Capabilities

#### **Administrateur (System Administrator)**
- Manage user profiles (all roles)
- Manage users: add/modify/delete/display
- Process partnership requests
- Process agency administrator account requests
- Full system access

#### **Propriétaire de l'agence (Agency Owner)**
- Manage profile
- Manage tenant complaints
- Manage vehicles
- Maintain list of excluded tenants
- View statistics (budgets, vehicles, employees)
- Request agency administrator accounts
- Modify vehicle rental prices (when not rented or at end of rental)

#### **Secrétaire de l'Agence (Agency Secretary)**
- Manage profile
- Create rental contracts
- View reservations
- Modify reservation status
- Add/remove vehicles from depots
- View tenant list
- Add/remove/ban tenants
- Manage problems reported by tenants

#### **Garagiste (Mechanic)**
- Manage profile
- Create vehicle state reports for agency vehicles

#### **Locataire (Renter/Tenant)**
- Manage profile
- Reserve one or multiple vehicles from an agency
- Start vehicle rental
- View vehicle list
- Sign rental contract
- View payment invoices (rental price + agency fees)
- Report accidents or problems with vehicle
- File complaints to agency owner
- View/cancel reservations

#### **Administrateur de l'Agence (Agency Administrator)**
- Manage profile
- Create promo codes
- Manage agency employee list
- Manage depot list
- Manage agency vehicle list

#### **Visiteur (Visitor)**
- Register
- View vehicle list
- Send partnership request

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **JWT Authentication** - Secure token-based auth
- **Pillow** - Image processing
- **OpenPyXL** - Excel export
- **ReportLab** - PDF generation

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **React Query** - Server state management
- **Axios** - HTTP client
- **CSS Modules** - Styling (preserving original design)

## 📁 Project Structure

```
Rent4You/
├── backend/                 # Django REST API
│   ├── accounts/           # User authentication & roles
│   ├── agencies/           # Agency management
│   ├── vehicles/           # Vehicle management
│   ├── reservations/       # Reservation system
│   ├── contracts/          # Contract management
│   ├── complaints/         # Complaints & reports
│   ├── partnerships/       # Partnership requests
│   ├── promotions/         # Promo codes
│   ├── notifications/      # In-app notifications
│   ├── statistics/        # Statistics & analytics
│   ├── core/               # Shared utilities
│   └── rent4you/           # Project configuration
├── frontend/                # Next.js application
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities & API clients
│   │   ├── hooks/          # Custom React hooks
│   │   ├── contexts/      # React contexts
│   │   ├── types/         # TypeScript types
│   │   ├── constants/     # Application constants
│   │   ├── utils/         # Utility functions
│   │   └── styles/        # Global styles
│   └── public/            # Static assets
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL database

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   Create `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## 🎨 Design System

The application maintains the original color scheme and design:

- **Primary Orange**: `#ff7800`
- **Primary Black**: `#130f40`
- **Light Gray**: `#666`
- **Font**: Poppins (Google Fonts)

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/accounts/users/me/` - Get current user
- `PUT /api/accounts/users/update_profile/` - Update profile
- `POST /api/accounts/users/change_password/` - Change password

### Vehicle Endpoints

- `GET /api/vehicles/vehicules/` - List vehicles (with filters)
- `POST /api/vehicles/vehicules/` - Create vehicle (agency staff)
- `GET /api/vehicles/vehicules/{id}/` - Get vehicle details
- `PUT /api/vehicles/vehicules/{id}/` - Update vehicle
- `POST /api/vehicles/vehicules/{id}/update_price/` - Update price (owner)

### Reservation Endpoints

- `GET /api/reservations/reservations/` - List reservations
- `POST /api/reservations/reservations/` - Create reservation (renter)
- `GET /api/reservations/reservations/{id}/` - Get reservation
- `POST /api/reservations/reservations/{id}/confirm/` - Confirm (secretary)
- `POST /api/reservations/reservations/{id}/cancel/` - Cancel

### Agency Endpoints

- `GET /api/agencies/agences/` - List agencies
- `POST /api/agencies/partenariats/` - Create partnership request
- `POST /api/agencies/partenariats/{id}/approve/` - Approve (admin)
- `POST /api/agencies/comptes-admin/` - Request admin account (owner)

### Notification Endpoints

- `GET /api/notifications/notifications/` - List notifications
- `GET /api/notifications/notifications/unread_count/` - Get unread count
- `POST /api/notifications/notifications/{id}/mark_read/` - Mark as read
- `POST /api/notifications/notifications/mark_all_read/` - Mark all as read

### Statistics Endpoints

- `GET /api/statistics/` - Get statistics (role-based)
- `GET /api/statistics/export/?format=excel|pdf` - Export statistics

See `backend/README.md` for complete API documentation.

## ✨ Key Features

### Backend Features
- ✅ JWT Authentication with token refresh
- ✅ Role-based access control (RBAC)
- ✅ Email notifications
- ✅ File upload with validation
- ✅ Statistics and analytics
- ✅ In-app notification system
- ✅ Export to Excel/PDF
- ✅ Rate limiting
- ✅ Caching support
- ✅ Advanced validation

### Frontend Features
- ✅ TypeScript for type safety
- ✅ Responsive design
- ✅ Real-time notifications
- ✅ Statistics dashboard
- ✅ Error boundaries
- ✅ Loading states
- ✅ Form validation

## 🔒 Security Features

- JWT token-based authentication
- Role-based access control (RBAC)
- Password strength validation
- CORS configuration
- SQL injection protection (Django ORM)
- XSS protection
- Rate limiting
- Environment variable configuration
- Secure file uploads

## 📝 Database

The project uses PostgreSQL. Connection details are configured via environment variables in the `.env` file.

**Important**: Never commit your `.env` file or database credentials to version control.

## 🧪 Testing

### Backend
```bash
cd backend
python manage.py test
```

### Frontend
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure `ALLOWED_HOSTS`
3. Set up static file serving
4. Configure database connection
5. Run migrations
6. Set up email service
7. Configure caching (Redis recommended)

### Frontend Deployment
1. Build the application:
   ```bash
   npm run build
   ```
2. Deploy to Vercel, Netlify, or your preferred hosting
3. Configure environment variables

## 📖 Documentation

- [Setup Guide](SETUP_GUIDE.md) - Detailed setup instructions
- [Backend README](backend/README.md) - Backend API documentation
- [Frontend README](frontend/README.md) - Frontend documentation
- [New Features](NEW_FEATURES.md) - List of new features
- [Refactoring Summary](REFACTORING_SUMMARY.md) - Code improvements
- [GitHub Setup](GITHUB_SETUP.md) - GitHub repository setup guide

## 📄 License

This project is proprietary software.

## 👥 Authors

- Development Team

## 🙏 Acknowledgments

- Original design and color scheme preserved
- Django REST Framework community
- Next.js team

---

For detailed setup instructions, see:
- [Setup Guide](SETUP_GUIDE.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)
