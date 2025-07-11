FROM python:3.10-slim

# Definimos el directorio de trabajo
WORKDIR /app

# Copiamos la carpeta 'server' dentro de /app/server para que los imports funcionen
COPY . /app/server

# Instalamos las dependencias desde requirements.txt dentro de server
RUN pip install --no-cache-dir -r /app/server/requirements.txt

# Exponemos el puerto 8000
EXPOSE 8000

# Arrancamos uvicorn apuntando a server.main:app
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

