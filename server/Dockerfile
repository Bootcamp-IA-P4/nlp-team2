# Usar una imagen base de Python con Chrome preinstalado
FROM python:3.10-slim

# Instalar dependencias del sistema incluyendo Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    gnupg \
    software-properties-common \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /server

# Copiar requirements.txt de producción (sin dependencias de testing)
COPY requirements-production.txt ./requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del servidor (excluyendo tests y archivos innecesarios según .dockerignore)
COPY . .

# Limpiar archivos innecesarios después de la copia
RUN find . -name "*.pyc" -delete && \
    find . -name "__pycache__" -type d -exec rm -rf {} + || true && \
    rm -rf htmlcov/ .coverage .pytest_cache/ tests/ || true

# Crear directorio para datos de salida
RUN mkdir -p /server/output

# Variables de entorno para Chrome y servidor
ENV ENTOR="DOCKER"
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV PYTHONPATH=/server

# Exponer puerto del servidor FastAPI
EXPOSE 8080

# Comando para iniciar el servidor FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
