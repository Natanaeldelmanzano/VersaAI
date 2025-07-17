$cutoffDate = (Get-Date).AddDays(-15)
$reportFile = "C:\Users\Neizan\Desktop\version max claude\versaai\disk_analysis_report.txt"

# Función para escribir tanto en consola como en archivo
function Write-Report {
    param($Message)
    Write-Host $Message
    Add-Content -Path $reportFile -Value $Message
}

# Limpiar archivo de reporte anterior
if (Test-Path $reportFile) { Remove-Item $reportFile }

Write-Report "=== REPORTE DE ANÁLISIS DE DISCO - $(Get-Date) ==="
Write-Report "Análisis de archivos modificados en los últimos 15 días"
Write-Report "Fecha de corte: $($cutoffDate.ToString('dd/MM/yyyy HH:mm'))"
Write-Report ""

# 1. Análisis de archivos grandes (>100MB) en todos los discos
Write-Report "=== 1. ARCHIVOS GRANDES (>100MB) EN TODOS LOS DISCOS ==="
$drives = @('C:', 'D:', 'E:', 'F:', 'G:', 'H:')
$allLargeFiles = @()

foreach ($drive in $drives) {
    if (Test-Path $drive) {
        Write-Report "Analizando disco $drive..."
        try {
            $largeFiles = Get-ChildItem -Path "$drive\" -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
                $_.LastWriteTime -gt $cutoffDate -and $_.Length -gt 100000000
            }
            
            if ($largeFiles.Count -gt 0) {
                Write-Report "  Encontrados $($largeFiles.Count) archivos grandes"
                $allLargeFiles += $largeFiles
            } else {
                Write-Report "  No se encontraron archivos grandes"
            }
        }
        catch {
            Write-Report "  Error: $($_.Exception.Message)"
        }
    }
}

if ($allLargeFiles.Count -gt 0) {
    $totalSizeGB = [math]::Round(($allLargeFiles | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
    Write-Report "Total: $($allLargeFiles.Count) archivos - $totalSizeGB GB"
    Write-Report ""
    
    # Top 10 archivos más grandes
    Write-Report "TOP 10 ARCHIVOS MÁS GRANDES:"
    $top10 = $allLargeFiles | Sort-Object Length -Descending | Select-Object -First 10
    foreach ($file in $top10) {
        $sizeGB = [math]::Round($file.Length / 1GB, 2)
        $drive = $file.FullName.Substring(0,2)
        Write-Report "[$drive] $($file.Name) - $sizeGB GB - $($file.LastWriteTime.ToString('dd/MM/yyyy'))"
    }
}

Write-Report ""

# 2. Análisis de carpetas específicas que suelen crecer
Write-Report "=== 2. ANÁLISIS DE CARPETAS CRÍTICAS ==="
$criticalFolders = @(
    "C:\Users\$env:USERNAME\Downloads",
    "C:\Users\$env:USERNAME\AppData\Local\Temp",
    "C:\Windows\Temp",
    "C:\Users\$env:USERNAME\.docker",
    "C:\Users\$env:USERNAME\.cache",
    "C:\Users\$env:USERNAME\.npm",
    "C:\ProgramData"
)

foreach ($folder in $criticalFolders) {
    if (Test-Path $folder) {
        try {
            $folderSize = (Get-ChildItem -Path $folder -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $folderSizeGB = [math]::Round($folderSize / 1GB, 2)
            
            $recentFiles = Get-ChildItem -Path $folder -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
                $_.LastWriteTime -gt $cutoffDate
            }
            
            Write-Report "$folder : $folderSizeGB GB total, $($recentFiles.Count) archivos recientes"
        }
        catch {
            Write-Report "$folder : Error de acceso"
        }
    }
}

Write-Report ""

# 3. Análisis de Docker (si existe)
Write-Report "=== 3. ANÁLISIS DE DOCKER ==="
try {
    $dockerInfo = docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}\t{{.Reclaimable}}" 2>$null
    if ($dockerInfo) {
        Write-Report "Docker está instalado:"
        foreach ($line in $dockerInfo) {
            Write-Report "  $line"
        }
    } else {
        Write-Report "Docker no está disponible o no está ejecutándose"
    }
}
catch {
    Write-Report "Docker no está instalado"
}

Write-Report ""
Write-Report "=== REPORTE COMPLETADO ==="
Write-Report "Archivo guardado en: $reportFile"

Write-Host "`nReporte completo guardado en: $reportFile"
Write-Host "Puedes abrir el archivo para ver todos los detalles."