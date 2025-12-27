import apiClient from './client';

export interface Contract {
  id: number;
  reservation: number;
  pdf_file?: string;
  pdf_url?: string;
  status: string;
  signed_at?: string;
  signature_locataire?: string;
}

export const contractsAPI = {
  getAll: async () => {
    const response = await apiClient.get<Contract[]>('/contracts/contrats/');
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Contract>(`/contracts/contrats/${id}/`);
    return response.data;
  },

  create: async (data: { reservation: number }) => {
    const response = await apiClient.post<Contract>('/contracts/contrats/', data);
    return response.data;
  },

  sign: async (id: number, signature: string) => {
    const response = await apiClient.post<Contract>(`/contracts/contrats/${id}/sign/`, {
      signature,
    });
    return response.data;
  },
};

