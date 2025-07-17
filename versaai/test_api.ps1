$headers = @{'Content-Type' = 'application/json'}
$body = Get-Content 'C:\Users\Neizan\Desktop\version max claude\versaai\test_chatbot.json' -Raw
try {
    $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/chatbots/' -Method POST -Body $body -Headers $headers
    Write-Host "Chatbot creado exitosamente:"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error al crear chatbot:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Respuesta del servidor: $responseBody"
    }
}