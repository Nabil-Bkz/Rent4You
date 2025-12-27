import apiClient from './client';
import { APIResponse } from '@/types';

export interface Statistics {
  vehicles?: {
    total: number;
    available: number;
    unavailable: number;
  };
  reservations?: {
    total: number;
    confirmed: number;
    active: number;
    completed: number;
    cancelled: number;
    recent_30_days: number;
  };
  revenue?: {
    total: number;
    average: number;
  };
  customers?: {
    unique: number;
  };
  overview?: {
    agencies: number;
    vehicles: number;
    users: number;
    renters: number;
  };
  monthly_stats?: Array<{
    month: string;
    reservations: number;
    revenue: number;
  }>;
}

export const statisticsAPI = {
  getStatistics: async (startDate?: string, endDate?: string): Promise<Statistics> => {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await apiClient.get<APIResponse<Statistics>>('/statistics/', { params });
    return response.data.data || response.data;
  },

  exportStatistics: async (format: 'excel' | 'pdf' = 'excel'): Promise<Blob> => {
    const response = await apiClient.get(`/statistics/export/?format=${format}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

