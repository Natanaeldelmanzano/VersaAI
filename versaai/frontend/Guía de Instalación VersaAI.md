# 🚀 Guía de Instalación VersaAI

## Opción 1: Instalación Rápida con Docker (Recomendada)

### Prerrequisitos
- Docker y Docker Compose instalados
- 4GB de RAM disponible
- 2GB de espacio en disco

### Pasos
```bash
# 1. Clonar o descargar los archivos
git clone <tu-repositorio> versaai
cd versaai

# 2. Iniciar solo PostgreSQL primero
docker-compose up -d postgres

# 3. Esperar que PostgreSQL esté listo (30 segundos)
docker-compose logs postgres

# 4. Construir e iniciar la aplicación
docker-compose up --build
```

### Verificación
- Aplicación: http://localhost:8000
- Documentación API: http://localhost:8000/docs
- Base de datos: localhost:5432

---

## Opción 2: Instalación Manual

### Prerrequisitos
- Python 3.11+
- PostgreSQL 13+
- Git

### Paso 1: Preparar el entorno
```bash
# Crear directorio del proyecto
mkdir versaai && cd versaai

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Configurar PostgreSQL
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb versaai_db
sudo -u postgres psql -c "CREATE USER versaai WITH PASSWORD 'tu_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE versaai_db TO versaai;"
```

### Paso 3: Configurar variables de entorno
```bash
# Crear archivo .env
cat > .env << EOF
DATABASE_URL=postgresql://versaai:tu_password@localhost:5432/versaai_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=versaai_db
DB_USER=versaai
DB_PASSWORD=tu_password
HOST=0.0.0.0
PORT=8000
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOF
```

### Paso 4: Verificar instalación
```bash
# Ejecutar script de verificación
python init_check.py

# Si todo está OK, iniciar servidor
uvicorn src.main:app --reload
```

---

## 🔧 Resolución de Problemas Comunes

### Error: "No module named 'psycopg2'"
```bash
# Solución
pip install psycopg2-binary
```

### Error: "Connection refused" (PostgreSQL)
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo systemctl status postgresql
sudo systemctl start postgresql

# Verificar puerto
sudo netstat -tlnp | grep 5432
```

### Error: "Out of memory" durante descarga del modelo
```bash
# Usar modelo más pequeño
export EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L12-v2"

# O descargar manualmente
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Error: "Port 8000 already in use"
```bash
# Cambiar puerto
uvicorn src.main:app --port 8001

# O liberar puerto
sudo lsof -ti:8000 | xargs kill -9
```

### Problemas con Docker
```bash
# Limpiar contenedores
docker-compose down -v
docker system prune -f

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up
```

---

## 📊 Verificación de Funcionamiento

### Tests básicos
```bash
# Test de conexión a la API
curl http://localhost:8000/health

# Test de base de datos
curl -X POST http://localhost:8000/api/conversations \
     -H "Content-Type: application/json" \
     -d '{"title": "Test"}'

# Test de IA
curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hola, ¿cómo estás?"}'
```

### Logs importantes
```bash
# Logs de la aplicación
tail -f logs/app.log

# Logs de Docker
docker-compose logs -f versaai_app

# Logs de PostgreSQL
docker-compose logs postgres
```

---

## 🎯 Próximos Pasos

1. **Personalizar la IA**: Edita `src/services/ai_service.py`
2. **Añadir autenticación**: Implementa JWT en `src/auth/`
3. **Frontend**: Conecta con React/Vue/Angular
4. **Monitoreo**: Añade Prometheus/Grafana
5. **Despliegue**: Configura para producción

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs detalladamente
2. Verifica que todos los servicios estén ejecutándose
3. Consulta la documentación de la API en `/docs`
4. Ejecuta `python init_check.py` para diagnósticos

**¡Tu plataforma VersaAI está lista para revolucionar la intermediación de vehículos! 🚗✨**