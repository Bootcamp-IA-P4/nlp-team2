import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';
const TOXICITY_API = `${API_BASE_URL}/v1/toxicity`;

// Hook para obtener lista de análisis/predicciones
export const useAnalysisHistory = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        console.log('🔍 Obteniendo historial de análisis...');
        
        // 🎯 LLAMAR A TU ENDPOINT DE FASTAPI
        const response = await axios.get(`${API_BASE_URL}/v1/prediction_list`);
        
        if (response.data && response.data.prediction_list) {
          const formattedData = response.data.prediction_list.map(item => ({
            id: item.id,
            videoTitle: item.video_title || 'Video sin título',
            videoUrl: item.video_url || '',
            date: item.created_at || item.inserted_at,
            totalComments: item.total_comments || 0,
            totalReplies: item.total_replies || 0,
            toxicityRate: item.toxicity_rate || 0,
            // Campos adicionales que puedas tener
            author: item.video_author || 'Desconocido',
            description: item.video_description || '',
            likes: item.total_likes || 0,
            emojis: item.total_emojis || 0
          }));
          
          console.log('✅ Historial obtenido:', formattedData.length, 'elementos');
          setData(formattedData);
        } else {
          setData([]);
        }
        
        setError(null);
      } catch (err) {
        console.error('❌ Error obteniendo historial:', err);
        setError(err.response?.data?.detail || 'Error cargando el historial');
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const refetch = () => {
    setLoading(true);
    setError(null);
    // Re-trigger useEffect
    setTimeout(() => {
      window.location.reload(); // Alternativa: implementar fetchHistory() aquí
    }, 100);
  };

  return { data, loading, error, refetch };
};

// Hook para obtener detalle de un análisis específico
export const useAnalysisDetail = (id) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;

    const fetchDetail = async () => {
      try {
        setLoading(true);
        console.log('🔍 Obteniendo detalle del análisis:', id);
        
        const response = await axios.get(`${API_BASE_URL}/v1/prediction_detail/${id}`);
        
        if (response.data && response.data.prediction) {
          setData(response.data.prediction);
          console.log('✅ Detalle obtenido para ID:', id);
        }
        
        setError(null);
      } catch (err) {
        console.error('❌ Error obteniendo detalle:', err);
        setError(err.response?.data?.detail || 'Error cargando los detalles');
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [id]);

  return { data, loading, error };
};

// Hook para estadísticas del dashboard
export const useDashboardStats = () => {
  const [stats, setStats] = useState({
    totalVideos: 0,
    totalComments: 0,
    averageToxicity: 0,
    safeVideos: 0,
    recentAnalysis: [],
    toxicityByCategory: [],
    weeklyStats: [],
    monthlyTrend: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        console.log('📊 Obteniendo estadísticas del dashboard...');
        
        // Obtener lista completa para calcular estadísticas
        const response = await axios.get(`${API_BASE_URL}/v1/prediction_list`);
        
        if (response.data && response.data.prediction_list) {
          const rawData = response.data.prediction_list;
          
          // 📊 CALCULAR ESTADÍSTICAS
          const totalVideos = rawData.length;
          const totalComments = rawData.reduce((sum, item) => sum + (item.total_comments || 0), 0);
          const averageToxicity = totalVideos > 0 
            ? rawData.reduce((sum, item) => sum + (item.toxicity_rate || 0), 0) / totalVideos 
            : 0;
          const safeVideos = rawData.filter(item => (item.toxicity_rate || 0) < 15).length;
          
          // Análisis recientes (últimos 5)
          const recentAnalysis = rawData
            .sort((a, b) => new Date(b.created_at || b.inserted_at) - new Date(a.created_at || a.inserted_at))
            .slice(0, 5)
            .map(item => ({
              id: item.id,
              videoTitle: item.video_title || 'Video sin título',
              date: item.created_at || item.inserted_at,
              totalComments: item.total_comments || 0,
              toxicityRate: Math.round((item.toxicity_rate || 0) * 100) / 100
            }));

          // Estadísticas semanales (simuladas basadas en fechas reales)
          const weeklyStats = generateWeeklyStats(rawData);
          
          // Tendencia mensual (simulada basadas en fechas reales)
          const monthlyTrend = generateMonthlyTrend(rawData);

          setStats({
            totalVideos,
            totalComments,
            averageToxicity: Math.round(averageToxicity * 100) / 100,
            safeVideos,
            recentAnalysis,
            toxicityByCategory: [], // TODO: Implementar cuando tengas categorías en BD
            weeklyStats,
            monthlyTrend
          });
          
          console.log('✅ Estadísticas calculadas:', {
            totalVideos,
            totalComments,
            averageToxicity,
            safeVideos
          });
        }
        
        setError(null);
      } catch (err) {
        console.error('❌ Error obteniendo estadísticas:', err);
        setError(err.response?.data?.detail || 'Error cargando estadísticas');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return { stats, loading, error };
};

// Funciones helper para generar estadísticas basadas en datos reales
const generateWeeklyStats = (rawData) => {
  const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
  const weeklyData = days.map(day => ({ day, analyzed: 0, toxic: 0 }));
  
  // Distribuir datos reales en días de la semana
  rawData.forEach(item => {
    const date = new Date(item.created_at || item.inserted_at);
    const dayIndex = (date.getDay() + 6) % 7; // Convertir domingo=0 a lunes=0
    if (dayIndex >= 0 && dayIndex < 7) {
      weeklyData[dayIndex].analyzed += 1;
      if ((item.toxicity_rate || 0) > 15) {
        weeklyData[dayIndex].toxic += 1;
      }
    }
  });
  
  return weeklyData;
};

const generateMonthlyTrend = (rawData) => {
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
  const monthlyData = months.map((month, index) => ({ 
    month, 
    rate: 0,
    count: 0 
  }));
  
  // Agrupar por mes y calcular promedio
  rawData.forEach(item => {
    const date = new Date(item.created_at || item.inserted_at);
    const monthIndex = date.getMonth();
    if (monthIndex >= 0 && monthIndex < 6) {
      monthlyData[monthIndex].rate += (item.toxicity_rate || 0);
      monthlyData[monthIndex].count += 1;
    }
  });
  
  // Calcular promedios
  return monthlyData.map(item => ({
    month: item.month,
    rate: item.count > 0 ? Math.round((item.rate / item.count) * 100) / 100 : 0
  }));
};

// Función para mapear las categorías técnicas a nombres amigables
export const mapToxicityCategories = (technicalCategories) => {
  const categoryMap = {
    'IsToxic': 'Contenido Tóxico',
    'IsAbusive': 'Lenguaje Abusivo',
    'IsThreat': 'Amenazas',
    'IsProvocative': 'Provocativo',
    'IsObscene': 'Lenguaje Obsceno',
    'IsHatespeech': 'Discurso de Odio',
    'IsRacist': 'Racismo',
    'IsNationalist': 'Nacionalismo Extremo',
    'IsSexist': 'Sexismo',
    'IsHomophobic': 'Homofobia',
    'IsReligiousHate': 'Odio Religioso',
    'IsRadicalism': 'Radicalismo'
  };

  if (!technicalCategories || typeof technicalCategories !== 'object') {
    return [];
  }

  return Object.entries(technicalCategories)
    .filter(([key, value]) => value === true || value === 1)
    .map(([key]) => ({
      technical: key,
      friendly: categoryMap[key] || key,
      severity: getSeverityLevel(key)
    }));
};

// Función para obtener nivel de severidad
const getSeverityLevel = (category) => {
  const severityMap = {
    'IsToxic': 'medio',
    'IsAbusive': 'alto',
    'IsThreat': 'crítico',
    'IsProvocative': 'bajo',
    'IsObscene': 'medio',
    'IsHatespeech': 'crítico',
    'IsRacist': 'crítico',
    'IsNationalist': 'alto',
    'IsSexist': 'alto',
    'IsHomophobic': 'crítico',
    'IsReligiousHate': 'crítico',
    'IsRadicalism': 'crítico'
  };
  
  return severityMap[category] || 'medio';
};

// Hook para obtener estadísticas de toxicidad con categorías reales
export const useToxicityStats = () => {
  const [stats, setStats] = useState({
    totalAnalyzed: 0,
    totalToxic: 0,
    categoriesDistribution: [],
    severityDistribution: { bajo: 0, medio: 0, alto: 0, crítico: 0 },
    recentToxicityTrends: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    const fetchToxicityStats = async () => {
      try {
        setStats(prev => ({ ...prev, loading: true }));
        console.log('📊 Obteniendo estadísticas de toxicidad...');
        
        // Obtener análisis con datos de toxicidad
        const response = await axios.get(`${API_BASE_URL}/v1/prediction_list`);
        
        if (response.data && response.data.prediction_list) {
          const rawData = response.data.prediction_list;
          
          // Procesar datos de toxicidad
          let totalAnalyzed = 0;
          let totalToxic = 0;
          let categoryCounts = {};
          let severityCounts = { bajo: 0, medio: 0, alto: 0, crítico: 0 };
          
          rawData.forEach(request => {
            // Si el request tiene análisis de toxicidad
            if (request.toxicity_summary || request.toxicity_analysis) {
              totalAnalyzed++;
              
              // Verificar si es tóxico
              const isToxic = request.toxicity_rate && request.toxicity_rate > 0.1;
              if (isToxic) {
                totalToxic++;
                
                // Procesar categorías si están disponibles
                const categories = request.categories_summary || 
                                 request.toxicity_summary?.categories_summary ||
                                 {};
                
                const friendlyCategories = mapToxicityCategories(categories);
                
                friendlyCategories.forEach(category => {
                  // Contar categorías
                  categoryCounts[category.friendly] = (categoryCounts[category.friendly] || 0) + 1;
                  
                  // Contar severidad
                  severityCounts[category.severity]++;
                });
              }
            }
          });
          
          // Convertir conteos a arrays para gráficas
          const categoriesDistribution = Object.entries(categoryCounts)
            .map(([name, count]) => ({ name, count }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 8); // Top 8 categorías
          
          setStats({
            totalAnalyzed,
            totalToxic,
            categoriesDistribution,
            severityDistribution: severityCounts,
            recentToxicityTrends: generateToxicityTrends(rawData),
            loading: false,
            error: null
          });
          
          console.log('✅ Estadísticas de toxicidad calculadas:', {
            totalAnalyzed,
            totalToxic,
            categoriesFound: categoriesDistribution.length
          });
        }
        
      } catch (err) {
        console.error('❌ Error obteniendo estadísticas de toxicidad:', err);
        setStats(prev => ({
          ...prev,
          loading: false,
          error: err.response?.data?.detail || 'Error cargando estadísticas de toxicidad'
        }));
      }
    };

    fetchToxicityStats();
  }, []);

  return stats;
};

// Función helper para generar tendencias de toxicidad
const generateToxicityTrends = (rawData) => {
  const trends = [];
  const now = new Date();
  
  // Últimos 7 días
  for (let i = 6; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    const dayData = rawData.filter(item => {
      const itemDate = new Date(item.created_at || item.request_date);
      return itemDate.toISOString().split('T')[0] === dateStr;
    });
    
    const toxicCount = dayData.filter(item => 
      item.toxicity_rate && item.toxicity_rate > 0.1
    ).length;
    
    trends.push({
      date: date.toLocaleDateString('es-ES', { weekday: 'short' }),
      total: dayData.length,
      toxic: toxicCount,
      rate: dayData.length > 0 ? Math.round((toxicCount / dayData.length) * 100) : 0
    });
  }
  
  return trends;
};

// ✅ NUEVAS FUNCIONES PARA ANÁLISIS DE TOXICIDAD
export const analyzeSingleComment = async (comment) => {
  try {
    const response = await axios.post(`${TOXICITY_API}/analyze-comment`, {
      comment: comment
    });
    return response.data;
  } catch (error) {
    console.error('Error analizando comentario:', error);
    throw error;
  }
};

export const analyzeMultipleComments = async (comments) => {
  try {
    const response = await axios.post(`${TOXICITY_API}/analyze-comments`, {
      comments: comments
    });
    return response.data;
  } catch (error) {
    console.error('Error analizando comentarios:', error);
    throw error;
  }
};

export const checkToxicityHealth = async () => {
  try {
    const response = await axios.get(`${TOXICITY_API}/health`);
    return response.data;
  } catch (error) {
    console.error('Error verificando salud del sistema:', error);
    throw error;
  }
};

export default { useAnalysisHistory, useAnalysisDetail, useDashboardStats };