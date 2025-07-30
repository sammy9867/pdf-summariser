import React, { useCallback, useState } from 'react';
import { useUploadDocument } from '../../hooks/useUploadDocument';
import { Document } from '../../types';
import './index.css';

interface UploadZoneProps {
  onUploadSuccess: (document: Document) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUploadSuccess }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const uploadMutation = useUploadDocument();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);

    const files = Array.from(e.dataTransfer.files);
    const pdfFile = files.find(file => file.type === 'application/pdf');

    if (pdfFile) {
      uploadMutation.mutate(pdfFile, {
        onSuccess: (document) => {
          onUploadSuccess(document);
        }
      });
    }
  }, [uploadMutation, onUploadSuccess]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      uploadMutation.mutate(file, {
        onSuccess: (document) => {
          onUploadSuccess(document);
        }
      });
    }
    e.target.value = '';
  }, [uploadMutation, onUploadSuccess]);

  return (
    <div className="upload-zone-container">
      <h2 className="upload-zone-title">Upload PDF</h2>
      <div
        className={`upload-zone ${isDragOver ? 'drag-over' : ''} ${uploadMutation.isPending ? 'uploading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {uploadMutation.isPending ? (
          <div className="upload-progress">
            <div className="spinner"></div>
            <p>Uploading PDF...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📄</div>
            <p className="upload-text">
              Drag & drop your PDF here or{' '}
              <label className="upload-button">
                browse files
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="upload-input"
                />
              </label>
            </p>
            <p className="upload-hint">Only PDF files are supported</p>
          </>
        )}
      </div>

      {uploadMutation.isError && (
        <div className="upload-error">
          <p>❌ {uploadMutation.error?.message || 'Upload failed'}</p>
        </div>
      )}
    </div>
  );
};
