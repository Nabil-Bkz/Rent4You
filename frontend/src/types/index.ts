/**
 * TypeScript type definitions for the application
 */

// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  date_of_birth?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type UserRole =
  | 'ADMIN'
  | 'OWNER'
  | 'SECRETARY'
  | 'MECHANIC'
  | 'RENTER'
  | 'AGENCY_ADMIN'
  | 'VISITOR';

export interface UserProfile {
  id: number;
  user: number;
  agence?: number;
  is_banned?: boolean;
  banned_from_agencies?: number[];
}

// Vehicle Types
export interface Vehicle {
  id: number;
  matricule: string;
  marque: string;
  model: string;
  prix_heure: number;
  prix_jour: number;
  description: string;
  etat_vehicule: VehicleState;
  disponibilite: boolean;
  categorie_vehicule: VehicleCategory;
  depot?: number;
  agence: number;
  img_vhl?: string;
  created_at: string;
  updated_at: string;
}

export type VehicleState =
  | 'intrusion'
  | 'enPanne'
  | 'prochainementDisponible'
  | 'enMarche'
  | 'enArret';

export type VehicleCategory =
  | 'Petites'
  | 'Moyennes'
  | 'Larges'
  | 'Premium'
  | 'Monospaces'
  | 'SUV';

// Reservation Types
export interface Reservation {
  id: number;
  date_debut: string;
  date_fin: string;
  prix: number;
  prix_original: number;
  reduction: number;
  status: ReservationStatus;
  locataire: number;
  vehicule: number;
  code_promo?: number;
  created_at: string;
  updated_at: string;
}

export type ReservationStatus =
  | 'PENDING'
  | 'CONFIRMED'
  | 'ACTIVE'
  | 'COMPLETED'
  | 'CANCELLED';

// Contract Types
export interface Contract {
  id: number;
  reservation: number;
  pdf_file?: string;
  status: ContractStatus;
  signed_at?: string;
  signature_locataire?: string;
  created_at: string;
  updated_at: string;
}

export type ContractStatus =
  | 'DRAFT'
  | 'PENDING_SIGNATURE'
  | 'SIGNED'
  | 'CANCELLED';

// Agency Types
export interface Agency {
  id: number;
  nom_agence: string;
  siege_agence: string;
  num_contact: string;
  email_agence: string;
  nmbr_succursales: number;
  nmbr_flotte: number;
  logo_agence?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Complaint Types
export interface Complaint {
  id: number;
  sujet: string;
  description: string;
  status: ComplaintStatus;
  locataire: number;
  agence: number;
  resolved_at?: string;
  created_at: string;
}

export type ComplaintStatus = 'PENDING' | 'RESOLVED';

// API Response Types
export interface APIResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone: string;
  date_of_birth: string;
  role: UserRole;
}

export interface AuthResponse {
  user: User;
  profile?: UserProfile;
  tokens: {
    access: string;
    refresh: string;
  };
}

// Filter Types
export interface VehicleFilters {
  disponibilite?: boolean;
  categorie?: VehicleCategory;
  agence?: number;
  depot?: number;
  prix_min?: number;
  prix_max?: number;
  search?: string;
}

