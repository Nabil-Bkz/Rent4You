# Rent4You - Professional Car Rental Management System

Modern car rental management platform. Built with Django REST API, Next.js, and PostgreSQL, featuring JWT auth, role-based access control, email notifications, statistics dashboard, and multi-role admin system.

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


