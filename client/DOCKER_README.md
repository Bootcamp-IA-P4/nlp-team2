# Configuración de Docker para el Cliente

Este directorio contiene la configuración para dockerizar el frontend React y desplegarlo en Render.

## Archivos creados:

### 1. `Dockerfile`
- Multi-stage build para optimizar el tamaño de la imagen
- Etapa 1: Build de la aplicación con Node.js
- Etapa 2: Servir con nginx (más eficiente para producción)

### 2. `nginx.conf`
- Configuración de nginx para servir la SPA de React
- Soporte para React Router (todas las rutas redirigen a index.html)
- Compresión gzip habilitada
- Headers de seguridad
- Cache para archivos estáticos

### 3. `.dockerignore`
- Excluye archivos innecesarios del contexto de Docker
- Reduce el tamaño de la imagen y mejora el tiempo de build

### 4. `.env.example`
- Ejemplo de variables de entorno necesarias
- Debes crear `.env.production` basado en este archivo

## Configuración de la API

**IMPORTANTE**: Para que funcionen las peticiones al backend, necesitas:

1. **Modificar `src/hooks/useApiData.js`** para usar variables de entorno:
   ```javascript
   // Cambiar esta línea:
   const API_BASE_URL = 'http://localhost:8000';
   
   // Por esta:
   const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
   ```

2. **Crear archivo `.env.production`**:
   ```
   VITE_API_BASE_URL=https://tu-backend-en-render.onrender.com
   ```

## Despliegue en Render

1. **Conecta tu repositorio** a Render
2. **Configura el servicio** como "Web Service"
3. **Configura las variables**:
   - **Build Command**: `docker build -t client ./client`
   - **Start Command**: `docker run -p 10000:80 client`
   - **Root Directory**: `client`
4. **Variables de entorno** en Render:
   - `VITE_API_BASE_URL`: URL de tu backend en producción

## Comandos para desarrollo local

```bash
# Construir la imagen
docker build -t nlp-client .

# Ejecutar el contenedor
docker run -p 3000:80 nlp-client

# Construir con variable de entorno específica
docker build --build-arg VITE_API_BASE_URL=https://tu-backend.com -t nlp-client .
```

## Notas importantes

- El contenedor expone el puerto 80
- En Render, mapea el puerto 10000:80
- Asegúrate de que tu backend esté configurado para CORS
- El frontend se sirve como archivos estáticos optimizados
