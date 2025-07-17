# Script para probar la conexión al servidor
try {
    Write-Host "Probando conexión al servidor..."
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 10
    Write-Host "Conexión exitosa:"
    Write-Host ($response | ConvertTo-Json)
} catch {
    Write-Host "Error de conexión:"
    Write-Host $_.Exception.Message
    
    # Intentar con 127.0.0.1 en lugar de localhost
    try {
        Write-Host "Probando con 127.0.0.1..."
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method GET -TimeoutSec 10
        Write-Host "Conexión exitosa con 127.0.0.1:"
        Write-Host ($response | ConvertTo-Json)
    } catch {
        Write-Host "Error también con 127.0.0.1:"
        Write-Host $_.Exception.Message
    }
}