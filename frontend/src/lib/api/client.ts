import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from 'axios';
import Cookies from 'js-cookie';
import { API_CONFIG, COOKIE_NAMES, ERROR_MESSAGES } from '@/constants';
import { APIResponse } from '@/types';

const API_URL = API_CONFIG.BASE_URL;

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = Cookies.get(COOKIE_NAMES.ACCESS_TOKEN);
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh and errors
apiClient.interceptors.response.use(
  (response) => {
    // Transform response to match APIResponse format if needed
    if (response.data && !response.data.success && response.data.data) {
      return {
        ...response,
        data: {
          success: true,
          data: response.data.data,
          message: response.data.message,
        },
      };
    }
    return response;
  },
  async (error: AxiosError<APIResponse>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 Unauthorized - try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = Cookies.get(COOKIE_NAMES.REFRESH_TOKEN);
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          Cookies.set(COOKIE_NAMES.ACCESS_TOKEN, access);

          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access}`;
          }

          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        Cookies.remove(COOKIE_NAMES.ACCESS_TOKEN);
        Cookies.remove(COOKIE_NAMES.REFRESH_TOKEN);
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }

    // Transform error response
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.error || 
                        error.message || 
                        ERROR_MESSAGES.NETWORK_ERROR;

    return Promise.reject({
      ...error,
      message: errorMessage,
      response: error.response ? {
        ...error.response,
        data: {
          success: false,
          message: errorMessage,
          errors: error.response.data?.errors,
        },
      } : undefined,
    });
  }
);

export default apiClient;

