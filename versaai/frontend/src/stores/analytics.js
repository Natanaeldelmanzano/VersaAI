import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useAnalyticsStore = defineStore('analytics', () => {
  // State
  const overview = ref({
    total_conversations: 0,
    unique_users: 0,
    average_satisfaction: 0,
    average_response_time: 0,
    total_chatbots: 0,
    active_chatbots: 0,
    total_messages: 0,
    growth_rate: 0
  })
  
  const conversationMetrics = ref({
    daily_conversations: [],
    hourly_distribution: [],
    conversation_duration: [],
    completion_rate: 0
  })
  
  const userEngagement = ref({
    new_users: [],
    returning_users: [],
    user_retention: [],
    session_duration: []
  })
  
  const chatbotPerformance = ref({
    top_chatbots: [],
    response_accuracy: [],
    resolution_rate: [],
    user_satisfaction: []
  })
  
  const responseMetrics = ref({
    average_response_time: [],
    response_time_distribution: [],
    peak_hours: [],
    slowest_responses: []
  })
  
  const topQueries = ref([])
  const recentFeedback = ref([])
  
  const isLoading = ref(false)
  const selectedPeriod = ref('7d')
  const dateRange = ref({
    start_date: null,
    end_date: null
  })
  
  const toast = useToast()

  // Getters
  const hasData = computed(() => {
    return overview.value.total_conversations > 0
  })
  
  const formattedResponseTime = computed(() => {
    const time = overview.value.average_response_time
    if (time < 1000) return `${Math.round(time)}ms`
    return `${(time / 1000).toFixed(1)}s`
  })
  
  const satisfactionPercentage = computed(() => {
    return Math.round(overview.value.average_satisfaction * 100)
  })
  
  const growthTrend = computed(() => {
    const rate = overview.value.growth_rate
    return {
      value: Math.abs(rate),
      direction: rate >= 0 ? 'up' : 'down',
      color: rate >= 0 ? 'text-green-600' : 'text-red-600'
    }
  })

  // Actions
  const fetchOverview = async (params = {}) => {
    try {
      isLoading.value = true
      
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      // Remove null values
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/overview', {
        params: queryParams
      })
      
      overview.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch overview error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas generales'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchConversationMetrics = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/conversations', {
        params: queryParams
      })
      
      conversationMetrics.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch conversation metrics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas de conversaciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchUserEngagement = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/users', {
        params: queryParams
      })
      
      userEngagement.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch user engagement error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas de usuarios'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchChatbotPerformance = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/chatbots', {
        params: queryParams
      })
      
      chatbotPerformance.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch chatbot performance error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas de chatbots'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchResponseMetrics = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/response-times', {
        params: queryParams
      })
      
      responseMetrics.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch response metrics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas de respuesta'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchTopQueries = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        limit: 10,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/top-queries', {
        params: queryParams
      })
      
      topQueries.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch top queries error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las consultas más frecuentes'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchRecentFeedback = async (params = {}) => {
    try {
      const queryParams = {
        limit: 10,
        ...params
      }
      
      const response = await axios.get('/api/v1/analytics/feedback', {
        params: queryParams
      })
      
      recentFeedback.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch recent feedback error:', error)
      const message = error.response?.data?.detail || 'Error al cargar los comentarios recientes'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchAllMetrics = async (params = {}) => {
    try {
      isLoading.value = true
      
      // Fetch all metrics in parallel
      const promises = [
        fetchOverview(params),
        fetchConversationMetrics(params),
        fetchUserEngagement(params),
        fetchChatbotPerformance(params),
        fetchResponseMetrics(params),
        fetchTopQueries(params),
        fetchRecentFeedback(params)
      ]
      
      const results = await Promise.allSettled(promises)
      
      // Check if any failed
      const failures = results.filter(result => result.status === 'rejected')
      if (failures.length > 0) {
        console.warn('Some metrics failed to load:', failures)
      }
      
      return { success: true }
    } catch (error) {
      console.error('Fetch all metrics error:', error)
      const message = 'Error al cargar las métricas'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const exportReport = async (format = 'pdf', params = {}) => {
    try {
      const queryParams = {
        format,
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/export', {
        params: queryParams,
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `analytics_report.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Reporte exportado exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Export report error:', error)
      const message = error.response?.data?.detail || 'Error al exportar el reporte'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const getChatbotAnalytics = async (chatbotId, params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get(`/api/v1/analytics/chatbots/${chatbotId}`, {
        params: queryParams
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get chatbot analytics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las analíticas del chatbot'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const getUsageMetrics = async (params = {}) => {
    try {
      const queryParams = {
        period: selectedPeriod.value,
        ...dateRange.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '') {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/analytics/usage', {
        params: queryParams
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get usage metrics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las métricas de uso'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  // Utility functions
  const setPeriod = (period) => {
    selectedPeriod.value = period
    // Clear custom date range when selecting predefined period
    if (period !== 'custom') {
      dateRange.value = {
        start_date: null,
        end_date: null
      }
    }
  }
  
  const setDateRange = (startDate, endDate) => {
    selectedPeriod.value = 'custom'
    dateRange.value = {
      start_date: startDate,
      end_date: endDate
    }
  }
  
  const clearData = () => {
    overview.value = {
      total_conversations: 0,
      unique_users: 0,
      average_satisfaction: 0,
      average_response_time: 0,
      total_chatbots: 0,
      active_chatbots: 0,
      total_messages: 0,
      growth_rate: 0
    }
    conversationMetrics.value = {
      daily_conversations: [],
      hourly_distribution: [],
      conversation_duration: [],
      completion_rate: 0
    }
    userEngagement.value = {
      new_users: [],
      returning_users: [],
      user_retention: [],
      session_duration: []
    }
    chatbotPerformance.value = {
      top_chatbots: [],
      response_accuracy: [],
      resolution_rate: [],
      user_satisfaction: []
    }
    responseMetrics.value = {
      average_response_time: [],
      response_time_distribution: [],
      peak_hours: [],
      slowest_responses: []
    }
    topQueries.value = []
    recentFeedback.value = []
  }
  
  const refreshData = async () => {
    return await fetchAllMetrics()
  }

  return {
    // State
    overview,
    conversationMetrics,
    userEngagement,
    chatbotPerformance,
    responseMetrics,
    topQueries,
    recentFeedback,
    isLoading,
    selectedPeriod,
    dateRange,
    
    // Getters
    hasData,
    formattedResponseTime,
    satisfactionPercentage,
    growthTrend,
    
    // Actions
    fetchOverview,
    fetchConversationMetrics,
    fetchUserEngagement,
    fetchChatbotPerformance,
    fetchResponseMetrics,
    fetchTopQueries,
    fetchRecentFeedback,
    fetchAllMetrics,
    exportReport,
    getChatbotAnalytics,
    getUsageMetrics,
    
    // Utilities
    setPeriod,
    setDateRange,
    clearData,
    refreshData
  }
})