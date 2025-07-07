import React, { useState, useEffect } from 'react';
import { Clock, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';

const ProgressLoader = ({ sessionId, onComplete, onError, maxComments = 50 }) => {
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('Iniciando análisis...');
  const [status, setStatus] = useState('connecting');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (!sessionId) return;

    // Conectar WebSocket
    const websocket = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    
    websocket.onopen = () => {
      console.log('🔌 WebSocket conectado');
      setStatus('connected');
      setMessage('Conectado al servidor...');
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📡 Mensaje recibido:', data);

        if (data.type === 'progress') {
          setProgress(data.percentage);
          setMessage(data.message);
          setStatus('processing');
        } else if (data.type === 'completion') {
          if (data.success) {
            setProgress(100);
            setMessage('¡Análisis completado exitosamente!');
            setStatus('completed');
            onComplete && onComplete(data.data);
          } else {
            setStatus('error');
            setMessage(`Error: ${data.error}`);
            onError && onError(data.error);
          }
        }
      } catch (error) {
        console.error('❌ Error parseando mensaje WebSocket:', error);
      }
    };

    websocket.onclose = () => {
      console.log('🔌 WebSocket desconectado');
      if (status === 'processing') {
        setStatus('disconnected');
        setMessage('Conexión perdida');
      }
    };

    websocket.onerror = (error) => {
      console.error('❌ Error WebSocket:', error);
      setStatus('error');
      setMessage('Error de conexión');
    };

    setWs(websocket);

    // Cleanup
    return () => {
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, [sessionId]);

  const getStatusIcon = () => {
    switch (status) {
      case 'connecting':
      case 'connected':
      case 'processing':
        return <Loader2 className="h-6 w-6 animate-spin text-accent-500" />;
      case 'completed':
        return <CheckCircle className="h-6 w-6 text-green-500" />;
      case 'error':
      case 'disconnected':
        return <AlertTriangle className="h-6 w-6 text-wine-500" />;
      default:
        return <Clock className="h-6 w-6 text-navy-500" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'completed':
        return 'text-green-600 dark:text-green-400';
      case 'error':
      case 'disconnected':
        return 'text-wine-600 dark:text-wine-400';
      default:
        return 'text-navy-600 dark:text-accent-400';
    }
  };

  const getProgressBarColor = () => {
    if (progress >= 100) return 'bg-green-500';
    if (status === 'error') return 'bg-wine-500';
    return 'bg-accent-500';
  };

  return (
    <div className="card">
      <div className="flex items-center space-x-4 mb-6">
        {getStatusIcon()}
        <div className="flex-1">
          <h3 className="section-title mb-2">Procesando Análisis</h3>
          <p className={`text-sm ${getStatusColor()}`}>
            {message}
          </p>
          {/* ✅ NUEVA información de configuración */}
          <p className="text-xs text-navy-500 dark:text-cream-500 mt-1">
            📊 Analizando hasta {maxComments} comentarios
          </p>
        </div>
      </div>

      {/* Barra de progreso */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-navy-700 dark:text-cream-300">
            Progreso
          </span>
          <span className="text-sm font-bold text-navy-800 dark:text-cream-200">
            {Math.max(0, Math.min(100, progress))}%
          </span>
        </div>
        
        <div className="w-full bg-cream-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
          <div 
            className={`h-full transition-all duration-500 ease-out ${getProgressBarColor()}`}
            style={{ 
              width: `${Math.max(0, Math.min(100, progress))}%`,
              backgroundImage: status === 'processing' ? 
                'linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.3) 25%, rgba(255,255,255,0.3) 50%, transparent 50%, transparent 75%, rgba(255,255,255,0.3) 75%)' : 
                'none',
              backgroundSize: status === 'processing' ? '20px 20px' : 'auto',
              animation: status === 'processing' ? 'progressStripes 1s linear infinite' : 'none'
            }}
          />
        </div>
      </div>

      {/* GIF divertido */}
      <div className="text-center py-6">
        <div className="inline-block relative">
          <img 
            src="/img/gifgodzilla.gif" 
            alt="Godzilla analizando..." 
            className="h-32 w-auto mx-auto rounded-lg shadow-md"
            style={{ imageRendering: 'pixelated' }}
          />
          <div className="mt-3">
            <p className="text-sm text-navy-600 dark:text-cream-400 font-medium">
              🦖 Godzilla está analizando {maxComments} comentarios...
            </p>
            <p className="text-xs text-navy-500 dark:text-cream-500 mt-1">
              {maxComments <= 50 ? 'Proceso rápido' : 
               maxComments <= 200 ? 'Proceso moderado' : 
               maxComments <= 500 ? 'Proceso extenso' : 'Proceso muy extenso'} - 
              Este proceso puede tomar {
                maxComments <= 50 ? '1-2 minutos' : 
                maxComments <= 200 ? '2-4 minutos' : 
                maxComments <= 500 ? '4-7 minutos' : '7-12 minutos'
              }
            </p>
          </div>
        </div>
      </div>

      {/* Información adicional - ACTUALIZADA */}
      <div className="border-t border-cream-200 dark:border-gray-700 pt-4">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="text-navy-500 dark:text-cream-500">Estado:</p>
            <p className={`font-medium ${getStatusColor()}`}>
              {status === 'connecting' && 'Conectando...'}
              {status === 'connected' && 'Conectado'}
              {status === 'processing' && 'Procesando'}
              {status === 'completed' && 'Completado'}
              {status === 'error' && 'Error'}
              {status === 'disconnected' && 'Desconectado'}
            </p>
          </div>
          
          {/* ✅ NUEVA información de comentarios */}
          <div>
            <p className="text-navy-500 dark:text-cream-500">Comentarios:</p>
            <p className="font-medium text-navy-700 dark:text-cream-300">
              Máximo {maxComments}
            </p>
          </div>
          
          <div>
            <p className="text-navy-500 dark:text-cream-500">Tiempo estimado:</p>
            <p className="font-medium text-navy-700 dark:text-cream-300">
              {progress < 20 ? 
                (maxComments <= 50 ? '1-2 min' : 
                 maxComments <= 200 ? '2-4 min' : 
                 maxComments <= 500 ? '4-7 min' : '7-12 min') : 
               progress < 60 ? 
                (maxComments <= 50 ? '30-60s' : 
                 maxComments <= 200 ? '1-2 min' : 
                 maxComments <= 500 ? '2-4 min' : '4-7 min') : 
               progress < 90 ? '30-60s' : '10-30s'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressLoader;