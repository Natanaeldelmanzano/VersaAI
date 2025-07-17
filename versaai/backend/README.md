# VersaAI Backend

Enterprise AI Chatbot Platform with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- **Multi-tenant Architecture**: Support for multiple organizations with isolated data
- **AI-Powered Chatbots**: Integration with Groq AI for natural language processing
- **RAG Capabilities**: Knowledge base integration with vector search
- **Widget System**: Embeddable chat widgets for websites
- **Analytics & Reporting**: Comprehensive analytics and performance metrics
- **User Management**: Role-based access control (Super Admin, Organization Admin, User)
- **Document Processing**: Support for PDF, DOCX, TXT, MD, HTML, and CSV files
- **Real-time Chat**: WebSocket support for real-time conversations
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: Groq API, Sentence Transformers
- **Authentication**: JWT tokens with refresh mechanism
- **Caching**: Redis (optional)
- **File Processing**: PyPDF2, python-docx, markdown
- **Deployment**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis (optional)
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd versaai/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb versaai
   
   # Run migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Setup (Recommended)

1. **Using Docker Compose**
   ```bash
   # Copy environment file
   cp .env.example .env
   # Edit .env with your configuration
   
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f api
   ```

2. **Services included**
   - **API**: FastAPI application (port 8000)
   - **Database**: PostgreSQL (port 5432)
   - **Cache**: Redis (port 6379)
   - **Proxy**: Nginx (port 80)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://versaai_user:versaai_password@localhost:5432/versaai

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Services
GROQ_API_KEY=your-groq-api-key

# App Settings
DEBUG=true
LOG_LEVEL=INFO
ALLOWED_HOSTS=["localhost", "127.0.0.1", "0.0.0.0"]

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Upload
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=["pdf", "txt", "docx", "md", "html", "csv"]
```

### Groq API Setup

1. Sign up at [Groq Console](https://console.groq.com/)
2. Create an API key
3. Add the key to your `.env` file as `GROQ_API_KEY`

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Organizations
- `GET /api/v1/organizations/` - List organizations
- `POST /api/v1/organizations/` - Create organization
- `GET /api/v1/organizations/me` - Get current organization
- `PUT /api/v1/organizations/me` - Update current organization
- `GET /api/v1/organizations/{org_id}` - Get organization
- `PUT /api/v1/organizations/{org_id}` - Update organization

### Chatbots
- `GET /api/v1/chatbots/` - List chatbots
- `POST /api/v1/chatbots/` - Create chatbot
- `GET /api/v1/chatbots/{chatbot_id}` - Get chatbot
- `PUT /api/v1/chatbots/{chatbot_id}` - Update chatbot
- `DELETE /api/v1/chatbots/{chatbot_id}` - Delete chatbot

### Conversations
- `GET /api/v1/conversations/` - List conversations
- `POST /api/v1/conversations/` - Create conversation
- `POST /api/v1/conversations/chat` - Send chat message
- `GET /api/v1/conversations/{conv_id}` - Get conversation
- `GET /api/v1/conversations/{conv_id}/messages` - Get messages

### Knowledge Base
- `GET /api/v1/knowledge-base/` - List knowledge bases
- `POST /api/v1/knowledge-base/` - Create knowledge base
- `POST /api/v1/knowledge-base/{kb_id}/documents/upload` - Upload document
- `GET /api/v1/knowledge-base/{kb_id}/search` - Search documents

### Widgets
- `GET /api/v1/widgets/{chatbot_id}/config` - Get widget config
- `GET /api/v1/widgets/{chatbot_id}/embed.js` - Get embed script
- `POST /api/v1/widgets/{chatbot_id}/chat` - Widget chat endpoint
- `GET /api/v1/widgets/{chatbot_id}/iframe` - Get iframe version
- `GET /api/v1/widgets/{chatbot_id}/preview` - Preview widget

### Analytics
- `GET /api/v1/analytics/overview` - Organization overview
- `GET /api/v1/analytics/chatbots` - Chatbot analytics
- `GET /api/v1/analytics/conversations` - Conversation analytics
- `GET /api/v1/analytics/usage` - Usage analytics

## Widget Integration

### JavaScript Embed

Add this script to your website:

```html
<script src="http://localhost:8000/api/v1/widgets/{chatbot_id}/embed.js"></script>
```

### iFrame Embed

```html
<iframe 
  src="http://localhost:8000/api/v1/widgets/{chatbot_id}/iframe" 
  width="400" 
  height="600" 
  frameborder="0">
</iframe>
```

### Widget Customization

The widget supports various customization options:

- **Theme**: `light`, `dark`, `auto`
- **Position**: `bottom-right`, `bottom-left`, `top-right`, `top-left`
- **Language**: `en`, `es`, `fr`, etc.
- **Colors**: Custom color schemes
- **Behavior**: Auto-open, welcome messages, etc.

## Development

### Project Structure

```
backend/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── tests/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=src
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black src/

# Sort imports
isort src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export DEBUG=false
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   export GROQ_API_KEY=your-groq-api-key
   ```

2. **Docker Deployment**
   ```bash
   # Build production image
   docker build -t versaai-backend .
   
   # Run with production settings
   docker run -d \
     --name versaai-api \
     -p 8000:8000 \
     -e DEBUG=false \
     -e DATABASE_URL=your-db-url \
     versaai-backend
   ```

3. **Using Docker Compose**
   ```bash
   # Production compose file
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Health Checks

- **Health endpoint**: `GET /health`
- **Database check**: Included in health endpoint
- **AI service check**: Validates Groq API connectivity

## Monitoring

### Logging

- Structured logging with configurable levels
- Request/response logging
- Error tracking with stack traces
- Performance metrics

### Metrics

- Request count and latency
- Database query performance
- AI service response times
- Error rates and types

## Security

### Authentication

- JWT tokens with refresh mechanism
- Password hashing with bcrypt
- Role-based access control
- Session management

### Data Protection

- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting

### Best Practices

- Environment variable configuration
- Secrets management
- Database connection pooling
- Error handling and logging
- API versioning

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check database status
   pg_isready -h localhost -p 5432
   
   # Verify credentials
   psql -h localhost -U versaai_user -d versaai
   ```

2. **Groq API Error**
   ```bash
   # Test API key
   curl -H "Authorization: Bearer $GROQ_API_KEY" \
        https://api.groq.com/openai/v1/models
   ```

3. **File Upload Issues**
   ```bash
   # Check upload directory permissions
   ls -la uploads/
   
   # Create directories if missing
   mkdir -p uploads/documents uploads/avatars
   ```

### Logs

```bash
# View application logs
docker-compose logs -f api

# View database logs
docker-compose logs -f db

# View all logs
docker-compose logs -f
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue on GitHub
- Check the documentation
- Review the API documentation at `/api/docs`

## Changelog

### v1.0.0
- Initial release
- Multi-tenant architecture
- AI chatbot integration
- RAG capabilities
- Widget system
- Analytics and reporting