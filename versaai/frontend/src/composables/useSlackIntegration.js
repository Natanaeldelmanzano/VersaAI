import { ref, reactive } from 'vue'
import { useNotifications } from './useNotifications'

// Global state for Slack integration
const slackState = reactive({
  isConnected: false,
  workspaceInfo: null,
  connectedChannels: [],
  settings: {
    notifications: {
      newConversations: true,
      importantMessages: true,
      dailySummary: false,
      mentionsOnly: false
    },
    automation: {
      autoResponses: true,
      escalationRules: false,
      workingHours: {
        enabled: true,
        start: '09:00',
        end: '18:00',
        timezone: 'America/Mexico_City'
      }
    }
  },
  metrics: {
    messagesSent: 0,
    messagesReceived: 0,
    activeChannels: 0,
    avgResponseTime: 0,
    lastSync: null
  }
})

// Mock data for development
const mockWorkspaceInfo = {
  id: 'T1234567890',
  name: 'VersaAI Team',
  domain: 'versaai',
  url: 'https://versaai.slack.com',
  icon: 'https://avatars.slack-edge.com/2023-01-01/1234567890_abc123def456_132.png'
}

const mockChannels = [
  {
    id: 'C1234567890',
    name: 'general',
    isPrivate: false,
    memberCount: 25,
    purpose: 'Canal general del equipo',
    isConnected: true,
    lastActivity: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
  },
  {
    id: 'C1234567891',
    name: 'support',
    isPrivate: false,
    memberCount: 12,
    purpose: 'Canal de soporte al cliente',
    isConnected: true,
    lastActivity: new Date(Date.now() - 1000 * 60 * 15) // 15 minutes ago
  },
  {
    id: 'C1234567892',
    name: 'development',
    isPrivate: false,
    memberCount: 8,
    purpose: 'Discusiones de desarrollo',
    isConnected: false,
    lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
  },
  {
    id: 'C1234567893',
    name: 'marketing',
    isPrivate: false,
    memberCount: 15,
    purpose: 'Estrategias de marketing',
    isConnected: false,
    lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 4) // 4 hours ago
  },
  {
    id: 'C1234567894',
    name: 'sales',
    isPrivate: false,
    memberCount: 10,
    purpose: 'Equipo de ventas',
    isConnected: false,
    lastActivity: new Date(Date.now() - 1000 * 60 * 60 * 6) // 6 hours ago
  }
]

const mockAutomationRules = [
  {
    id: 'rule_1',
    name: 'Auto-respuesta fuera de horario',
    description: 'Envía una respuesta automática cuando se recibe un mensaje fuera del horario laboral',
    trigger: {
      type: 'time_based',
      condition: 'outside_working_hours'
    },
    action: {
      type: 'send_message',
      template: 'Gracias por tu mensaje. Nuestro horario de atención es de 9:00 AM a 6:00 PM. Te responderemos lo antes posible.'
    },
    isActive: true,
    createdAt: new Date('2024-01-15'),
    lastTriggered: new Date(Date.now() - 1000 * 60 * 60 * 12) // 12 hours ago
  },
  {
    id: 'rule_2',
    name: 'Escalación de urgencias',
    description: 'Notifica al equipo de soporte cuando se detecta una urgencia',
    trigger: {
      type: 'keyword',
      keywords: ['urgente', 'emergency', 'crítico', 'down']
    },
    action: {
      type: 'notify_team',
      channels: ['#support'],
      users: ['@support-lead']
    },
    isActive: false,
    createdAt: new Date('2024-01-10'),
    lastTriggered: new Date(Date.now() - 1000 * 60 * 60 * 24 * 3) // 3 days ago
  },
  {
    id: 'rule_3',
    name: 'Bienvenida a nuevos miembros',
    description: 'Envía un mensaje de bienvenida cuando un nuevo miembro se une al workspace',
    trigger: {
      type: 'user_joined',
      condition: 'new_member'
    },
    action: {
      type: 'send_dm',
      template: '¡Bienvenido al equipo de VersaAI! 🎉 Si tienes alguna pregunta, no dudes en contactarnos.'
    },
    isActive: true,
    createdAt: new Date('2024-01-20'),
    lastTriggered: new Date(Date.now() - 1000 * 60 * 60 * 24) // 1 day ago
  }
]

export function useSlackIntegration() {
  const { showNotification } = useNotifications()
  
  const isLoading = ref(false)
  const error = ref(null)
  
  // Connection methods
  const connectToSlack = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      // Simulate OAuth flow
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock successful connection
      slackState.isConnected = true
      slackState.workspaceInfo = mockWorkspaceInfo
      slackState.connectedChannels = mockChannels.filter(ch => ch.isConnected)
      slackState.metrics = {
        messagesSent: 1247,
        messagesReceived: 892,
        activeChannels: slackState.connectedChannels.length,
        avgResponseTime: 2.3,
        lastSync: new Date()
      }
      
      showNotification('Conectado exitosamente con Slack', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al conectar con Slack', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const disconnectFromSlack = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Reset state
      slackState.isConnected = false
      slackState.workspaceInfo = null
      slackState.connectedChannels = []
      slackState.metrics = {
        messagesSent: 0,
        messagesReceived: 0,
        activeChannels: 0,
        avgResponseTime: 0,
        lastSync: null
      }
      
      showNotification('Desconectado de Slack exitosamente', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al desconectar de Slack', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Channel management
  const getAvailableChannels = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 800))
      return { success: true, data: mockChannels }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const connectChannel = async (channelId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const channel = mockChannels.find(ch => ch.id === channelId)
      if (channel) {
        channel.isConnected = true
        if (!slackState.connectedChannels.find(ch => ch.id === channelId)) {
          slackState.connectedChannels.push(channel)
        }
        slackState.metrics.activeChannels = slackState.connectedChannels.length
      }
      
      showNotification(`Canal ${channel?.name} conectado exitosamente`, 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al conectar canal', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const disconnectChannel = async (channelId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const channel = mockChannels.find(ch => ch.id === channelId)
      if (channel) {
        channel.isConnected = false
        slackState.connectedChannels = slackState.connectedChannels.filter(ch => ch.id !== channelId)
        slackState.metrics.activeChannels = slackState.connectedChannels.length
      }
      
      showNotification(`Canal ${channel?.name} desconectado`, 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al desconectar canal', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Settings management
  const updateNotificationSettings = async (settings) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 300))
      
      slackState.settings.notifications = { ...slackState.settings.notifications, ...settings }
      
      showNotification('Configuración de notificaciones actualizada', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al actualizar configuración', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const updateAutomationSettings = async (settings) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 300))
      
      slackState.settings.automation = { ...slackState.settings.automation, ...settings }
      
      showNotification('Configuración de automatización actualizada', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al actualizar configuración', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Automation rules
  const getAutomationRules = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 500))
      return { success: true, data: mockAutomationRules }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const createAutomationRule = async (ruleData) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const newRule = {
        id: `rule_${Date.now()}`,
        ...ruleData,
        isActive: true,
        createdAt: new Date(),
        lastTriggered: null
      }
      
      mockAutomationRules.push(newRule)
      
      showNotification('Regla de automatización creada exitosamente', 'success')
      return { success: true, data: newRule }
    } catch (err) {
      error.value = err.message
      showNotification('Error al crear regla de automatización', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const updateAutomationRule = async (ruleId, ruleData) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 600))
      
      const ruleIndex = mockAutomationRules.findIndex(rule => rule.id === ruleId)
      if (ruleIndex > -1) {
        mockAutomationRules[ruleIndex] = { ...mockAutomationRules[ruleIndex], ...ruleData }
        showNotification('Regla de automatización actualizada', 'success')
        return { success: true, data: mockAutomationRules[ruleIndex] }
      } else {
        throw new Error('Regla no encontrada')
      }
    } catch (err) {
      error.value = err.message
      showNotification('Error al actualizar regla', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const deleteAutomationRule = async (ruleId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 400))
      
      const ruleIndex = mockAutomationRules.findIndex(rule => rule.id === ruleId)
      if (ruleIndex > -1) {
        mockAutomationRules.splice(ruleIndex, 1)
        showNotification('Regla de automatización eliminada', 'success')
        return { success: true }
      } else {
        throw new Error('Regla no encontrada')
      }
    } catch (err) {
      error.value = err.message
      showNotification('Error al eliminar regla', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const toggleAutomationRule = async (ruleId) => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 300))
      
      const rule = mockAutomationRules.find(rule => rule.id === ruleId)
      if (rule) {
        rule.isActive = !rule.isActive
        const action = rule.isActive ? 'activada' : 'desactivada'
        showNotification(`Regla ${action}`, 'success')
        return { success: true, data: rule }
      } else {
        throw new Error('Regla no encontrada')
      }
    } catch (err) {
      error.value = err.message
      showNotification('Error al cambiar estado de la regla', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Metrics and analytics
  const getMetrics = async (timeRange = '7d') => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 600))
      
      // Mock metrics based on time range
      const baseMetrics = slackState.metrics
      const multiplier = timeRange === '30d' ? 4 : timeRange === '7d' ? 1 : 0.3
      
      const metrics = {
        ...baseMetrics,
        messagesSent: Math.floor(baseMetrics.messagesSent * multiplier),
        messagesReceived: Math.floor(baseMetrics.messagesReceived * multiplier),
        timeRange,
        generatedAt: new Date()
      }
      
      return { success: true, data: metrics }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const syncData = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Update last sync time
      slackState.metrics.lastSync = new Date()
      
      // Simulate updated metrics
      slackState.metrics.messagesSent += Math.floor(Math.random() * 50)
      slackState.metrics.messagesReceived += Math.floor(Math.random() * 30)
      slackState.metrics.avgResponseTime = Math.round((Math.random() * 3 + 1) * 10) / 10
      
      showNotification('Datos sincronizados exitosamente', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al sincronizar datos', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  // Test connection
  const testConnection = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      if (!slackState.isConnected) {
        throw new Error('No hay conexión activa con Slack')
      }
      
      showNotification('Conexión con Slack verificada exitosamente', 'success')
      return { success: true }
    } catch (err) {
      error.value = err.message
      showNotification('Error al verificar conexión', 'error')
      return { success: false, error: err.message }
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    // State
    slackState,
    isLoading,
    error,
    
    // Connection
    connectToSlack,
    disconnectFromSlack,
    testConnection,
    
    // Channels
    getAvailableChannels,
    connectChannel,
    disconnectChannel,
    
    // Settings
    updateNotificationSettings,
    updateAutomationSettings,
    
    // Automation
    getAutomationRules,
    createAutomationRule,
    updateAutomationRule,
    deleteAutomationRule,
    toggleAutomationRule,
    
    // Analytics
    getMetrics,
    syncData
  }
}

// Export state for direct access if needed
export { slackState }