import apiClient from './client';
import Cookies from 'js-cookie';
import { COOKIE_NAMES } from '@/constants';
import { LoginCredentials, RegisterData, AuthResponse, APIResponse, User } from '@/types';

// Types are now imported from @/types

export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<APIResponse<AuthResponse>>('/accounts/login/', credentials);
    const authData = response.data.data || response.data;
    const { tokens, user, profile } = authData;
    
    // Store tokens in cookies
    Cookies.set(COOKIE_NAMES.ACCESS_TOKEN, tokens.access, { expires: 1 });
    Cookies.set(COOKIE_NAMES.REFRESH_TOKEN, tokens.refresh, { expires: 7 });
    
    return authData;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post<APIResponse<AuthResponse>>('/accounts/register/', data);
    const authData = response.data.data || response.data;
    const { tokens } = authData;
    
    // Store tokens in cookies
    Cookies.set(COOKIE_NAMES.ACCESS_TOKEN, tokens.access, { expires: 1 });
    Cookies.set(COOKIE_NAMES.REFRESH_TOKEN, tokens.refresh, { expires: 7 });
    
    return authData;
  },

  logout: () => {
    Cookies.remove(COOKIE_NAMES.ACCESS_TOKEN);
    Cookies.remove(COOKIE_NAMES.REFRESH_TOKEN);
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<APIResponse<User>>('/accounts/users/me/');
    return response.data.data || response.data;
  },

  updateProfile: async (data: Partial<RegisterData>): Promise<User> => {
    const response = await apiClient.put<APIResponse<User>>('/accounts/users/update_profile/', data);
    return response.data.data || response.data;
  },

  changePassword: async (
    oldPassword: string, 
    newPassword: string, 
    newPasswordConfirm: string
  ): Promise<void> => {
    await apiClient.post<APIResponse>('/accounts/users/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
  },
};

