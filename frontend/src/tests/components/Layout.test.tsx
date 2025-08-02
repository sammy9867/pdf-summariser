import { render, screen } from '@testing-library/react';
import { Layout } from '../../components/Layout';

describe('Layout', () => {
  it('should render header and children', () => {
    render(
      <Layout>
        <div>Test Content</div>
      </Layout>
    );

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('PDF Summariser');
    expect(screen.getByText('Upload, Analyze & Summarize PDFs in Real-time')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('should have correct structure', () => {
    const { container } = render(
      <Layout>
        <div>Content</div>
      </Layout>
    );

    expect(container.firstChild).toHaveClass('layout');
    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByRole('main')).toBeInTheDocument();
  });
});
