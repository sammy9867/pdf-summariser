import React, { useEffect, useRef } from 'react';
import { useDocumentSummary } from '../../hooks/useDocumentSummary';
import './index.css';

interface SummaryViewerProps {
  documentUuid: string | null;
  documentName?: string;
}

export const SummaryViewer: React.FC<SummaryViewerProps> = ({ documentUuid, documentName }) => {
  const { summary, isStreaming, error, startStream } = useDocumentSummary();
  const summaryRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (documentUuid) {
      startStream(documentUuid);
    }
  }, [documentUuid, startStream]);

  useEffect(() => {
    if (summaryRef.current && isStreaming) {
      summaryRef.current.scrollTop = summaryRef.current.scrollHeight;
    }
  }, [summary, isStreaming]);

  if (!documentUuid) {
    return (
      <div className='summary-viewer-container'>
        <h2 className='summary-viewer-title'>AI Summary</h2>
        <div className='summary-placeholder'>
          <div className='summary-placeholder-icon'>🤖</div>
          <p>Upload a PDF or select a document to see its AI-generated summary</p>
        </div>
      </div>
    );
  }

  return (
    <div className='summary-viewer-container'>
      <h2 className='summary-viewer-title'>AI Summary</h2>
      {documentName && (
        <div className='summary-document-info'>
          <span className='summary-document-name'>📄 {documentName}</span>
          {isStreaming && <span className='summary-streaming-indicator'>✨ Generating...</span>}
        </div>
      )}

      <div className='summary-content' ref={summaryRef}>
        {error ? (
          <div className='summary-error'>
            <p>❌ {error}</p>
            <button
              className='summary-retry-button'
              onClick={() => documentUuid && startStream(documentUuid)}
            >
              Retry
            </button>
          </div>
        ) : (
          <>
            {summary ? (
              <div className='summary-text'>
                {summary.split('\n').map((paragraph, index) => (
                  <p key={index} className='summary-paragraph'>
                    {paragraph}
                  </p>
                ))}
              </div>
            ) : isStreaming ? (
              <div className='summary-loading'>
                <div className='summary-dots'>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <p>Analyzing document and generating summary...</p>
              </div>
            ) : (
              <div className='summary-placeholder'>
                <p>No summary available</p>
              </div>
            )}

            {isStreaming && summary && <div className='summary-cursor'>▌</div>}
          </>
        )}
      </div>
    </div>
  );
};
