import { ref, reactive, computed, nextTick } from 'vue'
import { conversationsAPI } from '@/services/api'

// Global state
const conversations = ref([])
const currentConversation = ref(null)
const messages = ref([])
const loading = ref(false)
const error = ref(null)
const typing = ref(false)
const connected = ref(false)

export function useChat() {
  // Reactive chat state
  const chatState = reactive({
    isMinimized: false,
    isFullscreen: false,
    selectedChatbot: null,
    userInput: '',
    attachments: [],
    quickReplies: [],
    suggestions: []
  })

  // WebSocket connection
  let websocket = null
  const wsUrl = computed(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    return `${protocol}//${host}/ws/chat`
  })

  // Computed properties
  const sortedMessages = computed(() => {
    return [...messages.value].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
  })

  const lastMessage = computed(() => {
    return sortedMessages.value[sortedMessages.value.length - 1]
  })

  const messageCount = computed(() => {
    return messages.value.length
  })

  const hasActiveConversation = computed(() => {
    return currentConversation.value !== null
  })

  const canSendMessage = computed(() => {
    return chatState.userInput.trim().length > 0 && !typing.value && connected.value
  })

  // Methods
  const loadConversations = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await conversationsAPI.getConversations()
      
      if (response.data) {
        conversations.value = response.data
      }
    } catch (err) {
      console.warn('Failed to load conversations from API, using fallback:', err)
      error.value = 'Error al cargar las conversaciones'
      
      // Fallback to sample data
      conversations.value = generateSampleConversations()
    } finally {
      loading.value = false
    }
  }

  const loadMessages = async (conversationId) => {
    loading.value = true
    error.value = null

    try {
      const response = await conversationsAPI.getMessages(conversationId)
      
      if (response.data) {
        messages.value = response.data
      }
    } catch (err) {
      console.warn('Failed to load messages from API, using fallback:', err)
      error.value = 'Error al cargar los mensajes'
      
      // Fallback to sample data
      messages.value = generateSampleMessages(conversationId)
    } finally {
      loading.value = false
    }
  }

  const createConversation = async (chatbotId, title = 'Nueva conversación') => {
    try {
      const response = await conversationsAPI.createConversation({
        chatbot_id: chatbotId,
        title: title,
        status: 'active'
      })
      
      if (response.data) {
        const newConversation = response.data
        conversations.value.unshift(newConversation)
        currentConversation.value = newConversation
        messages.value = []
        
        return newConversation
      }
    } catch (err) {
      console.error('Error creating conversation:', err)
      error.value = 'Error al crear la conversación'
      
      // Fallback: create local conversation
      const fallbackConversation = {
        id: Date.now(),
        chatbot_id: chatbotId,
        title: title,
        status: 'active',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        message_count: 0
      }
      
      conversations.value.unshift(fallbackConversation)
      currentConversation.value = fallbackConversation
      messages.value = []
      
      return fallbackConversation
    }
  }

  const sendMessage = async (content, type = 'text') => {
    if (!canSendMessage.value && type === 'text') {
      return
    }

    const tempMessage = {
      id: `temp-${Date.now()}`,
      content: content,
      type: type,
      sender: 'user',
      timestamp: new Date().toISOString(),
      status: 'sending'
    }

    // Add user message immediately
    messages.value.push(tempMessage)
    chatState.userInput = ''
    
    // Scroll to bottom
    await nextTick()
    scrollToBottom()

    try {
      // Send via WebSocket if connected, otherwise use API
      if (websocket && connected.value) {
        websocket.send(JSON.stringify({
          type: 'message',
          conversation_id: currentConversation.value?.id,
          content: content,
          message_type: type
        }))
      } else {
        // Fallback to API
        const response = await conversationsAPI.sendMessage(currentConversation.value?.id, {
          content: content,
          type: type
        })
        
        if (response.data) {
          // Update temp message with real data
          const messageIndex = messages.value.findIndex(m => m.id === tempMessage.id)
          if (messageIndex !== -1) {
            messages.value[messageIndex] = { ...response.data.user_message, status: 'sent' }
          }
          
          // Add bot response
          if (response.data.bot_response) {
            messages.value.push(response.data.bot_response)
          }
        }
      }
    } catch (err) {
      console.error('Error sending message:', err)
      
      // Update message status to failed
      const messageIndex = messages.value.findIndex(m => m.id === tempMessage.id)
      if (messageIndex !== -1) {
        messages.value[messageIndex].status = 'failed'
      }
      
      // Generate fallback bot response
      setTimeout(() => {
        const botResponse = {
          id: Date.now(),
          content: 'Lo siento, no pude procesar tu mensaje en este momento. Por favor, inténtalo de nuevo.',
          type: 'text',
          sender: 'bot',
          timestamp: new Date().toISOString(),
          status: 'delivered'
        }
        messages.value.push(botResponse)
        scrollToBottom()
      }, 1000)
    }
  }

  const retryMessage = async (messageId) => {
    const message = messages.value.find(m => m.id === messageId)
    if (message && message.status === 'failed') {
      message.status = 'sending'
      await sendMessage(message.content, message.type)
    }
  }

  const deleteMessage = async (messageId) => {
    try {
      await apiService.conversations.deleteMessage(messageId)
      messages.value = messages.value.filter(m => m.id !== messageId)
    } catch (err) {
      console.error('Error deleting message:', err)
      error.value = 'Error al eliminar el mensaje'
    }
  }

  const clearConversation = async () => {
    if (currentConversation.value) {
      try {
        await apiService.conversations.clear(currentConversation.value.id)
        messages.value = []
      } catch (err) {
        console.error('Error clearing conversation:', err)
        error.value = 'Error al limpiar la conversación'
      }
    }
  }

  const deleteConversation = async (conversationId) => {
    try {
      await apiService.conversations.delete(conversationId)
      conversations.value = conversations.value.filter(c => c.id !== conversationId)
      
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = null
        messages.value = []
      }
    } catch (err) {
      console.error('Error deleting conversation:', err)
      error.value = 'Error al eliminar la conversación'
    }
  }

  const selectConversation = async (conversation) => {
    currentConversation.value = conversation
    await loadMessages(conversation.id)
    
    // Connect to WebSocket for this conversation
    connectWebSocket(conversation.id)
  }

  const connectWebSocket = (conversationId) => {
    if (websocket) {
      websocket.close()
    }

    try {
      websocket = new WebSocket(`${wsUrl.value}/${conversationId}`)
      
      websocket.onopen = () => {
        connected.value = true
        console.log('WebSocket connected')
      }
      
      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        
        switch (data.type) {
          case 'message':
            messages.value.push(data.message)
            scrollToBottom()
            break
          case 'typing':
            typing.value = data.typing
            break
          case 'error':
            error.value = data.message
            break
        }
      }
      
      websocket.onclose = () => {
        connected.value = false
        console.log('WebSocket disconnected')
      }
      
      websocket.onerror = (error) => {
        console.error('WebSocket error:', error)
        connected.value = false
      }
    } catch (err) {
      console.error('Failed to connect WebSocket:', err)
      connected.value = false
    }
  }

  const disconnectWebSocket = () => {
    if (websocket) {
      websocket.close()
      websocket = null
    }
    connected.value = false
  }

  const scrollToBottom = () => {
    nextTick(() => {
      const chatContainer = document.querySelector('.chat-messages')
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight
      }
    })
  }

  const addQuickReply = (reply) => {
    chatState.quickReplies.push(reply)
  }

  const removeQuickReply = (index) => {
    chatState.quickReplies.splice(index, 1)
  }

  const addAttachment = (file) => {
    const attachment = {
      id: Date.now(),
      file: file,
      name: file.name,
      size: file.size,
      type: file.type,
      url: URL.createObjectURL(file)
    }
    chatState.attachments.push(attachment)
    return attachment
  }

  const removeAttachment = (attachmentId) => {
    const index = chatState.attachments.findIndex(a => a.id === attachmentId)
    if (index !== -1) {
      const attachment = chatState.attachments[index]
      URL.revokeObjectURL(attachment.url)
      chatState.attachments.splice(index, 1)
    }
  }

  // Sample data generators
  const generateSampleConversations = () => {
    return [
      {
        id: 1,
        title: 'Consulta sobre productos',
        chatbot_id: 1,
        status: 'active',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        updated_at: new Date(Date.now() - 3600000).toISOString(),
        message_count: 8
      },
      {
        id: 2,
        title: 'Soporte técnico',
        chatbot_id: 2,
        status: 'active',
        created_at: new Date(Date.now() - 172800000).toISOString(),
        updated_at: new Date(Date.now() - 7200000).toISOString(),
        message_count: 12
      }
    ]
  }

  const generateSampleMessages = (conversationId) => {
    return [
      {
        id: 1,
        content: '¡Hola! ¿En qué puedo ayudarte hoy?',
        type: 'text',
        sender: 'bot',
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        status: 'delivered'
      },
      {
        id: 2,
        content: 'Hola, necesito información sobre sus productos',
        type: 'text',
        sender: 'user',
        timestamp: new Date(Date.now() - 3500000).toISOString(),
        status: 'delivered'
      },
      {
        id: 3,
        content: 'Por supuesto, estaré encantado de ayudarte. ¿Qué tipo de producto te interesa?',
        type: 'text',
        sender: 'bot',
        timestamp: new Date(Date.now() - 3400000).toISOString(),
        status: 'delivered'
      }
    ]
  }

  // Utility functions
  const formatMessageTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    } else {
      return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })
    }
  }

  const getMessageStatusIcon = (status) => {
    switch (status) {
      case 'sending': return '⏳'
      case 'sent': return '✓'
      case 'delivered': return '✓✓'
      case 'read': return '✓✓'
      case 'failed': return '❌'
      default: return ''
    }
  }

  const isImageFile = (file) => {
    return file.type.startsWith('image/')
  }

  const isDocumentFile = (file) => {
    const documentTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ]
    return documentTypes.includes(file.type)
  }

  return {
    // State
    conversations,
    currentConversation,
    messages,
    loading,
    error,
    typing,
    connected,
    chatState,
    
    // Computed
    sortedMessages,
    lastMessage,
    messageCount,
    hasActiveConversation,
    canSendMessage,
    
    // Methods
    loadConversations,
    loadMessages,
    createConversation,
    sendMessage,
    retryMessage,
    deleteMessage,
    clearConversation,
    deleteConversation,
    selectConversation,
    connectWebSocket,
    disconnectWebSocket,
    scrollToBottom,
    addQuickReply,
    removeQuickReply,
    addAttachment,
    removeAttachment,
    
    // Utilities
    formatMessageTime,
    getMessageStatusIcon,
    isImageFile,
    isDocumentFile
  }
}

// Export singleton instance
export const chatStore = useChat()