import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

// Test básico de componente React
const BasicTestComponent = ({ title = "Test Component" }) => {
  return <div data-testid="basic-component">{title}</div>;
};

describe('Basic Component Tests', () => {
  it('should render a basic component', () => {
    render(<BasicTestComponent />);
    
    expect(screen.getByTestId('basic-component')).toBeInTheDocument();
    expect(screen.getByText('Test Component')).toBeInTheDocument();
  });

  it('should accept props correctly', () => {
    const customTitle = "Custom Title";
    render(<BasicTestComponent title={customTitle} />);
    
    expect(screen.getByText(customTitle)).toBeInTheDocument();
  });

  it('should have proper structure', () => {
    render(<BasicTestComponent />);
    
    const component = screen.getByTestId('basic-component');
    expect(component).toBeInTheDocument();
    expect(component.tagName).toBe('DIV');
  });
});
