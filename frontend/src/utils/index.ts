/**
 * Utility functions
 */

import { UserRole } from '@/types';

/**
 * Format date to display format
 */
export const formatDate = (date: string | Date, format: string = 'MMM dd, yyyy'): string => {
  if (!date) return '';
  
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  if (isNaN(dateObj.getTime())) return '';
  
  // Simple date formatting (can be replaced with date-fns format)
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const month = months[dateObj.getMonth()];
  const day = dateObj.getDate();
  const year = dateObj.getFullYear();
  
  return `${month} ${day}, ${year}`;
};

/**
 * Format currency
 */
export const formatCurrency = (amount: number, currency: string = 'MAD'): string => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: currency,
  }).format(amount);
};

/**
 * Get user role display name
 */
export const getRoleDisplayName = (role: UserRole): string => {
  const roleNames: Record<UserRole, string> = {
    ADMIN: 'Administrateur',
    OWNER: 'Propriétaire Agence',
    SECRETARY: 'Secrétaire Agence',
    MECHANIC: 'Garagiste',
    RENTER: 'Locataire',
    AGENCY_ADMIN: 'Administrateur Agence',
    VISITOR: 'Visiteur',
  };
  
  return roleNames[role] || role;
};

/**
 * Check if user has specific role
 */
export const hasRole = (userRole: UserRole, requiredRole: UserRole): boolean => {
  return userRole === requiredRole;
};

/**
 * Check if user is agency staff
 */
export const isAgencyStaff = (role: UserRole): boolean => {
  return ['OWNER', 'SECRETARY', 'MECHANIC', 'AGENCY_ADMIN'].includes(role);
};

/**
 * Debounce function
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * Truncate text
 */
export const truncate = (text: string, length: number): string => {
  if (text.length <= length) return text;
  return text.slice(0, length) + '...';
};

/**
 * Get initials from name
 */
export const getInitials = (firstName: string, lastName: string): string => {
  const first = firstName?.charAt(0).toUpperCase() || '';
  const last = lastName?.charAt(0).toUpperCase() || '';
  return `${first}${last}`;
};

/**
 * Validate email
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate phone number
 */
export const isValidPhone = (phone: string): boolean => {
  const phoneRegex = /^\+?[1-9]\d{1,14}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};

/**
 * Get error message from API response
 */
export const getErrorMessage = (error: any): string => {
  if (typeof error === 'string') return error;
  if (error?.response?.data?.message) return error.response.data.message;
  if (error?.response?.data?.error) return error.response.data.error;
  if (error?.message) return error.message;
  return 'An error occurred. Please try again.';
};

/**
 * Sleep utility for async operations
 */
export const sleep = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

