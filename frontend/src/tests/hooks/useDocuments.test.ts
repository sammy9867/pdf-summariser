import { renderHook, waitFor } from '@testing-library/react';
import { useDocuments } from '../../hooks/useDocuments';
import { TestQueryWrapper } from '../__mocks__/react-query';
import { server } from '../__mocks__/server';
import { Response } from 'miragejs';

describe('useDocuments', () => {
  it('should fetch documents successfully', async () => {
    const { result } = renderHook(() => useDocuments(), {
      wrapper: TestQueryWrapper,
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toHaveLength(2); // We seed with 2 documents
    expect(result.current.isSuccess).toBe(true);
    expect(result.current.data?.[0]).toHaveProperty('uuid');
    expect(result.current.data?.[0]).toHaveProperty('uploaded_file');
  });

  it('should handle fetch error', async () => {
    server.get('/documents', () => {
      return new Response(500, {}, { error: 'Server Error' });
    });

    const { result } = renderHook(() => useDocuments(), {
      wrapper: TestQueryWrapper,
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.isError).toBe(true);
    expect(result.current.error).toBeTruthy();
  });
});
