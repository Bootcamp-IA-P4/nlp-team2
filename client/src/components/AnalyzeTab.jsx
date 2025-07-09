import React, { useState } from 'react';
import AppMetadata from './AppMetadata';
import { Play, AlertTriangle, MessageCircle, TrendingUp, Clock, Send, Video, CheckCircle, XCircle, BarChart3, Settings } from 'lucide-react';
import axios from 'axios';
import ProgressLoader from './ProgressLoader';

const AnalyzeTab = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [comment, setComment] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState('');
  const [maxComments, setMaxComments] = useState(50);
  const [showAdvanced, setShowAdvanced] = useState(false);

  // 🎯 TÍTULO DINÁMICO BASADO EN EL ESTADO
  const getPageTitle = () => {
    if (isAnalyzing) return "Analizando Video en Tiempo Real...";
    if (analysisResult?.analysis) {
      const total = analysisResult.analysis.total_comments || 0;
      const toxic = analysisResult.analysis.toxic_comments || 0;
      return `Análisis Completado - ${total} comentarios (${toxic} tóxicos)`;
    }
    if (analysisResult?.single_comment) return "Comentario Analizado";
    return "Análisis de Toxicidad con IA";
  };

  const getPageDescription = () => {
    if (isAnalyzing) return `Analizando hasta ${maxComments} comentarios del video de YouTube en tiempo real...`;
    if (analysisResult?.analysis) {
      const rate = analysisResult.analysis.toxicity_rate || 0;
      return `Análisis completado: ${(rate * 100).toFixed(1)}% de toxicidad detectada en los comentarios.`;
    }
    if (analysisResult?.single_comment) {
      const isToxic = analysisResult.single_comment.is_toxic;
      return `Comentario individual analizado: ${isToxic ? 'Contenido tóxico detectado' : 'Contenido limpio'}`;
    }
    return "Analiza la toxicidad en comentarios de YouTube usando inteligencia artificial y machine learning.";
  };

  // Constantes de validación basadas en tu scraper
  const MIN_COMMENTS = 5;
  const MAX_COMMENTS = 1000; // Basado en tu scraper
  const RECOMMENDED_COMMENTS = [10, 25, 50, 100, 200, 500];

  // Validar número de comentarios
  const validateCommentsNumber = (value) => {
    const num = parseInt(value);
    if (isNaN(num)) return false;
    if (num < MIN_COMMENTS) return false;
    if (num > MAX_COMMENTS) return false;
    return true;
  };

  // Manejar cambio en número de comentarios
  const handleMaxCommentsChange = (value) => {
    const num = parseInt(value);
    if (!isNaN(num)) {
      setMaxComments(Math.min(Math.max(num, MIN_COMMENTS), MAX_COMMENTS));
    }
  };

  // Analizar video de YouTube (ACTUALIZADO)
  const handleAnalyzeVideo = async () => {
    if (!youtubeUrl.trim()) {
      setError('Por favor ingresa una URL válida');
      return;
    }

    if (!validateCommentsNumber(maxComments)) {
      setError(`El número de comentarios debe estar entre ${MIN_COMMENTS} y ${MAX_COMMENTS}`);
      return;
    }

    setIsAnalyzing(true);
    setError('');
    setAnalysisResult(null);
    setSessionId(null);

    try {
      // ✅ INCLUIR maxComments en la petición
      const response = await axios.post('http://localhost:8000/v1/analyze_video_with_ml', {
        url: youtubeUrl,
        max_comments: maxComments
      });

      if (response.data.success && response.data.session_id) {
        setSessionId(response.data.session_id);
        console.log('🎯 Análisis iniciado con session_id:', response.data.session_id);
        console.log('📊 Máximo comentarios:', maxComments);
      } else {
        throw new Error('No se pudo iniciar el análisis');
      }
    } catch (err) {
      console.error('❌ Error iniciando análisis:', err);
      setError(err.response?.data?.detail || 'Error iniciando el análisis');
      setIsAnalyzing(false);
    }
  };

  // Manejar finalización del análisis
  const handleAnalysisComplete = (data) => {
    console.log('🎉 Análisis completado:', data);
    setAnalysisResult(data);
    setIsAnalyzing(false);
    setSessionId(null);
    
  };

  // Manejar error del análisis
  const handleAnalysisError = (errorMessage) => {
    console.error('❌ Error en análisis:', errorMessage);
    setError(errorMessage);
    setIsAnalyzing(false);
    setSessionId(null);
  };

  // Analizar comentario individual
  const handleAnalyzeComment = async () => {
    if (!comment.trim()) {
      setError('Por favor ingresa un comentario');
      return;
    }

    setIsAnalyzing(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/v1/toxicity/analyze-comment', {
        comment: comment
      });

      setAnalysisResult({ 
        success: true, 
        single_comment: response.data.result 
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Error analizando el comentario');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <>
      {/* 🎯 METADATA ESPECÍFICA PARA ESTA PÁGINA */}
      <AppMetadata 
        pageTitle={getPageTitle()}
        pageDescription={getPageDescription()}
      />
      
      <div className="space-y-6">
        {/* Header */}
        <div className="card">
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-3 bg-accent-100 dark:bg-accent-900/30 rounded-lg">
              <BarChart3 className="h-8 w-8 text-accent-600 dark:text-accent-400" />
            </div>
            <div>
              <h2 className="page-title">Análisis de Toxicidad con IA</h2>
              <p className="text-gray-600 dark:text-gray-300">Analiza comentarios individuales o videos completos de YouTube</p>
            </div>
          </div>
        </div>

        {/* Análisis de Video YouTube - ACTUALIZADO */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <Video className="h-6 w-6 text-secondary-500 dark:text-secondary-400" />
            <h3 className="section-title">Analizar Video de YouTube</h3>
          </div>
          
          <div className="space-y-4">
            {/* Input URL */}
            <div className="flex flex-col md:flex-row md:items-end space-y-4 md:space-y-0 md:space-x-4">
              <div className="flex-1">
                <label className="block text-sm font-medium text-navy-700 dark:text-cream-300 mb-2">
                  URL del Video
                </label>
                <input
                  type="text"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="input-primary w-full"
                  disabled={isAnalyzing}
                />
              </div>
              
              {/* ✅ NUEVO: Selector de número de comentarios */}
              <div className="md:w-48">
                <label className="block text-sm font-medium text-navy-700 dark:text-cream-300 mb-2">
                  Comentarios a analizar
                </label>
                <div className="flex space-x-2">
                  <input
                    type="number"
                    value={maxComments}
                    onChange={(e) => handleMaxCommentsChange(e.target.value)}
                    min={MIN_COMMENTS}
                    max={MAX_COMMENTS}
                    className="input-primary w-20 text-center"
                    disabled={isAnalyzing}
                  />
                  <button
                    type="button"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="p-2 text-navy-500 hover:text-navy-700 dark:text-cream-300 dark:hover:text-cream-100 hover:bg-cream-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    disabled={isAnalyzing}
                  >
                    <Settings className="h-4 w-4" />
                  </button>
                </div>
              </div>

              <button
                onClick={handleAnalyzeVideo}
                disabled={isAnalyzing || !youtubeUrl.trim() || !validateCommentsNumber(maxComments)}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                {isAnalyzing ? (
                  <>
                    <Clock className="h-4 w-4 animate-spin" />
                    <span>Iniciando...</span>
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    <span>Analizar Video</span>
                  </>
                )}
              </button>
            </div>

            {/* ✅ NUEVO: Panel de configuración avanzada */}
            {showAdvanced && (
              <div className="p-4 bg-cream-50 dark:bg-gray-700/50 rounded-lg border border-cream-200 dark:border-gray-600">
                <div className="flex items-center space-x-2 mb-3">
                  <Settings className="h-4 w-4 text-navy-600 dark:text-cream-400" />
                  <h4 className="text-sm font-medium text-navy-700 dark:text-cream-300">Configuración Avanzada</h4>
                </div>
                
                {/* Botones rápidos */}
                <div className="space-y-3">
                  <div>
                    <p className="text-xs text-navy-600 dark:text-cream-400 mb-2">Presets recomendados:</p>
                    <div className="flex flex-wrap gap-2">
                      {RECOMMENDED_COMMENTS.map((preset) => (
                        <button
                          key={preset}
                          onClick={() => setMaxComments(preset)}
                          disabled={isAnalyzing}
                          className={`px-3 py-1 text-xs rounded-full transition-colors ${
                            maxComments === preset
                              ? 'bg-accent-500 text-white'
                              : 'bg-cream-200 dark:bg-gray-600 text-navy-700 dark:text-cream-300 hover:bg-cream-300 dark:hover:bg-gray-500'
                          }`}
                        >
                          {preset}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Información y validación */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                    <div className="p-2 bg-white dark:bg-gray-800 rounded border">
                      <p className="text-navy-500 dark:text-cream-500">Mínimo:</p>
                      <p className="font-medium text-navy-800 dark:text-cream-200">{MIN_COMMENTS} comentarios</p>
                    </div>
                    <div className="p-2 bg-white dark:bg-gray-800 rounded border">
                      <p className="text-navy-500 dark:text-cream-500">Máximo:</p>
                      <p className="font-medium text-navy-800 dark:text-cream-200">{MAX_COMMENTS} comentarios</p>
                    </div>
                    <div className="p-2 bg-white dark:bg-gray-800 rounded border">
                      <p className="text-navy-500 dark:text-cream-500">Tiempo estimado:</p>
                      <p className="font-medium text-navy-800 dark:text-cream-200">
                        {maxComments <= 50 ? '1-2 min' : 
                         maxComments <= 200 ? '2-4 min' : 
                         maxComments <= 500 ? '4-7 min' : '7-12 min'}
                      </p>
                    </div>
                  </div>

                  {/* Indicador de validación */}
                  <div className="flex items-center space-x-2">
                    {validateCommentsNumber(maxComments) ? (
                      <>
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span className="text-xs text-green-600 dark:text-green-400">
                          Configuración válida
                        </span>
                      </>
                    ) : (
                      <>
                        <XCircle className="h-4 w-4 text-red-500" />
                        <span className="text-xs text-red-600 dark:text-red-400">
                          Número debe estar entre {MIN_COMMENTS} y {MAX_COMMENTS}
                        </span>
                      </>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Información básica siempre visible */}
            <div className="flex items-center justify-between text-xs text-navy-600 dark:text-cream-400">
              <span>
                Se analizarán hasta <strong>{maxComments}</strong> comentarios
              </span>
              <span>
                Tiempo estimado: <strong>
                  {maxComments <= 50 ? '1-2 minutos' : 
                   maxComments <= 200 ? '2-4 minutos' : 
                   maxComments <= 500 ? '4-7 minutos' : '7-12 minutos'}
                </strong>
              </span>
            </div>
          </div>
        </div>

        {/* ✅ MOSTRAR loader con progreso (actualizado con número de comentarios) */}
        {isAnalyzing && sessionId && (
          <ProgressLoader 
            sessionId={sessionId}
            onComplete={handleAnalysisComplete}
            onError={handleAnalysisError}
            maxComments={maxComments} // Pasar el número para mostrar en el loader
          />
        )}

        {/* Análisis de Comentario Individual */}
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <MessageCircle className="h-6 w-6 text-accent-500 dark:text-accent-400" />
            <h3 className="section-title">Analizar Comentario Individual</h3>
          </div>
          
          <div className="space-y-4">
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Escribe un comentario para analizar..."
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                         focus:ring-2 focus:ring-accent-500 focus:border-transparent 
                         placeholder-gray-500 dark:placeholder-gray-400 resize-none"
              rows={4}
              disabled={isAnalyzing}
            />
            <div className="flex justify-end">
              <button
                onClick={handleAnalyzeComment}
                disabled={isAnalyzing || !comment.trim()}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isAnalyzing ? (
                  <>
                    <Clock className="h-4 w-4 animate-spin" />
                    <span>Analizando...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    <span>Analizar Comentario</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="card bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
            <div className="flex items-center space-x-3">
              <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          </div>
        )}

        {/* Resultados */}
        {analysisResult && (
          <div className="space-y-6">
            {/* Análisis de comentario individual */}
            {analysisResult.single_comment && (
              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <MessageCircle className="h-6 w-6 text-accent-500 dark:text-accent-400" />
                  <h3 className="section-title">Resultado del Análisis</h3>
                </div>
                
                <div className="space-y-4">
                  <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
                    <p className="text-gray-800 dark:text-gray-200 mb-3">
                      "{analysisResult.single_comment.text}"
                    </p>
                    
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        {/* Estados de toxicidad con nuevos colores */}
                        {analysisResult.single_comment.is_toxic ? (
                          <div className="flex items-center space-x-2">
                            <XCircle className="h-5 w-5 text-wine-500" />
                            <span className="px-3 py-1 toxicity-critical rounded-full text-sm font-medium">
                              Contenido Tóxico
                            </span>
                          </div>
                        ) : (
                          <div className="flex items-center space-x-2">
                            <CheckCircle className="h-5 w-5 text-green-500" />
                            <span className="px-3 py-1 toxicity-safe rounded-full text-sm font-medium">
                              Contenido Limpio
                            </span>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-right">
                        <p className="text-sm text-gray-600 dark:text-gray-400">Nivel de Confianza</p>
                        <p className="text-lg font-bold text-gray-800 dark:text-gray-200">
                          {(analysisResult.single_comment.toxicity_confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>

                    {analysisResult.single_comment.categories_detected.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Categorías detectadas:
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {analysisResult.single_comment.categories_detected.map((category) => (
                            <span 
                              key={category} 
                              className="px-2 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 rounded text-xs font-medium"
                            >
                              {category}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Análisis de video YouTube */}
            {analysisResult.analysis && (
              <div className="space-y-6">
                {/* Resumen general */}
                <div className="card">
                  <div className="flex items-center space-x-3 mb-6">
                    <TrendingUp className="h-6 w-6 text-primary-500 dark:text-accent-400" />
                    <h3 className="section-title">Resumen del Análisis</h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="metric-card text-center">
                      <div className="flex justify-center mb-2">
                        <MessageCircle className="h-8 w-8 text-accent-500 dark:text-accent-400" />
                      </div>
                      <p className="metric-value-primary">{analysisResult.analysis.total_comments}</p>
                      <p className="metric-label">Total Comentarios</p>
                    </div>
                    
                    <div className="metric-card text-center">
                      <div className="flex justify-center mb-2">
                        <AlertTriangle className="h-8 w-8 text-secondary-500 dark:text-secondary-400" />
                      </div>
                      <p className="metric-value-danger">{analysisResult.analysis.toxic_comments}</p>
                      <p className="metric-label">Comentarios Tóxicos</p>
                    </div>
                    
                    <div className="metric-card text-center">
                      <div className="flex justify-center mb-2">
                        <TrendingUp className="h-8 w-8 text-yellow-500 dark:text-yellow-400" />
                      </div>
                      <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400">
                        {(analysisResult.analysis.toxicity_rate * 100).toFixed(1)}%
                      </p>
                      <p className="metric-label">Tasa de Toxicidad</p>
                    </div>
                  </div>
                </div>

                {/* Estadísticas separadas */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="metric-card">
                    <h4 className="text-sm font-medium text-gray-600">Comentarios Principales</h4>
                    <p className="text-2xl font-bold text-primary-500">
                      {analysisResult.analysis.total_comments}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysisResult.analysis.toxic_comments} tóxicos ({(analysisResult.analysis.main_comments_toxicity_rate * 100).toFixed(1)}%)
                    </p>
                  </div>
                  
                  <div className="metric-card">
                    <h4 className="text-sm font-medium text-gray-600">Respuestas</h4>
                    <p className="text-2xl font-bold text-accent-500">
                      {analysisResult.analysis.total_replies}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysisResult.analysis.toxic_replies} tóxicas ({(analysisResult.analysis.replies_toxicity_rate * 100).toFixed(1)}%)
                    </p>
                  </div>
                  
                  <div className="metric-card">
                    <h4 className="text-sm font-medium text-gray-600">Total Analizado</h4>
                    <p className="text-2xl font-bold text-secondary-500">
                      {analysisResult.analysis.total_analyzed}
                    </p>
                    <p className="text-sm text-gray-500">
                      {analysisResult.analysis.total_toxic} tóxicos ({(analysisResult.analysis.toxicity_rate * 100).toFixed(1)}%)
                    </p>
                  </div>
                </div>

                {/* Categorías encontradas */}
                {Object.keys(analysisResult.analysis.summary.categories_found).length > 0 && (
                  <div className="card">
                    <h4 className="section-title mb-4">Categorías de Toxicidad Encontradas</h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                      {Object.entries(analysisResult.analysis.summary.categories_found).map(([category, count]) => (
                        <div key={category} className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
                          <p className="text-sm font-medium text-gray-800 dark:text-gray-200">{category}</p>
                          <div className="flex items-center justify-between mt-1">
                            <span className="text-xs text-gray-600 dark:text-gray-400">Casos</span>
                            <span className="px-2 py-0.5 bg-secondary-100 dark:bg-secondary-900/30 text-secondary-800 dark:text-secondary-300 rounded text-xs font-medium">
                              {count}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Comentario más tóxico */}
                {analysisResult.analysis.summary.most_toxic_comment && (
                  <div className="card">
                    <div className="flex items-center space-x-3 mb-4">
                      <AlertTriangle className="h-6 w-6 text-secondary-500 dark:text-secondary-400" />
                      <h4 className="section-title">Comentario Más Tóxico Detectado</h4>
                    </div>
                    
                    <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                      <p className="text-gray-800 dark:text-gray-200 mb-3">
                        "{analysisResult.analysis.summary.most_toxic_comment.text}"
                      </p>
                      
                      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-2 md:space-y-0">
                        <div className="flex items-center space-x-4">
                          <span className="text-sm font-medium text-red-800 dark:text-red-200">
                            Confianza: {(analysisResult.analysis.summary.most_toxic_comment.toxicity_confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                        
                        {analysisResult.analysis.summary.most_toxic_comment.categories_detected.length > 0 && (
                          <div className="flex flex-wrap gap-1">
                            {analysisResult.analysis.summary.most_toxic_comment.categories_detected.map((cat) => (
                              <span 
                                key={cat} 
                                className="px-2 py-1 bg-red-200 dark:bg-red-800/50 text-red-800 dark:text-red-200 rounded text-xs font-medium"
                              >
                                {cat}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Información del modelo */}
                {analysisResult.analysis.summary.model_info && (
                  <div className="card bg-accent-50 dark:bg-accent-900/20 border-accent-200 dark:border-accent-800">
                    <div className="flex items-center space-x-3 mb-3">
                      <CheckCircle className="h-5 w-5 text-accent-600 dark:text-accent-400" />
                      <h4 className="font-medium text-accent-900 dark:text-accent-200">Información del Modelo</h4>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-accent-700 dark:text-accent-300">Tipo</p>
                        <p className="font-medium text-accent-900 dark:text-accent-100">
                          {analysisResult.analysis.summary.model_info.model_type}
                        </p>
                      </div>
                      <div>
                        <p className="text-accent-700 dark:text-accent-300">Versión</p>
                        <p className="font-medium text-accent-900 dark:text-accent-100">
                          {analysisResult.analysis.summary.model_info.version}
                        </p>
                      </div>
                      <div>
                        <p className="text-accent-700 dark:text-accent-300">Dispositivo</p>
                        <p className="font-medium text-accent-900 dark:text-accent-100">
                          {analysisResult.analysis.summary.model_info.device}
                        </p>
                      </div>
                      <div>
                        <p className="text-accent-700 dark:text-accent-300">Promedio Toxicidad</p>
                        <p className="font-medium text-accent-900 dark:text-accent-100">
                          {(analysisResult.analysis.summary.average_toxicity * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
};

export default AnalyzeTab;