$cutoffDate = (Get-Date).AddDays(-15)
$drives = @('C:', 'D:', 'E:', 'F:', 'G:', 'H:')
$allLargeFiles = @()

Write-Host "=== ANÁLISIS DE ARCHIVOS GRANDES MODIFICADOS EN LOS ÚLTIMOS 15 DÍAS ==="
Write-Host "Fecha de corte: $($cutoffDate.ToString('dd/MM/yyyy HH:mm'))"
Write-Host "Buscando archivos mayores a 100 MB...`n"

foreach ($drive in $drives) {
    if (Test-Path $drive) {
        Write-Host "Analizando disco $drive..."
        try {
            $largeFiles = Get-ChildItem -Path "$drive\" -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
                $_.LastWriteTime -gt $cutoffDate -and $_.Length -gt 100000000
            }
            
            if ($largeFiles.Count -gt 0) {
                Write-Host "  Encontrados $($largeFiles.Count) archivos grandes en $drive"
                $allLargeFiles += $largeFiles
            } else {
                Write-Host "  No se encontraron archivos grandes en $drive"
            }
        }
        catch {
            Write-Host "  Error accediendo a $drive : $($_.Exception.Message)"
        }
    } else {
        Write-Host "Disco $drive no disponible"
    }
}

Write-Host "`n=== RESULTADOS DETALLADOS ==="
if ($allLargeFiles.Count -gt 0) {
    $sortedFiles = $allLargeFiles | Sort-Object Length -Descending
    
    foreach ($file in $sortedFiles) {
        $sizeMB = [math]::Round($file.Length / 1MB, 2)
        $sizeGB = [math]::Round($file.Length / 1GB, 2)
        $drive = $file.FullName.Substring(0,2)
        
        if ($sizeGB -gt 1) {
            Write-Host "[$drive] $($file.FullName) - $sizeGB GB - $($file.LastWriteTime.ToString('dd/MM/yyyy HH:mm'))"
        } else {
            Write-Host "[$drive] $($file.FullName) - $sizeMB MB - $($file.LastWriteTime.ToString('dd/MM/yyyy HH:mm'))"
        }
    }
    
    $totalSizeGB = [math]::Round(($allLargeFiles | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
    Write-Host "`n=== RESUMEN ==="
    Write-Host "Total de archivos encontrados: $($allLargeFiles.Count)"
    Write-Host "Tamaño total: $totalSizeGB GB"
    
    # Análisis por disco
    Write-Host "`n=== ANÁLISIS POR DISCO ==="
    $groupedByDrive = $allLargeFiles | Group-Object { $_.FullName.Substring(0,2) }
    foreach ($group in $groupedByDrive) {
        $driveSize = [math]::Round(($group.Group | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
        Write-Host "$($group.Name): $($group.Count) archivos - $driveSize GB"
    }
    
    # Top 5 archivos más grandes
    Write-Host "`n=== TOP 5 ARCHIVOS MÁS GRANDES ==="
    $top5 = $sortedFiles | Select-Object -First 5
    foreach ($file in $top5) {
        $sizeGB = [math]::Round($file.Length / 1GB, 2)
        Write-Host "$($file.Name) - $sizeGB GB"
    }
} else {
    Write-Host "No se encontraron archivos grandes modificados en los últimos 15 días."
}