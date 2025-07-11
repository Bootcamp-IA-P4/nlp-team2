import { vi } from 'vitest';

// Mock de datos para el Dashboard
export const mockDashboardStats = {
  stats: {
    totalVideos: 1247,
    totalComentarios: 45632,
    toxicityRate: 23.5,
    lastUpdate: '2025-01-09T10:15:00Z'
  },
  loading: false,
  error: null
};

export const mockToxicityStats = {
  categoriesDistribution: [
    { name: 'Contenido Tóxico', value: 45, color: '#ef4444' },
    { name: 'Lenguaje Abusivo', value: 30, color: '#dc2626' },
    { name: 'Amenazas', value: 15, color: '#991b1b' },
    { name: 'Provocativo', value: 10, color: '#f97316' }
  ],
  severityDistribution: [
    { name: 'bajo', value: 40, color: '#22c55e' },
    { name: 'medio', value: 35, color: '#eab308' },
    { name: 'alto', value: 20, color: '#f97316' },
    { name: 'crítico', value: 5, color: '#ef4444' }
  ],
  totalToxic: 10742,
  totalAnalyzed: 45632,
  recentToxicityTrends: [
    { month: 'Ene', toxicity: 22 },
    { month: 'Feb', toxicity: 25 },
    { month: 'Mar', toxicity: 23 },
    { month: 'Abr', toxicity: 28 },
    { month: 'May', toxicity: 24 }
  ],
  loading: false
};

export const mockAppInfo = {
  title: "Dashboard General - Análisis de Toxicidad",
  version: "1.0.0",
  description: "Resumen completo del estado de toxicidad y estadísticas generales de análisis",
  authors: "NLP Team 2",
  isLoading: false,
  error: null
};

// Mock para useDashboardStats
export const mockUseDashboardStats = vi.fn(() => mockDashboardStats);

// Mock para useToxicityStats
export const mockUseToxicityStats = vi.fn(() => mockToxicityStats);

// Mock para useAppInfo
export const mockUseAppInfo = vi.fn(() => mockAppInfo);

// Mock para fetch global
export const mockFetch = vi.fn();

// Mock para axios
export const mockAxios = {
  get: vi.fn(() => Promise.resolve({
    data: {
      prediction_list: [
        {
          id: 1,
          video_title: "Test Video",
          video_url: "https://youtube.com/test",
          created_at: "2025-01-09T10:00:00Z",
          total_comments: 150,
          total_replies: 45,
          toxicity_rate: 0.235
        }
      ]
    }
  }))
};
