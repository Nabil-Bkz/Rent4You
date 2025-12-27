import apiClient from './client';

export interface Complaint {
  id: number;
  contenu_reclamation: string;
  status: string;
  locataire: number;
  agence: number;
  reservation?: number;
  reponse?: string;
}

export interface Report {
  id: number;
  description: string;
  type_rapport: string;
  images: string[];
  locataire: number;
  agence: number;
  reservation: number;
  vehicule: number;
}

export const complaintsAPI = {
  getAll: async () => {
    const response = await apiClient.get<Complaint[]>('/complaints/reclamations/');
    return response.data;
  },

  create: async (data: {
    contenu_reclamation: string;
    agence: number;
    reservation?: number;
  }) => {
    const response = await apiClient.post<Complaint>('/complaints/reclamations/', data);
    return response.data;
  },

  resolve: async (id: number, reponse: string) => {
    const response = await apiClient.post<Complaint>(`/complaints/reclamations/${id}/resolve/`, {
      reponse,
    });
    return response.data;
  },

  createReport: async (data: {
    description: string;
    type_rapport: string;
    images: string[];
    agence: number;
    reservation: number;
    vehicule: number;
  }) => {
    const response = await apiClient.post<Report>('/complaints/rapports/', data);
    return response.data;
  },
};

