# Rent4You Frontend

Next.js 14 frontend application for the Rent4You car rental management system.

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   Create `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

   Application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app router
│   │   ├── (auth)/            # Authentication pages
│   │   ├── (admin)/           # Admin pages
│   │   ├── (owner)/           # Owner pages
│   │   ├── (secretary)/       # Secretary pages
│   │   ├── (renter)/          # Renter pages
│   │   ├── (mechanic)/        # Mechanic pages
│   │   ├── (agency-admin)/    # Agency admin pages
│   │   └── (visitor)/         # Visitor pages
│   ├── components/            # React components
│   │   ├── common/           # Shared components
│   │   ├── admin/            # Admin components
│   │   └── ...
│   ├── lib/                   # Utilities
│   │   └── api/              # API clients
│   ├── hooks/                 # Custom hooks
│   ├── contexts/              # React contexts
│   └── styles/               # Global styles
└── public/                    # Static assets
```

## Features

### Authentication
- JWT token-based authentication
- Automatic token refresh
- Role-based routing
- Protected routes

### API Integration
- Axios-based API client
- Request/response interceptors
- Error handling
- Token management

### Styling
- Preserved original color scheme
- Poppins font family
- Responsive design
- CSS modules

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Pages

### Public
- `/` - Home (redirects based on auth status)
- `/login` - Login page
- `/register` - Registration page
- `/visitor` - Visitor homepage (vehicle listing)

### Role-Based (Protected)
- `/admin` - Administrator dashboard
- `/owner` - Agency owner dashboard
- `/secretary` - Secretary dashboard
- `/renter` - Renter dashboard
- `/mechanic` - Mechanic dashboard
- `/agency-admin` - Agency admin dashboard

## Components

### Common Components
- `Navbar` - Navigation bar
- `Footer` - Footer
- `VehicleCard` - Vehicle display card
- `SearchBar` - Vehicle search
- `Modal` - Modal dialog
- `Button` - Button component

## API Client

The API client is configured in `src/lib/api/client.ts` and includes:
- Automatic token injection
- Token refresh on 401 errors
- Error handling
- Request/response interceptors

## State Management

- **Auth Context**: User authentication state
- **React Query**: Server state management
- **Local State**: Component-level state with useState

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL

## Deployment

1. Build the application:
   ```bash
   npm run build
   ```

2. Deploy to Vercel, Netlify, or your preferred hosting platform

3. Configure environment variables in your hosting platform

