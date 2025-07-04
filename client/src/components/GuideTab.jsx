import { useState } from 'react';
import { AlertCircle, Shield, BookOpen, ExternalLink, Search } from 'lucide-react';
import { toxicityGuide } from '../utils/mockData';

const GuideTab = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800';
      case 'high':
        return 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 border-orange-200 dark:border-orange-800';
      case 'medium':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800';
      default:
        return 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-700';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-400" />;
      case 'high':
        return <AlertCircle className="h-4 w-4 text-orange-600 dark:text-orange-400" />;
      case 'medium':
        return <Shield className="h-4 w-4 text-yellow-600 dark:text-yellow-400" />;
      default:
        return <Shield className="h-4 w-4 text-gray-600 dark:text-gray-400" />;
    }
  };

  const filteredCategories = toxicityGuide.categories.filter(category =>
    (selectedCategory === 'all' || category.severity === selectedCategory) &&
    (searchTerm === '' || 
     category.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
     category.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-3 bg-accent-100 dark:bg-accent-900/30 rounded-lg">
            <BookOpen className="h-8 w-8 text-accent-600 dark:text-accent-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Guía de Toxicidad</h2>
            <p className="text-gray-600 dark:text-gray-300">Aprende sobre los diferentes tipos de contenido tóxico y cómo identificarlos</p>
          </div>
        </div>

        {/* Filtros */}
        <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 h-4 w-4" />
              <input
                type="text"
                placeholder="Buscar categoría o descripción..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                           bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                           focus:ring-2 focus:ring-accent-500 focus:border-transparent 
                           placeholder-gray-500 dark:placeholder-gray-400"
              />
            </div>
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                       bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                       focus:ring-2 focus:ring-accent-500"
          >
            <option value="all">Todos los niveles</option>
            <option value="critical">Crítico</option>
            <option value="high">Alto</option>
            <option value="medium">Medio</option>
          </select>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="text-center">
            <div className="flex justify-center mb-2">
              <AlertCircle className="h-8 w-8 text-secondary-500 dark:text-secondary-400" />
            </div>
            <p className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
              {toxicityGuide.categories.filter(c => c.severity === 'critical').length}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Nivel Crítico</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <div className="flex justify-center mb-2">
              <AlertCircle className="h-8 w-8 text-orange-500 dark:text-orange-400" />
            </div>
            <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              {toxicityGuide.categories.filter(c => c.severity === 'high').length}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Nivel Alto</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <div className="flex justify-center mb-2">
              <Shield className="h-8 w-8 text-yellow-500 dark:text-yellow-400" />
            </div>
            <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
              {toxicityGuide.categories.filter(c => c.severity === 'medium').length}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Nivel Medio</p>
          </div>
        </div>
        <div className="metric-card">
          <div className="text-center">
            <div className="flex justify-center mb-2">
              <BookOpen className="h-8 w-8 text-accent-500 dark:text-accent-400" />
            </div>
            <p className="text-2xl font-bold text-accent-600 dark:text-accent-400">{toxicityGuide.categories.length}</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">Total Categorías</p>
          </div>
        </div>
      </div>

      {/* Categorías de toxicidad */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredCategories.map((category, index) => (
          <div key={index} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getSeverityIcon(category.severity)}
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">{category.type}</h3>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getSeverityColor(category.severity)}`}>
                {category.severity === 'critical' ? 'Crítico' : 
                 category.severity === 'high' ? 'Alto' : 
                 category.severity === 'medium' ? 'Medio' : 'Bajo'}
              </span>
            </div>

            <p className="text-gray-600 dark:text-gray-300 mb-4">{category.description}</p>

            <div className="mb-4">
              <h4 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Ejemplos comunes:</h4>
              <ul className="space-y-1">
                {category.examples.map((example, exampleIndex) => (
                  <li key={exampleIndex} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <div className="w-1.5 h-1.5 bg-gray-400 dark:bg-gray-500 rounded-full mr-2"></div>
                    {example}
                  </li>
                ))}
              </ul>
            </div>

            <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full`} style={{ backgroundColor: category.color === 'red' ? '#ef4444' : category.color === 'orange' ? '#f97316' : category.color === 'blue' ? '#3b82f6' : category.color === 'purple' ? '#8b5cf6' : category.color === 'pink' ? '#ec4899' : '#06b6d4' }}></div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">Color de identificación</span>
                </div>
                <button className="flex items-center space-x-1 text-accent-600 hover:text-accent-800 dark:text-accent-400 dark:hover:text-accent-300 text-sm">
                  <span>Más info</span>
                  <ExternalLink className="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Información adicional */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">¿Cómo funciona la detección?</h3>
          <div className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
            <p>• <strong className="text-gray-800 dark:text-gray-200">Análisis de texto:</strong> Utilizamos modelos de NLP avanzados para analizar el contenido.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Contexto:</strong> Consideramos el contexto y las relaciones entre palabras.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Confianza:</strong> Cada detección incluye un nivel de confianza del modelo.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Multi-etiqueta:</strong> Un comentario puede pertenecer a múltiples categorías.</p>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">Mejores Prácticas</h3>
          <div className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
            <p>• <strong className="text-gray-800 dark:text-gray-200">Revisión humana:</strong> Siempre revisa manualmente casos de alta toxicidad.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Contexto cultural:</strong> Considera diferencias culturales y regionales.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Falsos positivos:</strong> El sistema puede generar algunos falsos positivos.</p>
            <p>• <strong className="text-gray-800 dark:text-gray-200">Actualización:</strong> Los modelos se actualizan constantemente.</p>
          </div>
        </div>
      </div>

      {/* Footer con recursos */}
      <div className="card bg-accent-50 dark:bg-accent-900/20 border-accent-200 dark:border-accent-800">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-accent-100 dark:bg-accent-800/50 rounded-lg">
            <BookOpen className="h-6 w-6 text-accent-600 dark:text-accent-400" />
          </div>
          <div className="flex-1">
            <h4 className="font-semibold text-accent-900 dark:text-accent-200">¿Necesitas más ayuda?</h4>
            <p className="text-accent-700 dark:text-accent-300 text-sm">Consulta nuestra documentación completa o contacta al equipo de soporte.</p>
          </div>
          <button className="px-4 py-2 bg-accent-600 hover:bg-accent-700 dark:bg-accent-500 dark:hover:bg-accent-600 text-white rounded-lg text-sm">
            Ver Documentación
          </button>
        </div>
      </div>
    </div>
  );
};

export default GuideTab;