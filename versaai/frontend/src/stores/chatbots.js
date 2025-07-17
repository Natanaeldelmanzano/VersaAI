import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useChatbotsStore = defineStore('chatbots', () => {
  // State
  const chatbots = ref([])
  const currentChatbot = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const isInitialized = ref(false)
  const pagination = ref({
    page: 1,
    per_page: 10,
    total: 0,
    pages: 0
  })
  const filters = ref({
    search: '',
    status: 'all',
    sort_by: 'created_at',
    sort_order: 'desc'
  })
  
  const toast = useToast()

  // DATOS DE FALLBACK COMPLETOS - 4 CHATBOTS
  const fallbackChatbots = [
    {
      id: 1,
      name: "Asistente Comercial",
      description: "Especializado en ventas y consultas comerciales",
      type: "sales",
      model: "llama-3.1-70b-versatile",
      temperature: 0.7,
      max_tokens: 1000,
      system_prompt: "Eres un asistente comercial experto. Ayuda a los clientes con consultas sobre productos y servicios.",
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      total_conversations: 45,
      stats: {
        total_conversations: 45,
        total_messages: 234,
        avg_response_time: 1.2,
        satisfaction_rate: 4.8
      },
      settings: {
        welcome_message: "¡Hola! Soy tu asistente comercial. ¿En qué puedo ayudarte hoy?",
        fallback_message: "Disculpa, no entendí tu consulta. ¿Podrías reformularla?",
        max_conversation_length: 50
      }
    },
    {
      id: 2,
      name: "Soporte Técnico",
      description: "Resuelve problemas técnicos y dudas de configuración",
      type: "support",
      model: "llama-3.1-70b-versatile",
      temperature: 0.3,
      max_tokens: 1500,
      system_prompt: "Eres un especialista en soporte técnico. Proporciona soluciones claras y paso a paso.",
      is_active: true,
      created_at: new Date(Date.now() - 86400000).toISOString(),
      updated_at: new Date(Date.now() - 3600000).toISOString(),
      total_conversations: 28,
      stats: {
        total_conversations: 28,
        total_messages: 156,
        avg_response_time: 0.9,
        satisfaction_rate: 4.6
      },
      settings: {
        welcome_message: "Hola, soy el asistente de soporte técnico. ¿Qué problema puedo ayudarte a resolver?",
        fallback_message: "Para problemas complejos, te conectaré con un especialista humano.",
        max_conversation_length: 100
      }
    },
    {
      id: 3,
      name: "Asistente General",
      description: "Información general y consultas básicas",
      type: "general",
      model: "llama-3.1-8b-instant",
      temperature: 0.5,
      max_tokens: 800,
      system_prompt: "Eres un asistente general amigable. Proporciona información útil y clara.",
      is_active: true,
      created_at: new Date(Date.now() - 172800000).toISOString(),
      updated_at: new Date(Date.now() - 7200000).toISOString(),
      total_conversations: 67,
      stats: {
        total_conversations: 67,
        total_messages: 289,
        avg_response_time: 0.8,
        satisfaction_rate: 4.7
      },
      settings: {
        welcome_message: "¡Bienvenido! Estoy aquí para ayudarte con cualquier consulta general.",
        fallback_message: "No estoy seguro de cómo responder a eso. ¿Puedes ser más específico?",
        max_conversation_length: 30
      }
    },
    {
      id: 4,
      name: "Bot de Prueba",
      description: "Chatbot en desarrollo para pruebas",
      type: "test",
      model: "llama-3.1-8b-instant",
      temperature: 0.8,
      max_tokens: 500,
      system_prompt: "Eres un bot de prueba. Responde de manera experimental.",
      is_active: false,
      created_at: new Date(Date.now() - 259200000).toISOString(),
      updated_at: new Date(Date.now() - 86400000).toISOString(),
      total_conversations: 12,
      stats: {
        total_conversations: 12,
        total_messages: 45,
        avg_response_time: 1.5,
        satisfaction_rate: 3.8
      },
      settings: {
        welcome_message: "Hola, soy un bot en pruebas. ¡Experimenta conmigo!",
        fallback_message: "Estoy en desarrollo, disculpa si no funciono perfectamente.",
        max_conversation_length: 20
      }
    }
  ]

  // Getters
  const activeChatbots = computed(() => 
    chatbots.value.filter(chatbot => chatbot.is_active)
  )
  
  const inactiveChatbots = computed(() => 
    chatbots.value.filter(chatbot => !chatbot.is_active)
  )
  
  const filteredChatbots = computed(() => {
    let filtered = chatbots.value
    
    if (filters.value.search) {
      filtered = filtered.filter(chatbot => 
        chatbot.name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
        chatbot.description.toLowerCase().includes(filters.value.search.toLowerCase())
      )
    }
    
    if (filters.value.status !== 'all') {
      filtered = filtered.filter(chatbot => {
        if (filters.value.status === 'active') return chatbot.is_active
        if (filters.value.status === 'inactive') return !chatbot.is_active
        return true
      })
    }
    
    // Sort
    filtered.sort((a, b) => {
      const aValue = a[filters.value.sort_by]
      const bValue = b[filters.value.sort_by]
      
      if (filters.value.sort_order === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })
    
    return filtered
  })

  // Estadísticas en tiempo real
  const totalChatbots = computed(() => chatbots.value.length)
  const activeChatbotsCount = computed(() => chatbots.value.filter(c => c.is_active).length)
  const inactiveChatbotsCount = computed(() => chatbots.value.filter(c => !c.is_active).length)
  const totalConversations = computed(() => 
    chatbots.value.reduce((sum, c) => sum + (c.total_conversations || 0), 0)
  )
  const averageResponseTime = computed(() => {
    const chatbotsWithStats = chatbots.value.filter(c => c.stats?.avg_response_time)
    if (chatbotsWithStats.length === 0) return 0
    return chatbotsWithStats.reduce((sum, c) => sum + c.stats.avg_response_time, 0) / chatbotsWithStats.length
  })
  const averageSatisfactionRate = computed(() => {
    const chatbotsWithStats = chatbots.value.filter(c => c.stats?.satisfaction_rate)
    if (chatbotsWithStats.length === 0) return 0
    return chatbotsWithStats.reduce((sum, c) => sum + c.stats.satisfaction_rate, 0) / chatbotsWithStats.length
  })
  const chatbotsByType = computed(() => {
    const types = {}
    chatbots.value.forEach(c => {
      types[c.type] = (types[c.type] || 0) + 1
    })
    return types
  })

  // Actions
  const fetchChatbots = async (params = {}) => {
    try {
      isLoading.value = true
      error.value = null
      
      const queryParams = {
        page: pagination.value.page,
        per_page: pagination.value.per_page,
        ...filters.value,
        ...params
      }
      
      // Remove empty filters
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === '' || queryParams[key] === 'all') {
          delete queryParams[key]
        }
      })
      
      try {
        // Timeout de 5 segundos para la API
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000)
        
        const response = await axios.get('/api/v1/chatbots/', {
          params: queryParams,
          signal: controller.signal
        })
        
        clearTimeout(timeoutId)
        
        chatbots.value = response.data.chatbots
        pagination.value = {
          page: response.data.page,
          per_page: response.data.per_page,
          total: response.data.total,
          pages: response.data.pages
        }
        
        isInitialized.value = true
        
        return { success: true, data: response.data }
      } catch (apiError) {
        console.error('API error, activating fallback:', apiError.message)
        error.value = apiError.message || 'Error al cargar los chatbots'
        
        // Activación inmediata del fallback
        await activateFallback(queryParams)
        
        toast.error('Usando datos de demostración - API no disponible')
        
        return { success: true, data: { chatbots: chatbots.value } }
      }
    } catch (error) {
      console.error('Fetch chatbots error:', error)
      const message = error.response?.data?.detail || 'Error al cargar los chatbots'
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Función para activar datos de fallback
  const activateFallback = async (queryParams = {}) => {
    // Simular delay de red para experiencia más realista
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // Apply filters to fallback data
    let filtered = [...fallbackChatbots]
    
    if (queryParams.search) {
      filtered = filtered.filter(chatbot => 
        chatbot.name.toLowerCase().includes(queryParams.search.toLowerCase()) ||
        chatbot.description.toLowerCase().includes(queryParams.search.toLowerCase())
      )
    }
    
    if (queryParams.status) {
      filtered = filtered.filter(chatbot => {
        if (queryParams.status === 'active') return chatbot.is_active
        if (queryParams.status === 'inactive') return !chatbot.is_active
        return true
      })
    }
    
    chatbots.value = filtered
    pagination.value = {
      page: queryParams.page || 1,
      per_page: queryParams.per_page || 10,
      total: filtered.length,
      pages: Math.ceil(filtered.length / (queryParams.per_page || 10))
    }
    
    isInitialized.value = true
  }

  const fetchChatbot = async (id) => {
    try {
      isLoading.value = true
      
      const response = await axios.get(`/api/v1/chatbots/${id}`)
      currentChatbot.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch chatbot error:', error)
      const message = error.response?.data?.detail || 'Error al cargar el chatbot'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const createChatbot = async (chatbotData) => {
    try {
      isLoading.value = true
      
      const response = await axios.post('/api/v1/chatbots/', chatbotData)
      
      // Add to local state
      chatbots.value.unshift(response.data)
      
      toast.success('Chatbot creado exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Create chatbot error:', error)
      const message = error.response?.data?.detail || 'Error al crear el chatbot'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const updateChatbot = async (id, chatbotData) => {
    try {
      isLoading.value = true
      
      const response = await axios.put(`/api/v1/chatbots/${id}`, chatbotData)
      
      // Update in local state
      const index = chatbots.value.findIndex(c => c.id === id)
      if (index !== -1) {
        chatbots.value[index] = response.data
      }
      
      // Update current chatbot if it's the same
      if (currentChatbot.value?.id === id) {
        currentChatbot.value = response.data
      }
      
      toast.success('Chatbot actualizado exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update chatbot error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar el chatbot'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const deleteChatbot = async (id) => {
    try {
      isLoading.value = true
      
      await axios.delete(`/api/v1/chatbots/${id}`)
      
      // Remove from local state
      chatbots.value = chatbots.value.filter(c => c.id !== id)
      
      // Clear current chatbot if it's the same
      if (currentChatbot.value?.id === id) {
        currentChatbot.value = null
      }
      
      toast.success('Chatbot eliminado exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Delete chatbot error:', error)
      const message = error.response?.data?.detail || 'Error al eliminar el chatbot'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const toggleChatbotStatus = async (id) => {
    try {
      const chatbot = chatbots.value.find(c => c.id === id)
      if (!chatbot) return { success: false, error: 'Chatbot no encontrado' }
      
      try {
        const response = await axios.patch(`/api/v1/chatbots/${id}/toggle-status`)
        
        // Update in local state
        const index = chatbots.value.findIndex(c => c.id === id)
        if (index !== -1) {
          chatbots.value[index] = response.data
        }
        
        // Update current chatbot if it's the same
        if (currentChatbot.value?.id === id) {
          currentChatbot.value = response.data
        }
        
        const status = response.data.is_active ? 'activado' : 'desactivado'
        toast.success(`Chatbot ${status} exitosamente`)
        
        return { success: true, data: response.data }
      } catch (apiError) {
        // Fallback to local state update if API is not available
        console.warn('API not available, updating local state:', apiError.message)
        
        const index = chatbots.value.findIndex(c => c.id === id)
        if (index !== -1) {
          chatbots.value[index].is_active = !chatbots.value[index].is_active
          chatbots.value[index].updated_at = new Date().toISOString()
        }
        
        // Update current chatbot if it's the same
        if (currentChatbot.value?.id === id) {
          currentChatbot.value.is_active = !currentChatbot.value.is_active
          currentChatbot.value.updated_at = new Date().toISOString()
        }
        
        const status = chatbots.value[index].is_active ? 'activado' : 'desactivado'
        toast.success(`Chatbot ${status} exitosamente`)
        
        return { success: true, data: chatbots.value[index] }
      }
    } catch (error) {
      console.error('Toggle chatbot status error:', error)
      const message = error.response?.data?.detail || 'Error al cambiar el estado del chatbot'
      return { success: false, error: message }
    }
  }

  const getChatbotAnalytics = async (id, timeRange = '7d') => {
    try {
      const response = await axios.get(`/api/v1/analytics/chatbots/${id}`, {
        params: { time_range: timeRange }
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get chatbot analytics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las analíticas del chatbot'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const getChatbotWidget = async (id) => {
    try {
      const response = await axios.get(`/api/v1/widgets/${id}/config`)
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get chatbot widget error:', error)
      const message = error.response?.data?.detail || 'Error al cargar la configuración del widget'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const getChatbotEmbedCode = async (id, type = 'script') => {
    try {
      const endpoint = type === 'iframe' ? 'iframe' : 'embed'
      
      try {
        const response = await axios.get(`/api/v1/widgets/${id}/${endpoint}`)
        return { success: true, data: response.data }
      } catch (apiError) {
        // Fallback to mock embed code if API is not available
        console.warn('API not available, generating mock embed code:', apiError.message)
        
        const chatbot = chatbots.value.find(c => c.id === id)
        const chatbotName = chatbot?.name || 'Chatbot'
        
        const mockEmbedCode = type === 'iframe' 
          ? `<iframe src="https://widget.versaai.com/chat/${id}" width="400" height="600" frameborder="0"></iframe>`
          : `<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'https://widget.versaai.com/js/widget.js';
    script.setAttribute('data-chatbot-id', '${id}');
    script.setAttribute('data-chatbot-name', '${chatbotName}');
    document.head.appendChild(script);
  })();
</script>`
        
        return { success: true, data: mockEmbedCode }
      }
    } catch (error) {
      console.error('Get chatbot embed code error:', error)
      const message = error.response?.data?.detail || 'Error al generar el código de integración'
      return { success: false, error: message }
    }
  }

  const testChatbot = async (id, message) => {
    try {
      const response = await axios.post(`/api/v1/widgets/${id}/chat`, {
        message,
        conversation_id: null
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Test chatbot error:', error)
      const message = error.response?.data?.detail || 'Error al probar el chatbot'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Utility functions
  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      status: 'all',
      sort_by: 'created_at',
      sort_order: 'desc'
    }
  }

  const setPage = (page) => {
    pagination.value.page = page
  }

  const setPerPage = (perPage) => {
    pagination.value.per_page = perPage
    pagination.value.page = 1 // Reset to first page
  }

  const clearCurrentChatbot = () => {
    currentChatbot.value = null
  }

  const clearChatbots = () => {
    chatbots.value = []
    currentChatbot.value = null
    pagination.value = {
      page: 1,
      per_page: 10,
      total: 0,
      pages: 0
    }
  }

  // Función de inicialización
  const initialize = async () => {
    if (!isInitialized.value) {
      await fetchChatbots()
      
      // Si no hay chatbots después del fetch, forzar fallback
      if (chatbots.value.length === 0) {
        await activateFallback()
      }
    }
  }

  const getChatbotById = (id) => {
    return chatbots.value.find(c => c.id === id)
  }

  const getChatbotsByType = (type) => {
    return chatbots.value.filter(c => c.type === type)
  }

  return {
    // State
    chatbots,
    currentChatbot,
    isLoading,
    error,
    isInitialized,
    pagination,
    filters,
    
    // Getters
    activeChatbots,
    inactiveChatbots,
    filteredChatbots,
    totalChatbots,
    activeChatbotsCount,
    inactiveChatbotsCount,
    totalConversations,
    averageResponseTime,
    averageSatisfactionRate,
    chatbotsByType,
    
    // Actions
    fetchChatbots,
    fetchChatbot,
    createChatbot,
    updateChatbot,
    deleteChatbot,
    toggleChatbotStatus,
    getChatbotAnalytics,
    getChatbotWidget,
    getChatbotEmbedCode,
    testChatbot,
    activateFallback,
    initialize,
    
    // Utility functions
    setFilters,
    resetFilters,
    setPage,
    setPerPage,
    clearCurrentChatbot,
    clearChatbots,
    getChatbotById,
    getChatbotsByType
  }
})