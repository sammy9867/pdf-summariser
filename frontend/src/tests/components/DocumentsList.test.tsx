import React from 'react';
import { render, screen } from '@testing-library/react';
import { DocumentsList } from '../../components/DocumentsList';
import { TestQueryWrapper } from '../__mocks__/react-query';

const mockOnDocumentSelect = jest.fn();

const mockUseDocuments = {
  data: [
    {
      created: '2024-01-01T00:00:00Z',
      uploaded_file: { name: 'test.pdf', size: 1024 },
      uuid: 'doc-1',
    },
  ],
  isLoading: false,
  error: null,
};

jest.mock('../../hooks/useDocuments', () => ({
  useDocuments: () => mockUseDocuments,
}));

describe('DocumentsList', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders documents list', () => {
    render(
      <TestQueryWrapper>
        <DocumentsList onDocumentSelect={mockOnDocumentSelect} />
      </TestQueryWrapper>
    );

    expect(screen.getByText('Your Documents (1)')).toBeInTheDocument();
    expect(screen.getByText('test.pdf')).toBeInTheDocument();
  });

  it('shows empty state when no documents', () => {
    jest.mocked(mockUseDocuments).data = [];

    render(
      <TestQueryWrapper>
        <DocumentsList onDocumentSelect={mockOnDocumentSelect} />
      </TestQueryWrapper>
    );

    expect(screen.getByText('No documents uploaded yet')).toBeInTheDocument();
  });
});
