# 🚀 VersaAI Platform - Configuración Completa del Proyecto

## 📁 Estructura del Proyecto

```
versaai-platform/
├── 📁 frontend/                    # React + TypeScript Dashboard
│   ├── 📁 src/
│   │   ├── 📁 components/          # Componentes reutilizables
│   │   ├── 📁 pages/               # Páginas del dashboard
│   │   ├── 📁 store/               # Redux store y slices
│   │   ├── 📁 services/            # APIs y servicios
│   │   ├── 📁 types/               # Tipos TypeScript
│   │   ├── 📁 hooks/               # Custom hooks
│   │   └── 📁 utils/               # Utilidades
│   ├── 📄 package.json
│   ├── 📄 vite.config.ts
│   ├── 📄 tsconfig.json
│   └── 📄 Dockerfile
├── 📁 backend/                     # Django REST Framework
│   ├── 📁 versaai_backend/
│   ├── 📁 apps/
│   │   ├── 📁 authentication/     # Autenticación y usuarios
│   │   ├── 📁 chatbots/           # Gestión de chatbots
│   │   ├── 📁 knowledge_base/     # Sistema RAG
│   │   ├── 📁 analytics/          # Métricas y reportes
│   │   └── 📁 integrations/       # APIs externas
│   ├── 📄 requirements.txt
│   ├── 📄 manage.py
│   └── 📄 Dockerfile
├── 📁 widget/                      # Widget embebible
│   ├── 📁 src/
│   ├── 📄 package.json
│   ├── 📄 webpack.config.js
│   └── 📄 index.html
├── 📁 docker/                      # Configuraciones Docker
│   ├── 📄 nginx.conf
│   ├── 📄 postgres.conf
│   └── 📄 redis.conf
├── 📁 docs/                        # Documentación
├── 📁 scripts/                     # Scripts de automatización
├── 📄 docker-compose.yml
├── 📄 docker-compose.prod.yml
├── 📄 .env.example
├── 📄 .gitignore
└── 📄 README.md
```

## 🐳 Docker Compose - Configuración Principal

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: versaai_postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-versaai}
      POSTGRES_USER: ${POSTGRES_USER:-versaai_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-versaai_password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres.conf:/etc/postgresql/postgresql.conf
    ports:
      - "5432:5432"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-versaai_user}"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache & Celery Broker
  redis:
    image: redis:7-alpine
    container_name: versaai_redis
    command: redis-server /etc/redis/redis.conf
    volumes:
      - redis_data:/data
      - ./docker/redis.conf:/etc/redis/redis.conf
    ports:
      - "6379:6379"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    container_name: versaai_chromadb
    environment:
      CHROMA_SERVER_HOST: 0.0.0.0
      CHROMA_SERVER_HTTP_PORT: 8000
    volumes:
      - chroma_data:/chroma/chroma
    ports:
      - "8000:8000"
    networks:
      - versaai_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Django Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_backend
    environment:
      DEBUG: ${DEBUG:-False}
      SECRET_KEY: ${SECRET_KEY}
      DATABASE_URL: postgresql://${POSTGRES_USER:-versaai_user}:${POSTGRES_PASSWORD:-versaai_password}@postgres:5432/${POSTGRES_DB:-versaai}
      REDIS_URL: redis://redis:6379/0
      CHROMA_HOST: chromadb
      CHROMA_PORT: 8000
      GROQ_API_KEY: ${GROQ_API_KEY}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS:-localhost,127.0.0.1}
      CORS_ALLOWED_ORIGINS: ${CORS_ALLOWED_ORIGINS:-http://localhost:3000}
    volumes:
      - ./backend:/app
      - media_files:/app/media
    ports:
      - "8001:8000"
    depends_on:
      postgres:
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
             gunicorn versaai_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3"

  # Celery Worker
  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_celery_worker
    environment:
      DEBUG: ${DEBUG:-False}
      SECRET_KEY: ${SECRET_KEY}
      DATABASE_URL: postgresql://${POSTGRES_USER:-versaai_user}:${POSTGRES_PASSWORD:-versaai_password}@postgres:5432/${POSTGRES_DB:-versaai}
      REDIS_URL: redis://redis:6379/0
      CHROMA_HOST: chromadb
      CHROMA_PORT: 8000
      GROQ_API_KEY: ${GROQ_API_KEY}
    volumes:
      - ./backend:/app
      - media_files:/app/media
    depends_on:
      - postgres
      - redis
      - backend
    networks:
      - versaai_network
    command: celery -A versaai_backend worker -l info

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: versaai_frontend
    environment:
      VITE_API_BASE_URL: ${VITE_API_BASE_URL:-http://localhost:8001/api}
      VITE_WS_URL: ${VITE_WS_URL:-ws://localhost:8001/ws}
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - versaai_network
    command: npm run dev -- --host 0.0.0.0

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: versaai_nginx
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
      - media_files:/var/www/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
      - frontend
    networks:
      - versaai_network

volumes:
  postgres_data:
  redis_data:
  chroma_data:
  media_files:

networks:
  versaai_network:
    driver: bridge
```

## 🐍 Backend Django - Configuración

### `backend/requirements.txt`

```txt
# Django Core
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-filter==23.3
django-extensions==3.2.3

# Database
psycopg2-binary==2.9.7
django-environ==0.11.2

# Cache & Queue
redis==5.0.1
celery==5.3.4
django-celery-beat==2.5.0
django-celery-results==2.5.1

# AI & RAG
langchain==0.0.335
chromadb==0.4.15
sentence-transformers==2.2.2
groq==0.4.1
numpy==1.24.3
scipy==1.11.4

# File Processing
PyPDF2==3.0.1
python-docx==0.8.11
python-multipart==0.0.6
Pillow==10.0.1

# API Documentation
drf-spectacular==0.26.5

# Security
cryptography==41.0.7
django-ratelimit==4.1.0
django-guardian==2.4.0

# Monitoring & Logging
django-debug-toolbar==4.2.0
sentry-sdk==1.38.0

# Production
gunicorn==21.2.0
whitenoise==6.6.0

# Development
ipython==8.17.2
django-seed==0.3.1
factory-boy==3.3.0
```

### `backend/versaai_backend/settings.py`

```python
import os
from pathlib import Path
import environ
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

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
    'django_filters',
    'drf_spectacular',
    'django_celery_beat',
    'django_celery_results',
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.chatbots',
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
    'django_ratelimit.middleware.RatelimitMiddleware',
]

ROOT_URLCONF = 'versaai_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'versaai_backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='versaai'),
        'USER': env('POSTGRES_USER', default='versaai_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='versaai_password'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'prefer',
        },
    }
}

# Redis Configuration
REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')

# Cache
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
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

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
        'rest_framework.authentication.SessionAuthentication',
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
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
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
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'http://127.0.0.1:3000',
])

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

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'VersaAI Platform API',
    'DESCRIPTION': 'API para la plataforma de chatbots con IA',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1',
}

# AI & RAG Configuration
GROQ_API_KEY = env('GROQ_API_KEY', default='')
CHROMA_HOST = env('CHROMA_HOST', default='localhost')
CHROMA_PORT = env('CHROMA_PORT', default='8000')

# Embedding Model Configuration
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
EMBEDDING_DIMENSION = 384

# RAG Configuration
RAG_CHUNK_SIZE = 1000
RAG_CHUNK_OVERLAP = 200
RAG_TOP_K = 5
RAG_SIMILARITY_THRESHOLD = 0.7

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
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
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'versaai_backend': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Create logs directory
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
```

## ⚛️ Frontend React - Configuración

### `frontend/package.json`

```json
{
  "name": "versaai-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\""
  },
  "dependencies": {
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.16",
    "@mui/material": "^5.14.17",
    "@mui/x-data-grid": "^6.18.1",
    "@mui/x-date-pickers": "^6.18.1",
    "@reduxjs/toolkit": "^1.9.7",
    "axios": "^1.6.0",
    "dayjs": "^1.11.10",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^8.1.3",
    "react-router-dom": "^6.18.0",
    "recharts": "^2.8.0",
    "socket.io-client": "^4.7.4"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.4",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^14.5.1",
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "@vitest/ui": "^0.34.6",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "jsdom": "^22.1.0",
    "prettier": "^3.0.3",
    "typescript": "^5.2.2",
    "vite": "^4.5.0",
    "vitest": "^0.34.6"
  }
}
```

### `frontend/vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@store': path.resolve(__dirname, './src/store'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:8001',
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
    setupFiles: ['./src/test/setup.ts'],
  },
})
```

### `frontend/tsconfig.json`

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
      "@types/*": ["./src/types/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## 🔧 Widget Embebible - Configuración

### `widget/package.json`

```json
{
  "name": "versaai-widget",
  "version": "1.0.0",
  "description": "Widget embebible para VersaAI Platform",
  "main": "dist/versaai-widget.js",
  "scripts": {
    "dev": "webpack serve --mode development",
    "build": "webpack --mode production",
    "build:dev": "webpack --mode development",
    "analyze": "webpack-bundle-analyzer dist/stats.json",
    "test": "jest",
    "lint": "eslint src --ext .js,.ts",
    "format": "prettier --write \"src/**/*.{js,ts,css,html}\""
  },
  "dependencies": {
    "socket.io-client": "^4.7.4"
  },
  "devDependencies": {
    "@babel/core": "^7.23.3",
    "@babel/preset-env": "^7.23.3",
    "@types/jest": "^29.5.8",
    "babel-loader": "^9.1.3",
    "css-loader": "^6.8.1",
    "eslint": "^8.53.0",
    "html-webpack-plugin": "^5.5.3",
    "jest": "^29.7.0",
    "mini-css-extract-plugin": "^2.7.6",
    "prettier": "^3.0.3",
    "style-loader": "^3.3.3",
    "terser-webpack-plugin": "^5.3.9",
    "typescript": "^5.2.2",
    "webpack": "^5.89.0",
    "webpack-bundle-analyzer": "^4.9.1",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.1"
  }
}
```

## 📄 Variables de Entorno

### `.env.example`

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
POSTGRES_DB=versaai
POSTGRES_USER=versaai_user
POSTGRES_PASSWORD=versaai_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# AI Configuration
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8001/api
VITE_WS_URL=ws://localhost:8001/ws
VITE_GROQ_API_KEY=your-groq-api-key-here

# Email Configuration (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Monitoring (opcional)
SENTRY_DSN=your-sentry-dsn-here
```

## 🚀 Scripts de Automatización

### `scripts/setup.sh` (Linux/Mac)

```bash
#!/bin/bash

# VersaAI Platform - Setup Script
echo "🚀 Configurando VersaAI Platform..."

# Crear directorios
echo "📁 Creando estructura de directorios..."
mkdir -p frontend backend widget docs docker scripts

# Copiar archivo de variables de entorno
echo "📄 Configurando variables de entorno..."
cp .env.example .env
echo "⚠️  Recuerda configurar las variables en .env"

# Configurar backend
echo "🐍 Configurando backend Django..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

# Configurar frontend
echo "⚛️ Configurando frontend React..."
cd frontend
npm install
cd ..

# Configurar widget
echo "🔧 Configurando widget..."
cd widget
npm install
cd ..

echo "✅ Configuración completada!"
echo "🚀 Para iniciar el proyecto ejecuta: ./scripts/dev.sh"
```

### `scripts/dev.sh` (Linux/Mac)

```bash
#!/bin/bash

# VersaAI Platform - Development Script
echo "🚀 Iniciando VersaAI Platform en modo desarrollo..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Iniciar servicios con Docker Compose
echo "🐳 Iniciando servicios Docker..."
docker-compose up -d postgres redis chromadb

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Iniciar backend
echo "🐍 Iniciando backend Django..."
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001 &
BACKEND_PID=$!
cd ..

# Iniciar Celery worker
echo "⚡ Iniciando Celery worker..."
cd backend
celery -A versaai_backend worker -l info &
CELERY_PID=$!
cd ..

# Iniciar frontend
echo "⚛️ Iniciando frontend React..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Todos los servicios iniciados!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/api/docs"
echo "🗄️ ChromaDB: http://localhost:8000"

echo "Press Ctrl+C to stop all services"

# Función para limpiar procesos al salir
cleanup() {
    echo "\n🛑 Deteniendo servicios..."
    kill $BACKEND_PID $CELERY_PID $FRONTEND_PID 2>/dev/null
    docker-compose down
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT
wait
```

### `scripts/setup.bat` (Windows)

```batch
@echo off
echo 🚀 Configurando VersaAI Platform...

REM Crear directorios
echo 📁 Creando estructura de directorios...
mkdir frontend backend widget docs docker scripts 2>nul

REM Copiar archivo de variables de entorno
echo 📄 Configurando variables de entorno...
copy .env.example .env
echo ⚠️  Recuerda configurar las variables en .env

REM Configurar backend
echo 🐍 Configurando backend Django...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

REM Configurar frontend
echo ⚛️ Configurando frontend React...
cd frontend
npm install
cd ..

REM Configurar widget
echo 🔧 Configurando widget...
cd widget
npm install
cd ..

echo ✅ Configuración completada!
echo 🚀 Para iniciar el proyecto ejecuta: scripts\dev.bat
pause
```

## 🔗 Enlaces a Documentación Oficial

### 📚 **Documentación Principal**

- **[React Official Documentation](https://react.dev/)** - Documentación oficial de React 18
- **[TypeScript Handbook](https://www.typescriptlang.org/docs/)** - Guía completa de TypeScript
- **[Django REST Framework](https://www.django-rest-framework.org/)** - Framework para APIs REST
- **[Material-UI Documentation](https://mui.com/material-ui/)** - Componentes UI para React
- **[Redux Toolkit](https://redux-toolkit.js.org/)** - Gestión de estado moderna

### 🗄️ **Bases de Datos y Cache**

- **[PostgreSQL Documentation](https://www.postgresql.org/docs/)** - Base de datos relacional
- **[Redis Documentation](https://redis.io/documentation)** - Cache y broker de mensajes
- **[ChromaDB Guide](https://docs.trychroma.com/)** - Base de datos vectorial

### 🤖 **IA y Machine Learning**

- **[Groq API Documentation](https://console.groq.com/docs)** - API de modelos de lenguaje
- **[LangChain Documentation](https://python.langchain.com/)** - Framework para aplicaciones LLM
- **[Sentence Transformers](https://www.sbert.net/)** - Modelos de embeddings

### 🐳 **DevOps y Deployment**

- **[Docker Compose Documentation](https://docs.docker.com/compose/)** - Orquestación de contenedores
- **[Nginx Documentation](https://nginx.org/en/docs/)** - Servidor web y proxy reverso
- **[GitHub Actions](https://docs.github.com/en/actions)** - CI/CD automatizado

### 🔒 **Seguridad**

- **[Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)** - Mejores prácticas de seguridad
- **[JWT.io](https://jwt.io/)** - JSON Web Tokens
- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** - Vulnerabilidades de seguridad

## 🎯 Comandos de Inicio Rápido

```bash
# 1. Clonar y configurar
git clone <repository-url> versaai-platform
cd versaai-platform
cp .env.example .env
# Editar .env con tus configuraciones

# 2. Configuración inicial
./scripts/setup.sh  # Linux/Mac
# o
scripts\setup.bat   # Windows

# 3. Iniciar desarrollo
./scripts/dev.sh    # Linux/Mac
# o
scripts\dev.bat     # Windows

# 4. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend API: http://localhost:8001
# API Docs: http://localhost:8001/api/docs
```

---

**🚀 ¡VersaAI Platform está listo para el desarrollo!**

Esta configuración proporciona una base sólida y escalable para construir una plataforma de chatbots con IA, incluyendo todas las mejores prácticas de desarrollo moderno.