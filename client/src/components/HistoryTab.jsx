import { useState } from 'react';
import AppMetadata from './AppMetadata';
import { Calendar, Search, Filter, Eye, Download, Trash2, RefreshCw, AlertCircle } from 'lucide-react';
import { useAnalysisHistory, mapToxicityCategories } from '../hooks/useApiData';
import ToxicityBadge from './ToxicityBadge';

const HistoryTab = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLevel, setFilterLevel] = useState('all');
  const [filterDate, setFilterDate] = useState('');
  
  // 🎯 USAR DATOS REALES DE LA API
  const { data: historyData, loading, error, refetch } = useAnalysisHistory();

  // Filtrar datos basado en búsqueda y filtros
  const filteredData = historyData.filter(item => {
    const matchesSearch = item.videoTitle.toLowerCase().includes(searchTerm.toLowerCase());
    
    let matchesLevel = true;
    if (filterLevel !== 'all') {
      switch (filterLevel) {
        case 'low':
          matchesLevel = item.toxicityRate < 5;
          break;
        case 'moderate':
          matchesLevel = item.toxicityRate >= 5 && item.toxicityRate < 15;
          break;
        case 'high':
          matchesLevel = item.toxicityRate >= 15 && item.toxicityRate < 25;
          break;
        case 'critical':
          matchesLevel = item.toxicityRate >= 25;
          break;
      }
    }
    
    let matchesDate = true;
    if (filterDate) {
      const itemDate = new Date(item.date).toISOString().split('T')[0];
      matchesDate = itemDate === filterDate;
    }
    
    return matchesSearch && matchesLevel && matchesDate;
  });

  const getToxicityColor = (rate) => {
    if (rate < 5) return "text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30";
    if (rate < 15) return "text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30";
    if (rate < 25) return "text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/30";
    return "text-secondary-600 dark:text-secondary-400 bg-secondary-100 dark:bg-secondary-900/30";
  };

  const getToxicityLabel = (rate) => {
    if (rate < 5) return "Bajo";
    if (rate < 15) return "Moderado";
    if (rate < 25) return "Alto";
    return "Crítico";
  };

  // Calcular estadísticas rápidas
  const totalAnalysis = historyData.length;
  const safeVideos = historyData.filter(item => item.toxicityRate < 15).length;
  const criticalVideos = historyData.filter(item => item.toxicityRate >= 25).length;
  const averageToxicity = totalAnalysis > 0 
    ? Math.round(historyData.reduce((acc, item) => acc + item.toxicityRate, 0) / totalAnalysis)
    : 0;

  return (
    <>
      {/* 🎯 METADATA ESPECÍFICA PARA HISTORIAL */}
      <AppMetadata 
        pageTitle="Historial de Análisis"
        pageDescription={`Revisa el historial completo de ${totalAnalysis} análisis previos de videos y comentarios de YouTube.`}
      />
      
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Historial de Análisis</h2>
            <p className="text-gray-600 dark:text-gray-300">
              {loading ? 'Cargando...' : `${totalAnalysis} análisis en total`}
            </p>
          </div>
          <div className="flex space-x-3">
            <button 
              onClick={refetch}
              disabled={loading}
              className="flex items-center space-x-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 dark:bg-gray-500 dark:hover:bg-gray-600 text-white rounded-lg disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
              <span>Actualizar</span>
            </button>
            <button className="flex items-center space-x-2 px-4 py-2 bg-accent-600 hover:bg-accent-700 dark:bg-accent-500 dark:hover:bg-accent-600 text-white rounded-lg">
              <Download className="h-4 w-4" />
              <span>Exportar</span>
            </button>
          </div>
        </div>

        {/* Error state */}
        {error && (
          <div className="card bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
            <div className="flex items-center space-x-3">
              <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
              <div>
                <p className="text-red-800 dark:text-red-200 font-medium">Error cargando el historial</p>
                <p className="text-red-600 dark:text-red-300 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Filtros */}
        <div className="card">
          <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Buscar por título del video..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                             bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                             focus:ring-2 focus:ring-accent-500 focus:border-transparent 
                             placeholder-gray-500 dark:placeholder-gray-400"
                />
              </div>
            </div>
            <div className="flex space-x-4">
              <select 
                value={filterLevel}
                onChange={(e) => setFilterLevel(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:ring-2 focus:ring-accent-500"
              >
                <option value="all">Todos los niveles</option>
                <option value="low">Bajo (&lt;5%)</option>
                <option value="moderate">Moderado (5-15%)</option>
                <option value="high">Alto (15-25%)</option>
                <option value="critical">Crítico (&gt;25%)</option>
              </select>
              <input
                type="date"
                value={filterDate}
                onChange={(e) => setFilterDate(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:ring-2 focus:ring-accent-500"
              />
            </div>
          </div>
        </div>

        {/* 🎯 ESTADÍSTICAS REALES */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="metric-card">
            <div className="text-center">
              <p className="text-2xl font-bold text-accent-600 dark:text-accent-400">
                {loading ? '...' : totalAnalysis}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Análisis</p>
            </div>
          </div>
          <div className="metric-card">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                {loading ? '...' : safeVideos}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Videos Seguros</p>
            </div>
          </div>
          <div className="metric-card">
            <div className="text-center">
              <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
                {loading ? '...' : criticalVideos}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Videos Críticos</p>
            </div>
          </div>
          <div className="metric-card">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                {loading ? '...' : `${averageToxicity}%`}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Promedio Toxicidad</p>
            </div>
          </div>
        </div>

        {/* 🎯 TABLA CON DATOS REALES */}
        <div className="card">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <RefreshCw className="h-8 w-8 animate-spin text-accent-500" />
              <span className="ml-3 text-gray-600 dark:text-gray-400">Cargando historial...</span>
            </div>
          ) : filteredData.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 dark:text-gray-400">
                {historyData.length === 0 ? 'No hay análisis en el historial' : 'No se encontraron resultados con los filtros aplicados'}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Video</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Fecha</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Comentarios</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Respuestas</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Toxicidad</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Estado</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((item) => (
                    <tr key={item.id} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                      <td className="py-3 px-4">
                        <div>
                          <p className="font-medium text-gray-900 dark:text-gray-100 max-w-xs truncate">
                            {item.videoTitle}
                          </p>
                          <p className="text-sm text-gray-500 dark:text-gray-400">ID: {item.id}</p>
                          {item.author && (
                            <p className="text-xs text-gray-400 dark:text-gray-500">Por: {item.author}</p>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {new Date(item.date).toLocaleDateString('es-ES', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric'
                        })}
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {item.totalComments.toLocaleString()}
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {item.totalReplies.toLocaleString()}
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-lg font-bold text-gray-900 dark:text-gray-100">
                          {typeof item.toxicityRate === 'number' ? item.toxicityRate.toFixed(1) : item.toxicityRate}%
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <ToxicityBadge 
                          categories={mapToxicityCategories(item.categories_summary)}
                          severity={item.toxicityRate >= 25 ? 'crítico' : item.toxicityRate >= 15 ? 'alto' : item.toxicityRate >= 5 ? 'medio' : 'bajo'}
                          compact={true}
                        />
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex justify-end space-x-2">
                          <button 
                            onClick={() => {
                              // TODO: Implementar modal de detalles
                              console.log('Ver detalles de:', item.id);
                            }}
                            className="p-2 text-accent-600 dark:text-accent-400 hover:bg-accent-100 dark:hover:bg-accent-900/30 rounded"
                            title="Ver detalles"
                          >
                            <Eye className="h-4 w-4" />
                          </button>
                          <button 
                            onClick={() => {
                              // TODO: Implementar descarga
                              console.log('Descargar:', item.id);
                            }}
                            className="p-2 text-green-600 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/30 rounded"
                            title="Descargar"
                          >
                            <Download className="h-4 w-4" />
                          </button>
                          <button 
                            onClick={() => {
                              // TODO: Implementar eliminación
                              console.log('Eliminar:', item.id);
                            }}
                            className="p-2 text-secondary-600 dark:text-secondary-400 hover:bg-secondary-100 dark:hover:bg-secondary-900/30 rounded"
                            title="Eliminar"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Información de filtros aplicados */}
        {(searchTerm || filterLevel !== 'all' || filterDate) && (
          <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
            Mostrando {filteredData.length} de {historyData.length} análisis
            {searchTerm && ` • Búsqueda: "${searchTerm}"`}
            {filterLevel !== 'all' && ` • Nivel: ${filterLevel}`}
            {filterDate && ` • Fecha: ${filterDate}`}
          </div>
        )}
      </div>
    </>
  );
};

export default HistoryTab;