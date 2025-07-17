import { ref, reactive, computed } from 'vue'
import { useNotifications } from '@/composables/useNotifications'
import { useAuth } from '@/composables/useAuth'
import { api } from '@/config/api'

// Global state for integrations
const integrationsState = reactive({
  integrations: [],
  stats: {
    active: 0,
    activeGrowth: 0,
    totalRequests: 0,
    requestsGrowth: 0,
    successRate: 0,
    successRateGrowth: 0,
    avgResponseTime: 0,
    responseTimeImprovement: 0
  },
  isLoading: false,
  lastUpdated: null
})

// Mock data for development
const mockIntegrations = [
  {
    id: 'slack-001',
    name: 'Slack',
    description: 'Integración con Slack para notificaciones y comunicación en tiempo real',
    category: 'communication',
    status: 'active',
    icon: 'MessageSquare',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 15420,
      successRate: 99.2,
      avgResponseTime: 145,
      lastUsed: new Date(Date.now() - 300000),
      uptime: 99.8
    },
    config: {
      webhookUrl: 'https://hooks.slack.com/services/...',
      channels: ['#general', '#alerts', '#support'],
      botToken: 'xoxb-***'
    },
    webhooks: [
      {
        id: 'wh-001',
        name: 'Chat Notifications',
        url: 'https://api.versaai.com/webhooks/slack/chat',
        events: ['message.sent', 'conversation.started'],
        status: 'active'
      }
    ],
    apiKeys: [
      {
        id: 'api-001',
        name: 'Slack Bot Token',
        type: 'bearer',
        lastUsed: new Date(Date.now() - 3600000),
        status: 'active'
      }
    ]
  },
  {
    id: 'teams-001',
    name: 'Microsoft Teams',
    description: 'Integración con Microsoft Teams para colaboración empresarial',
    category: 'communication',
    status: 'inactive',
    icon: 'Users',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 8930,
      successRate: 98.5,
      avgResponseTime: 210,
      lastUsed: new Date(Date.now() - 86400000),
      uptime: 98.2
    },
    config: {
      tenantId: 'tenant-id',
      clientId: 'client-id',
      channels: ['General', 'VersaAI Alerts']
    }
  },
  {
    id: 'whatsapp-001',
    name: 'WhatsApp Business',
    description: 'Integración con WhatsApp Business API para comunicación directa con clientes',
    category: 'communication',
    status: 'active',
    icon: 'MessageCircle',
    isPopular: true,
    isPremium: true,
    metrics: {
      totalRequests: 25680,
      successRate: 97.8,
      avgResponseTime: 320,
      lastUsed: new Date(Date.now() - 120000),
      uptime: 99.1
    },
    config: {
      phoneNumberId: 'phone-id',
      accessToken: 'access-token',
      webhookVerifyToken: 'verify-token'
    }
  },
  {
    id: 'salesforce-001',
    name: 'Salesforce',
    description: 'Integración con Salesforce CRM para gestión de leads y oportunidades',
    category: 'crm',
    status: 'active',
    icon: 'Building',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 12450,
      successRate: 99.5,
      avgResponseTime: 180,
      lastUsed: new Date(Date.now() - 1800000),
      uptime: 99.9
    },
    config: {
      instanceUrl: 'https://company.salesforce.com',
      clientId: 'client-id',
      clientSecret: 'client-secret'
    }
  },
  {
    id: 'hubspot-001',
    name: 'HubSpot',
    description: 'Integración con HubSpot para marketing automation y CRM',
    category: 'crm',
    status: 'active',
    icon: 'Target',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 9870,
      successRate: 98.9,
      avgResponseTime: 165,
      lastUsed: new Date(Date.now() - 900000),
      uptime: 99.3
    },
    config: {
      apiKey: 'hubspot-api-key',
      portalId: 'portal-id'
    }
  },
  {
    id: 'pipedrive-001',
    name: 'Pipedrive',
    description: 'Integración con Pipedrive para gestión de pipeline de ventas',
    category: 'crm',
    status: 'inactive',
    icon: 'TrendingUp',
    isPopular: false,
    isPremium: false,
    metrics: {
      totalRequests: 5420,
      successRate: 97.2,
      avgResponseTime: 195,
      lastUsed: new Date(Date.now() - 172800000),
      uptime: 97.8
    },
    config: {
      apiToken: 'pipedrive-token',
      companyDomain: 'company.pipedrive.com'
    }
  },
  {
    id: 'zapier-001',
    name: 'Zapier',
    description: 'Integración con Zapier para automatización de workflows',
    category: 'automation',
    status: 'active',
    icon: 'Zap',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 18750,
      successRate: 99.1,
      avgResponseTime: 125,
      lastUsed: new Date(Date.now() - 600000),
      uptime: 99.6
    },
    config: {
      webhookUrl: 'https://hooks.zapier.com/hooks/catch/...',
      apiKey: 'zapier-api-key'
    }
  },
  {
    id: 'make-001',
    name: 'Make.com',
    description: 'Integración con Make.com (anteriormente Integromat) para automatización avanzada',
    category: 'automation',
    status: 'active',
    icon: 'Settings',
    isPopular: false,
    isPremium: true,
    metrics: {
      totalRequests: 7890,
      successRate: 98.7,
      avgResponseTime: 155,
      lastUsed: new Date(Date.now() - 1200000),
      uptime: 98.9
    },
    config: {
      webhookUrl: 'https://hook.integromat.com/...',
      apiKey: 'make-api-key'
    }
  },
  {
    id: 'google-analytics-001',
    name: 'Google Analytics',
    description: 'Integración con Google Analytics para tracking y análisis de conversaciones',
    category: 'analytics',
    status: 'active',
    icon: 'BarChart3',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 22100,
      successRate: 99.8,
      avgResponseTime: 95,
      lastUsed: new Date(Date.now() - 180000),
      uptime: 99.9
    },
    config: {
      trackingId: 'GA-XXXXXXX-X',
      propertyId: 'property-id',
      measurementId: 'G-XXXXXXXXXX'
    }
  },
  {
    id: 'mixpanel-001',
    name: 'Mixpanel',
    description: 'Integración con Mixpanel para análisis avanzado de eventos y comportamiento',
    category: 'analytics',
    status: 'inactive',
    icon: 'PieChart',
    isPopular: false,
    isPremium: true,
    metrics: {
      totalRequests: 6540,
      successRate: 98.3,
      avgResponseTime: 110,
      lastUsed: new Date(Date.now() - 259200000),
      uptime: 98.5
    },
    config: {
      projectToken: 'mixpanel-token',
      apiSecret: 'mixpanel-secret'
    }
  },
  {
    id: 'stripe-001',
    name: 'Stripe',
    description: 'Integración con Stripe para procesamiento de pagos y suscripciones',
    category: 'payment',
    status: 'active',
    icon: 'CreditCard',
    isPopular: true,
    isPremium: false,
    metrics: {
      totalRequests: 13680,
      successRate: 99.9,
      avgResponseTime: 85,
      lastUsed: new Date(Date.now() - 240000),
      uptime: 99.99
    },
    config: {
      publishableKey: 'pk_live_...',
      secretKey: 'sk_live_...',
      webhookSecret: 'whsec_...'
    }
  },
  {
    id: 'paypal-001',
    name: 'PayPal',
    description: 'Integración con PayPal para pagos alternativos y procesamiento global',
    category: 'payment',
    status: 'inactive',
    icon: 'Wallet',
    isPopular: false,
    isPremium: false,
    metrics: {
      totalRequests: 4320,
      successRate: 98.1,
      avgResponseTime: 220,
      lastUsed: new Date(Date.now() - 432000000),
      uptime: 97.9
    },
    config: {
      clientId: 'paypal-client-id',
      clientSecret: 'paypal-client-secret',
      mode: 'live'
    }
  }
]

// Mock stats
const mockStats = {
  active: 8,
  activeGrowth: 3,
  totalRequests: 156420,
  requestsGrowth: 12.5,
  successRate: 98.9,
  successRateGrowth: 1.2,
  avgResponseTime: 165,
  responseTimeImprovement: 25
}

export function useIntegrations() {
  const { showError, showSuccess } = useNotifications()
  const { isAuthenticated } = useAuth()

  // Initialize with mock data
  if (integrationsState.integrations.length === 0) {
    integrationsState.integrations = mockIntegrations
    integrationsState.stats = mockStats
  }

  // Computed properties
  const activeIntegrations = computed(() => 
    integrationsState.integrations.filter(integration => integration.status === 'active')
  )

  const popularIntegrations = computed(() => 
    integrationsState.integrations.filter(integration => integration.isPopular)
  )

  const integrationsByCategory = computed(() => {
    const categories = {}
    integrationsState.integrations.forEach(integration => {
      if (!categories[integration.category]) {
        categories[integration.category] = []
      }
      categories[integration.category].push(integration)
    })
    return categories
  })

  // Methods
  const refreshIntegrations = async () => {
    if (!isAuthenticated.value) {
      showError('Debes estar autenticado para acceder a las integraciones')
      return
    }

    try {
      integrationsState.isLoading = true
      
      // TODO: Replace with real API call
      // const response = await api.integrations.getAll()
      // integrationsState.integrations = response.data.integrations
      // integrationsState.stats = response.data.stats
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Update stats to simulate real-time data
      integrationsState.stats = {
        ...mockStats,
        totalRequests: mockStats.totalRequests + Math.floor(Math.random() * 1000),
        successRate: Math.round((mockStats.successRate + Math.random() * 0.5) * 10) / 10
      }
      
      integrationsState.lastUpdated = new Date()
      
    } catch (error) {
      console.error('Error refreshing integrations:', error)
      showError('Error al actualizar las integraciones')
      throw error
    } finally {
      integrationsState.isLoading = false
    }
  }

  const getIntegrationById = (id) => {
    return integrationsState.integrations.find(integration => integration.id === id)
  }

  const toggleIntegration = async (integrationId) => {
    try {
      const integration = getIntegrationById(integrationId)
      if (!integration) {
        throw new Error('Integración no encontrada')
      }

      // TODO: Replace with real API call
      // await api.integrations.toggle(integrationId)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Update local state
      integration.status = integration.status === 'active' ? 'inactive' : 'active'
      
      // Update stats
      if (integration.status === 'active') {
        integrationsState.stats.active++
      } else {
        integrationsState.stats.active--
      }
      
      showSuccess(`Integración ${integration.name} ${integration.status === 'active' ? 'activada' : 'desactivada'}`)
      
    } catch (error) {
      console.error('Error toggling integration:', error)
      showError('Error al cambiar el estado de la integración')
      throw error
    }
  }

  const testIntegration = async (integrationId) => {
    try {
      const integration = getIntegrationById(integrationId)
      if (!integration) {
        throw new Error('Integración no encontrada')
      }

      // TODO: Replace with real API call
      // const response = await api.integrations.test(integrationId)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Simulate random success/failure
      const success = Math.random() > 0.1 // 90% success rate
      
      if (success) {
        showSuccess(`Test de ${integration.name} ejecutado correctamente`)
        return { success: true, responseTime: Math.floor(Math.random() * 200) + 50 }
      } else {
        throw new Error('Test fallido')
      }
      
    } catch (error) {
      console.error('Error testing integration:', error)
      showError(`Error al probar la integración: ${error.message}`)
      throw error
    }
  }

  const updateIntegrationConfig = async (integrationId, config) => {
    try {
      const integration = getIntegrationById(integrationId)
      if (!integration) {
        throw new Error('Integración no encontrada')
      }

      // TODO: Replace with real API call
      // await api.integrations.updateConfig(integrationId, config)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Update local state
      integration.config = { ...integration.config, ...config }
      
      showSuccess(`Configuración de ${integration.name} actualizada`)
      
    } catch (error) {
      console.error('Error updating integration config:', error)
      showError('Error al actualizar la configuración')
      throw error
    }
  }

  const getIntegrationMetrics = async (integrationId, timeRange = '7d') => {
    try {
      const integration = getIntegrationById(integrationId)
      if (!integration) {
        throw new Error('Integración no encontrada')
      }

      // TODO: Replace with real API call
      // const response = await api.integrations.getMetrics(integrationId, timeRange)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Return mock metrics
      return {
        requests: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(Date.now() - (6 - i) * 24 * 60 * 60 * 1000),
          count: Math.floor(Math.random() * 1000) + 500
        })),
        successRate: integration.metrics.successRate,
        avgResponseTime: integration.metrics.avgResponseTime,
        errors: Array.from({ length: 5 }, (_, i) => ({
          timestamp: new Date(Date.now() - i * 60 * 60 * 1000),
          message: `Error de ejemplo ${i + 1}`,
          type: 'connection_error'
        }))
      }
      
    } catch (error) {
      console.error('Error getting integration metrics:', error)
      showError('Error al obtener las métricas')
      throw error
    }
  }

  return {
    // State
    integrations: computed(() => integrationsState.integrations),
    stats: computed(() => integrationsState.stats),
    isLoading: computed(() => integrationsState.isLoading),
    lastUpdated: computed(() => integrationsState.lastUpdated),
    
    // Computed
    activeIntegrations,
    popularIntegrations,
    integrationsByCategory,
    
    // Methods
    refreshIntegrations,
    getIntegrationById,
    toggleIntegration,
    testIntegration,
    updateIntegrationConfig,
    getIntegrationMetrics
  }
}

// Composable for webhook management
export function useWebhooks() {
  const { showError, showSuccess } = useNotifications()
  
  const webhooks = ref([])
  const isLoading = ref(false)
  
  const createWebhook = async (webhookData) => {
    try {
      isLoading.value = true
      
      // TODO: Replace with real API call
      // const response = await api.webhooks.create(webhookData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newWebhook = {
        id: `wh-${Date.now()}`,
        ...webhookData,
        status: 'active',
        createdAt: new Date()
      }
      
      webhooks.value.push(newWebhook)
      showSuccess('Webhook creado correctamente')
      
      return newWebhook
      
    } catch (error) {
      console.error('Error creating webhook:', error)
      showError('Error al crear el webhook')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const updateWebhook = async (webhookId, webhookData) => {
    try {
      isLoading.value = true
      
      // TODO: Replace with real API call
      // await api.webhooks.update(webhookId, webhookData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const index = webhooks.value.findIndex(wh => wh.id === webhookId)
      if (index !== -1) {
        webhooks.value[index] = { ...webhooks.value[index], ...webhookData }
      }
      
      showSuccess('Webhook actualizado correctamente')
      
    } catch (error) {
      console.error('Error updating webhook:', error)
      showError('Error al actualizar el webhook')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const deleteWebhook = async (webhookId) => {
    try {
      isLoading.value = true
      
      // TODO: Replace with real API call
      // await api.webhooks.delete(webhookId)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const index = webhooks.value.findIndex(wh => wh.id === webhookId)
      if (index !== -1) {
        webhooks.value.splice(index, 1)
      }
      
      showSuccess('Webhook eliminado correctamente')
      
    } catch (error) {
      console.error('Error deleting webhook:', error)
      showError('Error al eliminar el webhook')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    webhooks,
    isLoading,
    createWebhook,
    updateWebhook,
    deleteWebhook
  }
}

// Composable for API key management
export function useAPIKeys() {
  const { showError, showSuccess } = useNotifications()
  
  const apiKeys = ref([])
  const isLoading = ref(false)
  
  const createAPIKey = async (keyData) => {
    try {
      isLoading.value = true
      
      // TODO: Replace with real API call
      // const response = await api.apiKeys.create(keyData)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const newKey = {
        id: `key-${Date.now()}`,
        ...keyData,
        key: `vsa_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`,
        status: 'active',
        createdAt: new Date(),
        lastUsed: null
      }
      
      apiKeys.value.push(newKey)
      showSuccess('API Key creada correctamente')
      
      return newKey
      
    } catch (error) {
      console.error('Error creating API key:', error)
      showError('Error al crear la API key')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const revokeAPIKey = async (keyId) => {
    try {
      isLoading.value = true
      
      // TODO: Replace with real API call
      // await api.apiKeys.revoke(keyId)
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const key = apiKeys.value.find(k => k.id === keyId)
      if (key) {
        key.status = 'revoked'
      }
      
      showSuccess('API Key revocada correctamente')
      
    } catch (error) {
      console.error('Error revoking API key:', error)
      showError('Error al revocar la API key')
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    apiKeys,
    isLoading,
    createAPIKey,
    revokeAPIKey
  }
}