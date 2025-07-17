# Pruebas de Conexión Chat - API

## Estado Actual

✅ **Backend**: Funcionando en http://localhost:8000
✅ **Frontend**: Funcionando en http://localhost:3000
✅ **Chat modificado**: Conectado a la API real

## Cambios Realizados

### 1. Modificación del componente Chat.vue
- ✅ Importado el store de conversaciones
- ✅ Reemplazadas las funciones simuladas por llamadas reales a la API
- ✅ Implementada creación automática de conversaciones
- ✅ Integrado el manejo de errores con toast notifications

### 2. Configuración de Axios
- ✅ Actualizado el store para usar la instancia configurada de axios
- ✅ Configurado baseURL: http://localhost:8000
- ✅ Interceptores para logging y manejo de errores

## Endpoints Utilizados

### Conversaciones
- `GET /api/v1/conversations/` - Listar conversaciones
- `POST /api/v1/conversations/` - Crear nueva conversación
- `GET /api/v1/conversations/{id}/messages` - Obtener mensajes
- `POST /api/v1/conversations/chat` - Enviar mensaje y recibir respuesta IA

## Pasos para Probar

### 1. Verificar Servicios
```bash
# Backend debe estar corriendo en:
http://localhost:8000

# Frontend debe estar corriendo en:
http://localhost:3000
```

### 2. Probar Chat
1. Abrir http://localhost:3000/chat
2. Escribir un mensaje en el campo de texto
3. Presionar Enter o hacer clic en enviar
4. Verificar que:
   - Se crea una nueva conversación automáticamente
   - El mensaje del usuario aparece inmediatamente
   - Se muestra el indicador de "escribiendo"
   - Llega la respuesta de la IA
   - La conversación aparece en la lista lateral

### 3. Verificar en Consola del Navegador
- Abrir DevTools (F12)
- Ir a la pestaña Console
- Buscar logs de las peticiones API:
  ```
  🔄 API Request: POST /api/v1/conversations/chat
  ✅ API Response: POST /api/v1/conversations/chat
  ```

### 4. Verificar en Network Tab
- Ir a la pestaña Network en DevTools
- Enviar un mensaje
- Verificar que aparecen las peticiones:
  - POST a `/api/v1/conversations/` (si es nueva conversación)
  - POST a `/api/v1/conversations/chat`
  - GET a `/api/v1/conversations/{id}/messages`

## Posibles Problemas y Soluciones

### Error de CORS
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```
**Solución**: Verificar configuración CORS en el backend

### Error 404 - Endpoint no encontrado
```
404 Not Found
```
**Solución**: Verificar que el backend esté corriendo y los endpoints estén disponibles

### Error de conexión
```
Network Error
```
**Solución**: Verificar que ambos servicios estén corriendo en los puertos correctos

### Error de chatbot no encontrado
```
404 Chatbot not found or inactive
```
**Solución**: Verificar que existe un chatbot con ID 1 en la base de datos

## Funcionalidades Implementadas

✅ **Envío de mensajes**: Los mensajes se envían al backend real
✅ **Respuestas de IA**: Se reciben respuestas generadas por el servicio de IA
✅ **Historial de conversaciones**: Se cargan conversaciones existentes
✅ **Creación automática**: Se crean nuevas conversaciones automáticamente
✅ **Manejo de errores**: Notificaciones toast para errores
✅ **Indicador de escritura**: Muestra cuando la IA está procesando
✅ **Actualización en tiempo real**: La lista de conversaciones se actualiza

## Próximos Pasos

1. **Probar diferentes tipos de mensajes**
2. **Verificar el manejo de conversaciones múltiples**
3. **Probar la funcionalidad de historial**
4. **Verificar la persistencia de datos**
5. **Probar casos de error (backend desconectado, etc.)**

---

**Fecha**: $(Get-Date)
**Estado**: ✅ Listo para pruebas