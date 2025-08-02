import React from 'react';
import { render, screen } from '@testing-library/react';
import { SummaryViewer } from '../../components/SummaryViewer';

// Mock the hook
jest.mock('../../hooks/useDocumentSummary', () => ({
  useDocumentSummary: () => ({
    summary: 'Test summary content',
    isStreaming: false,
    error: null,
    startStream: jest.fn(),
  }),
}));

describe('SummaryViewer', () => {
  it('renders placeholder when no document', () => {
    render(<SummaryViewer documentUuid={null} />);

    expect(screen.getByText('AI Summary')).toBeInTheDocument();
    expect(screen.getByText(/upload a PDF/i)).toBeInTheDocument();
  });

  it('renders summary content when document provided', () => {
    render(<SummaryViewer documentUuid="test-id" documentName="test.pdf" />);

    expect(screen.getByText('AI Summary')).toBeInTheDocument();
    expect(screen.getByText('📄 test.pdf')).toBeInTheDocument();
  });
});
