# 🛠️ Acceso Interno para Desarrollo y Pruebas - VersaAI

## 📋 Descripción General

Este documento describe el entorno de desarrollo interno de VersaAI, que incluye portales web especializados para facilitar el desarrollo, testing y configuración de la plataforma.

## 🌐 Portales de Desarrollo

### 1. Portal Principal (`raiz.html`)
**URL:** `file:///C:/Users/Neizan/Desktop/version max claude/versaai/raiz.html`

- **Función:** Centro de control principal del entorno de desarrollo
- **Características:**
  - Dashboard unificado de todos los servicios
  - Enlaces rápidos a frontend y backend
  - Monitoreo de estado de servicios
  - Herramientas de configuración del sistema
  - Logs centralizados

### 2. Panel Frontend (`frontend/frontend.html`)
**URL:** `file:///C:/Users/Neizan/Desktop/version max claude/versaai/frontend/frontend.html`

- **Función:** Gestión específica del desarrollo frontend
- **Características:**
  - Control del servidor de desarrollo Vue.js
  - Gestión de dependencias npm
  - Build y despliegue
  - Testing y linting
  - Métricas del proyecto
  - Gestión de componentes Vue

### 3. Panel Backend (`backend/backend.html`)
**URL:** `file:///C:/Users/Neizan/Desktop/version max claude/versaai/backend/backend.html`

- **Función:** Gestión específica del desarrollo backend
- **Características:**
  - Control del servidor FastAPI
  - Gestión de base de datos PostgreSQL
  - Monitoreo de Redis
  - Testing con Pytest
  - Gestión de dependencias Python
  - Endpoints de la API
  - Métricas y logs del backend

## 🚀 Configuración Inicial

### Requisitos Previos

1. **Node.js** (v18 o superior)
2. **Python** (v3.11 o superior)
3. **PostgreSQL** (v14 o superior)
4. **Redis** (v6 o superior)
5. **Git**

### Instalación del Entorno

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd versaai

# 2. Configurar Backend
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar Frontend
cd ../frontend
npm install

# 4. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con las configuraciones necesarias
```

### Configuración de Base de Datos

```bash
# Crear base de datos
psql -U postgres
CREATE DATABASE versaai;
CREATE USER versaai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE versaai TO versaai_user;

# Ejecutar migraciones
cd backend
alembic upgrade head
```

## 🔧 Uso de los Portales

### Flujo de Trabajo Recomendado

1. **Inicio del Día:**
   - Abrir `raiz.html` en el navegador
   - Verificar estado de todos los servicios
   - Iniciar servicios necesarios

2. **Desarrollo Frontend:**
   - Acceder a `frontend/frontend.html`
   - Iniciar servidor de desarrollo
   - Monitorear builds y tests

3. **Desarrollo Backend:**
   - Acceder a `backend/backend.html`
   - Verificar conexiones de DB y Redis
   - Probar endpoints de la API
   - Ejecutar tests

### Comandos Principales

#### Frontend
```bash
# Desarrollo
npm run dev

# Build de producción
npm run build

# Testing
npm run test
npm run test:coverage

# Linting
npm run lint
npm run lint:fix
```

#### Backend
```bash
# Desarrollo
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest tests/ -v
pytest --cov=src tests/

# Linting
flake8 src/
black src/

# Migraciones
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 📊 Monitoreo y Métricas

### URLs de Servicios

- **Frontend Dev Server:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

### Métricas Disponibles

#### Frontend
- Tiempo de build
- Tamaño del bundle
- Cobertura de tests
- Errores de linting
- Dependencias desactualizadas

#### Backend
- Tiempo de respuesta de la API
- Número de requests
- Tasa de errores
- Cobertura de tests
- Estado de la base de datos
- Uso de memoria de Redis

## 🧪 Testing

### Frontend Testing
```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

### Backend Testing
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_auth.py

# Con cobertura
pytest --cov=src tests/

# Tests de integración
pytest tests/integration/
```

## 🔒 Seguridad

### Variables de Entorno Críticas

```env
# Backend (.env)
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/versaai
REDIS_URL=redis://localhost:6379
GROQ_API_KEY=your-groq-api-key
JWT_SECRET_KEY=your-jwt-secret
```

### Buenas Prácticas

1. **Nunca commitear archivos .env**
2. **Usar claves diferentes para desarrollo y producción**
3. **Rotar claves regularmente**
4. **Verificar vulnerabilidades con `safety check`**
5. **Mantener dependencias actualizadas**

## 🚨 Troubleshooting

### Problemas Comunes

#### Frontend
- **Error de puerto ocupado:** Cambiar puerto en `vite.config.js`
- **Dependencias desactualizadas:** Ejecutar `npm update`
- **Build fallando:** Verificar errores de TypeScript

#### Backend
- **Error de conexión DB:** Verificar PostgreSQL activo
- **Error de Redis:** Verificar Redis activo
- **Import errors:** Verificar PYTHONPATH

#### Base de Datos
- **Migraciones fallando:** Verificar esquema actual
- **Conexión rechazada:** Verificar credenciales
- **Datos corruptos:** Restaurar desde backup

### Logs de Depuración

```bash
# Frontend
npm run dev -- --debug

# Backend
uvicorn src.main:app --reload --log-level debug

# Base de datos
psql -U versaai_user -d versaai -c "SELECT * FROM pg_stat_activity;"
```

## 📚 Recursos Adicionales

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue.js 3 Guide](https://vuejs.org/guide/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Redis Docs](https://redis.io/documentation)

### Herramientas de Desarrollo
- **VS Code Extensions:** Vue Language Features, Python, PostgreSQL
- **Browser Extensions:** Vue DevTools, React DevTools
- **Database Tools:** pgAdmin, DBeaver
- **API Testing:** Postman, Insomnia

## 🔄 Actualizaciones

### Versionado
- **Frontend:** Seguir semantic versioning
- **Backend:** Usar Alembic para migraciones
- **Base de datos:** Backup antes de cambios mayores

### Proceso de Deploy
1. Ejecutar todos los tests
2. Verificar linting
3. Build de producción
4. Backup de base de datos
5. Deploy escalonado
6. Verificar métricas post-deploy

---

**Última actualización:** $(date)
**Versión del documento:** 1.0
**Mantenido por:** Equipo de Desarrollo VersaAI