import React, { useState } from 'react';
import { UploadZone } from '../UploadZone';
import { SummaryViewer } from '../SummaryViewer';
import { DocumentsList } from '../DocumentsList';
import { Document } from '../../types';
import './index.css';

export const MainContent: React.FC = () => {
  const [selectedDocumentUuid, setSelectedDocumentUuid] = useState<string | null>(null);
  const [selectedDocumentName, setSelectedDocumentName] = useState<string>('');

  const handleUploadSuccess = (document: Document) => {
    setSelectedDocumentUuid(document.uuid);
    setSelectedDocumentName(document.uploaded_file.name);
  };

  const handleDocumentSelect = (documentId: string, documentName: string) => {
    setSelectedDocumentUuid(documentId);
    setSelectedDocumentName(documentName);
  };

  return (
    <div className="main-content">
      <div className="main-content-top">
        <div className="main-content-left">
          <UploadZone onUploadSuccess={handleUploadSuccess} />
        </div>
        <div className="main-content-right">
          <SummaryViewer
            documentUuid={selectedDocumentUuid}
            documentName={selectedDocumentName}
          />
        </div>
      </div>

      <div className="main-content-bottom">
        <DocumentsList
          onDocumentSelect={handleDocumentSelect}
          selectedDocumentUuid={selectedDocumentUuid || undefined}
        />
      </div>
    </div>
  );
};
