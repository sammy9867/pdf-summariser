import { Document } from '../types';

const API_BASE = '/api/v1';

export const api = {
  getDocuments: async (): Promise<Document[]> => {
    const response = await fetch(`${API_BASE}/documents`);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch documents: ${errorText}`);
    }
    return response.json();
  },
};
