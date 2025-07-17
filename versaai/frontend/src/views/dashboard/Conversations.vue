<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Conversaciones</h1>
        <p class="text-gray-600">Monitorea y gestiona todas las conversaciones de tus chatbots</p>
      </div>
      <div class="flex space-x-3">
        <button
          @click="exportConversations"
          class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          Exportar
        </button>
        <button
          @click="refreshConversations"
          :disabled="loading"
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 disabled:opacity-50"
        >
          {{ loading ? 'Actualizando...' : 'Actualizar' }}
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Buscar
          </label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Buscar conversaciones..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Chatbot
          </label>
          <select
            v-model="filters.chatbot"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">Todos los chatbots</option>
            <option v-for="chatbot in chatbots" :key="chatbot.id" :value="chatbot.id">
              {{ chatbot.name }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Estado
          </label>
          <select
            v-model="filters.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activa</option>
            <option value="completed">Completada</option>
            <option value="abandoned">Abandonada</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Fecha
          </label>
          <select
            v-model="filters.dateRange"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="today">Hoy</option>
            <option value="week">Esta semana</option>
            <option value="month">Este mes</option>
            <option value="all">Todas</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <ChatBubbleLeftRightIcon class="h-8 w-8 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Total Conversaciones</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.total }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <CheckCircleIcon class="h-8 w-8 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Completadas</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.completed }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <ClockIcon class="h-8 w-8 text-yellow-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Promedio Duración</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.avgDuration }}m</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <FaceSmileIcon class="h-8 w-8 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Satisfacción</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.satisfaction }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Conversations List -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">Conversaciones Recientes</h2>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
        <p class="text-gray-500 mt-2">Cargando conversaciones...</p>
      </div>
      
      <div v-else-if="filteredConversations.length === 0" class="p-8 text-center">
        <ChatBubbleLeftRightIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p class="text-gray-500">No se encontraron conversaciones</p>
      </div>
      
      <div v-else class="divide-y divide-gray-200">
        <div
          v-for="conversation in paginatedConversations"
          :key="conversation.id"
          class="p-6 hover:bg-gray-50 cursor-pointer transition-colors duration-200"
          @click="viewConversation(conversation)"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                  <UserIcon class="h-5 w-5 text-primary-600" />
                </div>
              </div>
              
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {{ conversation.user || 'Usuario Anónimo' }}
                  </p>
                  <span
                    :class="[
                      'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                      conversation.status === 'active' ? 'bg-green-100 text-green-800' :
                      conversation.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ getStatusLabel(conversation.status) }}
                  </span>
                </div>
                
                <div class="flex items-center space-x-4 mt-1">
                  <p class="text-sm text-gray-500">
                    {{ conversation.chatbot.name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ conversation.messageCount }} mensajes
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ formatDate(conversation.startedAt) }}
                  </p>
                </div>
                
                <p class="text-sm text-gray-600 mt-2 truncate">
                  {{ conversation.lastMessage }}
                </p>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <div v-if="conversation.rating" class="flex items-center">
                <StarIcon class="h-4 w-4 text-yellow-400" />
                <span class="text-sm text-gray-600 ml-1">{{ conversation.rating }}/5</span>
              </div>
              
              <ChevronRightIcon class="h-5 w-5 text-gray-400" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a 
            {{ Math.min(currentPage * itemsPerPage, filteredConversations.length) }} 
            de {{ filteredConversations.length }} conversaciones
          </div>
          
          <div class="flex space-x-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Anterior
            </button>
            
            <span class="px-3 py-1 text-sm text-gray-700">
              Página {{ currentPage }} de {{ totalPages }}
            </span>
            
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Conversation Detail Modal -->
    <div
      v-if="selectedConversation"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="selectedConversation = null"
    >
      <div
        class="relative top-10 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-lg font-medium text-gray-900">
            Conversación con {{ selectedConversation.user || 'Usuario Anónimo' }}
          </h3>
          <button
            @click="selectedConversation = null"
            class="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="space-y-4 max-h-96 overflow-y-auto">
          <div
            v-for="message in selectedConversation.messages"
            :key="message.id"
            :class="[
              'flex',
              message.sender === 'user' ? 'justify-end' : 'justify-start'
            ]"
          >
            <div
              :class="[
                'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                message.sender === 'user'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              ]"
            >
              <p class="text-sm">{{ message.content }}</p>
              <p class="text-xs mt-1 opacity-75">
                {{ formatTime(message.timestamp) }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="exportConversation(selectedConversation)"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
          >
            Exportar
          </button>
          <button
            @click="selectedConversation = null"
            class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  ChatBubbleLeftRightIcon,
  CheckCircleIcon,
  ClockIcon,
  FaceSmileIcon,
  UserIcon,
  ChevronRightIcon,
  StarIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/api'

const toast = useToast()

const loading = ref(false)
const conversations = ref([])
const chatbots = ref([])
const selectedConversation = ref(null)
const currentPage = ref(1)
const itemsPerPage = ref(10)

const filters = ref({
  search: '',
  chatbot: '',
  status: '',
  dateRange: 'all'
})

const stats = ref({
  total: 0,
  completed: 0,
  avgDuration: 0,
  satisfaction: 0
})

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activa',
    completed: 'Completada',
    abandoned: 'Abandonada'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  return format(new Date(date), 'dd MMM yyyy HH:mm', { locale: es })
}

const formatTime = (date) => {
  return format(new Date(date), 'HH:mm', { locale: es })
}

const filteredConversations = computed(() => {
  let filtered = conversations.value
  
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(conv => 
      (conv.user && conv.user.toLowerCase().includes(search)) ||
      conv.lastMessage.toLowerCase().includes(search) ||
      conv.chatbot.name.toLowerCase().includes(search)
    )
  }
  
  if (filters.value.chatbot) {
    filtered = filtered.filter(conv => conv.chatbot.id === filters.value.chatbot)
  }
  
  if (filters.value.status) {
    filtered = filtered.filter(conv => conv.status === filters.value.status)
  }
  
  if (filters.value.dateRange !== 'all') {
    const now = new Date()
    const filterDate = new Date()
    
    switch (filters.value.dateRange) {
      case 'today':
        filterDate.setHours(0, 0, 0, 0)
        break
      case 'week':
        filterDate.setDate(now.getDate() - 7)
        break
      case 'month':
        filterDate.setMonth(now.getMonth() - 1)
        break
    }
    
    filtered = filtered.filter(conv => new Date(conv.startedAt) >= filterDate)
  }
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredConversations.value.length / itemsPerPage.value)
})

const paginatedConversations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredConversations.value.slice(start, end)
})

const fetchConversations = async () => {
  loading.value = true
  try {
    const response = await api.get('/conversations')
    conversations.value = response.data
  } catch (error) {
    console.error('Error fetching conversations:', error)
    toast.error('Error al cargar las conversaciones')
  } finally {
    loading.value = false
  }
}

const fetchChatbots = async () => {
  try {
    const response = await api.get('/chatbots')
    chatbots.value = response.data
  } catch (error) {
    console.error('Error fetching chatbots:', error)
  }
}

const fetchStats = async () => {
  try {
    const response = await api.get('/conversations/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

const refreshConversations = async () => {
  await Promise.all([
    fetchConversations(),
    fetchStats()
  ])
}

const viewConversation = async (conversation) => {
  try {
    const response = await api.get(`/conversations/${conversation.id}`)
    selectedConversation.value = response.data
  } catch (error) {
    console.error('Error fetching conversation details:', error)
    toast.error('Error al cargar los detalles de la conversación')
  }
}

const exportConversations = async () => {
  try {
    const response = await api.get('/conversations/export', {
      responseType: 'blob',
      params: filters.value
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `conversaciones_${format(new Date(), 'yyyy-MM-dd')}.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    toast.success('Conversaciones exportadas correctamente')
  } catch (error) {
    console.error('Error exporting conversations:', error)
    toast.error('Error al exportar las conversaciones')
  }
}

const exportConversation = async (conversation) => {
  try {
    const response = await api.get(`/conversations/${conversation.id}/export`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `conversacion_${conversation.id}.txt`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    toast.success('Conversación exportada correctamente')
  } catch (error) {
    console.error('Error exporting conversation:', error)
    toast.error('Error al exportar la conversación')
  }
}

// Reset pagination when filters change
watch(filters, () => {
  currentPage.value = 1
}, { deep: true })

onMounted(async () => {
  await Promise.all([
    fetchConversations(),
    fetchChatbots(),
    fetchStats()
  ])
})
</script>