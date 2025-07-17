# Configuración TRAE para VersaAI

Este directorio contiene la configuración optimizada de TRAE (el IDE de IA) específicamente para el desarrollo del proyecto VersaAI.

## 📁 Archivos de Configuración

### `config.json`
Configuración principal de TRAE que incluye:
- **Asistencia de IA**: Depuración inteligente, generación de endpoints, optimización de consultas
- **Desarrollo**: Detección de errores, auto-corrección, monitoreo de rendimiento
- **Base de datos**: PostgreSQL con configuraciones de desarrollo y testing
- **Docker**: Servicios containerizados con compose
- **Monitoreo**: Métricas y alertas en tiempo real
- **Seguridad**: Escaneo de dependencias y detección de secretos
- **Productividad**: Autocompletado inteligente y refactorización automática
- **Integraciones**: Groq AI, GitHub, y herramientas de desarrollo

### `snippets.json`
Plantillas de código reutilizables que incluyen:

#### Snippets Globales
- `versaai_header` - Encabezado estándar para archivos
- `versaai_todo` - Formato de tareas pendientes
- `versaai_function_doc` - Documentación de funciones
- `versaai_api_endpoint` - Endpoints de FastAPI
- `versaai_vue_component` - Componentes Vue 3
- `versaai_pinia_store` - Stores de Pinia

#### Snippets Específicos de VersaAI
- `vauth` - Endpoints de autenticación con validación completa
- `vchat` - Funciones de chatbot con integración Groq AI
- `vupload` - Manejadores de subida de archivos
- `vchatcomp` - Componente de chat completo para Vue

#### Snippets de IA
- `groq_integration` - Integración con Groq AI
- `ai_response_handler` - Manejo de respuestas de IA
- `conversation_manager` - Gestión de conversaciones

### `versaai-best-practices.json`
Guías de mejores prácticas específicas para VersaAI:
- **Backend**: Diseño de API, base de datos, integración de IA
- **Frontend**: Patrones Vue, UI/UX, interfaz de chat
- **Testing**: Estrategias de pruebas para backend y frontend
- **Seguridad**: Autenticación, protección de datos, seguridad de IA
- **Performance**: Optimizaciones para backend, frontend y IA
- **Deployment**: Gestión de entornos, Docker, monitoreo

## 🚀 Características Principales

### Asistencia de IA Mejorada
- **Depuración Inteligente**: Análisis automático de errores con sugerencias de solución
- **Generación de Endpoints**: Creación automática de endpoints FastAPI
- **Optimización de Consultas**: Sugerencias para mejorar consultas de base de datos
- **Validación de Esquemas**: Verificación automática de esquemas Pydantic

### Desarrollo Acelerado
- **Detección de Errores**: Identificación proactiva de problemas
- **Auto-corrección**: Sugerencias automáticas de corrección
- **Monitoreo de Rendimiento**: Análisis en tiempo real del rendimiento
- **Generación de Código**: Creación inteligente basada en contexto

### Comandos Personalizados
```bash
# Comandos disponibles en TRAE
trae:dev-start          # Iniciar entorno de desarrollo
trae:test-run           # Ejecutar suite de pruebas
trae:format-code        # Formatear código automáticamente
trae:build-prod         # Build de producción
trae:debug-auth         # Depurar problemas de autenticación
trae:db-reset           # Resetear base de datos
trae:generate-migration # Generar migración Alembic
trae:health-check       # Verificar salud del sistema
trae:optimize-imports   # Optimizar imports
```

### Plantillas de Archivos
- **FastAPI**: Endpoints, modelos, servicios
- **Vue 3**: Componentes, composables, stores
- **Pydantic**: Esquemas de validación
- **SQLAlchemy**: Modelos de base de datos
- **Pytest**: Suites de pruebas
- **Alembic**: Migraciones de base de datos

## 🛠️ Configuración Específica de VersaAI

### Desarrollo de Chatbots
- Plantillas para respuestas de IA
- Gestión de contexto de conversación
- Integración con Groq AI
- Manejo de streaming de respuestas

### Procesamiento de Archivos
- Validación de tipos de archivo
- Gestión de uploads
- Procesamiento asíncrono
- Almacenamiento seguro

### Gestión de Usuarios
- Autenticación JWT
- Roles y permisos
- Perfiles de usuario
- Actividad y estadísticas

### API Development
- Endpoints RESTful
- Documentación automática
- Validación de datos
- Manejo de errores

## 📊 Monitoreo y Métricas

### Métricas en Tiempo Real
- Tiempo de respuesta de API
- Uso de memoria y CPU
- Errores y excepciones
- Uso de IA (tokens, costos)

### Alertas Configuradas
- Errores críticos del sistema
- Rendimiento degradado
- Límites de uso de IA
- Problemas de seguridad

## 🔧 Uso de los Snippets

### En el Editor
1. Escribe el prefijo del snippet (ej: `vauth`)
2. Presiona `Tab` para expandir
3. Navega entre los placeholders con `Tab`
4. Personaliza según tus necesidades

### Ejemplos de Uso

#### Crear un Endpoint de Autenticación
```typescript
// Escribe 'vauth' y presiona Tab
@router.post('/auth/login', response_model=LoginResponse)
async def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> LoginResponse:
    """Endpoint para login de usuario"""
    // ... código generado automáticamente
```

#### Crear un Componente de Chat
```vue
<!-- Escribe 'vchatcomp' y presiona Tab -->
<template>
  <div class="chat-container flex flex-col h-full">
    <!-- Componente completo generado -->
  </div>
</template>
```

## 🎯 Beneficios de esta Configuración

1. **Desarrollo Más Rápido**: Snippets y plantillas aceleran la escritura de código
2. **Menos Errores**: Validación automática y mejores prácticas integradas
3. **Consistencia**: Patrones uniformes en todo el proyecto
4. **Mejor Calidad**: Estándares de código y testing integrados
5. **Productividad**: Herramientas de IA que asisten en el desarrollo
6. **Mantenibilidad**: Código bien estructurado y documentado

## 🔄 Actualizaciones

Esta configuración se actualiza regularmente para incluir:
- Nuevos patrones de desarrollo
- Mejores prácticas emergentes
- Optimizaciones de rendimiento
- Nuevas integraciones de IA

---

**Nota**: Esta configuración está optimizada específicamente para VersaAI y puede requerir ajustes para otros proyectos.

## 🛠️ Configuración Incluida

### 📁 Estructura de Archivos

```
.trae/
├── config.json          # Configuración principal de Trae AI
├── README.md            # Esta documentación
└── workflows/           # Flujos de trabajo automatizados
    ├── development.yml  # Workflow de desarrollo
    ├── testing.yml      # Workflow de testing
    └── deployment.yml   # Workflow de despliegue
```

### ⚙️ Características Principales

#### 🤖 Asistencia de IA
- **Auto-completado inteligente** para FastAPI y Vue.js
- **Análisis de errores** en tiempo real
- **Sugerencias de rendimiento** automáticas
- **Verificaciones de seguridad** continuas
- **Generación automática** de tests y documentación
- **Sugerencias de refactoring** basadas en mejores prácticas

#### 🔧 Desarrollo Backend (FastAPI)
- **Hot reload** automático con Uvicorn
- **Testing** automatizado con pytest y cobertura
- **Linting** con flake8, black e isort
- **Documentación API** automática (Swagger/ReDoc)
- **Migraciones** de base de datos con Alembic
- **Integración** con PostgreSQL y Redis

#### 🎨 Desarrollo Frontend (Vue.js 3)
- **Hot reload** con Vite
- **Testing** con Vitest y Vue Test Utils
- **Linting** con ESLint y Prettier
- **Styling** con Tailwind CSS
- **Estado** gestionado con Pinia
- **Routing** con Vue Router

#### 📊 Monitoreo y Métricas
- **Métricas de rendimiento** en tiempo real
- **Alertas** automáticas por errores y rendimiento
- **Monitoreo** de uso de recursos
- **Análisis** de llamadas a la API

## 🚀 Comandos Personalizados

### Desarrollo
```bash
# Iniciar entorno de desarrollo completo
trae run start_dev

# Ejecutar todos los tests
trae run run_tests

# Formatear todo el código
trae run format_code

# Build para producción
trae run build_prod
```

### Backend Específico
```bash
# Iniciar servidor FastAPI
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Ejecutar tests con cobertura
pytest tests/ -v --cov=src

# Formatear código Python
black src/ && isort src/

# Crear migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head
```

### Frontend Específico
```bash
# Iniciar servidor de desarrollo
npm run dev

# Ejecutar tests
npm run test

# Build de producción
npm run build

# Linting y formato
npm run lint:fix
```

## 📝 Plantillas de Código

### Snippets Disponibles

#### Backend (Python/FastAPI)
- `fastapi-crud` - Router completo con operaciones CRUD
- `sqlmodel` - Modelo SQLAlchemy con campos comunes
- `pydantic-schema` - Esquemas Pydantic con validación
- `service-layer` - Capa de servicio con lógica de negocio
- `pytest-test` - Suite de tests completa
- `alembic-migration` - Plantilla de migración
- `versaai-chatbot` - Modelo específico de chatbot
- `versaai-ai` - Servicio de IA con integración Groq

#### Frontend (Vue.js 3)
- `vue-component` - Componente Vue con Composition API
- `versaai-chat` - Componente de chat específico
- `pinia-store` - Store de Pinia con operaciones CRUD
- `vue-page` - Plantilla de página con Vue Router
- `api-service` - Servicio de API con operaciones CRUD
- `typescript-interface` - Interfaces TypeScript
- `vue-test` - Test de componente Vue

### Uso de Snippets

1. **En archivos Python (.py):**
   - Escribe el prefijo del snippet (ej: `fastapi-crud`)
   - Presiona `Tab` para expandir
   - Completa los placeholders

2. **En archivos Vue (.vue):**
   - Escribe el prefijo del snippet (ej: `vue-component`)
   - Presiona `Tab` para expandir
   - Personaliza según necesidades

## 🔧 Configuración de VS Code/Trae AI

### Archivos de Configuración

#### `.vscode/settings.json`
- Configuración optimizada para Vue.js y Python
- Formateadores automáticos
- Configuración de puertos y URLs
- Exclusiones de archivos
- Configuración de terminal y debugging

#### `.vscode/extensions.json`
- Extensiones recomendadas para VersaAI
- Herramientas de desarrollo específicas
- Extensiones de productividad
- Integraciones con servicios externos

#### `.vscode/launch.json`
- Configuraciones de debugging para frontend y backend
- Configuraciones para Docker
- Debugging full-stack
- Perfilado de rendimiento

#### `.vscode/tasks.json`
- Tareas automatizadas para desarrollo
- Scripts de build y testing
- Tareas de mantenimiento
- Workflows compuestos

#### `versaai.code-workspace`
- Configuración de workspace multi-carpeta
- Configuraciones específicas por proyecto
- Tareas y debugging unificados

## 🤖 Integración con IA

### Groq AI
- **Modelos disponibles:**
  - `llama3-8b-8192`
  - `llama3-70b-8192`
  - `mixtral-8x7b-32768`
  - `gemma-7b-it`

### Características de IA
- **Generación de código** contextual
- **Análisis de errores** inteligente
- **Sugerencias de optimización**
- **Documentación automática**
- **Generación de tests**
- **Refactoring inteligente**

## 📊 Monitoreo y Métricas

### Métricas Disponibles
- **Rendimiento de la API** (tiempo de respuesta)
- **Errores y excepciones**
- **Uso de recursos** (CPU, memoria)
- **Cobertura de tests**
- **Calidad del código**
- **Dependencias desactualizadas**

### Alertas Configuradas
- **Errores:** > 5 errores en 5 minutos
- **Rendimiento:** > 2000ms tiempo de respuesta
- **Disco:** > 90% de uso
- **Tests:** < 80% de cobertura

## 🔒 Seguridad

### Verificaciones Automáticas
- **Escaneo de dependencias** vulnerables
- **Detección de secretos** en código
- **Análisis de código** estático
- **Verificación de configuraciones**

### Mejores Prácticas
- Variables de entorno para secretos
- Validación de entrada de datos
- Autenticación JWT segura
- CORS configurado correctamente
- Rate limiting implementado

## 🚀 Flujos de Trabajo

### Desarrollo Diario
1. **Inicio del día:**
   ```bash
   trae run start_dev
   ```

2. **Durante el desarrollo:**
   - Trae AI proporciona sugerencias automáticas
   - Auto-completado inteligente
   - Detección de errores en tiempo real

3. **Antes de commit:**
   ```bash
   trae run format_code
   trae run run_tests
   ```

### Testing
- **Tests automáticos** en cada cambio
- **Cobertura mínima** del 80%
- **Tests de integración** incluidos
- **Mocking** de servicios externos

### Despliegue
- **Staging automático** desde rama `develop`
- **Producción manual** desde rama `main`
- **Rollback automático** en caso de errores
- **Backup automático** antes de despliegue

## 📚 Recursos Adicionales

### Documentación
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js 3 Guide](https://vuejs.org/guide/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

### Herramientas de Desarrollo
- **API Testing:** Thunder Client, Postman
- **Database:** pgAdmin, DBeaver
- **Monitoring:** Portales internos de VersaAI
- **Version Control:** Git con GitHub

## 🔧 Personalización

### Modificar Configuración
1. Edita `.trae/config.json` para cambiar configuraciones
2. Actualiza `.vscode/settings.json` para configuraciones del editor
3. Modifica snippets en `.vscode/*.code-snippets`

### Agregar Comandos Personalizados
```json
"custom_commands": {
  "mi_comando": {
    "description": "Descripción del comando",
    "command": "comando a ejecutar",
    "parallel": false
  }
}
```

### Crear Nuevos Snippets
1. Abre `.vscode/vue.code-snippets` o `.vscode/python.code-snippets`
2. Agrega tu snippet siguiendo el formato JSON
3. Reinicia Trae AI para aplicar cambios

## 🆘 Solución de Problemas

### Problemas Comunes

#### Trae AI no reconoce la configuración
```bash
# Reiniciar Trae AI
Ctrl+Shift+P -> "Trae: Reload Configuration"
```

#### Snippets no funcionan
```bash
# Verificar sintaxis JSON
# Reiniciar editor
# Verificar extensiones instaladas
```

#### Comandos personalizados fallan
```bash
# Verificar rutas en config.json
# Comprobar permisos de ejecución
# Revisar logs de Trae AI
```

### Logs y Debugging
- **Logs de Trae AI:** Panel de salida en VS Code
- **Logs del proyecto:** Configurados en `src/core/logging.py`
- **Debugging:** Configuraciones en `.vscode/launch.json`

## 📞 Soporte

Para soporte adicional:
1. Consulta la documentación oficial de Trae AI
2. Revisa los logs de error
3. Verifica la configuración del proyecto
4. Contacta al equipo de desarrollo de VersaAI

---

**Última actualización:** $(date)
**Versión de configuración:** 1.0.0
**Mantenido por:** Equipo de Desarrollo VersaAI

¡Disfruta desarrollando con Trae AI y VersaAI! 🚀🤖