import { useState } from 'react';
import { Calendar, Search, Filter, Eye, Download, Trash2 } from 'lucide-react';
import { mockToxicityData } from '../utils/mockData';

const HistoryTab = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const { recentAnalysis } = mockToxicityData;

  // Datos expandidos para el historial
  const historyData = [
    ...recentAnalysis,
    {
      id: 3,
      videoTitle: "Debate Político Intenso",
      date: "2024-12-18",
      toxicityRate: 32.8,
      totalComments: 2156,
      url: "https://youtube.com/watch?v=abc123"
    },
    {
      id: 4,
      videoTitle: "Review Película Controvertida",
      date: "2024-12-17",
      toxicityRate: 18.7,
      totalComments: 967,
      url: "https://youtube.com/watch?v=def456"
    },
    {
      id: 5,
      videoTitle: "Tutorial de Cocina",
      date: "2024-12-16",
      toxicityRate: 2.1,
      totalComments: 453,
      url: "https://youtube.com/watch?v=ghi789"
    }
  ];

  const getToxicityColor = (rate) => {
    if (rate < 5) return "text-green-600 bg-green-100";
    if (rate < 15) return "text-yellow-600 bg-yellow-100";
    if (rate < 25) return "text-orange-600 bg-orange-100";
    return "text-red-600 bg-red-100";
  };

  const getToxicityLabel = (rate) => {
    if (rate < 5) return "Bajo";
    if (rate < 15) return "Moderado";
    if (rate < 25) return "Alto";
    return "Crítico";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Historial de Análisis</h2>
          <p className="text-gray-600">Revisa los análisis previos de videos</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <Download className="h-4 w-4" />
          <span>Exportar</span>
        </button>
      </div>

      {/* Filtros */}
      <div className="card">
        <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Buscar por título del video..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex space-x-4">
            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option>Todos los niveles</option>
              <option>Bajo (&lt;5%)</option>
              <option>Moderado (5-15%)</option>
              <option>Alto (15-25%)</option>
              <option>Crítico (&gt;25%)</option>
            </select>
            <input
              type="date"
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{historyData.length}</p>
            <p className="text-sm text-gray-600">Total Análisis</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">
              {historyData.filter(item => item.toxicityRate < 15).length}
            </p>
            <p className="text-sm text-gray-600">Videos Seguros</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <p className="text-2xl font-bold text-red-600">
              {historyData.filter(item => item.toxicityRate >= 25).length}
            </p>
            <p className="text-sm text-gray-600">Videos Críticos</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-600">
              {Math.round(historyData.reduce((acc, item) => acc + item.toxicityRate, 0) / historyData.length)}%
            </p>
            <p className="text-sm text-gray-600">Promedio Toxicidad</p>
          </div>
        </div>
      </div>

      {/* Tabla de historial */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Video</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Fecha</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Comentarios</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Toxicidad</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-700">Estado</th>
                <th className="text-right py-3 px-4 font-semibold text-gray-700">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {historyData.map((item) => (
                <tr key={item.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4">
                    <div>
                      <p className="font-medium text-gray-900">{item.videoTitle}</p>
                      <p className="text-sm text-gray-500">ID: {item.id}</p>
                    </div>
                  </td>
                  <td className="py-3 px-4 text-gray-600">
                    {new Date(item.date).toLocaleDateString('es-ES')}
                  </td>
                  <td className="py-3 px-4 text-gray-600">
                    {item.totalComments.toLocaleString()}
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-lg font-bold">{item.toxicityRate}%</span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getToxicityColor(item.toxicityRate)}`}>
                      {getToxicityLabel(item.toxicityRate)}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex justify-end space-x-2">
                      <button className="p-2 text-blue-600 hover:bg-blue-100 rounded">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-green-600 hover:bg-green-100 rounded">
                        <Download className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-red-600 hover:bg-red-100 rounded">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
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

export default HistoryTab;