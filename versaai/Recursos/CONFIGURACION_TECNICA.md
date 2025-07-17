# ⚙️ Configuración Técnica VersaAI
## Guía Completa de Setup y Configuración

---

## 🚀 Setup Inicial Rápido

### 1. Verificación del Entorno

```bash
# Verificar versiones
python --version  # Debe ser 3.9+
node --version    # Debe ser 18+
npm --version     # Debe ser 8+
git --version     # Cualquier versión reciente
```

### 2. Configuración de Variables de Entorno

#### Backend (.env)
```env
# Base de Datos
DATABASE_URL=postgresql://versaai_user:versaai_pass@localhost:5432/versaai_db
DATABASE_URL_DEV=sqlite:///./versaai.db

# Seguridad
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# IA y APIs
GROQ_API_KEY=tu-groq-api-key-aqui
GROQ_MODEL=llama3-8b-8192

# Redis (Opcional)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=

# Configuración de Aplicación
APP_NAME=VersaAI
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]

# Uploads
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=["pdf", "txt", "docx", "md"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/versaai.log
```

#### Frontend (.env)
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=10000

# App Configuration
VITE_APP_NAME=VersaAI
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION="Plataforma de Chatbots Empresariales"

# Features
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=true
VITE_ENABLE_PWA=false

# UI Configuration
VITE_DEFAULT_THEME=light
VITE_DEFAULT_LANGUAGE=es

# External Services
VITE_SENTRY_DSN=
VITE_GOOGLE_ANALYTICS_ID=
```

---

## 🗄️ Configuración de Base de Datos

### PostgreSQL Setup

#### 1. Instalación (Windows)
```bash
# Descargar desde: https://www.postgresql.org/download/windows/
# O usar chocolatey:
choco install postgresql

# Verificar instalación
psql --version
```

#### 2. Configuración Inicial
```sql
-- Conectar como superusuario
psql -U postgres

-- Crear usuario
CREATE USER versaai_user WITH PASSWORD 'versaai_pass';

-- Crear base de datos
CREATE DATABASE versaai_db OWNER versaai_user;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE versaai_db TO versaai_user;

-- Verificar conexión
\c versaai_db versaai_user
\dt  -- Listar tablas (debe estar vacío inicialmente)
```

#### 3. Configuración de Alembic
```bash
cd backend

# Inicializar Alembic (ya hecho)
# alembic init alembic

# Crear migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head

# Verificar tablas creadas
psql -U versaai_user -d versaai_db -c "\dt"
```

### SQLite (Desarrollo)
```bash
# Para desarrollo rápido, usar SQLite
export DATABASE_URL="sqlite:///./versaai.db"
# O en Windows:
set DATABASE_URL=sqlite:///./versaai.db
```

---

## 🔧 Configuración de Dependencias

### Backend Dependencies

#### requirements.txt Completo
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI and ML
groq==0.4.1
langchain==0.1.0
langchain-community==0.0.10
sentence-transformers==2.2.2

# Document Processing
PyPDF2==3.0.1
python-docx==1.1.0
markdown==3.5.1

# Utilities
pydantic==2.5.0
python-dotenv==1.0.0
loguru==0.7.2
requests==2.31.0

# Caching
redis==5.0.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Development
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

#### Instalación
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación
pip list | grep fastapi
```

### Frontend Dependencies

#### package.json Completo
```json
{
  "name": "versaai-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix",
    "type-check": "vue-tsc --noEmit"
  },
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "@headlessui/vue": "^1.7.16",
    "@heroicons/vue": "^2.0.18",
    "chart.js": "^4.4.0",
    "vue-chartjs": "^5.2.0",
    "date-fns": "^2.30.0",
    "lodash-es": "^4.17.21"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.6",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "@vue/test-utils": "^2.4.2",
    "vitest": "^0.34.6",
    "@vitest/coverage-v8": "^0.34.6",
    "eslint": "^8.54.0",
    "@vue/eslint-config-prettier": "^8.0.0",
    "prettier": "^3.1.0",
    "typescript": "^5.3.2",
    "vue-tsc": "^1.8.22"
  }
}
```

#### Instalación
```bash
cd frontend

# Instalar dependencias
npm install

# Verificar instalación
npm list vue
npm run dev  # Debe iniciar en http://localhost:5173
```

---

## 🔐 Configuración de Seguridad

### JWT Configuration

#### Generar Secret Key
```python
# Generar clave secreta segura
import secrets
print(secrets.token_urlsafe(32))
# Usar el resultado en SECRET_KEY
```

#### Configuración de CORS
```python
# backend/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://tu-dominio.com"  # Producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting
```python
# Instalar slowapi
pip install slowapi

# Configurar en main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

---

## 📊 Configuración de Logging

### Backend Logging
```python
# backend/src/core/logging.py
from loguru import logger
import sys
from pathlib import Path

# Configurar logger
logger.remove()  # Remover handler por defecto

# Console logging
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# File logging
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

logger.add(
    "logs/versaai.log",
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)
```

### Frontend Logging
```javascript
// frontend/src/utils/logger.js
class Logger {
  constructor() {
    this.isDev = import.meta.env.DEV
  }

  info(message, ...args) {
    if (this.isDev) console.log(`[INFO] ${message}`, ...args)
  }

  error(message, ...args) {
    console.error(`[ERROR] ${message}`, ...args)
  }

  warn(message, ...args) {
    if (this.isDev) console.warn(`[WARN] ${message}`, ...args)
  }
}

export const logger = new Logger()
```

---

## 🧪 Configuración de Testing

### Backend Testing
```python
# backend/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.core.database import get_db, Base

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### Frontend Testing
```javascript
// frontend/vitest.config.js
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js']
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  }
})
```

---

## 🚀 Scripts de Desarrollo

### Backend Scripts
```bash
#!/bin/bash
# scripts/dev-backend.sh

echo "🚀 Iniciando Backend VersaAI..."

cd backend

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Verificar base de datos
echo "📊 Verificando base de datos..."
python -c "from src.core.database import engine; print('✅ Conexión DB exitosa')"

# Ejecutar migraciones
echo "🔄 Aplicando migraciones..."
alembic upgrade head

# Iniciar servidor
echo "🌐 Iniciando servidor FastAPI..."
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Scripts
```bash
#!/bin/bash
# scripts/dev-frontend.sh

echo "🎨 Iniciando Frontend VersaAI..."

cd frontend

# Verificar dependencias
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Verificar backend
echo "🔗 Verificando conexión con backend..."
curl -f http://localhost:8000/api/docs > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend disponible"
else
    echo "⚠️  Backend no disponible - iniciarlo primero"
fi

# Iniciar desarrollo
echo "🌐 Iniciando servidor de desarrollo..."
npm run dev
```

### Script Completo
```bash
#!/bin/bash
# scripts/dev-full.sh

echo "🚀 Iniciando VersaAI Completo..."

# Terminal 1: Backend
gnome-terminal --tab --title="Backend" -- bash -c "./scripts/dev-backend.sh; exec bash"

# Esperar un poco
sleep 3

# Terminal 2: Frontend
gnome-terminal --tab --title="Frontend" -- bash -c "./scripts/dev-frontend.sh; exec bash"

echo "✅ VersaAI iniciado en modo desarrollo"
echo "📚 Documentación: http://localhost:8000/api/docs"
echo "🎨 Frontend: http://localhost:5173"
```

---

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión a PostgreSQL
```bash
# Verificar servicio
sudo systemctl status postgresql  # Linux
# O en Windows: services.msc -> PostgreSQL

# Reiniciar servicio
sudo systemctl restart postgresql

# Verificar puerto
netstat -an | grep 5432
```

#### 2. Error de Dependencias Python
```bash
# Limpiar caché pip
pip cache purge

# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Verificar conflictos
pip check
```

#### 3. Error de Node Modules
```bash
# Limpiar caché npm
npm cache clean --force

# Eliminar node_modules
rm -rf node_modules package-lock.json

# Reinstalar
npm install
```

#### 4. Error de CORS
```python
# Verificar configuración en main.py
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
```

### Logs de Debug
```bash
# Backend logs
tail -f backend/logs/versaai.log

# Frontend logs (browser console)
# Abrir DevTools -> Console

# Sistema logs
journalctl -f  # Linux
# Event Viewer # Windows
```

---

## 📋 Checklist de Configuración

### ✅ Verificación Completa

- [ ] **Python 3.9+** instalado y funcionando
- [ ] **Node.js 18+** instalado y funcionando
- [ ] **PostgreSQL** instalado y configurado
- [ ] **Git** configurado con usuario
- [ ] **Variables de entorno** configuradas
- [ ] **Dependencias backend** instaladas
- [ ] **Dependencias frontend** instaladas
- [ ] **Base de datos** creada y migrada
- [ ] **Servidor backend** iniciando correctamente
- [ ] **Servidor frontend** iniciando correctamente
- [ ] **CORS** configurado correctamente
- [ ] **Logging** funcionando
- [ ] **Tests** ejecutándose

### 🔧 Comandos de Verificación
```bash
# Verificación completa
echo "🔍 Verificando configuración VersaAI..."

# Backend
cd backend && python -c "import src.main; print('✅ Backend OK')"

# Frontend
cd frontend && npm run build && echo "✅ Frontend OK"

# Base de datos
psql -U versaai_user -d versaai_db -c "SELECT 1;" && echo "✅ Database OK"

echo "🎉 Configuración completa!"
```

---

**Última Actualización:** $(date)  
**Versión:** 1.0  
**Mantenido por:** Equipo VersaAI