import { faker } from '@faker-js/faker';
import { api } from '../../utils/api';
import { server } from '../__mocks__/server';
import { Response } from 'miragejs';

// Mock EventSource
global.EventSource = jest.fn(() => ({
  close: jest.fn(),
  onmessage: null,
  onerror: null,
})) as any;

describe('API Utils', () => {
  describe('getDocuments', () => {
    it('should fetch documents successfully', async () => {
      const documents = await api.getDocuments();

      expect(documents).toHaveLength(2); // We seed with 2 documents
      expect(documents[0]).toHaveProperty('uuid');
      expect(documents[0]).toHaveProperty('uploaded_file');
    });

    it('should handle fetch error', async () => {
      server.get('/documents', () => {
        return new Response(500, {}, { error: 'Server Error' });
      });

      await expect(api.getDocuments()).rejects.toThrow('Failed to fetch documents');
    });
  });

  describe('uploadDocument', () => {
    it('should upload document successfully', async () => {
      const fileName = `${faker.system.fileName()}.pdf`;
      const mockFile = new File(['content'], fileName, { type: 'application/pdf' });

      const result = await api.uploadDocument(mockFile);

      expect(result).toHaveProperty('uuid');
      expect(result).toHaveProperty('uploaded_file');
      expect(result.uploaded_file).toHaveProperty('name');
    });

    it('should handle upload error', async () => {
      server.post('/documents/upload', () => {
        return new Response(400, {}, { error: 'Upload failed' });
      });

      const mockFile = new File(['content'], faker.system.fileName(), { type: 'application/pdf' });
      await expect(api.uploadDocument(mockFile)).rejects.toThrow('Failed to upload document');
    });
  });

  describe('streamSummary', () => {
    it('should create EventSource with correct URL and options', () => {
      const documentUuid = faker.string.uuid();
      api.streamSummary(documentUuid);

      expect(global.EventSource).toHaveBeenCalledWith(
        `http://localhost:8000/api/v1/documents/${documentUuid}/stream`,
        { withCredentials: true }
      );
    });
  });
});
