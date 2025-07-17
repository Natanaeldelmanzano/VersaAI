import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useDashboardStore = defineStore('dashboard', () => {
  // State
  const isLoading = ref(false)
  const stats = ref({
    chatbots: 0,
    users: 0,
    conversations: 0,
    knowledgeBases: 0
  })
  
  const recentChatbots = ref([])
  const recentConversations = ref([])
  const systemMetrics = ref({
    cpu_usage: 0,
    memory_usage: 0,
    disk_usage: 0,
    active_connections: 0
  })
  
  const analytics = ref({
    daily_conversations: [],
    user_satisfaction: 0,
    response_time: 0,
    popular_topics: []
  })
  
  const toast = useToast()

  // Getters
  const totalStats = computed(() => {
    return stats.value.chatbots + stats.value.users + 
           stats.value.conversations + stats.value.knowledgeBases
  })
  
  const hasData = computed(() => totalStats.value > 0)
  
  const formattedStats = computed(() => {
    return {
      chatbots: {
        value: stats.value.chatbots,
        label: 'Chatbots',
        color: 'blue',
        icon: 'ChatBubbleLeftRightIcon'
      },
      users: {
        value: stats.value.users,
        label: 'Usuarios',
        color: 'green',
        icon: 'UsersIcon'
      },
      conversations: {
        value: stats.value.conversations,
        label: 'Conversaciones',
        color: 'purple',
        icon: 'ChatBubbleOvalLeftEllipsisIcon'
      },
      knowledgeBases: {
        value: stats.value.knowledgeBases,
        label: 'Bases de Conocimiento',
        color: 'orange',
        icon: 'BookOpenIcon'
      }
    }
  })

  // Actions
  const fetchDashboardStats = async () => {
    try {
      isLoading.value = true
      
      const response = await axios.get('/api/v1/dashboard/stats')
      
      stats.value = {
        chatbots: response.data.chatbots || 0,
        users: response.data.users || 0,
        conversations: response.data.conversations || 0,
        knowledgeBases: response.data.knowledge_bases || 0
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch dashboard stats error:', error)
      
      // Fallback to mock data if API is not available
      if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
        console.warn('API not available, using mock data')
        stats.value = {
          chatbots: Math.floor(Math.random() * 10) + 3,
          users: Math.floor(Math.random() * 200) + 50,
          conversations: Math.floor(Math.random() * 2000) + 500,
          knowledgeBases: Math.floor(Math.random() * 15) + 5
        }
        return { success: true, data: stats.value, mock: true }
      }
      
      toast.error('Error al cargar las estadísticas del dashboard')
      return { success: false, error: error.message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchRecentChatbots = async (limit = 5) => {
    try {
      const response = await axios.get('/api/v1/chatbots', {
        params: {
          limit,
          sort: 'created_at',
          order: 'desc'
        }
      })
      
      recentChatbots.value = response.data.items || response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch recent chatbots error:', error)
      
      // Fallback to mock data
      if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
        recentChatbots.value = [
          {
            id: 1,
            name: 'Asistente de Ventas',
            description: 'Chatbot para atención al cliente',
            status: 'active',
            created_at: new Date().toISOString()
          },
          {
            id: 2,
            name: 'Soporte Técnico',
            description: 'Ayuda con problemas técnicos',
            status: 'active',
            created_at: new Date(Date.now() - 86400000).toISOString()
          }
        ]
        return { success: true, data: recentChatbots.value, mock: true }
      }
      
      return { success: false, error: error.message }
    }
  }
  
  const fetchRecentConversations = async (limit = 10) => {
    try {
      const response = await axios.get('/api/v1/conversations', {
        params: {
          limit,
          sort: 'created_at',
          order: 'desc'
        }
      })
      
      recentConversations.value = response.data.items || response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch recent conversations error:', error)
      
      // Fallback to mock data
      if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
        recentConversations.value = [
          {
            id: 1,
            user_name: 'Usuario Anónimo',
            chatbot_name: 'Asistente de Ventas',
            last_message: '¿Cuáles son sus precios?',
            created_at: new Date().toISOString(),
            status: 'active'
          },
          {
            id: 2,
            user_name: 'Cliente Premium',
            chatbot_name: 'Soporte Técnico',
            last_message: 'Necesito ayuda con la configuración',
            created_at: new Date(Date.now() - 3600000).toISOString(),
            status: 'resolved'
          }
        ]
        return { success: true, data: recentConversations.value, mock: true }
      }
      
      return { success: false, error: error.message }
    }
  }
  
  const fetchSystemMetrics = async () => {
    try {
      const response = await axios.get('/api/v1/system/metrics')
      
      systemMetrics.value = {
        cpu_usage: response.data.cpu_usage || 0,
        memory_usage: response.data.memory_usage || 0,
        disk_usage: response.data.disk_usage || 0,
        active_connections: response.data.active_connections || 0
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch system metrics error:', error)
      
      // Fallback to mock data
      if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
        systemMetrics.value = {
          cpu_usage: Math.floor(Math.random() * 80) + 10,
          memory_usage: Math.floor(Math.random() * 70) + 20,
          disk_usage: Math.floor(Math.random() * 60) + 30,
          active_connections: Math.floor(Math.random() * 100) + 10
        }
        return { success: true, data: systemMetrics.value, mock: true }
      }
      
      return { success: false, error: error.message }
    }
  }
  
  const fetchAnalytics = async (period = '7d') => {
    try {
      const response = await axios.get('/api/v1/analytics/overview', {
        params: { period }
      })
      
      analytics.value = {
        daily_conversations: response.data.daily_conversations || [],
        user_satisfaction: response.data.user_satisfaction || 0,
        response_time: response.data.avg_response_time || 0,
        popular_topics: response.data.popular_topics || []
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch analytics error:', error)
      
      // Fallback to mock data
      if (error.response?.status === 404 || error.code === 'ECONNREFUSED') {
        const mockData = []
        for (let i = 6; i >= 0; i--) {
          const date = new Date()
          date.setDate(date.getDate() - i)
          mockData.push({
            date: date.toISOString().split('T')[0],
            conversations: Math.floor(Math.random() * 100) + 20
          })
        }
        
        analytics.value = {
          daily_conversations: mockData,
          user_satisfaction: Math.floor(Math.random() * 30) + 70,
          response_time: Math.floor(Math.random() * 3000) + 500,
          popular_topics: [
            { topic: 'Precios', count: 45 },
            { topic: 'Soporte', count: 32 },
            { topic: 'Características', count: 28 }
          ]
        }
        return { success: true, data: analytics.value, mock: true }
      }
      
      return { success: false, error: error.message }
    }
  }
  
  const refreshAllData = async () => {
    try {
      isLoading.value = true
      
      const results = await Promise.allSettled([
        fetchDashboardStats(),
        fetchRecentChatbots(),
        fetchRecentConversations(),
        fetchSystemMetrics(),
        fetchAnalytics()
      ])
      
      const hasErrors = results.some(result => result.status === 'rejected')
      
      if (!hasErrors) {
        toast.success('Datos actualizados correctamente')
      }
      
      return { success: !hasErrors }
    } catch (error) {
      console.error('Refresh all data error:', error)
      toast.error('Error al actualizar los datos')
      return { success: false, error: error.message }
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    isLoading,
    stats,
    recentChatbots,
    recentConversations,
    systemMetrics,
    analytics,
    
    // Getters
    totalStats,
    hasData,
    formattedStats,
    
    // Actions
    fetchDashboardStats,
    fetchRecentChatbots,
    fetchRecentConversations,
    fetchSystemMetrics,
    fetchAnalytics,
    refreshAllData
  }
})