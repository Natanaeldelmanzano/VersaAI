# Script para resolver problemas de Docker VHDX y optimizar espacio
# Ejecutar como Administrador

Write-Host "=== Solucionando problemas de Docker VHDX ===" -ForegroundColor Green

# 1. Detener Docker Desktop completamente
Write-Host "1. Deteniendo Docker Desktop..." -ForegroundColor Yellow
Get-Process "Docker Desktop" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process "com.docker.proxy" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process "vpnkit" -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Detener WSL
Write-Host "2. Deteniendo WSL..." -ForegroundColor Yellow
wsl --shutdown

# 3. Esperar un momento
Start-Sleep -Seconds 5

# 4. Verificar tamaño actual del VHDX
$vhdxPath = "C:\Users\Neizan\AppData\Local\Docker\wsl\disk\docker_data.vhdx"
if (Test-Path $vhdxPath) {
    $currentSize = (Get-Item $vhdxPath).Length / 1GB
    Write-Host "Tamaño actual del VHDX: $([math]::Round($currentSize, 2)) GB" -ForegroundColor Cyan
}

# 5. Optimizar VHDX (requiere Hyper-V)
Write-Host "3. Optimizando archivo VHDX..." -ForegroundColor Yellow
try {
    Optimize-VHD -Path $vhdxPath -Mode Full
    Write-Host "✓ VHDX optimizado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "⚠ No se pudo optimizar con Optimize-VHD. Intentando método alternativo..." -ForegroundColor Yellow
    
    # Método alternativo usando diskpart
    $diskpartScript = @"
select vdisk file="$vhdxPath"
compact vdisk
exit
"@
    $diskpartScript | Out-File -FilePath "C:\temp_compact.txt" -Encoding ASCII
    diskpart /s "C:\temp_compact.txt"
    Remove-Item "C:\temp_compact.txt" -ErrorAction SilentlyContinue
}

# 6. Verificar nuevo tamaño
if (Test-Path $vhdxPath) {
    $newSize = (Get-Item $vhdxPath).Length / 1GB
    Write-Host "Nuevo tamaño del VHDX: $([math]::Round($newSize, 2)) GB" -ForegroundColor Cyan
    $saved = $currentSize - $newSize
    if ($saved -gt 0) {
        Write-Host "✓ Espacio liberado: $([math]::Round($saved, 2)) GB" -ForegroundColor Green
    }
}

# 7. Reiniciar Docker Desktop
Write-Host "4. Reiniciando Docker Desktop..." -ForegroundColor Yellow
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# 8. Esperar a que Docker se inicie
Write-Host "5. Esperando a que Docker se inicie..." -ForegroundColor Yellow
$timeout = 60
$elapsed = 0
do {
    Start-Sleep -Seconds 5
    $elapsed += 5
    try {
        $dockerStatus = docker version --format json 2>$null | ConvertFrom-Json
        if ($dockerStatus) {
            Write-Host "✓ Docker iniciado correctamente" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "Esperando Docker... ($elapsed/$timeout segundos)" -ForegroundColor Yellow
    }
} while ($elapsed -lt $timeout)

if ($elapsed -ge $timeout) {
    Write-Host "⚠ Docker tardó más de lo esperado en iniciarse" -ForegroundColor Red
    Write-Host "Intenta reiniciar Docker Desktop manualmente" -ForegroundColor Yellow
}

Write-Host "\n=== Proceso completado ===" -ForegroundColor Green
Write-Host "Recomendaciones adicionales:" -ForegroundColor Cyan
Write-Host "1. Configura limpieza automática: docker system prune --schedule" -ForegroundColor White
Write-Host "2. Limita el tamaño del VHDX en Docker Desktop Settings" -ForegroundColor White
Write-Host "3. Ejecuta 'docker system prune -a' regularmente" -ForegroundColor White