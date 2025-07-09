import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock de los hooks de API
vi.mock('../../src/hooks/useApiData.js', () => ({
  useDashboardStats: vi.fn(),
  useToxicityStats: vi.fn()
}));

// Mock de useAppInfo
vi.mock('../../src/hooks/useAppInfo.js', () => ({
  useAppInfo: vi.fn(),
  usePageTitle: vi.fn()
}));

import Dashboard from '../../src/components/Dashboard.jsx';
import { useDashboardStats, useToxicityStats } from '../../src/hooks/useApiData.js';
import { useAppInfo } from '../../src/hooks/useAppInfo.js';

// Obtener referencias a los mocks
const mockUseDashboardStats = vi.mocked(useDashboardStats);
const mockUseToxicityStats = vi.mocked(useToxicityStats);
const mockUseAppInfo = vi.mocked(useAppInfo);

// Mock de Recharts
vi.mock('recharts', () => ({
  BarChart: () => <div data-testid="bar-chart"></div>,
  Bar: () => <div data-testid="bar"></div>,
  XAxis: () => <div data-testid="x-axis"></div>,
  YAxis: () => <div data-testid="y-axis"></div>,
  CartesianGrid: () => <div data-testid="cartesian-grid"></div>,
  Tooltip: () => <div data-testid="tooltip"></div>,
  ResponsiveContainer: ({ children }) => <div data-testid="responsive-container">{children}</div>,
  PieChart: ({ children }) => <div data-testid="pie-chart">{children}</div>,
  Pie: () => <div data-testid="pie"></div>,
  Cell: () => <div data-testid="cell"></div>,
  LineChart: ({ children }) => <div data-testid="line-chart">{children}</div>,
  Line: () => <div data-testid="line"></div>,
  AreaChart: ({ children }) => <div data-testid="area-chart">{children}</div>,
  Area: () => <div data-testid="area"></div>
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
    
    // Reset mocks to return successful data
    mockUseDashboardStats.mockReturnValue({
      stats: {
        totalVideos: 1247,
        totalComments: 45632,
        averageToxicity: 23.5,
        safeVideos: 954,
        lastUpdate: '2025-01-09T10:15:00Z',
        recentAnalysis: [
          {
            id: 1,
            videoTitle: 'Test Video 1',
            toxicityRate: 12.5,
            comments: 234,
            totalComments: 234,
            timestamp: '2025-01-09 10:30'
          }
        ]
      },
      loading: false,
      error: null
    });

    mockUseToxicityStats.mockReturnValue({
      categoriesDistribution: [],
      severityDistribution: [],
      totalToxic: 10742,
      totalAnalyzed: 45632,
      recentToxicityTrends: [],
      loading: false
    });

    mockUseAppInfo.mockReturnValue({
      title: "Dashboard General - Análisis de Toxicidad",
      version: "1.0.0",
      description: "Resumen completo del estado de toxicidad y estadísticas generales de análisis",
      authors: "NLP Team 2",
      isLoading: false,
      error: null
    });
  });

  it('should render dashboard header', () => {
    render(<Dashboard />);
    expect(screen.getByText(/Dashboard General/i)).toBeInTheDocument();
  });

  it('should render key stats', () => {
    render(<Dashboard />);
    expect(screen.getByText(/Videos Analizados/i)).toBeInTheDocument();

    // Usar getAllByText para elementos duplicados como "Comentarios"
    const comentariosElements = screen.getAllByText(/Comentarios/i);
    expect(comentariosElements.length).toBeGreaterThan(0); // Al menos uno debe existir

    expect(screen.getByText(/Casos Tóxicos/i)).toBeInTheDocument();

    // Verificar datos numéricos básicos que vimos en el HTML
    expect(screen.getByText('1247')).toBeInTheDocument(); // totalVideos
    expect(screen.getByText('45.632')).toBeInTheDocument(); // totalComments
  });

  it('should render charts', () => {
    render(<Dashboard />);
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
  });

  it('should not show loading state', () => {
    render(<Dashboard />);
    expect(screen.queryByText(/Cargando/i)).not.toBeInTheDocument();
  });


});
