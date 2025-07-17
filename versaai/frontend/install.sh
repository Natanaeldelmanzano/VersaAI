#!/bin/bash

# VersaAI Enterprise Dashboard - Script de Instalación Automatizada
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
APP_VERSION="2.0.0"
INSTALL_DIR="/opt/versaai"
NGINX_CONF_DIR="/etc/nginx/sites-available"
NGINX_ENABLED_DIR="/etc/nginx/sites-enabled"
SERVICE_USER="versaai"
DOMAIN="dashboard.versaai.com"
API_DOMAIN="api.versaai.com"

# Función para mostrar banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    VersaAI Enterprise Dashboard             ║"
    echo "║                    Instalación Automatizada                 ║"
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

# Función para detectar el sistema operativo
detect_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        log_error "No se pudo detectar el sistema operativo"
        exit 1
    fi
    
    log_info "Sistema detectado: $OS $VER"
}

# Función para instalar dependencias del sistema
install_system_dependencies() {
    log_info "Instalando dependencias del sistema..."
    
    if [[ $OS == *"Ubuntu"* ]] || [[ $OS == *"Debian"* ]]; then
        apt update
        apt install -y curl wget git nginx certbot python3-certbot-nginx ufw fail2ban
    elif [[ $OS == *"CentOS"* ]] || [[ $OS == *"Red Hat"* ]]; then
        yum update -y
        yum install -y curl wget git nginx certbot python3-certbot-nginx firewalld fail2ban
    else
        log_error "Sistema operativo no soportado: $OS"
        exit 1
    fi
    
    log_success "Dependencias del sistema instaladas"
}

# Función para instalar Node.js
install_nodejs() {
    log_info "Instalando Node.js..."
    
    # Instalar Node.js 18.x
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
    
    # Verificar instalación
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    
    log_success "Node.js $NODE_VERSION y npm $NPM_VERSION instalados"
}

# Función para instalar Docker
install_docker() {
    log_info "Instalando Docker..."
    
    # Instalar Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    
    # Instalar Docker Compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Agregar usuario al grupo docker
    usermod -aG docker $SUDO_USER
    
    # Iniciar y habilitar Docker
    systemctl start docker
    systemctl enable docker
    
    log_success "Docker y Docker Compose instalados"
}

# Función para crear usuario del sistema
create_system_user() {
    log_info "Creando usuario del sistema..."
    
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -s /bin/bash -d $INSTALL_DIR $SERVICE_USER
        log_success "Usuario $SERVICE_USER creado"
    else
        log_warning "Usuario $SERVICE_USER ya existe"
    fi
}

# Función para configurar directorio de instalación
setup_install_directory() {
    log_info "Configurando directorio de instalación..."
    
    mkdir -p $INSTALL_DIR
    chown -R $SERVICE_USER:$SERVICE_USER $INSTALL_DIR
    
    log_success "Directorio $INSTALL_DIR configurado"
}

# Función para clonar repositorio
clone_repository() {
    log_info "Clonando repositorio..."
    
    cd $INSTALL_DIR
    
    if [[ -d "frontend" ]]; then
        log_warning "Directorio frontend ya existe, actualizando..."
        cd frontend
        sudo -u $SERVICE_USER git pull
    else
        sudo -u $SERVICE_USER git clone https://github.com/versaai/dashboard-frontend.git frontend
        cd frontend
    fi
    
    log_success "Repositorio clonado/actualizado"
}

# Función para instalar dependencias de Node.js
install_node_dependencies() {
    log_info "Instalando dependencias de Node.js..."
    
    cd $INSTALL_DIR/frontend
    sudo -u $SERVICE_USER npm ci --production
    
    log_success "Dependencias de Node.js instaladas"
}

# Función para configurar variables de entorno
setup_environment() {
    log_info "Configurando variables de entorno..."
    
    cd $INSTALL_DIR/frontend
    
    # Crear archivo .env.production si no existe
    if [[ ! -f ".env.production" ]]; then
        sudo -u $SERVICE_USER cp .env.production.example .env.production
        
        # Configurar variables básicas
        sudo -u $SERVICE_USER sed -i "s|VITE_API_URL=.*|VITE_API_URL=https://$API_DOMAIN|g" .env.production
        sudo -u $SERVICE_USER sed -i "s|VITE_APP_NAME=.*|VITE_APP_NAME=$APP_NAME|g" .env.production
        sudo -u $SERVICE_USER sed -i "s|VITE_APP_VERSION=.*|VITE_APP_VERSION=$APP_VERSION|g" .env.production
        
        log_success "Archivo .env.production configurado"
    else
        log_warning "Archivo .env.production ya existe"
    fi
}

# Función para construir la aplicación
build_application() {
    log_info "Construyendo aplicación para producción..."
    
    cd $INSTALL_DIR/frontend
    sudo -u $SERVICE_USER npm run build:prod
    
    log_success "Aplicación construida exitosamente"
}

# Función para configurar Nginx
setup_nginx() {
    log_info "Configurando Nginx..."
    
    # Copiar configuración de Nginx
    cp $INSTALL_DIR/frontend/nginx-default.conf $NGINX_CONF_DIR/versaai
    
    # Actualizar configuración con el dominio correcto
    sed -i "s|server_name _;|server_name $DOMAIN;|g" $NGINX_CONF_DIR/versaai
    sed -i "s|root /usr/share/nginx/html;|root $INSTALL_DIR/frontend/dist;|g" $NGINX_CONF_DIR/versaai
    
    # Habilitar sitio
    ln -sf $NGINX_CONF_DIR/versaai $NGINX_ENABLED_DIR/
    
    # Remover configuración por defecto
    rm -f $NGINX_ENABLED_DIR/default
    
    # Verificar configuración
    nginx -t
    
    # Reiniciar Nginx
    systemctl restart nginx
    systemctl enable nginx
    
    log_success "Nginx configurado y reiniciado"
}

# Función para configurar SSL con Let's Encrypt
setup_ssl() {
    log_info "Configurando SSL con Let's Encrypt..."
    
    read -p "¿Deseas configurar SSL automáticamente? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Ingresa tu email para Let's Encrypt: " EMAIL
        
        # Obtener certificado SSL
        certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive
        
        # Configurar renovación automática
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
        
        log_success "SSL configurado exitosamente"
    else
        log_warning "SSL no configurado. Recuerda configurarlo manualmente."
    fi
}

# Función para configurar firewall
setup_firewall() {
    log_info "Configurando firewall..."
    
    # Configurar UFW (Ubuntu/Debian)
    if command -v ufw &> /dev/null; then
        ufw --force enable
        ufw allow ssh
        ufw allow 'Nginx Full'
        ufw allow 80
        ufw allow 443
        
        log_success "UFW configurado"
    # Configurar firewalld (CentOS/RHEL)
    elif command -v firewall-cmd &> /dev/null; then
        systemctl start firewalld
        systemctl enable firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
        
        log_success "Firewalld configurado"
    else
        log_warning "No se pudo configurar el firewall automáticamente"
    fi
}

# Función para configurar fail2ban
setup_fail2ban() {
    log_info "Configurando Fail2ban..."
    
    # Crear configuración personalizada
    cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
logpath = /var/log/nginx/error.log
EOF
    
    # Reiniciar fail2ban
    systemctl restart fail2ban
    systemctl enable fail2ban
    
    log_success "Fail2ban configurado"
}

# Función para crear servicio systemd
create_systemd_service() {
    log_info "Creando servicio systemd..."
    
    cat > /etc/systemd/system/versaai-dashboard.service << EOF
[Unit]
Description=VersaAI Enterprise Dashboard
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$INSTALL_DIR/frontend
ExecStart=/usr/bin/npm run preview:prod
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF
    
    # Recargar systemd y habilitar servicio
    systemctl daemon-reload
    systemctl enable versaai-dashboard
    
    log_success "Servicio systemd creado"
}

# Función para verificar instalación
verify_installation() {
    log_info "Verificando instalación..."
    
    # Verificar servicios
    if systemctl is-active --quiet nginx; then
        log_success "Nginx está ejecutándose"
    else
        log_error "Nginx no está ejecutándose"
    fi
    
    if systemctl is-active --quiet fail2ban; then
        log_success "Fail2ban está ejecutándose"
    else
        log_warning "Fail2ban no está ejecutándose"
    fi
    
    # Verificar archivos
    if [[ -d "$INSTALL_DIR/frontend/dist" ]]; then
        log_success "Build de producción encontrado"
    else
        log_error "Build de producción no encontrado"
    fi
    
    # Verificar conectividad
    if curl -f -s http://localhost > /dev/null; then
        log_success "Servidor web responde correctamente"
    else
        log_warning "Servidor web no responde en localhost"
    fi
}

# Función para mostrar información final
show_final_info() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    ¡Instalación Completada!                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${BLUE}Información del Dashboard:${NC}"
    echo "  • Aplicación: $APP_NAME v$APP_VERSION"
    echo "  • Directorio: $INSTALL_DIR/frontend"
    echo "  • Usuario: $SERVICE_USER"
    echo "  • Dominio: $DOMAIN"
    echo ""
    echo -e "${BLUE}URLs de Acceso:${NC}"
    echo "  • Dashboard: https://$DOMAIN"
    echo "  • API: https://$API_DOMAIN"
    echo ""
    echo -e "${BLUE}Comandos Útiles:${NC}"
    echo "  • Ver logs de Nginx: sudo tail -f /var/log/nginx/access.log"
    echo "  • Reiniciar Nginx: sudo systemctl restart nginx"
    echo "  • Ver estado del servicio: sudo systemctl status versaai-dashboard"
    echo "  • Actualizar aplicación: cd $INSTALL_DIR/frontend && sudo -u $SERVICE_USER git pull && sudo -u $SERVICE_USER npm run build:prod"
    echo ""
    echo -e "${YELLOW}Próximos Pasos:${NC}"
    echo "  1. Configurar DNS para apuntar $DOMAIN a este servidor"
    echo "  2. Configurar variables de entorno en $INSTALL_DIR/frontend/.env.production"
    echo "  3. Configurar el backend API en $API_DOMAIN"
    echo "  4. Configurar monitoreo y backups"
    echo ""
    echo -e "${BLUE}Soporte:${NC}"
    echo "  • Documentación: $INSTALL_DIR/frontend/DEPLOYMENT.md"
    echo "  • Email: support@versaai.com"
    echo "  • GitHub: https://github.com/versaai/dashboard-frontend"
}

# Función principal
main() {
    show_banner
    
    log_info "Iniciando instalación de $APP_NAME v$APP_VERSION"
    
    # Verificaciones previas
    check_root
    detect_os
    
    # Preguntar por el tipo de instalación
    echo -e "${YELLOW}Selecciona el tipo de instalación:${NC}"
    echo "1) Instalación completa (recomendada)"
    echo "2) Solo frontend (sin Docker)"
    echo "3) Solo Docker"
    read -p "Opción [1-3]: " INSTALL_TYPE
    
    case $INSTALL_TYPE in
        1)
            log_info "Instalación completa seleccionada"
            install_system_dependencies
            install_nodejs
            install_docker
            create_system_user
            setup_install_directory
            clone_repository
            install_node_dependencies
            setup_environment
            build_application
            setup_nginx
            setup_ssl
            setup_firewall
            setup_fail2ban
            create_systemd_service
            ;;
        2)
            log_info "Instalación solo frontend seleccionada"
            install_system_dependencies
            install_nodejs
            create_system_user
            setup_install_directory
            clone_repository
            install_node_dependencies
            setup_environment
            build_application
            setup_nginx
            setup_ssl
            setup_firewall
            setup_fail2ban
            ;;
        3)
            log_info "Instalación solo Docker seleccionada"
            install_system_dependencies
            install_docker
            create_system_user
            setup_install_directory
            clone_repository
            setup_environment
            log_info "Para completar la instalación, ejecuta: cd $INSTALL_DIR/frontend && docker-compose up -d"
            ;;
        *)
            log_error "Opción inválida"
            exit 1
            ;;
    esac
    
    # Verificar instalación
    verify_installation
    
    # Mostrar información final
    show_final_info
    
    log_success "¡Instalación completada exitosamente!"
}

# Ejecutar función principal
main "$@"