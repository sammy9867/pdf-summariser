import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from '../utils/api';

interface UseSummaryResult {
  summary: string;
  isStreaming: boolean;
  error: string | null;
  startStream: (documentUuid: string) => void;
}

export const useDocumentSummary = (): UseSummaryResult => {
  const [summary, setSummary] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const startStream = useCallback((documentUuid: string) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    setSummary('');
    setError(null);
    setIsStreaming(true);

    const source = api.streamSummary(documentUuid);
    eventSourceRef.current = source;

    source.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'end') {
          setIsStreaming(false);
          source.close();
          eventSourceRef.current = null;
        } else if (data.type === 'error') {
          setError(data.error || 'An error occurred during streaming');
          setIsStreaming(false);
          source.close();
          eventSourceRef.current = null;
        } else if (data.type === 'summary' && data.summary) {
          setSummary((prev: string) => prev + data.summary);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
        setError('Error parsing stream data');
        setIsStreaming(false);
        source.close();
        eventSourceRef.current = null;
      }
    };

    source.onerror = (e) => {
      console.error('SSE error:', e);
      setError('Error streaming summary');
      setIsStreaming(false);
      source.close();
      eventSourceRef.current = null;
    };
  }, []);

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return {
    summary,
    isStreaming,
    error,
    startStream,
  };
};
