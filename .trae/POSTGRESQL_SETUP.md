# PostgreSQL Configuration - VersaAI

## Estado Actual

✅ **PostgreSQL está instalado y funcionando correctamente**

### Información de la Base de Datos

- **Tipo**: PostgreSQL 15-alpine (Docker)
- **Contenedor**: `versaai_db`
- **Estado**: Running and Healthy
- **Host**: localhost
- **Puerto**: 5432
- **Base de datos**: versaai
- **Usuario**: versaai_user
- **URL de conexión**: `postgresql://versaai_user:versaai_password@localhost:5432/versaai`

### Configuración Docker

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: versaai_db
    environment:
      POSTGRES_DB: versaai
      POSTGRES_USER: versaai_user
      POSTGRES_PASSWORD: versaai_password
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U versaai_user -d versaai"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

## Esquema de Base de Datos

### Migración Actual
- **Herramienta**: Alembic
- **Revisión**: 56476fb2ea93
- **Nombre**: Initial migration
- **Fecha**: 2025-07-09 01:33:07.002988
- **Estado**: Aplicada exitosamente
- **Tablas creadas**: 7

### Tablas Existentes

#### 1. organizations
- **Propósito**: Gestión de organizaciones multi-tenant
- **Campos clave**: id, name, description, domain, logo_url, is_active, max_users, max_chatbots
- **Índices**: ix_organizations_id, ix_organizations_name (unique)

#### 2. users
- **Propósito**: Cuentas de usuario y autenticación con roles
- **Campos clave**: id, email, username, full_name, hashed_password, role, organization_id
- **Enums**: UserRole (super_admin, org_admin, user, viewer)
- **Índices**: ix_users_id, ix_users_email (unique), ix_users_username (unique)
- **Claves foráneas**: organization_id → organizations.id

#### 3. knowledge_bases
- **Propósito**: Gestión de bases de conocimiento para documentos
- **Campos clave**: id, name, description, organization_id, created_by_id, embedding_model
- **Índices**: ix_knowledge_bases_id, ix_knowledge_bases_name
- **Claves foráneas**: organization_id → organizations.id, created_by_id → users.id

#### 4. chatbots
- **Propósito**: Configuraciones de chatbots de IA
- **Campos clave**: id, name, description, system_prompt, model_name, temperature, max_tokens
- **Índices**: ix_chatbots_id, ix_chatbots_name
- **Claves foráneas**: organization_id → organizations.id, created_by_id → users.id, knowledge_base_id → knowledge_bases.id

#### 5. conversations
- **Propósito**: Conversaciones de chat entre usuarios y chatbots
- **Campos clave**: id, title, user_id, chatbot_id, is_active
- **Índices**: ix_conversations_id
- **Claves foráneas**: user_id → users.id, chatbot_id → chatbots.id

#### 6. documents
- **Propósito**: Gestión de documentos para bases de conocimiento
- **Campos clave**: id, filename, original_filename, file_type, file_size, status, metadata
- **Enums**: DocumentStatus (pending, processing, completed, failed)
- **Índices**: ix_documents_id, ix_documents_filename
- **Claves foráneas**: knowledge_base_id → knowledge_bases.id, uploaded_by_id → users.id
- **Campos JSON**: metadata (metadatos de procesamiento)

#### 7. messages
- **Propósito**: Mensajes individuales dentro de conversaciones
- **Campos clave**: id, conversation_id, role, content, metadata
- **Enums**: MessageRole (user, assistant, system)
- **Índices**: ix_messages_id
- **Claves foráneas**: conversation_id → conversations.id
- **Campos JSON**: metadata (información del modelo IA, tiempo de procesamiento)

## Comandos de Gestión

### Docker
```bash
# Iniciar PostgreSQL
docker start versaai_db

# Verificar estado
docker ps | findstr postgres

# Ver logs
docker logs versaai_db

# Conectar a la base de datos
docker exec -it versaai_db psql -U versaai_user -d versaai
```

### Migraciones con Alembic
```bash
# Crear nueva migración
alembic revision --autogenerate -m "Description"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history

# Rollback
alembic downgrade -1
```

### Verificación de Salud
```bash
# Health check del API
curl http://localhost:8000/health

# Verificar conexión directa
psql -h localhost -p 5432 -U versaai_user -d versaai -c "SELECT 1;"
```

## Configuración de Conexión

### Variables de Entorno
```env
DATABASE_URL=postgresql://versaai_user:versaai_password@localhost:5432/versaai
DATABASE_POOL_SIZE=5
DATABASE_POOL_TIMEOUT=30
```

### Configuración SQLAlchemy
```python
# PostgreSQL configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)
```

## Características Implementadas

✅ **Configuración Multi-tenant**: Organizaciones con usuarios asociados
✅ **Sistema de Roles**: super_admin, org_admin, user, viewer
✅ **Gestión de Documentos**: Con estados de procesamiento
✅ **Bases de Conocimiento**: Para almacenamiento de documentos
✅ **Sistema de Chat**: Conversaciones y mensajes
✅ **Metadatos JSON**: Para documentos y mensajes
✅ **Índices Optimizados**: Para rendimiento de consultas
✅ **Claves Foráneas**: Integridad referencial
✅ **Timestamps**: created_at y updated_at automáticos

## Próximos Pasos

1. **Implementar Embeddings**: Tabla para vectores de documentos
2. **Auditoría**: Tabla de logs de actividad
3. **Configuraciones**: Tabla de configuraciones de sistema
4. **Notificaciones**: Sistema de notificaciones
5. **Métricas**: Tablas para analytics y métricas

## Troubleshooting

### Problemas Comunes

1. **Connection refused**: Verificar que el contenedor esté ejecutándose
2. **Authentication failed**: Verificar credenciales en .env
3. **Migration errors**: Verificar estado de Alembic con `alembic current`
4. **Performance issues**: Revisar índices y consultas lentas

### Logs Importantes
```bash
# Logs del contenedor PostgreSQL
docker logs versaai_db

# Logs del backend (conexión DB)
tail -f logs/app.log
```