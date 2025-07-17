<template>
  <div class="security-center">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Centro de Seguridad
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        Gestiona la seguridad y configuraciones de acceso de tu organización
      </p>
    </div>

    <!-- Security Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
            <ShieldCheckIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Estado de Seguridad</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">Seguro</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
            <KeyIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Claves API Activas</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ apiKeys.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
            <ExclamationTriangleIcon class="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Alertas de Seguridad</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ securityAlerts.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
            <UserGroupIcon class="h-6 w-6 text-purple-600 dark:text-purple-400" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Usuarios Activos</p>
            <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ activeUsers }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Security Sections -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- API Keys Management -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Gestión de Claves API</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Administra las claves de acceso a la API
          </p>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div v-for="key in apiKeys" :key="key.id" class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ key.name }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Creada: {{ formatDate(key.created_at) }}</p>
                <p class="text-sm text-gray-600 dark:text-gray-400">Último uso: {{ formatDate(key.last_used) }}</p>
              </div>
              <div class="flex space-x-2">
                <button class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
                  <EyeIcon class="h-5 w-5" />
                </button>
                <button class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300">
                  <TrashIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
          <button class="mt-4 w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            Generar Nueva Clave API
          </button>
        </div>
      </div>

      <!-- Security Settings -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Configuración de Seguridad</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Ajusta las políticas de seguridad
          </p>
        </div>
        <div class="p-6 space-y-6">
          <!-- Two-Factor Authentication -->
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Autenticación de Dos Factores</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Añade una capa extra de seguridad</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="twoFactorEnabled" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
            </label>
          </div>

          <!-- Session Timeout -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Tiempo de Sesión</h3>
            <select v-model="sessionTimeout" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
              <option value="30">30 minutos</option>
              <option value="60">1 hora</option>
              <option value="120">2 horas</option>
              <option value="480">8 horas</option>
              <option value="1440">24 horas</option>
            </select>
          </div>

          <!-- IP Whitelist -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Lista Blanca de IPs</h3>
            <div class="space-y-2">
              <div v-for="(ip, index) in ipWhitelist" :key="index" class="flex items-center space-x-2">
                <input 
                  v-model="ipWhitelist[index]" 
                  type="text" 
                  placeholder="192.168.1.1" 
                  class="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                <button @click="removeIP(index)" class="text-red-600 hover:text-red-800">
                  <XMarkIcon class="h-5 w-5" />
                </button>
              </div>
              <button @click="addIP" class="text-blue-600 hover:text-blue-800 text-sm">
                + Añadir IP
              </button>
            </div>
          </div>

          <button class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
            Guardar Configuración
          </button>
        </div>
      </div>
    </div>

    <!-- Security Alerts -->
    <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Alertas de Seguridad</h2>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Eventos de seguridad recientes
        </p>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div v-for="alert in securityAlerts" :key="alert.id" class="flex items-start space-x-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div class="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
              <ExclamationTriangleIcon class="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div class="flex-1">
              <h3 class="font-medium text-gray-900 dark:text-white">{{ alert.title }}</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ alert.description }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-500 mt-2">{{ formatDate(alert.timestamp) }}</p>
            </div>
            <button class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  ShieldCheckIcon,
  KeyIcon,
  ExclamationTriangleIcon,
  UserGroupIcon,
  EyeIcon,
  TrashIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Reactive data
const apiKeys = ref([
  {
    id: 1,
    name: 'Producción API',
    created_at: '2024-01-15T10:00:00Z',
    last_used: '2024-01-20T14:30:00Z'
  },
  {
    id: 2,
    name: 'Desarrollo API',
    created_at: '2024-01-10T09:00:00Z',
    last_used: '2024-01-19T16:45:00Z'
  }
])

const securityAlerts = ref([
  {
    id: 1,
    title: 'Intento de acceso fallido',
    description: 'Se detectaron múltiples intentos de acceso fallidos desde la IP 192.168.1.100',
    timestamp: '2024-01-20T15:30:00Z'
  },
  {
    id: 2,
    title: 'Nueva clave API generada',
    description: 'Se generó una nueva clave API para el usuario admin@empresa.com',
    timestamp: '2024-01-20T12:15:00Z'
  }
])

const activeUsers = ref(24)
const twoFactorEnabled = ref(true)
const sessionTimeout = ref(60)
const ipWhitelist = ref(['192.168.1.0/24', '10.0.0.0/8'])

// Methods
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const addIP = () => {
  ipWhitelist.value.push('')
}

const removeIP = (index) => {
  ipWhitelist.value.splice(index, 1)
}

onMounted(() => {
  // Load security data
  console.log('Security Center loaded')
})
</script>

<style scoped>
.security-center {
  @apply p-6;
}
</style>