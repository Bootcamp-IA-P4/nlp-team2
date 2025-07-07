import React, { useState } from 'react';
import axios from 'axios';
import { Play, AlertTriangle, MessageCircle, TrendingUp, Clock, Send, Video, CheckCircle, XCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

const AnalyzeTab = () => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [comment, setComment] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');

  // Analizar video de YouTube
  const handleAnalyzeVideo = async () => {
    if (!youtubeUrl.trim()) {
      setError('Por favor ingresa una URL válida');
      return;
    }

    setIsAnalyzing(true);
    setError('');
    setAnalysisResult(null);

    try {
      const response = await axios.post('http://localhost:8000/v1/analyze_video_with_ml', {
        url: youtubeUrl
      });

      setAnalysisResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error analizando el video');
    } finally {
      setIsAnalyzing(false);
    }
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
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-3 bg-accent-100 dark:bg-accent-900/30 rounded-lg">
            <BarChart className="h-8 w-8 text-accent-600 dark:text-accent-400" />
          </div>
          <div>
            <h2 className="page-title">Análisis de Toxicidad con IA</h2>
            <p className="text-gray-600 dark:text-gray-300">Analiza comentarios individuales o videos completos de YouTube</p>
          </div>
        </div>
      </div>

      {/* Análisis de Video YouTube */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Video className="h-6 w-6 text-secondary-500 dark:text-secondary-400" />
          <h3 className="section-title">Analizar Video de YouTube</h3>
        </div>
        
        <div className="space-y-4">
          <div className="flex flex-col md:flex-row md:items-center space-y-4 md:space-y-0 md:space-x-4">
            <input
              type="text"
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg 
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100
                         focus:ring-2 focus:ring-accent-500 focus:border-transparent 
                         placeholder-gray-500 dark:placeholder-gray-400"
              disabled={isAnalyzing}
            />
            <button
              onClick={handleAnalyzeVideo}
              disabled={isAnalyzing || !youtubeUrl.trim()}
              className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <>
                  <Clock className="h-4 w-4 animate-spin" />
                  <span>Analizando...</span>
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  <span>Analizar Video</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

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
  );
};

export default AnalyzeTab;