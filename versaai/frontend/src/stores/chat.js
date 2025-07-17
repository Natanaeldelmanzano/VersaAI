// frontend/src/stores/chat.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useChatStore = defineStore('chat', () => {
  // Estado
  const conversations = ref([])
  const currentMessages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const currentConversationId = ref(null)

  // Getters
  const hasConversations = computed(() => conversations.value.length > 0)
  const totalMessages = computed(() => currentMessages.value.length)
  const isConnected = computed(() => !error.value)

  // Actions
  const loadConversations = async () => {
    try {
      isLoading.value = true
      error.value = null

      const response = await axios.get('/api/conversations')

      if (response.data.success) {
        conversations.value = response.data.conversations
        console.log('✅ Conversaciones cargadas:', conversations.value.length)
      } else {
        // Datos de ejemplo si no hay conversaciones
        conversations.value = [
          {
            id: 1,
            title: 'Consulta sobre productos',
            user: 'Usuario Demo',
            lastMessage: '¿Podrías ayudarme con información sobre sus servicios?',
            updatedAt: new Date().toISOString(),
            status: 'active'
          },
          {
            id: 2,
            title: 'Soporte técnico',
            user: 'Cliente VIP',
            lastMessage: 'Necesito ayuda con la configuración',
            updatedAt: new Date(Date.now() - 3600000).toISOString(),
            status: 'resolved'
          },
          {
            id: 3,
            title: 'Información general',
            user: 'Nuevo Cliente',
            lastMessage: 'Hola, me gustaría conocer más sobre VersaAI',
            updatedAt: new Date(Date.now() - 7200000).toISOString(),
            status: 'active'
          }
        ]
        console.log('📝 Usando datos de ejemplo para conversaciones')
      }
    } catch (err) {
      console.error('❌ Error cargando conversaciones:', err)
      error.value = 'Error al cargar conversaciones'

      // Datos de fallback
      conversations.value = [
        {
          id: 1,
          title: 'Conversación de ejemplo',
          user: 'Usuario Demo',
          lastMessage: 'Hola, ¿cómo puedo ayudarte?',
          updatedAt: new Date().toISOString(),
          status: 'active'
        }
      ]
    } finally {
      isLoading.value = false
    }
  }

  const loadConversation = async (conversationId) => {
    try {
      isLoading.value = true
      currentConversationId.value = conversationId

      const response = await axios.get(`/api/conversations/${conversationId}/messages`)

      if (response.data.success) {
        currentMessages.value = response.data.messages
        console.log('✅ Mensajes cargados:', currentMessages.value.length)
      } else {
        // Mensajes de ejemplo
        currentMessages.value = [
          {
            id: 1,
            text: 'Hola, ¿cómo puedo ayudarte hoy?',
            sender: 'bot',
            timestamp: new Date(Date.now() - 300000).toISOString()
          },
          {
            id: 2,
            text: '¿Podrías darme información sobre sus servicios?',
            sender: 'user',
            timestamp: new Date(Date.now() - 240000).toISOString()
          },
          {
            id: 3,
            text: 'Por supuesto. VersaAI ofrece una amplia gama de servicios de IA empresarial, incluyendo chatbots inteligentes, análisis de datos y automatización de procesos.',
            sender: 'bot',
            timestamp: new Date(Date.now() - 180000).toISOString()
          },
          {
            id: 4,
            text: '¿Qué tipo de integración ofrecen?',
            sender: 'user',
            timestamp: new Date(Date.now() - 120000).toISOString()
          },
          {
            id: 5,
            text: 'Ofrecemos integraciones con APIs REST, webhooks, y conectores para plataformas populares como Slack, Teams, y WhatsApp.',
            sender: 'bot',
            timestamp: new Date(Date.now() - 60000).toISOString()
          }
        ]
        console.log('📝 Usando mensajes de ejemplo')
      }
    } catch (err) {
      console.error('❌ Error cargando mensajes:', err)
      error.value = 'Error al cargar mensajes'
      currentMessages.value = [
        {
          id: 1,
          text: 'Lo siento, hay un problema técnico. Por favor, intenta más tarde.',
          sender: 'bot',
          timestamp: new Date().toISOString()
        }
      ]
    } finally {
      isLoading.value = false
    }
  }

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return

    try {
      // Agregar mensaje del usuario inmediatamente
      const userMessage = {
        id: Date.now(),
        text: messageText.trim(),
        sender: 'user',
        timestamp: new Date().toISOString()
      }

      currentMessages.value.push(userMessage)
      console.log('📤 Mensaje enviado:', messageText)

      // Simular delay de respuesta
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Enviar al backend
      const response = await axios.post('/api/chat/send', {
        message: messageText,
        conversationId: currentConversationId.value || conversations.value[0]?.id
      })

      if (response.data.success) {
        // Agregar respuesta del bot
        const botMessage = {
          id: Date.now() + 1,
          text: response.data.reply,
          sender: 'bot',
          timestamp: new Date().toISOString()
        }

        currentMessages.value.push(botMessage)
        console.log('🤖 Respuesta recibida:', response.data.reply)
      } else {
        throw new Error('Error en la respuesta del servidor')
      }
    } catch (err) {
      console.error('❌ Error enviando mensaje:', err)

      // Respuesta de fallback inteligente
      const responses = [
        'Gracias por tu mensaje. Estoy procesando tu consulta...',
        'Entiendo tu pregunta. Permíteme ayudarte con eso.',
        'Es una excelente pregunta. Te puedo proporcionar más información al respecto.',
        'Perfecto, puedo asistirte con eso. ¿Hay algo específico que te gustaría saber?',
        'Me complace poder ayudarte. ¿Podrías darme más detalles sobre lo que necesitas?'
      ]

      const randomResponse = responses[Math.floor(Math.random() * responses.length)]

      const botMessage = {
        id: Date.now() + 1,
        text: randomResponse,
        sender: 'bot',
        timestamp: new Date().toISOString()
      }

      currentMessages.value.push(botMessage)
    }
  }

  const createNewConversation = async (title = 'Nueva conversación') => {
    try {
      const response = await axios.post('/api/conversations', { title })

      if (response.data.success) {
        const newConversation = response.data.conversation
        conversations.value.unshift(newConversation)
        console.log('✅ Nueva conversación creada:', title)
        return newConversation
      }
    } catch (err) {
      console.error('❌ Error creando conversación:', err)

      // Crear conversación local
      const newConversation = {
        id: Date.now(),
        title,
        user: 'Usuario',
        lastMessage: '',
        updatedAt: new Date().toISOString(),
        status: 'active'
      }

      conversations.value.unshift(newConversation)
      console.log('📝 Conversación creada localmente:', title)
      return newConversation
    }
  }

  const deleteConversation = async (conversationId) => {
    try {
      await axios.delete(`/api/conversations/${conversationId}`)
      conversations.value = conversations.value.filter(conv => conv.id !== conversationId)
      
      if (currentConversationId.value === conversationId) {
        currentConversationId.value = null
        currentMessages.value = []
      }
      
      console.log('🗑️ Conversación eliminada:', conversationId)
    } catch (err) {
      console.error('❌ Error eliminando conversación:', err)
      error.value = 'Error al eliminar conversación'
    }
  }

  const clearCurrentMessages = () => {
    currentMessages.value = []
    currentConversationId.value = null
    console.log('🧹 Mensajes actuales limpiados')
  }

  const markAsRead = async (conversationId) => {
    try {
      await axios.patch(`/api/conversations/${conversationId}/read`)
      
      const conversation = conversations.value.find(conv => conv.id === conversationId)
      if (conversation) {
        conversation.unread = false
      }
    } catch (err) {
      console.error('❌ Error marcando como leído:', err)
    }
  }

  const searchConversations = (query) => {
    if (!query.trim()) return conversations.value
    
    return conversations.value.filter(conv => 
      conv.title.toLowerCase().includes(query.toLowerCase()) ||
      conv.user.toLowerCase().includes(query.toLowerCase()) ||
      conv.lastMessage.toLowerCase().includes(query.toLowerCase())
    )
  }

  return {
    // State
    conversations,
    currentMessages,
    isLoading,
    error,
    currentConversationId,

    // Getters
    hasConversations,
    totalMessages,
    isConnected,

    // Actions
    loadConversations,
    loadConversation,
    sendMessage,
    createNewConversation,
    deleteConversation,
    clearCurrentMessages,
    markAsRead,
    searchConversations
  }
})