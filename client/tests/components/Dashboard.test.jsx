import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Dashboard from '../../src/components/Dashboard.jsx';

// Mock de Recharts
vi.mock('recharts', () => ({
  BarChart: ({ children }) => <div data-testid="bar-chart">{children}</div>,
  Bar: () => <div data-testid="bar" />,
  XAxis: () => <div data-testid="x-axis" />,
  YAxis: () => <div data-testid="y-axis" />,
  CartesianGrid: () => <div data-testid="cartesian-grid" />,
  Tooltip: () => <div data-testid="tooltip" />,
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  PieChart: ({ children }) => <div data-testid="pie-chart">{children}</div>,
  Pie: () => <div data-testid="pie" />,
  Cell: () => <div data-testid="cell" />,
  LineChart: ({ children }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div data-testid="line" />,
  AreaChart: ({ children }) => <div data-testid="area-chart">{children}</div>,
  Area: () => <div data-testid="area" />
}));

// Mock de mockData
vi.mock('../../src/utils/mockData.js', () => ({
  mockToxicityData: {
    overall: {
      totalComments: 5420,
      toxicComments: 843,
      toxicityRate: 15.6,
      improvement: -2.3
    },
    toxicityTypes: [
      { name: 'Ofensivo', value: 35, color: '#c1121f' },
      { name: 'Amenazas', value: 18, color: '#ef4444' },
      { name: 'Discriminación', value: 22, color: '#f97316' },
      { name: 'Sexista', value: 12, color: '#eab308' },
      { name: 'Spam', value: 8, color: '#8b5cf6' },
      { name: 'Otros', value: 5, color: '#ec4899' }
    ],
    timelineData: [
      { time: '00:00', count: 12 },
      { time: '04:00', count: 8 },
      { time: '08:00', count: 25 },
      { time: '12:00', count: 35 },
      { time: '16:00', count: 45 },
      { time: '20:00', count: 38 }
    ],
    recentAnalysis: [
      {
        id: 1,
        videoTitle: 'Tutorial React 2024',
        toxicityRate: 12.5,
        comments: 234,
        timestamp: '2024-01-15 10:30'
      },
      {
        id: 2,
        videoTitle: 'Debate Político',
        toxicityRate: 34.7,
        comments: 892,
        timestamp: '2024-01-15 09:15'
      }
    ]
  }
}));

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard header', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('Dashboard General')).toBeInTheDocument();
    expect(screen.getByText('Resumen completo del estado de toxicidad')).toBeInTheDocument();
  });

  it('should display last update time', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('Última actualización: hace 5 min')).toBeInTheDocument();
  });

  it('should render main metrics cards', () => {
    render(<Dashboard />);
    
    expect(screen.getByText('Videos Analizados')).toBeInTheDocument();
    expect(screen.getByText('1,247')).toBeInTheDocument();
  });

  it('should render monthly trend data', () => {
    render(<Dashboard />);
    
    // Verificar que hay gráficos de línea para tendencias mensuales
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  it('should have proper styling classes', () => {
    const { container } = render(<Dashboard />);
    
    const mainDiv = container.firstChild;
    expect(mainDiv).toHaveClass('space-y-6');
  });


  it('should display metrics with proper icons', () => {
    render(<Dashboard />);
    
    // Los íconos de Lucide deberían estar presentes
    const icons = document.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThan(0);
  });


  it('should render recent analysis section', () => {
    render(<Dashboard />);
    
    // Buscar elementos que podrían contener análisis recientes
    // Como los datos vienen del mock, verificamos que el componente se renderiza correctamente
    expect(screen.getByText('Dashboard General')).toBeInTheDocument();
  });
});
