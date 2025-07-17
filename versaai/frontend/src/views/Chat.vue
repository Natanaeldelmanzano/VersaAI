<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900">Chat IA</h1>
          <p class="text-sm text-gray-600 mt-1">Asistente inteligente para consultas empresariales</p>
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-sm text-gray-600">En línea</span>
          </div>
          <button 
            @click="createNewConversation"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Nueva conversación
          </button>
        </div>
      </div>
    </div>

    <div class="flex h-[calc(100vh-80px)]">
      <!-- Sidebar - Historial de conversaciones -->
      <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div class="p-4 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">Conversaciones</h2>
        </div>
        
        <div class="flex-1 overflow-y-auto">
          <div class="p-2">
            <div 
              v-for="conversation in conversations" 
              :key="conversation.id"
              :class="[
                'p-3 rounded-lg cursor-pointer transition-colors mb-2',
                conversation.id === activeConversation ? 'bg-blue-50 border border-blue-200' : 'hover:bg-gray-50'
              ]"
              @click="setActiveConversation(conversation.id)"
            >
              <div class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ conversation.title }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ conversation.lastMessage }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ formatTime(conversation.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="flex-1">
        <ChatInterface 
          :chatbot-id="currentChatbotId"
          :conversation-id="activeConversation"
          @message-sent="handleMessageSent"
          @conversation-created="handleConversationCreated"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useConversationsStore } from '@/stores/conversations'
import { useToast } from 'vue-toastification'
import ChatInterface from '@/components/ChatInterface.vue'

// Components
const components = {
  ChatInterface
}

// Stores
const conversationsStore = useConversationsStore()
const toast = useToast()

// Reactive data
const activeConversation = ref(null)
const currentChatbotId = ref(1) // Default chatbot ID

// Computed
const conversations = computed(() => conversationsStore.conversations || [])

// Methods
const setActiveConversation = (conversationId) => {
  activeConversation.value = conversationId
}

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 60) {
    return `hace ${minutes} min`
  } else if (hours < 24) {
    return `hace ${hours}h`
  } else {
    return `hace ${days}d`
  }
}

const createNewConversation = () => {
  activeConversation.value = null
  conversationsStore.messages = []
  toast.info('Nueva conversación iniciada')
}

// Event handlers for ChatInterface component
const handleMessageSent = async (event) => {
  const { message, conversationId, chatbotId } = event
  
  try {
    // If no active conversation, create a new one
    if (!conversationId) {
      const conversationResult = await conversationsStore.createConversation({
        chatbot_id: chatbotId || currentChatbotId.value,
        title: message.substring(0, 50) + (message.length > 50 ? '...' : '')
      })
      
      if (conversationResult.success) {
        activeConversation.value = conversationResult.data.id
        // Refresh conversations list
        await conversationsStore.fetchConversations()
      } else {
        toast.error('Error al crear la conversación')
        return
      }
    }
    
    // Send message to API (optional, as ChatInterface handles this with Groq)
    const result = await conversationsStore.sendMessage(conversationId || activeConversation.value, {
      message: message,
      chatbot_id: chatbotId || currentChatbotId.value
    })
    
    if (result.success) {
      // Refresh conversations list to update last message
      await conversationsStore.fetchConversations()
    }
  } catch (error) {
    console.error('Error handling message:', error)
    toast.error('Error al procesar el mensaje')
  }
}

const handleConversationCreated = async (conversationData) => {
  try {
    const result = await conversationsStore.createConversation(conversationData)
    if (result.success) {
      activeConversation.value = result.data.id
      await conversationsStore.fetchConversations()
      toast.success('Nueva conversación creada')
    }
  } catch (error) {
    console.error('Error creating conversation:', error)
    toast.error('Error al crear la conversación')
  }
}

// Initialize
onMounted(async () => {
  try {
    console.log('🚀 Inicializando Chat...')
    
    // Fetch conversations with fallback data
    const result = await conversationsStore.fetchConversations()
    
    if (!result.success) {
      console.warn('⚠️ Error al cargar conversaciones, usando datos de fallback')
    }
    
    // Set first conversation as active if exists
    if (conversations.value.length > 0) {
      activeConversation.value = conversations.value[0].id
    } else {
      console.log('📝 No hay conversaciones, listo para crear una nueva')
    }
    
    console.log('✅ Chat inicializado correctamente')
  } catch (error) {
    console.error('❌ Error inicializando Chat:', error)
    toast.error('Error al cargar el chat')
  }
})
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>