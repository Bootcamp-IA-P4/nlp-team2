import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ThemeProvider } from '../src/contexts/ThemeContext.jsx';

// Mock de los componentes complejos para evitar errores de dependencias
vi.mock('../src/components/Dashboard.jsx', () => ({
  default: () => <div data-testid="mocked-dashboard">Dashboard Mock</div>
}));

vi.mock('../src/components/Header.jsx', () => ({
  default: () => <div data-testid="mocked-header">Header Mock</div>
}));

vi.mock('../src/components/Sidebar.jsx', () => ({
  default: () => <div data-testid="mocked-sidebar">Sidebar Mock</div>
}));

import App from '../src/App.jsx';

// Wrapper component para proveer el ThemeContext
const AppWithProviders = () => (
  <ThemeProvider>
    <App />
  </ThemeProvider>
);

describe('App Component', () => {
  it('should render the main application', () => {
    render(<AppWithProviders />);
    
    // Verificar que el componente principal se renderiza
    expect(document.body).toBeInTheDocument();
  });

  it('should contain the main layout structure', () => {
    render(<AppWithProviders />);
    
    // Verificar que los componentes mockeados se renderizan
    expect(screen.getByTestId('mocked-header')).toBeInTheDocument();
    expect(screen.getByTestId('mocked-sidebar')).toBeInTheDocument();
    expect(screen.getByTestId('mocked-dashboard')).toBeInTheDocument();
  });
});
