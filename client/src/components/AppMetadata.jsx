import { useEffect } from 'react';
import { useAppInfo } from '../hooks/useAppInfo';

const AppMetadata = ({ 
  pageTitle = null, 
  pageDescription = null,
  pageSuffix = " - Análisis de Toxicidad" 
}) => {
  const appInfo = useAppInfo();

  useEffect(() => {
    // Función helper para actualizar o crear meta tags
    const updateMetaTag = (name, content, property = false) => {
      if (!content) return;
      
      const selector = property ? `meta[property="${name}"]` : `meta[name="${name}"]`;
      let metaTag = document.querySelector(selector);
      
      if (!metaTag) {
        metaTag = document.createElement('meta');
        if (property) {
          metaTag.setAttribute('property', name);
        } else {
          metaTag.setAttribute('name', name);
        }
        document.head.appendChild(metaTag);
      }
      
      metaTag.content = content;
    };

    // 🎯 CONSTRUIR TÍTULO DINÁMICO
    const finalTitle = pageTitle 
      ? `${pageTitle}${pageSuffix}` 
      : `${appInfo.title} v${appInfo.version}`;

    const finalDescription = pageDescription || appInfo.description;

    // ✅ ACTUALIZAR METADATA CON DATOS DE LA API
    document.title = finalTitle;
    
    updateMetaTag('description', finalDescription);
    updateMetaTag('author', appInfo.authors);
    updateMetaTag('version', appInfo.version);
    updateMetaTag('application-name', appInfo.title);
    updateMetaTag('keywords', 'toxicidad, nlp, machine learning, youtube, análisis, comentarios, ia, inteligencia artificial');
    
    // Open Graph (para redes sociales)
    updateMetaTag('og:title', finalTitle, true);
    updateMetaTag('og:description', finalDescription, true);
    updateMetaTag('og:type', 'website', true);
    updateMetaTag('og:site_name', appInfo.title, true);
    
    // Twitter Card
    updateMetaTag('twitter:card', 'summary_large_image');
    updateMetaTag('twitter:title', finalTitle);
    updateMetaTag('twitter:description', finalDescription);
    
    // Generator tag
    updateMetaTag('generator', `${appInfo.title} v${appInfo.version}`);
    
    // Meta viewport (importante para móviles)
    updateMetaTag('viewport', 'width=device-width, initial-scale=1.0');
    
    console.log('🏷️ Metadata actualizada:', {
      title: finalTitle,
      description: finalDescription,
      author: appInfo.authors,
      version: appInfo.version
    });

  }, [appInfo, pageTitle, pageDescription, pageSuffix]);

  // Mostrar estado de carga en desarrollo
  if (process.env.NODE_ENV === 'development' && appInfo.isLoading) {
    console.log('⏳ Cargando información de la API...');
  }

  if (process.env.NODE_ENV === 'development' && appInfo.error) {
    console.warn('⚠️ Error cargando información:', appInfo.error);
  }

  return null; // Este componente no renderiza nada visible
};

export default AppMetadata;