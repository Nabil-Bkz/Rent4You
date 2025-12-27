'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI, AuthResponse } from '@/lib/api/auth';
import Cookies from 'js-cookie';
import { User, UserProfile, UserRole } from '@/types';
import { COOKIE_NAMES } from '@/constants';

interface AuthContextType {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  hasRole: (role: UserRole) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = Cookies.get(COOKIE_NAMES.ACCESS_TOKEN);
    if (token) {
      loadUser();
    } else {
      setLoading(false);
    }
  }, []);

  const loadUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
      // Load profile based on role if needed
    } catch (error) {
      console.error('Failed to load user:', error);
      Cookies.remove(COOKIE_NAMES.ACCESS_TOKEN);
      Cookies.remove(COOKIE_NAMES.REFRESH_TOKEN);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response: AuthResponse = await authAPI.login({ email, password });
    setUser(response.user);
    setProfile(response.profile || null);
  };

  const register = async (data: any) => {
    const response: AuthResponse = await authAPI.register(data);
    setUser(response.user);
    setProfile(response.profile || null);
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
    setProfile(null);
  };

  const isAuthenticated = !!user;
  
  const hasRole = (role: UserRole): boolean => {
    return user?.role === role;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        login,
        register,
        logout,
        isAuthenticated,
        hasRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

