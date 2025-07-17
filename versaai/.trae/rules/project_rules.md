# 🚀 Reglas de Proyecto VersaAI - Configuración Optimizada para Trae AI

## 📋 Configuración General del Proyecto

### Información del Proyecto
- **Nombre**: VersaAI Enterprise Platform
- **Tipo**: Plataforma Full-Stack de Chatbots con IA
- **Stack**: FastAPI + Vue.js 3 + PostgreSQL + Redis
- **Arquitectura**: Microservicios con contenedores Docker
- **IA**: Integración con Groq AI (Llama, Mixtral)

### Idioma de Desarrollo
- **Idioma principal**: Español
- **Comentarios**: En español
- **Documentación**: En español
- **Variables y funciones**: En inglés (camelCase/snake_case)
- **Mensajes de commit**: En español

## 🎯 Reglas de Desarrollo

### Backend (FastAPI)

#### Estructura de Archivos
```
src/
├── main.py              # Punto de entrada principal
├── core/                # Configuración central
│   ├── config.py        # Variables de entorno
│   ├── database.py      # Configuración DB
│   └── security.py      # Autenticación JWT
├── models/              # Modelos SQLAlchemy
├── schemas/             # Esquemas Pydantic
├── routers/             # Endpoints API
├── services/            # Lógica de negocio
├── utils/               # Utilidades
└── tests/               # Pruebas unitarias
```

#### Convenciones de Código
- **Funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Variables**: `snake_case`
- **Archivos**: `snake_case.py`

#### Patrones Obligatorios
1. **Todos los endpoints deben incluir**:
   - Documentación con docstring
   - Response model definido
   - Manejo de errores con HTTPException
   - Validación de entrada con Pydantic
   - Autenticación cuando sea necesario

2. **Servicios deben ser**:
   - Asíncronos (`async def`)
   - Con manejo de errores
   - Con logging apropiado
   - Con type hints completos

3. **Modelos SQLAlchemy**:
   - Incluir `created_at` y `updated_at`
   - Definir relaciones explícitamente
   - Usar UUID como primary key cuando sea apropiado

### Frontend (Vue.js 3)

#### Estructura de Componentes
```
src/
├── main.js              # Punto de entrada
├── App.vue              # Componente raíz
├── components/          # Componentes reutilizables
│   ├── common/          # Componentes comunes
│   ├── chat/            # Componentes de chat
│   └── forms/           # Formularios
├── views/               # Páginas/vistas
├── stores/              # Stores Pinia
├── composables/         # Lógica reutilizable
├── utils/               # Utilidades
└── assets/              # Recursos estáticos
```

#### Convenciones Vue
- **Componentes**: `PascalCase.vue`
- **Props**: `camelCase`
- **Events**: `kebab-case`
- **Stores**: `camelCase`
- **Composables**: `use + PascalCase`

#### Patrones Obligatorios
1. **Composition API**: Usar siempre `<script setup>`
2. **TypeScript**: Todos los componentes con TS
3. **Props Interface**: Definir interfaces para props
4. **Emits**: Declarar eventos explícitamente
5. **Tailwind CSS**: Para estilos (no CSS custom)

## 🔧 Configuraciones Específicas

### Auto-Accept Rules

#### ✅ Auto-Aceptar SIEMPRE
- Creación de componentes Vue con Composition API
- Endpoints FastAPI con documentación completa
- Servicios con patrones async/await
- Esquemas Pydantic con validación
- Tests unitarios con pytest/vitest
- Formateo de código (Black, Prettier)
- Optimización de imports
- Documentación de funciones

#### ⚠️ Revisar MANUALMENTE
- Cambios en modelos de base de datos
- Migraciones de Alembic
- Configuraciones de seguridad
- Variables de entorno
- Configuraciones Docker
- Cambios en dependencias principales

#### ❌ NUNCA Auto-Aceptar
- Eliminación de archivos de configuración
- Cambios en claves de seguridad
- Modificaciones de esquemas de producción
- Eliminación de endpoints existentes

### Context Awareness

#### Contexto del Proyecto
- **Estado actual**: Desarrollo activo de funcionalidades core
- **Prioridades**: Autenticación, Chat, Gestión de archivos
- **Tecnologías**: FastAPI 0.104+, Vue 3.3+, PostgreSQL 15+
- **Patrones**: Repository pattern, Service layer, Composition API

#### Contexto de Desarrollo
- **Entorno**: Desarrollo local con Docker
- **Base de datos**: PostgreSQL en desarrollo, SQLite para tests
- **Cache**: Redis para sesiones y cache
- **IA**: Groq AI con modelos Llama y Mixtral

## 🎨 Snippets y Plantillas

### Snippets Prioritarios
1. `vauth` - Endpoint de autenticación completo
2. `vchat` - Funcionalidad de chat con IA
3. `vupload` - Manejo de archivos
4. `vservice` - Servicio con patrones async
5. `vcomponent` - Componente Vue completo
6. `vstore` - Store Pinia con TypeScript

### Plantillas de Archivos
- **FastAPI Router**: Con documentación y validación
- **Vue Component**: Con Composition API y TypeScript
- **Pydantic Schema**: Con validación completa
- **SQLAlchemy Model**: Con relaciones y timestamps
- **Test Suite**: Para backend y frontend

## 🚀 Workflows Automatizados

### Development Workflow
1. **Pre-commit**: Formateo automático
2. **Testing**: Ejecución automática de tests
3. **Linting**: Verificación de código
4. **Type Checking**: Validación de tipos

### AI Integration Workflow
1. **Context Loading**: Cargar contexto del proyecto
2. **Pattern Recognition**: Identificar patrones existentes
3. **Code Generation**: Generar código consistente
4. **Quality Check**: Verificar calidad automáticamente

## 📊 Métricas y Monitoreo

### Métricas de Desarrollo
- **Cobertura de tests**: Mínimo 80%
- **Complejidad ciclomática**: Máximo 10
- **Tiempo de respuesta API**: < 200ms
- **Tamaño de bundle**: < 2MB

### Alertas Configuradas
- Errores en desarrollo
- Tests fallidos
- Problemas de rendimiento
- Vulnerabilidades de seguridad

## 🔐 Seguridad

### Reglas de Seguridad
1. **Nunca** hardcodear credenciales
2. **Siempre** validar entrada de usuario
3. **Usar** HTTPS en producción
4. **Implementar** rate limiting
5. **Sanitizar** outputs

### Patrones de Autenticación
- JWT con refresh tokens
- Middleware de autenticación
- Roles y permisos granulares
- Sesiones seguras

## 🎯 Objetivos de Productividad

### Desarrollo Acelerado
- **Auto-completado**: 90% de código generado automáticamente
- **Debugging**: Detección proactiva de errores
- **Refactoring**: Sugerencias automáticas de mejora
- **Documentation**: Generación automática de docs

### Calidad de Código
- **Consistencia**: Patrones uniformes
- **Mantenibilidad**: Código limpio y documentado
- **Testabilidad**: Cobertura completa
- **Performance**: Optimizaciones automáticas

---

**Nota**: Estas reglas están optimizadas para el desarrollo de VersaAI y deben seguirse estrictamente para mantener la consistencia y calidad del proyecto.