# 🚀 **VersaAI Platform - Flujo de Trabajo Completo**

## 🎯 **Resumen Ejecutivo**

**VersaAI Platform** es una plataforma completa de chatbots con IA que combina un dashboard React + TypeScript, backend Django REST Framework, sistema RAG avanzado y widget embebible. Este documento presenta el flujo de trabajo optimizado y todos los archivos de configuración necesarios.

---

## 📋 **Flujo de Trabajo Recomendado**

### **Fase 1: Configuración del Entorno Base (Día 1-2)**

#### 🏗️ **1.1 Estructura del Proyecto**
```
versaai-platform/
├── 📁 frontend/                 # React + TypeScript Dashboard
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
├── 📁 backend/                  # Django REST Framework
│   ├── apps/
│   ├── config/
│   ├── requirements.txt
│   └── manage.py
├── 📁 widget/                   # JavaScript Embeddable Widget
│   ├── src/
│   ├── dist/
│   └── package.json
├── 📁 docker/                   # Docker Configuration
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── 📁 docs/                     # Documentation
│   ├── api/
│   ├── deployment/
│   └── user-guide/
└── 📁 scripts/                  # Development Scripts
    ├── setup.sh
    ├── dev.sh
    └── deploy.sh
```

#### 🐳 **1.2 Docker Compose Setup**
```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: versaai_db
      POSTGRES_USER: versaai_user
      POSTGRES_PASSWORD: versaai_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U versaai_user -d versaai_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
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
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000

  # Django Backend
  backend:
    build:
      context: ../backend
      dockerfile: ../docker/Dockerfile.backend
    ports:
      - "8001:8000"
    environment:
      - DEBUG=1
      - DATABASE_URL=postgresql://versaai_user:versaai_pass@db:5432/versaai_db
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_URL=http://chromadb:8000
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../backend:/app
      - media_files:/app/media

  # React Frontend
  frontend:
    build:
      context: ../frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8001/api/v1
      - REACT_APP_WS_URL=ws://localhost:8001/ws
    volumes:
      - ../frontend:/app
      - /app/node_modules
    depends_on:
      - backend

  # Celery Worker
  celery:
    build:
      context: ../backend
      dockerfile: ../docker/Dockerfile.backend
    command: celery -A config worker -l info
    environment:
      - DATABASE_URL=postgresql://versaai_user:versaai_pass@db:5432/versaai_db
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_URL=http://chromadb:8000
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ../backend:/app

volumes:
  postgres_data:
  redis_data:
  chroma_data:
  media_files:
```

---

### **Fase 2: Backend Django REST Framework (Día 3-7)**

#### 🐍 **2.1 Configuración Django**
```python
# backend/config/settings.py
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Applications
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
    'django_celery_beat',
    'django_celery_results',
    'channels',
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.organizations',
    'apps.chatbots',
    'apps.conversations',
    'apps.knowledge_base',
    'apps.analytics',
    'apps.integrations',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'versaai_db'),
        'USER': os.getenv('DB_USER', 'versaai_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'versaai_pass'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Redis Configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

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
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# AI Services Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
CHROMA_URL = os.getenv('CHROMA_URL', 'http://localhost:8000')

# File Upload
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

#### 🔐 **2.2 Modelos de Autenticación**
```python
# backend/apps/authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
```

#### 🤖 **2.3 Sistema RAG con Groq**
```python
# backend/apps/ai_services/rag_engine.py
import chromadb
from groq import Groq
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, groq_api_key: str, chroma_url: str):
        self.groq_client = Groq(api_key=groq_api_key)
        self.chroma_client = chromadb.HttpClient(host=chroma_url)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def create_collection(self, collection_name: str):
        """Crear colección en ChromaDB"""
        try:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            return collection
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            return None
    
    def add_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """Agregar documentos a la base de conocimiento"""
        try:
            collection = self.chroma_client.get_collection(collection_name)
            
            texts = [doc['content'] for doc in documents]
            embeddings = self.embedding_model.encode(texts).tolist()
            
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=[doc.get('metadata', {}) for doc in documents],
                ids=[doc['id'] for doc in documents]
            )
            
            logger.info(f"Added {len(documents)} documents to {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def semantic_search(self, collection_name: str, query: str, n_results: int = 5):
        """Búsqueda semántica en la base de conocimiento"""
        try:
            collection = self.chroma_client.get_collection(collection_name)
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            return {
                'documents': results['documents'][0],
                'metadatas': results['metadatas'][0],
                'distances': results['distances'][0]
            }
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return None
    
    def generate_response(self, query: str, context: str, system_prompt: str = None):
        """Generar respuesta usando Groq LLM"""
        try:
            if not system_prompt:
                system_prompt = """
                Eres un asistente de IA útil y preciso. Responde basándote en el contexto proporcionado.
                Si no tienes información suficiente en el contexto, indícalo claramente.
                Mantén un tono profesional y amigable.
                """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Contexto: {context}\n\nPregunta: {query}"}
            ]
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                'response': response.choices[0].message.content,
                'usage': response.usage._asdict() if response.usage else None
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    def rag_query(self, collection_name: str, query: str, system_prompt: str = None):
        """Consulta RAG completa: búsqueda + generación"""
        # 1. Búsqueda semántica
        search_results = self.semantic_search(collection_name, query)
        
        if not search_results or not search_results['documents']:
            return {
                'response': 'No encontré información relevante para responder tu pregunta.',
                'sources': [],
                'usage': None
            }
        
        # 2. Preparar contexto
        context = "\n\n".join(search_results['documents'][:3])
        
        # 3. Generar respuesta
        generation_result = self.generate_response(query, context, system_prompt)
        
        if not generation_result:
            return {
                'response': 'Error al generar la respuesta.',
                'sources': [],
                'usage': None
            }
        
        return {
            'response': generation_result['response'],
            'sources': search_results['metadatas'][:3],
            'usage': generation_result['usage']
        }
```

---

### **Fase 3: Frontend React + TypeScript (Día 8-12)**

#### ⚛️ **3.1 Configuración TypeScript**
```json
// frontend/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": [
      "dom",
      "dom.iterable",
      "ES6"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": "src",
    "paths": {
      "@/*": ["*"],
      "@/components/*": ["components/*"],
      "@/pages/*": ["pages/*"],
      "@/hooks/*": ["hooks/*"],
      "@/services/*": ["services/*"],
      "@/store/*": ["store/*"],
      "@/types/*": ["types/*"],
      "@/utils/*": ["utils/*"]
    }
  },
  "include": [
    "src"
  ]
}
```

#### 🎨 **3.2 Configuración Material-UI + Theme**
```typescript
// frontend/src/theme/index.ts
import { createTheme, ThemeOptions } from '@mui/material/styles';
import { esES } from '@mui/material/locale';

const themeOptions: ThemeOptions = {
  palette: {
    mode: 'light',
    primary: {
      main: '#667eea',
      light: '#9bb5ff',
      dark: '#3f51b5',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#764ba2',
      light: '#a777d3',
      dark: '#4a2c73',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f8fafc',
      paper: '#ffffff',
    },
    text: {
      primary: '#1a202c',
      secondary: '#4a5568',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 24px',
          fontSize: '0.95rem',
          fontWeight: 500,
        },
        contained: {
          boxShadow: '0 2px 8px rgba(102, 126, 234, 0.24)',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(102, 126, 234, 0.32)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff',
          color: '#1a202c',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
};

export const theme = createTheme(themeOptions, esES);
```

#### 🔄 **3.3 Redux Toolkit Store**
```typescript
// frontend/src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { authApi } from './api/authApi';
import { chatbotsApi } from './api/chatbotsApi';
import { conversationsApi } from './api/conversationsApi';
import authSlice from './slices/authSlice';
import uiSlice from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    // RTK Query APIs
    [authApi.reducerPath]: authApi.reducer,
    [chatbotsApi.reducerPath]: chatbotsApi.reducer,
    [conversationsApi.reducerPath]: conversationsApi.reducer,
    
    // Regular slices
    auth: authSlice,
    ui: uiSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [
          'persist/PERSIST',
          'persist/REHYDRATE',
          'persist/PAUSE',
          'persist/PURGE',
          'persist/REGISTER',
        ],
      },
    })
      .concat(authApi.middleware)
      .concat(chatbotsApi.middleware)
      .concat(conversationsApi.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

---

### **Fase 4: Widget Embebible (Día 13-15)**

#### 🔧 **4.1 Widget JavaScript Vanilla**
```javascript
// widget/src/versaai-widget.js
(function() {
    'use strict';
    
    class VersaAIWidget {
        constructor(config) {
            this.config = {
                apiUrl: config.apiUrl || 'https://api.versaai.com',
                chatbotId: config.chatbotId,
                theme: config.theme || 'light',
                position: config.position || 'bottom-right',
                primaryColor: config.primaryColor || '#667eea',
                ...config
            };
            
            this.isOpen = false;
            this.messages = [];
            this.sessionId = this.generateSessionId();
            
            this.init();
        }
        
        init() {
            this.createStyles();
            this.createWidget();
            this.bindEvents();
        }
        
        createStyles() {
            const styles = `
                .versaai-widget {
                    position: fixed;
                    ${this.config.position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
                    ${this.config.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
                    z-index: 10000;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }
                
                .versaai-chat-button {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: ${this.config.primaryColor};
                    border: none;
                    cursor: pointer;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.3s ease;
                }
                
                .versaai-chat-button:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                }
                
                .versaai-chat-window {
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 350px;
                    height: 500px;
                    background: white;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                }
                
                .versaai-chat-header {
                    background: ${this.config.primaryColor};
                    color: white;
                    padding: 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .versaai-chat-messages {
                    flex: 1;
                    padding: 16px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }
                
                .versaai-message {
                    max-width: 80%;
                    padding: 12px 16px;
                    border-radius: 18px;
                    word-wrap: break-word;
                }
                
                .versaai-message.user {
                    background: ${this.config.primaryColor};
                    color: white;
                    align-self: flex-end;
                }
                
                .versaai-message.bot {
                    background: #f1f3f4;
                    color: #333;
                    align-self: flex-start;
                }
                
                .versaai-chat-input {
                    padding: 16px;
                    border-top: 1px solid #e0e0e0;
                    display: flex;
                    gap: 8px;
                }
                
                .versaai-input {
                    flex: 1;
                    padding: 12px;
                    border: 1px solid #e0e0e0;
                    border-radius: 20px;
                    outline: none;
                    font-size: 14px;
                }
                
                .versaai-send-button {
                    padding: 12px 16px;
                    background: ${this.config.primaryColor};
                    color: white;
                    border: none;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 14px;
                }
            `;
            
            const styleSheet = document.createElement('style');
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }
        
        createWidget() {
            const widget = document.createElement('div');
            widget.className = 'versaai-widget';
            widget.innerHTML = `
                <button class="versaai-chat-button" id="versaai-toggle">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                    </svg>
                </button>
                
                <div class="versaai-chat-window" id="versaai-chat">
                    <div class="versaai-chat-header">
                        <h3>VersaAI Assistant</h3>
                        <button id="versaai-close" style="background: none; border: none; color: white; cursor: pointer; font-size: 18px;">×</button>
                    </div>
                    
                    <div class="versaai-chat-messages" id="versaai-messages">
                        <div class="versaai-message bot">
                            ¡Hola! 👋 Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?
                        </div>
                    </div>
                    
                    <div class="versaai-chat-input">
                        <input type="text" class="versaai-input" id="versaai-input" placeholder="Escribe tu mensaje...">
                        <button class="versaai-send-button" id="versaai-send">Enviar</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(widget);
        }
        
        bindEvents() {
            const toggleBtn = document.getElementById('versaai-toggle');
            const closeBtn = document.getElementById('versaai-close');
            const sendBtn = document.getElementById('versaai-send');
            const input = document.getElementById('versaai-input');
            
            toggleBtn.addEventListener('click', () => this.toggleChat());
            closeBtn.addEventListener('click', () => this.closeChat());
            sendBtn.addEventListener('click', () => this.sendMessage());
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }
        
        toggleChat() {
            const chatWindow = document.getElementById('versaai-chat');
            this.isOpen = !this.isOpen;
            chatWindow.style.display = this.isOpen ? 'flex' : 'none';
        }
        
        closeChat() {
            const chatWindow = document.getElementById('versaai-chat');
            this.isOpen = false;
            chatWindow.style.display = 'none';
        }
        
        async sendMessage() {
            const input = document.getElementById('versaai-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            this.addMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch(`${this.config.apiUrl}/widget/${this.config.chatbotId}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: this.sessionId
                    })
                });
                
                const data = await response.json();
                this.addMessage(data.response, 'bot');
                
            } catch (error) {
                console.error('Error sending message:', error);
                this.addMessage('Lo siento, ocurrió un error. Por favor intenta de nuevo.', 'bot');
            }
        }
        
        addMessage(text, sender) {
            const messagesContainer = document.getElementById('versaai-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `versaai-message ${sender}`;
            messageDiv.textContent = text;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        generateSessionId() {
            return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
        }
    }
    
    // Auto-initialize if config is provided
    window.VersaAIWidget = VersaAIWidget;
    
    // Auto-init from script tag data attributes
    const script = document.currentScript;
    if (script && script.dataset.chatbotId) {
        new VersaAIWidget({
            chatbotId: script.dataset.chatbotId,
            apiUrl: script.dataset.apiUrl,
            theme: script.dataset.theme,
            position: script.dataset.position,
            primaryColor: script.dataset.primaryColor
        });
    }
})();
```

---

### **Fase 5: Seguridad y Optimización (Día 16-18)**

#### 🔒 **5.1 Configuración de Seguridad**
```python
# backend/config/security.py
from django.conf import settings
import hashlib
import secrets
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.fernet = Fernet(settings.ENCRYPTION_KEY.encode())
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """Hash password with salt using PBKDF2"""
        if not salt:
            salt = secrets.token_hex(16)
        
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        
        return hashed.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify password against hash"""
        new_hash, _ = SecurityManager.hash_password(password, salt)
        return secrets.compare_digest(new_hash, hashed)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate secure API key"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        return len(api_key) == 43 and api_key.replace('-', '').replace('_', '').isalnum()

# Rate Limiting
from django_ratelimit.decorators import ratelimit
from functools import wraps

def api_rate_limit(group=None, key=None, rate='100/h', method='ALL'):
    """Custom rate limiting decorator for API endpoints"""
    def decorator(func):
        @wraps(func)
        @ratelimit(group=group, key=key, rate=rate, method=method)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 📚 **Recursos y Documentación Oficial**

### **🔗 Enlaces de Referencia**

| Tecnología | Documentación Oficial | Guías Específicas |
|------------|----------------------|-------------------|
| **Django REST Framework** | [DRF Docs](https://www.django-rest-framework.org/) | [Authentication Guide](https://www.django-rest-framework.org/api-guide/authentication/) |
| **React + TypeScript** | [React TypeScript](https://react.dev/learn/typescript) | [TypeScript Handbook](https://www.typescriptlang.org/docs/) |
| **Material-UI** | [MUI Documentation](https://mui.com/material-ui/getting-started/) | [Theming Guide](https://mui.com/material-ui/customization/theming/) |
| **Redux Toolkit** | [RTK Documentation](https://redux-toolkit.js.org/) | [RTK Query Guide](https://redux-toolkit.js.org/rtk-query/overview) |
| **Docker Compose** | [Docker Compose Docs](https://docs.docker.com/compose/) | [Best Practices](https://docs.docker.com/develop/best-practices/) |
| **PostgreSQL** | [PostgreSQL Docs](https://www.postgresql.org/docs/) | [Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization) |
| **Redis** | [Redis Documentation](https://redis.io/documentation) | [Redis Best Practices](https://redis.io/docs/manual/patterns/) |
| **Groq API** | [Groq Documentation](https://console.groq.com/docs/quickstart) | [API Reference](https://console.groq.com/docs/api-reference) |
| **ChromaDB** | [Chroma Documentation](https://docs.trychroma.com/) | [Getting Started](https://docs.trychroma.com/getting-started) |
| **Celery** | [Celery Documentation](https://docs.celeryproject.org/) | [Django Integration](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html) |

---

## 🚀 **Scripts de Automatización**

### **📝 Script de Setup Inicial**
```bash
#!/bin/bash
# scripts/setup.sh

echo "🚀 Configurando VersaAI Platform..."

# Crear directorios
mkdir -p {frontend,backend,widget,docker,docs,scripts}

# Configurar variables de entorno
cp .env.example .env
echo "✅ Archivo .env creado. Por favor configura las variables necesarias."

# Instalar dependencias del backend
echo "📦 Instalando dependencias del backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Instalar dependencias del frontend
echo "📦 Instalando dependencias del frontend..."
cd frontend
npm install
cd ..

# Instalar dependencias del widget
echo "📦 Instalando dependencias del widget..."
cd widget
npm install
cd ..

# Configurar Docker
echo "🐳 Configurando Docker..."
docker-compose -f docker/docker-compose.yml up -d db redis chromadb

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
cd backend
source venv/bin/activate
python manage.py migrate
cd ..

echo "✅ ¡Configuración completada!"
echo "📖 Consulta la documentación en /docs para los siguientes pasos."
```

### **🔄 Script de Desarrollo**
```bash
#!/bin/bash
# scripts/dev.sh

echo "🚀 Iniciando entorno de desarrollo..."

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker."
    exit 1
fi

# Iniciar servicios de base de datos
echo "🐳 Iniciando servicios..."
docker-compose -f docker/docker-compose.yml up -d db redis chromadb

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Iniciar backend en segundo plano
echo "🐍 Iniciando backend Django..."
cd backend
source venv/bin/activate
python manage.py runserver 8001 &
BACKEND_PID=$!
cd ..

# Iniciar Celery worker
echo "⚡ Iniciando Celery worker..."
cd backend
source venv/bin/activate
celery -A config worker -l info &
CELERY_PID=$!
cd ..

# Iniciar frontend
echo "⚛️ Iniciando frontend React..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Función para limpiar procesos al salir
cleanup() {
    echo "\n🛑 Deteniendo servicios..."
    kill $BACKEND_PID $CELERY_PID $FRONTEND_PID 2>/dev/null
    docker-compose -f docker/docker-compose.yml stop
    exit 0
}

# Capturar señal de interrupción
trap cleanup INT

echo "✅ Entorno de desarrollo iniciado!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8001"
echo "📊 Admin: http://localhost:8001/admin"
echo "\nPresiona Ctrl+C para detener todos los servicios."

# Mantener el script corriendo
wait
```

---

## 🎯 **Próximos Pasos Recomendados**

### **Semana 1-2: Configuración Base**
- [ ] Configurar entorno Docker completo
- [ ] Implementar autenticación JWT
- [ ] Crear modelos de datos básicos
- [ ] Configurar CI/CD básico

### **Semana 3-4: Funcionalidades Core**
- [ ] Sistema RAG con ChromaDB
- [ ] Dashboard React básico
- [ ] API REST completa
- [ ] Widget embebible v1

### **Semana 5-6: Optimización**
- [ ] Testing automatizado
- [ ] Optimización de rendimiento
- [ ] Seguridad avanzada
- [ ] Documentación completa

### **Semana 7-8: Producción**
- [ ] Deployment en producción
- [ ] Monitoreo y logging
- [ ] Backup y recuperación
- [ ] Escalabilidad

---

**🎉 ¡VersaAI Platform está listo para ser desarrollado!**

Este flujo de trabajo te guiará paso a paso para crear una plataforma robusta, escalable y moderna de chatbots con IA.