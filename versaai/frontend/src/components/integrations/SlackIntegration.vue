<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg">
            <MessageSquare class="h-6 w-6 text-white" />
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
              Integración con Slack
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Conecta tu workspace de Slack con VersaAI
            </p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <span
            :class="getConnectionStatusClasses()"
            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
          >
            <span :class="getConnectionDotClasses()" class="w-2 h-2 rounded-full mr-2"></span>
            {{ getConnectionStatusLabel() }}
          </span>
          <button
            v-if="!isConnected"
            @click="connectToSlack"
            :disabled="isConnecting"
            class="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors duration-200 disabled:opacity-50"
          >
            <div v-if="isConnecting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            <Zap v-else class="h-4 w-4 mr-2" />
            {{ isConnecting ? 'Conectando...' : 'Conectar con Slack' }}
          </button>
          <button
            v-else
            @click="disconnectFromSlack"
            :disabled="isDisconnecting"
            class="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition-colors duration-200 disabled:opacity-50"
          >
            <div v-if="isDisconnecting" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            <Unplug v-else class="h-4 w-4 mr-2" />
            {{ isDisconnecting ? 'Desconectando...' : 'Desconectar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Connection Status & Info -->
    <div v-if="isConnected" class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Building class="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                Workspace
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ slackConfig.workspaceName || 'No configurado' }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <Users class="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                Canales conectados
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ slackConfig.connectedChannels?.length || 0 }} canales
              </p>
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
              <Clock class="h-5 w-5 text-purple-600 dark:text-purple-400" />
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                Última sincronización
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ formatTimeAgo(slackConfig.lastSync) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Configuration Tabs -->
    <div v-if="isConnected" class="border-b border-gray-200 dark:border-gray-700">
      <nav class="flex space-x-8 px-6" aria-label="Tabs">
        <button
          v-for="tab in configTabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            activeTab === tab.id
              ? 'border-purple-500 text-purple-600 dark:text-purple-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors'
          ]"
        >
          <component :is="tab.icon" class="h-4 w-4 mr-2 inline" />
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- Tab Content -->
    <div v-if="isConnected" class="p-6">
      <!-- Channels Tab -->
      <div v-if="activeTab === 'channels'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white">
            Canales de Slack
          </h4>
          <button
            @click="refreshChannels"
            :disabled="isRefreshingChannels"
            class="inline-flex items-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <RotateCcw v-if="!isRefreshingChannels" class="h-4 w-4 mr-2" />
            <div v-else class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            Actualizar canales
          </button>
        </div>
        
        <div class="grid gap-4">
          <div
            v-for="channel in availableChannels"
            :key="channel.id"
            class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <Hash class="h-5 w-5 text-gray-400" />
              <div>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ channel.name }}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ channel.memberCount }} miembros
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span
                v-if="channel.isConnected"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
              >
                Conectado
              </span>
              <button
                @click="toggleChannelConnection(channel)"
                :disabled="isTogglingChannel === channel.id"
                :class="[
                  channel.isConnected
                    ? 'bg-red-600 hover:bg-red-700'
                    : 'bg-green-600 hover:bg-green-700',
                  'inline-flex items-center px-3 py-1 text-white text-sm font-medium rounded transition-colors disabled:opacity-50'
                ]"
              >
                <div v-if="isTogglingChannel === channel.id" class="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
                {{ channel.isConnected ? 'Desconectar' : 'Conectar' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Notifications Tab -->
      <div v-if="activeTab === 'notifications'" class="space-y-6">
        <h4 class="text-lg font-medium text-gray-900 dark:text-white">
          Configuración de Notificaciones
        </h4>
        
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">
                Notificar nuevas conversaciones
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Envía una notificación cuando se inicia una nueva conversación
              </p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="notificationSettings.newConversations"
                type="checkbox"
                class="sr-only peer"
                @change="updateNotificationSettings"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">
                Notificar mensajes importantes
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Envía notificaciones para mensajes marcados como importantes
              </p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="notificationSettings.importantMessages"
                type="checkbox"
                class="sr-only peer"
                @change="updateNotificationSettings"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <div>
              <p class="font-medium text-gray-900 dark:text-white">
                Resumen diario
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Envía un resumen diario de la actividad
              </p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input
                v-model="notificationSettings.dailySummary"
                type="checkbox"
                class="sr-only peer"
                @change="updateNotificationSettings"
              />
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
            </label>
          </div>
        </div>
      </div>

      <!-- Automation Tab -->
      <div v-if="activeTab === 'automation'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h4 class="text-lg font-medium text-gray-900 dark:text-white">
            Reglas de Automatización
          </h4>
          <button
            @click="showCreateRuleModal = true"
            class="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors"
          >
            <Plus class="h-4 w-4 mr-2" />
            Nueva regla
          </button>
        </div>
        
        <div v-if="automationRules.length === 0" class="text-center py-8">
          <Zap class="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No hay reglas de automatización
          </h3>
          <p class="text-gray-500 dark:text-gray-400 mb-4">
            Crea reglas para automatizar acciones basadas en eventos de Slack
          </p>
        </div>
        
        <div v-else class="space-y-4">
          <div
            v-for="rule in automationRules"
            :key="rule.id"
            class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h5 class="font-medium text-gray-900 dark:text-white mb-2">
                  {{ rule.name }}
                </h5>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {{ rule.description }}
                </p>
                <div class="flex items-center space-x-4 text-sm">
                  <span class="text-gray-500 dark:text-gray-400">
                    Trigger: <span class="font-medium">{{ rule.trigger }}</span>
                  </span>
                  <span class="text-gray-500 dark:text-gray-400">
                    Acción: <span class="font-medium">{{ rule.action }}</span>
                  </span>
                </div>
              </div>
              <div class="flex items-center space-x-2 ml-4">
                <label class="relative inline-flex items-center cursor-pointer">
                  <input
                    v-model="rule.isActive"
                    type="checkbox"
                    class="sr-only peer"
                    @change="toggleRule(rule)"
                  />
                  <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
                </label>
                <button
                  @click="editRule(rule)"
                  class="p-2 text-gray-400 hover:text-yellow-600 dark:hover:text-yellow-400 transition-colors"
                >
                  <Edit class="h-4 w-4" />
                </button>
                <button
                  @click="deleteRule(rule)"
                  class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                >
                  <Trash2 class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Tab -->
      <div v-if="activeTab === 'analytics'" class="space-y-6">
        <h4 class="text-lg font-medium text-gray-900 dark:text-white">
          Métricas de Slack
        </h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-blue-100 text-sm font-medium">
                  Mensajes enviados
                </p>
                <p class="text-2xl font-bold">
                  {{ formatNumber(slackMetrics.messagesSent) }}
                </p>
              </div>
              <MessageSquare class="h-8 w-8 text-blue-200" />
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-green-100 text-sm font-medium">
                  Mensajes recibidos
                </p>
                <p class="text-2xl font-bold">
                  {{ formatNumber(slackMetrics.messagesReceived) }}
                </p>
              </div>
              <MessageCircle class="h-8 w-8 text-green-200" />
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-purple-100 text-sm font-medium">
                  Canales activos
                </p>
                <p class="text-2xl font-bold">
                  {{ slackMetrics.activeChannels }}
                </p>
              </div>
              <Hash class="h-8 w-8 text-purple-200" />
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-orange-100 text-sm font-medium">
                  Tiempo de respuesta
                </p>
                <p class="text-2xl font-bold">
                  {{ slackMetrics.avgResponseTime }}s
                </p>
              </div>
              <Clock class="h-8 w-8 text-orange-200" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Setup Instructions for non-connected state -->
    <div v-if="!isConnected" class="p-6">
      <div class="max-w-2xl mx-auto text-center">
        <div class="mb-8">
          <div class="mx-auto w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center mb-4">
            <MessageSquare class="h-8 w-8 text-white" />
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Conecta tu workspace de Slack
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Integra VersaAI con Slack para recibir notificaciones y automatizar flujos de trabajo
          </p>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-6 mb-6">
          <h4 class="font-medium text-gray-900 dark:text-white mb-4">
            Beneficios de la integración:
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-400">
            <div class="flex items-center space-x-2">
              <CheckCircle class="h-4 w-4 text-green-500" />
              <span>Notificaciones en tiempo real</span>
            </div>
            <div class="flex items-center space-x-2">
              <CheckCircle class="h-4 w-4 text-green-500" />
              <span>Automatización de respuestas</span>
            </div>
            <div class="flex items-center space-x-2">
              <CheckCircle class="h-4 w-4 text-green-500" />
              <span>Sincronización de conversaciones</span>
            </div>
            <div class="flex items-center space-x-2">
              <CheckCircle class="h-4 w-4 text-green-500" />
              <span>Métricas y analytics</span>
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
  MessageSquare,
  Zap,
  Unplug,
  Building,
  Users,
  Clock,
  Hash,
  RotateCcw,
  Plus,
  Edit,
  Trash2,
  CheckCircle,
  MessageCircle,
  BarChart3
} from 'lucide-vue-next'
import { useSlackIntegration } from '@/composables/useSlackIntegration'
import { useNotifications } from '@/composables/useNotifications'

// Composables
const { showNotification } = useNotifications()

// Reactive state
const isConnected = ref(false)
const isConnecting = ref(false)
const isDisconnecting = ref(false)
const isRefreshingChannels = ref(false)
const isTogglingChannel = ref(null)
const activeTab = ref('channels')
const showCreateRuleModal = ref(false)

// Configuration data
const slackConfig = ref({
  workspaceName: 'VersaAI Team',
  connectedChannels: [
    { id: 'general', name: 'general', isConnected: true },
    { id: 'support', name: 'support', isConnected: true }
  ],
  lastSync: new Date()
})

const availableChannels = ref([
  { id: 'general', name: 'general', memberCount: 25, isConnected: true },
  { id: 'support', name: 'support', memberCount: 12, isConnected: true },
  { id: 'development', name: 'development', memberCount: 8, isConnected: false },
  { id: 'marketing', name: 'marketing', memberCount: 15, isConnected: false },
  { id: 'sales', name: 'sales', memberCount: 10, isConnected: false }
])

const notificationSettings = ref({
  newConversations: true,
  importantMessages: true,
  dailySummary: false
})

const automationRules = ref([
  {
    id: 1,
    name: 'Auto-respuesta fuera de horario',
    description: 'Envía una respuesta automática cuando se recibe un mensaje fuera del horario laboral',
    trigger: 'Mensaje fuera de horario',
    action: 'Enviar auto-respuesta',
    isActive: true
  },
  {
    id: 2,
    name: 'Escalación de urgencias',
    description: 'Notifica al equipo de soporte cuando se detecta una urgencia',
    trigger: 'Palabra clave: urgente',
    action: 'Notificar equipo',
    isActive: false
  }
])

const slackMetrics = ref({
  messagesSent: 1247,
  messagesReceived: 892,
  activeChannels: 5,
  avgResponseTime: 2.3
})

// Configuration tabs
const configTabs = [
  { id: 'channels', name: 'Canales', icon: Hash },
  { id: 'notifications', name: 'Notificaciones', icon: MessageCircle },
  { id: 'automation', name: 'Automatización', icon: Zap },
  { id: 'analytics', name: 'Métricas', icon: BarChart3 }
]

// Computed properties
const getConnectionStatusClasses = () => {
  return isConnected.value
    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
    : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
}

const getConnectionDotClasses = () => {
  return isConnected.value ? 'bg-green-400' : 'bg-red-400'
}

const getConnectionStatusLabel = () => {
  return isConnected.value ? 'Conectado' : 'Desconectado'
}

// Methods
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

const connectToSlack = async () => {
  isConnecting.value = true
  try {
    // Simulate OAuth flow
    await new Promise(resolve => setTimeout(resolve, 2000))
    isConnected.value = true
    showNotification('Conectado exitosamente con Slack', 'success')
  } catch (error) {
    showNotification('Error al conectar con Slack', 'error')
  } finally {
    isConnecting.value = false
  }
}

const disconnectFromSlack = async () => {
  if (confirm('¿Estás seguro de que quieres desconectar Slack? Se perderán todas las configuraciones.')) {
    isDisconnecting.value = true
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      isConnected.value = false
      showNotification('Desconectado de Slack exitosamente', 'success')
    } catch (error) {
      showNotification('Error al desconectar de Slack', 'error')
    } finally {
      isDisconnecting.value = false
    }
  }
}

const refreshChannels = async () => {
  isRefreshingChannels.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    showNotification('Canales actualizados', 'success')
  } catch (error) {
    showNotification('Error al actualizar canales', 'error')
  } finally {
    isRefreshingChannels.value = false
  }
}

const toggleChannelConnection = async (channel) => {
  isTogglingChannel.value = channel.id
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    channel.isConnected = !channel.isConnected
    const action = channel.isConnected ? 'conectado' : 'desconectado'
    showNotification(`Canal ${channel.name} ${action}`, 'success')
  } catch (error) {
    showNotification('Error al cambiar conexión del canal', 'error')
  } finally {
    isTogglingChannel.value = null
  }
}

const updateNotificationSettings = async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 300))
    showNotification('Configuración de notificaciones actualizada', 'success')
  } catch (error) {
    showNotification('Error al actualizar configuración', 'error')
  }
}

const toggleRule = async (rule) => {
  try {
    await new Promise(resolve => setTimeout(resolve, 300))
    const action = rule.isActive ? 'activada' : 'desactivada'
    showNotification(`Regla ${action}`, 'success')
  } catch (error) {
    showNotification('Error al cambiar estado de la regla', 'error')
  }
}

const editRule = (rule) => {
  // Implementation for editing rule
  showNotification('Función de edición en desarrollo', 'info')
}

const deleteRule = async (rule) => {
  if (confirm(`¿Estás seguro de que quieres eliminar la regla "${rule.name}"?`)) {
    try {
      const index = automationRules.value.findIndex(r => r.id === rule.id)
      if (index > -1) {
        automationRules.value.splice(index, 1)
        showNotification('Regla eliminada exitosamente', 'success')
      }
    } catch (error) {
      showNotification('Error al eliminar regla', 'error')
    }
  }
}

// Lifecycle
onMounted(() => {
  // Check if already connected
  isConnected.value = true // Simulate connected state
})
</script>