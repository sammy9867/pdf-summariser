import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MainContent } from '../../components/MainContent';
import { TestQueryWrapper } from '../__mocks__/react-query';

jest.mock('../../components/UploadZone', () => ({
  UploadZone: ({ onUploadSuccess }: { onUploadSuccess: (doc: any) => void }) => (
    <div data-testid='upload-zone'>
      <button
        onClick={() => onUploadSuccess({ uuid: 'test-uuid', uploaded_file: { name: 'test.pdf' } })}
      >
        Upload
      </button>
    </div>
  ),
}));

jest.mock('../../components/SummaryViewer', () => ({
  SummaryViewer: ({
    documentUuid,
    documentName,
  }: {
    documentUuid: string | null;
    documentName?: string;
  }) => (
    <div data-testid='summary-viewer'>
      {documentUuid ? `${documentName} (${documentUuid})` : 'No document'}
    </div>
  ),
}));

jest.mock('../../components/DocumentsList', () => ({
  DocumentsList: ({
    onDocumentSelect,
    selectedDocumentUuid,
  }: {
    onDocumentSelect: (id: string, name: string) => void;
    selectedDocumentUuid?: string;
  }) => (
    <div data-testid='documents-list'>
      <div>Selected: {selectedDocumentUuid || 'None'}</div>
      <button onClick={() => onDocumentSelect('doc-1', 'doc1.pdf')}>Select Document</button>
    </div>
  ),
}));

describe('MainContent', () => {
  it('should render all components', () => {
    render(
      <TestQueryWrapper>
        <MainContent />
      </TestQueryWrapper>
    );

    expect(screen.getByTestId('upload-zone')).toBeInTheDocument();
    expect(screen.getByTestId('summary-viewer')).toBeInTheDocument();
    expect(screen.getByTestId('documents-list')).toBeInTheDocument();
  });

  it('should handle document upload', () => {
    render(
      <TestQueryWrapper>
        <MainContent />
      </TestQueryWrapper>
    );

    fireEvent.click(screen.getByText('Upload'));

    expect(screen.getByTestId('summary-viewer')).toHaveTextContent('test.pdf (test-uuid)');
    expect(screen.getByText('Selected: test-uuid')).toBeInTheDocument();
  });

  it('should handle document selection', () => {
    render(
      <TestQueryWrapper>
        <MainContent />
      </TestQueryWrapper>
    );

    fireEvent.click(screen.getByText('Select Document'));

    expect(screen.getByTestId('summary-viewer')).toHaveTextContent('doc1.pdf (doc-1)');
    expect(screen.getByText('Selected: doc-1')).toBeInTheDocument();
  });
});
