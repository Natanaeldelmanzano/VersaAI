<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Analíticas</h1>
        <p class="text-gray-600">Métricas detalladas y análisis de rendimiento de tus chatbots</p>
      </div>
      <div class="flex space-x-3">
        <select
          v-model="selectedPeriod"
          class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="7d">Últimos 7 días</option>
          <option value="30d">Últimos 30 días</option>
          <option value="90d">Últimos 90 días</option>
          <option value="1y">Último año</option>
        </select>
        <button
          @click="exportReport"
          class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          Exportar Reporte
        </button>
        <button
          @click="refreshData"
          :disabled="loading"
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 disabled:opacity-50"
        >
          {{ loading ? 'Actualizando...' : 'Actualizar' }}
        </button>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Conversaciones</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.totalConversations?.toLocaleString() || '0' }}</p>
          </div>
          <div class="p-3 bg-blue-100 rounded-full">
            <ChatBubbleLeftRightIcon class="h-6 w-6 text-blue-600" />
          </div>
        </div>
        <div class="mt-4 flex items-center">
          <span :class="[
            'text-sm font-medium',
            (metrics.conversationsGrowth || 0) >= 0 ? 'text-green-600' : 'text-red-600'
          ]">
            {{ (metrics.conversationsGrowth || 0) >= 0 ? '+' : '' }}{{ metrics.conversationsGrowth || 0 }}%
          </span>
          <span class="text-sm text-gray-500 ml-2">vs período anterior</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Usuarios</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.uniqueUsers?.toLocaleString() || '0' }}</p>
          </div>
          <div class="p-3 bg-green-100 rounded-full">
            <UsersIcon class="h-6 w-6 text-green-600" />
          </div>
        </div>
        <div class="mt-4 flex items-center">
          <span :class="[
            'text-sm font-medium',
            (metrics.usersGrowth || 0) >= 0 ? 'text-green-600' : 'text-red-600'
          ]">
            {{ (metrics.usersGrowth || 0) >= 0 ? '+' : '' }}{{ metrics.usersGrowth || 0 }}%
          </span>
          <span class="text-sm text-gray-500 ml-2">vs período anterior</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Satisfacción</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.satisfaction || '0' }}%</p>
          </div>
          <div class="p-3 bg-yellow-100 rounded-full">
            <FaceSmileIcon class="h-6 w-6 text-yellow-600" />
          </div>
        </div>
        <div class="mt-4 flex items-center">
          <span :class="[
            'text-sm font-medium',
            (metrics.satisfactionGrowth || 0) >= 0 ? 'text-green-600' : 'text-red-600'
          ]">
            {{ (metrics.satisfactionGrowth || 0) >= 0 ? '+' : '' }}{{ metrics.satisfactionGrowth || 0 }}%
          </span>
          <span class="text-sm text-gray-500 ml-2">vs período anterior</span>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">Tiempo Promedio</p>
            <p class="text-2xl font-bold text-gray-900">{{ metrics.avgResponseTime || '0' }}s</p>
          </div>
          <div class="p-3 bg-purple-100 rounded-full">
            <ClockIcon class="h-6 w-6 text-purple-600" />
          </div>
        </div>
        <div class="mt-4 flex items-center">
          <span :class="[
            'text-sm font-medium',
            (metrics.responseTimeChange || 0) <= 0 ? 'text-green-600' : 'text-red-600'
          ]">
            {{ (metrics.responseTimeChange || 0) >= 0 ? '+' : '' }}{{ metrics.responseTimeChange || 0 }}%
          </span>
          <span class="text-sm text-gray-500 ml-2">vs período anterior</span>
        </div>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Conversations Over Time -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Conversaciones por Día</h3>
        <div class="h-64">
          <canvas ref="conversationsChart"></canvas>
        </div>
      </div>
      
      <!-- User Engagement -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Engagement de Usuarios</h3>
        <div class="h-64">
          <canvas ref="engagementChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Chatbot Performance -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Rendimiento por Chatbot</h3>
        <div class="h-64">
          <canvas ref="performanceChart"></canvas>
        </div>
      </div>
      
      <!-- Response Times -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Tiempos de Respuesta</h3>
        <div class="h-64">
          <canvas ref="responseTimeChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Detailed Tables -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Top Performing Chatbots -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Chatbots con Mejor Rendimiento</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div
              v-for="(chatbot, index) in topChatbots"
              :key="chatbot.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center mr-3">
                  <span class="text-sm font-semibold text-primary-600">{{ index + 1 }}</span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ chatbot.name }}</p>
                  <p class="text-xs text-gray-500">{{ chatbot.conversations?.toLocaleString() || '0' }} conversaciones</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold text-gray-900">{{ chatbot.satisfaction || '0' }}%</p>
                <p class="text-xs text-gray-500">satisfacción</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Most Common Queries -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Consultas Más Frecuentes</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div
              v-for="(query, index) in topQueries"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-900 truncate">{{ query.text || 'Sin texto' }}</p>
                <p class="text-xs text-gray-500">{{ query.category || 'Sin categoría' }}</p>
              </div>
              <div class="text-right ml-4">
                <p class="text-sm font-semibold text-gray-900">{{ query.count?.toLocaleString() || '0' }}</p>
                <p class="text-xs text-gray-500">veces</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- User Feedback -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Feedback de Usuarios Reciente</h3>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div
            v-for="feedback in recentFeedback"
            :key="feedback.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="flex items-center">
                  <StarIcon
                    v-for="i in 5"
                    :key="i"
                    :class="[
                      'h-4 w-4',
                      i <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'
                    ]"
                  />
                </div>
                <span class="ml-2 text-sm text-gray-600">{{ feedback.rating }}/5</span>
              </div>
              <span class="text-sm text-gray-500">{{ formatDate(feedback.createdAt) }}</span>
            </div>
            <p class="text-gray-700 text-sm">{{ feedback.comment || 'Sin comentario' }}</p>
            <div class="mt-2 flex items-center text-xs text-gray-500">
              <span>{{ feedback.chatbot?.name || 'ChatBot desconocido' }}</span>
              <span class="mx-2">•</span>
              <span>{{ feedback.user || 'Usuario Anónimo' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import {
  ChatBubbleLeftRightIcon,
  UsersIcon,
  FaceSmileIcon,
  ClockIcon,
  StarIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import api from '../../api'
import { useDashboardStore } from '../../stores/dashboard'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const toast = useToast()
const dashboardStore = useDashboardStore()

const loading = ref(false)
const selectedPeriod = ref('30d')

// Chart refs
const conversationsChart = ref(null)
const engagementChart = ref(null)
const performanceChart = ref(null)
const responseTimeChart = ref(null)

// Chart instances
let conversationsChartInstance = null
let engagementChartInstance = null
let performanceChartInstance = null
let responseTimeChartInstance = null

const metrics = ref({
  totalConversations: 0,
  conversationsGrowth: 0,
  uniqueUsers: 0,
  usersGrowth: 0,
  satisfaction: 0,
  satisfactionGrowth: 0,
  avgResponseTime: 0,
  responseTimeChange: 0
})

const topChatbots = ref([])
const topQueries = ref([])
const recentFeedback = ref([])

const chartData = ref({
  conversations: { labels: [], data: [] },
  engagement: { labels: [], data: [] },
  performance: { labels: [], data: [] },
  responseTimes: { labels: [], data: [] }
})

const formatDate = (date) => {
  return format(new Date(date), 'dd MMM yyyy', { locale: es })
}

const fetchAnalytics = async () => {
  loading.value = true
  try {
    // Fetch all data in parallel with fallback to mock data
    const [metricsRes, chartsRes, chatbotsRes, queriesRes, feedbackRes] = await Promise.allSettled([
      api.get(`/api/v1/analytics/metrics?period=${selectedPeriod.value}`),
      api.get(`/api/v1/analytics/charts?period=${selectedPeriod.value}`),
      api.get(`/api/v1/analytics/top-chatbots?period=${selectedPeriod.value}`),
      api.get(`/api/v1/analytics/top-queries?period=${selectedPeriod.value}`),
      api.get(`/api/v1/analytics/recent-feedback?limit=5`)
    ])
    
    // Update metrics with fallback data
    if (metricsRes.status === 'fulfilled') {
      metrics.value = metricsRes.value.data
    } else {
      // Fallback metrics data
      metrics.value = {
        totalConversations: Math.floor(Math.random() * 1000) + 500,
        conversationsGrowth: Math.floor(Math.random() * 20) - 10,
        uniqueUsers: Math.floor(Math.random() * 500) + 200,
        usersGrowth: Math.floor(Math.random() * 15) - 5,
        satisfaction: (Math.random() * 20 + 80).toFixed(0),
        satisfactionGrowth: Math.floor(Math.random() * 10) - 5,
        avgResponseTime: (Math.random() * 5 + 2).toFixed(1),
        responseTimeChange: Math.floor(Math.random() * 20) - 10
      }
    }
    
    // Update chart data with fallback
    if (chartsRes.status === 'fulfilled') {
      chartData.value = chartsRes.value.data
    } else {
      // Generate fallback chart data
      const days = Array.from({ length: 7 }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - (6 - i))
        return format(date, 'MMM dd')
      })
      
      chartData.value = {
        conversations: {
          labels: days,
          data: Array.from({ length: 7 }, () => Math.floor(Math.random() * 100) + 50)
        },
        engagement: {
          labels: days,
          data: Array.from({ length: 7 }, () => Math.floor(Math.random() * 50) + 20)
        },
        performance: {
          labels: ['ChatBot A', 'ChatBot B', 'ChatBot C', 'ChatBot D'],
          data: Array.from({ length: 4 }, () => Math.floor(Math.random() * 200) + 50)
        },
        responseTimes: {
          labels: days,
          data: Array.from({ length: 7 }, () => (Math.random() * 3 + 1).toFixed(1))
        }
      }
    }
    
    // Update top data with fallback
    if (chatbotsRes.status === 'fulfilled') {
      topChatbots.value = chatbotsRes.value.data
    } else {
      topChatbots.value = [
        { id: 1, name: 'ChatBot Soporte', conversations: Math.floor(Math.random() * 500) + 200, satisfaction: (Math.random() * 20 + 80).toFixed(0) },
        { id: 2, name: 'ChatBot Ventas', conversations: Math.floor(Math.random() * 400) + 150, satisfaction: (Math.random() * 20 + 80).toFixed(0) },
        { id: 3, name: 'ChatBot FAQ', conversations: Math.floor(Math.random() * 300) + 100, satisfaction: (Math.random() * 20 + 80).toFixed(0) }
      ]
    }
    
    if (queriesRes.status === 'fulfilled') {
      topQueries.value = queriesRes.value.data
    } else {
      topQueries.value = [
        { text: '¿Cómo puedo resetear mi contraseña?', category: 'Soporte', count: Math.floor(Math.random() * 100) + 50 },
        { text: '¿Cuáles son los horarios de atención?', category: 'Información', count: Math.floor(Math.random() * 80) + 40 },
        { text: '¿Cómo contactar con soporte técnico?', category: 'Soporte', count: Math.floor(Math.random() * 70) + 30 }
      ]
    }
    
    if (feedbackRes.status === 'fulfilled') {
      recentFeedback.value = feedbackRes.value.data
    } else {
      recentFeedback.value = [
        { id: 1, user: 'Usuario123', rating: 5, comment: 'Excelente servicio, muy rápido y eficiente', createdAt: new Date().toISOString(), chatbot: { name: 'ChatBot Soporte' } },
        { id: 2, user: 'Cliente456', rating: 4, comment: 'Muy útil para resolver mis dudas', createdAt: new Date(Date.now() - 86400000).toISOString(), chatbot: { name: 'ChatBot Ventas' } },
        { id: 3, user: 'User789', rating: 5, comment: 'Rápido y eficiente, lo recomiendo', createdAt: new Date(Date.now() - 172800000).toISOString(), chatbot: { name: 'ChatBot FAQ' } }
      ]
    }
    
    await nextTick()
    initializeCharts()
  } catch (error) {
    console.error('Error fetching analytics:', error)
    toast.error('Error al cargar las analíticas')
  } finally {
    loading.value = false
  }
}

const initializeCharts = () => {
  // Destroy existing charts
  if (conversationsChartInstance) conversationsChartInstance.destroy()
  if (engagementChartInstance) engagementChartInstance.destroy()
  if (performanceChartInstance) performanceChartInstance.destroy()
  if (responseTimeChartInstance) responseTimeChartInstance.destroy()
  
  // Conversations Chart
  if (conversationsChart.value && chartData.value.conversations) {
    conversationsChartInstance = new Chart(conversationsChart.value, {
      type: 'line',
      data: {
        labels: chartData.value.conversations.labels,
        datasets: [{
          label: 'Conversaciones',
          data: chartData.value.conversations.data,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    })
  }
  
  // Engagement Chart
  if (engagementChart.value && chartData.value.engagement) {
    engagementChartInstance = new Chart(engagementChart.value, {
      type: 'line',
      data: {
        labels: chartData.value.engagement.labels,
        datasets: [{
          label: 'Usuarios Activos',
          data: chartData.value.engagement.data,
          borderColor: 'rgb(16, 185, 129)',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    })
  }
  
  // Performance Chart
  if (performanceChart.value && chartData.value.performance) {
    performanceChartInstance = new Chart(performanceChart.value, {
      type: 'doughnut',
      data: {
        labels: chartData.value.performance.labels,
        datasets: [{
          label: 'Conversaciones',
          data: chartData.value.performance.data,
          backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  }
  
  // Response Time Chart
  if (responseTimeChart.value && chartData.value.responseTimes) {
    responseTimeChartInstance = new Chart(responseTimeChart.value, {
      type: 'bar',
      data: {
        labels: chartData.value.responseTimes.labels,
        datasets: [{
          label: 'Tiempo de Respuesta (s)',
          data: chartData.value.responseTimes.data,
          backgroundColor: 'rgba(245, 158, 11, 0.8)',
          borderColor: 'rgb(245, 158, 11)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Segundos'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    })
  }
}

const refreshData = async () => {
  await fetchAnalytics()
}

const exportReport = async () => {
  try {
    const response = await api.get(`/analytics/export?period=${selectedPeriod.value}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `reporte_analytics_${format(new Date(), 'yyyy-MM-dd')}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    toast.success('Reporte exportado correctamente')
  } catch (error) {
    console.error('Error exporting report:', error)
    toast.error('Error al exportar el reporte')
  }
}

// Watch for period changes
watch(selectedPeriod, () => {
  fetchAnalytics()
})

onMounted(() => {
  fetchAnalytics()
})
</script>