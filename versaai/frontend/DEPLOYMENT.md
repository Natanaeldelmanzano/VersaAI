# Guía de Despliegue - VersaAI Enterprise Dashboard

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración de Entorno](#configuración-de-entorno)
3. [Despliegue Local](#despliegue-local)
4. [Despliegue en Producción](#despliegue-en-producción)
5. [Configuración de Dominio](#configuración-de-dominio)
6. [Monitoreo y Logs](#monitoreo-y-logs)
7. [Troubleshooting](#troubleshooting)

## 🔧 Requisitos Previos

### Software Necesario
- **Node.js** >= 18.0.0
- **npm** >= 8.0.0
- **Docker** >= 20.10.0 (para despliegue con contenedores)
- **Docker Compose** >= 2.0.0

### Recursos del Servidor
- **CPU**: Mínimo 2 cores, recomendado 4+ cores
- **RAM**: Mínimo 4GB, recomendado 8GB+
- **Almacenamiento**: Mínimo 20GB SSD
- **Ancho de banda**: 100Mbps+

## ⚙️ Configuración de Entorno

### 1. Variables de Entorno

Crea un archivo `.env.production` con las siguientes variables:

```bash
# API Configuration
VITE_API_URL=https://api.versaai.com
VITE_API_VERSION=v1

# App Configuration
VITE_APP_NAME=VersaAI Enterprise Dashboard
VITE_APP_VERSION=2.0.0

# Features
VITE_ENABLE_PWA=true
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_REAL_TIME=true

# Security
VITE_ENABLE_CSP=true
VITE_ENABLE_HTTPS_ONLY=true

# External Services
VITE_GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
VITE_SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 2. Configuración de Docker

Crea un archivo `.env` para Docker Compose:

```bash
# Database
POSTGRES_DB=versaai
POSTGRES_USER=versaai
POSTGRES_PASSWORD=tu_password_seguro

# Redis
REDIS_PASSWORD=tu_redis_password

# JWT
JWT_SECRET=tu_jwt_secret_muy_seguro

# SSL/TLS
ACME_EMAIL=admin@versaai.com

# Monitoring
GRAFANA_PASSWORD=tu_grafana_password
```

## 🚀 Despliegue Local

### Opción 1: Desarrollo

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# El dashboard estará disponible en http://localhost:3000
```

### Opción 2: Build de Producción Local

```bash
# Build optimizado
npm run build:prod

# Preview del build
npm run preview:prod

# El dashboard estará disponible en http://localhost:4173
```

### Opción 3: Docker Local

```bash
# Build y ejecutar con Docker
docker-compose up --build

# Solo frontend en desarrollo
docker-compose --profile development up frontend-dev
```

## 🌐 Despliegue en Producción

### Opción 1: Servidor VPS/Dedicado

#### 1. Preparar el Servidor

```bash
# Actualizar sistema (Ubuntu/Debian)
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar Nginx (si no usas Docker)
sudo apt install nginx -y
```

#### 2. Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/versaai/dashboard-frontend.git
cd dashboard-frontend

# Configurar variables de entorno
cp .env.production.example .env.production
cp .env.example .env

# Editar configuraciones
nano .env.production
nano .env
```

#### 3. Desplegar

```bash
# Despliegue completo con Docker
docker-compose up -d

# Verificar estado
docker-compose ps
docker-compose logs -f frontend
```

### Opción 2: Servicios en la Nube

#### Vercel (Recomendado para Frontend)

1. **Conectar repositorio** en Vercel
2. **Configurar variables de entorno** en el dashboard de Vercel
3. **Configurar build settings**:
   - Build Command: `npm run build:prod`
   - Output Directory: `dist`
   - Install Command: `npm ci`

#### Netlify

1. **Conectar repositorio** en Netlify
2. **Configurar build settings**:
   ```
   Build command: npm run build:prod
   Publish directory: dist
   ```
3. **Configurar redirects** en `netlify.toml`:
   ```toml
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

#### AWS S3 + CloudFront

```bash
# Build para producción
npm run build:prod

# Subir a S3
aws s3 sync dist/ s3://tu-bucket-versaai --delete

# Invalidar CloudFront
aws cloudfront create-invalidation --distribution-id XXXXXX --paths "/*"
```

## 🌍 Configuración de Dominio

### 1. DNS Records

```
# Registros A para IPv4
dashboard.versaai.com.    A    1.2.3.4
api.versaai.com.         A    1.2.3.4

# Registros AAAA para IPv6 (opcional)
dashboard.versaai.com.    AAAA    2001:db8::1

# Registro CNAME para www
www.versaai.com.         CNAME    dashboard.versaai.com.
```

### 2. SSL/TLS Certificate

#### Con Let's Encrypt (Automático con Traefik)

```bash
# Ya configurado en docker-compose.yml
# Traefik manejará automáticamente los certificados
```

#### Manual con Certbot

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d dashboard.versaai.com

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Configuración de Nginx (sin Docker)

```nginx
server {
    listen 80;
    server_name dashboard.versaai.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dashboard.versaai.com;
    
    ssl_certificate /etc/letsencrypt/live/dashboard.versaai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dashboard.versaai.com/privkey.pem;
    
    root /var/www/versaai/dist;
    index index.html;
    
    # Configuración SPA
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoreo y Logs

### 1. Health Checks

```bash
# Verificar estado de servicios
curl -f http://dashboard.versaai.com/health

# Verificar con Docker
docker-compose ps
docker-compose logs frontend
```

### 2. Métricas con Prometheus

Accede a `http://prometheus.versaai.com` para ver métricas.

### 3. Dashboards con Grafana

Accede a `http://grafana.versaai.com` para dashboards visuales.

### 4. Logs Centralizados

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Logs específicos del frontend
docker-compose logs -f frontend

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Error 404 en rutas de Vue Router

**Problema**: Las rutas de Vue Router devuelven 404.

**Solución**: Configurar correctamente el servidor web para SPA:

```nginx
# Nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

#### 2. CORS Errors

**Problema**: Errores de CORS al conectar con la API.

**Solución**: Configurar headers CORS en el backend o proxy:

```nginx
add_header Access-Control-Allow-Origin "https://dashboard.versaai.com";
add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization";
```

#### 3. Problemas de Performance

**Problema**: Carga lenta del dashboard.

**Soluciones**:
- Verificar compresión gzip
- Optimizar imágenes
- Configurar cache headers
- Usar CDN

```bash
# Analizar bundle
npm run build:analyze

# Verificar compresión
curl -H "Accept-Encoding: gzip" -I http://dashboard.versaai.com
```

#### 4. Problemas de SSL

**Problema**: Certificado SSL inválido o expirado.

**Soluciones**:

```bash
# Verificar certificado
openssl s_client -connect dashboard.versaai.com:443 -servername dashboard.versaai.com

# Renovar con Certbot
sudo certbot renew

# Verificar configuración SSL
sudo nginx -t
sudo systemctl reload nginx
```

### Comandos Útiles

```bash
# Reiniciar servicios
docker-compose restart

# Rebuild completo
docker-compose down
docker-compose up --build -d

# Limpiar Docker
docker system prune -a

# Backup de base de datos
docker-compose exec database pg_dump -U versaai versaai > backup.sql

# Restaurar base de datos
docker-compose exec -T database psql -U versaai versaai < backup.sql
```

## 📞 Soporte

Para soporte técnico:
- **Email**: support@versaai.com
- **Documentación**: https://docs.versaai.com
- **Issues**: https://github.com/versaai/dashboard-frontend/issues

---

**Última actualización**: Diciembre 2024  
**Versión**: 2.0.0