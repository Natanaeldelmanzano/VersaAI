# 🧹 Script de Limpieza Completa de Docker - VersaAI
# Este script limpia completamente todos los contenedores, imágenes y volúmenes de Docker

Write-Host "🧹 INICIANDO LIMPIEZA COMPLETA DE DOCKER - VersaAI" -ForegroundColor Yellow
Write-Host "⚠️  ADVERTENCIA: Este script eliminará TODOS los contenedores, imágenes y volúmenes de Docker" -ForegroundColor Red
Write-Host "📋 Presiona ENTER para continuar o Ctrl+C para cancelar..."
Read-Host

# Función para mostrar progreso
function Show-Progress {
    param([string]$Message)
    Write-Host "🔄 $Message" -ForegroundColor Cyan
}

# Función para mostrar éxito
function Show-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

# Función para mostrar error
function Show-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

try {
    # 1. Detener todos los contenedores
    Show-Progress "Deteniendo todos los contenedores..."
    $runningContainers = docker ps -q
    if ($runningContainers) {
        docker stop $runningContainers
        Show-Success "Contenedores detenidos"
    } else {
        Write-Host "ℹ️  No hay contenedores ejecutándose" -ForegroundColor Blue
    }

    # 2. Eliminar todos los contenedores
    Show-Progress "Eliminando todos los contenedores..."
    $allContainers = docker ps -aq
    if ($allContainers) {
        docker rm -f $allContainers
        Show-Success "Contenedores eliminados"
    } else {
        Write-Host "ℹ️  No hay contenedores para eliminar" -ForegroundColor Blue
    }

    # 3. Eliminar todas las imágenes
    Show-Progress "Eliminando todas las imágenes..."
    $allImages = docker images -q
    if ($allImages) {
        docker rmi -f $allImages
        Show-Success "Imágenes eliminadas"
    } else {
        Write-Host "ℹ️  No hay imágenes para eliminar" -ForegroundColor Blue
    }

    # 4. Eliminar todos los volúmenes
    Show-Progress "Eliminando todos los volúmenes..."
    $allVolumes = docker volume ls -q
    if ($allVolumes) {
        docker volume rm -f $allVolumes
        Show-Success "Volúmenes eliminados"
    } else {
        Write-Host "ℹ️  No hay volúmenes para eliminar" -ForegroundColor Blue
    }

    # 5. Eliminar todas las redes personalizadas
    Show-Progress "Eliminando redes personalizadas..."
    $customNetworks = docker network ls --filter "type=custom" -q
    if ($customNetworks) {
        docker network rm $customNetworks
        Show-Success "Redes personalizadas eliminadas"
    } else {
        Write-Host "ℹ️  No hay redes personalizadas para eliminar" -ForegroundColor Blue
    }

    # 6. Limpiar caché de build
    Show-Progress "Limpiando caché de build..."
    docker builder prune -af
    Show-Success "Caché de build limpiado"

    # 7. Limpieza completa del sistema
    Show-Progress "Ejecutando limpieza completa del sistema..."
    docker system prune -af --volumes
    Show-Success "Limpieza completa del sistema ejecutada"

    # 8. Verificar limpieza
    Write-Host "\n📊 VERIFICACIÓN POST-LIMPIEZA:" -ForegroundColor Yellow
    
    Write-Host "\n🐳 Contenedores:" -ForegroundColor Cyan
    $containers = docker ps -a
    if ($containers -match "CONTAINER ID") {
        docker ps -a
    } else {
        Write-Host "✅ No hay contenedores" -ForegroundColor Green
    }
    
    Write-Host "\n🖼️  Imágenes:" -ForegroundColor Cyan
    $images = docker images
    if ($images -match "REPOSITORY") {
        docker images
    } else {
        Write-Host "✅ No hay imágenes" -ForegroundColor Green
    }
    
    Write-Host "\n💾 Volúmenes:" -ForegroundColor Cyan
    $volumes = docker volume ls
    if ($volumes -match "DRIVER") {
        docker volume ls
    } else {
        Write-Host "✅ No hay volúmenes" -ForegroundColor Green
    }
    
    Write-Host "\n🌐 Redes:" -ForegroundColor Cyan
    docker network ls
    
    Write-Host "\n💽 Uso de espacio:" -ForegroundColor Cyan
    docker system df

    Write-Host "\n🎉 LIMPIEZA COMPLETA FINALIZADA EXITOSAMENTE" -ForegroundColor Green
    Write-Host "✨ Docker está ahora completamente limpio y listo para una nueva instalación" -ForegroundColor Green
    
} catch {
    Show-Error "Error durante la limpieza: $($_.Exception.Message)"
    Write-Host "\n🔧 Intentando limpieza de emergencia..." -ForegroundColor Yellow
    
    # Limpieza de emergencia
    docker system prune -af --volumes 2>$null
    docker container prune -f 2>$null
    docker image prune -af 2>$null
    docker volume prune -f 2>$null
    docker network prune -f 2>$null
    
    Write-Host "✅ Limpieza de emergencia completada" -ForegroundColor Green
}

Write-Host "\n📋 Próximos pasos recomendados:" -ForegroundColor Yellow
Write-Host "1. Ejecutar: .\docker-setup-optimized.ps1" -ForegroundColor White
Write-Host "2. Verificar que los servicios estén funcionando" -ForegroundColor White
Write-Host "3. Probar la conectividad del backend" -ForegroundColor White

Write-Host "\n🔄 Presiona ENTER para continuar..."
Read-Host