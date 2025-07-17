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
  Vector DB: Pinecone / ChromaDB
  LLM: Llama3, GPT-4, Claude-3
  RAG: LangChain / LlamaIndex
```

## 🔌 APIs y Endpoints

### Autenticación (/api/v1/auth/)
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Respuesta:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Organizaciones (/api/v1/organizations/)
```http
POST /api/v1/organizations/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Mi Empresa",
  "slug": "mi-empresa",
  "subscription_plan": "professional"
}
```

### Chatbots (/api/v1/chatbots/)
```http
POST /api/v1/chatbots/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Asistente AutoBróker",
  "description": "Chatbot especializado en vehículos",
  "ai_model": "llama3-8b-8192",
  "system_prompt": "Eres un experto en vehículos...",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

## 🧠 Sistema RAG (Retrieval-Augmented Generation)

### Procesamiento de Documentos
```python
# Tipos de archivo soportados
SUPPORTED_FORMATS = {
    'text': ['.txt', '.md', '.rtf'],
    'pdf': ['.pdf'],
    'office': ['.docx', '.xlsx', '.pptx'],
    'web': ['.html', '.xml'],
    'structured': ['.json', '.csv', '.yaml']
}

# Configuración de chunking
CHUNK_CONFIG = {
    'size': 1000,
    'overlap': 200,
    'strategy': 'semantic',  # 'fixed', 'semantic', 'recursive'
    'separators': ['\n\n', '\n', '. ', ' ']
}
```

### Base de Conocimiento (/api/v1/knowledge-base/)
```http
POST /api/v1/knowledge-base/documents/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

file: [archivo.pdf]
metadata: {
  "title": "Manual de Tasación",
  "category": "vehiculos",
  "tags": ["tasacion", "evaluacion", "precios"]
}
```

## ⚙️ Configuración del Sistema

### Variables de Entorno
```bash
# Base de Datos
DATABASE_URL=postgresql://user:pass@localhost:5432/versaai
REDIS_URL=redis://localhost:6379/0

# AI/ML
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Storage
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=versaai-storage

# Security
SECRET_KEY=your-django-secret-key
JWT_SECRET_KEY=your-jwt-secret
ALLOWED_HOSTS=localhost,yourdomain.com

# Features
ENABLE_RAG=true
MAX_UPLOAD_SIZE=50MB
DEFAULT_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Configuración Docker
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/versaai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: versaai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    
  celery:
    build: .
    command: celery -A versaai worker -l info
    depends_on:
      - db
      - redis
      
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

## 📊 Límites y Recursos por Plan

### Planes de Suscripción
| Característica | Free | Professional | Enterprise |
|----------------|------|--------------|------------|
| Chatbots | 1 | 10 | Ilimitado |
| Usuarios | 3 | 25 | Ilimitado |
| Conversaciones/mes | 100 | 10,000 | Ilimitado |
| Base Conocimiento | 10MB | 1GB | Ilimitado |
| Documentos | 10 | 1,000 | Ilimitado |
| Modelos IA | Básicos | Todos | Todos + Custom |
| Soporte | Comunidad | Email | Prioritario |
| Branding | No | Sí | Sí |
| API Access | No | Limitado | Completo |
| SSO | No | No | Sí |

## 🔧 Configuración de Widgets

### Widget Embebido
```html
<!-- Integración básica -->
<div id="versaai-widget"></div>
<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'https://cdn.versaai.com/widget.js';
    script.async = true;
    script.onload = function() {
      VersaAI.init({
        chatbotId: 'your-chatbot-id',
        apiKey: 'your-api-key',
        container: '#versaai-widget',
        theme: {
          primaryColor: '#1a365d',
          fontFamily: 'Arial, sans-serif'
        },
        behavior: {
          welcomeMessage: '¡Hola! ¿En qué puedo ayudarte?',
          placeholder: 'Escribe tu mensaje...',
          quickReplies: [
            'Quiero vender mi coche',
            'Busco un vehículo',
            'Necesito tasación'
          ]
        }
      });
    };
    document.head.appendChild(script);
  })();
</script>
```

### Configuración Avanzada del Widget
```javascript
VersaAI.init({
  chatbotId: 'chatbot-123',
  apiKey: 'api-key-456',
  container: '#chat-widget',
  
  // Apariencia
  theme: {
    primaryColor: '#1a365d',
    secondaryColor: '#2d3748',
    backgroundColor: '#ffffff',
    textColor: '#2d3748',
    fontFamily: 'Inter, sans-serif',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
  },
  
  // Comportamiento
  behavior: {
    welcomeMessage: '¡Bienvenido! Soy tu asistente especializado en vehículos.',
    placeholder: 'Pregúntame sobre tasación, compra, venta...',
    enableTypingIndicator: true,
    enableSoundNotifications: false,
    autoOpen: false,
    enableQuickReplies: true,
    quickReplies: [
      { text: 'Quiero vender mi coche', payload: 'SELL_CAR' },
      { text: 'Busco un vehículo', payload: 'BUY_CAR' },
      { text: 'Necesito tasación', payload: 'VALUATION' },
      { text: 'Ayuda con documentos', payload: 'DOCUMENTS' }
    ]
  },
  
  // Configuración avanzada
  advanced: {
    enableAnalytics: true,
    sessionTimeout: 30, // minutos
    maxMessages: 100,
    enableFileUpload: true,
    allowedFileTypes: ['pdf', 'jpg', 'png', 'docx'],
    maxFileSize: '5MB'
  },
  
  // Callbacks
  callbacks: {
    onInit: function() {
      console.log('Widget inicializado');
    },
    onMessageSent: function(message) {
      console.log('Mensaje enviado:', message);
    },
    onMessageReceived: function(message) {
      console.log('Mensaje recibido:', message);
    },
    onError: function(error) {
      console.error('Error:', error);
    }
  }
});
```

## 🔍 Analytics y Monitoreo

### Métricas Disponibles
```http
GET /api/v1/analytics/conversations/
Authorization: Bearer {access_token}

Query Parameters:
- start_date: 2024-01-01
- end_date: 2024-12-31
- chatbot_id: optional
- group_by: day|week|month
```

**Respuesta:**
```json
{
  "total_conversations": 1250,
  "total_messages": 8750,
  "avg_conversation_length": 7.2,
  "avg_response_time": 1.8,
  "satisfaction_score": 4.3,
  "top_intents": [
    {"intent": "vehicle_valuation", "count": 450},
    {"intent": "sell_car", "count": 320},
    {"intent": "buy_car", "count": 280}
  ],
  "daily_stats": [
    {"date": "2024-01-01", "conversations": 45, "messages": 315},
    {"date": "2024-01-02", "conversations": 52, "messages": 364}
  ]
}
```

## 🚀 Despliegue y Escalabilidad

### Configuración de Producción
```bash
# Instalación de dependencias
pip install -r requirements.txt

# Migraciones de base de datos
python manage.py migrate

# Creación de superusuario
python manage.py createsuperuser

# Recolección de archivos estáticos
python manage.py collectstatic

# Inicio del servidor
gunicorn versaai.wsgi:application --bind 0.0.0.0:8000
```

### Monitoreo y Logs
```python
# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/versaai/app.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'versaai': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔐 Seguridad y Mejores Prácticas

### Configuración de Seguridad
```python
# settings.py
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
```

## 📝 Ejemplos de Uso

### Creación de Chatbot Especializado
```python
import requests

# Autenticación
auth_response = requests.post('https://api.versaai.com/api/v1/auth/login/json', {
    'email': 'your@email.com',
    'password': 'your_password'
})
token = auth_response.json()['tokens']['access']

# Crear organización
org_response = requests.post(
    'https://api.versaai.com/api/v1/organizations/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'name': 'AutoBróker Pro',
        'slug': 'autobroker-pro',
        'subscription_plan': 'professional'
    }
)

# Crear chatbot
chatbot_response = requests.post(
    'https://api.versaai.com/api/v1/chatbots/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'name': 'Asistente Vehículos',
        'description': 'Especialista en compra-venta de vehículos',
        'ai_model': 'llama3-8b-8192',
        'system_prompt': '''
        Eres un experto bróker de vehículos con amplia experiencia en:
        - Tasación y evaluación de vehículos usados
        - Procesos de compra-venta
        - Documentación legal requerida
        - Tendencias del mercado automotriz
        - Financiación y seguros
        
        Responde de manera profesional, clara y útil.
        ''',
        'temperature': 0.7,
        'max_tokens': 2048
    }
)

print(f"Chatbot creado con ID: {chatbot_response.json()['id']}")
```

## 🎯 Próximos Pasos

1. **Configurar entorno de desarrollo**
2. **Implementar autenticación y organizaciones**
3. **Crear chatbot especializado**
4. **Configurar base de conocimiento**
5. **Integrar widgets en sitio web**
6. **Configurar analytics y monitoreo**
7. **Optimizar rendimiento**
8. **Escalar según demanda**