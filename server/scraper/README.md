# YouTube Comment Scraper 🎬

Un scraper de comentarios de YouTube optimizado usando Chrome/Selenium que extrae comentarios, respuestas, emojis y estadísticas de videos de YouTube.

## 🚀 Características

- **Extracción completa de comentarios**: Autor, contenido, likes, tiempo de publicación
- **Procesamiento de respuestas**: Extrae respuestas a comentarios principales
- **Análisis de emojis**: Cuenta y analiza emojis utilizados en comentarios
- **Optimizado para Docker**: Configuración específica para contenedores
- **Navegador sin interfaz**: Modo headless para mejor rendimiento
- **Datos estructurados**: Salida en formato JSON

## 📋 Requisitos

- Python 3.7+
- Google Chrome instalado
- Conexión a Internet

### Dependencias Python

```bash
pip install selenium pandas webdriver-manager emoji
```

## 🛠️ Instalación

1. Clona o descarga el archivo `youtube_scraper_chrome_docker.py`

2. Instala las dependencias:
```bash
pip install selenium pandas webdriver-manager emoji
```

3. Asegúrate de tener Google Chrome instalado en tu sistema

## 📖 Uso

### Uso Básico

```python
from youtube_scraper_chrome_docker import scrape_youtube_comments

# URL del video de YouTube
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"

# Ejecutar scraping
scrape_youtube_comments(video_url, max_comments=100)
```

### Uso como Script

```bash
python youtube_scraper_chrome_docker.py
```

### Variables de Entorno (Docker)

- `MAX_COMMENTS`: Número máximo de comentarios a extraer (default: 1000)
- `ENTOR`: Entorno de ejecución (default: Python)

## 📊 Datos Extraídos

### Información del Video
- ID del video
- URL
- Título
- Descripción
- Autor del canal

### Por cada Comentario
- **Autor**: Nombre del usuario
- **Contenido**: Texto del comentario
- **Likes**: Número de me gusta
- **Tiempo**: Cuándo fue publicado
- **Emojis**: Lista de emojis utilizados
- **Respuestas**: Comentarios de respuesta (si los hay)

### Estadísticas Generales
- Total de comentarios extraídos
- Total de respuestas
- Estadísticas de emojis más utilizados
- Total de likes

## 🔧 Configuración para Docker

El scraper incluye configuraciones optimizadas para Docker:

```python
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
```

## 📄 Formato de Salida

```json
{
  "video_id": "VIDEO_ID",
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "title": "Título del Video",
  "description": "Descripción del video...",
  "author": "Nombre del Canal",
  "total_comments": 50,
  "total_threads": 25,
  "total_emojis": 150,
  "total_likes": 1250,
  "emoji_stats": {
    "😂": 10,
    "❤️": 8,
    "👍": 15
  },
  "most_common_emojis": {
    "👍": 15,
    "😂": 10,
    "❤️": 8
  },
  "threads": [
    {
      "author": "Usuario1",
      "comment": "Excelente video! 👍",
      "likes": 5,
      "published_time": "hace 2 días",
      "emojis": ["👍"],
      "emoji_count": 1,
      "has_replies": true,
      "replies_count": 2,
      "replies": [
        {
          "author": "Usuario2",
          "comment": "Totalmente de acuerdo",
          "likes": 1,
          "emojis": [],
          "emoji_count": 0
        }
      ]
    }
  ]
}
```

## ⚙️ Parámetros de Configuración

### YouTubeCommentScraperChrome

```python
scraper = YouTubeCommentScraperChrome(headless=True)
```

- `headless`: Ejecutar navegador sin interfaz gráfica (recomendado: True)

### scrape_video_comments

```python
data = scraper.scrape_video_comments(video_url, max_comments=50)
```

- `video_url`: URL del video de YouTube
- `max_comments`: Número máximo de comentarios a extraer

## 🐳 Uso con Docker

Este scraper está optimizado para ejecutarse en contenedores Docker. Incluye todas las configuraciones necesarias para Chrome en entornos containerizados.

## ⚠️ Limitaciones

- Depende de la estructura HTML de YouTube (puede cambiar)
- Limitado por las políticas de rate limiting de YouTube
- Requiere conexión a Internet estable
- Algunos comentarios pueden no ser accesibles debido a restricciones de privacidad

## 🛡️ Consideraciones Éticas

- Respeta los términos de servicio de YouTube
- Usa el scraper de manera responsable
- No hagas scraping masivo que pueda sobrecargar los servidores
- Considera la privacidad de los usuarios

## 🔧 Troubleshooting

### Error: Chrome no encontrado
```bash
# En Ubuntu/Debian
sudo apt-get update
sudo apt-get install google-chrome-stable

# En CentOS/RHEL
sudo yum install google-chrome-stable
```

### Error: ChromeDriver
El scraper utiliza `webdriver-manager` que descarga automáticamente la versión correcta de ChromeDriver.

### Error: Timeout
Aumenta los tiempos de espera si tienes una conexión lenta:
```python
time.sleep(5)  # Aumentar valores de sleep
```

## 📝 Notas

- El scraper incluye mecanismos anti-detección básicos
- Funciona mejor con videos públicos que tienen comentarios habilitados
- La extracción de respuestas está limitada a 8 por comentario para optimizar rendimiento

## 🤝 Contribuciones

Si encuentras errores o tienes mejoras, siéntete libre de contribuir al proyecto.

## 📄 Licencia

Este proyecto es de código abierto. Úsalo bajo tu propia responsabilidad y respetando los términos de servicio de YouTube.
