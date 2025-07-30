import { Document } from '../types';

const API_BASE = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

export const api = {
  getDocuments: async (): Promise<Document[]> => {
    const response = await fetch(`${API_BASE}/documents`, {
      credentials: 'include',
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to fetch documents: ${errorText}`);
    }
    return response.json();
  },

  uploadDocument: async (file: File): Promise<Document> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/documents/upload`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to upload document: ${errorText}`);
    }

    return response.json();
  },

  streamSummary: (documentUuid: string): EventSource => {
    return new EventSource(`${API_BASE}/documents/${documentUuid}/stream`, {
      withCredentials: true,
    });
  },
};
