# 📚 Base de Conocimiento Técnica - VersaAI Platform

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico Principal
```yaml
Backend:
  Framework: Django REST Framework 3.14+
  Base de Datos: PostgreSQL 14+
  Cache: Redis 7+
  Queue: Celery + Redis
  Storage: AWS S3 / MinIO
  
Frontend:
  Framework: React 18+ / Next.js 13+
  Estado: Redux Toolkit / Zustand
  UI: Material-UI v5 / Tailwind CSS
  Build: Vite / Webpack 5
  
AI/ML:
  Embeddings: all-MiniLM-L6-v2
  Vector DB: Pinecone / ChromaDB / Weaviate
  LLM: Llama3, GPT-4, Claude-3, Mistral
  RAG: LangChain / LlamaIndex
  
DevOps:
  Containerization: Docker + Docker Compose
  Orchestration: Kubernetes (opcional)
  CI/CD: GitHub Actions / GitLab CI
  Monitoring: Prometheus + Grafana
  Logging: ELK Stack / Loki
```

## 🔌 APIs y Endpoints Completos

### Autenticación (/api/v1/auth/)
```http
# Registro de usuario
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "company": "Tech Solutions Inc"
}
```

**Respuesta de éxito:**
```json
{
  "status": "success",
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "date_joined": "2024-07-10T12:55:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 86400
  }
}
```

```http
# Login de usuario
POST /api/v1/auth/login/json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

```http
# Refresh token
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

```http
# Obtener información del usuario actual
GET /api/v1/auth/me
Authorization: Bearer {access_token}
```

### Organizaciones (/api/v1/organizations/)
```http
# Crear organización
POST /api/v1/organizations/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Mi Empresa Tech",
  "slug": "mi-empresa-tech",
  "description": "Empresa de soluciones tecnológicas",
  "subscription_plan": "professional",
  "settings": {
    "timezone": "Europe/Madrid",
    "language": "es",
    "branding": {
      "primary_color": "#1a365d",
      "logo_url": "https://example.com/logo.png"
    }
  }
}
```

```http
# Listar organizaciones del usuario
GET /api/v1/organizations/
Authorization: Bearer {access_token}
```

```http
# Obtener detalles de organización
GET /api/v1/organizations/{org_id}/
Authorization: Bearer {access_token}
```

```http
# Actualizar organización
PATCH /api/v1/organizations/{org_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Nuevo Nombre",
  "settings": {
    "branding": {
      "primary_color": "#2d3748"
    }
  }
}
```

### Chatbots (/api/v1/chatbots/)
```http
# Crear chatbot
POST /api/v1/chatbots/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Asistente Virtual",
  "description": "Chatbot inteligente para atención al cliente",
  "ai_model": "llama3-8b-8192",
  "system_prompt": "Eres un asistente virtual profesional y amigable. Ayudas a los usuarios con sus consultas de manera clara y precisa.",
  "temperature": 0.7,
  "max_tokens": 2048,
  "configuration": {
    "enable_rag": true,
    "enable_memory": true,
    "response_format": "markdown",
    "fallback_responses": [
      "Lo siento, no tengo información sobre eso. ¿Puedes reformular tu pregunta?",
      "No estoy seguro de cómo ayudarte con eso. ¿Hay algo más específico que pueda hacer por ti?"
    ]
  }
}
```

```http
# Listar chatbots
GET /api/v1/chatbots/
Authorization: Bearer {access_token}
Query Parameters:
- organization_id: {org_id}
- search: {search_term}
- status: active|inactive
- page: 1
- page_size: 20
```

```http
# Conversación con chatbot
POST /api/v1/chatbots/{chatbot_id}/chat
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "message": "¿Cuáles son tus servicios principales?",
  "conversation_id": "conv_123456",
  "context": {
    "user_id": "user_789",
    "session_id": "session_abc123",
    "metadata": {
      "source": "website",
      "page": "/servicios"
    }
  }
}
```

## 🧠 Sistema RAG Avanzado

### Procesamiento de Documentos
```python
# Configuración completa de tipos de archivo
DOCUMENT_PROCESSORS = {
    'text': {
        'extensions': ['.txt', '.md', '.rtf'],
        'processor': 'TextProcessor',
        'chunking_strategy': 'semantic',
        'max_size': '10MB',
        'encoding': 'utf-8'
    },
    'pdf': {
        'extensions': ['.pdf'],
        'processor': 'PDFProcessor',
        'ocr_support': True,
        'table_extraction': True,
        'image_extraction': True,
        'max_size': '50MB',
        'ocr_languages': ['es', 'en', 'fr']
    },
    'office': {
        'extensions': ['.docx', '.xlsx', '.pptx'],
        'processor': 'OfficeProcessor',
        'metadata_extraction': True,
        'table_support': True,
        'max_size': '25MB'
    },
    'web': {
        'extensions': ['.html', '.xml'],
        'processor': 'WebProcessor',
        'link_following': True,
        'css_selector_filtering': True,
        'javascript_rendering': False
    },
    'structured': {
        'extensions': ['.json', '.csv', '.yaml', '.xml'],
        'processor': 'StructuredProcessor',
        'schema_validation': True,
        'nested_object_support': True
    },
    'code': {
        'extensions': ['.py', '.js', '.java', '.cpp', '.go'],
        'processor': 'CodeProcessor',
        'syntax_highlighting': True,
        'function_extraction': True,
        'comment_parsing': True
    }
}

# Configuración de chunking avanzada
CHUNKING_STRATEGIES = {
    'fixed': {
        'chunk_size': 1000,
        'overlap': 200,
        'separator': '\n\n'
    },
    'semantic': {
        'model': 'all-MiniLM-L6-v2',
        'similarity_threshold': 0.8,
        'min_chunk_size': 100,
        'max_chunk_size': 1500
    },
    'recursive': {
        'separators': ['\n\n', '\n', '. ', ' '],
        'chunk_size': 1000,
        'overlap': 200,
        'keep_separator': True
    },
    'document_structure': {
        'respect_headers': True,
        'respect_paragraphs': True,
        'respect_lists': True,
        'max_chunk_size': 2000
    }
}
```

### Base de Conocimiento (/api/v1/knowledge-base/)
```http
# Subir documento
POST /api/v1/knowledge-base/documents/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

file: [archivo.pdf]
metadata: {
  "title": "Manual de Usuario",
  "description": "Guía completa de uso del sistema",
  "category": "documentation",
  "tags": ["manual", "guia", "usuario"],
  "language": "es",
  "author": "Equipo Técnico",
  "version": "1.0",
  "access_level": "public"
}
processing_options: {
  "chunking_strategy": "semantic",
  "enable_ocr": true,
  "extract_tables": true,
  "extract_images": false
}
```

```http
# Buscar en base de conocimiento
GET /api/v1/knowledge-base/search/
Authorization: Bearer {access_token}
Query Parameters:
- q: consulta de búsqueda
- category: categoría específica
- tags: etiquetas separadas por coma
- limit: número de resultados (default: 10)
- similarity_threshold: umbral de similitud (0.0-1.0)
- include_metadata: true|false
```

```http
# Obtener estadísticas de la base de conocimiento
GET /api/v1/knowledge-base/stats/
Authorization: Bearer {access_token}
```

**Respuesta:**
```json
{
  "total_documents": 156,
  "total_chunks": 3420,
  "total_size": "245.7 MB",
  "categories": {
    "documentation": 45,
    "policies": 23,
    "faqs": 67,
    "tutorials": 21
  },
  "languages": {
    "es": 120,
    "en": 30,
    "fr": 6
  },
  "processing_status": {
    "completed": 150,
    "processing": 4,
    "failed": 2
  }
}
```

## ⚙️ Configuración del Sistema

### Variables de Entorno Completas
```bash
# ======================
# CONFIGURACIÓN BÁSICA
# ======================
DEBUG=False
SECRET_KEY=your-super-secret-django-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com,*.yourdomain.com

# ======================
# BASE DE DATOS
# ======================
DATABASE_URL=postgresql://versaai_user:secure_password@localhost:5432/versaai_db
DATABASE_CONN_MAX_AGE=60
DATABASE_CONN_HEALTH_CHECKS=True

# ======================
# REDIS Y CACHE
# ======================
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600
SESSION_CACHE_ALIAS=default

# ======================
# CELERY (TAREAS ASÍNCRONAS)
# ======================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
CELERY_TASK_SERIALIZER=json
CELERY_ACCEPT_CONTENT=json
CELERY_RESULT_SERIALIZER=json
CELERY_TIMEZONE=Europe/Madrid

# ======================
# AI/ML CONFIGURACIÓN
# ======================
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GROQ_API_KEY=gsk_your-groq-api-key-here
MISTRAL_API_KEY=your-mistral-api-key-here

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
VECTOR_DB_TYPE=pinecone  # pinecone|chromadb|weaviate

# Pinecone (si se usa)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-east1-gcp
PINECONE_INDEX_NAME=versaai-embeddings

# ChromaDB (si se usa)
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
CHROMADB_COLLECTION_NAME=versaai_knowledge

# ======================
# STORAGE Y ARCHIVOS
# ======================
# AWS S3
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=versaai-storage
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=cdn.yourdomain.com
AWS_DEFAULT_ACL=private

# Configuración de archivos
MAX_UPLOAD_SIZE=52428800  # 50MB en bytes
ALLOWED_FILE_EXTENSIONS=pdf,docx,xlsx,pptx,txt,md,html,json,csv

# ======================
# SEGURIDAD
# ======================
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=86400  # 24 horas en segundos
JWT_REFRESH_TOKEN_LIFETIME=604800  # 7 días en segundos

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_CREDENTIALS=True

# Rate Limiting
RATELIMIT_ENABLE=True
RATELIMIT_VIEW=100/hour
RATELIMIT_LOGIN=5/minute

# ======================
# FEATURES Y FUNCIONALIDADES
# ======================
ENABLE_RAG=True
ENABLE_ANALYTICS=True
ENABLE_WEBHOOKS=True
ENABLE_API_DOCS=True

# Configuración RAG
DEFAULT_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
SIMILARITY_THRESHOLD=0.7
MAX_SEARCH_RESULTS=10

# ======================
# MONITOREO Y LOGGING
# ======================
LOG_LEVEL=INFO
LOG_FILE=/var/log/versaai/app.log
SENTRY_DSN=https://your-sentry-dsn-here

# Métricas
ENABLE_PROMETHEUS_METRICS=True
PROMETHEUS_METRICS_PATH=/metrics

# ======================
# EMAIL
# ======================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=VersaAI Platform <noreply@yourdomain.com>

# ======================
# WEBHOOKS Y INTEGRACIONES
# ======================
WEBHOOK_SECRET=your-webhook-secret-key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# ======================
# DESARROLLO Y TESTING
# ======================
ENABLE_DEBUG_TOOLBAR=False
ENABLE_SILK_PROFILING=False
TEST_DATABASE_NAME=test_versaai_db
```

## 🔧 Scripts de Utilidad y Monitoreo

### Script de Verificación de PostgreSQL
```python
#!/usr/bin/env python3
"""
Script para verificar el estado de PostgreSQL en Docker
Uso: python check_postgres.py
"""

import os
import sys
import time
import psycopg2
import docker
from datetime import datetime
from urllib.parse import urlparse

class PostgreSQLChecker:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/versaai')
        self.docker_client = docker.from_env()
        self.container_name = os.getenv('POSTGRES_CONTAINER_NAME', 'versaai_db')
        
    def parse_database_url(self):
        """Parsea la URL de la base de datos"""
        parsed = urlparse(self.database_url)
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],  # Quitar el '/' inicial
            'user': parsed.username,
            'password': parsed.password
        }
    
    def check_docker_container(self):
        """Verifica el estado del contenedor Docker"""
        try:
            container = self.docker_client.containers.get(self.container_name)
            status = container.status
            
            print(f"🐳 Estado del contenedor '{self.container_name}': {status}")
            
            if status == 'running':
                # Obtener información adicional
                stats = container.stats(stream=False)
                memory_usage = stats['memory_stats']['usage'] / (1024**2)  # MB
                cpu_percent = self._calculate_cpu_percent(stats)
                
                print(f"   📊 Uso de memoria: {memory_usage:.2f} MB")
                print(f"   🔄 Uso de CPU: {cpu_percent:.2f}%")
                
                # Verificar logs recientes
                logs = container.logs(tail=5).decode('utf-8')
                if logs:
                    print(f"   📝 Últimos logs:")
                    for line in logs.strip().split('\n')[-3:]:
                        print(f"      {line}")
                
                return True
            else:
                print(f"   ❌ El contenedor no está ejecutándose")
                return False
                
        except docker.errors.NotFound:
            print(f"❌ Contenedor '{self.container_name}' no encontrado")
            return False
        except Exception as e:
            print(f"❌ Error verificando contenedor: {e}")
            return False
    
    def _calculate_cpu_percent(self, stats):
        """Calcula el porcentaje de uso de CPU"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            
            if system_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * 100.0
                return cpu_percent
        except (KeyError, ZeroDivisionError):
            pass
        return 0.0
    
    def check_database_connection(self):
        """Verifica la conexión a la base de datos"""
        db_config = self.parse_database_url()
        
        try:
            print(f"🔌 Conectando a PostgreSQL en {db_config['host']}:{db_config['port']}...")
            
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password'],
                connect_timeout=10
            )
            
            cursor = conn.cursor()
            
            # Verificar versión de PostgreSQL
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]
            print(f"   ✅ Conexión exitosa")
            print(f"   📋 Versión: {version.split(',')[0]}")
            
            # Verificar estadísticas de la base de datos
            cursor.execute("""
                SELECT 
                    pg_database_size(%s) as db_size,
                    (SELECT count(*) FROM pg_stat_activity WHERE datname = %s) as connections
            """, (db_config['database'], db_config['database']))
            
            db_size, connections = cursor.fetchone()
            db_size_mb = db_size / (1024**2)
            
            print(f"   💾 Tamaño de BD: {db_size_mb:.2f} MB")
            print(f"   🔗 Conexiones activas: {connections}")
            
            # Verificar tablas principales
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            
            tables = cursor.fetchall()
            print(f"   📊 Tablas encontradas: {len(tables)}")
            
            if tables:
                print("   📋 Principales tablas:")
                for table in tables[:5]:  # Mostrar solo las primeras 5
                    cursor.execute(f"SELECT count(*) FROM {table[0]};")
                    count = cursor.fetchone()[0]
                    print(f"      - {table[0]}: {count} registros")
            
            cursor.close()
            conn.close()
            return True
            
        except psycopg2.OperationalError as e:
            print(f"   ❌ Error de conexión: {e}")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
            return False
    
    def check_database_performance(self):
        """Verifica el rendimiento de la base de datos"""
        db_config = self.parse_database_url()
        
        try:
            conn = psycopg2.connect(**db_config, connect_timeout=5)
            cursor = conn.cursor()
            
            print("🚀 Verificando rendimiento de la base de datos...")
            
            # Test de velocidad de consulta simple
            start_time = time.time()
            cursor.execute("SELECT 1;")
            cursor.fetchone()
            query_time = (time.time() - start_time) * 1000
            
            print(f"   ⚡ Tiempo de consulta simple: {query_time:.2f}ms")
            
            # Verificar consultas lentas activas
            cursor.execute("""
                SELECT query, state, query_start, now() - query_start as duration
                FROM pg_stat_activity 
                WHERE state = 'active' 
                AND query NOT LIKE '%pg_stat_activity%'
                AND now() - query_start > interval '1 second';
            """)
            
            slow_queries = cursor.fetchall()
            if slow_queries:
                print(f"   ⚠️  Consultas lentas detectadas: {len(slow_queries)}")
                for query, state, start, duration in slow_queries[:3]:
                    print(f"      - Duración: {duration}, Estado: {state}")
                    print(f"        Query: {query[:100]}...")
            else:
                print("   ✅ No hay consultas lentas activas")
            
            # Verificar locks
            cursor.execute("""
                SELECT mode, count(*) 
                FROM pg_locks 
                WHERE granted = true 
                GROUP BY mode;
            """)
            
            locks = cursor.fetchall()
            total_locks = sum(count for _, count in locks)
            print(f"   🔒 Locks activos: {total_locks}")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"   ❌ Error verificando rendimiento: {e}")
            return False
    
    def run_full_check(self):
        """Ejecuta todas las verificaciones"""
        print("=" * 60)
        print(f"🔍 VERIFICACIÓN DE POSTGRESQL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Verificar contenedor Docker
        container_ok = self.check_docker_container()
        print()
        
        # Verificar conexión a la base de datos
        if container_ok:
            connection_ok = self.check_database_connection()
            print()
            
            # Verificar rendimiento
            if connection_ok:
                self.check_database_performance()
        
        print("=" * 60)
        
        # Resumen final
        if container_ok and connection_ok:
            print("✅ ESTADO GENERAL: SALUDABLE")
            return True
        else:
            print("❌ ESTADO GENERAL: REQUIERE ATENCIÓN")
            return False

def main():
    """Función principal"""
    checker = PostgreSQLChecker()
    
    # Verificar si se pasan argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--watch':
            # Modo de monitoreo continuo
            print("👀 Iniciando monitoreo continuo (Ctrl+C para salir)...")
            try:
                while True:
                    checker.run_full_check()
                    print("\n⏰ Esperando 30 segundos para la próxima verificación...\n")
                    time.sleep(30)
            except KeyboardInterrupt:
                print("\n👋 Monitoreo detenido por el usuario")
                sys.exit(0)
        elif sys.argv[1] == '--help':
            print("""
🔍 PostgreSQL Health Checker para VersaAI

Uso:
    python check_postgres.py              # Verificación única
    python check_postgres.py --watch      # Monitoreo continuo
    python check_postgres.py --help       # Mostrar esta ayuda

Variables de entorno:
    DATABASE_URL                 # URL de conexión a PostgreSQL
    POSTGRES_CONTAINER_NAME      # Nombre del contenedor Docker
            """)
            sys.exit(0)
    else:
        # Verificación única
        success = checker.run_full_check()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### Script de Verificación de Redis
```python
#!/usr/bin/env python3
"""
Script para verificar el estado de Redis
Uso: python check_redis.py
"""

import os
import sys
import time
import redis
import docker
from datetime import datetime, timedelta

class RedisChecker:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.docker_client = docker.from_env()
        self.container_name = os.getenv('REDIS_CONTAINER_NAME', 'versaai_redis')
        
    def check_docker_container(self):
        """Verifica el estado del contenedor Redis"""
        try:
            container = self.docker_client.containers.get(self.container_name)
            status = container.status
            
            print(f"🐳 Estado del contenedor Redis '{self.container_name}': {status}")
            
            if status == 'running':
                # Información del contenedor
                stats = container.stats(stream=False)
                memory_usage = stats['memory_stats']['usage'] / (1024**2)
                
                print(f"   📊 Uso de memoria: {memory_usage:.2f} MB")
                
                # Verificar puertos
                ports = container.attrs['NetworkSettings']['Ports']
                if '6379/tcp' in ports and ports['6379/tcp']:
                    host_port = ports['6379/tcp'][0]['HostPort']
                    print(f"   🔌 Puerto expuesto: {host_port}")
                
                return True
            else:
                print(f"   ❌ El contenedor no está ejecutándose")
                return False
                
        except docker.errors.NotFound:
            print(f"❌ Contenedor '{self.container_name}' no encontrado")
            return False
        except Exception as e:
            print(f"❌ Error verificando contenedor: {e}")
            return False
    