# Script para identificar carpetas con acceso denegado
$reportFile = "C:\Users\Neizan\Desktop\version max claude\versaai\access_denied_report.txt"
$accessDeniedFolders = @()

# Función para escribir tanto en consola como en archivo
function Write-Report {
    param($Message)
    Write-Host $Message
    Add-Content -Path $reportFile -Value $Message
}

# Limpiar archivo de reporte anterior
if (Test-Path $reportFile) { Remove-Item $reportFile }

Write-Report "=== REPORTE DE ACCESO DENEGADO - $(Get-Date) ==="
Write-Report "Análisis de carpetas y archivos con acceso restringido"
Write-Report ""

# Función para probar acceso a una carpeta
function Test-FolderAccess {
    param($Path)
    try {
        $null = Get-ChildItem -Path $Path -Force -ErrorAction Stop | Select-Object -First 1
        return $true
    }
    catch [System.UnauthorizedAccessException] {
        return $false
    }
    catch {
        return $null
    }
}

# Lista de carpetas críticas del sistema para probar
$systemFolders = @(
    "C:\Windows\System32\config",
    "C:\Windows\System32\drivers",
    "C:\Windows\System32\DriverStore",
    "C:\Windows\WinSxS",
    "C:\Windows\servicing",
    "C:\Windows\Logs",
    "C:\Windows\Panther",
    "C:\ProgramData\Microsoft\Windows\WER",
    "C:\ProgramData\Microsoft\Diagnosis",
    "C:\Users\All Users",
    "C:\Users\Default",
    "C:\Users\Public",
    "C:\System Volume Information",
    "C:\Recovery",
    "C:\PerfLogs",
    "C:\Windows\CSC",
    "C:\Windows\SystemApps",
    "C:\Windows\Temp"
)

Write-Report "=== 1. PROBANDO ACCESO A CARPETAS DEL SISTEMA ==="
foreach ($folder in $systemFolders) {
    if (Test-Path $folder) {
        $access = Test-FolderAccess -Path $folder
        if ($access -eq $false) {
            Write-Report "ACCESO DENEGADO: $folder"
            $accessDeniedFolders += $folder
        } elseif ($access -eq $true) {
            Write-Report "ACCESO PERMITIDO: $folder"
        } else {
            Write-Report "ERROR/NO EXISTE: $folder"
        }
    } else {
        Write-Report "NO EXISTE: $folder"
    }
}

Write-Report ""
Write-Report "=== 2. ANÁLISIS DE CARPETAS PRINCIPALES ==="

# Analizar directorios principales
$rootDirectories = @("C:\Windows", "C:\Program Files", "C:\Program Files (x86)", "C:\ProgramData")

foreach ($rootDir in $rootDirectories) {
    if (Test-Path $rootDir) {
        Write-Report "Analizando: $rootDir"
        try {
            $items = Get-ChildItem -Path $rootDir -Directory -Force -ErrorAction Stop
            foreach ($item in $items) {
                $access = Test-FolderAccess -Path $item.FullName
                if ($access -eq $false) {
                    Write-Report "ACCESO DENEGADO: $($item.FullName)"
                    $accessDeniedFolders += $item.FullName
                }
            }
        }
        catch [System.UnauthorizedAccessException] {
            Write-Report "ACCESO DENEGADO AL DIRECTORIO RAIZ: $rootDir"
            $accessDeniedFolders += $rootDir
        }
        catch {
            Write-Report "ERROR EN: $rootDir - $($_.Exception.Message)"
        }
    }
}

Write-Report ""
Write-Report "=== 3. RESUMEN DE CARPETAS CON ACCESO DENEGADO ==="
if ($accessDeniedFolders.Count -gt 0) {
    Write-Report "Total de carpetas con acceso denegado: $($accessDeniedFolders.Count)"
    Write-Report ""
    Write-Report "Lista completa:"
    $accessDeniedFolders | Sort-Object | ForEach-Object {
        Write-Report "  - $_"
    }
} else {
    Write-Report "No se encontraron carpetas con acceso denegado en el análisis."
}

Write-Report ""
Write-Report "=== REPORTE COMPLETADO ==="
Write-Report "Archivo guardado en: $reportFile"

Write-Host "`nReporte de acceso denegado guardado en: $reportFile"
Write-Host "Total de carpetas con acceso restringido: $($accessDeniedFolders.Count)"