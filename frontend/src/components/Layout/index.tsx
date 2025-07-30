import React from 'react';
import './index.css';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="layout">
      <header className="layout-header">
        <h1 className="layout-title">PDF Summarizer</h1>
        <p className="layout-subtitle">Upload, Analyze & Summarize PDFs in Real-time</p>
      </header>
      <main className="layout-main">
        {children}
      </main>
    </div>
  );
};
