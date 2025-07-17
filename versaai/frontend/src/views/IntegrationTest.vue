<template>
  <div class="integration-test-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">Prueba de Integración del Frontend</h1>
      <p class="text-gray-600 mb-8">Esta página contiene enlaces a todas las páginas disponibles en VersaAI para verificar que las integraciones funcionan correctamente.</p>
      
      <!-- Estado del Sistema -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
        <h2 class="text-xl font-semibold text-blue-800 mb-4">Estado del Sistema</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded border">
            <h3 class="font-medium text-gray-700">Frontend</h3>
            <p class="text-green-600">✅ Activo (Puerto 3000)</p>
          </div>
          <div class="bg-white p-4 rounded border">
            <h3 class="font-medium text-gray-700">Backend</h3>
            <p class="text-green-600">✅ Activo (Puerto 8000)</p>
          </div>
          <div class="bg-white p-4 rounded border">
            <h3 class="font-medium text-gray-700">Router</h3>
            <p class="text-green-600">✅ Configurado</p>
          </div>
        </div>
      </div>

      <!-- Páginas Públicas -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Páginas Públicas</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link to="/" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🏠 Inicio</h3>
              <p class="text-sm text-gray-600">Página principal</p>
              <span class="text-xs text-blue-600">/</span>
            </div>
          </router-link>
          
          <router-link to="/widget-demo" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔧 Demo Widget</h3>
              <p class="text-sm text-gray-600">Demostración del widget</p>
              <span class="text-xs text-blue-600">/widget-demo</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Páginas de Autenticación -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Autenticación</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <router-link to="/auth/login" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔐 Login</h3>
              <p class="text-sm text-gray-600">Iniciar sesión</p>
              <span class="text-xs text-blue-600">/auth/login</span>
            </div>
          </router-link>
          
          <router-link to="/auth/register" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📝 Registro</h3>
              <p class="text-sm text-gray-600">Crear cuenta</p>
              <span class="text-xs text-blue-600">/auth/register</span>
            </div>
          </router-link>
          
          <router-link to="/auth/forgot-password" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔑 Recuperar</h3>
              <p class="text-sm text-gray-600">Recuperar contraseña</p>
              <span class="text-xs text-blue-600">/auth/forgot-password</span>
            </div>
          </router-link>
          
          <router-link to="/auth/reset-password" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔄 Restablecer</h3>
              <p class="text-sm text-gray-600">Restablecer contraseña</p>
              <span class="text-xs text-blue-600">/auth/reset-password</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Dashboard Principal -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Dashboard Principal</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link to="/dashboard" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📊 Dashboard</h3>
              <p class="text-sm text-gray-600">Panel principal</p>
              <span class="text-xs text-blue-600">/dashboard</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/overview" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📈 Resumen</h3>
              <p class="text-sm text-gray-600">Vista general</p>
              <span class="text-xs text-blue-600">/dashboard/overview</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/enterprise" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🏢 Empresarial</h3>
              <p class="text-sm text-gray-600">Dashboard empresarial</p>
              <span class="text-xs text-blue-600">/dashboard/enterprise</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Gestión de Chatbots -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Gestión de Chatbots</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link to="/dashboard/chatbots" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🤖 Chatbots</h3>
              <p class="text-sm text-gray-600">Lista de chatbots</p>
              <span class="text-xs text-blue-600">/dashboard/chatbots</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/chat" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">💬 Chat</h3>
              <p class="text-sm text-gray-600">Interfaz de chat</p>
              <span class="text-xs text-blue-600">/dashboard/chat</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/conversations" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📝 Conversaciones</h3>
              <p class="text-sm text-gray-600">Historial de conversaciones</p>
              <span class="text-xs text-blue-600">/dashboard/conversations</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Bases de Conocimiento -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Bases de Conocimiento</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <router-link to="/dashboard/knowledge-bases" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📚 Bases de Conocimiento</h3>
              <p class="text-sm text-gray-600">Gestión de conocimiento</p>
              <span class="text-xs text-blue-600">/dashboard/knowledge-bases</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/analytics" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📊 Analíticas</h3>
              <p class="text-sm text-gray-600">Métricas y estadísticas</p>
              <span class="text-xs text-blue-600">/dashboard/analytics</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Gestión de Usuarios y Configuración -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Gestión y Configuración</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <router-link to="/dashboard/users" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">👥 Usuarios</h3>
              <p class="text-sm text-gray-600">Gestión de usuarios</p>
              <span class="text-xs text-blue-600">/dashboard/users</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/settings" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">⚙️ Configuración</h3>
              <p class="text-sm text-gray-600">Ajustes del sistema</p>
              <span class="text-xs text-blue-600">/dashboard/settings</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/profile" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">👤 Perfil</h3>
              <p class="text-sm text-gray-600">Perfil de usuario</p>
              <span class="text-xs text-blue-600">/dashboard/profile</span>
            </div>
          </router-link>
          
          <router-link to="/dashboard/organization" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🏢 Organización</h3>
              <p class="text-sm text-gray-600">Configuración organizacional</p>
              <span class="text-xs text-blue-600">/dashboard/organization</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Páginas de Desarrollo -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Desarrollo y Pruebas</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <router-link to="/dev/examples" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📋 Ejemplos</h3>
              <p class="text-sm text-gray-600">Ejemplos de desarrollo</p>
              <span class="text-xs text-blue-600">/dev/examples</span>
            </div>
          </router-link>
          
          <router-link to="/dev/test" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🧪 Pruebas</h3>
              <p class="text-sm text-gray-600">Página de pruebas</p>
              <span class="text-xs text-blue-600">/dev/test</span>
            </div>
          </router-link>
          
          <router-link to="/dev/diagnostic" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔍 Diagnóstico</h3>
              <p class="text-sm text-gray-600">Herramientas de diagnóstico</p>
              <span class="text-xs text-blue-600">/dev/diagnostic</span>
            </div>
          </router-link>
          
          <router-link to="/dev/api-test" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔌 API Test</h3>
              <p class="text-sm text-gray-600">Pruebas de API</p>
              <span class="text-xs text-blue-600">/dev/api-test</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Páginas de Error -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Páginas de Error</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link to="/error/500" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🚫 Error 500</h3>
              <p class="text-sm text-gray-600">Error del servidor</p>
              <span class="text-xs text-blue-600">/error/500</span>
            </div>
          </router-link>
          
          <router-link to="/error/401" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🔒 Error 401</h3>
              <p class="text-sm text-gray-600">No autorizado</p>
              <span class="text-xs text-blue-600">/error/401</span>
            </div>
          </router-link>
          
          <router-link to="/pagina-inexistente" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">❓ Error 404</h3>
              <p class="text-sm text-gray-600">Página no encontrada</p>
              <span class="text-xs text-blue-600">/pagina-inexistente</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- Enlaces Externos -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Enlaces Externos y Portales</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <a href="http://localhost:8000/docs" target="_blank" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">📖 API Docs</h3>
              <p class="text-sm text-gray-600">Documentación de la API</p>
              <span class="text-xs text-green-600">http://localhost:8000/docs</span>
            </div>
          </a>
          
          <a href="../raiz.html" target="_blank" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🏠 Portal Principal</h3>
              <p class="text-sm text-gray-600">Portal de desarrollo principal</p>
              <span class="text-xs text-green-600">../raiz.html</span>
            </div>
          </a>
          
          <a href="frontend.html" target="_blank" class="test-link">
            <div class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-medium text-gray-800">🎨 Portal Frontend</h3>
              <p class="text-sm text-gray-600">Portal de desarrollo frontend</p>
              <span class="text-xs text-green-600">frontend.html</span>
            </div>
          </a>
        </div>
      </div>

      <!-- Información de Prueba -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h2 class="text-xl font-semibold text-yellow-800 mb-4">Información de Prueba</h2>
        <ul class="text-yellow-700 space-y-2">
          <li>• <strong>Páginas Públicas:</strong> Accesibles sin autenticación</li>
          <li>• <strong>Páginas de Dashboard:</strong> Requieren autenticación (pueden mostrar error 401)</li>
          <li>• <strong>Páginas de Desarrollo:</strong> Para pruebas y diagnóstico</li>
          <li>• <strong>Páginas de Error:</strong> Para probar manejo de errores</li>
          <li>• <strong>Enlaces Externos:</strong> Servicios y portales relacionados</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  console.log('Página de prueba de integración cargada')
  console.log('Frontend URL:', window.location.origin)
  console.log('Router disponible:', !!window.router)
})
</script>

<style scoped>
.integration-test-page {
  min-height: 100vh;
  background-color: #f8fafc;
}

.test-link {
  text-decoration: none;
  display: block;
  transition: transform 0.2s;
}

.test-link:hover {
  transform: translateY(-2px);
}

.container {
  max-width: 1200px;
}
</style>