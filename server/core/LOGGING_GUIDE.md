# 📋 Guía de Logging Simple - Sistema Actualizado

## 🎯 Descripción

Sistema simple de logging que guarda:
- ✅ **Fecha y hora** completa (YYYY-MM-DD HH:MM:SS)
- ✅ **Tipo de mensaje** con color en consola
- ✅ **Origen exacto** (archivo:función:línea)
- ✅ **Descripción** del mensaje
- ✅ **Archivos diarios** automáticos
- ✅ **Guardado permanente** en `server/logs/`

## 📁 Nueva Estructura

```
nlp-team2/
├── server/
│   ├── core/
│   │   ├── print_dev.py              # Logger simple
│   │   └── LOGGING_GUIDE_UPDATED.md  # Esta guía
│   ├── logs/                         # ← Se crea automáticamente
│   │   ├── 07_07_2025_app.log        # Logs de hoy
│   │   ├── 08_07_2025_app.log        # Logs de mañana
│   │   └── ...
│   ├── main.py
│   ├── scraper/
│   └── ...
└── ...
```

## 🚀 Implementación Básica

### 1. Importar en cualquier archivo de Python:

```python
from server.core.print_dev import log_info, log_error, log_warning, log_debug
```

### 2. Usar en lugar de `print()`:

```python
# Antes:
print("Usuario conectado")
print(f"Error: {e}")

# Ahora:
log_info("Usuario conectado")
log_error(f"Error: {e}")
```

## 📋 Ejemplos de Implementación

### En main.py (API FastAPI):
```python
from fastapi import FastAPI
from server.core.print_dev import log_info, log_error, log_warning

app = FastAPI()

@app.get("/predict")
async def predict_text(text: str):
    log_info(f"Nueva predicción recibida: {text[:50]}...")
    
    try:
        # Tu lógica aquí
        result = model.predict(text)
        log_info(f"Predicción exitosa: {result}")
        return result
        
    except Exception as e:
        log_error(f"Error en predicción: {e}")
        raise

@app.on_event("startup")
async def startup():
    log_info("🚀 Servidor iniciado correctamente")

@app.on_event("shutdown") 
async def shutdown():
    log_warning("🛑 Servidor detenido")
```

### En scraper/scrp.py:
```python
import os
import time
from selenium import webdriver
from server.core.print_dev import log_info, log_error, log_warning, log_debug

class YouTubeCommentScraperChrome:
    def __init__(self, headless=True):
        log_info("🤖 Inicializando scraper de YouTube")
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        log_info("🔧 Configurando Chrome driver")
        try:
            # Tu código de configuración
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            # ... más configuración
            log_info("✅ Chrome driver configurado exitosamente")
        except Exception as e:
            log_error(f"❌ Error configurando driver: {e}")
            raise
    
    def scrape_video_comments(self, video_url, max_comments=50):
        log_info(f"🎬 Iniciando scraping: {video_url}")
        log_info(f"📊 Máximo comentarios: {max_comments}")
        
        try:
            self.setup_driver()
            
            # Proceso de scraping
            log_info("📜 Cargando comentarios...")
            self.scroll_to_load_comments(max_comments)
            
            # Extracción
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")
            log_debug(f"🔍 Encontrados {len(comment_elements)} elementos de comentarios")
            
            # Resultado
            comments_found = len(self.comments_data)
            log_info(f"✅ Scraping completado: {comments_found} comentarios extraídos")
            
        except Exception as e:
            log_error(f"❌ Error en scraping: {e}")
        finally:
            if self.driver:
                log_debug("🧹 Cerrando driver")
                self.driver.quit()
```

### En modelos de ML:
```python
import torch
from transformers import pipeline
from server.core.print_dev import log_info, log_error, log_debug

class ToxicityClassifier:
    def __init__(self):
        log_info("🧠 Inicializando modelo de toxicidad")
        self.model = None
        self.load_model()
    
    def load_model(self):
        try:
            log_debug("📥 Cargando modelo desde Hugging Face")
            self.model = pipeline("text-classification", 
                                model="martin-ha/toxic-comment-model")
            log_info("✅ Modelo cargado exitosamente")
        except Exception as e:
            log_error(f"❌ Error cargando modelo: {e}")
            raise
    
    def predict(self, text: str):
        log_debug(f"🔍 Analizando texto: {text[:30]}...")
        
        try:
            result = self.model(text)
            confidence = result[0]['score']
            label = result[0]['label']
            
            log_info(f"📊 Predicción: {label} (confianza: {confidence:.2f})")
            return result
            
        except Exception as e:
            log_error(f"❌ Error en predicción: {e}")
            return None
```

## 🎨 Tipos de Logging y Colores

| Función | Color Consola | Cuándo Usar | Ejemplo |
|---------|---------------|-------------|---------|
| `log_debug()` | 🔵 Cyan | Información detallada de depuración | `log_debug("Variable X = 123")` |
| `log_info()` | 🟢 Verde | Flujo normal, eventos importantes | `log_info("Usuario autenticado")` |
| `log_warning()` | 🟡 Amarillo | Advertencias, situaciones anómalas | `log_warning("Memoria baja: 85%")` |
| `log_error()` | 🔴 Rojo | Errores, excepciones | `log_error("Base de datos no responde")` |

## 📊 Formato de Salida

### En Consola (con colores):
```
[12:30:15] INFO    | 🚀 Servidor iniciado correctamente
[12:30:45] INFO    | 🎬 Iniciando scraping: https://youtube.com/...
[12:31:02] WARNING | ⚠️ Rate limit detectado, esperando...
[12:31:15] ERROR   | ❌ Error de conexión: timeout
```

### En Archivo (`server/logs/07_07_2025_app.log`):
```
2025-07-07 12:30:15 | INFO    | main.py:startup:25             | 🚀 Servidor iniciado correctamente
2025-07-07 12:30:45 | INFO    | scrp.py:scrape_video_comments:150 | 🎬 Iniciando scraping: https://youtube.com/...
2025-07-07 12:31:02 | WARNING | scrp.py:scroll_to_load:95      | ⚠️ Rate limit detectado, esperando...
2025-07-07 12:31:15 | ERROR   | scrp.py:setup_driver:65        | ❌ Error de conexión: timeout
```

## 🔄 Migración Rápida

### Paso 1: Buscar y reemplazar en todos los archivos
```python
# Buscar:
print(

# Reemplazar por:
log_info(
```

### Paso 2: Importar en cada archivo
```python
# Añadir al inicio de cada archivo:
from server.core.print_dev import log_info, log_error, log_warning, log_debug
```

### Paso 3: Mejorar mensajes con emojis
```python
# Antes:
log_info("Procesando datos")

# Mejor:
log_info("⚙️ Procesando datos de entrada")
```

## ⚡ Ventajas del Sistema

### ✅ **Automático:**
- Detecta automáticamente archivo, función y línea
- Crea archivos diarios sin configuración
- Carpeta `server/logs/` se crea automáticamente

### ✅ **Trazabilidad Completa:**
- Cada log muestra exactamente dónde se originó
- Historial permanente por días
- Fácil búsqueda y análisis

### ✅ **Desarrollo Amigable:**
- Colores en consola para fácil lectura
- Timestamps legibles
- Mensajes descriptivos

### ✅ **Producción Ready:**
- Funciona en cualquier entorno
- Sin dependencias externas complejas
- Archivos de log rotan diariamente

## 🛠️ Personalización Avanzada

### Usar emojis para categorizar:
```python
# APIs
log_info("🌐 API request recibido")
log_info("📤 Respuesta enviada")

# Base de datos
log_info("💾 Conectando a base de datos")
log_error("🔌 Error de conexión DB")

# Scraping
log_info("🤖 Iniciando bot")
log_warning("⏳ Esperando elemento")

# ML/AI
log_info("🧠 Cargando modelo")
log_info("🔍 Analizando texto")
```

### Compatibilidad con código existente:
```python
# La función original sigue funcionando:
from server.core.print_dev import printer_mensaje

printer_mensaje("Mensaje de compatibilidad")
# Se guarda como log_info automáticamente
```

## 🎯 Implementación Inmediata

1. **El sistema ya está listo** - no necesitas configurar nada
2. **Importa y usa** - `from server.core.print_dev import log_info`
3. **Reemplaza print()** - cambia `print()` por `log_info()`
4. **Los logs se guardan automáticamente** en `server/logs/`

## 📝 Resumen de Cambios Realizados

### ✅ **Ubicación de logs actualizada:**
- **Antes:** `logs/` (raíz del proyecto)
- **Ahora:** `server/logs/` (dentro de server)

### ✅ **Comportamiento simplificado:**
- **Antes:** Solo consola en desarrollo
- **Ahora:** Siempre guarda en archivo + siempre muestra en consola

### ✅ **Detección automática mejorada:**
- **Antes:** Usaba `co_function` (incorrecto)
- **Ahora:** Usa `co_name` (correcto)

### ✅ **Formato consistente:**
- Archivo: `YYYY-MM-DD HH:MM:SS | LEVEL | archivo:función:línea | mensaje`
- Consola: `[HH:MM:SS] LEVEL | mensaje` (con colores)

## 🚀 ¡Listo para usar!

**¡Tu sistema de logging está completamente funcional y listo para implementar inmediatamente!** 

Empieza ahora mismo reemplazando tus `print()` por `log_info()` y verás la diferencia inmediatamente. 🎉
