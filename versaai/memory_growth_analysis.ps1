# Script para analizar el incremento de memoria en directorios específicos
$reportFile = "C:\Users\Neizan\Desktop\version max claude\versaai\memory_growth_report.txt"
$baselineFile = "C:\Users\Neizan\Desktop\version max claude\versaai\memory_baseline.json"
$currentDate = Get-Date

# Función para escribir tanto en consola como en archivo
function Write-Report {
    param($Message)
    Write-Host $Message
    Add-Content -Path $reportFile -Value $Message
}

# Función para obtener el tamaño de un directorio de forma segura
function Get-DirectorySize {
    param($Path)
    try {
        if (Test-Path $Path) {
            $size = (Get-ChildItem -Path $Path -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            if ($size -eq $null) { $size = 0 }
            return $size
        } else {
            return 0
        }
    }
    catch {
        return -1  # Indica error de acceso
    }
}

# Función para formatear bytes
function Format-Bytes {
    param($Bytes)
    if ($Bytes -eq -1) { return "ACCESO DENEGADO" }
    if ($Bytes -eq 0) { return "0 B" }
    
    $sizes = @("B", "KB", "MB", "GB", "TB")
    $order = [Math]::Floor([Math]::Log($Bytes, 1024))
    $num = [Math]::Round($Bytes / [Math]::Pow(1024, $order), 2)
    return "$num $($sizes[$order])"
}

# Limpiar archivo de reporte anterior
if (Test-Path $reportFile) { Remove-Item $reportFile }

Write-Report "=== ANALISIS DE INCREMENTO DE MEMORIA - $($currentDate.ToString('dd/MM/yyyy HH:mm:ss')) ==="
Write-Report "Analisis de crecimiento en directorios del sistema"
Write-Report ""

# Directorios a monitorear
$directoriesToMonitor = @(
    "C:\Windows\System32\config",
    "C:\Windows\CSC",
    "C:\Windows\LiveKernelReports",
    "C:\Windows\ModemLogs",
    "C:\Windows\Prefetch",
    "C:\Windows\ServiceState",
    "C:\Windows\SystemTemp",
    "C:\Windows\Temp",
    "C:\System Volume Information",
    "C:\PerfLogs",
    "C:\ProgramData\Microsoft\Diagnosis",
    "C:\Program Files\WindowsApps",
    "C:\ProgramData\Packages",
    "C:\ProgramData\WindowsHolographicDevices",
    "C:\Windows\Logs",
    "C:\Windows\SoftwareDistribution",
    "C:\Windows\WinSxS",
    "C:\ProgramData\Microsoft\Windows\WER",
    "C:\Users\$env:USERNAME\AppData\Local\Temp",
    "C:\Users\$env:USERNAME\AppData\Local\Microsoft\Windows\INetCache",
    "C:\Users\$env:USERNAME\AppData\Local\CrashDumps",
    "C:\Users\$env:USERNAME\Downloads",
    "C:\ProgramData"
)

# Obtener mediciones actuales
$currentMeasurements = @{}
Write-Report "=== 1. MEDICIONES ACTUALES ==="

foreach ($dir in $directoriesToMonitor) {
    $size = Get-DirectorySize -Path $dir
    $currentMeasurements[$dir] = @{
        'Size' = $size
        'Timestamp' = $currentDate
        'FormattedSize' = Format-Bytes -Bytes $size
    }
    
    Write-Report "$dir : $($currentMeasurements[$dir].FormattedSize)"
}

# Cargar mediciones anteriores si existen
$baselineExists = Test-Path $baselineFile
$previousMeasurements = @{}

if ($baselineExists) {
    try {
        $jsonContent = Get-Content $baselineFile -Raw | ConvertFrom-Json
        foreach ($property in $jsonContent.PSObject.Properties) {
            $previousMeasurements[$property.Name] = @{
                'Size' = $property.Value.Size
                'Timestamp' = [DateTime]$property.Value.Timestamp
                'FormattedSize' = $property.Value.FormattedSize
            }
        }
        Write-Report ""
        Write-Report "=== 2. COMPARACION CON MEDICION ANTERIOR ==="
        Write-Report "Medicion anterior: $($previousMeasurements.Values[0].Timestamp.ToString('dd/MM/yyyy HH:mm:ss'))"
        Write-Report ""
    }
    catch {
        Write-Report ""
        Write-Report "Error al cargar mediciones anteriores: $($_.Exception.Message)"
        $baselineExists = $false
    }
}

if ($baselineExists) {
    # Analizar cambios
    $significantChanges = @()
    $totalGrowth = 0
    
    Write-Report "DIRECTORIO | ANTERIOR | ACTUAL | CAMBIO | PORCENTAJE CAMBIO"
    Write-Report "$('-' * 80)"
    
    foreach ($dir in $directoriesToMonitor) {
        if ($previousMeasurements.ContainsKey($dir) -and $currentMeasurements.ContainsKey($dir)) {
            $prevSize = $previousMeasurements[$dir].Size
            $currSize = $currentMeasurements[$dir].Size
            
            if ($prevSize -ge 0 -and $currSize -ge 0) {
                $change = $currSize - $prevSize
                $percentChange = if ($prevSize -gt 0) { [Math]::Round(($change / $prevSize) * 100, 2) } else { 0 }
                
                $changeFormatted = if ($change -gt 0) { 
                    "+$(Format-Bytes -Bytes $change)" 
                } elseif ($change -lt 0) { 
                    "-$(Format-Bytes -Bytes ([Math]::Abs($change)))" 
                } else { 
                    "Sin cambio" 
                }
                
                $dirShort = if ($dir.Length -gt 35) { $dir.Substring(0, 32) + "..." } else { $dir }
                Write-Report "$($dirShort.PadRight(35)) | $($previousMeasurements[$dir].FormattedSize.PadLeft(10)) | $($currentMeasurements[$dir].FormattedSize.PadLeft(10)) | $($changeFormatted.PadLeft(12)) | $($percentChange.ToString().PadLeft(8))%"
                
                if ([Math]::Abs($change) -gt 10MB -or [Math]::Abs($percentChange) -gt 10) {
                    $significantChanges += @{
                        'Directory' = $dir
                        'Change' = $change
                        'PercentChange' = $percentChange
                        'Previous' = $prevSize
                        'Current' = $currSize
                    }
                }
                
                if ($change -gt 0) { $totalGrowth += $change }
            }
        }
    }
    
    Write-Report ""
    Write-Report "=== 3. RESUMEN DE CAMBIOS SIGNIFICATIVOS ==="
    
    if ($significantChanges.Count -gt 0) {
        Write-Report "Cambios significativos detectados (>10MB o >10%):"
        Write-Report ""
        
        $significantChanges | Sort-Object { [Math]::Abs($_.Change) } -Descending | ForEach-Object {
            $changeFormatted = if ($_.Change -gt 0) { 
                "+$(Format-Bytes -Bytes $_.Change)" 
            } else { 
                "-$(Format-Bytes -Bytes ([Math]::Abs($_.Change)))" 
            }
            Write-Report "  Directorio: $($_.Directory)"
            Write-Report "     Cambio: $changeFormatted ($($_.PercentChange)%)"
            Write-Report "     Anterior: $(Format-Bytes -Bytes $_.Previous) -> Actual: $(Format-Bytes -Bytes $_.Current)"
            Write-Report ""
        }
    } else {
        Write-Report "No se detectaron cambios significativos en los directorios monitoreados."
    }
    
    Write-Report "Crecimiento total detectado: $(Format-Bytes -Bytes $totalGrowth)"
    
} else {
    Write-Report ""
    Write-Report "=== PRIMERA MEDICION ==="
    Write-Report "Esta es la primera vez que se ejecuta el analisis."
    Write-Report "Las mediciones actuales se guardaran como linea base para futuras comparaciones."
}

# Guardar mediciones actuales como nueva línea base
try {
    $currentMeasurements | ConvertTo-Json -Depth 3 | Set-Content $baselineFile
    Write-Report ""
    Write-Report "Mediciones guardadas en: $baselineFile"
}
catch {
    Write-Report ""
    Write-Report "Error al guardar mediciones: $($_.Exception.Message)"
}

Write-Report ""
Write-Report "=== 4. RECOMENDACIONES ==="
Write-Report "• Ejecute este script regularmente para monitorear el crecimiento"
Write-Report "• Los directorios con acceso denegado no pueden ser analizados en detalle"
Write-Report "• Considere limpiar directorios temporales si muestran crecimiento excesivo"
Write-Report "• Use herramientas del sistema como Liberador de espacio en disco para limpieza"

Write-Report ""
Write-Report "=== ANALISIS COMPLETADO ==="
Write-Report "Reporte guardado en: $reportFile"
Write-Report "Linea base actualizada en: $baselineFile"

Write-Host "`nAnalisis de incremento de memoria completado."
Write-Host "Reporte: $reportFile"
Write-Host "Linea base: $baselineFile"