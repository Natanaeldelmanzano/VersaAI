<template>
  <div class="analytics-page">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Analíticas</h1>
            <p class="text-gray-600 mt-1">Métricas y estadísticas de rendimiento de tus chatbots</p>
          </div>
          <div class="flex items-center space-x-3">
            <!-- Scroll to top button -->
            <button
              @click="scrollToTop"
              class="text-gray-600 hover:text-gray-800 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title="Ir al inicio"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
              </svg>
            </button>
            <!-- Date Range Selector -->
            <select
              v-model="selectedPeriod"
              @change="loadAnalytics(selectedPeriod)"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="7d">Últimos 7 días</option>
              <option value="30d">Últimos 30 días</option>
              <option value="90d">Últimos 90 días</option>
              <option value="1y">Último año</option>
            </select>
            
            <button
              @click="exportReport('pdf', selectedPeriod)"
              :disabled="isLoading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Exportar
            </button>
            
            <button
              @click="refreshData"
              :disabled="isLoading"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {{ isLoading ? 'Actualizando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !hasData" class="flex-1 flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Cargando analíticas...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 flex items-center justify-center">
      <div class="text-center">
        <div class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error al cargar analíticas</h3>
              <p class="mt-1 text-sm text-red-700">{{ error }}</p>
              <button @click="refreshData" class="mt-2 text-sm text-red-600 hover:text-red-500 underline">
                Intentar de nuevo
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analytics Content -->
    <div v-else class="flex-1 overflow-y-auto bg-gray-50 scroll-smooth">
      <div class="p-6 space-y-6 analytics-content">
        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Total Conversaciones</p>
                <div class="flex items-baseline">
                  <p class="text-2xl font-semibold text-gray-900">{{ formatNumber(metrics.totalConversations) }}</p>
                  <p class="ml-2 flex items-baseline text-sm font-semibold" :class="getChangeClass(metrics.conversationsChange)">
                    <svg class="self-center flex-shrink-0 h-4 w-4" :class="getChangeIconClass(metrics.conversationsChange)" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" :d="getChangeIconPath(metrics.conversationsChange)" clip-rule="evenodd" />
                    </svg>
                    <span class="sr-only">{{ metrics.conversationsChange > 0 ? 'Increased' : 'Decreased' }} by</span>
                    {{ Math.abs(metrics.conversationsChange) }}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Usuarios Únicos</p>
                <div class="flex items-baseline">
                  <p class="text-2xl font-semibold text-gray-900">{{ formatNumber(metrics.uniqueUsers) }}</p>
                  <p class="ml-2 flex items-baseline text-sm font-semibold" :class="getChangeClass(metrics.usersChange)">
                    <svg class="self-center flex-shrink-0 h-4 w-4" :class="getChangeIconClass(metrics.usersChange)" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" :d="getChangeIconPath(metrics.usersChange)" clip-rule="evenodd" />
                    </svg>
                    {{ Math.abs(metrics.usersChange) }}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Tiempo Promedio</p>
                <div class="flex items-baseline">
                  <p class="text-2xl font-semibold text-gray-900">{{ formatDuration(metrics.avgSessionDuration) }}</p>
                  <p class="ml-2 flex items-baseline text-sm font-semibold" :class="getChangeClass(metrics.durationChange)">
                    <svg class="self-center flex-shrink-0 h-4 w-4" :class="getChangeIconClass(metrics.durationChange)" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" :d="getChangeIconPath(metrics.durationChange)" clip-rule="evenodd" />
                    </svg>
                    {{ Math.abs(metrics.durationChange) }}%
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">Tasa de Satisfacción</p>
                <div class="flex items-baseline">
                  <p class="text-2xl font-semibold text-gray-900">{{ metrics.satisfactionRate }}%</p>
                  <p class="ml-2 flex items-baseline text-sm font-semibold" :class="getChangeClass(metrics.satisfactionChange)">
                    <svg class="self-center flex-shrink-0 h-4 w-4" :class="getChangeIconClass(metrics.satisfactionChange)" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" :d="getChangeIconPath(metrics.satisfactionChange)" clip-rule="evenodd" />
                    </svg>
                    {{ Math.abs(metrics.satisfactionChange) }}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 max-h-screen overflow-y-auto scrollable">
          <!-- Conversations Chart -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900">Conversaciones por Día</h3>
              <div class="flex items-center space-x-2">
                <button
                  v-for="period in chartPeriods"
                  :key="period.value"
                  @click="selectedChartPeriod = period.value"
                  :class="[
                    'px-3 py-1 text-xs font-medium rounded-full',
                    selectedChartPeriod === period.value
                      ? 'bg-blue-100 text-blue-800'
                      : 'text-gray-500 hover:text-gray-700'
                  ]"
                >
                  {{ period.label }}
                </button>
              </div>
            </div>
            <div class="h-64">
              <!-- Chart placeholder -->
              <div class="w-full h-full bg-gray-50 rounded-lg flex items-center justify-center">
                <div class="text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <p class="mt-2 text-sm text-gray-500">Gráfico de conversaciones</p>
                  <p class="text-xs text-gray-400">Integración con Chart.js pendiente</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Top Chatbots -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Chatbots Más Activos</h3>
            <div class="space-y-4">
              <div v-for="(bot, index) in topChatbots" :key="bot.id" class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-sm font-medium text-blue-600">{{ index + 1 }}</span>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900">{{ bot.name }}</p>
                    <p class="text-sm text-gray-500">{{ formatNumber(bot.conversations) }}</p>
                  </div>
                  <div class="mt-1">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-blue-600 h-2 rounded-full" :style="{ width: (bot.conversations / topChatbots[0].conversations) * 100 + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Analytics -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- User Engagement -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Engagement de Usuarios</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Nuevos usuarios</span>
                <span class="text-sm font-medium text-gray-900">{{ formatNumber(engagement.newUsers) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Usuarios recurrentes</span>
                <span class="text-sm font-medium text-gray-900">{{ formatNumber(engagement.returningUsers) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tasa de retención</span>
                <span class="text-sm font-medium text-gray-900">{{ engagement.retentionRate }}%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Sesiones por usuario</span>
                <span class="text-sm font-medium text-gray-900">{{ engagement.sessionsPerUser }}</span>
              </div>
            </div>
          </div>

          <!-- Message Analytics -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Análisis de Mensajes</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Total mensajes</span>
                <span class="text-sm font-medium text-gray-900">{{ formatNumber(messageAnalytics.totalMessages) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Mensajes por conversación</span>
                <span class="text-sm font-medium text-gray-900">{{ messageAnalytics.avgMessagesPerConversation }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tiempo de respuesta</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDuration(messageAnalytics.avgResponseTime) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Tasa de resolución</span>
                <span class="text-sm font-medium text-gray-900">{{ messageAnalytics.resolutionRate }}%</span>
              </div>
            </div>
          </div>

          <!-- Popular Topics -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Temas Populares</h3>
            <div class="space-y-3">
              <div v-for="topic in popularTopics" :key="topic.name" class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="w-3 h-3 rounded-full mr-3" :style="{ backgroundColor: topic.color }"></div>
                  <span class="text-sm text-gray-600">{{ topic.name }}</span>
                </div>
                <div class="flex items-center">
                  <span class="text-sm font-medium text-gray-900 mr-2">{{ topic.count }}</span>
                  <span class="text-xs text-gray-500">{{ topic.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Actividad Reciente</h3>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="activity in recentActivity" :key="activity.id" class="px-6 py-4">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div :class="getActivityIconClass(activity.type)" class="w-8 h-8 rounded-full flex items-center justify-center">
                    <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path :d="getActivityIconPath(activity.type)" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                    <p class="text-sm text-gray-500">{{ formatTimeAgo(activity.timestamp) }}</p>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ activity.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'

export default {
  name: 'Analytics',
  setup() {
    const toast = useToast()
    
    // State
    const isLoading = ref(false)
    const error = ref(null)
    const selectedPeriod = ref('30d')
    const selectedChartPeriod = ref('7d')
    const hasData = ref(true)
    
    // Chart periods
    const chartPeriods = [
      { value: '7d', label: '7D' },
      { value: '30d', label: '30D' },
      { value: '90d', label: '90D' }
    ]
    
    // Mock data
    const metrics = ref({
      totalConversations: 12847,
      conversationsChange: 12.5,
      uniqueUsers: 3421,
      usersChange: 8.2,
      avgSessionDuration: 420, // seconds
      durationChange: -3.1,
      satisfactionRate: 87.3,
      satisfactionChange: 5.7
    })
    
    const topChatbots = ref([
      { id: 1, name: 'Soporte Técnico', conversations: 4521 },
      { id: 2, name: 'Ventas', conversations: 3847 },
      { id: 3, name: 'FAQ General', conversations: 2156 },
      { id: 4, name: 'Recursos Humanos', conversations: 1823 },
      { id: 5, name: 'Facturación', conversations: 1234 }
    ])
    
    const engagement = ref({
      newUsers: 1247,
      returningUsers: 2174,
      retentionRate: 63.5,
      sessionsPerUser: 2.8
    })
    
    const messageAnalytics = ref({
      totalMessages: 45623,
      avgMessagesPerConversation: 3.6,
      avgResponseTime: 2.3, // seconds
      resolutionRate: 89.2
    })
    
    const popularTopics = ref([
      { name: 'Problemas técnicos', count: 1247, percentage: 28.5, color: '#3B82F6' },
      { name: 'Información de productos', count: 987, percentage: 22.6, color: '#10B981' },
      { name: 'Facturación', count: 756, percentage: 17.3, color: '#F59E0B' },
      { name: 'Devoluciones', count: 543, percentage: 12.4, color: '#EF4444' },
      { name: 'Otros', count: 834, percentage: 19.2, color: '#8B5CF6' }
    ])
    
    const recentActivity = ref([
      {
        id: 1,
        type: 'conversation',
        title: 'Nueva conversación iniciada',
        description: 'Usuario anónimo inició chat con Soporte Técnico',
        timestamp: new Date(Date.now() - 5 * 60 * 1000)
      },
      {
        id: 2,
        type: 'chatbot',
        title: 'Chatbot actualizado',
        description: 'Se actualizó la configuración del bot de Ventas',
        timestamp: new Date(Date.now() - 15 * 60 * 1000)
      },
      {
        id: 3,
        type: 'user',
        title: 'Nuevo usuario registrado',
        description: 'juan.perez@empresa.com se registró en el sistema',
        timestamp: new Date(Date.now() - 30 * 60 * 1000)
      },
      {
        id: 4,
        type: 'document',
        title: 'Documento procesado',
        description: 'Manual de usuario.pdf fue procesado exitosamente',
        timestamp: new Date(Date.now() - 45 * 60 * 1000)
      },
      {
        id: 5,
        type: 'error',
        title: 'Error en procesamiento',
        description: 'Falló el procesamiento de documento-grande.pdf',
        timestamp: new Date(Date.now() - 60 * 60 * 1000)
      }
    ])
    
    // Methods
    const loadAnalytics = async (period) => {
      try {
        isLoading.value = true
        error.value = null
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        toast.success('Analíticas actualizadas')
      } catch (err) {
        console.error('Error loading analytics:', err)
        error.value = 'Error al cargar las analíticas'
        toast.error('Error al cargar las analíticas')
      } finally {
        isLoading.value = false
      }
    }
    
    const exportReport = async (format, period) => {
      try {
        toast.info('Exportando reporte...')
        // Simulate export
        await new Promise(resolve => setTimeout(resolve, 2000))
        toast.success('Reporte exportado exitosamente')
      } catch (err) {
        console.error('Error exporting report:', err)
        toast.error('Error al exportar el reporte')
      }
    }
    
    const refreshData = async () => {
      await loadAnalytics(selectedPeriod.value)
    }
    
    const scrollToTop = () => {
      const analyticsContent = document.querySelector('.analytics-content')
      if (analyticsContent) {
        analyticsContent.scrollTo({ top: 0, behavior: 'smooth' })
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }
    }
    
    // Utility functions
    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }
    
    const formatDuration = (seconds) => {
      if (seconds < 60) {
        return `${seconds}s`
      } else if (seconds < 3600) {
        return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
      } else {
        const hours = Math.floor(seconds / 3600)
        const minutes = Math.floor((seconds % 3600) / 60)
        return `${hours}h ${minutes}m`
      }
    }
    
    const formatTimeAgo = (date) => {
      const now = new Date()
      const diffInMinutes = Math.floor((now - date) / (1000 * 60))
      
      if (diffInMinutes < 1) {
        return 'Hace un momento'
      } else if (diffInMinutes < 60) {
        return `Hace ${diffInMinutes} minutos`
      } else if (diffInMinutes < 1440) {
        return `Hace ${Math.floor(diffInMinutes / 60)} horas`
      } else {
        return `Hace ${Math.floor(diffInMinutes / 1440)} días`
      }
    }
    
    const getChangeClass = (change) => {
      return change > 0 ? 'text-green-600' : 'text-red-600'
    }
    
    const getChangeIconClass = (change) => {
      return change > 0 ? 'text-green-500' : 'text-red-500'
    }
    
    const getChangeIconPath = (change) => {
      return change > 0
        ? 'M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z'
        : 'M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z'
    }
    
    const getActivityIconClass = (type) => {
      const classes = {
        conversation: 'bg-blue-500',
        chatbot: 'bg-green-500',
        user: 'bg-purple-500',
        document: 'bg-yellow-500',
        error: 'bg-red-500'
      }
      return classes[type] || 'bg-gray-500'
    }
    
    const getActivityIconPath = (type) => {
      const paths = {
        conversation: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
        chatbot: 'M13 10V3L4 14h7v7l9-11h-7z',
        user: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
        document: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
        error: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
      }
      return paths[type] || ''
    }
    
    // Lifecycle
    onMounted(() => {
      loadAnalytics(selectedPeriod.value)
    })
    
    return {
      // State
      isLoading,
      error,
      selectedPeriod,
      selectedChartPeriod,
      chartPeriods,
      metrics,
      topChatbots,
      engagement,
      messageAnalytics,
      popularTopics,
      recentActivity,
      hasData,
      
      // Methods
      loadAnalytics,
      exportReport,
      refreshData,
      scrollToTop,
      
      // Utilities
      formatNumber,
      formatDuration,
      formatTimeAgo,
      getChangeClass,
      getChangeIconClass,
      getChangeIconPath,
      getActivityIconClass,
      getActivityIconPath
    }
  }
}
</script>

<style scoped>
.analytics-page {
  @apply h-full flex flex-col;
}

.analytics-content {
  scroll-behavior: smooth;
}

.scrollable {
  scrollbar-width: thin;
  scrollbar-color: #c1c1c1 #f1f1f1;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
  transition: background 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Smooth transitions */
.transition-shadow {
  transition: box-shadow 0.2s ease;
}

.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease;
}
</style>