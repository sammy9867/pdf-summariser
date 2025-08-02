import { renderHook, waitFor, act } from '@testing-library/react';
import { useUploadDocument } from '../../hooks/useUploadDocument';
import { TestQueryWrapper } from '../__mocks__/react-query';
import { server } from '../__mocks__/server';
import { Response } from 'miragejs';

describe('useUploadDocument', () => {
  const mockFile = new File(['content'], 'test.pdf', { type: 'application/pdf' });

  it('should upload document successfully', async () => {
    const { result } = renderHook(() => useUploadDocument(), {
      wrapper: TestQueryWrapper,
    });

    act(() => {
      result.current.mutate(mockFile);
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.isPending).toBe(false);
    expect(result.current.data).toHaveProperty('uuid');
    expect(result.current.data).toHaveProperty('uploaded_file');
  });

  it('should handle upload error', async () => {
    server.post('/documents/upload', () => {
      return new Response(400, {}, { error: 'Upload failed' });
    });

    const { result } = renderHook(() => useUploadDocument(), {
      wrapper: TestQueryWrapper,
    });

    act(() => {
      result.current.mutate(mockFile);
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.isPending).toBe(false);
    expect(result.current.error).toBeTruthy();
  });
});
