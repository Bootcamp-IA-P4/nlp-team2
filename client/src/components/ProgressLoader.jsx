import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Clock, AlertTriangle } from 'lucide-react';
import { API_BASE_URL } from '../config';

const ProgressLoader = ({ sessionId, onComplete, onError, maxComments }) => {
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('Conectando...');
  const [status, setStatus] = useState('connecting');
  const [websocket, setWebsocket] = useState(null);
  const [hasConnected, setHasConnected] = useState(false);

  useEffect(() => {
    if (!sessionId) return;

    console.log('🎯 Iniciando WebSocket para session:', sessionId);
    
    // Crear URL WebSocket basada en la configuración de API
    const wsUrl = API_BASE_URL.replace('http', 'ws').replace('https', 'wss');
    const ws = new WebSocket(`${wsUrl}/ws/${sessionId}`);
    setWebsocket(ws);

    ws.onopen = () => {
      console.log('✅ WebSocket conectado exitosamente');
      setStatus('connected');
      setMessage('Conectado al servidor...');
      setHasConnected(true);
    };

    ws.onmessage = (event) => {
      console.log('📨 RAW MESSAGE:', event.data);
      try {
        const data = JSON.parse(event.data);
        console.log('📋 PARSED MESSAGE:', data);
        
        if (data.type === 'progress') {
          setProgress(data.percentage);
          setMessage(data.message);
          setStatus('processing');
          console.log(`📊 Progreso actualizado: ${data.percentage}% - ${data.message}`);
        } 
        else if (data.type === 'completion') {
          setStatus('completed');
          if (data.success) {
            setProgress(100);
            setMessage('Análisis completado exitosamente');
            setTimeout(() => {
              onComplete(data.data);
            }, 1000);
          } else {
            setStatus('error');
            setMessage(`Error: ${data.error}`);
            onError(data.error);
          }
        }
      } catch (error) {
        console.error('❌ Error parseando mensaje WebSocket:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
      setStatus('error');
      setMessage('Error de conexión');
      onError('Error de conexión WebSocket');
    };

    ws.onclose = (event) => {
      console.log('🔌 WebSocket cerrado:', event.code, event.reason);
      if (!hasConnected) {
        setStatus('error');
        setMessage('No se pudo conectar al servidor');
        onError('No se pudo conectar al servidor');
      }
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [sessionId, onComplete, onError, hasConnected]);

  const getProgressBarColor = () => {
    if (status === 'error') return 'bg-red-500';
    if (status === 'completed') return 'bg-green-500';
    if (progress < 30) return 'bg-blue-500';
    if (progress < 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'connecting':
      case 'connected':
      case 'processing':
        return <Clock className="h-6 w-6 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="h-6 w-6 text-green-500" />;
      case 'error':
        return <XCircle className="h-6 w-6 text-red-500" />;
      default:
        return <AlertTriangle className="h-6 w-6 text-yellow-500" />;
    }
  };

  return (
    <div className="card">
      <div className="space-y-6">
        {/* ✅ GIF CENTRADO CON ASPECT RATIO WIDESCREEN */}
        {status === 'processing' || status === 'connected' ? (
          <div className="flex flex-col items-center text-center space-y-4">
            {/* GIF en formato widescreen centrado */}
            <div className="w-full max-w-2xl mx-auto">
              <img 
                src="/img/gifgodzilla.gif" 
                alt="Analizando..." 
                className="w-full h-48 md:h-56 lg:h-64 rounded-lg object-cover object-center"
                style={{ aspectRatio: '16/9' }}
              />
            </div>
            
            {/* ✅ TÍTULO Y PORCENTAJE JUNTOS Y CENTRADOS */}
            <div className="text-center space-y-2">
              <h3 className="text-xl md:text-2xl font-bold text-navy-800 dark:text-cream-100">
                Análisis en Progreso
              </h3>
              <div className="text-4xl md:text-5xl font-bold text-accent-600 dark:text-accent-400">
                {Math.round(progress)}%
              </div>
              <p className="text-sm text-navy-600 dark:text-cream-300">
                {maxComments ? `Analizando hasta ${maxComments} comentarios` : 'Procesando solicitud...'}
              </p>
            </div>
          </div>
        ) : (
          // Para otros estados (connecting, completed, error)
          <div className="flex items-center justify-center space-x-4">
            <div className="h-16 w-16 flex items-center justify-center bg-gray-100 dark:bg-gray-700 rounded-lg">
              {getStatusIcon()}
            </div>
            <div className="text-center">
              <h3 className="text-lg font-semibold text-navy-800 dark:text-cream-100">
                {status === 'connecting' ? 'Conectando...' :
                 status === 'completed' ? 'Análisis Completado' :
                 status === 'error' ? 'Error en el Análisis' : 'Procesando...'}
              </h3>
              <div className="text-2xl font-bold text-accent-600 dark:text-accent-400">
                {Math.round(progress)}%
              </div>
            </div>
          </div>
        )}

        {/* ✅ BARRA DE PROGRESO MEJORADA */}
        <div className="space-y-3">
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
            <div 
              className={`h-4 rounded-full transition-all duration-700 ease-out ${getProgressBarColor()}`}
              style={{ 
                width: `${Math.min(Math.max(progress, 0), 100)}%`,
                boxShadow: progress > 0 ? '0 2px 8px rgba(59, 130, 246, 0.3)' : 'none'
              }}
            />
          </div>
          
          {/* ✅ MENSAJE DE ESTADO CENTRADO */}
          <div className="text-center">
            <span className="text-navy-700 dark:text-cream-200 font-medium">
              {message}
            </span>
          </div>
        </div>

        {/* ✅ INFORMACIÓN DETALLADA - SIN DEBUG INFO */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200 dark:border-gray-600">
          <div className="text-center">
            <div className="text-sm font-medium text-navy-700 dark:text-cream-300">Estado</div>
            <div className={`text-xs px-2 py-1 rounded-full mt-1 ${
              status === 'connecting' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' :
              status === 'connected' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' :
              status === 'processing' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300' :
              status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' :
              'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
            }`}>
              {status === 'connecting' && 'Conectando'}
              {status === 'connected' && 'Conectado'}
              {status === 'processing' && 'Procesando'}
              {status === 'completed' && 'Completado'}
              {status === 'error' && 'Error'}
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-sm font-medium text-navy-700 dark:text-cream-300">Progreso</div>
            <div className="text-xs text-navy-600 dark:text-cream-400 mt-1">
              {progress < 20 ? 'Iniciando...' :
               progress < 40 ? 'Configurando...' :
               progress < 60 ? 'Extrayendo...' :
               progress < 80 ? 'Analizando...' :
               progress < 95 ? 'Finalizando...' : 'Completado'}
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-sm font-medium text-navy-700 dark:text-cream-300">Comentarios</div>
            <div className="text-xs text-navy-600 dark:text-cream-400 mt-1">
              {maxComments ? `Max: ${maxComments}` : 'Configurando...'}
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-sm font-medium text-navy-700 dark:text-cream-300">WebSocket</div>
            <div className="text-xs mt-1">
              <span className={`px-2 py-1 rounded-full ${
                websocket?.readyState === WebSocket.OPEN 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' 
                  : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
              }`}>
                {websocket?.readyState === WebSocket.OPEN ? 'Activo' : 'Inactivo'}
              </span>
            </div>
          </div>
        </div>

        {/* Debug info MEJORADO */}
        {import.meta.env.MODE === 'development' && (
          <div className="mt-4 p-3 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
            <div><strong>🔧 Debug Info:</strong></div>
            <div>Session ID: {sessionId}</div>
            <div>WebSocket State: {websocket?.readyState} 
              {websocket?.readyState === WebSocket.OPEN && ' (CONECTADO ✅)'}
            </div>
            <div>Progress: {progress}%</div>
            <div>Status: {status}</div>
            <div>Message: {message}</div>
            <div>Has Connected: {hasConnected.toString()}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressLoader;