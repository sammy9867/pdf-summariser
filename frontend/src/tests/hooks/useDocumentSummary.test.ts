import { faker } from '@faker-js/faker';
import { renderHook, act } from '@testing-library/react';
import { useDocumentSummary } from '../../hooks/useDocumentSummary';

// Mock EventSource
let mockEventSource: any;

beforeEach(() => {
  mockEventSource = {
    close: jest.fn(),
    onmessage: null as ((event: MessageEvent) => void) | null,
    onerror: null as ((event: Event) => void) | null,
  };

  (global.EventSource as any) = jest.fn(() => mockEventSource);
});

describe('useDocumentSummary', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    if (mockEventSource) {
      mockEventSource.onmessage = null;
      mockEventSource.onerror = null;
    }
  });

  it('should start streaming', () => {
    const { result } = renderHook(() => useDocumentSummary());
    const documentUuid = faker.string.uuid();

    act(() => {
      result.current.startStream(documentUuid);
    });

    expect(global.EventSource).toHaveBeenCalledWith(
      `http://localhost:8000/api/v1/documents/${documentUuid}/stream`,
      { withCredentials: true }
    );
    expect(result.current.isStreaming).toBe(true);
  });

  it('should handle summary messages', () => {
    const { result } = renderHook(() => useDocumentSummary());
    const summaryText = faker.lorem.paragraph();

    act(() => {
      result.current.startStream(faker.string.uuid());
    });

    const summaryMessage = {
      data: JSON.stringify({ type: 'summary', summary: summaryText })
    } as MessageEvent;

    act(() => {
      if (mockEventSource.onmessage) {
        mockEventSource.onmessage(summaryMessage);
      }
    });

    expect(result.current.summary).toBe(summaryText);
  });

  it('should handle end message', () => {
    const { result } = renderHook(() => useDocumentSummary());

    act(() => {
      result.current.startStream(faker.string.uuid());
    });

    const endMessage = {
      data: JSON.stringify({ type: 'end' })
    } as MessageEvent;

    act(() => {
      if (mockEventSource.onmessage) {
        mockEventSource.onmessage(endMessage);
      }
    });

    expect(result.current.isStreaming).toBe(false);
    expect(mockEventSource.close).toHaveBeenCalled();
  });

  it('should handle error messages', () => {
    const { result } = renderHook(() => useDocumentSummary());
    const errorText = faker.lorem.sentence();

    act(() => {
      result.current.startStream(faker.string.uuid());
    });

    const errorMessage = {
      data: JSON.stringify({ type: 'error', error: errorText })
    } as MessageEvent;

    act(() => {
      if (mockEventSource.onmessage) {
        mockEventSource.onmessage(errorMessage);
      }
    });

    expect(result.current.error).toBe(errorText);
    expect(result.current.isStreaming).toBe(false);
  });
});
