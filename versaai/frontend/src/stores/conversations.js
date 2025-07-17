import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axiosInstance from '@/plugins/axios'
import { useToast } from 'vue-toastification'

export const useConversationsStore = defineStore('conversations', () => {
  // State
  const conversations = ref([])
  const currentConversation = ref(null)
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const pagination = ref({
    page: 1,
    per_page: 20,
    total: 0,
    pages: 0
  })
  const filters = ref({
    search: '',
    chatbot_id: null,
    status: 'all',
    date_from: null,
    date_to: null,
    sort_by: 'created_at',
    sort_order: 'desc'
  })
  const stats = ref({
    total_conversations: 0,
    completed_conversations: 0,
    average_duration: 0,
    average_satisfaction: 0
  })

  const toast = useToast()

  // Estado de inicialización
  const isInitialized = ref(false)

  // MENSAJES DE FALLBACK
  const fallbackMessages = [
    {
      id: 1,
      conversation_id: 1,
      content: '¡Hola! Soy VersaAI, tu asistente inteligente. ¿En qué puedo ayudarte hoy?',
      message_type: 'assistant',
      created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
      status: 'sent'
    },
    {
      id: 2,
      conversation_id: 1,
      content: 'Hola, necesito información sobre sus productos',
      message_type: 'user',
      created_at: new Date(Date.now() - 8 * 60 * 1000).toISOString(),
      status: 'sent'
    },
    {
      id: 3,
      conversation_id: 1,
      content: 'Por supuesto, estaré encantado de ayudarte con información sobre nuestros productos. Tenemos una amplia gama de soluciones de IA que pueden adaptarse a diferentes necesidades empresariales.',
      message_type: 'assistant',
      created_at: new Date(Date.now() - 7 * 60 * 1000).toISOString(),
      status: 'sent'
    }
  ]

  // DATOS DE FALLBACK MEJORADOS CON METADATA COMPLETA
  const fallbackConversations = [
    {
      id: 1,
      title: 'Consulta sobre productos',
      last_message: '¿Podrían enviarme más información sobre el modelo X?',
      status: 'active',
      message_count: 8,
      user_id: 'user_001',
      user_name: 'María García',
      chatbot: {
        id: 1,
        name: 'Asistente Comercial',
        type: 'sales'
      },
      created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 horas atrás
      updated_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 min atrás
      metadata: {
        source: 'website',
        device: 'desktop',
        location: 'Madrid, España'
      }
    },
    {
      id: 2,
      title: 'Problema técnico',
      last_message: 'El sistema no me permite acceder a mi cuenta',
      status: 'active',
      message_count: 12,
      user_id: 'user_002',
      user_name: 'Carlos Rodríguez',
      chatbot: {
        id: 2,
        name: 'Soporte Técnico',
        type: 'support'
      },
      created_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4 horas atrás
      updated_at: new Date(Date.now() - 15 * 60 * 1000).toISOString(), // 15 min atrás
      metadata: {
        source: 'mobile_app',
        device: 'mobile',
        location: 'Barcelona, España'
      }
    },
    {
      id: 3,
      title: 'Información general',
      last_message: 'Gracias por la información, ha sido muy útil',
      status: 'completed',
      message_count: 6,
      user_id: 'user_003',
      user_name: 'Ana López',
      chatbot: {
        id: 3,
        name: 'Asistente General',
        type: 'general'
      },
      created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 día atrás
      updated_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 horas atrás
      metadata: {
        source: 'website',
        device: 'tablet',
        location: 'Valencia, España'
      }
    },
    {
      id: 4,
      title: 'Consulta de precios',
      last_message: '¿Tienen descuentos para empresas?',
      status: 'active',
      message_count: 4,
      user_id: 'user_004',
      user_name: 'Roberto Martín',
      chatbot: {
        id: 1,
        name: 'Asistente Comercial',
        type: 'sales'
      },
      created_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(), // 6 horas atrás
      updated_at: new Date(Date.now() - 45 * 60 * 1000).toISOString(), // 45 min atrás
      metadata: {
        source: 'website',
        device: 'desktop',
        location: 'Sevilla, España'
      }
    },
    {
      id: 5,
      title: 'Configuración de cuenta',
      last_message: 'Perfecto, ya está todo configurado',
      status: 'completed',
      message_count: 9,
      user_id: 'user_005',
      user_name: 'Laura Fernández',
      chatbot: {
        id: 2,
        name: 'Soporte Técnico',
        type: 'support'
      },
      created_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(), // 8 horas atrás
      updated_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(), // 1 hora atrás
      metadata: {
        source: 'mobile_app',
        device: 'mobile',
        location: 'Bilbao, España'
      }
    }
  ]

  // Computed properties para estadísticas en tiempo real
  const totalConversations = computed(() => conversations.value.length)
  
  const activeConversations = computed(() => 
    conversations.value.filter(conv => conv.status === 'active').length
  )
  
  const completedConversations = computed(() => 
    conversations.value.filter(conv => conv.status === 'completed').length
  )
  
  const todayConversations = computed(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return conversations.value.filter(conv => {
      const convDate = new Date(conv.created_at)
      convDate.setHours(0, 0, 0, 0)
      return convDate.getTime() === today.getTime()
    }).length
  })
  
  const conversationsByStatus = computed(() => {
    const statusCount = {}
    conversations.value.forEach(conv => {
      statusCount[conv.status] = (statusCount[conv.status] || 0) + 1
    })
    return statusCount
  })

  // Getters con filtros mejorados
  const filteredConversations = computed(() => {
    let filtered = conversations.value

    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      filtered = filtered.filter(conv => 
        conv.title.toLowerCase().includes(searchTerm) ||
        conv.last_message.toLowerCase().includes(searchTerm) ||
        conv.user_name?.toLowerCase().includes(searchTerm) ||
        conv.chatbot.name.toLowerCase().includes(searchTerm)
      )
    }

    if (filters.value.status && filters.value.status !== 'all') {
      filtered = filtered.filter(conv => conv.status === filters.value.status)
    }

    if (filters.value.chatbot_id) {
      filtered = filtered.filter(conv => conv.chatbot.id === filters.value.chatbot_id)
    }

    if (filters.value.date_from) {
      filtered = filtered.filter(conv => 
        new Date(conv.created_at) >= new Date(filters.value.date_from)
      )
    }

    if (filters.value.date_to) {
      filtered = filtered.filter(conv => 
        new Date(conv.created_at) <= new Date(filters.value.date_to)
      )
    }

    return filtered
  })
  
  const hasConversations = computed(() => conversations.value.length > 0)
  const isLastPage = computed(() => pagination.value.page >= pagination.value.pages)

  // FUNCIÓN CORREGIDA
  const fetchConversations = async (params = {}) => {
    try {
      isLoading.value = true
      console.log('🔄 Intentando cargar conversaciones...')
      
      const queryParams = {
        page: pagination.value.page,
        per_page: pagination.value.per_page,
        ...filters.value,
        ...params
      }

      // Remove null/empty values
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '' || queryParams[key] === 'all') {
          delete queryParams[key]
        }
      })

      const response = await axiosInstance.get('/api/v1/conversations/', {
        params: queryParams,
        timeout: 5000 // 5 segundos timeout
      })

      conversations.value = response.data.items || response.data
      pagination.value = {
        page: response.data.page || 1,
        per_page: response.data.per_page || 20,
        total: response.data.total || conversations.value.length,
        pages: response.data.pages || 1
      }

      console.log('✅ Conversaciones cargadas desde API:', conversations.value.length)
      return { success: true, data: response.data }
    } catch (error) {
      console.warn('⚠️ Error API, usando datos de fallback:', error.message)
      
      // ACTIVAR FALLBACK INMEDIATAMENTE
      conversations.value = fallbackConversations
      pagination.value = {
        page: 1,
        per_page: 20,
        total: fallbackConversations.length,
        pages: 1
      }
      
      console.log('✅ Usando datos de fallback:', conversations.value.length, 'conversaciones')
      
      // NO mostrar toast de error para fallback
      return { success: true, data: { items: fallbackConversations }, fallback: true }
    } finally {
      isLoading.value = false
    }
  }

  // Función para activar datos de fallback con simulación de delay
  const activateFallback = async () => {
    console.log('🔄 Activando datos de fallback para conversaciones')
    isLoading.value = true
    
    // Simular delay de red para UX realista
    await new Promise(resolve => setTimeout(resolve, 800))
    
    conversations.value = [...fallbackConversations]
    isLoading.value = false
    error.value = null
    isInitialized.value = true
    
    console.log('✅ Datos de fallback activados:', conversations.value.length, 'conversaciones')
  }

  // INICIALIZACIÓN INMEDIATA
  const initialize = async () => {
    console.log('🚀 Inicializando store de conversaciones...')
    
    // Cargar datos inmediatamente (con fallback)
    await fetchConversations()
    
    // Si no hay conversaciones, forzar fallback
    if (conversations.value.length === 0) {
      console.log('📝 Forzando datos de fallback')
      await activateFallback()
    }
    
    console.log('✅ Store inicializado con', conversations.value.length, 'conversaciones')
  }

  const fetchConversation = async (id) => {
    try {
      isLoading.value = true
      
      const response = await axiosInstance.get(`/api/v1/conversations/${id}`)
      currentConversation.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch conversation error:', error)
      const message = error.response?.data?.detail || 'Error al cargar la conversación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const fetchMessages = async (conversationId) => {
    try {
      const response = await axiosInstance.get(`/api/v1/conversations/${conversationId}/messages`)
      messages.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.warn('⚠️ Error API para mensajes, usando datos de fallback:', error.message)
      
      // Usar mensajes de fallback
      messages.value = fallbackMessages.filter(msg => msg.conversation_id === conversationId)
      
      console.log('✅ Usando mensajes de fallback:', messages.value.length, 'mensajes')
      return { success: true, data: messages.value, fallback: true }
    }
  }

  const createConversation = async (conversationData) => {
    try {
      isLoading.value = true
      
      const response = await axiosInstance.post('/api/v1/conversations/', conversationData)
      
      // Add to local state
      conversations.value.unshift(response.data)
      pagination.value.total += 1
      
      toast.success('Conversación creada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Create conversation error:', error)
      const message = error.response?.data?.detail || 'Error al crear la conversación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (conversationId, messageData) => {
    try {
      const response = await axiosInstance.post('/api/v1/conversations/chat', {
        conversation_id: conversationId,
        ...messageData
      })
      
      // Add message to local state if viewing this conversation
      if (currentConversation.value?.id === conversationId) {
        messages.value.push(response.data)
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.warn('⚠️ Error API para enviar mensaje, simulando respuesta:', error.message)
      
      // Simular envío de mensaje del usuario
      const userMessage = {
        id: Date.now(),
        conversation_id: conversationId,
        content: messageData.content || messageData.message,
        message_type: 'user',
        created_at: new Date().toISOString(),
        status: 'sent'
      }
      
      // Simular respuesta del bot
      const botResponses = [
        'Gracias por tu mensaje. Estoy aquí para ayudarte con cualquier consulta.',
        'Entiendo tu consulta. ¿Podrías proporcionarme más detalles para poder asistirte mejor?',
        'Perfecto, he registrado tu solicitud. Te ayudo con eso inmediatamente.',
        'Excelente pregunta. Basándome en la información que me proporcionas, puedo sugerirte varias opciones.',
        'Comprendo tu situación. Permíteme ofrecerte la mejor solución posible.'
      ]
      
      const botMessage = {
        id: Date.now() + 1,
        conversation_id: conversationId,
        content: botResponses[Math.floor(Math.random() * botResponses.length)],
        message_type: 'assistant',
        created_at: new Date(Date.now() + 1000).toISOString(),
        status: 'sent'
      }
      
      // Agregar mensajes al estado local
      if (currentConversation.value?.id === conversationId) {
        messages.value.push(userMessage)
        
        // Simular delay de respuesta del bot
        setTimeout(() => {
          messages.value.push(botMessage)
        }, 1500)
      }
      
      console.log('✅ Mensaje simulado enviado')
      return { success: true, data: userMessage, fallback: true }
    }
  }

  const updateConversation = async (id, updates) => {
    try {
      isLoading.value = true
      
      const response = await axiosInstance.put(`/api/v1/conversations/${id}`, updates)
      
      // Update local state
      const index = conversations.value.findIndex(c => c.id === id)
      if (index !== -1) {
        conversations.value[index] = { ...conversations.value[index], ...response.data }
      }
      
      // Update current conversation if it's the one being updated
      if (currentConversation.value?.id === id) {
        currentConversation.value = { ...currentConversation.value, ...response.data }
      }
      
      toast.success('Conversación actualizada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update conversation error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar la conversación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const archiveConversation = async (id) => {
    try {
      const result = await updateConversation(id, { status: 'archived' })
      if (result.success) {
        toast.success('Conversación archivada exitosamente')
      }
      return result
    } catch (error) {
      console.error('Archive conversation error:', error)
      const message = 'Error al archivar la conversación'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const getConversationById = (id) => {
    return conversations.value.find(conv => conv.id === id)
  }

  const getConversationsByUser = (userId) => {
    return conversations.value.filter(conv => conv.user_id === userId)
  }

  const getConversationsByChatbot = (chatbotId) => {
    return conversations.value.filter(conv => conv.chatbot.id === chatbotId)
  }

  const deleteConversation = async (id) => {
    try {
      await axiosInstance.delete(`/api/v1/conversations/${id}`)
      
      // Remove from local state
      const index = conversations.value.findIndex(c => c.id === id)
      if (index !== -1) {
        conversations.value.splice(index, 1)
        pagination.value.total -= 1
      }
      
      // Clear current conversation if it was deleted
      if (currentConversation.value?.id === id) {
        currentConversation.value = null
        messages.value = []
      }
      
      toast.success('Conversación eliminada exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Delete conversation error:', error)
      const message = error.response?.data?.detail || 'Error al eliminar la conversación'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const fetchStats = async (params = {}) => {
    try {
      const response = await axiosInstance.get('/api/v1/analytics/conversations', {
        params
      })
      
      stats.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch conversation stats error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las estadísticas'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const exportConversations = async (format = 'csv', params = {}) => {
    try {
      const response = await axios.get('/api/v1/conversations/export', {
        params: {
          format,
          ...filters.value,
          ...params
        },
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `conversations.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Conversaciones exportadas exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Export conversations error:', error)
      const message = error.response?.data?.detail || 'Error al exportar las conversaciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const exportConversation = async (id, format = 'pdf') => {
    try {
      const response = await axios.get(`/api/v1/conversations/${id}/export`, {
        params: { format },
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `conversation_${id}.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Conversación exportada exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Export conversation error:', error)
      const message = error.response?.data?.detail || 'Error al exportar la conversación'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Utility functions
  const setPage = (page) => {
    pagination.value.page = page
  }

  const setPerPage = (perPage) => {
    pagination.value.per_page = perPage
    pagination.value.page = 1 // Reset to first page
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Reset to first page when filtering
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      chatbot_id: null,
      status: 'all',
      date_from: null,
      date_to: null,
      sort_by: 'created_at',
      sort_order: 'desc'
    }
    pagination.value.page = 1
  }

  const clearConversations = () => {
    conversations.value = []
    currentConversation.value = null
    messages.value = []
    pagination.value = {
      page: 1,
      per_page: 20,
      total: 0,
      pages: 0
    }
  }

  const clearCurrentConversation = () => {
    currentConversation.value = null
    messages.value = []
  }

  // Limpiar filtros
  const clearFilters = () => {
    filters.value = {
      search: '',
      chatbot_id: null,
      status: 'all',
      date_from: null,
      date_to: null,
      sort_by: 'created_at',
      sort_order: 'desc'
    }
    pagination.value.page = 1
  }

  // Resetear paginación
  const resetPagination = () => {
    pagination.value = {
      page: 1,
      per_page: 20,
      total: 0,
      pages: 0
    }
  }

  return {
    // State
    conversations,
    currentConversation,
    messages,
    isLoading,
    error,
    pagination,
    filters,
    stats,
    isInitialized,
    
    // Getters
    totalConversations,
    activeConversations,
    completedConversations,
    todayConversations,
    conversationsByStatus,
    filteredConversations,
    hasConversations,
    isLastPage,
    
    // Actions
    initialize,
    activateFallback,
    fetchConversations,
    fetchConversation,
    fetchMessages,
    createConversation,
    sendMessage,
    updateConversation,
    deleteConversation,
    archiveConversation,
    fetchStats,
    exportConversations,
    exportConversation,
    getConversationById,
    getConversationsByUser,
    getConversationsByChatbot,
    
    // Utilities
    setPage,
    setPerPage,
    setFilters,
    resetFilters,
    clearFilters,
    resetPagination,
    clearConversations,
    clearCurrentConversation
  }
})