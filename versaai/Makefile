# VersaAI Development Makefile
# Automatización de tareas comunes de desarrollo

.PHONY: help install dev test lint format clean docker-up docker-down migrate backup

# Variables
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose
BACKEND_DIR := backend
FRONTEND_DIR := frontend

# Colores para output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Mostrar ayuda
	@echo "$(BLUE)VersaAI Development Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

# === INSTALACIÓN Y CONFIGURACIÓN ===

install: ## Instalar todas las dependencias
	@echo "$(BLUE)Instalando dependencias...$(RESET)"
	$(MAKE) install-backend
	$(MAKE) install-frontend
	@echo "$(GREEN)✅ Instalación completada$(RESET)"

install-backend: ## Instalar dependencias del backend
	@echo "$(YELLOW)Instalando dependencias del backend...$(RESET)"
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt
	cd $(BACKEND_DIR) && $(PIP) install -r requirements_dev.txt

install-frontend: ## Instalar dependencias del frontend
	@echo "$(YELLOW)Instalando dependencias del frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm install

setup: ## Configuración inicial completa del proyecto
	@echo "$(BLUE)Configuración inicial de VersaAI...$(RESET)"
	$(MAKE) install
	$(MAKE) docker-up
	@sleep 10
	$(MAKE) migrate
	@echo "$(GREEN)✅ Configuración inicial completada$(RESET)"

# === DESARROLLO ===

dev: ## Iniciar entorno de desarrollo completo
	@echo "$(BLUE)Iniciando entorno de desarrollo...$(RESET)"
	$(MAKE) docker-up
	@sleep 5
	$(MAKE) dev-backend &
	$(MAKE) dev-frontend &
	wait

dev-backend: ## Iniciar solo el backend en modo desarrollo
	@echo "$(YELLOW)Iniciando backend en modo desarrollo...$(RESET)"
	cd $(BACKEND_DIR) && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Iniciar solo el frontend en modo desarrollo
	@echo "$(YELLOW)Iniciando frontend en modo desarrollo...$(RESET)"
	cd $(FRONTEND_DIR) && npm run dev

stop: ## Detener todos los servicios
	@echo "$(YELLOW)Deteniendo servicios...$(RESET)"
	$(MAKE) docker-down
	@pkill -f "uvicorn" || true
	@pkill -f "npm run dev" || true
	@echo "$(GREEN)✅ Servicios detenidos$(RESET)"

# === DOCKER DEVELOPMENT ===

docker-up: ## Iniciar servicios Docker (PostgreSQL, Redis)
	@echo "$(YELLOW)Iniciando servicios Docker...$(RESET)"
	cd $(BACKEND_DIR) && $(DOCKER_COMPOSE) up -d db redis
	@echo "$(GREEN)✅ Servicios Docker iniciados$(RESET)"

docker-down: ## Detener servicios Docker
	@echo "$(YELLOW)Deteniendo servicios Docker...$(RESET)"
	cd $(BACKEND_DIR) && $(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Servicios Docker detenidos$(RESET)"

docker-logs: ## Ver logs de Docker
	cd $(BACKEND_DIR) && $(DOCKER_COMPOSE) logs -f

docker-status: ## Ver estado de contenedores Docker
	@echo "$(BLUE)Estado de contenedores Docker:$(RESET)"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

docker-clean: ## Limpiar contenedores y volúmenes Docker
	@echo "$(YELLOW)Limpiando Docker...$(RESET)"
	cd $(BACKEND_DIR) && $(DOCKER_COMPOSE) down -v
	docker system prune -f
	@echo "$(GREEN)✅ Docker limpiado$(RESET)"

# === DOCKER FULL STACK ===

full-dev: ## Iniciar stack completo en desarrollo
	@echo "$(BLUE)🚀 Iniciando VersaAI stack completo...$(RESET)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)📋 Creando .env desde template...$(RESET)"; \
		cp .env.example .env; \
		echo "$(RED)⚠️  Actualiza .env con tu configuración$(RESET)"; \
	fi
	$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)✅ Stack completo iniciado!$(RESET)"
	@echo "$(BLUE)📊 Frontend: http://localhost:5173$(RESET)"
	@echo "$(BLUE)🔧 Backend: http://localhost:8000$(RESET)"
	@echo "$(BLUE)📚 API Docs: http://localhost:8000/api/docs$(RESET)"

full-stop: ## Detener stack completo
	@echo "$(YELLOW)Deteniendo stack completo...$(RESET)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Stack completo detenido$(RESET)"

full-logs: ## Ver logs del stack completo
	@echo "$(BLUE)Logs del stack completo:$(RESET)"
	$(DOCKER_COMPOSE) logs -f

full-restart: ## Reiniciar stack completo
	@echo "$(YELLOW)Reiniciando stack completo...$(RESET)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✅ Stack reiniciado$(RESET)"

# === DOCKER PRODUCTION ===

prod-build: ## Build para producción
	@echo "$(BLUE)🏭 Building imágenes de producción...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml build
	@echo "$(GREEN)✅ Imágenes de producción creadas$(RESET)"

prod-start: ## Iniciar en producción
	@echo "$(BLUE)🚀 Iniciando VersaAI en producción...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✅ Producción iniciada!$(RESET)"
	@echo "$(BLUE)🌐 Aplicación: http://localhost$(RESET)"

prod-stop: ## Detener producción
	@echo "$(YELLOW)Deteniendo producción...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml down
	@echo "$(GREEN)✅ Producción detenida$(RESET)"

prod-logs: ## Ver logs de producción
	@echo "$(BLUE)Logs de producción:$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml logs -f

prod-deploy: ## Deploy completo con monitoreo
	@echo "$(BLUE)🚀 Desplegando con monitoreo...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml --profile monitoring up -d --build
	@echo "$(GREEN)✅ Deploy completo!$(RESET)"
	@echo "$(BLUE)🌐 App: http://localhost$(RESET)"
	@echo "$(BLUE)📊 Prometheus: http://localhost:9090$(RESET)"
	@echo "$(BLUE)📈 Grafana: http://localhost:3001$(RESET)"

# === BASE DE DATOS ===

migrate: ## Ejecutar migraciones de base de datos
	@echo "$(YELLOW)Ejecutando migraciones...$(RESET)"
	cd $(BACKEND_DIR) && alembic upgrade head
	@echo "$(GREEN)✅ Migraciones completadas$(RESET)"

migration: ## Crear nueva migración (usar: make migration m="descripción")
	@echo "$(YELLOW)Creando nueva migración...$(RESET)"
	cd $(BACKEND_DIR) && alembic revision --autogenerate -m "$(m)"
	@echo "$(GREEN)✅ Migración creada$(RESET)"

db-reset: ## Resetear base de datos completamente
	@echo "$(RED)⚠️  Reseteando base de datos...$(RESET)"
	$(MAKE) docker-down
	$(MAKE) docker-clean
	$(MAKE) docker-up
	@sleep 10
	$(MAKE) migrate
	@echo "$(GREEN)✅ Base de datos reseteada$(RESET)"

backup: ## Crear backup de la base de datos
	@echo "$(YELLOW)Creando backup...$(RESET)"
	@mkdir -p backups
	docker exec versaai_db pg_dump -U versaai_user versaai > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Backup creado en backups/$(RESET)"

restore: ## Restaurar backup (usar: make restore file=backup_file.sql)
	@echo "$(YELLOW)Restaurando backup...$(RESET)"
	docker exec -i versaai_db psql -U versaai_user -d versaai < $(file)
	@echo "$(GREEN)✅ Backup restaurado$(RESET)"

# === TESTING ===

test: ## Ejecutar todos los tests
	@echo "$(BLUE)Ejecutando tests...$(RESET)"
	$(MAKE) test-backend
	$(MAKE) test-frontend
	@echo "$(GREEN)✅ Tests completados$(RESET)"

test-backend: ## Ejecutar tests del backend
	@echo "$(YELLOW)Ejecutando tests del backend...$(RESET)"
	cd $(BACKEND_DIR) && pytest tests/ -v --cov=src --cov-report=html

test-frontend: ## Ejecutar tests del frontend
	@echo "$(YELLOW)Ejecutando tests del frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm run test

test-watch: ## Ejecutar tests en modo watch
	cd $(BACKEND_DIR) && pytest tests/ -v --cov=src -f

test-coverage: ## Generar reporte de cobertura
	@echo "$(YELLOW)Generando reporte de cobertura...$(RESET)"
	cd $(BACKEND_DIR) && pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Reporte disponible en backend/htmlcov/index.html$(RESET)"

# === CALIDAD DE CÓDIGO ===

lint: ## Ejecutar linting en todo el código
	@echo "$(BLUE)Ejecutando linting...$(RESET)"
	$(MAKE) lint-backend
	$(MAKE) lint-frontend
	@echo "$(GREEN)✅ Linting completado$(RESET)"

lint-backend: ## Linting del backend
	@echo "$(YELLOW)Linting backend...$(RESET)"
	cd $(BACKEND_DIR) && flake8 src/ tests/
	cd $(BACKEND_DIR) && mypy src/

lint-frontend: ## Linting del frontend
	@echo "$(YELLOW)Linting frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm run lint

format: ## Formatear código automáticamente
	@echo "$(BLUE)Formateando código...$(RESET)"
	$(MAKE) format-backend
	$(MAKE) format-frontend
	@echo "$(GREEN)✅ Código formateado$(RESET)"

format-backend: ## Formatear código del backend
	@echo "$(YELLOW)Formateando backend...$(RESET)"
	cd $(BACKEND_DIR) && black src/ tests/
	cd $(BACKEND_DIR) && isort src/ tests/

format-frontend: ## Formatear código del frontend
	@echo "$(YELLOW)Formateando frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm run format

# === BUILD Y DEPLOY ===

build: ## Build de producción
	@echo "$(BLUE)Building para producción...$(RESET)"
	$(MAKE) build-frontend
	@echo "$(GREEN)✅ Build completado$(RESET)"

build-frontend: ## Build del frontend
	@echo "$(YELLOW)Building frontend...$(RESET)"
	cd $(FRONTEND_DIR) && npm run build

docker-build: ## Build de imágenes Docker (desarrollo)
	@echo "$(YELLOW)Building imágenes Docker...$(RESET)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✅ Imágenes Docker creadas$(RESET)"

docker-build-prod: ## Build de imágenes Docker (producción)
	@echo "$(YELLOW)Building imágenes Docker para producción...$(RESET)"
	$(DOCKER_COMPOSE) -f docker-compose.prod.yml build
	@echo "$(GREEN)✅ Imágenes de producción creadas$(RESET)"

# === UTILIDADES ===

clean: ## Limpiar archivos temporales y cache
	@echo "$(YELLOW)Limpiando archivos temporales...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	cd $(FRONTEND_DIR) && rm -rf node_modules/.cache
	cd $(BACKEND_DIR) && rm -rf .coverage htmlcov/
	@echo "$(GREEN)✅ Limpieza completada$(RESET)"

status: ## Ver estado de todos los servicios
	@echo "$(BLUE)Estado de servicios VersaAI:$(RESET)"
	@echo ""
	@echo "$(YELLOW)Docker Containers:$(RESET)"
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || echo "Docker no disponible"
	@echo ""
	@echo "$(YELLOW)Procesos Python:$(RESET)"
	@ps aux | grep -E "(uvicorn|python.*main)" | grep -v grep || echo "No hay procesos Python ejecutándose"
	@echo ""
	@echo "$(YELLOW)Procesos Node:$(RESET)"
	@ps aux | grep -E "(npm|node.*dev)" | grep -v grep || echo "No hay procesos Node ejecutándose"

health: ## Verificar salud de todos los servicios
	@echo "$(BLUE)Verificando salud de servicios...$(RESET)"
	@curl -s http://localhost:8000/health | jq . || echo "Backend no disponible"
	@curl -s http://localhost:8000/api/health/detailed | jq . || echo "Health check detallado no disponible"

logs: ## Ver logs en tiempo real
	@echo "$(BLUE)Logs de servicios (Ctrl+C para salir):$(RESET)"
	$(MAKE) docker-logs

ports: ## Verificar puertos en uso
	@echo "$(BLUE)Puertos en uso:$(RESET)"
	@echo "Backend (8000): $$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "No disponible")"
	@echo "Frontend (5173): $$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 || echo "No disponible")"
	@echo "PostgreSQL (5432): $$(nc -z localhost 5432 && echo "Activo" || echo "No disponible")"
	@echo "Redis (6379): $$(nc -z localhost 6379 && echo "Activo" || echo "No disponible")"

# === DOCUMENTACIÓN ===

docs: ## Generar documentación
	@echo "$(YELLOW)Generando documentación...$(RESET)"
	@echo "API Docs: http://localhost:8000/api/docs"
	@echo "ReDoc: http://localhost:8000/api/redoc"
	@echo "Health Check: http://localhost:8000/api/health/detailed"

info: ## Mostrar información del proyecto
	@echo "$(BLUE)=== VersaAI Project Information ===$(RESET)"
	@echo "Backend: FastAPI + PostgreSQL + Redis"
	@echo "Frontend: Vue.js 3 + Tailwind CSS"
	@echo "Development: Docker Compose"
	@echo ""
	@echo "$(YELLOW)URLs importantes:$(RESET)"
	@echo "• Backend API: http://localhost:8000"
	@echo "• API Docs: http://localhost:8000/api/docs"
	@echo "• Frontend: http://localhost:5173"
	@echo "• Health Check: http://localhost:8000/api/health/detailed"
	@echo ""
	@echo "$(YELLOW)Comandos útiles:$(RESET)"
	@echo "• make setup    - Configuración inicial"
	@echo "• make dev      - Iniciar desarrollo"
	@echo "• make test     - Ejecutar tests"
	@echo "• make status   - Ver estado de servicios"

quick-start: ## Inicio rápido para nuevos desarrolladores
	@echo "$(BLUE)🚀 VersaAI Quick Start$(RESET)"
	@echo ""
	@echo "$(YELLOW)1. Configuración inicial...$(RESET)"
	$(MAKE) setup
	@echo ""
	@echo "$(YELLOW)2. Verificando servicios...$(RESET)"
	@sleep 5
	$(MAKE) status
	@echo ""
	@echo "$(GREEN)✅ VersaAI está listo para desarrollo!$(RESET)"
	@echo ""
	@echo "$(BLUE)Próximos pasos:$(RESET)"
	@echo "• Visita http://localhost:8000/api/docs para la API"
	@echo "• Ejecuta 'make dev' para iniciar el desarrollo"
	@echo "• Usa 'make help' para ver todos los comandos"