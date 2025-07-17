<template>
  <div class="enterprise-integrations">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Integraciones Empresariales</h2>
        <p class="text-gray-600 mt-2">Gestiona conexiones con sistemas externos y APIs de terceros</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="openIntegrationModal"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Nueva Integración
        </button>
        
        <button
          @click="refreshIntegrations"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          <ArrowPathIcon :class="['w-4 h-4 mr-2', { 'animate-spin': isLoading }]" />
          Actualizar
        </button>
      </div>
    </div>

    <!-- Integration Categories -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">SSO Activos</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ integrationStats.sso }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+2</span>
              <span class="text-sm text-gray-500 ml-2">este mes</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <ShieldCheckIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">APIs Conectadas</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ integrationStats.apis }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+5</span>
              <span class="text-sm text-gray-500 ml-2">este mes</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <CloudIcon class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Webhooks</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ integrationStats.webhooks }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+3</span>
              <span class="text-sm text-gray-500 ml-2">este mes</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <BoltIcon class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">CRM Conectados</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ integrationStats.crm }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+1</span>
              <span class="text-sm text-gray-500 ml-2">este mes</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <BuildingOfficeIcon class="w-6 h-6 text-orange-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Integration Tabs -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
          <button
            v-for="tab in integrationTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === tab.id
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5 mr-2 inline" />
            {{ tab.name }}
            <span :class="[
              'ml-2 py-0.5 px-2 rounded-full text-xs font-medium',
              activeTab === tab.id
                ? 'bg-primary-100 text-primary-600'
                : 'bg-gray-100 text-gray-600'
            ]">
              {{ tab.count }}
            </span>
          </button>
        </nav>
      </div>
      
      <div class="p-6">
        <!-- SSO Integrations -->
        <div v-if="activeTab === 'sso'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div 
              v-for="sso in ssoIntegrations" 
              :key="sso.id"
              class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <img :src="sso.logo" :alt="sso.name" class="w-8 h-8" />
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">{{ sso.name }}</h3>
                    <p class="text-sm text-gray-600">{{ sso.description }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span :class="[
                    'w-3 h-3 rounded-full',
                    sso.status === 'active' ? 'bg-green-500' :
                    sso.status === 'inactive' ? 'bg-red-500' : 'bg-yellow-500'
                  ]"></span>
                  <span class="text-sm font-medium text-gray-600">{{ getStatusLabel(sso.status) }}</span>
                </div>
              </div>
              
              <div class="mt-4 space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Usuarios activos:</span>
                  <span class="font-medium">{{ sso.activeUsers }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Último login:</span>
                  <span class="font-medium">{{ sso.lastLogin }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Configurado:</span>
                  <span class="font-medium">{{ sso.configuredDate }}</span>
                </div>
              </div>
              
              <div class="mt-6 flex space-x-3">
                <button
                  @click="configureSSO(sso)"
                  class="flex-1 px-3 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700"
                >
                  Configurar
                </button>
                <button
                  @click="testSSO(sso)"
                  class="flex-1 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50"
                >
                  Probar
                </button>
                <button
                  @click="toggleSSO(sso)"
                  :class="[
                    'px-3 py-2 rounded-lg text-sm font-medium',
                    sso.status === 'active'
                      ? 'bg-red-600 text-white hover:bg-red-700'
                      : 'bg-green-600 text-white hover:bg-green-700'
                  ]"
                >
                  {{ sso.status === 'active' ? 'Desactivar' : 'Activar' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- API Integrations -->
        <div v-if="activeTab === 'apis'" class="space-y-6">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    API
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Requests/día
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Latencia
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Última actividad
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="api in apiIntegrations" :key="api.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mr-4">
                        <component :is="api.icon" class="w-5 h-5 text-gray-600" />
                      </div>
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ api.name }}</div>
                        <div class="text-sm text-gray-500">{{ api.endpoint }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                      api.status === 'active' ? 'bg-green-100 text-green-800' :
                      api.status === 'error' ? 'bg-red-100 text-red-800' :
                      api.status === 'warning' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                    ]">
                      {{ getStatusLabel(api.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ api.requestsPerDay.toLocaleString() }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ api.latency }}ms
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ api.lastActivity }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      @click="configureAPI(api)"
                      class="text-primary-600 hover:text-primary-900"
                    >
                      Configurar
                    </button>
                    <button
                      @click="testAPI(api)"
                      class="text-green-600 hover:text-green-900"
                    >
                      Probar
                    </button>
                    <button
                      @click="viewAPILogs(api)"
                      class="text-gray-600 hover:text-gray-900"
                    >
                      Logs
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Webhooks -->
        <div v-if="activeTab === 'webhooks'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div 
              v-for="webhook in webhookIntegrations" 
              :key="webhook.id"
              class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">{{ webhook.name }}</h3>
                  <p class="text-sm text-gray-600">{{ webhook.description }}</p>
                  <p class="text-xs text-gray-500 mt-1 font-mono">{{ webhook.url }}</p>
                </div>
                <span :class="[
                  'w-3 h-3 rounded-full',
                  webhook.status === 'active' ? 'bg-green-500' :
                  webhook.status === 'error' ? 'bg-red-500' : 'bg-yellow-500'
                ]"></span>
              </div>
              
              <div class="space-y-2 mb-4">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Eventos:</span>
                  <span class="font-medium">{{ webhook.events.join(', ') }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Último trigger:</span>
                  <span class="font-medium">{{ webhook.lastTrigger }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Success rate:</span>
                  <span class="font-medium">{{ webhook.successRate }}%</span>
                </div>
              </div>
              
              <div class="flex space-x-3">
                <button
                  @click="configureWebhook(webhook)"
                  class="flex-1 px-3 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700"
                >
                  Configurar
                </button>
                <button
                  @click="testWebhook(webhook)"
                  class="flex-1 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50"
                >
                  Probar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- CRM Integrations -->
        <div v-if="activeTab === 'crm'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div 
              v-for="crm in crmIntegrations" 
              :key="crm.id"
              class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <img :src="crm.logo" :alt="crm.name" class="w-8 h-8" />
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">{{ crm.name }}</h3>
                    <p class="text-sm text-gray-600">{{ crm.description }}</p>
                  </div>
                </div>
                <span :class="[
                  'w-3 h-3 rounded-full',
                  crm.status === 'active' ? 'bg-green-500' :
                  crm.status === 'inactive' ? 'bg-red-500' : 'bg-yellow-500'
                ]"></span>
              </div>
              
              <div class="mt-4 space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Contactos sincronizados:</span>
                  <span class="font-medium">{{ crm.syncedContacts.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Última sincronización:</span>
                  <span class="font-medium">{{ crm.lastSync }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Configurado:</span>
                  <span class="font-medium">{{ crm.configuredDate }}</span>
                </div>
              </div>
              
              <div class="mt-6 flex space-x-3">
                <button
                  @click="configureCRM(crm)"
                  class="flex-1 px-3 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700"
                >
                  Configurar
                </button>
                <button
                  @click="syncCRM(crm)"
                  class="flex-1 px-3 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50"
                >
                  Sincronizar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Integration Logs -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Logs de Integración</h3>
          <div class="flex items-center space-x-4">
            <select 
              v-model="logFilter"
              class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option value="all">Todas las integraciones</option>
              <option value="sso">SSO</option>
              <option value="api">APIs</option>
              <option value="webhook">Webhooks</option>
              <option value="crm">CRM</option>
            </select>
            
            <button
              @click="clearIntegrationLogs"
              class="px-3 py-1 text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Limpiar
            </button>
          </div>
        </div>
      </div>
      <div class="p-6">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Integración
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Evento
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Detalles
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="log in filteredIntegrationLogs" :key="log.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatLogTime(log.timestamp) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <span :class="[
                      'w-2 h-2 rounded-full mr-2',
                      log.type === 'sso' ? 'bg-blue-500' :
                      log.type === 'api' ? 'bg-green-500' :
                      log.type === 'webhook' ? 'bg-purple-500' :
                      log.type === 'crm' ? 'bg-orange-500' : 'bg-gray-500'
                    ]"></span>
                    <span class="text-sm font-medium text-gray-900">{{ log.integration }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ log.event }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    log.status === 'success' ? 'bg-green-100 text-green-800' :
                    log.status === 'error' ? 'bg-red-100 text-red-800' :
                    log.status === 'warning' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                  ]">
                    {{ getStatusLabel(log.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500">
                  {{ log.details }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="filteredIntegrationLogs.length === 0" class="text-center py-8">
          <p class="text-gray-500">No hay logs disponibles</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import {
  PlusIcon,
  ArrowPathIcon,
  ArrowUpIcon,
  ShieldCheckIcon,
  CloudIcon,
  BoltIcon,
  BuildingOfficeIcon,
  CogIcon,
  GlobeAltIcon,
  LinkIcon
} from '@heroicons/vue/24/outline'

// Store
const dashboardStore = useDashboardStore()

// State
const isLoading = ref(false)
const activeTab = ref('sso')
const logFilter = ref('all')

// Mock data
const integrationStats = ref({
  sso: 3,
  apis: 12,
  webhooks: 8,
  crm: 2
})

const integrationTabs = [
  { id: 'sso', name: 'SSO', icon: ShieldCheckIcon, count: 3 },
  { id: 'apis', name: 'APIs', icon: CloudIcon, count: 12 },
  { id: 'webhooks', name: 'Webhooks', icon: BoltIcon, count: 8 },
  { id: 'crm', name: 'CRM', icon: BuildingOfficeIcon, count: 2 }
]

const ssoIntegrations = ref([
  {
    id: 1,
    name: 'Google Workspace',
    description: 'Autenticación con Google SSO',
    logo: '/api/placeholder/32/32',
    status: 'active',
    activeUsers: 245,
    lastLogin: 'Hace 5 minutos',
    configuredDate: '15 Mar 2024'
  },
  {
    id: 2,
    name: 'Microsoft Azure AD',
    description: 'Autenticación con Azure Active Directory',
    logo: '/api/placeholder/32/32',
    status: 'active',
    activeUsers: 189,
    lastLogin: 'Hace 12 minutos',
    configuredDate: '10 Mar 2024'
  },
  {
    id: 3,
    name: 'Okta',
    description: 'Autenticación con Okta SSO',
    logo: '/api/placeholder/32/32',
    status: 'inactive',
    activeUsers: 0,
    lastLogin: 'Nunca',
    configuredDate: '5 Mar 2024'
  }
])

const apiIntegrations = ref([
  {
    id: 1,
    name: 'Slack API',
    endpoint: 'https://slack.com/api/v1',
    icon: CloudIcon,
    status: 'active',
    requestsPerDay: 1250,
    latency: 120,
    lastActivity: 'Hace 2 minutos'
  },
  {
    id: 2,
    name: 'Zendesk API',
    endpoint: 'https://api.zendesk.com/v2',
    icon: CloudIcon,
    status: 'active',
    requestsPerDay: 890,
    latency: 95,
    lastActivity: 'Hace 15 minutos'
  },
  {
    id: 3,
    name: 'Stripe API',
    endpoint: 'https://api.stripe.com/v1',
    icon: CloudIcon,
    status: 'warning',
    requestsPerDay: 456,
    latency: 250,
    lastActivity: 'Hace 1 hora'
  }
])

const webhookIntegrations = ref([
  {
    id: 1,
    name: 'Payment Notifications',
    description: 'Notificaciones de pagos desde Stripe',
    url: 'https://api.versaai.com/webhooks/payments',
    status: 'active',
    events: ['payment.success', 'payment.failed'],
    lastTrigger: 'Hace 30 minutos',
    successRate: 98.5
  },
  {
    id: 2,
    name: 'User Events',
    description: 'Eventos de usuarios desde CRM',
    url: 'https://api.versaai.com/webhooks/users',
    status: 'active',
    events: ['user.created', 'user.updated'],
    lastTrigger: 'Hace 1 hora',
    successRate: 99.2
  }
])

const crmIntegrations = ref([
  {
    id: 1,
    name: 'Salesforce',
    description: 'Integración con Salesforce CRM',
    logo: '/api/placeholder/32/32',
    status: 'active',
    syncedContacts: 15420,
    lastSync: 'Hace 2 horas',
    configuredDate: '20 Feb 2024'
  },
  {
    id: 2,
    name: 'HubSpot',
    description: 'Integración con HubSpot CRM',
    logo: '/api/placeholder/32/32',
    status: 'active',
    syncedContacts: 8930,
    lastSync: 'Hace 4 horas',
    configuredDate: '25 Feb 2024'
  }
])

const integrationLogs = ref([
  {
    id: 1,
    timestamp: new Date(),
    type: 'sso',
    integration: 'Google Workspace',
    event: 'User Login',
    status: 'success',
    details: 'Usuario john.doe@company.com autenticado exitosamente'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 300000),
    type: 'api',
    integration: 'Slack API',
    event: 'Message Sent',
    status: 'success',
    details: 'Mensaje enviado al canal #general'
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 600000),
    type: 'webhook',
    integration: 'Payment Notifications',
    event: 'Payment Received',
    status: 'success',
    details: 'Pago de $99.00 procesado exitosamente'
  },
  {
    id: 4,
    timestamp: new Date(Date.now() - 900000),
    type: 'crm',
    integration: 'Salesforce',
    event: 'Contact Sync',
    status: 'error',
    details: 'Error al sincronizar contacto: API rate limit exceeded'
  }
])

// Computed
const filteredIntegrationLogs = computed(() => {
  if (logFilter.value === 'all') {
    return integrationLogs.value
  }
  return integrationLogs.value.filter(log => log.type === logFilter.value)
})

// Methods
const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    error: 'Error',
    warning: 'Advertencia',
    success: 'Éxito'
  }
  return labels[status] || status
}

const formatLogTime = (timestamp) => {
  return new Intl.DateTimeFormat('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(timestamp)
}

const refreshIntegrations = async () => {
  isLoading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Refreshing integrations...')
  } catch (error) {
    console.error('Error refreshing integrations:', error)
  } finally {
    isLoading.value = false
  }
}

const openIntegrationModal = () => {
  console.log('Opening integration modal...')
}

// SSO Methods
const configureSSO = (sso) => {
  console.log('Configuring SSO:', sso.name)
}

const testSSO = (sso) => {
  console.log('Testing SSO:', sso.name)
}

const toggleSSO = (sso) => {
  sso.status = sso.status === 'active' ? 'inactive' : 'active'
  console.log(`${sso.status === 'active' ? 'Activated' : 'Deactivated'} SSO:`, sso.name)
}

// API Methods
const configureAPI = (api) => {
  console.log('Configuring API:', api.name)
}

const testAPI = (api) => {
  console.log('Testing API:', api.name)
}

const viewAPILogs = (api) => {
  console.log('Viewing API logs:', api.name)
}

// Webhook Methods
const configureWebhook = (webhook) => {
  console.log('Configuring webhook:', webhook.name)
}

const testWebhook = (webhook) => {
  console.log('Testing webhook:', webhook.name)
}

// CRM Methods
const configureCRM = (crm) => {
  console.log('Configuring CRM:', crm.name)
}

const syncCRM = (crm) => {
  console.log('Syncing CRM:', crm.name)
}

const clearIntegrationLogs = () => {
  integrationLogs.value = []
}

// Lifecycle
onMounted(() => {
  refreshIntegrations()
})
</script>

<style scoped>
.enterprise-integrations {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>