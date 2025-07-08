# Etapa 1: Build con Node
FROM node:18-alpine AS builder

WORKDIR /app

# Copia archivos necesarios para instalar dependencias
COPY package.json package-lock.json ./

RUN npm install

# Copia todo el código fuente del cliente
COPY . .

# Construye la app React con vite
RUN npm run build

# Etapa 2: Servir con nginx
FROM nginx:stable-alpine

# Copia la build de la etapa anterior al folder que nginx sirve
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer el puerto 80 para HTTP
EXPOSE 80

# Comando por defecto: arrancar nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]

