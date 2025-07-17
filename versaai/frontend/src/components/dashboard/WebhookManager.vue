<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Gestión de Webhooks</h3>
          <p class="text-sm text-gray-600 mt-1">Configura webhooks para recibir eventos en tiempo real</p>
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
              Webhooks Activos ({{ webhooks.length }})
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
              {{ editingWebhook ? 'Editar Webhook' : 'Nuevo Webhook' }}
            </button>
            <button
              @click="activeTab = 'logs'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'logs'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Logs de Eventos
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- Webhooks List -->
        <div v-if="activeTab === 'list'" class="space-y-4">
          <div v-if="webhooks.length === 0" class="text-center py-12">
            <GlobeAltIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No hay webhooks configurados</h3>
            <p class="mt-1 text-sm text-gray-500">Comienza creando tu primer webhook.</p>
            <div class="mt-6">
              <button
                @click="activeTab = 'create'"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon class="-ml-1 mr-2 h-5 w-5" />
                Nuevo Webhook
              </button>
            </div>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="webhook in webhooks"
              :key="webhook.id"
              class="bg-gray-50 rounded-lg p-4 border border-gray-200"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h4 class="text-sm font-medium text-gray-900">{{ webhook.name }}</h4>
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      webhook.status === 'active' ? 'bg-green-100 text-green-800' :
                      webhook.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                      'bg-red-100 text-red-800'
                    ]">
                      {{ webhook.status === 'active' ? 'Activo' : webhook.status === 'inactive' ? 'Inactivo' : 'Error' }}
                    </span>
                  </div>
                  
                  <p class="text-sm text-gray-600 mt-1">{{ webhook.description }}</p>
                  
                  <div class="mt-2 space-y-1">
                    <div class="flex items-center text-xs text-gray-500">
                      <span class="font-medium mr-2">URL:</span>
                      <code class="bg-gray-100 px-2 py-1 rounded">{{ webhook.url }}</code>
                    </div>
                    <div class="flex items-center text-xs text-gray-500">
                      <span class="font-medium mr-2">Eventos:</span>
                      <span>{{ webhook.events.join(', ') }}</span>
                    </div>
                    <div class="flex items-center text-xs text-gray-500">
                      <span class="font-medium mr-2">Última actividad:</span>
                      <span>{{ formatDate(webhook.lastTriggered) }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2">
                  <button
                    @click="testWebhook(webhook)"
                    class="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    <PlayIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="editWebhook(webhook)"
                    class="text-gray-600 hover:text-gray-800 text-sm"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="toggleWebhook(webhook)"
                    :class="[
                      'text-sm',
                      webhook.status === 'active' ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'
                    ]"
                  >
                    <PowerIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="deleteWebhook(webhook)"
                    class="text-red-600 hover:text-red-800 text-sm"
                  >
                    <TrashIcon class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Create/Edit Webhook -->
        <div v-if="activeTab === 'create'" class="space-y-6">
          <form @submit.prevent="saveWebhook" class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="webhook-name" class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Webhook
                </label>
                <input
                  id="webhook-name"
                  v-model="webhookForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Mi Webhook"
                />
              </div>
              
              <div>
                <label for="webhook-url" class="block text-sm font-medium text-gray-700 mb-2">
                  URL del Endpoint
                </label>
                <input
                  id="webhook-url"
                  v-model="webhookForm.url"
                  type="url"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="https://api.ejemplo.com/webhook"
                />
              </div>
            </div>
            
            <div>
              <label for="webhook-description" class="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                id="webhook-description"
                v-model="webhookForm.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Descripción del webhook..."
              ></textarea>
            </div>

            <!-- Events Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">
                Eventos a Escuchar
              </label>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                <label
                  v-for="event in availableEvents"
                  :key="event.value"
                  class="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                >
                  <input
                    v-model="webhookForm.events"
                    :value="event.value"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ event.label }}</div>
                    <div class="text-xs text-gray-500">{{ event.description }}</div>
                  </div>
                </label>
              </div>
            </div>

            <!-- Advanced Settings -->
            <div class="border-t border-gray-200 pt-6">
              <h4 class="text-sm font-medium text-gray-900 mb-4">Configuración Avanzada</h4>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="webhook-method" class="block text-sm font-medium text-gray-700 mb-2">
                    Método HTTP
                  </label>
                  <select
                    id="webhook-method"
                    v-model="webhookForm.method"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="PATCH">PATCH</option>
                  </select>
                </div>
                
                <div>
                  <label for="webhook-timeout" class="block text-sm font-medium text-gray-700 mb-2">
                    Timeout (segundos)
                  </label>
                  <input
                    id="webhook-timeout"
                    v-model.number="webhookForm.timeout"
                    type="number"
                    min="1"
                    max="60"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              
              <div class="mt-4">
                <label for="webhook-secret" class="block text-sm font-medium text-gray-700 mb-2">
                  Secret Key (opcional)
                </label>
                <input
                  id="webhook-secret"
                  v-model="webhookForm.secret"
                  type="password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Clave secreta para firmar las peticiones"
                />
              </div>
              
              <div class="mt-4">
                <label class="flex items-center space-x-3">
                  <input
                    v-model="webhookForm.retryOnFailure"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span class="text-sm text-gray-700">Reintentar en caso de fallo</span>
                </label>
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
                {{ editingWebhook ? 'Actualizar' : 'Crear' }} Webhook
              </button>
            </div>
          </form>
        </div>

        <!-- Event Logs -->
        <div v-if="activeTab === 'logs'" class="space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-medium text-gray-900">Logs de Eventos Recientes</h4>
            <button
              @click="refreshLogs"
              class="text-blue-600 hover:text-blue-800 text-sm flex items-center space-x-1"
            >
              <ArrowPathIcon class="h-4 w-4" />
              <span>Actualizar</span>
            </button>
          </div>
          
          <div class="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <div v-if="eventLogs.length === 0" class="text-center py-8">
              <DocumentTextIcon class="mx-auto h-8 w-8 text-gray-400" />
              <p class="text-sm text-gray-500 mt-2">No hay logs disponibles</p>
            </div>
            
            <div v-else class="space-y-3">
              <div
                v-for="log in eventLogs"
                :key="log.id"
                class="bg-white rounded-lg p-3 border border-gray-200"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span :class="[
                        'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                        log.status === 'success' ? 'bg-green-100 text-green-800' :
                        log.status === 'failed' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      ]">
                        {{ log.status === 'success' ? 'Éxito' : log.status === 'failed' ? 'Fallo' : 'Pendiente' }}
                      </span>
                      <span class="text-sm font-medium text-gray-900">{{ log.event }}</span>
                    </div>
                    
                    <p class="text-xs text-gray-500 mt-1">{{ log.webhook }} • {{ formatDate(log.timestamp) }}</p>
                    
                    <div v-if="log.error" class="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded">
                      {{ log.error }}
                    </div>
                  </div>
                  
                  <div class="text-xs text-gray-500">
                    {{ log.responseTime }}ms
                  </div>
                </div>
              </div>
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
  GlobeAltIcon,
  PlayIcon,
  PencilIcon,
  PowerIcon,
  TrashIcon,
  ArrowPathIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const activeTab = ref('list')
const editingWebhook = ref(null)
const webhooks = ref([
  {
    id: 1,
    name: 'Slack Notifications',
    description: 'Envía notificaciones a Slack cuando hay nuevas conversaciones',
    url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX',
    events: ['conversation.created', 'message.received'],
    method: 'POST',
    timeout: 30,
    status: 'active',
    retryOnFailure: true,
    lastTriggered: new Date('2024-01-15T10:30:00')
  },
  {
    id: 2,
    name: 'CRM Integration',
    description: 'Sincroniza contactos con el CRM',
    url: 'https://api.crm.com/webhooks/versaai',
    events: ['user.created', 'conversation.ended'],
    method: 'POST',
    timeout: 15,
    status: 'active',
    retryOnFailure: true,
    lastTriggered: new Date('2024-01-15T09:15:00')
  }
])

const webhookForm = ref({
  name: '',
  description: '',
  url: '',
  events: [],
  method: 'POST',
  timeout: 30,
  secret: '',
  retryOnFailure: true
})

const availableEvents = ref([
  {
    value: 'conversation.created',
    label: 'Nueva Conversación',
    description: 'Se inicia una nueva conversación'
  },
  {
    value: 'conversation.ended',
    label: 'Conversación Finalizada',
    description: 'Una conversación ha terminado'
  },
  {
    value: 'message.received',
    label: 'Mensaje Recibido',
    description: 'Se recibe un nuevo mensaje'
  },
  {
    value: 'message.sent',
    label: 'Mensaje Enviado',
    description: 'El bot envía un mensaje'
  },
  {
    value: 'user.created',
    label: 'Usuario Creado',
    description: 'Se registra un nuevo usuario'
  },
  {
    value: 'chatbot.updated',
    label: 'Chatbot Actualizado',
    description: 'Se actualiza la configuración del chatbot'
  }
])

const eventLogs = ref([
  {
    id: 1,
    webhook: 'Slack Notifications',
    event: 'conversation.created',
    status: 'success',
    timestamp: new Date('2024-01-15T10:30:00'),
    responseTime: 245
  },
  {
    id: 2,
    webhook: 'CRM Integration',
    event: 'user.created',
    status: 'failed',
    timestamp: new Date('2024-01-15T10:25:00'),
    responseTime: 5000,
    error: 'Connection timeout'
  },
  {
    id: 3,
    webhook: 'Slack Notifications',
    event: 'message.received',
    status: 'success',
    timestamp: new Date('2024-01-15T10:20:00'),
    responseTime: 156
  }
])

// Computed properties
const isFormValid = computed(() => {
  return webhookForm.value.name && 
         webhookForm.value.url && 
         webhookForm.value.events.length > 0
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const editWebhook = (webhook) => {
  editingWebhook.value = webhook
  webhookForm.value = { ...webhook }
  activeTab.value = 'create'
}

const resetForm = () => {
  editingWebhook.value = null
  webhookForm.value = {
    name: '',
    description: '',
    url: '',
    events: [],
    method: 'POST',
    timeout: 30,
    secret: '',
    retryOnFailure: true
  }
  activeTab.value = 'list'
}

const saveWebhook = () => {
  if (editingWebhook.value) {
    // Update existing webhook
    const index = webhooks.value.findIndex(w => w.id === editingWebhook.value.id)
    if (index > -1) {
      webhooks.value[index] = { ...webhookForm.value, id: editingWebhook.value.id, status: 'active' }
    }
  } else {
    // Create new webhook
    const newWebhook = {
      ...webhookForm.value,
      id: Date.now(),
      status: 'active',
      lastTriggered: new Date()
    }
    webhooks.value.push(newWebhook)
  }
  
  emit('save', webhookForm.value)
  resetForm()
}

const testWebhook = (webhook) => {
  console.log('Testing webhook:', webhook.name)
  // Implementar lógica de prueba
}

const toggleWebhook = (webhook) => {
  webhook.status = webhook.status === 'active' ? 'inactive' : 'active'
}

const deleteWebhook = (webhook) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el webhook "${webhook.name}"?`)) {
    const index = webhooks.value.findIndex(w => w.id === webhook.id)
    if (index > -1) {
      webhooks.value.splice(index, 1)
    }
  }
}

const refreshLogs = () => {
  console.log('Refreshing event logs')
  // Implementar lógica de actualización de logs
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  // Cargar datos iniciales si es necesario
})
</script>