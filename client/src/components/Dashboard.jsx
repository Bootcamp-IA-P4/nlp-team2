import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, Shield, MessageCircle, Clock, RefreshCw, AlertCircle } from 'lucide-react';
import AppMetadata from './AppMetadata';
import { useDashboardStats, useToxicityStats } from '../hooks/useApiData';

const Dashboard = () => {
  // 🎯 USAR DATOS REALES DE LA API
  const { stats, loading, error } = useDashboardStats();
  const { 
    categoriesDistribution, 
    severityDistribution, 
    totalToxic, 
    totalAnalyzed,
    recentToxicityTrends,
    loading: toxicityLoading 
  } = useToxicityStats();

  // 🎯 COLORES PARA CATEGORÍAS DE TOXICIDAD
  const TOXICITY_COLORS = {
    'Contenido Tóxico': '#ef4444',      // Rojo
    'Lenguaje Abusivo': '#dc2626',      // Rojo oscuro
    'Amenazas': '#991b1b',              // Rojo muy oscuro
    'Provocativo': '#f97316',           // Naranja
    'Lenguaje Obsceno': '#ea580c',      // Naranja oscuro
    'Discurso de Odio': '#7c2d12',      // Marrón
    'Racismo': '#451a03',               // Marrón oscuro
    'Nacionalismo Extremo': '#a21caf',  // Púrpura
    'Sexismo': '#be185d',               // Rosa oscuro
    'Homofobia': '#831843',             // Rosa muy oscuro
    'Odio Religioso': '#581c87',        // Púrpura oscuro
    'Radicalismo': '#312e81'            // Índigo oscuro
  };

  // 🎯 COLORES PARA SEVERIDAD
  const SEVERITY_COLORS = {
    'bajo': '#22c55e',      // Verde
    'medio': '#eab308',     // Amarillo
    'alto': '#f97316',      // Naranja
    'crítico': '#ef4444'    // Rojo
  };

  if (loading || toxicityLoading) {
    return (
      <>
        <AppMetadata 
          pageTitle="Dashboard General"
          pageDescription="Cargando estadísticas del dashboard..."
        />
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <RefreshCw className="h-12 w-12 animate-spin text-accent-500 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-400">Cargando estadísticas...</p>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <AppMetadata 
          pageTitle="Dashboard General - Error"
          pageDescription="Error cargando las estadísticas del dashboard"
        />
        <div className="card bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
          <div className="flex items-center space-x-3">
            <AlertCircle className="h-8 w-8 text-red-600 dark:text-red-400" />
            <div>
              <h3 className="text-lg font-medium text-red-800 dark:text-red-200">Error cargando el dashboard</h3>
              <p className="text-red-600 dark:text-red-300">{error}</p>
              <button 
                onClick={() => window.location.reload()} 
                className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Reintentar
              </button>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      {/* 🎯 METADATA CON DATOS REALES */}
      <AppMetadata 
        pageTitle="Dashboard General"
        pageDescription={`Resumen completo: ${stats.totalVideos} videos analizados, ${stats.totalComments.toLocaleString()} comentarios procesados, ${totalToxic} casos de toxicidad detectados.`}
      />
      
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Dashboard General</h2>
            <p className="text-gray-600 dark:text-gray-300">Resumen completo del estado de toxicidad</p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
            <Clock className="h-4 w-4" />
            <span>Última actualización: {new Date().toLocaleTimeString('es-ES')}</span>
          </div>
        </div>

        {/* 🎯 MÉTRICAS REALES EXPANDIDAS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Videos Analizados</p>
                <p className="text-2xl font-bold text-primary-500 dark:text-accent-400">
                  {stats.totalVideos.toLocaleString()}
                </p>
                <div className="flex items-center mt-1">
                  <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                  <span className="text-xs text-green-600 dark:text-green-400">Total acumulado</span>
                </div>
              </div>
              <MessageCircle className="h-8 w-8 text-primary-500 dark:text-accent-400 opacity-80" />
            </div>
          </div>

          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Comentarios</p>
                <p className="text-2xl font-bold text-accent-500 dark:text-accent-300">
                  {stats.totalComments.toLocaleString()}
                </p>
                <div className="flex items-center mt-1">
                  <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                  <span className="text-xs text-green-600 dark:text-green-400">Procesados</span>
                </div>
              </div>
              <BarChart className="h-8 w-8 text-accent-500 dark:text-accent-300 opacity-80" />
            </div>
          </div>

          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Casos Tóxicos</p>
                <p className="text-2xl font-bold text-red-500 dark:text-red-400">
                  {totalToxic.toLocaleString()}
                </p>
                <div className="flex items-center mt-1">
                  <AlertTriangle className="h-3 w-3 text-red-500 mr-1" />
                  <span className="text-xs text-red-600 dark:text-red-400">
                    {totalAnalyzed > 0 ? Math.round((totalToxic / totalAnalyzed) * 100) : 0}% del total
                  </span>
                </div>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-500 dark:text-red-400 opacity-80" />
            </div>
          </div>

          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Tasa Promedio</p>
                <p className="text-2xl font-bold text-secondary-500 dark:text-secondary-400">
                  {stats.averageToxicity}%
                </p>
                <div className="flex items-center mt-1">
                  {stats.averageToxicity < 15 ? (
                    <>
                      <TrendingDown className="h-3 w-3 text-green-500 mr-1" />
                      <span className="text-xs text-green-600 dark:text-green-400">Aceptable</span>
                    </>
                  ) : (
                    <>
                      <TrendingUp className="h-3 w-3 text-red-500 mr-1" />
                      <span className="text-xs text-red-600 dark:text-red-400">Elevado</span>
                    </>
                  )}
                </div>
              </div>
              <Shield className="h-8 w-8 text-secondary-500 dark:text-secondary-400 opacity-80" />
            </div>
          </div>

          <div className="metric-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Videos Seguros</p>
                <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                  {stats.safeVideos.toLocaleString()}
                </p>
                <div className="flex items-center mt-1">
                  <Shield className="h-3 w-3 text-green-500 mr-1" />
                  <span className="text-xs text-green-600 dark:text-green-400">
                    {stats.totalVideos > 0 ? Math.round((stats.safeVideos / stats.totalVideos) * 100) : 0}%
                  </span>
                </div>
              </div>
              <Shield className="h-8 w-8 text-green-500 dark:text-green-400 opacity-80" />
            </div>
          </div>
        </div>

        {/* 🎯 GRÁFICAS PRINCIPALES CON DATOS REALES */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Categorías de Toxicidad REALES */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">
              Tipos de Toxicidad Detectados
            </h3>
            {categoriesDistribution.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoriesDistribution} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={120} />
                  <Tooltip />
                  <Bar dataKey="count">
                    {categoriesDistribution.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={TOXICITY_COLORS[entry.name] || '#ef4444'} 
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
                <div className="text-center">
                  <Shield className="h-12 w-12 mx-auto mb-2 text-green-500" />
                  <p>No se han detectado categorías de toxicidad</p>
                  <p className="text-sm">¡Excelente! El contenido parece ser seguro</p>
                </div>
              </div>
            )}
          </div>

          {/* Tendencia de Toxicidad (7 días) */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">
              Tendencia de Toxicidad (7 días)
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={recentToxicityTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [
                    name === 'rate' ? `${value}%` : value,
                    name === 'rate' ? 'Tasa de Toxicidad' : name === 'total' ? 'Total Análisis' : 'Casos Tóxicos'
                  ]}
                />
                <Line 
                  type="monotone" 
                  dataKey="rate" 
                  stroke="#ef4444" 
                  strokeWidth={3}
                  dot={{ fill: '#ef4444', strokeWidth: 2, r: 6 }}
                  name="rate"
                />
                <Line 
                  type="monotone" 
                  dataKey="toxic" 
                  stroke="#f97316" 
                  strokeWidth={2}
                  dot={{ fill: '#f97316', strokeWidth: 2, r: 4 }}
                  name="toxic"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 🎯 DISTRIBUCIÓN POR SEVERIDAD */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Distribución por Severidad */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">
              Distribución por Severidad
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={Object.entries(severityDistribution).map(([severity, count]) => ({
                    name: severity.charAt(0).toUpperCase() + severity.slice(1),
                    value: count,
                    fill: SEVERITY_COLORS[severity]
                  }))}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  <Tooltip />
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Resumen de Severidad */}
          <div className="lg:col-span-2 card">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">
              Resumen por Nivel de Severidad
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(severityDistribution).map(([severity, count]) => {
                const percentage = totalToxic > 0 ? Math.round((count / totalToxic) * 100) : 0;
                const color = SEVERITY_COLORS[severity];
                
                return (
                  <div 
                    key={severity}
                    className="flex items-center justify-between p-4 rounded-lg border-2"
                    style={{ 
                      borderColor: color + '40', 
                      backgroundColor: color + '10' 
                    }}
                  >
                    <div>
                      <p className="text-sm font-medium" style={{ color }}>
                        {severity.charAt(0).toUpperCase() + severity.slice(1)}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">
                        {percentage}% del total tóxico
                      </p>
                      <div className="mt-2">
                        <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div 
                            className="h-2 rounded-full transition-all duration-300"
                            style={{ 
                              width: `${percentage}%`,
                              backgroundColor: color 
                            }}
                          />
                        </div>
                      </div>
                    </div>
                    <span className="text-2xl font-bold" style={{ color }}>
                      {count}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* 🎯 ANÁLISIS RECIENTES CON CATEGORÍAS */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
              Análisis Recientes con Detección de Toxicidad
            </h3>
            <button className="text-secondary-500 hover:text-secondary-600 dark:text-secondary-400 dark:hover:text-secondary-300 text-sm font-medium">
              Ver todos
            </button>
          </div>
          {stats.recentAnalysis.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500 dark:text-gray-400">No hay análisis recientes</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Video</th>
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Fecha</th>
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Comentarios</th>
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Toxicidad</th>
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Categorías</th>
                    <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recentAnalysis.map((analysis) => (
                    <tr key={analysis.id} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                      <td className="py-3 px-4">
                        <p className="font-medium text-gray-900 dark:text-gray-100 truncate max-w-xs">
                          {analysis.videoTitle}
                        </p>
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {new Date(analysis.date).toLocaleDateString('es-ES')}
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {analysis.totalComments.toLocaleString()}
                      </td>
                      <td className="py-3 px-4">
                        <span className="font-semibold text-secondary-500 dark:text-secondary-400">
                          {analysis.toxicityRate}%
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex flex-wrap gap-1">
                          {/* TODO: Mostrar categorías específicas cuando estén disponibles */}
                          {analysis.toxicityRate > 15 ? (
                            <span className="px-2 py-1 rounded-full text-xs bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300">
                              Alto riesgo
                            </span>
                          ) : analysis.toxicityRate > 5 ? (
                            <span className="px-2 py-1 rounded-full text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300">
                              Moderado
                            </span>
                          ) : (
                            <span className="px-2 py-1 rounded-full text-xs bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300">
                              Seguro
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          analysis.toxicityRate < 10 
                            ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' 
                            : analysis.toxicityRate < 20 
                            ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300'
                            : 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
                        }`}>
                          {analysis.toxicityRate < 10 ? 'Seguro' : analysis.toxicityRate < 20 ? 'Moderado' : 'Alto'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Dashboard;
