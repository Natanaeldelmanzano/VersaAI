# Script para registrar un usuario de prueba
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    email = "test@example.com"
    password = "testpassword123"
    full_name = "Usuario de Prueba"
} | ConvertTo-Json

try {
    Write-Host "Registrando usuario de prueba..."
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method POST -Headers $headers -Body $body
    Write-Host "Usuario registrado exitosamente:"
    Write-Host ($response | ConvertTo-Json -Depth 3)
} catch {
    Write-Host "Error al registrar usuario:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Respuesta del servidor: $responseBody"
    }
}