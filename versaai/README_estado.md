# 📊 VersaAI - Estado del Proyecto y Plan de Desarrollo

[![Estado del Proyecto](https://img.shields.io/badge/Estado-Fase%201%20Fundación-blue)](https://github.com/versaai/versaai)
[![Progreso](https://img.shields.io/badge/Progreso-30%25%20Completado-orange)](https://github.com/versaai/versaai)
[![Próximo Hito](https://img.shields.io/badge/Próximo%20Hito-PostgreSQL%20Setup-red)](https://github.com/versaai/versaai)

## 📋 Resumen Ejecutivo

**VersaAI** está en desarrollo activo con un progreso del **30% completado**. La infraestructura base está sólida y el proyecto está listo para acelerar el desarrollo en las próximas 12 semanas.

### 🎯 Estado Actual
- **Fase Actual:** Fase 1 - Fundación (Completándose)
- **Progreso General:** 45% Completado, 25% En Progreso, 30% Pendiente
- **Logros Recientes:** PostgreSQL configurado, autenticación básica implementada ✅
- **Timeline:** 12 semanas estructuradas en 4 fases
- **Metodología:** Desarrollo ágil con sprints semanales

### 🚨 Bloqueadores Críticos
1. **PostgreSQL no configurado** - Bloquea todo el backend
2. **Autenticación incompleta** - Sin usuarios funcionales
3. **Frontend-Backend desconectados** - Sin integración real

---

## 📅 Plan de Desarrollo de 12 Semanas

### 🏗️ **FASE 1: FUNDACIÓN** (Semanas 1-3)
**Objetivo:** Establecer base sólida y funcional

#### 📊 Progreso de Fase 1: 65% Completado
```
██████████████████████████████████████████████████████████████████░░░░░░░░░░ 65%
```

#### ✅ **SEMANA 1: Configuración Base y PostgreSQL**
**Estado:** 🔥 **CRÍTICO - EN PROGRESO**

##### Día 1: PostgreSQL Setup (CRÍTICO) ✅
- [x] **Configurar PostgreSQL 15** ✅
  - [x] Instalar PostgreSQL localmente o usar Docker
  - [x] Crear base de datos `versaai`
  - [x] Crear usuario `versaai_user` con permisos
  - [x] Configurar variables de entorno en `.env`
  - [x] Verificar conexión desde backend
- [x] **Ejecutar migraciones** ✅
  - [x] `alembic upgrade head`
  - [x] Verificar tablas creadas correctamente
  - [x] Poblar datos de prueba básicos

**🎯 Criterio de Aceptación:** Backend API responde en http://localhost:8000/docs

##### Días 2-3: Autenticación Backend ✅
- [x] **Endpoints de Autenticación** ✅
  - [x] `POST /api/v1/auth/register` - Registro de usuarios
  - [x] `POST /api/v1/auth/login` - Login con JWT
  - [x] `POST /api/v1/auth/refresh` - Refresh token
  - [x] `GET /api/v1/auth/me` - Perfil de usuario
  - [x] `POST /api/v1/auth/logout` - Logout
- [x] **Middleware de Seguridad** ✅
  - [x] Validación JWT en rutas protegidas
  - [x] Rate limiting básico
  - [x] CORS configurado correctamente
- [x] **Testing Backend** ✅
  - [x] Tests unitarios para auth endpoints
  - [x] Tests de validación de tokens
  - [x] Coverage >70% en módulo auth

**🎯 Criterio de Aceptación:** Registro y login funcional vía API ✅

##### Días 4-5: Integración Frontend-Backend ✅
- [x] **Conexión API** ✅
  - [x] Configurar proxy de Vite correctamente
  - [x] Implementar interceptors de Axios
  - [x] Conectar stores de Pinia con endpoints
  - [x] Manejo de errores HTTP
- [x] **Autenticación Frontend** ✅
  - [x] Conectar formularios de login/registro
  - [x] Implementar guards de Vue Router
  - [x] Persistencia de sesión con cookies
  - [x] Loading states y UX optimizada
- [x] **Testing Integración** ✅
  - [x] Tests E2E básicos con Cypress
  - [x] Tests de flujo de autenticación
  - [x] Verificación de protección de rutas

**🎯 Criterio de Aceptación:** Login completo frontend-backend funcional ✅

##### Días 6-7: Estabilización
- [ ] **Documentación**
  - [ ] Actualizar README con setup actualizado
  - [ ] Documentar endpoints en Swagger
  - [ ] Guía de desarrollo local
- [ ] **Optimización**
  - [ ] Optimizar queries de base de datos
  - [ ] Configurar logs estructurados
  - [ ] Métricas básicas de performance

**🎯 Entregable Semana 1:** Sistema de autenticación completo y funcional

---

#### ✅ **SEMANA 2: Testing y CI/CD**
**Estado:** 🔄 **EN PROGRESO AVANZADO**

##### Días 8-10: Testing Automatizado 🔄
- [x] **Backend Testing** ✅
  - [x] Configurar pytest con fixtures
  - [x] Tests unitarios para todos los modelos
  - [x] Tests de integración para API
  - [x] Coverage >80% objetivo
  - [x] Tests de performance básicos
- [x] **Frontend Testing** ✅
  - [x] Configurar Vitest para componentes
  - [x] Tests unitarios para stores Pinia
  - [x] Tests de componentes críticos
  - [x] Tests de integración con API mock
- [ ] **Quality Gates** 🔄
  - [x] ESLint y Prettier configurados
  - [x] Pre-commit hooks
  - [ ] Security scanning básico (en progreso)

##### Días 11-14: CI/CD Pipeline 🔄
- [ ] **GitHub Actions** 🔄
  - [x] Workflow de testing automático
  - [ ] Build y deploy de staging (en progreso)
  - [x] Notificaciones de estado
  - [x] Cache de dependencias
- [ ] **Docker Optimization** 🔄
  - [x] Multi-stage builds
  - [ ] Optimización de imágenes (en progreso)
  - [x] Health checks mejorados
  - [ ] Secrets management (en progreso)

**🎯 Entregable Semana 2:** Pipeline CI/CD funcional con testing automático

---

#### ✅ **SEMANA 3: Estabilización y Preparación**
**Estado:** ⏳ **PENDIENTE**

##### Días 15-17: Optimización y Refactoring
- [ ] **Code Quality**
  - [ ] Refactoring de código duplicado
  - [ ] Optimización de performance
  - [ ] Documentación de código
  - [ ] Security audit básico
- [ ] **Database Optimization**
  - [ ] Índices optimizados
  - [ ] Queries eficientes
  - [ ] Connection pooling
  - [ ] Backup strategy

##### Días 18-21: Preparación Fase 2
- [ ] **Planning Fase 2**
  - [ ] Definir user stories para chatbots
  - [ ] Diseño de arquitectura RAG
  - [ ] Preparar entorno de desarrollo
  - [ ] Sprint planning detallado
- [ ] **Documentación**
  - [ ] Actualizar documentación técnica
  - [ ] Guías de contribución
  - [ ] Roadmap actualizado

**🎯 Entregable Semana 3:** Base sólida y estable para desarrollo acelerado

---

### 🤖 **FASE 2: CORE FEATURES** (Semanas 4-6)
**Objetivo:** Implementar funcionalidades principales del producto

#### 📊 Progreso de Fase 2: 0% Completado
```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

#### ✅ **SEMANA 4: Motor de Chatbots**
**Estado:** ⏳ **PENDIENTE**

##### Días 22-24: Backend Chatbots
- [ ] **Modelos y API**
  - [ ] Endpoints CRUD para chatbots
  - [ ] Configuración de personalidad y comportamiento
  - [ ] Gestión de prompts y templates
  - [ ] Validación de configuraciones
- [ ] **Integración Groq AI**
  - [ ] Cliente Groq funcional
  - [ ] Manejo de rate limits
  - [ ] Streaming de respuestas
  - [ ] Error handling robusto
- [ ] **Testing IA**
  - [ ] Tests unitarios para motor IA
  - [ ] Tests de integración con Groq
  - [ ] Mocks para desarrollo offline

##### Días 25-28: Frontend Chatbots
- [ ] **Interface de Creación**
  - [ ] Formulario de configuración de chatbot
  - [ ] Preview en tiempo real
  - [ ] Gestión de prompts
  - [ ] Configuración de personalidad
- [ ] **Dashboard de Chatbots**
  - [ ] Lista de chatbots creados
  - [ ] Métricas básicas por chatbot
  - [ ] Acciones rápidas (editar, duplicar, eliminar)
  - [ ] Búsqueda y filtros

**🎯 Entregable Semana 4:** Motor de chatbots básico funcional

---

#### ✅ **SEMANA 5: Sistema de Conversaciones**
**Estado:** ⏳ **PENDIENTE**

##### Días 29-31: Backend Conversaciones
- [ ] **API de Conversaciones**
  - [ ] Endpoints para crear/gestionar conversaciones
  - [ ] Sistema de mensajes en tiempo real
  - [ ] Historial de conversaciones
  - [ ] Búsqueda en conversaciones
- [ ] **WebSocket (Opcional)**
  - [ ] Configurar WebSocket para chat en tiempo real
  - [ ] Manejo de conexiones múltiples
  - [ ] Notificaciones push

##### Días 32-35: Frontend Chat
- [ ] **Interface de Chat**
  - [ ] Componente de chat en tiempo real
  - [ ] Historial de mensajes
  - [ ] Indicadores de typing
  - [ ] Manejo de archivos adjuntos
- [ ] **Gestión de Conversaciones**
  - [ ] Lista de conversaciones
  - [ ] Búsqueda y filtros
  - [ ] Exportación de conversaciones

**🎯 Entregable Semana 5:** Sistema de chat funcional

---

#### ✅ **SEMANA 6: Dashboard Completo**
**Estado:** ⏳ **PENDIENTE**

##### Días 36-38: Analytics Backend
- [ ] **Métricas y Analytics**
  - [ ] Sistema de tracking de eventos
  - [ ] Métricas de uso por chatbot
  - [ ] Analytics de conversaciones
  - [ ] KPIs empresariales
- [ ] **Reportes**
  - [ ] Generación de reportes automáticos
  - [ ] Exportación en múltiples formatos
  - [ ] Programación de reportes

##### Días 39-42: Dashboard Frontend
- [ ] **Dashboard Principal**
  - [ ] Métricas en tiempo real
  - [ ] Gráficos interactivos
  - [ ] Widgets personalizables
  - [ ] Filtros temporales
- [ ] **Gestión de Usuarios**
  - [ ] CRUD de usuarios
  - [ ] Gestión de roles y permisos
  - [ ] Configuraciones de organización

**🎯 Entregable Semana 6:** Dashboard completo con analytics

---

### 📚 **FASE 3: FUNCIONALIDADES AVANZADAS** (Semanas 7-9)
**Objetivo:** Implementar sistema RAG y funcionalidades avanzadas

#### 📊 Progreso de Fase 3: 0% Completado
```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

#### ✅ **SEMANA 7: Sistema RAG - Procesamiento**
**Estado:** ⏳ **PENDIENTE**

##### Días 43-45: Procesamiento de Documentos
- [ ] **Upload y Procesamiento**
  - [ ] Sistema de upload de archivos
  - [ ] Procesamiento de PDF, DOCX, TXT
  - [ ] Extracción de texto y metadatos
  - [ ] Validación y sanitización
- [ ] **Chunking y Preprocessing**
  - [ ] Algoritmos de chunking inteligente
  - [ ] Preprocessing de texto
  - [ ] Detección de idioma
  - [ ] Limpieza de datos

##### Días 46-49: Generación de Embeddings
- [ ] **Vector Database**
  - [ ] Integración con vector database (Pinecone/Weaviate)
  - [ ] Generación de embeddings
  - [ ] Almacenamiento eficiente
  - [ ] Indexación optimizada
- [ ] **Knowledge Base Management**
  - [ ] CRUD de documentos
  - [ ] Versionado de documentos
  - [ ] Organización por categorías
  - [ ] Metadatos enriquecidos

**🎯 Entregable Semana 7:** Sistema de procesamiento de documentos

---

#### ✅ **SEMANA 8: Sistema RAG - Búsqueda**
**Estado:** ⏳ **PENDIENTE**

##### Días 50-52: Motor de Búsqueda
- [ ] **Búsqueda Semántica**
  - [ ] Algoritmos de similarity search
  - [ ] Ranking de resultados
  - [ ] Filtros contextuales
  - [ ] Optimización de performance
- [ ] **Retrieval Augmented Generation**
  - [ ] Integración RAG con chatbots
  - [ ] Context injection
  - [ ] Citación de fuentes
  - [ ] Confidence scoring

##### Días 53-56: Interface RAG
- [ ] **Knowledge Base UI**
  - [ ] Interface de gestión de documentos
  - [ ] Preview de documentos
  - [ ] Búsqueda avanzada
  - [ ] Analytics de uso
- [ ] **Configuración RAG**
  - [ ] Configuración por chatbot
  - [ ] Ajuste de parámetros
  - [ ] Testing de calidad

**🎯 Entregable Semana 8:** Sistema RAG completo y funcional

---

#### ✅ **SEMANA 9: Analytics Avanzados**
**Estado:** ⏳ **PENDIENTE**

##### Días 57-59: Analytics Backend
- [ ] **Sistema de Métricas**
  - [ ] Tracking avanzado de eventos
  - [ ] Métricas de satisfacción
  - [ ] Analytics de performance
  - [ ] Detección de anomalías
- [ ] **Reportes Personalizables**
  - [ ] Builder de reportes
  - [ ] Programación automática
  - [ ] Múltiples formatos de export
  - [ ] Dashboards personalizados

##### Días 60-63: Analytics Frontend
- [ ] **Dashboard Avanzado**
  - [ ] Gráficos interactivos avanzados
  - [ ] Filtros dinámicos
  - [ ] Comparativas temporales
  - [ ] Drill-down capabilities
- [ ] **Reportes y Exports**
  - [ ] Generador de reportes visual
  - [ ] Programación de reportes
  - [ ] Compartir dashboards
  - [ ] Alertas automáticas

**🎯 Entregable Semana 9:** Sistema de analytics empresarial completo

---

### 🚀 **FASE 4: OPTIMIZACIÓN Y PRODUCCIÓN** (Semanas 10-12)
**Objetivo:** Preparar para producción y optimizar performance

#### 📊 Progreso de Fase 4: 0% Completado
```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

#### ✅ **SEMANA 10: Widget y API Pública**
**Estado:** ⏳ **PENDIENTE**

##### Días 64-66: Widget Embebible
- [ ] **Widget Development**
  - [ ] Widget JavaScript standalone
  - [ ] Configuración personalizable
  - [ ] Temas y estilos
  - [ ] Responsive design
- [ ] **Integración**
  - [ ] Script de instalación simple
  - [ ] Documentación de integración
  - [ ] Ejemplos de uso
  - [ ] Testing cross-browser

##### Días 67-70: API Pública
- [ ] **API Documentation**
  - [ ] Documentación completa
  - [ ] SDKs en múltiples lenguajes
  - [ ] Rate limiting avanzado
  - [ ] API versioning
- [ ] **Developer Portal**
  - [ ] Portal para desarrolladores
  - [ ] Gestión de API keys
  - [ ] Analytics de uso de API
  - [ ] Soporte y ejemplos

**🎯 Entregable Semana 10:** Widget y API pública listos

---

#### ✅ **SEMANA 11: Optimización Performance**
**Estado:** ⏳ **PENDIENTE**

##### Días 71-73: Backend Optimization
- [ ] **Performance**
  - [ ] Optimización de queries SQL
  - [ ] Caching estratégico (Redis)
  - [ ] Connection pooling
  - [ ] Async optimization
- [ ] **Scalability**
  - [ ] Load balancing
  - [ ] Database sharding prep
  - [ ] Microservices architecture
  - [ ] CDN integration

##### Días 74-77: Frontend Optimization
- [ ] **Performance Frontend**
  - [ ] Code splitting avanzado
  - [ ] Lazy loading optimizado
  - [ ] Bundle optimization
  - [ ] PWA capabilities
- [ ] **Monitoring**
  - [ ] Performance monitoring
  - [ ] Error tracking (Sentry)
  - [ ] User analytics
  - [ ] Real-time alerts

**🎯 Entregable Semana 11:** Sistema optimizado para alta carga

---

#### ✅ **SEMANA 12: Preparación Producción**
**Estado:** ⏳ **PENDIENTE**

##### Días 78-80: Seguridad y Compliance
- [ ] **Security Hardening**
  - [ ] Security audit completo
  - [ ] Penetration testing
  - [ ] Vulnerability scanning
  - [ ] OWASP compliance
- [ ] **Compliance**
  - [ ] GDPR compliance
  - [ ] Data privacy measures
  - [ ] Audit logging
  - [ ] Backup and recovery

##### Días 81-84: Deploy y Launch
- [ ] **Production Deploy**
  - [ ] Infrastructure as Code
  - [ ] Blue-green deployment
  - [ ] Rollback procedures
  - [ ] Health monitoring
- [ ] **Launch Preparation**
  - [ ] Documentation final
  - [ ] User training materials
  - [ ] Support procedures
  - [ ] Marketing materials

**🎯 Entregable Semana 12:** VersaAI listo para producción

---

## 📊 Métricas y KPIs

### 🎯 KPIs por Fase

#### Fase 1: Fundación
- **Coverage de Tests:** >80%
- **Performance API:** <200ms response time
- **Uptime:** >99%
- **Security Score:** A+ (según herramientas de audit)

#### Fase 2: Core Features
- **Chatbots Creados:** >10 chatbots de prueba
- **Conversaciones:** >100 conversaciones de test
- **Response Time IA:** <3 segundos
- **User Satisfaction:** >4.5/5

#### Fase 3: Funcionalidades Avanzadas
- **Documentos Procesados:** >1000 documentos
- **Accuracy RAG:** >85%
- **Search Performance:** <500ms
- **Analytics Coverage:** 100% de eventos

#### Fase 4: Producción
- **Load Capacity:** 1000+ usuarios concurrentes
- **Security Score:** A+ (penetration testing)
- **Performance Score:** >90 (Lighthouse)
- **Documentation Coverage:** 100%

### 📈 Métricas de Progreso

```
Progreso General del Proyecto:
████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 65% Completado
██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 20% En Progreso
███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 15% Pendiente

Desglose por Componente:
🏗️ Infraestructura:     ███████████████████████████████████████████████████████████████████████████████████████████████ 95%
⚡ Backend Core:        ██████████████████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 70%
🖥️ Frontend Base:       ████████████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 65%
🔐 Autenticación:       ██████████████████████████████████████████████████████████████████████████████████████░░░░░░░░░░░░ 90%
🤖 Motor Chatbots:      █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 25%
📚 Sistema RAG:         ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 15%
📊 Analytics:           ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10%
🧪 Testing:             ████████████████████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░ 60%
```

---

## 🚨 Gestión de Riesgos

### 🔥 Riesgos Críticos

#### 1. PostgreSQL Setup Fallido
**Probabilidad:** Media | **Impacto:** Crítico
- **Mitigación:** Documentación detallada + Docker como backup
- **Plan B:** Usar SQLite para desarrollo inicial
- **Responsable:** DevOps/Backend Lead

#### 2. Integración Groq AI Problemática
- **Probabilidad:** Baja | **Impacto:** Alto
- **Mitigación:** API key válida + rate limiting + fallbacks
- **Plan B:** OpenAI API como alternativa
- **Responsable:** IA/Backend Lead

#### 3. Performance Issues en Producción
- **Probabilidad:** Media | **Impacto:** Alto
- **Mitigación:** Testing de carga + monitoring + optimization
- **Plan B:** Scaling horizontal + CDN
- **Responsable:** DevOps/Performance Team

### 🟡 Riesgos Moderados

#### 1. Retrasos en Testing
- **Mitigación:** TDD desde el inicio + CI/CD automático
- **Plan B:** Testing paralelo + recursos adicionales

#### 2. Complejidad RAG Subestimada
- **Mitigación:** POC temprano + investigación previa
- **Plan B:** Simplificar MVP + iteración posterior

#### 3. Scope Creep
- **Mitigación:** Sprints definidos + product owner fuerte
- **Plan B:** Priorización estricta + backlog management

---

## ✅ Criterios de Aceptación por Fase

### Fase 1: Fundación
- [ ] PostgreSQL configurado y migraciones ejecutadas
- [ ] Sistema de autenticación completo (registro, login, JWT)
- [ ] Frontend y backend conectados funcionalmente
- [ ] Tests automatizados con >70% coverage
- [ ] CI/CD pipeline básico funcionando
- [ ] Documentación actualizada

### Fase 2: Core Features
- [ ] Motor de chatbots funcional con Groq AI
- [ ] Sistema de conversaciones en tiempo real
- [ ] Dashboard con métricas básicas
- [ ] CRUD completo de usuarios y organizaciones
- [ ] Performance <3s para respuestas IA
- [ ] Tests E2E para flujos principales

### Fase 3: Funcionalidades Avanzadas
- [ ] Sistema RAG completo (upload, processing, search)
- [ ] Base de conocimiento funcional
- [ ] Analytics avanzados con reportes
- [ ] Búsqueda semántica operativa
- [ ] Citación de fuentes en respuestas
- [ ] Performance <500ms para búsquedas

### Fase 4: Producción
- [ ] Widget embebible funcional
- [ ] API pública documentada
- [ ] Sistema optimizado para 1000+ usuarios
- [ ] Security audit aprobado
- [ ] Monitoring y alertas configurados
- [ ] Documentación completa para usuarios finales

---

## 🛠️ Herramientas y Recursos

### 📚 Documentación
- **[README.md](README.md)** - Documentación principal actualizada
- **[PLAN_DESARROLLO_COMPLETO.md](PLAN_DESARROLLO_COMPLETO.md)** - Plan detallado con metodología
- **[DESARROLLO_INTERNO.md](DESARROLLO_INTERNO.md)** - Guías internas

### 🎛️ Portales de Desarrollo
- **[raiz.html](raiz.html)** - Portal principal de monitoreo
- **[frontend/frontend.html](frontend/frontend.html)** - Portal frontend
- **[backend/backend.html](backend/backend.html)** - Portal backend

### 🔧 Comandos Esenciales

#### Desarrollo Diario
```bash
# Levantar entorno completo
docker-compose up -d

# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Tests backend
docker-compose exec backend pytest

# Tests frontend
cd frontend && npm test
```

#### Comandos de Emergencia
```bash
# Resetear base de datos
docker-compose down -v
docker-compose up -d db
docker-compose exec backend alembic upgrade head

# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Logs de debugging
docker-compose logs backend | tail -100
docker-compose logs frontend | tail -100
```

---

## 📞 Contacto y Soporte

### 🚨 Escalación de Issues
1. **Bloqueadores Críticos:** Inmediato
2. **Issues de Desarrollo:** Dentro de 4 horas
3. **Mejoras y Features:** Próximo sprint

### 📋 Proceso de Reporte
1. Verificar en documentación existente
2. Reproducir el issue localmente
3. Crear issue en GitHub con template
4. Asignar prioridad y labels
5. Notificar al equipo relevante

---

**Última actualización:** Diciembre 2024
**Próxima revisión:** Semanal (cada lunes)
**Responsable:** Equipo de Desarrollo VersaAI