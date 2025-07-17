# VersaAI Development Scripts for Windows PowerShell
# Automatización de tareas comunes de desarrollo

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    [string]$Message = ""
)

# Colores para output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

# Variables
$BackendDir = "backend"
$FrontendDir = "frontend"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "VersaAI Development Commands" $Blue
    Write-Host ""
    Write-ColorOutput "INSTALACIÓN Y CONFIGURACIÓN:" $Green
    Write-Host "  install          - Instalar todas las dependencias"
    Write-Host "  install-backend  - Instalar dependencias del backend"
    Write-Host "  install-frontend - Instalar dependencias del frontend"
    Write-Host "  setup            - Configuración inicial completa"
    Write-Host ""
    Write-ColorOutput "DESARROLLO:" $Green
    Write-Host "  dev              - Iniciar entorno de desarrollo completo"
    Write-Host "  dev-backend      - Iniciar solo el backend"
    Write-Host "  dev-frontend     - Iniciar solo el frontend"
    Write-Host "  stop             - Detener todos los servicios"
    Write-Host ""
    Write-ColorOutput "DOCKER:" $Green
    Write-Host "  docker-up        - Iniciar servicios Docker"
    Write-Host "  docker-down      - Detener servicios Docker"
    Write-Host "  docker-status    - Ver estado de contenedores"
    Write-Host "  docker-logs      - Ver logs de Docker"
    Write-Host ""
    Write-ColorOutput "BASE DE DATOS:" $Green
    Write-Host "  migrate          - Ejecutar migraciones"
    Write-Host "  db-reset         - Resetear base de datos"
    Write-Host ""
    Write-ColorOutput "TESTING:" $Green
    Write-Host "  test             - Ejecutar todos los tests"
    Write-Host "  test-backend     - Tests del backend"
    Write-Host "  test-frontend    - Tests del frontend"
    Write-Host ""
    Write-ColorOutput "UTILIDADES:" $Green
    Write-Host "  health           - Verificar estado de servicios"
    Write-Host "  status           - Estado general del proyecto"
    Write-Host "  ports            - Verificar puertos en uso"
    Write-Host ""
    Write-ColorOutput "Uso: .\scripts.ps1 <comando>" $Yellow
}

function Install-All {
    Write-ColorOutput "Instalando todas las dependencias..." $Blue
    Install-Backend
    Install-Frontend
    Write-ColorOutput "✅ Instalación completada" $Green
}

function Install-Backend {
    Write-ColorOutput "Instalando dependencias del backend..." $Yellow
    Set-Location $BackendDir
    pip install -r requirements.txt
    if (Test-Path "requirements_dev.txt") {
        pip install -r requirements_dev.txt
    }
    Set-Location ..
}

function Install-Frontend {
    Write-ColorOutput "Instalando dependencias del frontend..." $Yellow
    Set-Location $FrontendDir
    npm install
    Set-Location ..
}

function Start-Setup {
    Write-ColorOutput "Configuración inicial de VersaAI..." $Blue
    Install-All
    Start-Docker
    Start-Sleep -Seconds 10
    Run-Migrations
    Write-ColorOutput "✅ Configuración inicial completada" $Green
}

function Start-Dev {
    Write-ColorOutput "Iniciando entorno de desarrollo..." $Blue
    Start-Docker
    Start-Sleep -Seconds 5
    
    # Iniciar backend en proceso separado
    Start-Process powershell -ArgumentList "-Command", "cd '$PWD\$BackendDir'; python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
    
    # Iniciar frontend en proceso separado
    Start-Process powershell -ArgumentList "-Command", "cd '$PWD\$FrontendDir'; npm run dev"
    
    Write-ColorOutput "✅ Servicios iniciados" $Green
    Write-ColorOutput "Backend: http://localhost:8000" $Yellow
    Write-ColorOutput "Frontend: http://localhost:3000" $Yellow
}

function Start-DevBackend {
    Write-ColorOutput "Iniciando backend en modo desarrollo..." $Yellow
    Set-Location $BackendDir
    python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    Set-Location ..
}

function Start-DevFrontend {
    Write-ColorOutput "Iniciando frontend en modo desarrollo..." $Yellow
    Set-Location $FrontendDir
    npm run dev
    Set-Location ..
}

function Stop-Services {
    Write-ColorOutput "Deteniendo servicios..." $Yellow
    Stop-Docker
    
    # Detener procesos de uvicorn y npm
    Get-Process | Where-Object {$_.ProcessName -like "*python*" -and $_.CommandLine -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process | Where-Object {$_.ProcessName -like "*node*" -and $_.CommandLine -like "*npm*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-ColorOutput "✅ Servicios detenidos" $Green
}

function Start-Docker {
    Write-ColorOutput "Iniciando servicios Docker..." $Yellow
    Set-Location $BackendDir
    docker-compose up -d db redis
    Set-Location ..
    Write-ColorOutput "✅ Servicios Docker iniciados" $Green
}

function Stop-Docker {
    Write-ColorOutput "Deteniendo servicios Docker..." $Yellow
    Set-Location $BackendDir
    docker-compose down
    Set-Location ..
    Write-ColorOutput "✅ Servicios Docker detenidos" $Green
}

function Show-DockerStatus {
    Write-ColorOutput "Estado de contenedores Docker:" $Blue
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

function Show-DockerLogs {
    Set-Location $BackendDir
    docker-compose logs -f
    Set-Location ..
}

function Run-Migrations {
    Write-ColorOutput "Ejecutando migraciones..." $Yellow
    Set-Location $BackendDir
    alembic upgrade head
    Set-Location ..
    Write-ColorOutput "✅ Migraciones completadas" $Green
}

function Reset-Database {
    Write-ColorOutput "⚠️  Reseteando base de datos..." $Red
    Stop-Docker
    Start-Sleep -Seconds 2
    Start-Docker
    Start-Sleep -Seconds 10
    Run-Migrations
    Write-ColorOutput "✅ Base de datos reseteada" $Green
}

function Run-Tests {
    Write-ColorOutput "Ejecutando todos los tests..." $Blue
    Test-Backend
    Test-Frontend
    Write-ColorOutput "✅ Tests completados" $Green
}

function Test-Backend {
    Write-ColorOutput "Ejecutando tests del backend..." $Yellow
    Set-Location $BackendDir
    if (Test-Path "tests") {
        pytest tests/ -v
    } else {
        Write-ColorOutput "⚠️  Directorio de tests no encontrado" $Yellow
    }
    Set-Location ..
}

function Test-Frontend {
    Write-ColorOutput "Ejecutando tests del frontend..." $Yellow
    Set-Location $FrontendDir
    npm run test
    Set-Location ..
}

function Check-Health {
    Write-ColorOutput "Verificando estado de servicios..." $Blue
    Write-Host ""
    
    # Verificar Docker
    Write-ColorOutput "🐳 Docker Services:" $Yellow
    try {
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Where-Object {$_ -like "*versaai*" -or $_ -like "*postgres*" -or $_ -like "*redis*"}
    } catch {
        Write-ColorOutput "❌ Docker no disponible" $Red
    }
    
    Write-Host ""
    
    # Verificar Backend
    Write-ColorOutput "🔧 Backend API:" $Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "✅ Backend API funcionando (Puerto 8000)" $Green
        }
    } catch {
        Write-ColorOutput "❌ Backend API no disponible (Puerto 8000)" $Red
    }
    
    # Verificar Frontend
    Write-ColorOutput "🎨 Frontend:" $Yellow
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "✅ Frontend funcionando (Puerto 3000)" $Green
        }
    } catch {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3001" -Method GET -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput "✅ Frontend funcionando (Puerto 3001)" $Green
            }
        } catch {
            Write-ColorOutput "❌ Frontend no disponible" $Red
        }
    }
    
    Write-Host ""
}

function Show-Status {
    Write-ColorOutput "Estado general del proyecto VersaAI" $Blue
    Write-Host ""
    
    # Verificar estructura de directorios
    Write-ColorOutput "📁 Estructura del proyecto:" $Yellow
    if (Test-Path $BackendDir) {
        Write-ColorOutput "✅ Directorio backend existe" $Green
    } else {
        Write-ColorOutput "❌ Directorio backend no encontrado" $Red
    }
    
    if (Test-Path $FrontendDir) {
        Write-ColorOutput "✅ Directorio frontend existe" $Green
    } else {
        Write-ColorOutput "❌ Directorio frontend no encontrado" $Red
    }
    
    # Verificar archivos críticos
    Write-ColorOutput "📄 Archivos críticos:" $Yellow
    $criticalFiles = @(
        "$BackendDir\requirements.txt",
        "$BackendDir\src\main.py",
        "$FrontendDir\package.json",
        "$FrontendDir\src\main.js",
        "README.md",
        "docker-compose.yml"
    )
    
    foreach ($file in $criticalFiles) {
        if (Test-Path $file) {
            Write-ColorOutput "✅ $file" $Green
        } else {
            Write-ColorOutput "❌ $file" $Red
        }
    }
    
    Write-Host ""
    Check-Health
}

function Show-Ports {
    Write-ColorOutput "Verificando puertos en uso..." $Blue
    Write-Host ""
    
    $ports = @(3000, 3001, 8000, 5432, 6379)
    foreach ($port in $ports) {
        $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-ColorOutput "✅ Puerto $port en uso" $Green
        } else {
            Write-ColorOutput "❌ Puerto $port libre" $Yellow
        }
    }
}

# Ejecutar comando
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-All }
    "install-backend" { Install-Backend }
    "install-frontend" { Install-Frontend }
    "setup" { Start-Setup }
    "dev" { Start-Dev }
    "dev-backend" { Start-DevBackend }
    "dev-frontend" { Start-DevFrontend }
    "stop" { Stop-Services }
    "docker-up" { Start-Docker }
    "docker-down" { Stop-Docker }
    "docker-status" { Show-DockerStatus }
    "docker-logs" { Show-DockerLogs }
    "migrate" { Run-Migrations }
    "db-reset" { Reset-Database }
    "test" { Run-Tests }
    "test-backend" { Test-Backend }
    "test-frontend" { Test-Frontend }
    "health" { Check-Health }
    "status" { Show-Status }
    "ports" { Show-Ports }
    default {
        Write-ColorOutput "Comando no reconocido: $Command" $Red
        Write-ColorOutput "Usa '.\scripts.ps1 help' para ver comandos disponibles" $Yellow
    }
}