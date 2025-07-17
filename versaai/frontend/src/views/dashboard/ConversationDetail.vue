<template>
  <div class="conversation-detail">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            @click="$router.go(-1)"
            class="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Conversación #{{ conversationId }}</h1>
            <p class="text-sm text-gray-500 mt-1">{{ conversation.created_at ? formatDate(conversation.created_at) : 'Cargando...' }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="statusClasses">
            {{ conversation.status || 'Activa' }}
          </span>
          <button 
            @click="exportConversation"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Exportar
          </button>
        </div>
      </div>
    </div>

    <!-- Conversation Info -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <p class="text-sm font-medium text-gray-500">Usuario</p>
          <p class="text-sm text-gray-900">{{ conversation.user_name || 'Anónimo' }}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Chatbot</p>
          <p class="text-sm text-gray-900">{{ conversation.chatbot_name || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Duración</p>
          <p class="text-sm text-gray-900">{{ conversation.duration || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-500">Mensajes</p>
          <p class="text-sm text-gray-900">{{ messages.length }}</p>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-hidden">
      <div class="h-full flex">
        <!-- Messages List -->
        <div class="flex-1 flex flex-col">
          <div class="flex-1 overflow-y-auto p-6">
            <div class="space-y-4">
              <div 
                v-for="message in messages" 
                :key="message.id"
                class="flex" 
                :class="message.sender === 'user' ? 'justify-end' : 'justify-start'"
              >
                <div 
                  class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
                  :class="message.sender === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-900'"
                >
                  <p class="text-sm">{{ message.content }}</p>
                  <p class="text-xs mt-1 opacity-75">{{ formatTime(message.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="w-80 bg-gray-50 border-l border-gray-200 p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Detalles</h3>
          
          <!-- Conversation Metrics -->
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Métricas</h4>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Tiempo de respuesta promedio</span>
                  <span class="text-gray-900">{{ conversation.avg_response_time || '2.3s' }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Satisfacción</span>
                  <span class="text-gray-900">{{ conversation.satisfaction_score || 'N/A' }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Resuelto</span>
                  <span class="text-gray-900">{{ conversation.resolved ? 'Sí' : 'No' }}</span>
                </div>
              </div>
            </div>

            <!-- Tags -->
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Etiquetas</h4>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="tag in conversation.tags || ['soporte', 'consulta']" 
                  :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ tag }}
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Acciones</h4>
              <div class="space-y-2">
                <button class="w-full text-left text-sm text-gray-700 hover:text-gray-900 py-1">
                  Marcar como resuelto
                </button>
                <button class="w-full text-left text-sm text-gray-700 hover:text-gray-900 py-1">
                  Agregar etiqueta
                </button>
                <button class="w-full text-left text-sm text-red-600 hover:text-red-700 py-1">
                  Eliminar conversación
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

const route = useRoute()
const toast = useToast()

const conversationId = computed(() => route.params.id)
const conversation = ref({})
const messages = ref([])
const loading = ref(true)

const statusClasses = computed(() => {
  const status = conversation.value.status || 'active'
  return {
    'bg-green-100 text-green-800': status === 'active',
    'bg-gray-100 text-gray-800': status === 'ended',
    'bg-red-100 text-red-800': status === 'error'
  }
})

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadConversation = async () => {
  try {
    loading.value = true
    // Simulated data - replace with actual API call
    conversation.value = {
      id: conversationId.value,
      user_name: 'Juan Pérez',
      chatbot_name: 'Asistente de Ventas',
      status: 'active',
      created_at: new Date().toISOString(),
      duration: '15 min',
      avg_response_time: '1.8s',
      satisfaction_score: '4.5/5',
      resolved: true,
      tags: ['ventas', 'producto', 'consulta']
    }
    
    messages.value = [
      {
        id: 1,
        sender: 'user',
        content: 'Hola, necesito información sobre sus productos',
        timestamp: new Date(Date.now() - 900000).toISOString()
      },
      {
        id: 2,
        sender: 'bot',
        content: '¡Hola! Estaré encantado de ayudarte con información sobre nuestros productos. ¿Hay algún producto específico que te interese?',
        timestamp: new Date(Date.now() - 880000).toISOString()
      },
      {
        id: 3,
        sender: 'user',
        content: 'Estoy buscando una solución de software para mi empresa',
        timestamp: new Date(Date.now() - 860000).toISOString()
      },
      {
        id: 4,
        sender: 'bot',
        content: 'Perfecto. Tenemos varias soluciones empresariales. ¿Podrías contarme un poco más sobre el tamaño de tu empresa y qué tipo de funcionalidades necesitas?',
        timestamp: new Date(Date.now() - 840000).toISOString()
      }
    ]
  } catch (error) {
    console.error('Error loading conversation:', error)
    toast.error('Error al cargar la conversación')
  } finally {
    loading.value = false
  }
}

const exportConversation = () => {
  // Implement export functionality
  toast.success('Conversación exportada exitosamente')
}

onMounted(() => {
  loadConversation()
})
</script>

<style scoped>
.conversation-detail {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}
</style>