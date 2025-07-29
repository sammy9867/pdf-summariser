import { useState, useEffect } from 'react';
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
  const [eventSource, setEventSource] = useState<EventSource | null>(null);

  const startStream = (documentUuid: string) => {
    if (eventSource) {
      eventSource.close();
    }

    setSummary('');
    setError(null);
    setIsStreaming(true);

    const source = api.streamSummary(documentUuid);
    setEventSource(source);

    source.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'end') {
          setIsStreaming(false);
          source.close();
          setEventSource(null);
        } else if (data.type === 'error') {
          setError(data.error || 'An error occurred during streaming');
          setIsStreaming(false);
          source.close();
          setEventSource(null);
        } else if (data.type === 'summary' && data.summary) {
          setSummary((prev: string) => prev + data.summary);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
        setError('Error parsing stream data');
        setIsStreaming(false);
        source.close();
        setEventSource(null);
      }
    };

    source.onerror = (e) => {
      console.error('SSE error:', e);
      setError('Error streaming summary');
      setIsStreaming(false);
      source.close();
      setEventSource(null);
    };
  };

  useEffect(() => {
    return () => {
      if (eventSource) {
        eventSource.close();
      }
    };
  }, [eventSource]);

  return {
    summary,
    isStreaming,
    error,
    startStream,
  };
};
