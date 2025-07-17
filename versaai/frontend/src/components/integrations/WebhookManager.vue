<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
            <Webhook class="h-5 w-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Gestión de Webhooks
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Configura y gestiona webhooks para tus integraciones
            </p>
          </div>
        </div>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors duration-200"
        >
          <Plus class="h-4 w-4 mr-2" />
          Nuevo Webhook
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
              placeholder="Buscar webhooks..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        <div class="flex gap-2">
          <select
            v-model="selectedStatus"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
            <option value="error">Error</option>
          </select>
          <select
            v-model="selectedIntegration"
            class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todas las integraciones</option>
            <option v-for="integration in availableIntegrations" :key="integration.id" :value="integration.id">
              {{ integration.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Webhooks List -->
    <div class="p-6">
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="filteredWebhooks.length === 0" class="text-center py-12">
        <Webhook class="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No hay webhooks configurados
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">
          Crea tu primer webhook para comenzar a recibir eventos
        </p>
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors duration-200"
        >
          <Plus class="h-4 w-4 mr-2" />
          Crear Webhook
        </button>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="webhook in filteredWebhooks"
          :key="webhook.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-3 mb-2">
                <h4 class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ webhook.name }}
                </h4>
                <span
                  :class="getStatusClasses(webhook.status)"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  <span :class="getStatusDotClasses(webhook.status)" class="w-1.5 h-1.5 rounded-full mr-1.5"></span>
                  {{ getStatusLabel(webhook.status) }}
                </span>
              </div>
              
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {{ webhook.description }}
              </p>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    URL
                  </label>
                  <div class="flex items-center mt-1">
                    <code class="text-sm bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-gray-900 dark:text-white font-mono truncate flex-1">
                      {{ webhook.url }}
                    </code>
                    <button
                      @click="copyToClipboard(webhook.url)"
                      class="ml-2 p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    >
                      <Copy class="h-4 w-4" />
                    </button>
                  </div>
                </div>
                
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    Eventos
                  </label>
                  <div class="mt-1">
                    <div class="flex flex-wrap gap-1">
                      <span
                        v-for="event in webhook.events.slice(0, 3)"
                        :key="event"
                        class="inline-flex items-center px-2 py-1 rounded text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300"
                      >
                        {{ event }}
                      </span>
                      <span
                        v-if="webhook.events.length > 3"
                        class="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                      >
                        +{{ webhook.events.length - 3 }} más
                      </span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    Última actividad
                  </label>
                  <p class="text-sm text-gray-900 dark:text-white mt-1">
                    {{ formatTimeAgo(webhook.lastTriggered) }}
                  </p>
                </div>
              </div>
              
              <!-- Metrics -->
              <div class="grid grid-cols-3 gap-4 py-3 border-t border-gray-200 dark:border-gray-700">
                <div class="text-center">
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ formatNumber(webhook.metrics.totalDeliveries) }}
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Entregas</p>
                </div>
                <div class="text-center">
                  <p class="text-lg font-semibold" :class="getSuccessRateColor(webhook.metrics.successRate)">
                    {{ webhook.metrics.successRate }}%
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Éxito</p>
                </div>
                <div class="text-center">
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ webhook.metrics.avgResponseTime }}ms
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Respuesta</p>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center space-x-2 ml-4">
              <button
                @click="testWebhook(webhook)"
                :disabled="isTestingWebhook === webhook.id"
                class="p-2 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors disabled:opacity-50"
                title="Probar webhook"
              >
                <Play v-if="isTestingWebhook !== webhook.id" class="h-4 w-4" />
                <div v-else class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              </button>
              
              <button
                @click="editWebhook(webhook)"
                class="p-2 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 transition-colors"
                title="Editar webhook"
              >
                <Edit class="h-4 w-4" />
              </button>
              
              <button
                @click="toggleWebhook(webhook)"
                :disabled="isTogglingWebhook === webhook.id"
                class="p-2 transition-colors disabled:opacity-50"
                :class="webhook.status === 'active' ? 'text-gray-400 hover:text-red-600 dark:hover:text-red-400' : 'text-gray-400 hover:text-green-600 dark:hover:text-green-400'"
                :title="webhook.status === 'active' ? 'Desactivar webhook' : 'Activar webhook'"
              >
                <Power v-if="isTogglingWebhook !== webhook.id" class="h-4 w-4" />
                <div v-else class="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
              </button>
              
              <button
                @click="deleteWebhook(webhook)"
                class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                title="Eliminar webhook"
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
            {{ showCreateModal ? 'Crear Nuevo Webhook' : 'Editar Webhook' }}
          </h3>
        </div>
        
        <form @submit.prevent="saveWebhook" class="p-6 space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre del Webhook
            </label>
            <input
              v-model="webhookForm.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ej: Notificaciones de Slack"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Descripción
            </label>
            <textarea
              v-model="webhookForm.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe el propósito de este webhook..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              URL del Webhook
            </label>
            <input
              v-model="webhookForm.url"
              type="url"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="https://ejemplo.com/webhook"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Integración
            </label>
            <select
              v-model="webhookForm.integrationId"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Selecciona una integración</option>
              <option v-for="integration in availableIntegrations" :key="integration.id" :value="integration.id">
                {{ integration.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Eventos
            </label>
            <div class="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-lg p-3">
              <label
                v-for="event in availableEvents"
                :key="event"
                class="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  v-model="webhookForm.events"
                  type="checkbox"
                  :value="event"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ event }}</span>
              </label>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <input
              v-model="webhookForm.isActive"
              type="checkbox"
              id="webhook-active"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label for="webhook-active" class="text-sm font-medium text-gray-700 dark:text-gray-300">
              Activar webhook inmediatamente
            </label>
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
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center"
            >
              <div v-if="isSaving" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              {{ showCreateModal ? 'Crear Webhook' : 'Guardar Cambios' }}
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
  Webhook,
  Plus,
  Search,
  Copy,
  Play,
  Edit,
  Power,
  Trash2
} from 'lucide-vue-next'
import { useWebhooks } from '@/composables/useWebhooks'
import { useIntegrations } from '@/composables/useIntegrations'
import { useNotifications } from '@/composables/useNotifications'

// Composables
const { webhooks, isLoading, createWebhook, updateWebhook, deleteWebhook: removeWebhook, toggleWebhook: toggleWebhookStatus, testWebhook: testWebhookEndpoint } = useWebhooks()
const { integrations } = useIntegrations()
const { showNotification } = useNotifications()

// Reactive state
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedIntegration = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const isSaving = ref(false)
const isTestingWebhook = ref(null)
const isTogglingWebhook = ref(null)
const editingWebhook = ref(null)

// Form data
const webhookForm = ref({
  name: '',
  description: '',
  url: '',
  integrationId: '',
  events: [],
  isActive: true
})

// Available events for webhooks
const availableEvents = [
  'message.sent',
  'message.received',
  'conversation.started',
  'conversation.ended',
  'user.created',
  'user.updated',
  'integration.connected',
  'integration.disconnected',
  'error.occurred',
  'system.maintenance'
]

// Computed properties
const availableIntegrations = computed(() => {
  return integrations.value.filter(integration => integration.status === 'active')
})

const filteredWebhooks = computed(() => {
  let filtered = webhooks.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(webhook => 
      webhook.name.toLowerCase().includes(query) ||
      webhook.description.toLowerCase().includes(query) ||
      webhook.url.toLowerCase().includes(query)
    )
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(webhook => webhook.status === selectedStatus.value)
  }
  
  if (selectedIntegration.value) {
    filtered = filtered.filter(webhook => webhook.integrationId === selectedIntegration.value)
  }
  
  return filtered
})

// Methods
const getStatusClasses = (status) => {
  const classes = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    error: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
  }
  return classes[status] || classes.inactive
}

const getStatusDotClasses = (status) => {
  const classes = {
    active: 'bg-green-400',
    inactive: 'bg-gray-400',
    error: 'bg-red-400'
  }
  return classes[status] || classes.inactive
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    error: 'Error'
  }
  return labels[status] || status
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatTimeAgo = (date) => {
  const now = new Date()
  const diff = now - new Date(date)
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (days > 0) {
    return `hace ${days} día${days > 1 ? 's' : ''}`
  } else if (hours > 0) {
    return `hace ${hours} hora${hours > 1 ? 's' : ''}`
  } else if (minutes > 0) {
    return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  } else {
    return 'hace un momento'
  }
}

const getSuccessRateColor = (rate) => {
  if (rate >= 99) return 'text-green-600 dark:text-green-400'
  if (rate >= 95) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showNotification('URL copiada al portapapeles', 'success')
  } catch (error) {
    showNotification('Error al copiar URL', 'error')
  }
}

const testWebhook = async (webhook) => {
  isTestingWebhook.value = webhook.id
  try {
    await testWebhookEndpoint(webhook.id)
    showNotification('Webhook probado exitosamente', 'success')
  } catch (error) {
    showNotification('Error al probar webhook', 'error')
  } finally {
    isTestingWebhook.value = null
  }
}

const toggleWebhook = async (webhook) => {
  isTogglingWebhook.value = webhook.id
  try {
    await toggleWebhookStatus(webhook.id)
    const action = webhook.status === 'active' ? 'desactivado' : 'activado'
    showNotification(`Webhook ${action} exitosamente`, 'success')
  } catch (error) {
    showNotification('Error al cambiar estado del webhook', 'error')
  } finally {
    isTogglingWebhook.value = null
  }
}

const editWebhook = (webhook) => {
  editingWebhook.value = webhook
  webhookForm.value = {
    name: webhook.name,
    description: webhook.description,
    url: webhook.url,
    integrationId: webhook.integrationId,
    events: [...webhook.events],
    isActive: webhook.status === 'active'
  }
  showEditModal.value = true
}

const deleteWebhook = async (webhook) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el webhook "${webhook.name}"?`)) {
    try {
      await removeWebhook(webhook.id)
      showNotification('Webhook eliminado exitosamente', 'success')
    } catch (error) {
      showNotification('Error al eliminar webhook', 'error')
    }
  }
}

const saveWebhook = async () => {
  isSaving.value = true
  try {
    const webhookData = {
      ...webhookForm.value,
      status: webhookForm.value.isActive ? 'active' : 'inactive'
    }
    
    if (showCreateModal.value) {
      await createWebhook(webhookData)
      showNotification('Webhook creado exitosamente', 'success')
    } else {
      await updateWebhook(editingWebhook.value.id, webhookData)
      showNotification('Webhook actualizado exitosamente', 'success')
    }
    
    closeModals()
  } catch (error) {
    showNotification('Error al guardar webhook', 'error')
  } finally {
    isSaving.value = false
  }
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingWebhook.value = null
  webhookForm.value = {
    name: '',
    description: '',
    url: '',
    integrationId: '',
    events: [],
    isActive: true
  }
}

// Lifecycle
onMounted(() => {
  // Webhooks are loaded automatically by the composable
})
</script>