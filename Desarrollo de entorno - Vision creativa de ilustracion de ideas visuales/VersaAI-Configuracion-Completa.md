# 🚀 **VersaAI Platform - Configuración Completa del Proyecto**

## 📁 **Estructura del Proyecto**

```
versaai-platform/
├── 📁 frontend/                    # React + TypeScript Dashboard
│   ├── 📁 public/
│   ├── 📁 src/
│   │   ├── 📁 components/          # Componentes reutilizables
│   │   ├── 📁 pages/               # Páginas del dashboard
│   │   ├── 📁 store/               # Redux Toolkit store
│   │   ├── 📁 services/            # API services
│   │   ├── 📁 hooks/               # Custom hooks
│   │   ├── 📁 utils/               # Utilidades
│   │   ├── 📁 types/               # TypeScript types
│   │   └── 📁 assets/              # Recursos estáticos
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── 📁 backend/                     # Django REST Framework
│   ├── 📁 config/                 # Configuración Django
│   ├── 📁 apps/
│   │   ├── 📁 authentication/     # Auth & usuarios
│   │   ├── 📁 chatbots/           # Gestión de chatbots
│   │   ├── 📁 conversations/      # Conversaciones
│   │   ├── 📁 knowledge_base/     # Sistema RAG
│   │   ├── 📁 analytics/          # Métricas y reportes
│   │   └── 📁 integrations/       # APIs externas
│   ├── 📁 core/                   # Utilidades compartidas
│   ├── requirements.txt
│   ├── manage.py
│   └── Dockerfile
├── 📁 widget/                      # Widget embebible
│   ├── 📁 src/
│   ├── 📁 dist/
│   ├── package.json
│   └── webpack.config.js
├── 📁 docker/                      # Configuración Docker
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── 📁 nginx/
│   └── 📁 scripts/
├── 📁 docs/                        # Documentación
├── 📁 scripts/                     # Scripts de automatización
├── .env.example
├── .gitignore
└── README.md
```

---

## 🐳 **Docker Compose - Configuración Completa**

### **docker-compose.yml**
```yaml
version: '3.8'

services:
  # Base de datos PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: versaai_db
    environment:
      POSTGRES_DB: versaai
      POSTGRES_USER: versaai_user
      POSTGRES_PASSWORD: versaai_password_2024
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U versaai_user -d versaai"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis para caché y sesiones
  redis:
    image: redis:7-alpine
    container_name: versaai_redis
    command: redis-server --appendonly yes --requirepass redis_password_2024
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ChromaDB para vectores
  chromadb:
    image: chromadb/chroma:latest
    container_name: versaai_chromadb
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
    volumes:
      - chromadb_data:/chroma/chroma
    ports:
      - "8001:8000"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Backend Django
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_backend
    environment:
      - DEBUG=True
      - SECRET_KEY=django-secret-key-for-development-only
      - DATABASE_URL=postgresql://versaai_user:versaai_password_2024@db:5432/versaai
      - REDIS_URL=redis://:redis_password_2024@redis:6379/0
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - GROQ_API_KEY=${GROQ_API_KEY}
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
      - CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
    volumes:
      - ./backend:/app
      - media_files:/app/media
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
      chromadb:
        condition: service_healthy
    networks:
      - versaai_network
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"

  # Celery Worker
  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_celery
    environment:
      - DEBUG=True
      - SECRET_KEY=django-secret-key-for-development-only
      - DATABASE_URL=postgresql://versaai_user:versaai_password_2024@db:5432/versaai
      - REDIS_URL=redis://:redis_password_2024@redis:6379/0
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
      - backend
    networks:
      - versaai_network
    command: celery -A config worker -l info

  # Frontend React
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: versaai_frontend
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1
      - VITE_WS_URL=ws://localhost:8000/ws
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - versaai_network
    command: npm run dev

  # Nginx (Opcional para producción)
  nginx:
    image: nginx:alpine
    container_name: versaai_nginx
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
      - media_files:/var/www/media
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend
    networks:
      - versaai_network
    profiles:
      - production

volumes:
  postgres_data:
  redis_data:
  chromadb_data:
  media_files:

networks:
  versaai_network:
    driver: bridge
```

---

## 🐍 **Backend Django - Configuración**

### **requirements.txt**
```txt
# Django Core
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-environ==0.11.2
django-extensions==3.2.3

# Base de datos
psycopg2-binary==2.9.7
redis==5.0.1
django-redis==5.4.0

# Celery para tareas asíncronas
celery==5.3.4
celery[redis]==5.3.4

# IA y Machine Learning
groq==0.4.1
chromadb==0.4.18
langchain==0.0.350
langchain-community==0.0.1
sentence-transformers==2.2.2
numpy==1.24.3
scipy==1.11.4

# Procesamiento de documentos
PyPDF2==3.0.1
python-docx==0.8.11
markdown==3.5.1
beautifulsoup4==4.12.2

# Validación y serialización
marshmallow==3.20.1
django-filter==23.3

# Seguridad
cryptography==41.0.7
argon2-cffi==23.1.0

# Monitoreo y logging
sentry-sdk==1.38.0
django-debug-toolbar==4.2.0

# Testing
pytest==7.4.3
pytest-django==4.7.0
factory-boy==3.3.0

# Utilidades
pillow==10.1.0
requests==2.31.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
```

### **config/settings.py**
```python
import os
from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_extensions',
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.chatbots',
    'apps.conversations',
    'apps.knowledge_base',
    'apps.analytics',
    'apps.integrations',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='versaai'),
        'USER': config('DB_USER', default='versaai_user'),
        'PASSWORD': config('DB_PASSWORD', default='versaai_password_2024'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}

# Redis Configuration
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# AI Configuration
GROQ_API_KEY = config('GROQ_API_KEY', default='')
CHROMA_HOST = config('CHROMA_HOST', default='localhost')
CHROMA_PORT = config('CHROMA_PORT', default='8001')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Security Settings
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

---

## ⚛️ **Frontend React - Configuración**

### **package.json**
```json
{
  "name": "versaai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "@reduxjs/toolkit": "^1.9.7",
    "react-redux": "^8.1.3",
    "@mui/material": "^5.14.18",
    "@mui/icons-material": "^5.14.18",
    "@mui/x-data-grid": "^6.18.1",
    "@mui/x-charts": "^6.18.1",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "axios": "^1.6.0",
    "react-query": "^3.39.3",
    "react-hook-form": "^7.47.0",
    "@hookform/resolvers": "^3.3.2",
    "yup": "^1.3.3",
    "date-fns": "^2.30.0",
    "recharts": "^2.8.0",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "socket.io-client": "^4.7.4",
    "uuid": "^9.0.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@types/uuid": "^9.0.7",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "typescript": "^5.2.2",
    "vite": "^4.5.0",
    "vitest": "^0.34.6",
    "@vitest/ui": "^0.34.6",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^6.1.4",
    "jsdom": "^22.1.0"
  }
}
```

### **vite.config.ts**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@store': path.resolve(__dirname, './src/store'),
      '@services': path.resolve(__dirname, './src/services'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types'),
      '@assets': path.resolve(__dirname, './src/assets'),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          mui: ['@mui/material', '@mui/icons-material'],
          redux: ['@reduxjs/toolkit', 'react-redux'],
        },
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
})
```

### **tsconfig.json**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@pages/*": ["./src/pages/*"],
      "@store/*": ["./src/store/*"],
      "@services/*": ["./src/services/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@utils/*": ["./src/utils/*"],
      "@types/*": ["./src/types/*"],
      "@assets/*": ["./src/assets/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

## 🔧 **Widget Embebible - Configuración**

### **widget/package.json**
```json
{
  "name": "versaai-widget",
  "version": "1.0.0",
  "description": "Widget embebible de VersaAI",
  "main": "dist/widget.js",
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack --mode development --watch",
    "serve": "webpack serve --mode development"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "socket.io-client": "^4.7.4"
  },
  "devDependencies": {
    "@babel/core": "^7.23.3",
    "@babel/preset-env": "^7.23.3",
    "babel-loader": "^9.1.3",
    "css-loader": "^6.8.1",
    "html-webpack-plugin": "^5.5.3",
    "mini-css-extract-plugin": "^2.7.6",
    "style-loader": "^3.3.3",
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.1"
  }
}
```

---

## 📝 **Scripts de Automatización**

### **scripts/setup.sh**
```bash
#!/bin/bash

# Script de configuración inicial de VersaAI Platform
echo "🚀 Configurando VersaAI Platform..."

# Crear directorios necesarios
mkdir -p logs
mkdir -p backend/media
mkdir -p backend/staticfiles

# Copiar archivo de variables de entorno
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Archivo .env creado. Por favor, configura las variables necesarias."
fi

# Construir y levantar servicios
echo "🐳 Construyendo contenedores Docker..."
docker-compose build

echo "🚀 Iniciando servicios..."
docker-compose up -d db redis chromadb

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Ejecutar migraciones
echo "📊 Ejecutando migraciones de base de datos..."
docker-compose run --rm backend python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
docker-compose run --rm backend python manage.py createsuperuser --noinput --email admin@versaai.com || true

# Cargar datos de prueba
echo "📋 Cargando datos de prueba..."
docker-compose run --rm backend python manage.py loaddata fixtures/initial_data.json || true

echo "✅ Configuración completada!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000/api/v1"
echo "📚 Admin: http://localhost:8000/admin"
echo "🔍 ChromaDB: http://localhost:8001"
```

### **scripts/dev.sh**
```bash
#!/bin/bash

# Script para desarrollo
echo "🚀 Iniciando entorno de desarrollo..."

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor, inicia Docker Desktop."
    exit 1
fi

# Levantar servicios de base de datos
echo "🗄️ Iniciando servicios de base de datos..."
docker-compose up -d db redis chromadb

# Esperar a que estén listos
echo "⏳ Esperando servicios..."
sleep 10

# Ejecutar migraciones si es necesario
echo "📊 Verificando migraciones..."
docker-compose run --rm backend python manage.py migrate

# Iniciar backend y frontend
echo "🚀 Iniciando aplicación..."
docker-compose up backend frontend
```

### **scripts/test.sh**
```bash
#!/bin/bash

# Script para ejecutar tests
echo "🧪 Ejecutando tests..."

# Tests del backend
echo "🐍 Tests de Django..."
docker-compose run --rm backend python manage.py test

# Tests del frontend
echo "⚛️ Tests de React..."
docker-compose run --rm frontend npm test

# Tests del widget
echo "🔧 Tests del widget..."
cd widget && npm test

echo "✅ Todos los tests completados!"
```

---

## 🌍 **Variables de Entorno**

### **.env.example**
```env
# Django Configuration
DEBUG=True
SECRET_KEY=django-secret-key-for-development-only
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=versaai
DB_USER=versaai_user
DB_PASSWORD=versaai_password_2024
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://:redis_password_2024@localhost:6379/0

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8001

# AI Configuration
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email Configuration (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sentry (opcional)
SENTRY_DSN=your-sentry-dsn-here

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_GROQ_API_KEY=your-groq-api-key-here
```

---

## 🚀 **Comandos de Inicio Rápido**

```bash
# 1. Clonar y configurar
git clone <repository-url> versaai-platform
cd versaai-platform
chmod +x scripts/*.sh

# 2. Configuración inicial
./scripts/setup.sh

# 3. Desarrollo
./scripts/dev.sh

# 4. Tests
./scripts/test.sh

# 5. Producción
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 **Recursos de Documentación**

### **Enlaces Oficiales:**
- 🐍 [Django REST Framework](https://www.django-rest-framework.org/)
- ⚛️ [React + TypeScript](https://react.dev/learn/typescript)
- 🎨 [Material-UI](https://mui.com/material-ui/getting-started/)
- 🔄 [Redux Toolkit](https://redux-toolkit.js.org/)
- 🐳 [Docker Compose](https://docs.docker.com/compose/)
- 🤖 [Groq API](https://console.groq.com/docs/quickstart)
- 🔍 [ChromaDB](https://docs.trychroma.com/)
- ⚡ [Celery](https://docs.celeryproject.org/)

### **Guías Específicas:**
- 🔐 [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- 🌐 [CORS Configuration](https://github.com/adamchainz/django-cors-headers)
- 📊 [PostgreSQL + Django](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- 🔴 [Redis + Django](https://django-redis.readthedocs.io/)

---

## ✅ **Checklist de Configuración**

- [ ] ✅ Estructura de proyecto creada
- [ ] 🐳 Docker Compose configurado
- [ ] 🐍 Backend Django configurado
- [ ] ⚛️ Frontend React configurado
- [ ] 🔧 Widget embebible configurado
- [ ] 🗄️ Base de datos PostgreSQL
- [ ] 🔴 Redis para caché
- [ ] 🔍 ChromaDB para vectores
- [ ] 🤖 Groq API integrado
- [ ] 🔐 Seguridad JWT configurada
- [ ] 🌐 CORS configurado
- [ ] 📝 Scripts de automatización
- [ ] 🧪 Tests configurados
- [ ] 📚 Documentación completa

---

**🎯 ¡VersaAI Platform está listo para ser desarrollado!**

*Una plataforma completa, moderna y escalable para chatbots con IA* 🚀