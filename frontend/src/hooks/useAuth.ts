/**
 * Custom hook for authentication
 */
import { useAuth as useAuthContext } from '@/contexts/AuthContext';
import { UserRole } from '@/types';

export const useAuth = () => {
  const auth = useAuthContext();
  
  const hasRole = (role: UserRole): boolean => {
    return auth.user?.role === role;
  };
  
  const isAgencyStaff = (): boolean => {
    if (auth.user) {
      const role = auth.user.role;
      return ['OWNER', 'SECRETARY', 'MECHANIC', 'AGENCY_ADMIN'].includes(role);
    }
    return false;
  };
  
  const isAdmin = (): boolean => {
    return hasRole('ADMIN');
  };
  
  const isOwner = (): boolean => {
    return hasRole('OWNER');
  };
  
  const isSecretary = (): boolean => {
    return hasRole('SECRETARY');
  };
  
  const isRenter = (): boolean => {
    return hasRole('RENTER');
  };
  
  return {
    ...auth,
    hasRole,
    isAgencyStaff,
    isAdmin,
    isOwner,
    isSecretary,
    isRenter,
  };
};

