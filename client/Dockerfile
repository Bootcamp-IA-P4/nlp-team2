# Dockerfile para el cliente React
FROM node:18-alpine AS build

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json (si existe)
COPY package*.json ./

# Instalar dependencias (incluye devDependencies para el build)
RUN npm ci

# Copiar el código fuente
COPY . .

# Definir variable de entorno para el build
ARG VITE_API_BASE_URL=https://nlp-server-yhz7mfez3a-ul.a.run.app
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Construir la aplicación para producción
RUN npm run build

# Etapa de producción con nginx
FROM nginx:alpine

# Copiar los archivos construidos desde la etapa de build
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto 80
EXPOSE 80

# Comando para ejecutar nginx
CMD ["nginx", "-g", "daemon off;"]
