/**
 * Application-wide constants
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  TIMEOUT: 30000,
} as const;

// User Roles
export const USER_ROLES = {
  ADMIN: 'ADMIN',
  OWNER: 'OWNER',
  SECRETARY: 'SECRETARY',
  MECHANIC: 'MECHANIC',
  RENTER: 'RENTER',
  AGENCY_ADMIN: 'AGENCY_ADMIN',
  VISITOR: 'VISITOR',
} as const;

// Vehicle States
export const VEHICLE_STATES = {
  INTRUSION: 'intrusion',
  EN_PANNE: 'enPanne',
  PROCHAINEMENT_DISPONIBLE: 'prochainementDisponible',
  EN_MARCHE: 'enMarche',
  EN_ARRET: 'enArret',
} as const;

// Vehicle Categories
export const VEHICLE_CATEGORIES = {
  PETITES: 'Petites',
  MOYENNES: 'Moyennes',
  LARGES: 'Larges',
  PREMIUM: 'Premium',
  MONOSPACES: 'Monospaces',
  SUV: 'SUV',
} as const;

// Reservation Status
export const RESERVATION_STATUS = {
  PENDING: 'PENDING',
  CONFIRMED: 'CONFIRMED',
  ACTIVE: 'ACTIVE',
  COMPLETED: 'COMPLETED',
  CANCELLED: 'CANCELLED',
} as const;

// Contract Status
export const CONTRACT_STATUS = {
  DRAFT: 'DRAFT',
  PENDING_SIGNATURE: 'PENDING_SIGNATURE',
  SIGNED: 'SIGNED',
  CANCELLED: 'CANCELLED',
} as const;

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  VISITOR: '/visitor',
  RENTER: '/renter',
  ADMIN: '/admin',
  OWNER: '/owner',
  SECRETARY: '/secretary',
  MECHANIC: '/mechanic',
  AGENCY_ADMIN: '/agency-admin',
} as const;

// Cookie Names
export const COOKIE_NAMES = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  USER: 'user',
  PROFILE: 'profile',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'Resource not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
  INVALID_CREDENTIALS: 'Invalid email or password.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Login successful!',
  REGISTER_SUCCESS: 'Registration successful!',
  LOGOUT_SUCCESS: 'Logged out successfully!',
  UPDATE_SUCCESS: 'Updated successfully!',
  DELETE_SUCCESS: 'Deleted successfully!',
  CREATE_SUCCESS: 'Created successfully!',
} as const;

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
} as const;

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  INPUT: 'yyyy-MM-dd',
  DATETIME: 'MMM dd, yyyy HH:mm',
} as const;

