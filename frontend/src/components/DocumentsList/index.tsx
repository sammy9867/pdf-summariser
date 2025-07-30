import React from 'react';
import { useDocuments } from '../../hooks/useDocuments';
import { Document } from '../../types';
import './index.css';

interface DocumentsListProps {
  onDocumentSelect: (documentUuid: string, documentName: string) => void;
  selectedDocumentUuid?: string;
}

export const DocumentsList: React.FC<DocumentsListProps> = ({ 
  onDocumentSelect, 
  selectedDocumentUuid 
}) => {
  const { data: documents, isLoading, error } = useDocuments();

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  if (isLoading) {
    return (
      <div className="documents-list-container">
        <h2 className="documents-list-title">Your Documents</h2>
        <div className="documents-loading">
          <div className="documents-spinner"></div>
          <p>Loading documents...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="documents-list-container">
        <h2 className="documents-list-title">Your Documents</h2>
        <div className="documents-error">
          <p>❌ Failed to load documents</p>
        </div>
      </div>
    );
  }

  if (!documents || documents.length === 0) {
    return (
      <div className="documents-list-container">
        <h2 className="documents-list-title">Your Documents</h2>
        <div className="documents-empty">
          <div className="documents-empty-icon">📂</div>
          <p>No documents uploaded yet</p>
          <p className="documents-empty-hint">Upload your first PDF to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="documents-list-container">
      <h2 className="documents-list-title">Your Documents ({documents.length})</h2>
      <div className="documents-grid">
        {documents.map((document: Document) => (
          <div
            key={document.uuid}
            className={`document-card ${selectedDocumentUuid === document.uuid ? 'selected' : ''}`}
            onClick={() => onDocumentSelect(document.uuid, document.uploaded_file.name)}
          >
            <div className="document-card-header">
              <div className="document-icon">📄</div>
              <div className="document-status">
                {selectedDocumentUuid === document.uuid && (
                  <span className="document-active">● Active</span>
                )}
              </div>
            </div>
            
            <div className="document-info">
              <h3 className="document-name" title={document.uploaded_file.name}>
                {document.uploaded_file.name}
              </h3>
              <div className="document-meta">
                <span className="document-size">
                  {formatFileSize(document.uploaded_file.size)}
                </span>
                <span className="document-date">
                  {formatDate(document.created)}
                </span>
              </div>
            </div>
            
            <div className="document-card-footer">
              <button className="document-action-button">
                ✨ Summarize
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
