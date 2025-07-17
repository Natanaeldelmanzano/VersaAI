# 🚀 **VersaAI Platform - Documentación Técnica Completa**

## 📋 **Índice**

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Configuración Docker](#configuración-docker)
3. [Backend Django](#backend-django)
4. [Frontend React](#frontend-react)
5. [Widget Embebible](#widget-embebible)
6. [Sistema RAG](#sistema-rag)
7. [Seguridad](#seguridad)
8. [Scripts de Automatización](#scripts-de-automatización)
9. [Variables de Entorno](#variables-de-entorno)
10. [Comandos de Desarrollo](#comandos-de-desarrollo)
11. [Enlaces de Documentación](#enlaces-de-documentación)

---

## 🏗️ **Estructura del Proyecto**

```
versaai-platform/
├── 📁 frontend/                    # React + TypeScript Dashboard
│   ├── 📁 public/
│   ├── 📁 src/
│   │   ├── 📁 components/          # Componentes reutilizables
│   │   │   ├── 📁 common/          # Botones, inputs, modales
│   │   │   ├── 📁 layout/          # Sidebar, header, footer
│   │   │   └── 📁 charts/          # Gráficos y visualizaciones
│   │   ├── 📁 pages/               # Páginas principales
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ChatbotManager.tsx
│   │   │   ├── KnowledgeBase.tsx
│   │   │   └── Analytics.tsx
│   │   ├── 📁 hooks/               # Custom hooks
│   │   ├── 📁 store/               # Redux store
│   │   ├── 📁 services/            # API calls
│   │   ├── 📁 types/               # TypeScript types
│   │   ├── 📁 utils/               # Utilidades
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── 📁 backend/                     # Django REST Framework
│   ├── 📁 apps/
│   │   ├── 📁 authentication/     # JWT, usuarios, organizaciones
│   │   ├── 📁 chatbots/           # Gestión de chatbots
│   │   ├── 📁 knowledge_base/     # RAG, documentos, embeddings
│   │   ├── 📁 analytics/          # Métricas y reportes
│   │   └── 📁 integrations/       # APIs externas, webhooks
│   ├── 📁 core/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── 📁 utils/                  # Utilidades compartidas
│   ├── requirements.txt
│   └── manage.py
│
├── 📁 widget/                      # Widget embebible
│   ├── 📁 src/
│   │   ├── main.js                # Punto de entrada
│   │   ├── chat.js                # Lógica del chat
│   │   ├── styles.css             # Estilos del widget
│   │   └── config.js              # Configuración
│   ├── 📁 dist/                   # Build del widget
│   ├── package.json
│   └── webpack.config.js
│
├── 📁 docker/                      # Configuración Docker
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
│
├── 📁 docs/                        # Documentación
│   ├── api.md
│   ├── deployment.md
│   └── development.md
│
├── 📁 scripts/                     # Scripts de automatización
│   ├── setup.sh
│   ├── dev.sh
│   ├── build.sh
│   └── deploy.sh
│
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## 🐳 **Configuración Docker**

### **docker-compose.yml**

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
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-versaai_user}"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache & Session Store
  redis:
    image: redis:7-alpine
    container_name: versaai_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    container_name: versaai_chromadb
    ports:
      - "8000:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000

  # Django Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_backend
    ports:
      - "8001:8000"
    environment:
      - DEBUG=${DEBUG:-True}
      - SECRET_KEY=${SECRET_KEY}
      - POSTGRES_HOST=postgres
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_HOST=chromadb
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      chromadb:
        condition: service_started
    volumes:
      - ./backend:/app
      - media_files:/app/media
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: versaai_frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8001/api/v1
      - REACT_APP_WIDGET_URL=http://localhost:3000/widget
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

  # Celery Worker
  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: versaai_celery
    environment:
      - DEBUG=${DEBUG:-True}
      - SECRET_KEY=${SECRET_KEY}
      - POSTGRES_HOST=postgres
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_HOST=chromadb
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      - postgres
      - redis
      - chromadb
    volumes:
      - ./backend:/app
    command: celery -A core worker -l info

volumes:
  postgres_data:
  redis_data:
  chromadb_data:
  media_files:

networks:
  default:
    name: versaai_network
```

---

## 🐍 **Backend Django**

### **requirements.txt**

```txt
# Django Core
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-environ==0.11.2
django-extensions==3.2.3

# Database
psycopg2-binary==2.9.7
redis==5.0.1
django-redis==5.4.0

# Celery
celery==5.3.4
celery[redis]==5.3.4

# AI & ML
groq==0.4.1
chromadb==0.4.15
sentence-transformers==2.2.2
langchain==0.0.335
langchain-community==0.0.6

# File Processing
PyPDF2==3.0.1
python-docx==0.8.11
python-magic==0.4.27

# Security
cryptography==41.0.7
argon2-cffi==23.1.0

# Utilities
requests==2.31.0
Pillow==10.1.0
validators==0.22.0

# Development
django-debug-toolbar==4.2.0
ipython==8.17.2
```

### **settings/base.py**

```python
import os
from pathlib import Path
import environ
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Security
SECRET_KEY = env('SECRET_KEY')
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
    'django_extensions',
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='versaai'),
        'USER': env('POSTGRES_USER', default='versaai_user'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}

# Redis Configuration
REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')

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

# REST Framework
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
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# AI Configuration
GROQ_API_KEY = env('GROQ_API_KEY', default='')
CHROMA_HOST = env('CHROMA_HOST', default='localhost')
CHROMA_PORT = env('CHROMA_PORT', default='8000')

# File Upload
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

---

## ⚛️ **Frontend React**

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
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "@reduxjs/toolkit": "^1.9.7",
    "react-redux": "^8.1.3",
    "@mui/material": "^5.14.18",
    "@mui/icons-material": "^5.14.18",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/x-charts": "^6.18.1",
    "@mui/x-data-grid": "^6.18.1",
    "axios": "^1.6.0",
    "react-query": "^3.39.3",
    "react-hook-form": "^7.47.0",
    "yup": "^1.3.3",
    "@hookform/resolvers": "^3.3.2",
    "date-fns": "^2.30.0",
    "recharts": "^2.8.0",
    "react-beautiful-dnd": "^13.1.1",
    "react-markdown": "^9.0.1",
    "prismjs": "^1.29.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "typescript": "^5.2.2",
    "vite": "^4.5.0",
    "vite-tsconfig-paths": "^4.2.1"
  }
}
```

### **vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'
import path from 'path'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@store': path.resolve(__dirname, './src/store'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
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
          charts: ['recharts', '@mui/x-charts'],
        },
      },
    },
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
      "@hooks/*": ["./src/hooks/*"],
      "@store/*": ["./src/store/*"],
      "@services/*": ["./src/services/*"],
      "@types/*": ["./src/types/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

## 🔧 **Widget Embebible**

### **package.json**

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
    "analyze": "webpack-bundle-analyzer dist/stats.json"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.1",
    "css-loader": "^6.8.1",
    "style-loader": "^3.3.3",
    "mini-css-extract-plugin": "^2.7.6",
    "terser-webpack-plugin": "^5.3.9",
    "webpack-bundle-analyzer": "^4.9.1"
  }
}
```

### **src/main.js**

```javascript
// VersaAI Widget - Punto de entrada principal
class VersaAIWidget {
  constructor(config) {
    this.config = {
      apiUrl: 'http://localhost:8001/api/v1',
      chatbotId: null,
      theme: 'light',
      position: 'bottom-right',
      primaryColor: '#4c6ef5',
      ...config
    };
    
    this.isOpen = false;
    this.messages = [];
    this.sessionId = this.generateSessionId();
    
    this.init();
  }

  init() {
    this.createWidget();
    this.attachEventListeners();
    this.loadStyles();
  }

  createWidget() {
    // Crear contenedor principal
    this.container = document.createElement('div');
    this.container.id = 'versaai-widget';
    this.container.className = `versaai-widget ${this.config.position}`;
    
    // Botón flotante
    this.button = document.createElement('button');
    this.button.className = 'versaai-button';
    this.button.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/>
      </svg>
    `;
    
    // Panel de chat
    this.chatPanel = document.createElement('div');
    this.chatPanel.className = 'versaai-chat-panel';
    this.chatPanel.innerHTML = `
      <div class="versaai-header">
        <h3>VersaAI Assistant</h3>
        <button class="versaai-close">×</button>
      </div>
      <div class="versaai-messages" id="versaai-messages"></div>
      <div class="versaai-input-container">
        <input type="text" id="versaai-input" placeholder="Escribe tu mensaje..." />
        <button id="versaai-send">Enviar</button>
      </div>
    `;
    
    this.container.appendChild(this.button);
    this.container.appendChild(this.chatPanel);
    document.body.appendChild(this.container);
  }

  attachEventListeners() {
    // Abrir/cerrar chat
    this.button.addEventListener('click', () => this.toggleChat());
    
    // Cerrar chat
    this.container.querySelector('.versaai-close').addEventListener('click', () => this.closeChat());
    
    // Enviar mensaje
    const sendButton = this.container.querySelector('#versaai-send');
    const input = this.container.querySelector('#versaai-input');
    
    sendButton.addEventListener('click', () => this.sendMessage());
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
  }

  loadStyles() {
    const styles = `
      .versaai-widget {
        position: fixed;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }
      
      .versaai-widget.bottom-right {
        bottom: 20px;
        right: 20px;
      }
      
      .versaai-button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: ${this.config.primaryColor};
        border: none;
        color: white;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
      }
      
      .versaai-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
      }
      
      .versaai-chat-panel {
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        display: none;
        flex-direction: column;
        overflow: hidden;
      }
      
      .versaai-chat-panel.open {
        display: flex;
      }
      
      .versaai-header {
        background: ${this.config.primaryColor};
        color: white;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .versaai-header h3 {
        margin: 0;
        font-size: 16px;
      }
      
      .versaai-close {
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
      }
      
      .versaai-messages {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
      }
      
      .versaai-message {
        margin-bottom: 12px;
        padding: 8px 12px;
        border-radius: 8px;
        max-width: 80%;
      }
      
      .versaai-message.user {
        background: #e3f2fd;
        margin-left: auto;
        text-align: right;
      }
      
      .versaai-message.bot {
        background: #f5f5f5;
      }
      
      .versaai-input-container {
        padding: 15px;
        border-top: 1px solid #eee;
        display: flex;
        gap: 10px;
      }
      
      .versaai-input-container input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 6px;
        outline: none;
      }
      
      .versaai-input-container button {
        padding: 10px 15px;
        background: ${this.config.primaryColor};
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
      }
    `;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    this.chatPanel.classList.toggle('open', this.isOpen);
    
    if (this.isOpen && this.messages.length === 0) {
      this.addMessage('¡Hola! Soy tu asistente de VersaAI. ¿En qué puedo ayudarte?', 'bot');
    }
  }

  closeChat() {
    this.isOpen = false;
    this.chatPanel.classList.remove('open');
  }

  async sendMessage() {
    const input = this.container.querySelector('#versaai-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Agregar mensaje del usuario
    this.addMessage(message, 'user');
    input.value = '';
    
    // Mostrar indicador de escritura
    this.addTypingIndicator();
    
    try {
      // Enviar a la API
      const response = await fetch(`${this.config.apiUrl}/widget/${this.config.chatbotId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: this.sessionId,
        }),
      });
      
      const data = await response.json();
      
      // Remover indicador de escritura
      this.removeTypingIndicator();
      
      // Agregar respuesta del bot
      this.addMessage(data.response, 'bot');
      
    } catch (error) {
      console.error('Error sending message:', error);
      this.removeTypingIndicator();
      this.addMessage('Lo siento, hubo un error. Por favor intenta de nuevo.', 'bot');
    }
  }

  addMessage(text, sender) {
    const messagesContainer = this.container.querySelector('#versaai-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `versaai-message ${sender}`;
    messageDiv.textContent = text;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    this.messages.push({ text, sender, timestamp: new Date() });
  }

  addTypingIndicator() {
    const messagesContainer = this.container.querySelector('#versaai-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'versaai-message bot versaai-typing';
    typingDiv.innerHTML = '<span>●</span><span>●</span><span>●</span>';
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  removeTypingIndicator() {
    const typingIndicator = this.container.querySelector('.versaai-typing');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
  }
}

// Función global para inicializar el widget
window.VersaAIWidget = VersaAIWidget;

// Auto-inicialización si hay configuración en el script tag
const scriptTag = document.currentScript;
if (scriptTag && scriptTag.dataset.chatbotId) {
  new VersaAIWidget({
    chatbotId: scriptTag.dataset.chatbotId,
    apiUrl: scriptTag.dataset.apiUrl,
    theme: scriptTag.dataset.theme,
    primaryColor: scriptTag.dataset.primaryColor,
  });
}
```

---

## 🧠 **Sistema RAG**

### **apps/knowledge_base/services/rag_service.py**

```python
import os
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from groq import Groq
from django.conf import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Configurar ChromaDB
        self.chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=Settings(allow_reset=True)
        )
        
    def create_collection(self, organization_id: int, name: str = None) -> str:
        """Crear una nueva colección para una organización"""
        collection_name = name or f"org_{organization_id}_knowledge"
        
        try:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"organization_id": organization_id}
            )
            logger.info(f"Colección creada: {collection_name}")
            return collection_name
        except Exception as e:
            logger.error(f"Error creando colección: {e}")
            raise
    
    def add_document(self, collection_name: str, document_id: str, 
                    content: str, metadata: Dict[str, Any] = None) -> bool:
        """Agregar un documento a la base de conocimiento"""
        try:
            # Dividir el documento en chunks
            chunks = self._chunk_document(content)
            
            # Generar embeddings
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Preparar metadatos
            chunk_metadata = []
            chunk_ids = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id}_chunk_{i}"
                chunk_meta = {
                    "document_id": document_id,
                    "chunk_index": i,
                    "chunk_size": len(chunk),
                    **(metadata or {})
                }
                
                chunk_ids.append(chunk_id)
                chunk_metadata.append(chunk_meta)
            
            # Obtener colección
            collection = self.chroma_client.get_collection(collection_name)
            
            # Agregar chunks a ChromaDB
            collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=chunk_metadata,
                ids=chunk_ids
            )
            
            logger.info(f"Documento {document_id} agregado con {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error agregando documento: {e}")
            return False
    
    def search_knowledge(self, collection_name: str, query: str, 
                        n_results: int = 5) -> List[Dict[str, Any]]:
        """Buscar en la base de conocimiento"""
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Obtener colección
            collection = self.chroma_client.get_collection(collection_name)
            
            # Realizar búsqueda
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Formatear resultados
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "similarity": 1 - results['distances'][0][i],  # Convertir distancia a similitud
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []
    
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]], 
                         chatbot_config: Dict[str, Any] = None) -> str:
        """Generar respuesta usando Groq con contexto RAG"""
        try:
            # Preparar contexto
            context = "\n\n".join([
                f"Documento {i+1}: {doc['content']}"
                for i, doc in enumerate(context_docs[:3])  # Usar solo los 3 más relevantes
            ])
            
            # Configuración del chatbot
            config = chatbot_config or {}
            system_prompt = config.get('system_prompt', 
                'Eres un asistente útil. Responde basándote en el contexto proporcionado.')
            temperature = config.get('temperature', 0.7)
            model = config.get('ai_model', 'llama3-8b-8192')
            
            # Construir prompt
            prompt = f"""
Contexto relevante:
{context}

Pregunta del usuario: {query}

Instrucciones:
- Responde basándote únicamente en el contexto proporcionado
- Si la información no está en el contexto, indica que no tienes esa información
- Sé conciso y útil
- Responde en español
"""
            
            # Llamar a Groq
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return "Lo siento, hubo un error procesando tu consulta. Por favor intenta de nuevo."
    
    def _chunk_document(self, content: str, chunk_size: int = 1000, 
                       overlap: int = 200) -> List[str]:
        """Dividir documento en chunks con overlap"""
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            
            # Si no es el último chunk, buscar un punto de corte natural
            if end < len(content):
                # Buscar el último punto, nueva línea o espacio antes del límite
                for separator in ['.', '\n', ' ']:
                    last_sep = content.rfind(separator, start, end)
                    if last_sep > start:
                        end = last_sep + 1
                        break
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap if end < len(content) else end
        
        return chunks
    
    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """Eliminar un documento de la base de conocimiento"""
        try:
            collection = self.chroma_client.get_collection(collection_name)
            
            # Buscar todos los chunks del documento
            results = collection.get(
                where={"document_id": document_id}
            )
            
            if results['ids']:
                collection.delete(ids=results['ids'])
                logger.info(f"Documento {document_id} eliminado")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando documento: {e}")
            return False
```

---

## 🔒 **Seguridad**

### **Configuración de Seguridad Django**

```python
# settings/security.py

# Password Hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF Protection
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# Session Security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hora

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# API Security
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/hour',
    'user': '1000/hour',
    'login': '5/min',
    'register': '3/min',
}

# File Upload Security
FILE_UPLOAD_PERMISSIONS = 0o644
ALLOWED_UPLOAD_EXTENSIONS = [
    '.pdf', '.doc', '.docx', '.txt', '.md',
    '.jpg', '.jpeg', '.png', '.gif'
]
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB

# Data Encryption
FIELD_ENCRYPTION_KEY = env('FIELD_ENCRYPTION_KEY', default='')
```

### **Middleware de Seguridad**

```python
# utils/middleware.py

import time
import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Rate limiting por IP
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{client_ip}"
        
        requests_count = cache.get(cache_key, 0)
        if requests_count > 100:  # 100 requests por minuto
            return JsonResponse({
                'error': 'Rate limit exceeded'
            }, status=429)
        
        cache.set(cache_key, requests_count + 1, 60)
        
        # Log de requests sospechosos
        if self.is_suspicious_request(request):
            logger.warning(f"Suspicious request from {client_ip}: {request.path}")
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_suspicious_request(self, request):
        # Detectar patrones sospechosos
        suspicious_patterns = [
            'script', 'javascript:', 'vbscript:', 'onload=', 'onerror='
        ]
        
        query_string = request.META.get('QUERY_STRING', '').lower()
        return any(pattern in query_string for pattern in suspicious_patterns)
```

---

## 🤖 **Scripts de Automatización**

### **scripts/setup.sh** (Linux/Mac)

```bash
#!/bin/bash

# VersaAI Platform - Script de configuración inicial

echo "🚀 Configurando VersaAI Platform..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    
    # Generar SECRET_KEY
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    
    echo "⚠️  Por favor configura las variables de entorno en .env antes de continuar."
    echo "   Especialmente: GROQ_API_KEY, POSTGRES_PASSWORD"
    read -p "Presiona Enter cuando hayas configurado .env..."
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p backend/media
mkdir -p backend/staticfiles
mkdir -p frontend/dist
mkdir -p widget/dist

# Iniciar servicios de base de datos
echo "🐳 Iniciando servicios de base de datos..."
docker-compose up -d postgres redis chromadb

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Configurar backend
echo "🐍 Configurando backend Django..."
cd backend

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

cd ..

# Configurar frontend
echo "⚛️ Configurando frontend React..."
cd frontend

# Instalar dependencias
npm install

# Build inicial
npm run build

cd ..

# Configurar widget
echo "🔧 Configurando widget..."
cd widget

# Instalar dependencias
npm install

# Build inicial
npm run build

cd ..

echo "✅ Configuración completada!"
echo ""
echo "🚀 Para iniciar el entorno de desarrollo:"
echo "   ./scripts/dev.sh"
echo ""
echo "🌐 URLs de acceso:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   Admin Django: http://localhost:8001/admin"
echo "   ChromaDB: http://localhost:8000"
```

### **scripts/dev.sh** (Linux/Mac)

```bash
#!/bin/bash

# VersaAI Platform - Script de desarrollo

echo "🚀 Iniciando entorno de desarrollo VersaAI..."

# Verificar que .env existe
if [ ! -f .env ]; then
    echo "❌ Archivo .env no encontrado. Ejecuta ./scripts/setup.sh primero."
    exit 1
fi

# Iniciar servicios Docker
echo "🐳 Iniciando servicios Docker..."
docker-compose up -d postgres redis chromadb

# Esperar a que los servicios estén listos
echo "⏳ Esperando servicios..."
sleep 5

# Función para manejar la terminación
cleanup() {
    echo "\n🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID $CELERY_PID 2>/dev/null
    docker-compose stop
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar backend Django
echo "🐍 Iniciando backend Django..."
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001 &
BACKEND_PID=$!
cd ..

# Iniciar Celery worker
echo "🔄 Iniciando Celery worker..."
cd backend
celery -A core worker -l info &
CELERY_PID=$!
cd ..

# Iniciar frontend React
echo "⚛️ Iniciando frontend React..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Entorno de desarrollo iniciado!"
echo ""
echo "🌐 URLs disponibles:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8001"
echo "   Admin Django: http://localhost:8001/admin"
echo "   ChromaDB: http://localhost:8000"
echo ""
echo "📝 Logs en tiempo real:"
echo "   Backend: tail -f backend/logs/django.log"
echo "   Celery: tail -f backend/logs/celery.log"
echo ""
echo "🛑 Para detener: Ctrl+C"

# Esperar indefinidamente
wait
```

### **scripts/setup.ps1** (Windows)

```powershell
# VersaAI Platform - Script de configuración para Windows

Write-Host "🚀 Configurando VersaAI Platform..." -ForegroundColor Green

# Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker no está instalado. Por favor instala Docker Desktop primero." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero." -ForegroundColor Red
    exit 1
}

# Crear archivo .env si no existe
if (-not (Test-Path .env)) {
    Write-Host "📝 Creando archivo .env..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    
    # Generar SECRET_KEY
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})
    (Get-Content .env) -replace 'SECRET_KEY=.*', "SECRET_KEY=$secretKey" | Set-Content .env
    
    Write-Host "⚠️  Por favor configura las variables de entorno en .env antes de continuar." -ForegroundColor Yellow
    Write-Host "   Especialmente: GROQ_API_KEY, POSTGRES_PASSWORD" -ForegroundColor Yellow
    Read-Host "Presiona Enter cuando hayas configurado .env..."
}

# Crear directorios necesarios
Write-Host "📁 Creando directorios..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "backend\media"
New-Item -ItemType Directory -Force -Path "backend\staticfiles"
New-Item -ItemType Directory -Force -Path "frontend\dist"
New-Item -ItemType Directory -Force -Path "widget\dist"

# Iniciar servicios de base de datos
Write-Host "🐳 Iniciando servicios de base de datos..." -ForegroundColor Yellow
docker-compose up -d postgres redis chromadb

# Esperar a que los servicios estén listos
Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Configurar backend
Write-Host "🐍 Configurando backend Django..." -ForegroundColor Yellow
Set-Location ..

# Configurar frontend
Write-Host "⚛️ Configurando frontend React..." -ForegroundColor Yellow
Set-Location frontend

# Instalar dependencias
npm install

# Build inicial
npm run build

Set-Location ..

# Configurar widget
Write-Host "🔧 Configurando widget..." -ForegroundColor Yellow
Set-Location widget

# Instalar dependencias
npm install

# Build inicial
npm run build

Set-Location ..

Write-Host "✅ Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Para iniciar el entorno de desarrollo:" -ForegroundColor Cyan
Write-Host "   .\scripts\dev.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URLs de acceso:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8001" -ForegroundColor White
Write-Host "   Admin Django: http://localhost:8001/admin" -ForegroundColor White
Write-Host "   ChromaDB: http://localhost:8000" -ForegroundColor White
```

---

## 🌍 **Variables de Entorno**

### **.env.example**

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
POSTGRES_DB=versaai
POSTGRES_USER=versaai_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000

# AI Configuration
GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-api-key

# Security
FIELD_ENCRYPTION_KEY=your-encryption-key
JWT_SECRET_KEY=your-jwt-secret

# Email Configuration (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Storage Configuration (opcional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# Monitoring (opcional)
SENTRY_DSN=your-sentry-dsn
```

---

## 🚀 **Comandos de Desarrollo**

### **Comandos Principales**

```bash
# Configuración inicial
./scripts/setup.sh          # Linux/Mac
.\scripts\setup.ps1         # Windows

# Desarrollo
./scripts/dev.sh             # Linux/Mac
.\scripts\dev.ps1            # Windows

# Build para producción
./scripts/build.sh           # Linux/Mac
.\scripts\build.ps1          # Windows

# Despliegue
./scripts/deploy.sh          # Linux/Mac
.\scripts\deploy.ps1         # Windows
```

### **Comandos Docker**

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart backend

# Ejecutar comandos en contenedor
docker-compose exec backend python manage.py shell

# Limpiar volúmenes
docker-compose down -v
```

### **Comandos Backend**

```bash
# Activar entorno virtual
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Shell de Django
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic
```

### **Comandos Frontend**

```bash
# Instalar dependencias
npm install

# Desarrollo
npm run dev

# Build
npm run build

# Preview
npm run preview

# Linting
npm run lint
npm run lint:fix

# Type checking
npm run type-check
```

---

## 📚 **Enlaces de Documentación**

### **Frameworks y Librerías**

- **React**: [https://react.dev/](https://react.dev/)
- **TypeScript**: [https://www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)
- **Vite**: [https://vitejs.dev/guide/](https://vitejs.dev/guide/)
- **Material-UI**: [https://mui.com/material-ui/getting-started/](https://mui.com/material-ui/getting-started/)
- **Redux Toolkit**: [https://redux-toolkit.js.org/](https://redux-toolkit.js.org/)
- **Django**: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
- **Django REST Framework**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

### **Bases de Datos y Cache**

- **PostgreSQL**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
- **Redis**: [https://redis.io/docs/](https://redis.io/docs/)
- **ChromaDB**: [https://docs.trychroma.com/](https://docs.trychroma.com/)

### **IA y Machine Learning**

- **Groq API**: [https://console.groq.com/docs/quickstart](https://console.groq.com/docs/quickstart)
- **Sentence Transformers**: [https://www.sbert.net/](https://www.sbert.net/)
- **LangChain**: [https://python.langchain.com/docs/get_started/introduction](https://python.langchain.com/docs/get_started/introduction)

### **Infraestructura**

- **Docker**: [https://docs.docker.com/](https://docs.docker.com/)
- **Docker Compose**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Celery**: [https://docs.celeryq.dev/](https://docs.celeryq.dev/)

### **Seguridad**

- **JWT**: [https://jwt.io/introduction](https://jwt.io/introduction)
- **Django Security**: [https://docs.djangoproject.com/en/4.2/topics/security/](https://docs.djangoproject.com/en/4.2/topics/security/)
- **CORS**: [https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

## 🎯 **Próximos Pasos Recomendados**

### **Fase 1: Configuración Base (Semana 1)**
1. ✅ Ejecutar script de configuración inicial
2. ✅ Configurar variables de entorno
3. ✅ Verificar conexiones a bases de datos
4. ✅ Crear primer superusuario
5. ✅ Probar endpoints básicos de autenticación

### **Fase 2: Desarrollo Core (Semanas 2-3)**
1. 🔄 Implementar modelos de datos completos
2. 🔄 Desarrollar APIs REST principales
3. 🔄 Crear componentes React base
4. 🔄 Configurar sistema de autenticación JWT
5. 🔄 Implementar dashboard básico

### **Fase 3: Sistema RAG (Semana 4)**
1. 🔄 Configurar ChromaDB y embeddings
2. 🔄 Implementar carga de documentos
3. 🔄 Desarrollar búsqueda semántica
4. 🔄 Integrar con Groq API
5. 🔄 Crear interfaz de gestión de conocimiento

### **Fase 4: Widget y Integraciones (Semana 5)**
1. 🔄 Desarrollar widget embebible
2. 🔄 Implementar API para widget
3. 🔄 Crear sistema de webhooks
4. 🔄 Desarrollar integraciones externas
5. 🔄 Optimizar rendimiento

### **Fase 5: Testing y Despliegue (Semana 6)**
1. 🔄 Implementar tests unitarios y de integración
2. 🔄 Configurar CI/CD
3. 🔄 Optimizar para producción
4. 🔄 Configurar monitoreo
5. 🔄 Documentar APIs

---

## 📞 **Soporte y Recursos**

### **Comunidades y Foros**
- **Stack Overflow**: [https://stackoverflow.com/](https://stackoverflow.com/)
- **Reddit Django**: [https://www.reddit.com/r/django/](https://www.reddit.com/r/django/)
- **Reddit React**: [https://www.reddit.com/r/reactjs/](https://www.reddit.com/r/reactjs/)
- **Discord Django**: [https://discord.gg/xcRH6mN4fa](https://discord.gg/xcRH6mN4fa)

### **Herramientas de Desarrollo**
- **VS Code Extensions**: Python, TypeScript, Docker, GitLens
- **Postman**: Para testing de APIs
- **pgAdmin**: Para gestión de PostgreSQL
- **Redis Insight**: Para monitoreo de Redis

---

**🚀 ¡VersaAI Platform está listo para el desarrollo!**

*Esta documentación proporciona todo lo necesario para configurar y desarrollar la plataforma VersaAI con las mejores prácticas y tecnologías modernas.* backend

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
Write-Host "👤 Creando superusuario..." -ForegroundColor Yellow
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

Set-Location