$cutoffDate = (Get-Date).AddDays(-15)
$hiddenFolders = @(
    "C:\Users\$env:USERNAME\AppData",
    "C:\ProgramData",
    "C:\Windows\Temp",
    "C:\Users\$env:USERNAME\AppData\Local\Temp",
    "C:\\$Recycle.Bin",
    "C:\System Volume Information",
    "C:\Users\$env:USERNAME\.cache",
    "C:\Users\$env:USERNAME\.npm",
    "C:\Users\$env:USERNAME\.docker",
    "C:\Users\$env:USERNAME\.vscode",
    "C:\Users\$env:USERNAME\.windsurf",
    "C:\Users\$env:USERNAME\.trae"
)

Write-Host "=== ANÁLISIS DE CARPETAS OCULTAS Y TEMPORALES ==="
Write-Host "Fecha de corte: $($cutoffDate.ToString('dd/MM/yyyy HH:mm'))"
Write-Host "Buscando archivos mayores a 50 MB en carpetas ocultas...`n"

$allHiddenFiles = @()

foreach ($folder in $hiddenFolders) {
    if (Test-Path $folder) {
        Write-Host "Analizando: $folder"
        try {
            $files = Get-ChildItem -Path $folder -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {
                $_.LastWriteTime -gt $cutoffDate -and $_.Length -gt 50000000
            }
            
            if ($files.Count -gt 0) {
                Write-Host "  Encontrados $($files.Count) archivos grandes"
                $allHiddenFiles += $files
                
                # Mostrar los 3 más grandes de esta carpeta
                $topFiles = $files | Sort-Object Length -Descending | Select-Object -First 3
                foreach ($file in $topFiles) {
                    $sizeMB = [math]::Round($file.Length / 1MB, 2)
                    Write-Host "    - $($file.Name): $sizeMB MB"
                }
            } else {
                Write-Host "  No se encontraron archivos grandes"
            }
        }
        catch {
            Write-Host "  Error: $($_.Exception.Message)"
        }
    } else {
        Write-Host "No existe: $folder"
    }
    Write-Host ""
}

Write-Host "=== RESUMEN DE CARPETAS OCULTAS ==="
if ($allHiddenFiles.Count -gt 0) {
    $totalSizeGB = [math]::Round(($allHiddenFiles | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
    Write-Host "Total de archivos en carpetas ocultas: $($allHiddenFiles.Count)"
    Write-Host "Tamaño total: $totalSizeGB GB`n"
    
    # Análisis por tipo de archivo
    Write-Host "=== ANÁLISIS POR EXTENSIÓN ==="
    $groupedByExt = $allHiddenFiles | Group-Object Extension
    foreach ($group in $groupedByExt | Sort-Object {($_.Group | Measure-Object -Property Length -Sum).Sum} -Descending) {
        $extSize = [math]::Round(($group.Group | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
        $ext = if ($group.Name) { $group.Name } else { "(sin extensión)"
        Write-Host "$ext : $($group.Count) archivos - $extSize MB"
    }
} else {
    Write-Host "No se encontraron archivos grandes en carpetas ocultas."
}