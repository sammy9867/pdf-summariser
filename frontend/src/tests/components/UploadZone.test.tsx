import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UploadZone } from '../../components/UploadZone';
import { TestQueryWrapper } from '../__mocks__/react-query';

const mockOnUploadSuccess = jest.fn();

describe('UploadZone', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders upload interface', () => {
    render(
      <TestQueryWrapper>
        <UploadZone onUploadSuccess={mockOnUploadSuccess} />
      </TestQueryWrapper>
    );

    expect(screen.getByText('Upload PDF')).toBeInTheDocument();
    expect(screen.getByText(/drag & drop/i)).toBeInTheDocument();
  });

  it('handles file upload', async () => {
    render(
      <TestQueryWrapper>
        <UploadZone onUploadSuccess={mockOnUploadSuccess} />
      </TestQueryWrapper>
    );

    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    const mockFile = new File(['content'], 'test.pdf', { type: 'application/pdf' });

    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    await waitFor(() => {
      expect(mockOnUploadSuccess).toHaveBeenCalled();
    });
  });
});
