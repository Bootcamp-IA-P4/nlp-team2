import { useState, useEffect } from 'react';

export const useAppInfo = () => {
  const [appInfo, setAppInfo] = useState({
    title: "NLP Team 2 - Análisis de Toxicidad",
    version: "1.0.0", 
    description: "Aplicación para análisis de toxicidad en comentarios de YouTube",
    authors: "NLP Team 2",
    isLoading: true,
    error: null
  });

  useEffect(() => {
    const fetchAppInfo = async () => {
      try {
        console.log('🔍 Obteniendo información de la API...');
        
        //ENDPOINT DE FASTAPI
        const response = await fetch('http://localhost:8000/', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('✅ Información obtenida:', data);

        // MAPEAR LA RESPUESTA DE API
        setAppInfo({
          title: data["Título"] || "NLP Team 2",
          version: data["Version"] || "1.0.0",
          description: data["Descripcion"] || "Aplicación para análisis de toxicidad",
          authors: Array.isArray(data["Autores"]) 
            ? data["Autores"].join(', ') 
            : data["Autores"] || "NLP Team 2",
          endpoints: data.endpoints || {},
          isLoading: false,
          error: null
        });

      } catch (error) {
        console.error('❌ Error obteniendo información de la API:', error);
        setAppInfo(prev => ({
          ...prev,
          isLoading: false,
          error: error.message
        }));
      }
    };

    fetchAppInfo();
  }, []);

  return appInfo;
};

// Hook para títulos dinámicos por página
export const usePageTitle = (title, suffix = " - Análisis de Toxicidad") => {
  useEffect(() => {
    const previousTitle = document.title;
    document.title = title + suffix;
    
    return () => {
      document.title = previousTitle;
    };
  }, [title, suffix]);
};