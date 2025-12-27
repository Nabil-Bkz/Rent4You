import apiClient from './client';
import { APIResponse, PaginatedResponse } from '@/types';

export interface Notification {
  id: number;
  type: string;
  type_display: string;
  title: string;
  message: string;
  is_read: boolean;
  related_object_type?: string;
  related_object_id?: number;
  created_at: string;
  read_at?: string;
}

export const notificationsAPI = {
  getNotifications: async (isRead?: boolean): Promise<Notification[]> => {
    const params = isRead !== undefined ? { is_read: isRead.toString() } : {};
    const response = await apiClient.get<APIResponse<Notification[]>>('/notifications/notifications/', { params });
    return response.data.data || response.data;
  },

  getUnreadCount: async (): Promise<number> => {
    const response = await apiClient.get<APIResponse<{ count: number }>>('/notifications/notifications/unread_count/');
    return response.data.data?.count || 0;
  },

  markAsRead: async (notificationId: number): Promise<void> => {
    await apiClient.post(`/notifications/notifications/${notificationId}/mark_read/`);
  },

  markAllAsRead: async (): Promise<void> => {
    await apiClient.post('/notifications/notifications/mark_all_read/', { mark_all: true });
  },
};

