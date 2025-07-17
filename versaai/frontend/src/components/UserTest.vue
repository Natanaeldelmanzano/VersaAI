<template>
  <div class="user-test p-6 bg-white rounded-lg shadow-lg max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">🧪 Prueba de Integración - Sistema de Usuarios</h2>
    
    <!-- Estado del Sistema -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">📊 Estado del Sistema</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 border rounded-lg">
          <div class="flex items-center">
            <div :class="backendStatus ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                 class="px-2 py-1 rounded-full text-sm font-medium">
              {{ backendStatus ? '✅ Backend Conectado' : '❌ Backend Desconectado' }}
            </div>
          </div>
          <p class="text-sm text-gray-600 mt-2">API: http://localhost:8000</p>
        </div>
        <div class="p-4 border rounded-lg">
          <div class="flex items-center">
            <div class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm font-medium">
              🌐 Frontend Activo
            </div>
          </div>
          <p class="text-sm text-gray-600 mt-2">Puerto: 3000</p>
        </div>
      </div>
    </div>

    <!-- Pruebas de Autenticación -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">🔐 Pruebas de Autenticación</h3>
      <div class="space-y-3">
        <button 
          @click="testRegister" 
          :disabled="loading"
          class="w-full md:w-auto bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {{ loading ? 'Procesando...' : '👤 Probar Registro' }}
        </button>
        <button 
          @click="testLogin" 
          :disabled="loading"
          class="w-full md:w-auto bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors ml-0 md:ml-3"
        >
          {{ loading ? 'Procesando...' : '🔑 Probar Login' }}
        </button>
        <button 
          @click="testProtectedEndpoint" 
          :disabled="loading || !authToken"
          class="w-full md:w-auto bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors ml-0 md:ml-3"
        >
          {{ loading ? 'Procesando...' : '🛡️ Probar Endpoint Protegido' }}
        </button>
      </div>
    </div>

    <!-- Gestión de Usuarios -->
    <div class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">👥 Gestión de Usuarios</h3>
      <div class="space-y-3">
        <button 
          @click="fetchUsers" 
          :disabled="loading || !authToken"
          class="w-full md:w-auto bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {{ loading ? 'Cargando...' : '📋 Listar Usuarios' }}
        </button>
        <button 
          @click="getUserStats" 
          :disabled="loading || !authToken"
          class="w-full md:w-auto bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors ml-0 md:ml-3"
        >
          {{ loading ? 'Cargando...' : '📊 Estadísticas' }}
        </button>
      </div>
    </div>

    <!-- Resultados -->
    <div v-if="results.length > 0" class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">📋 Resultados de Pruebas</h3>
      <div class="space-y-2 max-h-96 overflow-y-auto">
        <div 
          v-for="(result, index) in results" 
          :key="index"
          :class="result.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'"
          class="p-3 border rounded-lg"
        >
          <div class="flex items-start">
            <span class="text-lg mr-2">{{ result.success ? '✅' : '❌' }}</span>
            <div class="flex-1">
              <p class="font-medium text-gray-900">{{ result.action }}</p>
              <p class="text-sm text-gray-600 mt-1">{{ result.message }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ result.timestamp }}</p>
            </div>
          </div>
        </div>
      </div>
      <button 
        @click="clearResults" 
        class="mt-3 text-sm text-gray-600 hover:text-gray-800 underline"
      >
        Limpiar resultados
      </button>
    </div>

    <!-- Datos de Usuario Actual -->
    <div v-if="currentUser" class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">👤 Usuario Actual</h3>
      <div class="bg-gray-50 p-4 rounded-lg">
        <pre class="text-sm text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(currentUser, null, 2) }}</pre>
      </div>
    </div>

    <!-- Lista de Usuarios -->
    <div v-if="users.length > 0" class="mb-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">👥 Lista de Usuarios ({{ users.length }})</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">ID</th>
              <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Nombre</th>
              <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Email</th>
              <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Rol</th>
              <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Estado</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="px-4 py-2 text-sm text-gray-900">{{ user.id }}</td>
              <td class="px-4 py-2 text-sm text-gray-900">{{ user.full_name || user.name }}</td>
              <td class="px-4 py-2 text-sm text-gray-600">{{ user.email }}</td>
              <td class="px-4 py-2 text-sm">
                <span :class="getRoleColor(user.role)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-4 py-2 text-sm">
                <span :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                      class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ user.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Próximas Acciones -->
    <div class="bg-blue-50 p-4 rounded-lg">
      <h3 class="text-lg font-semibold text-blue-900 mb-3">🎯 Próximas Acciones del Plan</h3>
      <ul class="space-y-2 text-sm text-blue-800">
        <li>✅ Backend FastAPI ejecutándose</li>
        <li>✅ Frontend Vue.js ejecutándose</li>
        <li>✅ Sistema de autenticación básico</li>
        <li>✅ CRUD de usuarios implementado</li>
        <li>🔄 Implementar sistema de organizaciones</li>
        <li>🔄 Motor de chatbots con Groq AI</li>
        <li>🔄 Interface de chat en tiempo real</li>
        <li>🔄 Dashboard con métricas avanzadas</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Estado reactivo
const loading = ref(false)
const backendStatus = ref(false)
const authToken = ref(localStorage.getItem('access_token'))
const currentUser = ref(null)
const users = ref([])
const results = ref([])

// Configuración de axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000
})

// Interceptor para agregar token
api.interceptors.request.use(config => {
  if (authToken.value) {
    config.headers.Authorization = `Bearer ${authToken.value}`
  }
  return config
})

// Funciones de utilidad
const addResult = (action, success, message) => {
  results.value.unshift({
    action,
    success,
    message,
    timestamp: new Date().toLocaleTimeString()
  })
  // Mantener solo los últimos 10 resultados
  if (results.value.length > 10) {
    results.value = results.value.slice(0, 10)
  }
}

const clearResults = () => {
  results.value = []
}

const getRoleColor = (role) => {
  const colors = {
    'super_admin': 'bg-purple-100 text-purple-800',
    'org_admin': 'bg-blue-100 text-blue-800',
    'user': 'bg-green-100 text-green-800',
    'viewer': 'bg-gray-100 text-gray-800'
  }
  return colors[role] || 'bg-gray-100 text-gray-800'
}

// Verificar estado del backend
const checkBackendStatus = async () => {
  try {
    const response = await api.get('/health')
    backendStatus.value = response.status === 200
    addResult('Verificación Backend', true, 'Backend conectado correctamente')
  } catch (error) {
    backendStatus.value = false
    addResult('Verificación Backend', false, `Error: ${error.message}`)
  }
}

// Probar registro de usuario
const testRegister = async () => {
  loading.value = true
  try {
    const userData = {
      email: 'test@versaai.com',
      password: 'TestPassword123!',
      full_name: 'Usuario de Prueba VersaAI',
      username: 'testuser'
    }
    
    const response = await api.post('/auth/register', userData)
    addResult('Registro Usuario', true, `Usuario registrado: ${response.data.email}`)
  } catch (error) {
    const message = error.response?.data?.detail || error.message
    if (message.includes('already registered')) {
      addResult('Registro Usuario', true, 'Usuario ya existe, continuando...')
    } else {
      addResult('Registro Usuario', false, `Error: ${message}`)
    }
  } finally {
    loading.value = false
  }
}

// Probar login
const testLogin = async () => {
  loading.value = true
  try {
    const loginData = {
      email: 'test@versaai.com',
      password: 'TestPassword123!'
    }
    
    const response = await api.post('/auth/login', loginData)
    authToken.value = response.data.access_token
    localStorage.setItem('access_token', authToken.value)
    addResult('Login Usuario', true, 'Login exitoso, token guardado')
  } catch (error) {
    const message = error.response?.data?.detail || error.message
    addResult('Login Usuario', false, `Error: ${message}`)
  } finally {
    loading.value = false
  }
}

// Probar endpoint protegido
const testProtectedEndpoint = async () => {
  loading.value = true
  try {
    const response = await api.get('/users/me')
    currentUser.value = response.data
    addResult('Endpoint Protegido', true, `Datos obtenidos: ${response.data.email}`)
  } catch (error) {
    const message = error.response?.data?.detail || error.message
    addResult('Endpoint Protegido', false, `Error: ${message}`)
  } finally {
    loading.value = false
  }
}

// Obtener lista de usuarios
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await api.get('/users/')
    users.value = response.data
    addResult('Listar Usuarios', true, `${response.data.length} usuarios obtenidos`)
  } catch (error) {
    const message = error.response?.data?.detail || error.message
    addResult('Listar Usuarios', false, `Error: ${message}`)
  } finally {
    loading.value = false
  }
}

// Obtener estadísticas
const getUserStats = async () => {
  loading.value = true
  try {
    const response = await api.get('/users/stats/overview')
    addResult('Estadísticas', true, `Total: ${response.data.total_users}, Activos: ${response.data.active_users}`)
  } catch (error) {
    const message = error.response?.data?.detail || error.message
    addResult('Estadísticas', false, `Error: ${message}`)
  } finally {
    loading.value = false
  }
}

// Inicialización
onMounted(async () => {
  await checkBackendStatus()
  if (authToken.value) {
    await testProtectedEndpoint()
  }
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
.user-test {
  font-family: 'Inter', sans-serif;
}
</style>