#!/bin/bash

# VersaAI Enterprise Dashboard - Script de Actualización
# Versión: 2.0.0
# Autor: VersaAI Team

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Variables de configuración
APP_NAME="VersaAI Enterprise Dashboard"
INSTALL_DIR="/opt/versaai"
SERVICE_USER="versaai"
BACKUP_DIR="/opt/versaai/backups"
DATE=$(date +"%Y%m%d_%H%M%S")

# Función para mostrar banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    VersaAI Enterprise Dashboard             ║"
    echo "║                    Script de Actualización                  ║"
    echo "║                         Versión 2.0.0                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para verificar si el usuario es root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "Este script debe ejecutarse como root (sudo)"
        exit 1
    fi
}

# Función para verificar si la instalación existe
check_installation() {
    if [[ ! -d "$INSTALL_DIR/frontend" ]]; then
        log_error "No se encontró una instalación existente en $INSTALL_DIR/frontend"
        log_info "Ejecuta primero el script de instalación: ./install.sh"
        exit 1
    fi
    
    log_success "Instalación existente encontrada"
}

# Función para crear backup
create_backup() {
    log_info "Creando backup de la instalación actual..."
    
    mkdir -p $BACKUP_DIR
    
    # Backup del código
    tar -czf "$BACKUP_DIR/frontend_backup_$DATE.tar.gz" -C "$INSTALL_DIR" frontend
    
    # Backup de configuración de Nginx
    if [[ -f "/etc/nginx/sites-available/versaai" ]]; then
        cp /etc/nginx/sites-available/versaai "$BACKUP_DIR/nginx_versaai_$DATE.conf"
    fi
    
    # Backup de variables de entorno
    if [[ -f "$INSTALL_DIR/frontend/.env.production" ]]; then
        cp "$INSTALL_DIR/frontend/.env.production" "$BACKUP_DIR/env_production_$DATE"
    fi
    
    log_success "Backup creado en $BACKUP_DIR/frontend_backup_$DATE.tar.gz"
}

# Función para obtener versión actual
get_current_version() {
    if [[ -f "$INSTALL_DIR/frontend/package.json" ]]; then
        CURRENT_VERSION=$(grep '"version"' "$INSTALL_DIR/frontend/package.json" | head -1 | awk -F: '{ print $2 }' | sed 's/[",]//g' | tr -d ' ')
        log_info "Versión actual: $CURRENT_VERSION"
    else
        CURRENT_VERSION="unknown"
        log_warning "No se pudo determinar la versión actual"
    fi
}

# Función para detener servicios
stop_services() {
    log_info "Deteniendo servicios..."
    
    # Detener servicio systemd si existe
    if systemctl is-active --quiet versaai-dashboard; then
        systemctl stop versaai-dashboard
        log_success "Servicio versaai-dashboard detenido"
    fi
    
    # Detener Docker si está ejecutándose
    if [[ -f "$INSTALL_DIR/frontend/docker-compose.yml" ]]; then
        cd "$INSTALL_DIR/frontend"
        if docker-compose ps | grep -q "Up"; then
            sudo -u $SERVICE_USER docker-compose down
            log_success "Contenedores Docker detenidos"
        fi
    fi
}

# Función para actualizar código
update_code() {
    log_info "Actualizando código desde repositorio..."
    
    cd "$INSTALL_DIR/frontend"
    
    # Guardar cambios locales si existen
    if ! sudo -u $SERVICE_USER git diff --quiet; then
        log_warning "Se encontraron cambios locales, creando stash..."
        sudo -u $SERVICE_USER git stash push -m "Auto-stash before update $DATE"
    fi
    
    # Actualizar repositorio
    sudo -u $SERVICE_USER git fetch origin
    sudo -u $SERVICE_USER git pull origin main
    
    log_success "Código actualizado desde repositorio"
}

# Función para actualizar dependencias
update_dependencies() {
    log_info "Actualizando dependencias de Node.js..."
    
    cd "$INSTALL_DIR/frontend"
    
    # Limpiar cache de npm
    sudo -u $SERVICE_USER npm cache clean --force
    
    # Actualizar dependencias
    sudo -u $SERVICE_USER npm ci --production
    
    log_success "Dependencias actualizadas"
}

# Función para ejecutar migraciones/scripts de actualización
run_migrations() {
    log_info "Ejecutando scripts de migración..."
    
    cd "$INSTALL_DIR/frontend"
    
    # Verificar si existe script de migración
    if [[ -f "scripts/migrate.sh" ]]; then
        sudo -u $SERVICE_USER bash scripts/migrate.sh
        log_success "Scripts de migración ejecutados"
    else
        log_info "No se encontraron scripts de migración"
    fi
}

# Función para construir aplicación
build_application() {
    log_info "Construyendo aplicación actualizada..."
    
    cd "$INSTALL_DIR/frontend"
    
    # Limpiar build anterior
    sudo -u $SERVICE_USER rm -rf dist
    
    # Construir para producción
    sudo -u $SERVICE_USER npm run build:prod
    
    log_success "Aplicación construida exitosamente"
}

# Función para actualizar configuración de Nginx
update_nginx_config() {
    log_info "Verificando configuración de Nginx..."
    
    # Verificar si hay nueva configuración
    if [[ -f "$INSTALL_DIR/frontend/nginx-default.conf" ]]; then
        # Comparar con configuración actual
        if ! diff -q "$INSTALL_DIR/frontend/nginx-default.conf" "/etc/nginx/sites-available/versaai" > /dev/null 2>&1; then
            log_warning "Se detectaron cambios en la configuración de Nginx"
            read -p "¿Deseas actualizar la configuración de Nginx? (y/n): " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Backup de configuración actual
                cp /etc/nginx/sites-available/versaai "$BACKUP_DIR/nginx_versaai_old_$DATE.conf"
                
                # Actualizar configuración
                cp "$INSTALL_DIR/frontend/nginx-default.conf" /etc/nginx/sites-available/versaai
                
                # Verificar configuración
                if nginx -t; then
                    systemctl reload nginx
                    log_success "Configuración de Nginx actualizada"
                else
                    # Restaurar configuración anterior
                    cp "$BACKUP_DIR/nginx_versaai_old_$DATE.conf" /etc/nginx/sites-available/versaai
                    log_error "Error en la nueva configuración, restaurando anterior"
                fi
            fi
        else
            log_info "Configuración de Nginx sin cambios"
        fi
    fi
}

# Función para iniciar servicios
start_services() {
    log_info "Iniciando servicios..."
    
    # Iniciar servicio systemd si existe
    if [[ -f "/etc/systemd/system/versaai-dashboard.service" ]]; then
        systemctl start versaai-dashboard
        log_success "Servicio versaai-dashboard iniciado"
    fi
    
    # Iniciar Docker si existe configuración
    if [[ -f "$INSTALL_DIR/frontend/docker-compose.yml" ]]; then
        cd "$INSTALL_DIR/frontend"
        sudo -u $SERVICE_USER docker-compose up -d
        log_success "Contenedores Docker iniciados"
    fi
    
    # Verificar Nginx
    if systemctl is-active --quiet nginx; then
        log_success "Nginx está ejecutándose"
    else
        systemctl start nginx
        log_success "Nginx iniciado"
    fi
}

# Función para verificar actualización
verify_update() {
    log_info "Verificando actualización..."
    
    # Verificar nueva versión
    if [[ -f "$INSTALL_DIR/frontend/package.json" ]]; then
        NEW_VERSION=$(grep '"version"' "$INSTALL_DIR/frontend/package.json" | head -1 | awk -F: '{ print $2 }' | sed 's/[",]//g' | tr -d ' ')
        log_info "Nueva versión: $NEW_VERSION"
    fi
    
    # Verificar servicios
    sleep 5  # Esperar a que los servicios se inicien
    
    if systemctl is-active --quiet nginx; then
        log_success "Nginx está ejecutándose correctamente"
    else
        log_error "Nginx no está ejecutándose"
    fi
    
    # Verificar conectividad
    if curl -f -s http://localhost > /dev/null; then
        log_success "Servidor web responde correctamente"
    else
        log_warning "Servidor web no responde en localhost"
    fi
    
    # Verificar build
    if [[ -d "$INSTALL_DIR/frontend/dist" ]]; then
        log_success "Build de producción encontrado"
    else
        log_error "Build de producción no encontrado"
    fi
}

# Función para limpiar archivos antiguos
cleanup() {
    log_info "Limpiando archivos temporales..."
    
    cd "$INSTALL_DIR/frontend"
    
    # Limpiar cache de npm
    sudo -u $SERVICE_USER npm cache clean --force
    
    # Limpiar node_modules si es necesario
    if [[ -d "node_modules" ]]; then
        MODULES_SIZE=$(du -sh node_modules | cut -f1)
        log_info "Tamaño de node_modules: $MODULES_SIZE"
    fi
    
    # Limpiar backups antiguos (mantener solo los últimos 5)
    if [[ -d "$BACKUP_DIR" ]]; then
        cd "$BACKUP_DIR"
        ls -t frontend_backup_*.tar.gz | tail -n +6 | xargs -r rm
        log_info "Backups antiguos limpiados"
    fi
    
    log_success "Limpieza completada"
}

# Función para mostrar información de rollback
show_rollback_info() {
    echo -e "${YELLOW}Información de Rollback:${NC}"
    echo "Si experimentas problemas con la actualización, puedes hacer rollback:"
    echo ""
    echo "1. Detener servicios:"
    echo "   sudo systemctl stop versaai-dashboard"
    echo "   sudo systemctl stop nginx"
    echo ""
    echo "2. Restaurar backup:"
    echo "   cd $INSTALL_DIR"
    echo "   sudo rm -rf frontend"
    echo "   sudo tar -xzf $BACKUP_DIR/frontend_backup_$DATE.tar.gz"
    echo "   sudo chown -R $SERVICE_USER:$SERVICE_USER frontend"
    echo ""
    echo "3. Restaurar configuración de Nginx:"
    echo "   sudo cp $BACKUP_DIR/nginx_versaai_$DATE.conf /etc/nginx/sites-available/versaai"
    echo "   sudo nginx -t && sudo systemctl reload nginx"
    echo ""
    echo "4. Iniciar servicios:"
    echo "   sudo systemctl start nginx"
    echo "   sudo systemctl start versaai-dashboard"
}

# Función para mostrar información final
show_final_info() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   ¡Actualización Completada!                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${BLUE}Información de la Actualización:${NC}"
    echo "  • Versión anterior: $CURRENT_VERSION"
    echo "  • Versión actual: $NEW_VERSION"
    echo "  • Fecha: $(date)"
    echo "  • Backup: $BACKUP_DIR/frontend_backup_$DATE.tar.gz"
    echo ""
    echo -e "${BLUE}Comandos Útiles:${NC}"
    echo "  • Ver logs: sudo journalctl -u versaai-dashboard -f"
    echo "  • Ver logs de Nginx: sudo tail -f /var/log/nginx/access.log"
    echo "  • Reiniciar servicios: sudo systemctl restart versaai-dashboard nginx"
    echo "  • Ver estado: sudo systemctl status versaai-dashboard"
    echo ""
    show_rollback_info
}

# Función principal
main() {
    show_banner
    
    log_info "Iniciando actualización de $APP_NAME"
    
    # Verificaciones previas
    check_root
    check_installation
    get_current_version
    
    # Preguntar confirmación
    echo -e "${YELLOW}¿Estás seguro de que deseas actualizar el dashboard?${NC}"
    echo "Esta operación:"
    echo "  • Creará un backup automático"
    echo "  • Detendrá los servicios temporalmente"
    echo "  • Actualizará el código y dependencias"
    echo "  • Reconstruirá la aplicación"
    echo ""
    read -p "Continuar con la actualización? (y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Actualización cancelada por el usuario"
        exit 0
    fi
    
    # Proceso de actualización
    create_backup
    stop_services
    update_code
    update_dependencies
    run_migrations
    build_application
    update_nginx_config
    start_services
    
    # Verificación y limpieza
    verify_update
    cleanup
    
    # Información final
    show_final_info
    
    log_success "¡Actualización completada exitosamente!"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -v, --version  Mostrar versión actual"
    echo "  -b, --backup   Solo crear backup"
    echo "  -c, --check    Solo verificar estado"
    echo "  --rollback     Mostrar instrucciones de rollback"
    echo ""
    echo "Ejemplos:"
    echo "  $0              Ejecutar actualización completa"
    echo "  $0 --backup     Solo crear backup"
    echo "  $0 --check      Verificar estado actual"
}

# Procesar argumentos de línea de comandos
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -v|--version)
        check_installation
        get_current_version
        echo "Versión actual: $CURRENT_VERSION"
        exit 0
        ;;
    -b|--backup)
        check_root
        check_installation
        create_backup
        exit 0
        ;;
    -c|--check)
        check_installation
        verify_update
        exit 0
        ;;
    --rollback)
        show_rollback_info
        exit 0
        ;;
    "")
        # Sin argumentos, ejecutar actualización completa
        main
        ;;
    *)
        echo "Opción desconocida: $1"
        show_help
        exit 1
        ;;
esac