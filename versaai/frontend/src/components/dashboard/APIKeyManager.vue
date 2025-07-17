<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Gestión de API Keys</h3>
          <p class="text-sm text-gray-600 mt-1">Administra las claves de API para integraciones externas</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Tabs -->
      <div class="mt-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeTab = 'list'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'list'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              API Keys ({{ apiKeys.length }})
            </button>
            <button
              @click="activeTab = 'create'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'create'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ editingKey ? 'Editar API Key' : 'Nueva API Key' }}
            </button>
            <button
              @click="activeTab = 'usage'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'usage'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Uso y Estadísticas
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- API Keys List -->
        <div v-if="activeTab === 'list'" class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="relative">
                <MagnifyingGlassIcon class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar API keys..."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select
                v-model="filterStatus"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los estados</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="expired">Expirado</option>
              </select>
            </div>
            
            <button
              @click="activeTab = 'create'"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <PlusIcon class="h-5 w-5" />
              <span>Nueva API Key</span>
            </button>
          </div>

          <div v-if="filteredApiKeys.length === 0" class="text-center py-12">
            <KeyIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No hay API keys configuradas</h3>
            <p class="mt-1 text-sm text-gray-500">Comienza creando tu primera API key.</p>
            <div class="mt-6">
              <button
                @click="activeTab = 'create'"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon class="-ml-1 mr-2 h-5 w-5" />
                Nueva API Key
              </button>
            </div>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="apiKey in filteredApiKeys"
              :key="apiKey.id"
              class="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h4 class="text-lg font-medium text-gray-900">{{ apiKey.name }}</h4>
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      apiKey.status === 'active' ? 'bg-green-100 text-green-800' :
                      apiKey.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                      'bg-red-100 text-red-800'
                    ]">
                      {{ getStatusLabel(apiKey.status) }}
                    </span>
                  </div>
                  
                  <p class="text-sm text-gray-600 mt-1">{{ apiKey.description }}</p>
                  
                  <div class="mt-4 space-y-3">
                    <!-- API Key Display -->
                    <div class="flex items-center space-x-3">
                      <span class="text-sm font-medium text-gray-700">API Key:</span>
                      <div class="flex items-center space-x-2 flex-1">
                        <code class="bg-gray-100 px-3 py-1 rounded font-mono text-sm flex-1">
                          {{ showKey[apiKey.id] ? apiKey.key : maskApiKey(apiKey.key) }}
                        </code>
                        <button
                          @click="toggleKeyVisibility(apiKey.id)"
                          class="text-gray-500 hover:text-gray-700"
                        >
                          <EyeIcon v-if="!showKey[apiKey.id]" class="h-4 w-4" />
                          <EyeSlashIcon v-else class="h-4 w-4" />
                        </button>
                        <button
                          @click="copyToClipboard(apiKey.key)"
                          class="text-gray-500 hover:text-gray-700"
                        >
                          <ClipboardDocumentIcon class="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                    
                    <!-- Permissions -->
                    <div class="flex items-center space-x-3">
                      <span class="text-sm font-medium text-gray-700">Permisos:</span>
                      <div class="flex flex-wrap gap-1">
                        <span
                          v-for="permission in apiKey.permissions"
                          :key="permission"
                          class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          {{ getPermissionLabel(permission) }}
                        </span>
                      </div>
                    </div>
                    
                    <!-- Usage Stats -->
                    <div class="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span class="text-gray-500">Último uso:</span>
                        <div class="font-medium">{{ formatDate(apiKey.lastUsed) }}</div>
                      </div>
                      <div>
                        <span class="text-gray-500">Requests hoy:</span>
                        <div class="font-medium">{{ apiKey.requestsToday.toLocaleString() }}</div>
                      </div>
                      <div>
                        <span class="text-gray-500">Límite:</span>
                        <div class="font-medium">
                          {{ apiKey.rateLimit ? `${apiKey.rateLimit}/hora` : 'Sin límite' }}
                        </div>
                      </div>
                    </div>
                    
                    <!-- Expiration -->
                    <div v-if="apiKey.expiresAt" class="flex items-center space-x-2">
                      <ClockIcon class="h-4 w-4 text-gray-400" />
                      <span class="text-sm text-gray-600">
                        Expira: {{ formatDate(apiKey.expiresAt) }}
                        <span :class="[
                          'ml-2 text-xs',
                          isExpiringSoon(apiKey.expiresAt) ? 'text-orange-600' : 'text-gray-500'
                        ]">
                          ({{ getTimeUntilExpiration(apiKey.expiresAt) }})
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- Actions -->
                <div class="flex items-center space-x-2">
                  <button
                    @click="regenerateKey(apiKey)"
                    class="text-blue-600 hover:text-blue-800 text-sm p-2 rounded-lg hover:bg-blue-50"
                    title="Regenerar clave"
                  >
                    <ArrowPathIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="editApiKey(apiKey)"
                    class="text-gray-600 hover:text-gray-800 text-sm p-2 rounded-lg hover:bg-gray-50"
                    title="Editar"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="toggleApiKey(apiKey)"
                    :class="[
                      'text-sm p-2 rounded-lg',
                      apiKey.status === 'active' 
                        ? 'text-red-600 hover:text-red-800 hover:bg-red-50' 
                        : 'text-green-600 hover:text-green-800 hover:bg-green-50'
                    ]"
                    :title="apiKey.status === 'active' ? 'Desactivar' : 'Activar'"
                  >
                    <PowerIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="deleteApiKey(apiKey)"
                    class="text-red-600 hover:text-red-800 text-sm p-2 rounded-lg hover:bg-red-50"
                    title="Eliminar"
                  >
                    <TrashIcon class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Create/Edit API Key -->
        <div v-if="activeTab === 'create'" class="space-y-6">
          <form @submit.prevent="saveApiKey" class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="key-name" class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre de la API Key
                </label>
                <input
                  id="key-name"
                  v-model="keyForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Mi API Key"
                />
              </div>
              
              <div>
                <label for="key-rate-limit" class="block text-sm font-medium text-gray-700 mb-2">
                  Límite de Requests (por hora)
                </label>
                <input
                  id="key-rate-limit"
                  v-model.number="keyForm.rateLimit"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="1000 (0 = sin límite)"
                />
              </div>
            </div>
            
            <div>
              <label for="key-description" class="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                id="key-description"
                v-model="keyForm.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Descripción de la API key..."
              ></textarea>
            </div>

            <!-- Permissions -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">
                Permisos
              </label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label
                  v-for="permission in availablePermissions"
                  :key="permission.value"
                  class="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                >
                  <input
                    v-model="keyForm.permissions"
                    :value="permission.value"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ permission.label }}</div>
                    <div class="text-xs text-gray-500">{{ permission.description }}</div>
                  </div>
                </label>
              </div>
            </div>

            <!-- Expiration -->
            <div>
              <label class="flex items-center space-x-3 mb-4">
                <input
                  v-model="keyForm.hasExpiration"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span class="text-sm font-medium text-gray-700">Configurar fecha de expiración</span>
              </label>
              
              <div v-if="keyForm.hasExpiration" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="key-expires" class="block text-sm font-medium text-gray-700 mb-2">
                    Fecha de Expiración
                  </label>
                  <input
                    id="key-expires"
                    v-model="keyForm.expiresAt"
                    type="datetime-local"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Presets de Expiración
                  </label>
                  <div class="flex space-x-2">
                    <button
                      type="button"
                      @click="setExpirationPreset(30)"
                      class="px-3 py-1 text-xs border border-gray-300 rounded hover:bg-gray-50"
                    >
                      30 días
                    </button>
                    <button
                      type="button"
                      @click="setExpirationPreset(90)"
                      class="px-3 py-1 text-xs border border-gray-300 rounded hover:bg-gray-50"
                    >
                      90 días
                    </button>
                    <button
                      type="button"
                      @click="setExpirationPreset(365)"
                      class="px-3 py-1 text-xs border border-gray-300 rounded hover:bg-gray-50"
                    >
                      1 año
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
              <button
                type="button"
                @click="resetForm"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="!isFormValid"
                class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ editingKey ? 'Actualizar' : 'Crear' }} API Key
              </button>
            </div>
          </form>
        </div>

        <!-- Usage Statistics -->
        <div v-if="activeTab === 'usage'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-blue-50 rounded-lg p-6">
              <div class="flex items-center">
                <div class="p-2 bg-blue-100 rounded-lg">
                  <ChartBarIcon class="h-6 w-6 text-blue-600" />
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600">Requests Hoy</p>
                  <p class="text-2xl font-bold text-gray-900">{{ totalRequestsToday.toLocaleString() }}</p>
                </div>
              </div>
            </div>
            
            <div class="bg-green-50 rounded-lg p-6">
              <div class="flex items-center">
                <div class="p-2 bg-green-100 rounded-lg">
                  <CheckCircleIcon class="h-6 w-6 text-green-600" />
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600">Requests Exitosos</p>
                  <p class="text-2xl font-bold text-gray-900">{{ successfulRequests.toLocaleString() }}</p>
                </div>
              </div>
            </div>
            
            <div class="bg-red-50 rounded-lg p-6">
              <div class="flex items-center">
                <div class="p-2 bg-red-100 rounded-lg">
                  <ExclamationTriangleIcon class="h-6 w-6 text-red-600" />
                </div>
                <div class="ml-4">
                  <p class="text-sm font-medium text-gray-600">Requests Fallidos</p>
                  <p class="text-2xl font-bold text-gray-900">{{ failedRequests.toLocaleString() }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Usage Chart Placeholder -->
          <div class="bg-white rounded-lg border border-gray-200 p-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Uso de API en los últimos 7 días</h4>
            <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
              <p class="text-gray-500">Gráfico de uso de API (implementar con Chart.js)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  PlusIcon,
  KeyIcon,
  MagnifyingGlassIcon,
  EyeIcon,
  EyeSlashIcon,
  ClipboardDocumentIcon,
  ClockIcon,
  ArrowPathIcon,
  PencilIcon,
  PowerIcon,
  TrashIcon,
  ChartBarIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const activeTab = ref('list')
const searchQuery = ref('')
const filterStatus = ref('')
const editingKey = ref(null)
const showKey = ref({})

const apiKeys = ref([
  {
    id: 1,
    name: 'Production API',
    description: 'Clave principal para el entorno de producción',
    key: 'vsa_live_1234567890abcdef1234567890abcdef',
    permissions: ['chatbots.read', 'chatbots.write', 'conversations.read', 'analytics.read'],
    status: 'active',
    rateLimit: 1000,
    requestsToday: 847,
    lastUsed: new Date('2024-01-15T10:30:00'),
    expiresAt: new Date('2024-12-31T23:59:59'),
    createdAt: new Date('2024-01-01T00:00:00')
  },
  {
    id: 2,
    name: 'Development API',
    description: 'Clave para desarrollo y testing',
    key: 'vsa_test_abcdef1234567890abcdef1234567890',
    permissions: ['chatbots.read', 'conversations.read'],
    status: 'active',
    rateLimit: 100,
    requestsToday: 23,
    lastUsed: new Date('2024-01-15T09:15:00'),
    expiresAt: null,
    createdAt: new Date('2024-01-10T00:00:00')
  },
  {
    id: 3,
    name: 'Analytics Only',
    description: 'Acceso de solo lectura para analytics',
    key: 'vsa_analytics_fedcba0987654321fedcba0987654321',
    permissions: ['analytics.read'],
    status: 'inactive',
    rateLimit: 500,
    requestsToday: 0,
    lastUsed: new Date('2024-01-10T15:20:00'),
    expiresAt: new Date('2024-02-15T23:59:59'),
    createdAt: new Date('2024-01-05T00:00:00')
  }
])

const keyForm = ref({
  name: '',
  description: '',
  permissions: [],
  rateLimit: 1000,
  hasExpiration: false,
  expiresAt: ''
})

const availablePermissions = ref([
  {
    value: 'chatbots.read',
    label: 'Leer Chatbots',
    description: 'Ver información de chatbots'
  },
  {
    value: 'chatbots.write',
    label: 'Escribir Chatbots',
    description: 'Crear y modificar chatbots'
  },
  {
    value: 'conversations.read',
    label: 'Leer Conversaciones',
    description: 'Acceder a conversaciones'
  },
  {
    value: 'conversations.write',
    label: 'Escribir Conversaciones',
    description: 'Crear y modificar conversaciones'
  },
  {
    value: 'analytics.read',
    label: 'Leer Analytics',
    description: 'Acceder a métricas y reportes'
  },
  {
    value: 'users.read',
    label: 'Leer Usuarios',
    description: 'Ver información de usuarios'
  },
  {
    value: 'users.write',
    label: 'Escribir Usuarios',
    description: 'Gestionar usuarios'
  },
  {
    value: 'admin',
    label: 'Administrador',
    description: 'Acceso completo al sistema'
  }
])

// Computed properties
const filteredApiKeys = computed(() => {
  return apiKeys.value.filter(key => {
    const matchesSearch = key.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         key.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = !filterStatus.value || key.status === filterStatus.value
    
    return matchesSearch && matchesStatus
  })
})

const isFormValid = computed(() => {
  return keyForm.value.name && keyForm.value.permissions.length > 0
})

const totalRequestsToday = computed(() => {
  return apiKeys.value.reduce((total, key) => total + key.requestsToday, 0)
})

const successfulRequests = computed(() => {
  return Math.floor(totalRequestsToday.value * 0.95) // 95% success rate
})

const failedRequests = computed(() => {
  return totalRequestsToday.value - successfulRequests.value
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const toggleKeyVisibility = (keyId) => {
  showKey.value[keyId] = !showKey.value[keyId]
}

const maskApiKey = (key) => {
  if (key.length <= 8) return key
  return key.substring(0, 8) + '*'.repeat(key.length - 12) + key.substring(key.length - 4)
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    // Mostrar notificación de éxito
    console.log('API key copiada al portapapeles')
  } catch (err) {
    console.error('Error al copiar:', err)
  }
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    expired: 'Expirado'
  }
  return labels[status] || status
}

const getPermissionLabel = (permission) => {
  const found = availablePermissions.value.find(p => p.value === permission)
  return found ? found.label : permission
}

const formatDate = (date) => {
  if (!date) return 'Nunca'
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const isExpiringSoon = (expiresAt) => {
  if (!expiresAt) return false
  const now = new Date()
  const expiration = new Date(expiresAt)
  const daysUntilExpiration = (expiration - now) / (1000 * 60 * 60 * 24)
  return daysUntilExpiration <= 30
}

const getTimeUntilExpiration = (expiresAt) => {
  if (!expiresAt) return ''
  const now = new Date()
  const expiration = new Date(expiresAt)
  const diff = expiration - now
  
  if (diff <= 0) return 'Expirado'
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days > 0) return `${days} días`
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  return `${hours} horas`
}

const editApiKey = (apiKey) => {
  editingKey.value = apiKey
  keyForm.value = {
    name: apiKey.name,
    description: apiKey.description,
    permissions: [...apiKey.permissions],
    rateLimit: apiKey.rateLimit,
    hasExpiration: !!apiKey.expiresAt,
    expiresAt: apiKey.expiresAt ? apiKey.expiresAt.toISOString().slice(0, 16) : ''
  }
  activeTab.value = 'create'
}

const resetForm = () => {
  editingKey.value = null
  keyForm.value = {
    name: '',
    description: '',
    permissions: [],
    rateLimit: 1000,
    hasExpiration: false,
    expiresAt: ''
  }
  activeTab.value = 'list'
}

const generateApiKey = () => {
  const prefix = 'vsa_live_'
  const chars = 'abcdef0123456789'
  let result = prefix
  for (let i = 0; i < 32; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

const saveApiKey = () => {
  const apiKeyData = {
    ...keyForm.value,
    expiresAt: keyForm.value.hasExpiration && keyForm.value.expiresAt 
      ? new Date(keyForm.value.expiresAt) 
      : null
  }
  
  if (editingKey.value) {
    // Update existing key
    const index = apiKeys.value.findIndex(k => k.id === editingKey.value.id)
    if (index > -1) {
      apiKeys.value[index] = {
        ...apiKeys.value[index],
        ...apiKeyData
      }
    }
  } else {
    // Create new key
    const newKey = {
      ...apiKeyData,
      id: Date.now(),
      key: generateApiKey(),
      status: 'active',
      requestsToday: 0,
      lastUsed: null,
      createdAt: new Date()
    }
    apiKeys.value.push(newKey)
  }
  
  emit('save', apiKeyData)
  resetForm()
}

const regenerateKey = (apiKey) => {
  if (confirm(`¿Estás seguro de que quieres regenerar la clave "${apiKey.name}"? La clave actual dejará de funcionar.`)) {
    apiKey.key = generateApiKey()
    console.log('API key regenerada:', apiKey.name)
  }
}

const toggleApiKey = (apiKey) => {
  apiKey.status = apiKey.status === 'active' ? 'inactive' : 'active'
}

const deleteApiKey = (apiKey) => {
  if (confirm(`¿Estás seguro de que quieres eliminar la API key "${apiKey.name}"?`)) {
    const index = apiKeys.value.findIndex(k => k.id === apiKey.id)
    if (index > -1) {
      apiKeys.value.splice(index, 1)
    }
  }
}

const setExpirationPreset = (days) => {
  const date = new Date()
  date.setDate(date.getDate() + days)
  keyForm.value.expiresAt = date.toISOString().slice(0, 16)
}

onMounted(() => {
  // Initialize show/hide state for all keys
  apiKeys.value.forEach(key => {
    showKey.value[key.id] = false
  })
})
</script>