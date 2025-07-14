# Despliegue en Render - Cliente NLP

## ✅ Imagen Docker subida exitosamente

**Imagen en Docker Hub**: `jcmacias/nlp-client:latest`
**Versión específica**: `jcmacias/nlp-client:v3.0.0`
**Tamaño**: 55.1MB

**🔧 URL del backend actualizada**: `https://nlp-server-yhz7mfez3a-ul.a.run.app`

## 🚀 Configuración para Render

### Método 1: Web Service con Docker

1. **Crear nuevo Web Service** en Render
2. **Configuración básica**:
   - **Service Type**: Web Service
   - **Repository**: Tu repositorio de GitHub
   - **Branch**: main (o la rama que uses)

3. **Configuración Docker**:
   - **Runtime**: Docker
   - **Dockerfile Path**: `client/Dockerfile`
   - **Docker Command**: (dejar vacío, usa el CMD del Dockerfile)

4. **Variables de entorno**:
   ```
   VITE_API_BASE_URL=https://nlp-server-212396604740.us-east5.run.app
   ```

5. **Configuración de puerto**:
   - Render detectará automáticamente el puerto 80
   - No necesitas configurar nada adicional

### Método 2: Static Site (Alternativo)

Si prefieres como sitio estático:

1. **Crear nuevo Static Site** en Render
2. **Build Command**: 
   ```bash
   cd client && npm ci && npm run build
   ```
3. **Publish Directory**: `client/dist`
4. **Variables de entorno**:
   ```
   VITE_API_BASE_URL=https://nlp-server-212396604740.us-east5.run.app
   ```

## 🔧 Comandos útiles para desarrollo

### Ejecutar imagen localmente
```bash
# Desde Docker Hub
docker run -p 3000:80 jcmacias/nlp-client:latest

# Con variables de entorno
docker run -p 3000:80 -e VITE_API_BASE_URL=https://tu-backend.com jcmacias/nlp-client:latest
```

### Actualizar imagen
```bash
# Después de hacer cambios
docker build -t nlp-client .
docker tag nlp-client jcmacias/nlp-client:latest
docker push jcmacias/nlp-client:latest
```

### Crear nueva versión
```bash
# Con nuevo tag de versión
docker tag nlp-client jcmacias/nlp-client:v1.0.1
docker push jcmacias/nlp-client:v1.0.1
```

## 📋 Checklist de despliegue

- ✅ Imagen Docker construida y probada localmente
- ✅ Imagen subida a Docker Hub (`jcmacias/nlp-client:latest`)
- ✅ Variables de entorno configuradas (`.env.example`)
- ✅ API URL actualizada para producción
- ⏳ Configurar servicio en Render
- ⏳ Verificar funcionamiento en producción

## 🌐 URLs importantes

- **Docker Hub**: https://hub.docker.com/r/jcmacias/nlp-client
- **Backend API**: https://nlp-server-212396604740.us-east5.run.app
- **Frontend en Render**: (se generará después del despliegue)

## 🔍 Troubleshooting

### Si hay problemas de CORS
Asegúrate de que tu backend en Google Cloud Run esté configurado para permitir el dominio de Render:
```python
# En tu FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend-en-render.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Si la imagen no se actualiza en Render
1. Crea un nuevo tag de versión
2. Actualiza la configuración en Render para usar el nuevo tag
3. O fuerza un nuevo despliegue en Render

### Verificar logs
En Render, ve a la pestaña "Logs" para ver si hay errores durante el despliegue.
