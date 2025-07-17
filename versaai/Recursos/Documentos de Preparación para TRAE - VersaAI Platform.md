# 🚀 **VersaAI Platform - Documentos para TRAE**

## 📋 **1. Especificaciones Técnicas**

### **Stack Tecnológico Completo**
```yaml
Frontend:
  Framework: "React 18.2+"
  Language: "TypeScript 5.0+"
  State_Management: "Redux Toolkit + RTK Query"
  UI_Library: "Material-UI v5 + Custom Components"
  Build_Tool: "Vite 4.0+"
  Testing: "Jest + React Testing Library + Cypress"
  
Backend:
  Framework: "Django 4.2+ REST Framework"
  Language: "Python 3.11+"
  Database: "PostgreSQL 15+"
  Cache: "Redis 7+"
  Queue: "Celery + Redis"
  Search: "Elasticsearch 8+ (opcional)"
  
AI_Services:
  LLM_Providers: ["OpenAI", "Anthropic", "Groq", "Mistral", "Ollama"]
  Embeddings: "all-MiniLM-L6-v2, OpenAI Ada-002"
  Vector_Stores: ["Pinecone", "ChromaDB", "Weaviate", "Qdrant"]
  
Infrastructure:
  Containerization: "Docker + Docker Compose"
  Orchestration: "Kubernetes (opcional)"
  Monitoring: "Prometheus + Grafana"
  CI_CD: "GitHub Actions"
  
Widget:
  Framework: "Vanilla JS + Web Components"
  Size: "< 50KB gzipped"
  Compatibility: "IE11+, All modern browsers"
```

### **Arquitectura del Sistema**
```mermaid
graph TB
    A[React Dashboard] --> B[API Gateway]
    B --> C[Authentication Service]
    B --> D[Organization Management]
    B --> E[Chatbot Engine]
    B --> F[Knowledge Base RAG]
    B --> G[Analytics Engine]
    
    E --> H[LLM Models]
    E --> I[Conversation Manager]
    F --> J[Vector Database]
    F --> K[Document Processor]
    
    L[Widget SDK] --> B
    M[Mobile Apps] --> B
    N[Third-party Integrations] --> B
```

### **Funcionalidades Core**
```typescript
interface CoreFeatures {
  authentication: {
    jwt_tokens: boolean;
    two_factor_auth: boolean;
    sso_integration: boolean;
    password_reset: boolean;
  };
  
  chatbot_management: {
    visual_flow_editor: boolean;
    ai_model_selection: boolean;
    personality_configuration: boolean;
    response_templates: boolean;
    multilingual_support: boolean;
  };
  
  knowledge_base: {
    document_upload: string[]; // ['pdf', 'docx', 'txt', 'html']
    semantic_search: boolean;
    chunking_strategies: string[]; // ['semantic', 'hierarchical']
    embedding_models: string[];
  };
  
  analytics: {
    real_time_metrics: boolean;
    conversation_analytics: boolean;
    user_behavior_tracking: boolean;
    custom_reports: boolean;
  };
  
  integrations: {
    webhook_support: boolean;
    rest_api: boolean;
    third_party_platforms: string[]; // ['slack', 'discord', 'whatsapp']
  };
}
```

## 🎨 **2. Wireframes del Dashboard**

### **Layout Principal**
```ascii
┌─────────────────────────────────────────────────────────────────┐
│ 🚀 VersaAI Platform                    🔔 👤 Settings ⚙️      │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ │                                               │
│ │ 📊 Overview │ │  ┌─ Dashboard Content Area ─────────────────┐ │
│ │ 🤖 Chatbots │ │  │                                           │ │
│ │ 📚 Knowledge│ │  │  [Dynamic Content Based on Selection]     │ │
│ │ 📈 Analytics│ │  │                                           │ │
│ │ 🔧 Settings │ │  │                                           │ │
│ │ 👥 Team     │ │  │                                           │ │
│ │ 💳 Billing  │ │  │                                           │ │
│ │ 📖 Docs     │ │  │                                           │ │
│ └─────────────┘ │  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **Dashboard Overview**
```ascii
┌─ Overview Dashboard ──────────────────────────────────────────────┐
│                                                                   │
│ ┌─ Quick Stats ──────────────────────────────────────────────────┐ │
│ │ 📊 Total Conversations: 1,234  📈 This Month: +23%            │ │
│ │ 🤖 Active Chatbots: 5          ⚡ Avg Response: 1.2s          │ │
│ │ 👥 Team Members: 8             💾 Storage Used: 234MB/1GB     │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                   │
│ ┌─ Recent Activity ─────────────┐ ┌─ Performance Chart ─────────┐ │
│ │ • New conversation started    │ │    📈                       │ │
│ │ • Document uploaded to KB     │ │   /│  \                     │ │
│ │ • Chatbot "Support" updated   │ │  / │   \                    │ │
│ │ • Team member invited        │ │ /  │    \                   │ │
│ │ • [View all activities]      │ │    │     \                  │ │
│ └───────────────────────────────┘ └─────────────────────────────┘ │
│                                                                   │
│ ┌─ Quick Actions ─────────────────────────────────────────────────┐ │
│ │ [+ New Chatbot] [📄 Upload Docs] [⚙️ Settings] [👥 Invite]    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### **Chatbot Management**
```ascii
┌─ Chatbot Management ──────────────────────────────────────────────┐
│                                                                   │
│ ┌─ Chatbot List ────────────────────────────────────────────────┐ │
│ │                                              [+ New Chatbot]  │ │
│ │ ┌─ Support Bot ──────────────────────────────────────────────┐ │ │
│ │ │ 🤖 Status: ✅ Active    📊 Conversations: 456             │ │ │
│ │ │ 🎯 Purpose: Customer Support                               │ │ │
│ │ │ 🧠 Model: GPT-4 Turbo    📈 Satisfaction: 4.2/5          │ │ │
│ │ │ [Edit] [Test] [Analytics] [Settings] [⋯]                  │ │ │
│ │ └────────────────────────────────────────────────────────────┘ │ │
│ │                                                               │ │
│ │ ┌─ Sales Assistant ──────────────────────────────────────────┐ │ │
│ │ │ 🤖 Status: 🟡 Draft     📊 Conversations: 0              │ │ │
│ │ │ 🎯 Purpose: Lead Generation                                │ │ │
│ │ │ 🧠 Model: Claude-3       📈 Satisfaction: N/A             │ │ │
│ │ │ [Edit] [Test] [Deploy] [Settings] [⋯]                     │ │ │
│ │ └────────────────────────────────────────────────────────────┘ │ │
│ └───────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### **Visual Flow Editor**
```ascii
┌─ Visual Flow Editor ──────────────────────────────────────────────┐
│ [💾 Save] [▶️ Test] [📋 Templates] [⚙️ Settings]                  │
│                                                                   │
│ ┌─ Node Palette ─┐ ┌─ Canvas ─────────────────────────────────────┐ │
│ │ 💬 Message     │ │                                             │ │
│ │ ❓ Question    │ │    ┌─ Start ─┐                              │ │
│ │ 🔀 Condition   │ │    │ Welcome │ ──────┐                     │ │
│ │ 🔍 Knowledge   │ │    └─────────┘       ▼                     │ │
│ │ 🌐 API Call    │ │                 ┌─ Question ─┐             │ │
│ │ 📝 Input       │ │                 │ How can I  │             │ │
│ │ 🎯 Action      │ │                 │ help you?  │             │ │
│ │ 🔗 Webhook     │ │                 └────────────┘             │ │
│ └────────────────┘ │                       │                    │ │
│                    │                       ▼                    │ │
│                    │                 ┌─ Condition ─┐           │ │
│                    │                 │ Intent      │           │ │
│                    │                 │ Detection   │           │ │
│                    │                 └─────────────┘           │ │
│                    └─────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

## 🔗 **3. API Endpoints Definidos**

### **Authentication Endpoints**
```http
# Registro y autenticación
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/auth/verify-email?token={token}
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password

# 2FA
POST   /api/v1/auth/2fa/setup
POST   /api/v1/auth/2fa/verify
POST   /api/v1/auth/2fa/disable
GET    /api/v1/auth/2fa/backup-codes
```

### **User & Organization Management**
```http
# Usuario
GET    /api/v1/users/profile
PUT    /api/v1/users/profile
POST   /api/v1/users/upload-avatar
DELETE /api/v1/users/account

# Organización
GET    /api/v1/organizations
POST   /api/v1/organizations
GET    /api/v1/organizations/{org_id}
PUT    /api/v1/organizations/{org_id}
DELETE /api/v1/organizations/{org_id}

# Miembros del equipo
GET    /api/v1/organizations/{org_id}/members
POST   /api/v1/organizations/{org_id}/members/invite
PUT    /api/v1/organizations/{org_id}/members/{user_id}
DELETE /api/v1/organizations/{org_id}/members/{user_id}
```

### **Chatbot Management**
```http
# CRUD Chatbots
GET    /api/v1/chatbots
POST   /api/v1/chatbots
GET    /api/v1/chatbots/{chatbot_id}
PUT    /api/v1/chatbots/{chatbot_id}
DELETE /api/v1/chatbots/{chatbot_id}

# Configuración
GET    /api/v1/chatbots/{chatbot_id}/config
PUT    /api/v1/chatbots/{chatbot_id}/config
POST   /api/v1/chatbots/{chatbot_id}/test
POST   /api/v1/chatbots/{chatbot_id}/deploy

# Conversaciones
GET    /api/v1/chatbots/{chatbot_id}/conversations
GET    /api/v1/conversations/{conversation_id}
POST   /api/v1/conversations/{conversation_id}/messages
```

### **Knowledge Base**
```http
# Documentos
GET    /api/v1/knowledge-base/documents
POST   /api/v1/knowledge-base/documents/upload
GET    /api/v1/knowledge-base/documents/{doc_id}
PUT    /api/v1/knowledge-base/documents/{doc_id}
DELETE /api/v1/knowledge-base/documents/{doc_id}

# Búsqueda
POST   /api/v1/knowledge-base/search
POST   /api/v1/knowledge-base/semantic-search

# Configuración RAG
GET    /api/v1/knowledge-base/config
PUT    /api/v1/knowledge-base/config
POST   /api/v1/knowledge-base/reindex
```

### **Analytics & Reporting**
```http
# Métricas generales
GET    /api/v1/analytics/overview
GET    /api/v1/analytics/conversations
GET    /api/v1/analytics/performance
GET    /api/v1/analytics/user-satisfaction

# Reportes
GET    /api/v1/reports/daily
GET    /api/v1/reports/weekly
GET    /api/v1/reports/monthly
POST   /api/v1/reports/custom
```

### **Widget & Integration**
```http
# Widget
GET    /api/v1/widget/{chatbot_id}/config
POST   /api/v1/widget/{chatbot_id}/chat
GET    /api/v1/widget/{chatbot_id}/status

# Webhooks
GET    /api/v1/webhooks
POST   /api/v1/webhooks
PUT    /api/v1/webhooks/{webhook_id}
DELETE /api/v1/webhooks/{webhook_id}
POST   /api/v1/webhooks/{webhook_id}/test
```

## 🗄️ **4. Esquema de Base de Datos**

### **Tablas Principales**
```sql
-- Usuarios y Autenticación
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(32),
    last_login TIMESTAMP,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Organizaciones
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    website VARCHAR(500),
    industry VARCHAR(50),
    company_size VARCHAR(20),
    country VARCHAR(2),
    timezone VARCHAR(50) DEFAULT 'UTC',
    subscription_plan VARCHAR(20) DEFAULT 'free',
    owner_id INTEGER REFERENCES users(id),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Miembros de organización
CREATE TABLE organization_members (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- owner, admin, member, viewer
    permissions JSONB DEFAULT '{}',
    invited_by INTEGER REFERENCES users(id),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, user_id)
);

-- Chatbots
CREATE TABLE chatbots (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    slug VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft', -- draft, active, inactive, archived
    ai_model VARCHAR(50) DEFAULT 'llama3-8b-8192',
    system_prompt TEXT,
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    personality VARCHAR(50) DEFAULT 'professional',
    language VARCHAR(5) DEFAULT 'es',
    use_case VARCHAR(50),
    config JSONB DEFAULT '{}',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, slug)
);

-- Conversaciones
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    chatbot_id INTEGER REFERENCES chatbots(id) ON DELETE CASCADE,
    session_id VARCHAR(100) NOT NULL,
    user_identifier VARCHAR(255), -- IP, user_id, email, etc.
    user_metadata JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'active', -- active, ended, escalated
    satisfaction_rating INTEGER CHECK (satisfaction_rating >= 1 AND satisfaction_rating <= 5),
    feedback TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mensajes
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}', -- tokens_used, response_time, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Base de Conocimiento - Documentos
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_type VARCHAR(50),
    file_size INTEGER,
    file_url VARCHAR(500),
    content_text TEXT,
    metadata JSONB DEFAULT '{}',
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    uploaded_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chunks de documentos para RAG
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(384), -- Para all-MiniLM-L6-v2
    chunk_index INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhooks
CREATE TABLE webhooks (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    events TEXT[] NOT NULL, -- ['message_received', 'conversation_ended']
    secret VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics - Métricas diarias
CREATE TABLE daily_metrics (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) ON DELETE CASCADE,
    chatbot_id INTEGER REFERENCES chatbots(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_conversations INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    avg_response_time DECIMAL(8,3),
    avg_satisfaction DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, chatbot_id, date)
);
```

### **Índices para Performance**
```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_chatbots_org_status ON chatbots(organization_id, status);
CREATE INDEX idx_conversations_chatbot_status ON conversations(chatbot_id, status);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
CREATE INDEX idx_documents_org_status ON documents(organization_id, processing_status);

-- Índice para búsqueda vectorial (requiere extensión pgvector)
CREATE INDEX idx_document_chunks_embedding ON document_chunks 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Índices para analytics
CREATE INDEX idx_daily_metrics_org_date ON daily_metrics(organization_id, date);
CREATE INDEX idx_conversations_started_at ON conversations(started_at);
```

## ⚙️ **5. Configuración de Entorno**

### **Variables de Entorno (.env)**
```bash
# === APLICACIÓN ===
APP_NAME=VersaAI Platform
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:3000
API_URL=http://localhost:8000

# === BASE DE DATOS ===
DATABASE_URL=postgresql://versaai:password@localhost:5432/versaai_db
REDIS_URL=redis://localhost:6379/0

# === DJANGO SETTINGS ===
SECRET_KEY=your-super-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# === JWT CONFIGURATION ===
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=24  # hours
JWT_REFRESH_TOKEN_LIFETIME=168  # hours (7 days)

# === AI PROVIDERS ===
# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ORG_ID=org-your-organization-id

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Groq
GROQ_API_KEY=gsk_your-groq-api-key

# Mistral
MISTRAL_API_KEY=your-mistral-api-key

# === VECTOR DATABASES ===
# Pinecone
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-west1-gcp-free

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8001

# === EMAIL CONFIGURATION ===
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=noreply@versaai.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=VersaAI Platform <noreply@versaai.com>

# === STORAGE ===
# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=versaai-storage
AWS_S3_REGION_NAME=us-east-1

# Local storage (development)
MEDIA_ROOT=./media
MEDIA_URL=/media/

# === MONITORING ===
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# === ANALYTICS ===
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# === DEVELOPMENT TOOLS ===
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# === SECURITY ===
SECURE_SSL_REDIRECT=false  # true in production
SESSION_COOKIE_SECURE=false  # true in production
CSRF_COOKIE_SECURE=false  # true in production
```

### **Docker Compose (docker-compose.yml)**
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: versaai_db
      POSTGRES_USER: versaai
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U versaai"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache & Queue
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # Backend Django API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://versaai:password@db:5432/versaai_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - ./backend:/app
      - media_files:/app/media
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"

  # Celery Worker
  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://versaai:password@db:5432/versaai_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - ./backend:/app
      - media_files:/app/media
    depends_on:
      - db
      - redis
    command: celery -A versaai worker -l info

  # Celery Beat (Scheduler)
  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://versaai:password@db:5432/versaai_db
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    command: celery -A versaai beat -l info

  # Frontend React App
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_ENVIRONMENT=development
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    command: npm start

  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_PORT=8000

  # Nginx (Production)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - media_files:/var/www/media
    depends_on:
      - backend
      - frontend
    profiles:
      - production

volumes:
  postgres_data:
  redis_data:
  chroma_data:
  media_files:

networks:
  default:
    name: versaai_network
```

### **Package.json (Frontend)**
```json
  {
    "name": "versaai-frontend",
    "version": "1.0.0",
    "private": true,
    "dependencies": {
      "@emotion/react": "^11.11.1",
      "@emotion/styled": "^11.11.0",
      "@mui/icons-material": "^5.14.19",
      "@mui/material": "^5.14.20",
      "@mui/x-charts": "^6.18.1",
      "@mui/x-data-grid": "^6.18.1",
      "@mui/x-date-pickers": "^6.18.1",
      "@reduxjs/toolkit": "^1.9.7",
      "@types/node": "^20.10.0",
      "@types/react": "^18.2.38",
      "@types/react-dom": "^18.2.17",
      "axios": "^1.6.2",
      "dayjs": "^1.11.10",
      "formik": "^2.4.5",
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "react-redux": "^8.1.3",
      "react-router-dom": "^6.20.0",
      "react-scripts": "5.0.1",
      "recharts": "^2.8.0",
      "typescript": "^5.3.2",
      "yup": "^1.3.3"
    },
    "devDependencies": {
      "@testing-library/jest-dom": "^6.1.5",
      "@testing-library/react": "^13.4.0",
      "@testing-library/user-event": "^14.5.1",
      "@types/jest": "^29.5.8",
      "cypress": "^13.6.0",
      "eslint": "^8.54.0",
      "eslint-config-prettier": "^9.0.0",
      "eslint-plugin-react": "^7.33.2",
      "prettier": "^3.1.0"
    },
    "scripts": {
      "start": "react-scripts start",
      "build": "react-scripts build",
      "test": "react-scripts test",
      "eject": "react-scripts eject",
      "cypress:open": "cypress open",
      "cypress:run": "cypress run",
      "lint": "eslint src --ext .ts,.tsx",
      "lint:fix": "eslint src --ext .ts,.tsx --fix",
      "format": "prettier --write src/**/*.{ts,tsx,css,scss,json}"
    },
    "eslintConfig": {
      "extends": [
        "react-app",
        "react-app/jest",
        "prettier"
      ]
    },
    "browserslist": {
      "production": [
        ">0.2%",
        "not dead",
        "not op_mini all"
      ],
      "development": [
        "last 1 chrome version",
        "last 1 firefox version",
        "last 1 safari version"
      ]
    },
    "proxy": "http://localhost:8000"
  }
  ```

  ### **Requirements.txt (Backend)**
  ```txt
  # Django Core
  Django==4.2.7
  djangorestframework==3.14.0
  django-cors-headers==4.3.1
  django-filter==23.4
  django-extensions==3.2.3
  
  # Authentication & Security
  djangorestframework-simplejwt==5.3.0
  django-allauth==0.57.0
  cryptography==41.0.7
  pyotp==2.9.0
  qrcode[pil]==7.4.2
  
  # Database
  psycopg2-binary==2.9.9
  redis==5.0.1
  
  # AI & ML
  openai==1.3.7
  anthropic==0.7.7
  groq==0.4.1
  sentence-transformers==2.2.2
  chromadb==0.4.18
  pinecone-client==2.2.4
  
  # Document Processing
  pypdf2==3.0.1
  python-docx==1.1.0
  python-magic==0.4.27
  pillow==10.1.0
  
  # Task Queue
  celery==5.3.4
  django-celery-beat==2.5.0
  django-celery-results==2.5.0
  
  # Storage & Files
  boto3==1.34.0
  django-storages==1.14.2
  
  # Monitoring & Logging
  sentry-sdk==1.38.0
  django-debug-toolbar==4.2.0
  
  # API Documentation
  drf-spectacular==0.26.5
  
  # Development
  python-decouple==3.8
  factory-boy==3.3.0
  faker==20.1.0
  
  # Testing
  pytest==7.4.3
  pytest-django==4.7.0
  pytest-cov==4.1.0
  
  # Utilities
  requests==2.31.0
  python-dateutil==2.8.2
  pytz==2023.3
  ```

  ### **Dockerfile (Backend)**
  ```dockerfile
  FROM python:3.11-slim

  # Set environment variables
  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1
  ENV DEBIAN_FRONTEND=noninteractive

  # Install system dependencies
  RUN apt-get update \
      && apt-get install -y --no-install-recommends \
          postgresql-client \
          build-essential \
          libpq-dev \
          libmagic1 \
          curl \
          git \
      && rm -rf /var/lib/apt/lists/*

  # Set work directory
  WORKDIR /app

  # Install Python dependencies
  COPY requirements.txt /app/
  RUN pip install --no-cache-dir -r requirements.txt

  # Copy project
  COPY . /app/

  # Create media directory
  RUN mkdir -p /app/media

  # Collect static files
  RUN python manage.py collectstatic --noinput

  # Expose port
  EXPOSE 8000

  # Run the application
  CMD ["gunicorn", "--bind", "0.0.0.0:8000", "versaai.wsgi:application"]
  ```

  ### **Dockerfile (Frontend)**
  ```dockerfile
  FROM node:18-alpine

  # Set working directory
  WORKDIR /app

  # Copy package files
  COPY package*.json ./

  # Install dependencies
  RUN npm ci --only=production

  # Copy source code
  COPY . .

  # Build the app
  RUN npm run build

  # Expose port
  EXPOSE 3000

  # Start the application
  CMD ["npm", "start"]
  ```

  ### **Configuración de Desarrollo (settings/development.py)**
  ```python
  from .base import *
  import os

  # Debug mode
  DEBUG = True

  # Database
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': os.getenv('DB_NAME', 'versaai_db'),
          'USER': os.getenv('DB_USER', 'versaai'),
          'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
          'HOST': os.getenv('DB_HOST', 'localhost'),
          'PORT': os.getenv('DB_PORT', '5432'),
      }
  }

  # Redis configuration
  REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

  # Celery configuration
  CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
  CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')

  # Email backend for development
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

  # Static files
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

  # Media files
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

  # CORS settings for development
  CORS_ALLOW_ALL_ORIGINS = True
  CORS_ALLOW_CREDENTIALS = True

  # Debug toolbar
  if DEBUG:
      INSTALLED_APPS += ['debug_toolbar']
      MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
      INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']

  # Logging configuration
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
          'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'verbose',
          },
      },
      'root': {
          'handlers': ['console'],
          'level': 'INFO',
      },
      'loggers': {
          'django': {
              'handlers': ['console'],
              'level': 'INFO',
              'propagate': False,
          },
          'versaai': {
              'handlers': ['console'],
              'level': 'DEBUG',
              'propagate': False,
          },
      },
  }
  ```

  ### **Makefile para Desarrollo**
  ```makefile
  # VersaAI Platform - Development Commands

  .PHONY: help install setup dev test clean build deploy

  # Default target
  help:
  	@echo "VersaAI Platform - Available Commands:"
  	@echo "  install     - Install all dependencies"
  	@echo "  setup       - Initial project setup"
  	@echo "  dev         - Start development environment"
  	@echo "  test        - Run all tests"
  	@echo "  clean       - Clean build artifacts"
  	@echo "  build       - Build for production"
  	@echo "  deploy      - Deploy to production"

  # Install dependencies
  install:
  	@echo "Installing backend dependencies..."
  	cd backend && pip install -r requirements.txt
  	@echo "Installing frontend dependencies..."
  	cd frontend && npm install

  # Initial setup
  setup: install
  	@echo "Setting up database..."
  	docker-compose up -d db redis
  	sleep 5
  	cd backend && python manage.py migrate
  	cd backend && python manage.py createsuperuser --noinput || true
  	@echo "Loading initial data..."
  	cd backend && python manage.py loaddata fixtures/initial_data.json
  	@echo "Setup complete!"

  # Start development environment
  dev:
  	@echo "Starting development environment..."
  	docker-compose up --build

  # Run tests
  test:
  	@echo "Running backend tests..."
  	cd backend && python manage.py test
  	@echo "Running frontend tests..."
  	cd frontend && npm test -- --coverage --watchAll=false
  	@echo "Running E2E tests..."
  	cd frontend && npm run cypress:run

  # Clean build artifacts
  clean:
  	@echo "Cleaning build artifacts..."
  	cd frontend && rm -rf build node_modules/.cache
  	cd backend && find . -name "*.pyc" -delete
  	cd backend && find . -name "__pycache__" -delete
  	docker system prune -f

  # Build for production
  build:
  	@echo "Building frontend..."
  	cd frontend && npm run build
  	@echo "Collecting static files..."
  	cd backend && python manage.py collectstatic --noinput
  	@echo "Building Docker images..."
  	docker-compose -f docker-compose.prod.yml build

  # Deploy to production
  deploy: build
  	@echo "Deploying to production..."
  	docker-compose -f docker-compose.prod.yml up -d
  	@echo "Running migrations..."
  	docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
  	@echo "Deployment complete!"

  # Database operations
  migrate:
  	cd backend && python manage.py makemigrations
  	cd backend && python manage.py migrate

  shell:
  	cd backend && python manage.py shell

  # Monitoring
  logs:
  	docker-compose logs -f

  status:
  	docker-compose ps
  ```

  ### **Scripts de Inicialización**
  ```bash
  #!/bin/bash
  # init-dev.sh - Script de inicialización para desarrollo

  echo "🚀 Inicializando VersaAI Platform - Entorno de Desarrollo"

  # Verificar dependencias
  command -v docker >/dev/null 2>&1 || { echo "❌ Docker no está instalado"; exit 1; }
  command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose no está instalado"; exit 1; }
  command -v node >/dev/null 2>&1 || { echo "❌ Node.js no está instalado"; exit 1; }
  command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 no está instalado"; exit 1; }

  # Crear directorios necesarios
  mkdir -p backend/media
  mkdir -p backend/staticfiles
  mkdir -p frontend/build
  mkdir -p logs

  # Copiar archivos de configuración
  if [ ! -f .env ]; then
      cp .env.example .env
      echo "📝 Archivo .env creado. Por favor, configura las variables necesarias."
  fi

  # Inicializar base de datos
  echo "🗄️ Inicializando base de datos..."
  docker-compose up -d db redis chromadb
  sleep 10

  # Instalar dependencias del backend
  echo "🐍 Instalando dependencias de Python..."
  cd backend
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  # Ejecutar migraciones
  echo "🔄 Ejecutando migraciones..."
  python manage.py migrate

  # Crear superusuario
  echo "👤 Creando superusuario..."
  python manage.py createsuperuser --noinput || echo "Superusuario ya existe"

  # Cargar datos iniciales
  echo "📊 Cargando datos iniciales..."
  python manage.py loaddata fixtures/initial_data.json || echo "Datos ya cargados"

  cd ..

  # Instalar dependencias del frontend
  echo "⚛️ Instalando dependencias de Node.js..."
  cd frontend
  npm install
  cd ..

  echo "✅ Inicialización completa!"
  echo ""
  echo "Para iniciar el entorno de desarrollo:"
  echo "  make dev"
  echo ""
  echo "Para acceder a los servicios:"
  echo "  Frontend: http://localhost:3000"
  echo "  Backend API: http://localhost:8000"
  echo "  Admin Panel: http://localhost:8000/admin"
  echo "  ChromaDB: http://localhost:8001"
  ```

  ## 🎯 **Resumen para TRAE**

  ### **Información Clave a Compartir:**

  1. **Stack Completo**: React + TypeScript + Django + PostgreSQL + Redis + ChromaDB
  2. **Arquitectura**: Microservicios con API REST y sistema RAG
  3. **Funcionalidades**: Dashboard completo, editor visual, analytics, widget embebible
  4. **Configuración**: Docker Compose para desarrollo, variables de entorno definidas
  5. **Base de Datos**: Esquema completo con relaciones y índices optimizados

  ### **Preguntas Específicas para TRAE:**

  ```
  1. ¿Cómo estructurarías el proyecto con estos requisitos?
  2. ¿Qué configuración de Webpack/Vite recomiendas para el frontend?
  3. ¿Cómo implementarías el hot-reload entre servicios?
  4. ¿Qué patrones de arquitectura sugieres para el dashboard?
  5. ¿Cómo optimizarías la configuración Docker para desarrollo?
  ```

  ### **Archivos Prioritarios a Generar con TRAE:**

  - [ ] Estructura de carpetas completa
  - [ ] Configuración de TypeScript y ESLint
  - [ ] Componentes base del dashboard
  - [ ] Configuración de Redux Toolkit
  - [ ] Setup de Django con DRF
  - [ ] Configuración de Celery y Redis
  - [ ] Scripts de desarrollo automatizados

  ---

  **🚀 ¡Listo para compartir con TRAE!**

  Estos documentos proporcionan toda la información técnica necesaria para que TRAE pueda generar una arquitectura optimizada y configuración completa del proyecto.
````

¡Perfecto! 🎯 Ya tienes todos los **documentos de preparación** listos para compartir con **TRAE**. 

## 📋 **Checklist de Documentos Completados:**

✅ **Especificaciones Técnicas** - Stack completo y arquitectura  
✅ **Wireframes del Dashboard** - Layouts ASCII detallados  
✅ **API Endpoints** - Todos los endpoints definidos  
✅ **Esquema de Base de Datos** - Tablas, relaciones e índices  
✅ **Configuración de Entorno** - Docker, variables, scripts  

## 🚀 **Próximos Pasos Recomendados:**

### **1. Consulta Inicial con TRAE**
Comparte este documento completo y pregúntale:

```
"Basándome en estas especificaciones técnicas completas de VersaAI Platform, 
¿puedes ayudarme a generar la estructura de proyecto optimizada, 
configuración de desarrollo y los componentes base del dashboard?"
```

### **2. Solicitudes Específicas**
Después de su respuesta inicial, pide:

- **Estructura de carpetas** detallada
- **Configuración de TypeScript** y herramientas
- **Componentes React** base del dashboard
- **Setup de Django** con las APIs definidas
- **Scripts de automatización** para desarrollo

### **3. Iteración y Refinamiento**
Una vez que TRAE genere el código base:

- **Revisa la arquitectura** propuesta
- **Solicita ajustes** específicos si es necesario  
- **Pide optimizaciones** de rendimiento
- **Configura testing** y CI/CD

## 💡 **Ventajas de esta Preparación:**

🎯 **Contexto Completo** - TRAE tendrá toda la información necesaria  
⚡ **Respuestas Precisas** - Generará código específico para tus necesidades  
🔧 **Configuración Optimizada** - Aprovechará las mejores prácticas  
📈 **Escalabilidad** - La arquitectura estará preparada para crecer  

¿Estás listo para hacer la consulta con TRAE? ¿Necesitas que ajuste algún aspecto de la documentación antes de compartirla?