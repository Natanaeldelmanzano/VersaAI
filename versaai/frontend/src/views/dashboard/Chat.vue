<template>
  <div class="chat-interface">
    <!-- Header -->
    <div class="chat-header">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-semibold text-gray-900">VersaAI Chat</h1>
              <p class="text-sm text-gray-500">{{ currentChatbot?.name || 'Asistente General' }}</p>
            </div>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <!-- Model Selector -->
          <select 
            v-model="selectedModel" 
            class="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="gpt-4">GPT-4</option>
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="claude-3">Claude 3</option>
            <option value="gemini-pro">Gemini Pro</option>
          </select>
          
          <!-- New Chat Button -->
          <button 
            @click="startNewChat"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Nuevo Chat</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Chat Container -->
    <div class="chat-container">
      <!-- Sidebar -->
      <div class="chat-sidebar" :class="{ 'hidden': !showSidebar }">
        <div class="sidebar-header">
          <h3 class="text-lg font-medium text-gray-900">Conversaciones</h3>
          <button 
            @click="toggleSidebar"
            class="lg:hidden text-gray-500 hover:text-gray-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Conversation List -->
        <div class="conversation-list">
          <div 
            v-for="conversation in conversations" 
            :key="conversation.id"
            @click="loadConversation(conversation.id)"
            class="conversation-item"
            :class="{ 'active': currentConversation?.id === conversation.id }"
          >
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ conversation.title || 'Nueva conversación' }}
              </p>
              <p class="text-xs text-gray-500 truncate">
                {{ conversation.last_message || 'Sin mensajes' }}
              </p>
            </div>
            <div class="flex flex-col items-end space-y-1">
              <span class="text-xs text-gray-400">
                {{ formatRelativeTime(conversation.updated_at) }}
              </span>
              <div v-if="conversation.unread_count" class="w-2 h-2 bg-blue-500 rounded-full"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Chat Area -->
      <div class="chat-main">
        <!-- Messages Area -->
        <div class="messages-container" ref="messagesContainer">
          <!-- Welcome Message -->
          <div v-if="!currentConversation || messages.length === 0" class="welcome-message">
            <div class="text-center">
              <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-gray-900 mb-2">¡Hola! Soy VersaAI</h2>
              <p class="text-gray-600 mb-6">Tu asistente de inteligencia artificial. ¿En qué puedo ayudarte hoy?</p>
              
              <!-- Quick Actions -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                <button 
                  v-for="suggestion in quickSuggestions" 
                  :key="suggestion.id"
                  @click="sendMessage(suggestion.text)"
                  class="p-4 text-left border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <component :is="suggestion.icon" class="w-4 h-4 text-blue-600" />
                    </div>
                    <div>
                      <p class="font-medium text-gray-900">{{ suggestion.title }}</p>
                      <p class="text-sm text-gray-500">{{ suggestion.description }}</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>
          </div>

          <!-- Messages -->
          <div v-else class="messages-list">
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="message-wrapper"
              :class="message.message_type === 'user' ? 'user-message' : 'bot-message'"
            >
              <div class="message-content">
                <div class="message-avatar">
                  <div v-if="message.message_type === 'user'" class="user-avatar">
                    {{ userInitials }}
                  </div>
                  <div v-else class="bot-avatar">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                
                <div class="message-bubble">
                  <div class="message-text" v-html="formatMessage(message.content)"></div>
                  <div class="message-time">
                    {{ formatTime(message.timestamp) }}
                    <span v-if="message.message_type === 'user' && message.status" class="message-status">
                      <svg v-if="message.status === 'sent'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                      <svg v-else-if="message.status === 'delivered'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Typing Indicator -->
            <div v-if="isTyping" class="message-wrapper bot-message">
              <div class="message-content">
                <div class="message-avatar">
                  <div class="bot-avatar">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div class="message-bubble">
                  <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <div class="input-container">
            <!-- File Upload -->
            <button 
              @click="$refs.fileInput.click()"
              class="input-action-btn"
              title="Adjuntar archivo"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
            </button>
            
            <!-- Text Input -->
            <div class="flex-1 relative">
              <textarea
                ref="messageInput"
                v-model="newMessage"
                @keydown="handleKeyDown"
                @input="adjustTextareaHeight"
                placeholder="Escribe tu mensaje aquí..."
                class="message-input"
                rows="1"
                :disabled="isLoading"
              ></textarea>
              
              <!-- Character Count -->
              <div v-if="newMessage.length > 0" class="character-count">
                {{ newMessage.length }}/4000
              </div>
            </div>
            
            <!-- Send Button -->
            <button 
              @click="sendMessage()"
              :disabled="!canSend"
              class="send-btn"
              :class="{ 'sending': isLoading }"
            >
              <svg v-if="!isLoading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </button>
          </div>
          
          <!-- File Input -->
          <input 
            ref="fileInput"
            type="file"
            multiple
            accept=".txt,.pdf,.doc,.docx,.md"
            @change="handleFileUpload"
            class="hidden"
          />
          
          <!-- Uploaded Files -->
          <div v-if="uploadedFiles.length > 0" class="uploaded-files">
            <div 
              v-for="file in uploadedFiles" 
              :key="file.id"
              class="uploaded-file"
            >
              <div class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="text-sm text-gray-700">{{ file.name }}</span>
                <button 
                  @click="removeFile(file.id)"
                  class="text-red-500 hover:text-red-700"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mobile Sidebar Toggle -->
    <button 
      v-if="!showSidebar"
      @click="toggleSidebar"
      class="lg:hidden fixed bottom-4 left-4 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useConversationsStore } from '@/stores/conversations'
import { useAuthStore } from '@/stores/auth'

// Stores
const conversationsStore = useConversationsStore()
const authStore = useAuthStore()
const router = useRouter()
const toast = useToast()

// Refs
const messagesContainer = ref(null)
const messageInput = ref(null)
const fileInput = ref(null)

// State
const showSidebar = ref(true)
const newMessage = ref('')
const selectedModel = ref('gpt-4')
const uploadedFiles = ref([])
const isTyping = ref(false)

// Computed properties from store
const conversations = computed(() => conversationsStore.conversations)
const currentConversation = computed(() => conversationsStore.currentConversation)
const messages = computed(() => conversationsStore.messages)
const isLoading = computed(() => conversationsStore.isLoading)

const quickSuggestions = ref([
  {
    id: 1,
    title: 'Explicar un concepto',
    description: 'Obtén explicaciones claras y detalladas',
    text: 'Explícame qué es la inteligencia artificial',
    icon: 'AcademicCapIcon'
  },
  {
    id: 2,
    title: 'Generar código',
    description: 'Crea código en cualquier lenguaje',
    text: 'Genera un ejemplo de API REST en Python',
    icon: 'CodeIcon'
  },
  {
    id: 3,
    title: 'Analizar documento',
    description: 'Sube un archivo para análisis',
    text: 'Ayúdame a analizar este documento',
    icon: 'DocumentTextIcon'
  },
  {
    id: 4,
    title: 'Resolver problema',
    description: 'Encuentra soluciones paso a paso',
    text: 'Ayúdame a resolver este problema',
    icon: 'LightBulbIcon'
  }
])

// Computed
const canSend = computed(() => {
  return (newMessage.value.trim().length > 0 || uploadedFiles.value.length > 0) && !isLoading.value
})

const userInitials = computed(() => {
  const user = authStore.user
  if (user?.name) {
    return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }
  return 'U'
})

// Methods
const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}

const startNewChat = async () => {
  try {
    // Create a new conversation
    const result = await conversationsStore.createConversation({
      title: 'Nueva conversación',
      chatbot_id: 1 // Default chatbot ID, you might want to make this configurable
    })
    
    if (result.success) {
      newMessage.value = ''
      uploadedFiles.value = []
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('Error creating new chat:', error)
    toast.error('Error al crear nueva conversación')
  }
}

const loadConversation = async (conversationId) => {
  try {
    await conversationsStore.fetchConversation(conversationId)
    await conversationsStore.fetchMessages(conversationId)
    
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Error loading conversation:', error)
    toast.error('Error al cargar la conversación')
  }
}

const sendMessage = async (messageText = null) => {
  const content = messageText || newMessage.value.trim()
  
  if (!content && uploadedFiles.value.length === 0) return
  
  try {
    // If no current conversation, create one first
    if (!currentConversation.value) {
      await startNewChat()
      if (!currentConversation.value) {
        toast.error('Error al crear la conversación')
        return
      }
    }
    
    isTyping.value = true
    
    // Send message through store
    const result = await conversationsStore.sendMessage(currentConversation.value.id, {
      message: content,
      chatbot_id: currentConversation.value.chatbot_id || 1
    })
    
    if (result.success) {
      newMessage.value = ''
      uploadedFiles.value = []
      
      await nextTick()
      scrollToBottom()
    } else {
      toast.error(result.error || 'Error al enviar el mensaje')
    }
    
  } catch (error) {
    console.error('Error sending message:', error)
    toast.error('Error al enviar el mensaje')
  } finally {
    isTyping.value = false
  }
}



const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const adjustTextareaHeight = () => {
  const textarea = messageInput.value
  if (textarea) {
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }
}

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files)
  
  files.forEach(file => {
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      toast.error(`El archivo ${file.name} es demasiado grande (máximo 10MB)`)
      return
    }
    
    uploadedFiles.value.push({
      id: Date.now() + Math.random(),
      name: file.name,
      size: file.size,
      file: file
    })
  })
  
  // Clear input
  event.target.value = ''
}

const removeFile = (fileId) => {
  uploadedFiles.value = uploadedFiles.value.filter(f => f.id !== fileId)
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatMessage = (content) => {
  // Simple markdown-like formatting
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRelativeTime = (timestamp) => {
  const now = new Date()
  const date = new Date(timestamp)
  const diffInMinutes = Math.floor((now - date) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Ahora'
  if (diffInMinutes < 60) return `${diffInMinutes}m`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h`
  return `${Math.floor(diffInMinutes / 1440)}d`
}

// Watchers
watch(showSidebar, (newValue) => {
  if (window.innerWidth < 1024) {
    document.body.style.overflow = newValue ? 'hidden' : 'auto'
  }
})

// Lifecycle
onMounted(async () => {
  // Load conversations from backend
  try {
    await conversationsStore.fetchConversations()
  } catch (error) {
    console.error('Error loading conversations:', error)
    toast.error('Error al cargar las conversaciones')
  }
  
  // Auto-focus input
  if (messageInput.value) {
    messageInput.value.focus()
  }
  
  // Handle responsive sidebar
  const handleResize = () => {
    if (window.innerWidth >= 1024) {
      showSidebar.value = true
      document.body.style.overflow = 'auto'
    } else {
      showSidebar.value = false
    }
  }
  
  window.addEventListener('resize', handleResize)
  handleResize()
  
  // Cleanup
  return () => {
    window.removeEventListener('resize', handleResize)
    document.body.style.overflow = 'auto'
  }
})
</script>

<style scoped>
.chat-interface {
  @apply h-screen flex flex-col bg-gray-50;
}

.chat-header {
  @apply bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0;
}

.chat-container {
  @apply flex-1 flex overflow-hidden;
}

.chat-sidebar {
  @apply w-80 bg-white border-r border-gray-200 flex flex-col;
}

@media (max-width: 1023px) {
  .chat-sidebar {
    @apply fixed inset-y-0 left-0 z-40 w-80 transform transition-transform duration-300 ease-in-out;
  }
  
  .chat-sidebar.hidden {
    @apply -translate-x-full;
  }
}

.sidebar-header {
  @apply p-4 border-b border-gray-200 flex items-center justify-between;
}

.conversation-list {
  @apply flex-1 overflow-y-auto p-2 space-y-1;
}

.conversation-item {
  @apply p-3 rounded-lg cursor-pointer transition-colors hover:bg-gray-50 flex items-center space-x-3;
}

.conversation-item.active {
  @apply bg-blue-50 border border-blue-200;
}

.chat-main {
  @apply flex-1 flex flex-col;
}

.messages-container {
  @apply flex-1 overflow-y-auto;
}

.welcome-message {
  @apply flex items-center justify-center h-full p-8;
}

.messages-list {
  @apply p-6 space-y-6;
}

.message-wrapper {
  @apply flex;
}

.message-wrapper.user-message {
  @apply justify-end;
}

.message-wrapper.bot-message {
  @apply justify-start;
}

.message-content {
  @apply flex items-end space-x-3 max-w-3xl;
}

.user-message .message-content {
  @apply flex-row-reverse space-x-reverse;
}

.message-avatar {
  @apply flex-shrink-0;
}

.user-avatar {
  @apply w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium;
}

.bot-avatar {
  @apply w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center;
}

.message-bubble {
  @apply max-w-md;
}

.user-message .message-bubble {
  @apply bg-blue-600 text-white rounded-2xl rounded-br-md px-4 py-3;
}

.bot-message .message-bubble {
  @apply bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm;
}

.message-text {
  @apply text-sm leading-relaxed;
}

.message-time {
  @apply text-xs opacity-70 mt-1 flex items-center space-x-1;
}

.message-status {
  @apply flex items-center;
}

.typing-indicator {
  @apply flex space-x-1 py-2;
}

.typing-dot {
  @apply w-2 h-2 bg-gray-400 rounded-full animate-pulse;
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

.input-area {
  @apply bg-white border-t border-gray-200 p-4 flex-shrink-0;
}

.input-container {
  @apply flex items-end space-x-3 max-w-4xl mx-auto;
}

.input-action-btn {
  @apply p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors;
}

.message-input {
  @apply w-full resize-none border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm leading-relaxed;
  min-height: 44px;
  max-height: 120px;
}

.character-count {
  @apply absolute bottom-2 right-2 text-xs text-gray-400;
}

.send-btn {
  @apply bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors;
}

.send-btn.sending {
  @apply bg-blue-700;
}

.uploaded-files {
  @apply mt-3 flex flex-wrap gap-2;
}

.uploaded-file {
  @apply bg-gray-100 rounded-lg px-3 py-2 text-sm;
}

/* Scrollbar styling */
.messages-container::-webkit-scrollbar,
.conversation-list::-webkit-scrollbar {
  @apply w-2;
}

.messages-container::-webkit-scrollbar-track,
.conversation-list::-webkit-scrollbar-track {
  @apply bg-gray-100;
}

.messages-container::-webkit-scrollbar-thumb,
.conversation-list::-webkit-scrollbar-thumb {
  @apply bg-gray-300 rounded-full;
}

.messages-container::-webkit-scrollbar-thumb:hover,
.conversation-list::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400;
}
</style>