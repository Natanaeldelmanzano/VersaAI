<template>
  <div class="conversations-page">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Conversaciones</h1>
            <p class="text-gray-600 mt-1">Gestiona y revisa todas las conversaciones de tus chatbots</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="exportConversations"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Exportar
            </button>
            <button
              @click="refreshConversations"
              :disabled="isLoading"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Buscar conversaciones..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @input="debouncedSearch"
            >
          </div>

          <!-- Chatbot Filter -->
          <select
            v-model="filters.chatbot_id"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los chatbots</option>
            <option v-for="chatbot in availableChatbots" :key="chatbot.id" :value="chatbot.id">
              {{ chatbot.name }}
            </option>
          </select>

          <!-- Status Filter -->
          <select
            v-model="filters.status"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activas</option>
            <option value="completed">Completadas</option>
            <option value="abandoned">Abandonadas</option>
          </select>

          <!-- Date Range -->
          <select
            v-model="filters.date_range"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todas las fechas</option>
            <option value="today">Hoy</option>
            <option value="week">Esta semana</option>
            <option value="month">Este mes</option>
            <option value="quarter">Este trimestre</option>
          </select>
        </div>

        <!-- Clear Filters -->
        <div class="mt-4 flex items-center justify-between">
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Limpiar filtros
          </button>
          <div class="text-sm text-gray-500">
            {{ totalConversations }} conversaciones encontradas
          </div>
        </div>
      </div>
    </div>

    <!-- Conversations List -->
    <div class="flex-1 overflow-hidden">
      <div class="h-full flex">
        <!-- Conversations Sidebar -->
        <div class="w-1/3 bg-white border-r border-gray-200 overflow-y-auto conversations-list scrollable">
          <div v-if="isLoading" class="p-6">
            <div class="space-y-4">
              <div v-for="i in 5" :key="i" class="animate-pulse">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
                  <div class="flex-1">
                    <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div class="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="conversations.length === 0" class="p-6 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.959 8.959 0 01-4.906-1.471L3 21l2.471-5.094A8.959 8.959 0 013 12c0-4.418 3.582-8 8-8s8 3.582 8 8z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No hay conversaciones</h3>
            <p class="mt-1 text-sm text-gray-500">No se encontraron conversaciones con los filtros aplicados.</p>
          </div>

          <div v-else class="divide-y divide-gray-200">
            <div
              v-for="conversation in conversations"
              :key="conversation.id"
              @click="selectConversation(conversation)"
              :class="[
                'p-4 cursor-pointer hover:bg-gray-50 transition-colors',
                selectedConversation?.id === conversation.id ? 'bg-blue-50 border-r-2 border-blue-500' : ''
              ]"
            >
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                    {{ conversation.user_name ? conversation.user_name.charAt(0).toUpperCase() : 'U' }}
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900 truncate">
                      {{ conversation.user_name || 'Usuario Anónimo' }}
                    </p>
                    <span :class="getStatusBadgeClass(conversation.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
                      {{ getStatusText(conversation.status) }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 truncate mt-1">
                    {{ conversation.chatbot_name }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ formatDate(conversation.created_at) }} • {{ conversation.message_count }} mensajes
                  </p>
                  <p v-if="conversation.last_message" class="text-xs text-gray-400 mt-1 truncate">
                    {{ conversation.last_message }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Conversation Detail -->
        <div class="flex-1 flex flex-col">
          <div v-if="!selectedConversation" class="flex-1 flex items-center justify-center bg-gray-50">
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.959 8.959 0 01-4.906-1.471L3 21l2.471-5.094A8.959 8.959 0 013 12c0-4.418 3.582-8 8-8s8 3.582 8 8z" />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">Selecciona una conversación</h3>
              <p class="mt-1 text-sm text-gray-500">Elige una conversación de la lista para ver los detalles.</p>
            </div>
          </div>

          <div v-else class="flex-1 flex flex-col">
            <!-- Conversation Header -->
            <div class="bg-white border-b border-gray-200 px-6 py-4">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-lg font-semibold text-gray-900">
                    {{ selectedConversation.user_name || 'Usuario Anónimo' }}
                  </h2>
                  <p class="text-sm text-gray-600">
                    {{ selectedConversation.chatbot_name }} • {{ formatDate(selectedConversation.created_at) }}
                  </p>
                </div>
                <div class="flex items-center space-x-3">
                  <span :class="getStatusBadgeClass(selectedConversation.status)" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium">
                    {{ getStatusText(selectedConversation.status) }}
                  </span>
                  <div class="relative">
                    <button
                      @click="showConversationMenu = !showConversationMenu"
                      class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                    >
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                      </svg>
                    </button>
                    <div
                      v-if="showConversationMenu"
                      class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
                    >
                      <div class="py-1">
                        <button
                          @click="exportConversation(selectedConversation.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Exportar conversación
                        </button>
                        <button
                          @click="markAsResolved(selectedConversation.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Marcar como resuelta
                        </button>
                        <button
                          @click="deleteConversation(selectedConversation.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                        >
                          Eliminar conversación
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Messages -->
            <div class="flex-1 overflow-y-auto bg-gray-50 p-6">
              <div class="space-y-4">
                <div
                  v-for="message in selectedConversation.messages"
                  :key="message.id"
                  :class="[
                    'flex',
                    message.sender_type === 'user' ? 'justify-end' : 'justify-start'
                  ]"
                >
                  <div
                    :class="[
                      'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                      message.sender_type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-900 border border-gray-200'
                    ]"
                  >
                    <p class="text-sm">{{ message.content }}</p>
                    <p
                      :class="[
                        'text-xs mt-1',
                        message.sender_type === 'user' ? 'text-blue-100' : 'text-gray-500'
                      ]"
                    >
                      {{ formatTime(message.created_at) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="bg-white border-t border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-700">
          Mostrando {{ (currentPage - 1) * perPage + 1 }} a {{ Math.min(currentPage * perPage, totalConversations) }} de {{ totalConversations }} conversaciones
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>
          <span class="px-3 py-2 text-sm font-medium text-gray-700">
            Página {{ currentPage }} de {{ totalPages }}
          </span>
          <button
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Siguiente
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'vue-toastification'
import { debounce } from 'lodash-es'

export default {
  name: 'Conversations',
  setup() {
    const toast = useToast()
    
    // State
    const isLoading = ref(false)
    const conversations = ref([])
    const selectedConversation = ref(null)
    const showConversationMenu = ref(false)
    const availableChatbots = ref([])
    const searchQuery = ref('')
    
    // Filters
    const filters = ref({
      search: '',
      chatbot_id: '',
      status: '',
      date_range: ''
    })
    
    // Pagination
    const currentPage = ref(1)
    const perPage = ref(20)
    const totalConversations = ref(0)
    const totalPages = computed(() => Math.ceil(totalConversations.value / perPage.value))
    
    // Computed
    const hasActiveFilters = computed(() => {
      return Object.values(filters.value).some(value => value !== '')
    })
    
    const stats = computed(() => ({
      total: conversations.value.length,
      active: conversations.value.filter(c => c.status === 'active').length,
      archived: conversations.value.filter(c => c.status === 'archived').length
    }))

    const filteredConversations = computed(() => {
      if (!searchQuery.value) return conversations.value
      
      return conversations.value.filter(conversation => 
        (conversation.user_name && conversation.user_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
        conversation.chatbot_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (conversation.last_message && conversation.last_message.toLowerCase().includes(searchQuery.value.toLowerCase()))
      )
    })
    
    // Mock data
    const mockConversations = [
      {
        id: 1,
        user_name: 'María García',
        chatbot_name: 'Asistente de Ventas',
        status: 'completed',
        message_count: 12,
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        last_message: '¡Perfecto! Gracias por la información.',
        messages: [
          {
            id: 1,
            content: 'Hola, necesito información sobre sus productos',
            sender_type: 'user',
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 2,
            content: '¡Hola María! Estaré encantado de ayudarte con información sobre nuestros productos. ¿Hay algo específico que te interese?',
            sender_type: 'bot',
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000 + 30000).toISOString()
          },
          {
            id: 3,
            content: 'Me interesa conocer los planes de suscripción',
            sender_type: 'user',
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000 + 60000).toISOString()
          },
          {
            id: 4,
            content: 'Tenemos tres planes principales: Básico ($29/mes), Profesional ($79/mes) y Empresarial ($199/mes). Cada uno incluye diferentes características. ¿Te gustaría que te explique las diferencias?',
            sender_type: 'bot',
            created_at: new Date(Date.now() - 2 * 60 * 60 * 1000 + 90000).toISOString()
          }
        ]
      },
      {
        id: 2,
        user_name: 'Carlos Rodríguez',
        chatbot_name: 'Soporte Técnico',
        status: 'active',
        message_count: 8,
        created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        last_message: 'Estoy revisando tu problema...',
        messages: [
          {
            id: 5,
            content: 'Tengo un problema con mi cuenta, no puedo acceder',
            sender_type: 'user',
            created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString()
          },
          {
            id: 6,
            content: 'Lamento escuchar que tienes problemas para acceder. ¿Podrías decirme qué mensaje de error ves cuando intentas iniciar sesión?',
            sender_type: 'bot',
            created_at: new Date(Date.now() - 29 * 60 * 1000).toISOString()
          }
        ]
      },
      {
        id: 3,
        user_name: null,
        chatbot_name: 'Recursos Humanos',
        status: 'abandoned',
        message_count: 3,
        created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        last_message: 'Hola, ¿en qué puedo ayudarte?',
        messages: [
          {
            id: 7,
            content: 'Hola',
            sender_type: 'user',
            created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 8,
            content: 'Hola, ¿en qué puedo ayudarte?',
            sender_type: 'bot',
            created_at: new Date(Date.now() - 24 * 60 * 60 * 1000 + 5000).toISOString()
          }
        ]
      }
    ]
    
    const mockChatbots = [
      { id: 1, name: 'Asistente de Ventas' },
      { id: 2, name: 'Soporte Técnico' },
      { id: 3, name: 'Recursos Humanos' }
    ]
    
    // Methods
    const loadConversations = async () => {
      try {
        isLoading.value = true
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Apply filters to mock data
        let filteredConversations = [...mockConversations]
        
        if (filters.value.search) {
          filteredConversations = filteredConversations.filter(conv => 
            (conv.user_name && conv.user_name.toLowerCase().includes(filters.value.search.toLowerCase())) ||
            conv.chatbot_name.toLowerCase().includes(filters.value.search.toLowerCase())
          )
        }
        
        if (filters.value.chatbot_id) {
          filteredConversations = filteredConversations.filter(conv => 
            conv.chatbot_name === mockChatbots.find(bot => bot.id == filters.value.chatbot_id)?.name
          )
        }
        
        if (filters.value.status) {
          filteredConversations = filteredConversations.filter(conv => conv.status === filters.value.status)
        }
        
        conversations.value = filteredConversations
        totalConversations.value = filteredConversations.length
        
      } catch (error) {
        console.error('Error loading conversations:', error)
        toast.error('Error al cargar las conversaciones')
      } finally {
        isLoading.value = false
      }
    }
    
    const loadChatbots = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500))
        availableChatbots.value = mockChatbots
      } catch (error) {
        console.error('Error loading chatbots:', error)
      }
    }
    
    const selectConversation = (conversation) => {
      selectedConversation.value = conversation
      showConversationMenu.value = false
    }
    
    const applyFilters = () => {
      currentPage.value = 1
      loadConversations()
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        chatbot_id: '',
        status: '',
        date_range: ''
      }
      applyFilters()
    }
    
    const debouncedSearch = debounce(() => {
      applyFilters()
    }, 300)
    
    const refreshConversations = () => {
      loadConversations()
    }
    
    const exportConversations = () => {
      toast.info('Función de exportación en desarrollo')
    }
    
    const exportConversation = (id) => {
      toast.info(`Exportando conversación ${id}...`)
      showConversationMenu.value = false
    }
    
    const markAsResolved = (id) => {
      toast.success('Conversación marcada como resuelta')
      showConversationMenu.value = false
    }
    
    const deleteConversation = (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar esta conversación?')) {
        conversations.value = conversations.value.filter(conv => conv.id !== id)
        if (selectedConversation.value?.id === id) {
          selectedConversation.value = null
        }
        toast.success('Conversación eliminada')
      }
      showConversationMenu.value = false
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        loadConversations()
      }
    }
    
    // Utility functions
    const getStatusBadgeClass = (status) => {
      const classes = {
        active: 'bg-green-100 text-green-800',
        completed: 'bg-blue-100 text-blue-800',
        abandoned: 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
    
    const getStatusText = (status) => {
      const texts = {
        active: 'Activa',
        completed: 'Completada',
        abandoned: 'Abandonada'
      }
      return texts[status] || 'Desconocido'
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInHours = (now - date) / (1000 * 60 * 60)
      
      if (diffInHours < 1) {
        return 'Hace unos minutos'
      } else if (diffInHours < 24) {
        return `Hace ${Math.floor(diffInHours)} horas`
      } else if (diffInHours < 48) {
        return 'Ayer'
      } else {
        return date.toLocaleDateString('es-ES', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        })
      }
    }
    
    const formatTime = (dateString) => {
      return new Date(dateString).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const scrollToTop = () => {
      const conversationsList = document.querySelector('.conversations-list')
      if (conversationsList) {
        conversationsList.scrollTo({
          top: 0,
          behavior: 'smooth'
        })
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadConversations()
      loadChatbots()
    })
    
    // Close menu when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        showConversationMenu.value = false
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })
    
    return {
      // State
      isLoading,
      conversations,
      selectedConversation,
      showConversationMenu,
      availableChatbots,
      filters,
      currentPage,
      perPage,
      totalConversations,
      totalPages,
      
      // Computed
      hasActiveFilters,
      stats,
      filteredConversations,
      
      // Methods
      selectConversation,
      applyFilters,
      clearFilters,
      debouncedSearch,
      refreshConversations,
      exportConversations,
      exportConversation,
      markAsResolved,
      deleteConversation,
      goToPage,
      scrollToTop,
      
      // Utilities
      getStatusBadgeClass,
      getStatusText,
      formatDate,
      formatTime,
      
      // Search
      searchQuery
    }
  }
}
</script>

<style scoped>
.conversations-page {
  @apply h-full flex flex-col;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>