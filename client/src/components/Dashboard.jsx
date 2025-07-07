import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, Shield, MessageCircle, Clock } from 'lucide-react';
import { mockToxicityData } from '../utils/mockData';

const Dashboard = () => {
  const { overall, toxicityTypes, timelineData, recentAnalysis } = mockToxicityData;

  // Datos adicionales para el dashboard
  const weeklyStats = [
    { day: 'Lun', analyzed: 45, toxic: 8 },
    { day: 'Mar', analyzed: 52, toxic: 12 },
    { day: 'Mié', analyzed: 38, toxic: 6 },
    { day: 'Jue', analyzed: 67, toxic: 15 },
    { day: 'Vie', analyzed: 71, toxic: 18 },
    { day: 'Sáb', analyzed: 43, toxic: 9 },
    { day: 'Dom', analyzed: 29, toxic: 4 }
  ];

  const monthlyTrend = [
    { month: 'Ene', rate: 14.2 },
    { month: 'Feb', rate: 16.8 },
    { month: 'Mar', rate: 12.5 },
    { month: 'Abr', rate: 18.9 },
    { month: 'May', rate: 15.3 },
    { month: 'Jun', rate: 11.7 }
  ];

  const COLORS = ['#c1121f', '#ef4444', '#f97316', '#eab308', '#8b5cf6', '#ec4899'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Dashboard General</h2>
          <p className="text-gray-600 dark:text-gray-300">Resumen completo del estado de toxicidad</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
          <Clock className="h-4 w-4" />
          <span>Última actualización: hace 5 min</span>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Videos Analizados</p>
              <p className="text-2xl font-bold text-primary-500 dark:text-accent-400">1,247</p>
              <div className="flex items-center mt-1">
                <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600 dark:text-green-400">+12% vs mes anterior</span>
              </div>
            </div>
            <MessageCircle className="h-8 w-8 text-primary-500 dark:text-accent-400 opacity-80" />
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Comentarios Procesados</p>
              <p className="text-2xl font-bold text-accent-500 dark:text-accent-300">89,324</p>
              <div className="flex items-center mt-1">
                <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600 dark:text-green-400">+8% vs mes anterior</span>
              </div>
            </div>
            <BarChart className="h-8 w-8 text-accent-500 dark:text-accent-300 opacity-80" />
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Tasa Promedio</p>
              <p className="text-2xl font-bold text-secondary-500 dark:text-secondary-400">13.7%</p>
              <div className="flex items-center mt-1">
                <TrendingDown className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600 dark:text-green-400">-2.3% vs mes anterior</span>
              </div>
            </div>
            <AlertTriangle className="h-8 w-8 text-secondary-500 dark:text-secondary-400 opacity-80" />
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Videos Seguros</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">1,089</p>
              <div className="flex items-center mt-1">
                <Shield className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600 dark:text-green-400">87.3% del total</span>
              </div>
            </div>
            <Shield className="h-8 w-8 text-green-500 dark:text-green-400 opacity-80" />
          </div>
        </div>
      </div>

      {/* Gráficas principales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Actividad semanal */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Actividad de la Semana</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={weeklyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="analyzed" 
                stackId="1"
                stroke="#669bbc" 
                fill="#669bbc" 
                fillOpacity={0.6}
                name="Analizados"
              />
              <Area 
                type="monotone" 
                dataKey="toxic" 
                stackId="2"
                stroke="#c1121f" 
                fill="#c1121f" 
                fillOpacity={0.8}
                name="Tóxicos"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Tendencia mensual */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Tendencia de Toxicidad (6 meses)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => [`${value}%`, 'Tasa de Toxicidad']} />
              <Line 
                type="monotone" 
                dataKey="rate" 
                stroke="#c1121f" 
                strokeWidth={3}
                dot={{ fill: '#c1121f', strokeWidth: 2, r: 6 }}
                name="Tasa (%)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Distribución de tipos de toxicidad */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Distribución por Tipo de Toxicidad</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={toxicityTypes} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="count" fill="#c1121f">
                {toxicityTypes.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Resumen rápido */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Resumen Rápido</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
              <div>
                <p className="text-sm font-medium text-red-800 dark:text-red-300">Crítico</p>
                <p className="text-xs text-red-600 dark:text-red-400">Necesita atención inmediata</p>
              </div>
              <span className="text-lg font-bold text-red-600 dark:text-red-400">23</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
              <div>
                <p className="text-sm font-medium text-orange-800 dark:text-orange-300">Alto</p>
                <p className="text-xs text-orange-600 dark:text-orange-400">Requiere supervisión</p>
              </div>
              <span className="text-lg font-bold text-orange-600 dark:text-orange-400">67</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <div>
                <p className="text-sm font-medium text-yellow-800 dark:text-yellow-300">Moderado</p>
                <p className="text-xs text-yellow-600 dark:text-yellow-400">Monitoreo regular</p>
              </div>
              <span className="text-lg font-bold text-yellow-600 dark:text-yellow-400">134</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <div>
                <p className="text-sm font-medium text-green-800 dark:text-green-300">Bajo</p>
                <p className="text-xs text-green-600 dark:text-green-400">Contenido seguro</p>
              </div>
              <span className="text-lg font-bold text-green-600 dark:text-green-400">1,023</span>
            </div>
          </div>
        </div>
      </div>

      {/* Análisis recientes */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">Análisis Recientes</h3>
          <button className="text-secondary-500 hover:text-secondary-600 dark:text-secondary-400 dark:hover:text-secondary-300 text-sm font-medium">
            Ver todos
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Video</th>
                <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Fecha</th>
                <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Comentarios</th>
                <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Toxicidad</th>
                <th className="text-left py-2 px-4 font-medium text-gray-600 dark:text-gray-300">Estado</th>
              </tr>
            </thead>
            <tbody>
              {recentAnalysis.slice(0, 5).map((analysis) => (
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
      </div>
    </div>
  );
};

export default Dashboard;
