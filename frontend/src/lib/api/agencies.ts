import apiClient from './client';

export interface Agency {
  id: number;
  nom_agence: string;
  siege_agence: string;
  num_contact: string;
  email_agence: string;
  nmbr_succursales: number;
  nmbr_flotte: number;
  logo_agence?: string;
  logo_url?: string;
  is_active: boolean;
}

export interface PartnershipRequest {
  nom_prop: string;
  prenom_prop: string;
  ddn_prop: string;
  email_prop: string;
  phone_prop: string;
  password: string;
  nom_agence: string;
  siege_agence: string;
  num_contact: string;
  email_agence: string;
  nmbr_succursales: number;
  nmbr_flotte: number;
}

export const agenciesAPI = {
  getAll: async () => {
    const response = await apiClient.get<Agency[]>('/agencies/agences/');
    return response.data;
  },

  getActive: async () => {
    const response = await apiClient.get<Agency[]>('/agencies/agences/active/');
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Agency>(`/agencies/agences/${id}/`);
    return response.data;
  },

  createPartnershipRequest: async (data: PartnershipRequest) => {
    const response = await apiClient.post('/agencies/partenariats/', data);
    return response.data;
  },

  approvePartnership: async (id: number) => {
    const response = await apiClient.post(`/agencies/partenariats/${id}/approve/`);
    return response.data;
  },

  rejectPartnership: async (id: number) => {
    const response = await apiClient.post(`/agencies/partenariats/${id}/reject/`);
    return response.data;
  },
};

