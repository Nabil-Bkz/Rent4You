import apiClient from './client';

export interface Vehicle {
  id: number;
  matricule: string;
  marque: string;
  model: string;
  prix_heure: number;
  prix_jour: number;
  description: string;
  etat_vehicule: string;
  disponibilite: boolean;
  categorie_vehicule: string;
  depot?: number;
  agence: number;
  img_vhl?: string;
  image_url?: string;
}

export interface VehicleFilters {
  disponibilite?: boolean;
  categorie?: string;
  agence?: number;
  depot?: number;
  prix_min?: number;
  prix_max?: number;
  search?: string;
}

export const vehiclesAPI = {
  getAll: async (filters?: VehicleFilters) => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }
    const response = await apiClient.get<Vehicle[]>(`/vehicles/vehicules/?${params.toString()}`);
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Vehicle>(`/vehicles/vehicules/${id}/`);
    return response.data;
  },

  create: async (data: Partial<Vehicle>) => {
    const response = await apiClient.post<Vehicle>('/vehicles/vehicules/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<Vehicle>) => {
    const response = await apiClient.put<Vehicle>(`/vehicles/vehicules/${id}/`, data);
    return response.data;
  },

  updatePrice: async (id: number, prix_jour?: number, prix_heure?: number) => {
    const response = await apiClient.post(`/vehicles/vehicules/${id}/update_price/`, {
      prix_jour,
      prix_heure,
    });
    return response.data;
  },

  delete: async (id: number) => {
    await apiClient.delete(`/vehicles/vehicules/${id}/`);
  },
};

