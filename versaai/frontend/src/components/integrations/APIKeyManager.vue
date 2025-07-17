<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
            <Key class="h-5 w-5 text-purple-600 dark:text-purple-400" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Gestión de API Keys
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Administra las claves de API para tus integraciones
            </p>
          </div>
        </div>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors duration-200"
        >
          <Plus class="h-4 w-4 mr-2" />
          Nueva API Key
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex flex-col sm:flex-row gap-4">
        <div class="flex-1">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar API keys..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
        </div>
        <div class="flex gap-2">
          <select
            v-model="selectedStatus"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activa</option>
            <option value="expired">Expirada</option>
            <option value="revoked">Revocada</option>
          </select>
          <select
            v-model="selectedIntegration"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            <option value="">Todas las integraciones</option>
            <option v-for="integration in availableIntegrations" :key="integration.id" :value="integration.id">
              {{ integration.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- API Keys List -->
    <div class="p-6">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
      </div>
      
      <div v-else-if="filteredAPIKeys.length === 0" class="text-center py-12">
        <Key class="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No hay API keys configuradas
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">
          Crea tu primera API key para comenzar a usar las integraciones
        </p>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors duration-200"
        >
          <Plus class="h-4 w-4 mr-2" />
          Crear API Key
        </button>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="apiKey in filteredAPIKeys"
          :key="apiKey.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ apiKey.name }}
                </h4>
                <span
                  :class="getStatusClasses(apiKey.status)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  <span :class="getStatusDotClasses(apiKey.status)" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
                  {{ getStatusLabel(apiKey.status) }}
                </span>
                <span
                  v-if="isExpiringSoon(apiKey.expiresAt)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
                >
                  <AlertTriangle class="w-3 h-3 mr-1" />
                  Expira pronto
                </span>
              </div>
              
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {{ apiKey.description }}
              </p>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    API Key
                  </label>
                  <div class="flex items-center mt-1">
                    <code class="text-sm bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-900 dark:text-white font-mono flex-1">
                      {{ showFullKey[apiKey.id] ? apiKey.key : maskAPIKey(apiKey.key) }}
                    </code>
                    <button
                      @click="toggleKeyVisibility(apiKey.id)"
                      class="ml-2 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                      :title="showFullKey[apiKey.id] ? 'Ocultar clave' : 'Mostrar clave'"
                    >
                      <Eye v-if="!showFullKey[apiKey.id]" class="h-4 w-4" />
                      <EyeOff v-else class="h-4 w-4" />
                    </button>
                    <button
                      @click="copyToClipboard(apiKey.key)"
                      class="ml-1 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                      title="Copiar clave"
                    >
                      <Copy class="h-4 w-4" />
                    </button>
                  </div>
                </div>
                
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    Permisos
                  </label>
                  <div class="mt-1">
                    <div class="flex flex-wrap gap-1">
                      <span
                        v-for="permission in apiKey.permissions.slice(0, 3)"
                        :key="permission"
                        class="inline-flex items-center px-2 py-1 rounded text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300"
                      >
                        {{ permission }}
                      </span>
                      <span
                        v-if="apiKey.permissions.length > 3"
                        class="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                      >
                        +{{ apiKey.permissions.length - 3 }} más
                      </span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    Expira
                  </label>
                  <p class="text-sm text-gray-900 dark:text-white mt-1">
                    {{ formatExpirationDate(apiKey.expiresAt) }}
                  </p>
                </div>
              </div>
              
              <!-- Usage Stats -->
              <div class="grid grid-cols-3 gap-4 py-3 border-t border-gray-200 dark:border-gray-700">
                <div class="text-center">
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ formatNumber(apiKey.usage.totalRequests) }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Requests</p>
                </div>
                <div class="text-center">
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ formatNumber(apiKey.usage.requestsToday) }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Hoy</p>
                </div>
                <div class="text-center">
                  <p class="text-lg font-semibold" :class="getRateLimitColor(apiKey.usage.rateLimitUsage)">
                    {{ apiKey.usage.rateLimitUsage }}%
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Rate Limit</p>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center space-x-2 ml-4">
              <button
                @click="regenerateAPIKey(apiKey)"
                :disabled="isRegeneratingKey === apiKey.id"
                class="p-2 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors disabled:opacity-50"
                title="Regenerar clave"
              >
                <RotateCcw v-if="isRegeneratingKey !== apiKey.id" class="h-4 w-4" />
                <div v-else class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              </button>
              
              <button
                @click="editAPIKey(apiKey)"
                class="p-2 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 transition-colors"
                title="Editar API key"
              >
                <Edit class="h-4 w-4" />
              </button>
              
              <button
                @click="revokeAPIKey(apiKey)"
                :disabled="isRevokingKey === apiKey.id || apiKey.status === 'revoked'"
                class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors disabled:opacity-50"
                title="Revocar API key"
              >
                <Shield v-if="isRevokingKey !== apiKey.id" class="h-4 w-4" />
                <div v-else class="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
              </button>
              
              <button
                @click="deleteAPIKey(apiKey)"
                class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                title="Eliminar API key"
              >
                <Trash2 class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || showEditModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="closeModals"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ showCreateModal ? 'Crear Nueva API Key' : 'Editar API Key' }}
          </h3>
        </div>
        
        <form @submit.prevent="saveAPIKey" class="p-6 space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre de la API Key
            </label>
            <input
              v-model="apiKeyForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Ej: Slack Integration Key"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Descripción
            </label>
            <textarea
              v-model="apiKeyForm.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Describe el propósito de esta API key..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Integración
            </label>
            <select
              v-model="apiKeyForm.integrationId"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="">Selecciona una integración</option>
              <option v-for="integration in availableIntegrations" :key="integration.id" :value="integration.id">
                {{ integration.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Permisos
            </label>
            <div class="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-lg p-3">
              <label
                v-for="permission in availablePermissions"
                :key="permission"
                class="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  v-model="apiKeyForm.permissions"
                  type="checkbox"
                  :value="permission"
                  class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ permission }}</span>
              </label>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Fecha de expiración
            </label>
            <input
              v-model="apiKeyForm.expiresAt"
              type="date"
              :min="minExpirationDate"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Límite de requests por día
            </label>
            <input
              v-model.number="apiKeyForm.rateLimit"
              type="number"
              min="1"
              max="100000"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="10000"
            />
          </div>
          
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              type="button"
              @click="closeModals"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isSaving"
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center"
            >
              <div v-if="isSaving" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              {{ showCreateModal ? 'Crear API Key' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Key,
  Plus,
  Search,
  Copy,
  Eye,
  EyeOff,
  Edit,
  RotateCcw,
  Shield,
  Trash2,
  AlertTriangle
} from 'lucide-vue-next'
import { useAPIKeys } from '@/composables/useAPIKeys'
import { useIntegrations } from '@/composables/useIntegrations'
import { useNotifications } from '@/composables/useNotifications'

// Composables
const { apiKeys, isLoading, createAPIKey, updateAPIKey, deleteAPIKey: removeAPIKey, revokeAPIKey: revokeKey, regenerateAPIKey: regenerateKey } = useAPIKeys()
const { integrations } = useIntegrations()
const { showNotification } = useNotifications()

// Reactive state
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedIntegration = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const isSaving = ref(false)
const isRegeneratingKey = ref(null)
const isRevokingKey = ref(null)
const editingAPIKey = ref(null)
const showFullKey = ref({})

// Form data
const apiKeyForm = ref({
  name: '',
  description: '',
  integrationId: '',
  permissions: [],
  expiresAt: '',
  rateLimit: 10000
})

// Available permissions for API keys
const availablePermissions = [
  'read:messages',
  'write:messages',
  'read:conversations',
  'write:conversations',
  'read:users',
  'write:users',
  'read:integrations',
  'write:integrations',
  'read:webhooks',
  'write:webhooks',
  'read:analytics',
  'admin:all'
]

// Computed properties
const availableIntegrations = computed(() => {
  return integrations.value.filter(integration => integration.status === 'active')
})

const filteredAPIKeys = computed(() => {
  let filtered = apiKeys.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(apiKey => 
      apiKey.name.toLowerCase().includes(query) ||
      apiKey.description.toLowerCase().includes(query)
    )
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(apiKey => apiKey.status === selectedStatus.value)
  }
  
  if (selectedIntegration.value) {
    filtered = filtered.filter(apiKey => apiKey.integrationId === selectedIntegration.value)
  }
  
  return filtered
})

const minExpirationDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
})

// Methods
const getStatusClasses = (status) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    expired: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    revoked: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
  }
  return classes[status] || classes.active
}

const getStatusDotClasses = (status) => {
  const classes = {
    active: 'bg-green-400',
    expired: 'bg-yellow-400',
    revoked: 'bg-red-400'
  }
  return classes[status] || classes.active
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activa',
    expired: 'Expirada',
    revoked: 'Revocada'
  }
  return labels[status] || status
}

const maskAPIKey = (key) => {
  if (!key || key.length < 8) return key
  return key.substring(0, 4) + '•'.repeat(key.length - 8) + key.substring(key.length - 4)
}

const toggleKeyVisibility = (keyId) => {
  showFullKey.value[keyId] = !showFullKey.value[keyId]
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatExpirationDate = (date) => {
  if (!date) return 'Sin expiración'
  const expDate = new Date(date)
  const now = new Date()
  const diffDays = Math.ceil((expDate - now) / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return 'Expirada'
  } else if (diffDays === 0) {
    return 'Expira hoy'
  } else if (diffDays === 1) {
    return 'Expira mañana'
  } else if (diffDays <= 7) {
    return `Expira en ${diffDays} días`
  } else {
    return expDate.toLocaleDateString('es-ES')
  }
}

const isExpiringSoon = (date) => {
  if (!date) return false
  const expDate = new Date(date)
  const now = new Date()
  const diffDays = Math.ceil((expDate - now) / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays > 0
}

const getRateLimitColor = (usage) => {
  if (usage >= 90) return 'text-red-600 dark:text-red-400'
  if (usage >= 75) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-green-600 dark:text-green-400'
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showNotification('API key copiada al portapapeles', 'success')
  } catch (error) {
    showNotification('Error al copiar API key', 'error')
  }
}

const regenerateAPIKey = async (apiKey) => {
  if (confirm(`¿Estás seguro de que quieres regenerar la API key "${apiKey.name}"? La clave actual dejará de funcionar.`)) {
    isRegeneratingKey.value = apiKey.id
    try {
      await regenerateKey(apiKey.id)
      showNotification('API key regenerada exitosamente', 'success')
    } catch (error) {
      showNotification('Error al regenerar API key', 'error')
    } finally {
      isRegeneratingKey.value = null
    }
  }
}

const revokeAPIKey = async (apiKey) => {
  if (confirm(`¿Estás seguro de que quieres revocar la API key "${apiKey.name}"? Esta acción no se puede deshacer.`)) {
    isRevokingKey.value = apiKey.id
    try {
      await revokeKey(apiKey.id)
      showNotification('API key revocada exitosamente', 'success')
    } catch (error) {
      showNotification('Error al revocar API key', 'error')
    } finally {
      isRevokingKey.value = null
    }
  }
}

const editAPIKey = (apiKey) => {
  editingAPIKey.value = apiKey
  apiKeyForm.value = {
    name: apiKey.name,
    description: apiKey.description,
    integrationId: apiKey.integrationId,
    permissions: [...apiKey.permissions],
    expiresAt: apiKey.expiresAt ? new Date(apiKey.expiresAt).toISOString().split('T')[0] : '',
    rateLimit: apiKey.rateLimit || 10000
  }
  showEditModal.value = true
}

const deleteAPIKey = async (apiKey) => {
  if (confirm(`¿Estás seguro de que quieres eliminar la API key "${apiKey.name}"?`)) {
    try {
      await removeAPIKey(apiKey.id)
      showNotification('API key eliminada exitosamente', 'success')
    } catch (error) {
      showNotification('Error al eliminar API key', 'error')
    }
  }
}

const saveAPIKey = async () => {
  isSaving.value = true
  try {
    const apiKeyData = {
      ...apiKeyForm.value,
      expiresAt: apiKeyForm.value.expiresAt ? new Date(apiKeyForm.value.expiresAt) : null
    }
    
    if (showCreateModal.value) {
      await createAPIKey(apiKeyData)
      showNotification('API key creada exitosamente', 'success')
    } else {
      await updateAPIKey(editingAPIKey.value.id, apiKeyData)
      showNotification('API key actualizada exitosamente', 'success')
    }
    
    closeModals()
  } catch (error) {
    showNotification('Error al guardar API key', 'error')
  } finally {
    isSaving.value = false
  }
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingAPIKey.value = null
  apiKeyForm.value = {
    name: '',
    description: '',
    integrationId: '',
    permissions: [],
    expiresAt: '',
    rateLimit: 10000
  }
}

// Lifecycle
onMounted(() => {
  // API keys are loaded automatically by the composable
})
</script>