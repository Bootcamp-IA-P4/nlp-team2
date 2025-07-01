import { useState } from 'react';
import { Play, AlertTriangle, MessageCircle, TrendingUp, Clock } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { mockToxicityData } from '../utils/mockData';

const AnalyzeTab = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasResults, setHasResults] = useState(false);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // Simular análisis
    setTimeout(() => {
      setIsAnalyzing(false);
      setHasResults(true);
    }, 3000);
  };

  const { overall, toxicityTypes, timelineData } = mockToxicityData;

  return (
    <div className="space-y-6">
      {/* Header con input de URL */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Analizar Video de YouTube</h2>
        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleAnalyze}
            disabled={!youtubeUrl || isAnalyzing}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Analizando...</span>
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                <span>Analizar</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Métricas principales */}
      {hasResults && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Comentarios</p>
                  <p className="text-2xl font-bold text-gray-900">{overall.totalComments.toLocaleString()}</p>
                </div>
                <MessageCircle className="h-8 w-8 text-blue-500" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Comentarios Tóxicos</p>
                  <p className="text-2xl font-bold text-red-600">{overall.toxicComments.toLocaleString()}</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-500" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Tasa de Toxicidad</p>
                  <p className="text-2xl font-bold text-orange-600">{overall.toxicityRate}%</p>
                </div>
                <TrendingUp className="h-8 w-8 text-orange-500" />
              </div>
            </div>

            <div className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Estado</p>
                  <p className="text-sm font-semibold text-green-600">Análisis Completo</p>
                </div>
                <Clock className="h-8 w-8 text-green-500" />
              </div>
            </div>
          </div>

          {/* Gráficas */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Gráfico de barras - Tipos de toxicidad */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Tipos de Toxicidad</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={toxicityTypes}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#ef4444" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Gráfico circular - Distribución */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Distribución de Toxicidad</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Comentarios Limpios', value: overall.totalComments - overall.toxicComments, color: '#22c55e' },
                      { name: 'Comentarios Tóxicos', value: overall.toxicComments, color: '#ef4444' }
                    ]}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    <Cell fill="#22c55e" />
                    <Cell fill="#ef4444" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Timeline de toxicidad */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Timeline de Toxicidad</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="toxic" stroke="#ef4444" strokeWidth={3} name="Tóxicos" />
                <Line type="monotone" dataKey="clean" stroke="#22c55e" strokeWidth={3} name="Limpios" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Lista de comentarios tóxicos (simulada) */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Comentarios Más Tóxicos</h3>
            <div className="space-y-4">
              {[
                { comment: "Este comentario contiene lenguaje abusivo simulado...", type: "Abusive", confidence: 0.95 },
                { comment: "Ejemplo de discurso de odio simulado...", type: "Hate Speech", confidence: 0.87 },
                { comment: "Contenido con amenazas simuladas...", type: "Threat", confidence: 0.92 }
              ].map((item, index) => (
                <div key={index} className="border border-red-200 rounded-lg p-4 bg-red-50">
                  <div className="flex justify-between items-start mb-2">
                    <span className={`px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800`}>
                      {item.type}
                    </span>
                    <span className="text-xs text-gray-500">Confianza: {(item.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <p className="text-sm text-gray-700">{item.comment}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AnalyzeTab;