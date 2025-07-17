// VersaAI Conversations Composable
import { ref, computed, reactive, nextTick } from 'vue'
import { api } from '@/config/api'
import { useToast } from 'vue-toastification'

// Global state
const conversations = ref([])
const currentConversation = ref(null)
const messages = ref([])
const isLoading = ref(false)
const isSending = ref(false)
const isTyping = ref(false)

// Chat state
const chatState = reactive({
  isConnected: false,
  lastActivity: null,
  unreadCount: 0
})

export function useConversations() {
  const toast = useToast()

  // Computed properties
  const sortedConversations = computed(() => {
    return [...conversations.value].sort((a, b) => 
      new Date(b.updated_at) - new Date(a.updated_at)
    )
  })

  const activeConversations = computed(() => 
    conversations.value.filter(conv => conv.status === 'active')
  )

  const archivedConversations = computed(() => 
    conversations.value.filter(conv => conv.status === 'archived')
  )

  const currentMessages = computed(() => 
    messages.value.filter(msg => msg.conversation_id === currentConversation.value?.id)
  )

  // Load conversations for a chatbot
  const loadConversations = async (chatbotId) => {
    try {
      isLoading.value = true
      const response = await api.conversations.list(chatbotId)
      conversations.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Load conversations error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las conversaciones'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Get conversation by ID
  const getConversation = async (id) => {
    try {
      isLoading.value = true
      const response = await api.conversations.get(id)
      currentConversation.value = response.data
      
      // Load messages for this conversation
      if (response.data.messages) {
        messages.value = response.data.messages
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get conversation error:', error)
      const message = error.response?.data?.detail || 'Error al cargar la conversación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Create new conversation
  const createConversation = async (conversationData) => {
    try {
      isLoading.value = true
      const response = await api.conversations.create(conversationData)
      conversations.value.unshift(response.data)
      currentConversation.value = response.data
      messages.value = []
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

  // Send message
  const sendMessage = async (content, conversationId = null) => {
    try {
      isSending.value = true
      
      const targetConversationId = conversationId || currentConversation.value?.id
      if (!targetConversationId) {
        throw new Error('No hay conversación activa')
      }

      // Add user message immediately to UI
      const userMessage = {
        id: `temp-${Date.now()}`,
        content,
        role: 'user',
        conversation_id: targetConversationId,
        created_at: new Date().toISOString(),
        is_temporary: true
      }
      messages.value.push(userMessage)
      
      // Scroll to bottom
      await nextTick()
      scrollToBottom()
      
      // Show typing indicator
      isTyping.value = true
      
      // Send to API
      const response = await api.conversations.sendMessage(targetConversationId, content)
      
      // Remove temporary message
      messages.value = messages.value.filter(msg => msg.id !== userMessage.id)
      
      // Add real messages from response
      if (response.data.messages) {
        messages.value.push(...response.data.messages)
      } else if (response.data.user_message && response.data.bot_response) {
        messages.value.push(response.data.user_message, response.data.bot_response)
      }
      
      // Update conversation timestamp
      const convIndex = conversations.value.findIndex(conv => conv.id === targetConversationId)
      if (convIndex !== -1) {
        conversations.value[convIndex].updated_at = new Date().toISOString()
        conversations.value[convIndex].last_message = content
      }
      
      // Scroll to bottom again
      await nextTick()
      scrollToBottom()
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Send message error:', error)
      
      // Remove temporary message on error
      messages.value = messages.value.filter(msg => !msg.is_temporary)
      
      const message = error.response?.data?.detail || 'Error al enviar el mensaje'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSending.value = false
      isTyping.value = false
    }
  }

  // Archive conversation
  const archiveConversation = async (id) => {
    try {
      const convIndex = conversations.value.findIndex(conv => conv.id === id)
      if (convIndex !== -1) {
        conversations.value[convIndex].status = 'archived'
        toast.success('Conversación archivada')
      }
      return { success: true }
    } catch (error) {
      console.error('Archive conversation error:', error)
      toast.error('Error al archivar la conversación')
      return { success: false, error: error.message }
    }
  }

  // Restore conversation
  const restoreConversation = async (id) => {
    try {
      const convIndex = conversations.value.findIndex(conv => conv.id === id)
      if (convIndex !== -1) {
        conversations.value[convIndex].status = 'active'
        toast.success('Conversación restaurada')
      }
      return { success: true }
    } catch (error) {
      console.error('Restore conversation error:', error)
      toast.error('Error al restaurar la conversación')
      return { success: false, error: error.message }
    }
  }

  // Delete conversation
  const deleteConversation = async (id) => {
    try {
      conversations.value = conversations.value.filter(conv => conv.id !== id)
      
      if (currentConversation.value?.id === id) {
        currentConversation.value = null
        messages.value = []
      }
      
      toast.success('Conversación eliminada')
      return { success: true }
    } catch (error) {
      console.error('Delete conversation error:', error)
      toast.error('Error al eliminar la conversación')
      return { success: false, error: error.message }
    }
  }

  // Set current conversation
  const setCurrentConversation = async (conversation) => {
    currentConversation.value = conversation
    
    if (conversation) {
      // Load messages if not already loaded
      if (!conversation.messages) {
        await getConversation(conversation.id)
      } else {
        messages.value = conversation.messages
      }
      
      // Mark as read
      markAsRead(conversation.id)
      
      // Scroll to bottom
      await nextTick()
      scrollToBottom()
    } else {
      messages.value = []
    }
  }

  // Mark conversation as read
  const markAsRead = (conversationId) => {
    const convIndex = conversations.value.findIndex(conv => conv.id === conversationId)
    if (convIndex !== -1) {
      conversations.value[convIndex].unread_count = 0
    }
    
    // Update global unread count
    chatState.unreadCount = conversations.value.reduce((total, conv) => 
      total + (conv.unread_count || 0), 0
    )
  }

  // Search conversations
  const searchConversations = (query) => {
    if (!query.trim()) {
      return conversations.value
    }
    
    const searchTerm = query.toLowerCase()
    return conversations.value.filter(conv => 
      conv.title?.toLowerCase().includes(searchTerm) ||
      conv.last_message?.toLowerCase().includes(searchTerm) ||
      conv.user_name?.toLowerCase().includes(searchTerm)
    )
  }

  // Export conversation
  const exportConversation = async (id, format = 'json') => {
    try {
      const conversation = conversations.value.find(conv => conv.id === id)
      if (!conversation) {
        throw new Error('Conversación no encontrada')
      }
      
      const conversationMessages = messages.value.filter(msg => msg.conversation_id === id)
      
      let content, filename, mimeType
      
      if (format === 'json') {
        content = JSON.stringify({
          conversation,
          messages: conversationMessages,
          exported_at: new Date().toISOString()
        }, null, 2)
        filename = `conversation_${id}.json`
        mimeType = 'application/json'
      } else if (format === 'txt') {
        content = conversationMessages.map(msg => 
          `[${new Date(msg.created_at).toLocaleString()}] ${msg.role.toUpperCase()}: ${msg.content}`
        ).join('\n\n')
        filename = `conversation_${id}.txt`
        mimeType = 'text/plain'
      }
      
      // Create and download file
      const blob = new Blob([content], { type: mimeType })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      toast.success('Conversación exportada exitosamente')
      return { success: true }
    } catch (error) {
      console.error('Export conversation error:', error)
      const message = error.message || 'Error al exportar la conversación'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Scroll to bottom of chat
  const scrollToBottom = () => {
    const chatContainer = document.querySelector('.chat-messages')
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight
    }
  }

  // Clear current conversation
  const clearCurrentConversation = () => {
    currentConversation.value = null
    messages.value = []
  }

  // Update chat state
  const updateChatState = (newState) => {
    Object.assign(chatState, newState)
  }

  return {
    // State
    conversations: computed(() => conversations.value),
    currentConversation: computed(() => currentConversation.value),
    messages: computed(() => messages.value),
    isLoading: computed(() => isLoading.value),
    isSending: computed(() => isSending.value),
    isTyping: computed(() => isTyping.value),
    chatState: computed(() => chatState),
    
    // Computed
    sortedConversations,
    activeConversations,
    archivedConversations,
    currentMessages,
    
    // Methods
    loadConversations,
    getConversation,
    createConversation,
    sendMessage,
    archiveConversation,
    restoreConversation,
    deleteConversation,
    setCurrentConversation,
    markAsRead,
    searchConversations,
    exportConversation,
    scrollToBottom,
    clearCurrentConversation,
    updateChatState
  }
}

// Export for global access
export { conversations, currentConversation, messages, isLoading, isSending, isTyping, chatState }