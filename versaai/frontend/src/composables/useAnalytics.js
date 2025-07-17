import { ref, reactive, computed } from 'vue'
import { analyticsAPI } from '@/services/api'
import { useToast } from 'vue-toastification'

export function useAnalytics() {
  const toast = useToast()
  const isLoading = ref(false)
  const error = ref(null)
  
  // Analytics data
  const metrics = reactive({
    totalConversations: 0,
    conversationsChange: 0,
    uniqueUsers: 0,
    usersChange: 0,
    avgSessionDuration: 0,
    durationChange: 0,
    satisfactionRate: 0,
    satisfactionChange: 0
  })
  
  const chartData = reactive({
    conversations: [],
    users: [],
    satisfaction: [],
    performance: []
  })
  
  const topChatbots = ref([])
  const recentActivity = ref([])
  const performanceMetrics = ref({})
  
  // Computed properties
  const hasData = computed(() => {
    return metrics.totalConversations > 0 || topChatbots.value.length > 0
  })
  
  const totalActiveUsers = computed(() => {
    return chartData.users.reduce((sum, day) => sum + day.value, 0)
  })
  
  const averageResponseTime = computed(() => {
    if (!performanceMetrics.value.response_times) return 0
    const times = performanceMetrics.value.response_times
    return times.reduce((sum, time) => sum + time, 0) / times.length
  })
  
  // Methods
  const loadAnalytics = async (period = '30d') => {
    isLoading.value = true
    error.value = null
    
    try {
      // Load overview metrics
      const overviewResponse = await analyticsAPI.getOverview({ period })
      Object.assign(metrics, overviewResponse.data)
      
      // Load chatbot analytics
      const chatbotResponse = await analyticsAPI.getChatbotAnalytics({ period, limit: 10 })
      topChatbots.value = chatbotResponse.data.top_chatbots || []
      
      // Load conversation analytics for charts
      const conversationResponse = await analyticsAPI.getConversationAnalytics({ period })
      chartData.conversations = conversationResponse.data.daily_conversations || []
      chartData.satisfaction = conversationResponse.data.satisfaction_trends || []
      
      // Load user analytics
      const userResponse = await analyticsAPI.getUserAnalytics({ period })
      chartData.users = userResponse.data.daily_users || []
      
      // Load performance metrics
      const performanceResponse = await analyticsAPI.getPerformanceMetrics({ period })
      performanceMetrics.value = performanceResponse.data
      
    } catch (err) {
      error.value = err.message
      console.error('Error loading analytics:', err)
      
      // Fallback to mock data if API fails
      loadMockData()
      toast.warning('Usando datos de demostración. Verifica la conexión con el servidor.')
    } finally {
      isLoading.value = false
    }
  }
  
  const loadMockData = () => {
    // Mock metrics data
    Object.assign(metrics, {
      totalConversations: 1247,
      conversationsChange: 12.5,
      uniqueUsers: 892,
      usersChange: 8.3,
      avgSessionDuration: 245, // seconds
      durationChange: -3.2,
      satisfactionRate: 94.2,
      satisfactionChange: 2.1
    })
    
    // Mock chart data
    const last30Days = Array.from({ length: 30 }, (_, i) => {
      const date = new Date()
      date.setDate(date.getDate() - (29 - i))
      return {
        date: date.toISOString().split('T')[0],
        conversations: Math.floor(Math.random() * 50) + 20,
        users: Math.floor(Math.random() * 30) + 15,
        satisfaction: Math.random() * 20 + 80
      }
    })
    
    chartData.conversations = last30Days.map(day => ({
      date: day.date,
      value: day.conversations
    }))
    
    chartData.users = last30Days.map(day => ({
      date: day.date,
      value: day.users
    }))
    
    chartData.satisfaction = last30Days.map(day => ({
      date: day.date,
      value: day.satisfaction
    }))
    
    // Mock top chatbots
    topChatbots.value = [
      {
        id: 1,
        name: 'Asistente de Ventas',
        avatar: '🛒',
        conversations: 342,
        satisfaction: 96.5,
        status: 'active',
        change: 15.2
      },
      {
        id: 2,
        name: 'Soporte Técnico',
        avatar: '🔧',
        conversations: 289,
        satisfaction: 92.1,
        status: 'active',
        change: 8.7
      },
      {
        id: 3,
        name: 'Atención al Cliente',
        avatar: '💬',
        conversations: 234,
        satisfaction: 94.8,
        status: 'active',
        change: -2.3
      },
      {
        id: 4,
        name: 'FAQ Automático',
        avatar: '❓',
        conversations: 187,
        satisfaction: 89.2,
        status: 'active',
        change: 22.1
      },
      {
        id: 5,
        name: 'Reservas y Citas',
        avatar: '📅',
        conversations: 156,
        satisfaction: 97.3,
        status: 'active',
        change: 5.8
      }
    ]
    
    // Mock performance metrics
    performanceMetrics.value = {
      response_times: [0.8, 1.2, 0.9, 1.1, 0.7, 1.3, 0.6],
      uptime: 99.8,
      error_rate: 0.2,
      throughput: 1250
    }
  }
  
  const exportReport = async (format = 'pdf', period = '30d') => {
    try {
      isLoading.value = true
      const response = await analyticsAPI.exportReport(format, { period })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `analytics-report-${period}.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Reporte exportado exitosamente')
    } catch (err) {
      console.error('Error exporting report:', err)
      toast.error('Error al exportar el reporte')
    } finally {
      isLoading.value = false
    }
  }
  
  const getRealtimeMetrics = async () => {
    try {
      const response = await analyticsAPI.getRealtimeMetrics()
      return response.data
    } catch (err) {
      console.error('Error getting realtime metrics:', err)
      // Return mock realtime data
      return {
        active_conversations: Math.floor(Math.random() * 50) + 10,
        active_users: Math.floor(Math.random() * 100) + 50,
        messages_per_minute: Math.floor(Math.random() * 20) + 5,
        response_time: Math.random() * 2 + 0.5
      }
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
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    
    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`
    }
    return `${remainingSeconds}s`
  }
  
  const getChangeClass = (change) => {
    if (change > 0) return 'text-green-600'
    if (change < 0) return 'text-red-600'
    return 'text-gray-500'
  }
  
  const getChangeIconClass = (change) => {
    if (change > 0) return 'text-green-500'
    if (change < 0) return 'text-red-500 transform rotate-180'
    return 'text-gray-400'
  }
  
  const getChangeIconPath = (change) => {
    return change !== 0
      ? 'M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z'
      : 'M5 12h14'
  }
  
  const refreshData = () => {
    loadAnalytics()
  }
  
  return {
    // State
    isLoading,
    error,
    metrics,
    chartData,
    topChatbots,
    recentActivity,
    performanceMetrics,
    
    // Computed
    hasData,
    totalActiveUsers,
    averageResponseTime,
    
    // Methods
    loadAnalytics,
    loadMockData,
    exportReport,
    getRealtimeMetrics,
    refreshData,
    
    // Utilities
    formatNumber,
    formatDuration,
    getChangeClass,
    getChangeIconClass,
    getChangeIconPath
  }
}