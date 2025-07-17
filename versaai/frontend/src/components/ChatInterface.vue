<template>
  <div class="chat-container h-full flex flex-col">
    <!-- Header del Chat -->
    <div class="chat-header bg-blue-600 text-white p-4 flex justify-between items-center">
      <div>
        <h3 class="font-semibold">{{ currentChatbot.name }}</h3>
        <p class="text-sm opacity-80">{{ currentChatbot.status }}</p>
      </div>
      <div class="flex space-x-2">
        <button @click="clearChat" class="p-2 hover:bg-blue-700 rounded" title="Limpiar chat">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
        </button>
        <button @click="exportChat" class="p-2 hover:bg-blue-700 rounded" title="Exportar chat">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Área de Mensajes -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 chat-messages scrollable scroll-smooth">
      <!-- Scroll to top button -->
      <div v-if="messages.length > 5" class="sticky top-2 z-10 flex justify-end mb-2">
        <button 
          @click="scrollToTop"
          class="bg-white shadow-md hover:shadow-lg text-gray-600 hover:text-gray-800 p-2 rounded-full transition-all duration-200 hover:scale-105"
          title="Ir al inicio"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
          </svg>
        </button>
      </div>
      <div v-for="message in messages" :key="message.id" 
           :class="['flex', message.isUser ? 'justify-end' : 'justify-start']">
        <div :class="[
          'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
          message.isUser 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-200 text-gray-800'
        ]">
          <p class="whitespace-pre-wrap">{{ message.text }}</p>
          <span class="text-xs opacity-70 block mt-1">
            {{ formatTime(message.timestamp) }}
          </span>
        </div>
      </div>
      
      <!-- Indicador de escritura -->
      <div v-if="isTyping" class="flex justify-start">
        <div class="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg">
          <div class="flex space-x-1">
            <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
      </div>
      
      <!-- Scroll to bottom button -->
      <div v-if="messages.length > 0" class="sticky bottom-2 z-10 flex justify-end mt-2">
        <button 
          @click="scrollToBottom"
          class="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full shadow-md hover:shadow-lg transition-all duration-200 hover:scale-105"
          title="Ir al final"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Input de Mensaje -->
    <div class="chat-input border-t p-4">
      <div class="flex space-x-2">
        <textarea 
          v-model="newMessage" 
          @keypress.enter.prevent="handleEnterKey"
          :disabled="isTyping"
          placeholder="Escribe tu mensaje..."
          rows="1"
          class="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          style="min-height: 40px; max-height: 120px;"
        />
        <button 
          @click="sendMessage" 
          :disabled="!newMessage.trim() || isTyping"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
          </svg>
        </button>
      </div>
      <div class="text-xs text-gray-500 mt-1">
        {{ newMessage.length }}/1000 caracteres
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useGroqAPI } from '@/composables/useGroqAPI'

// Props
const props = defineProps({
  chatbotId: {
    type: [String, Number],
    default: null
  },
  conversationId: {
    type: [String, Number],
    default: null
  }
})

// Emits
const emit = defineEmits(['message-sent', 'conversation-created'])

// Reactive data
const messages = ref([])
const newMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref(null)
const { sendToGroq, generateChatbotResponse, loading, error } = useGroqAPI()

const currentChatbot = ref({
  name: 'Asistente IA',
  status: 'En línea',
  type: 'general'
})

// Methods
const sendMessage = async () => {
  if (!newMessage.value.trim() || isTyping.value) return
  
  // Agregar mensaje del usuario
  const userMessage = {
    id: Date.now(),
    text: newMessage.value.trim(),
    isUser: true,
    timestamp: new Date()
  }
  messages.value.push(userMessage)
  
  const messageToSend = newMessage.value.trim()
  newMessage.value = ''
  
  // Emit evento de mensaje enviado
  emit('message-sent', {
    message: messageToSend,
    conversationId: props.conversationId,
    chatbotId: props.chatbotId
  })
  
  // Scroll automático
  await nextTick()
  scrollToBottom()
  
  // Mostrar indicador de escritura
  isTyping.value = true
  
  try {
    // Enviar a Groq API con contexto del chatbot
    const response = await generateChatbotResponse(messageToSend, currentChatbot.value.type)
    
    // Agregar respuesta de la IA
    const aiMessage = {
      id: Date.now() + 1,
      text: response,
      isUser: false,
      timestamp: new Date()
    }
    messages.value.push(aiMessage)
    
    // Emit evento para respuesta exitosa
    emit('message-sent', {
      user: userMessage,
      assistant: aiMessage
    })
    
  } catch (error) {
    console.error('Error sending message:', error)
    // Respuesta de fallback
    const errorMessage = {
      id: Date.now() + 1,
      text: 'Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.',
      isUser: false,
      timestamp: new Date(),
      isError: true
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    await nextTick()
    scrollToBottom()
  }
}

const handleEnterKey = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  } else {
    // Allow line break with Shift+Enter
    return true
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const scrollToTop = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = 0
  }
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const clearChat = () => {
  if (confirm('¿Estás seguro de que quieres limpiar el chat?')) {
    messages.value = []
    // Agregar mensaje de bienvenida nuevamente
    addWelcomeMessage()
  }
}

const exportChat = () => {
  const chatData = messages.value.map(msg => ({
    sender: msg.isUser ? 'Usuario' : 'IA',
    message: msg.text,
    timestamp: msg.timestamp
  }))
  
  const dataStr = JSON.stringify(chatData, null, 2)
  const dataBlob = new Blob([dataStr], {type: 'application/json'})
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `chat-export-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const addWelcomeMessage = () => {
  const welcomeMessages = {
    general: '¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?',
    sales: '¡Bienvenido! Soy tu asistente comercial. ¿Te interesa conocer nuestros productos?',
    support: 'Hola, soy tu asistente de soporte técnico. ¿Qué problema puedo ayudarte a resolver?',
    technical: 'Saludos, soy tu especialista técnico. ¿Necesitas ayuda con alguna configuración?'
  }
  
  messages.value.push({
    id: 1,
    text: welcomeMessages[currentChatbot.value.type] || welcomeMessages.general,
    isUser: false,
    timestamp: new Date()
  })
}

// Watchers
watch(() => props.chatbotId, (newChatbotId) => {
  if (newChatbotId) {
    // Actualizar información del chatbot basado en el ID
    // Aquí podrías hacer una llamada a la API para obtener los detalles del chatbot
    console.log('Chatbot changed:', newChatbotId)
  }
})

// Auto-resize textarea
watch(newMessage, () => {
  nextTick(() => {
    const textarea = document.querySelector('textarea')
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
    }
  })
})

// Lifecycle
onMounted(() => {
  addWelcomeMessage()
  scrollToBottom()
})

// Expose methods for parent components
defineExpose({
  clearChat,
  scrollToTop,
  addMessage: (message) => {
    messages.value.push({
      id: Date.now(),
      text: message.text,
      isUser: message.isUser || false,
      timestamp: new Date()
    })
    nextTick(() => scrollToBottom())
  },
  getMessages: () => messages.value
})
</script>

<style scoped>
.chat-container {
  background: #f8fafc;
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.animate-bounce {
  animation: bounce 1.4s infinite;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-6px);
  }
}

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

/* Message animations */
.flex {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>