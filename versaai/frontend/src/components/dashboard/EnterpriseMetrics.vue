<template>
  <div class="enterprise-metrics space-y-6">
    <!-- Header con filtros de tiempo -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Métricas Empresariales</h2>
        <p class="text-gray-600 mt-1">Dashboard en tiempo real con analytics avanzados</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Selector de período -->
        <select 
          v-model="selectedPeriod" 
          @change="refreshMetrics"
          class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          <option value="1h">Última hora</option>
          <option value="24h">Últimas 24h</option>
          <option value="7d">Últimos 7 días</option>
          <option value="30d">Últimos 30 días</option>
          <option value="90d">Últimos 90 días</option>
        </select>
        
        <!-- Botón de actualización -->
        <button 
          @click="refreshMetrics" 
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          <ArrowPathIcon 
            :class="['w-4 h-4 mr-2', { 'animate-spin': isLoading }]" 
          />
          Actualizar
        </button>
        
        <!-- Indicador de tiempo real -->
        <div class="flex items-center text-sm text-gray-500">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></div>
          Tiempo real
        </div>
      </div>
    </div>

    <!-- KPIs principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <MetricCard
        v-for="metric in mainKPIs"
        :key="metric.key"
        :title="metric.title"
        :value="metric.value"
        :change="metric.change"
        :trend="metric.trend"
        :icon="metric.icon"
        :color="metric.color"
        :loading="isLoading"
      />
    </div>

    <!-- Gráficos principales -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Gráfico de conversaciones en tiempo real -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Conversaciones en Tiempo Real</h3>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-500">Actualizado hace {{ lastUpdateTime }}</span>
          </div>
        </div>
        <div class="h-80">
          <ConversationChart 
            :data="conversationData" 
            :loading="isLoading"
            :period="selectedPeriod"
          />
        </div>
      </div>

      <!-- Gráfico de satisfacción del usuario -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Satisfacción del Usuario</h3>
          <div class="text-2xl font-bold text-green-600">{{ satisfactionScore }}%</div>
        </div>
        <div class="h-80">
          <SatisfactionChart 
            :data="satisfactionData" 
            :loading="isLoading"
          />
        </div>
      </div>
    </div>

    <!-- Métricas de rendimiento -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Tiempo de respuesta -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Tiempo de Respuesta</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-600">Promedio</span>
            <span class="text-lg font-semibold text-blue-600">{{ averageResponseTime }}ms</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-500 h-2 rounded-full transition-all duration-1000"
              :style="{ width: responseTimeProgress + '%' }"
            ></div>
          </div>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-600">Mínimo:</span>
              <span class="font-medium ml-1">{{ minResponseTime }}ms</span>
            </div>
            <div>
              <span class="text-gray-600">Máximo:</span>
              <span class="font-medium ml-1">{{ maxResponseTime }}ms</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Chatbots -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Top Chatbots</h3>
        <div class="space-y-3">
          <div 
            v-for="(chatbot, index) in topChatbots" 
            :key="chatbot.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span class="text-sm font-semibold text-primary-600">{{ index + 1 }}</span>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ chatbot.name }}</p>
                <p class="text-sm text-gray-500">{{ chatbot.conversations }} conversaciones</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm font-medium text-green-600">{{ chatbot.satisfaction }}%</div>
              <div class="text-xs text-gray-500">satisfacción</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actividad por hora -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Actividad por Hora</h3>
        <div class="h-48">
          <HourlyActivityChart 
            :data="hourlyActivity" 
            :loading="isLoading"
          />
        </div>
      </div>
    </div>

    <!-- Tabla de conversaciones recientes -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Conversaciones Recientes</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usuario
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Chatbot
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Último Mensaje
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tiempo
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="conversation in recentConversations" :key="conversation.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                    <UserIcon class="w-4 h-4 text-gray-600" />
                  </div>
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">{{ conversation.user_name || 'Anónimo' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ conversation.chatbot_name }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900 max-w-xs truncate">{{ conversation.last_message }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    conversation.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ conversation.status === 'active' ? 'Activa' : 'Finalizada' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatTimeAgo(conversation.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  @click="viewConversation(conversation.id)"
                  class="text-primary-600 hover:text-primary-900"
                >
                  Ver
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import { useDashboardStore } from '@/stores/dashboard'
import { ArrowPathIcon, UserIcon } from '@heroicons/vue/24/outline'
import MetricCard from './MetricCard.vue'
import ConversationChart from './charts/ConversationChart.vue'
import SatisfactionChart from './charts/SatisfactionChart.vue'
import HourlyActivityChart from './charts/HourlyActivityChart.vue'

// Stores
const analyticsStore = useAnalyticsStore()
const dashboardStore = useDashboardStore()

// State
const selectedPeriod = ref('24h')
const isLoading = ref(false)
const lastUpdateTime = ref('0s')
const refreshInterval = ref(null)

// Computed
const mainKPIs = computed(() => [
  {
    key: 'conversations',
    title: 'Conversaciones Totales',
    value: analyticsStore.overview.total_conversations || 0,
    change: '+12%',
    trend: 'up',
    icon: 'ChatBubbleLeftRightIcon',
    color: 'blue'
  },
  {
    key: 'users',
    title: 'Usuarios Únicos',
    value: analyticsStore.overview.unique_users || 0,
    change: '+8%',
    trend: 'up',
    icon: 'UsersIcon',
    color: 'green'
  },
  {
    key: 'satisfaction',
    title: 'Satisfacción Promedio',
    value: `${Math.round((analyticsStore.overview.average_satisfaction || 0) * 100)}%`,
    change: '+5%',
    trend: 'up',
    icon: 'HeartIcon',
    color: 'purple'
  },
  {
    key: 'response_time',
    title: 'Tiempo de Respuesta',
    value: `${Math.round(analyticsStore.overview.average_response_time || 0)}ms`,
    change: '-15%',
    trend: 'down',
    icon: 'ClockIcon',
    color: 'orange'
  }
])

const conversationData = computed(() => analyticsStore.conversationMetrics.daily_conversations || [])
const satisfactionData = computed(() => analyticsStore.chatbotPerformance.user_satisfaction || [])
const satisfactionScore = computed(() => Math.round((analyticsStore.overview.average_satisfaction || 0) * 100))
const hourlyActivity = computed(() => analyticsStore.conversationMetrics.hourly_distribution || [])
const recentConversations = computed(() => dashboardStore.recentConversations.slice(0, 10))

const averageResponseTime = computed(() => Math.round(analyticsStore.overview.average_response_time || 0))
const minResponseTime = computed(() => 150) // Mock data
const maxResponseTime = computed(() => 2500) // Mock data
const responseTimeProgress = computed(() => {
  const avg = averageResponseTime.value
  return Math.min((avg / 1000) * 100, 100)
})

const topChatbots = computed(() => [
  { id: 1, name: 'Asistente de Ventas', conversations: 245, satisfaction: 94 },
  { id: 2, name: 'Soporte Técnico', conversations: 189, satisfaction: 91 },
  { id: 3, name: 'FAQ General', conversations: 156, satisfaction: 88 }
])

// Methods
const refreshMetrics = async () => {
  isLoading.value = true
  try {
    await Promise.all([
      analyticsStore.fetchOverview({ period: selectedPeriod.value }),
      analyticsStore.fetchConversationMetrics({ period: selectedPeriod.value }),
      analyticsStore.fetchChatbotPerformance({ period: selectedPeriod.value }),
      dashboardStore.fetchRecentConversations()
    ])
    updateLastUpdateTime()
  } catch (error) {
    console.error('Error refreshing metrics:', error)
  } finally {
    isLoading.value = false
  }
}

const updateLastUpdateTime = () => {
  lastUpdateTime.value = '0s'
}

const formatTimeAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)
  
  if (diffInSeconds < 60) return `${diffInSeconds}s`
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h`
  return `${Math.floor(diffInSeconds / 86400)}d`
}

const viewConversation = (conversationId) => {
  // Navigate to conversation detail
  console.log('View conversation:', conversationId)
}

// Lifecycle
onMounted(() => {
  refreshMetrics()
  
  // Set up real-time updates
  refreshInterval.value = setInterval(() => {
    refreshMetrics()
  }, 30000) // Update every 30 seconds
  
  // Update time counter
  setInterval(() => {
    const current = lastUpdateTime.value
    if (current.endsWith('s')) {
      const seconds = parseInt(current) + 1
      if (seconds < 60) {
        lastUpdateTime.value = `${seconds}s`
      } else {
        lastUpdateTime.value = `${Math.floor(seconds / 60)}m`
      }
    }
  }, 1000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.enterprise-metrics {
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