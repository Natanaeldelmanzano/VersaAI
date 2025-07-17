<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Integraciones</h1>
            <p class="text-gray-600 mt-1">Conecta VersaAI con tus herramientas favoritas</p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="showWebhookManager = true"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <PlusIcon class="h-5 w-5" />
              <span>Nuevo Webhook</span>
            </button>
            <button
              @click="showAPIKeyManager = true"
              class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
            >
              <KeyIcon class="h-5 w-5" />
              <span>API Keys</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="px-6 py-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 rounded-lg">
              <LinkIcon class="h-6 w-6 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Integraciones Activas</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.activeIntegrations }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <CheckCircleIcon class="h-6 w-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Webhooks Configurados</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.webhooks }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 rounded-lg">
              <KeyIcon class="h-6 w-6 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">API Keys</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.apiKeys }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-orange-100 rounded-lg">
              <ClockIcon class="h-6 w-6 text-orange-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Eventos Hoy</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.eventsToday }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex space-x-4">
              <div class="relative">
                <MagnifyingGlassIcon class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar integraciones..."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select
                v-model="selectedCategory"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todas las categorías</option>
                <option value="crm">CRM</option>
                <option value="communication">Comunicación</option>
                <option value="analytics">Analytics</option>
                <option value="productivity">Productividad</option>
                <option value="ecommerce">E-commerce</option>
              </select>
              
              <select
                v-model="selectedStatus"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los estados</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="error">Error</option>
              </select>
            </div>
            
            <div class="flex items-center space-x-2">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <Squares2X2Icon class="h-5 w-5" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <ListBulletIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Integrations Grid/List -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <IntegrationCard
          v-for="integration in filteredIntegrations"
          :key="integration.id"
          :integration="integration"
          @configure="configureIntegration"
          @toggle="toggleIntegration"
          @delete="deleteIntegration"
        />
      </div>
      
      <div v-else class="bg-white rounded-lg shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Integración
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Categoría
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Última Actividad
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="integration in filteredIntegrations" :key="integration.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <img :src="integration.logo" :alt="integration.name" class="h-10 w-10 rounded-lg" />
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ integration.name }}</div>
                    <div class="text-sm text-gray-500">{{ integration.description }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ integration.category }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  integration.status === 'active' ? 'bg-green-100 text-green-800' :
                  integration.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                  'bg-red-100 text-red-800'
                ]">
                  {{ integration.status === 'active' ? 'Activo' : integration.status === 'inactive' ? 'Inactivo' : 'Error' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(integration.lastActivity) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex space-x-2">
                  <button
                    @click="configureIntegration(integration)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    <CogIcon class="h-5 w-5" />
                  </button>
                  <button
                    @click="toggleIntegration(integration)"
                    :class="[
                      integration.status === 'active' ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'
                    ]"
                  >
                    <PowerIcon class="h-5 w-5" />
                  </button>
                  <button
                    @click="deleteIntegration(integration)"
                    class="text-red-600 hover:text-red-900"
                  >
                    <TrashIcon class="h-5 w-5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Webhook Manager Modal -->
    <WebhookManager
      v-if="showWebhookManager"
      @close="showWebhookManager = false"
      @save="handleWebhookSave"
    />

    <!-- API Key Manager Modal -->
    <APIKeyManager
      v-if="showAPIKeyManager"
      @close="showAPIKeyManager = false"
      @save="handleAPIKeySave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  PlusIcon,
  KeyIcon,
  LinkIcon,
  CheckCircleIcon,
  ClockIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  CogIcon,
  PowerIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import IntegrationCard from '@/components/dashboard/IntegrationCard.vue'
import WebhookManager from '@/components/dashboard/WebhookManager.vue'
import APIKeyManager from '@/components/dashboard/APIKeyManager.vue'

// Reactive state
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedStatus = ref('')
const viewMode = ref('grid')
const showWebhookManager = ref(false)
const showAPIKeyManager = ref(false)
const loading = ref(false)

// Stats data
const stats = ref({
  activeIntegrations: 12,
  webhooks: 8,
  apiKeys: 5,
  eventsToday: 247
})

// Integrations data
const integrations = ref([
  {
    id: 1,
    name: 'Salesforce',
    description: 'CRM líder mundial',
    category: 'crm',
    status: 'active',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-15T10:30:00'),
    config: {
      apiKey: '***************',
      endpoint: 'https://api.salesforce.com',
      syncInterval: '15m'
    }
  },
  {
    id: 2,
    name: 'HubSpot',
    description: 'Plataforma de marketing y ventas',
    category: 'crm',
    status: 'active',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-15T09:15:00'),
    config: {
      apiKey: '***************',
      portalId: '12345678'
    }
  },
  {
    id: 3,
    name: 'Slack',
    description: 'Comunicación de equipos',
    category: 'communication',
    status: 'active',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-15T11:45:00'),
    config: {
      webhookUrl: 'https://hooks.slack.com/services/...',
      channel: '#general'
    }
  },
  {
    id: 4,
    name: 'Google Analytics',
    description: 'Análisis web avanzado',
    category: 'analytics',
    status: 'inactive',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-14T16:20:00'),
    config: {
      trackingId: 'GA-XXXXXXXXX',
      propertyId: '123456789'
    }
  },
  {
    id: 5,
    name: 'Zapier',
    description: 'Automatización de workflows',
    category: 'productivity',
    status: 'active',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-15T08:30:00'),
    config: {
      webhookUrl: 'https://hooks.zapier.com/hooks/catch/...',
      triggers: ['new_conversation', 'user_message']
    }
  },
  {
    id: 6,
    name: 'Shopify',
    description: 'Plataforma de e-commerce',
    category: 'ecommerce',
    status: 'error',
    logo: '/api/placeholder/40/40',
    lastActivity: new Date('2024-01-15T07:00:00'),
    config: {
      shopDomain: 'mystore.myshopify.com',
      apiKey: '***************',
      error: 'Invalid API credentials'
    }
  }
])

// Computed properties
const filteredIntegrations = computed(() => {
  return integrations.value.filter(integration => {
    const matchesSearch = integration.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         integration.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = !selectedCategory.value || integration.category === selectedCategory.value
    const matchesStatus = !selectedStatus.value || integration.status === selectedStatus.value
    
    return matchesSearch && matchesCategory && matchesStatus
  })
})

// Methods
const configureIntegration = (integration) => {
  console.log('Configuring integration:', integration.name)
  // Implementar lógica de configuración
}

const toggleIntegration = (integration) => {
  integration.status = integration.status === 'active' ? 'inactive' : 'active'
  console.log(`Integration ${integration.name} ${integration.status}`)
}

const deleteIntegration = (integration) => {
  if (confirm(`¿Estás seguro de que quieres eliminar la integración con ${integration.name}?`)) {
    const index = integrations.value.findIndex(i => i.id === integration.id)
    if (index > -1) {
      integrations.value.splice(index, 1)
    }
  }
}

const handleWebhookSave = (webhookData) => {
  console.log('Webhook saved:', webhookData)
  showWebhookManager.value = false
  // Actualizar lista de webhooks
}

const handleAPIKeySave = (apiKeyData) => {
  console.log('API Key saved:', apiKeyData)
  showAPIKeyManager.value = false
  // Actualizar lista de API keys
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

const loadIntegrations = async () => {
  loading.value = true
  try {
    // Simular carga de datos
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Integrations loaded')
  } catch (error) {
    console.error('Error loading integrations:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadIntegrations()
})
</script>