import apiClient from './client';

export interface Reservation {
  id: number;
  date_debut: string;
  date_fin: string;
  prix: number;
  prix_original: number;
  reduction: number;
  status: string;
  locataire: number;
  vehicule: number;
  code_promo?: number;
  vehicule_details?: any;
}

export const reservationsAPI = {
  getAll: async () => {
    const response = await apiClient.get<Reservation[]>('/reservations/reservations/');
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Reservation>(`/reservations/reservations/${id}/`);
    return response.data;
  },

  create: async (data: {
    date_debut: string;
    date_fin: string;
    vehicule: number;
    code_promo?: string;
  }) => {
    const response = await apiClient.post<Reservation>('/reservations/reservations/', data);
    return response.data;
  },

  confirm: async (id: number) => {
    const response = await apiClient.post<Reservation>(`/reservations/reservations/${id}/confirm/`);
    return response.data;
  },

  cancel: async (id: number) => {
    const response = await apiClient.post<Reservation>(`/reservations/reservations/${id}/cancel/`);
    return response.data;
  },
};

