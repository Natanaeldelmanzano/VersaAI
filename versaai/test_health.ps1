try {
    Write-Host "Probando conexión al servidor..."
    $response = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method GET -TimeoutSec 10
    Write-Host "Servidor respondiendo correctamente:"
    $response | ConvertTo-Json
} catch {
    Write-Host "Error de conexión:"
    Write-Host $_.Exception.Message
    
    # Probar con la documentación de la API
    try {
        Write-Host "Probando endpoint de documentación..."
        $docsResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/docs' -Method GET -TimeoutSec 5
        Write-Host "Documentación accesible - Código de estado: $($docsResponse.StatusCode)"
    } catch {
        Write-Host "Error accediendo a documentación: $($_.Exception.Message)"
    }
}