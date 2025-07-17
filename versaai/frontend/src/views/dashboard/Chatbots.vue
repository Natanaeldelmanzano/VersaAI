<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Chatbots
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          Gestiona y configura tus chatbots inteligentes
        </p>
      </div>
      <div class="mt-4 flex md:mt-0 md:ml-4">
        <router-link
          to="/dashboard/chatbots/new"
          class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PlusIcon class="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
          Nuevo Chatbot
        </router-link>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white shadow rounded-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label for="search" class="block text-sm font-medium text-gray-700 mb-1">
            Buscar
          </label>
          <input
            id="search"
            v-model="filters.search"
            type="text"
            placeholder="Nombre del chatbot..."
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
        </div>
        
        <div>
          <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
            Estado
          </label>
          <select
            id="status"
            v-model="filters.status"
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="">Todos</option>
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
            <option value="draft">Borrador</option>
          </select>
        </div>
        
        <div>
          <label for="sort" class="block text-sm font-medium text-gray-700 mb-1">
            Ordenar por
          </label>
          <select
            id="sort"
            v-model="filters.sort"
            class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="created_at">Fecha de creación</option>
            <option value="name">Nombre</option>
            <option value="updated_at">Última actualización</option>
          </select>
        </div>
        
        <div class="flex items-end">
          <button
            @click="resetFilters"
            class="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <XMarkIcon class="-ml-1 mr-2 h-4 w-4" />
            Limpiar
          </button>
        </div>
      </div>
    </div>

    <!-- Chatbots Grid -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="bg-white shadow rounded-lg p-6 animate-pulse">
        <div class="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div class="h-3 bg-gray-200 rounded w-full mb-2"></div>
        <div class="h-3 bg-gray-200 rounded w-2/3 mb-4"></div>
        <div class="h-8 bg-gray-200 rounded w-1/3"></div>
      </div>
    </div>
    
    <div v-else-if="chatbots.length === 0" class="text-center py-12">
      <CpuChipIcon class="mx-auto h-12 w-12 text-gray-400" />
      <h3 class="mt-2 text-sm font-medium text-gray-900">No hay chatbots</h3>
      <p class="mt-1 text-sm text-gray-500">
        Comienza creando tu primer chatbot inteligente.
      </p>
      <div class="mt-6">
        <router-link
          to="/dashboard/chatbots/new"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PlusIcon class="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
          Nuevo Chatbot
        </router-link>
      </div>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="chatbot in chatbots"
        :key="chatbot.id"
        class="bg-white shadow rounded-lg hover:shadow-md transition-shadow duration-200"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 truncate">
              {{ chatbot.name }}
            </h3>
            <span
              :class="[
                'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                chatbot.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              ]"
            >
              {{ chatbot.is_active ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          
          <p class="text-sm text-gray-500 mb-4 line-clamp-2">
            {{ chatbot.description || 'Sin descripción' }}
          </p>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center text-sm text-gray-500">
              <ChatBubbleLeftRightIcon class="h-4 w-4 mr-2" />
              {{ chatbot.total_conversations || 0 }} conversaciones
            </div>
            <div class="flex items-center text-sm text-gray-500">
              <ClockIcon class="h-4 w-4 mr-2" />
              Actualizado {{ formatDate(chatbot.updated_at) }}
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex space-x-2">
              <router-link
                :to="`/dashboard/chatbots/${chatbot.id}`"
                class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-primary-700 bg-primary-100 hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PencilIcon class="-ml-0.5 mr-1 h-3 w-3" />
                Editar
              </router-link>
              
              <button
                @click="toggleChatbotStatus(chatbot)"
                :class="[
                  'inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2',
                  chatbot.is_active
                    ? 'text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500'
                    : 'text-green-700 bg-green-100 hover:bg-green-200 focus:ring-green-500'
                ]"
                :disabled="statusLoading[chatbot.id]"
              >
                <component
                  :is="chatbot.is_active ? PauseIcon : PlayIcon"
                  class="-ml-0.5 mr-1 h-3 w-3"
                />
                {{ chatbot.is_active ? 'Pausar' : 'Activar' }}
              </button>
            </div>
            
            <div class="relative">
              <button
                @click="toggleDropdown(chatbot.id)"
                class="inline-flex items-center p-1.5 border border-transparent rounded text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <EllipsisVerticalIcon class="h-4 w-4" />
              </button>
              
              <div
                v-if="activeDropdown === chatbot.id"
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
              >
                <div class="py-1">
                  <button
                    @click="viewAnalytics(chatbot)"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <ChartBarIcon class="inline h-4 w-4 mr-2" />
                    Ver Analytics
                  </button>
                  
                  <button
                    @click="getEmbedCode(chatbot)"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <CodeBracketIcon class="inline h-4 w-4 mr-2" />
                    Código de Embed
                  </button>
                  
                  <button
                    @click="duplicateChatbot(chatbot)"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <DocumentDuplicateIcon class="inline h-4 w-4 mr-2" />
                    Duplicar
                  </button>
                  
                  <button
                    @click="deleteChatbot(chatbot)"
                    class="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50"
                  >
                    <TrashIcon class="inline h-4 w-4 mr-2" />
                    Eliminar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="pagination.total > 12" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 rounded-lg shadow">
      <div class="flex-1 flex justify-between sm:hidden">
        <button
          @click="previousPage"
          :disabled="pagination.page === 1"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Anterior
        </button>
        <button
          @click="nextPage"
          :disabled="pagination.page >= Math.ceil(pagination.total / 12)"
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Siguiente
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Mostrando
            <span class="font-medium">{{ (pagination.page - 1) * 12 + 1 }}</span>
            a
            <span class="font-medium">{{ Math.min(pagination.page * 12, pagination.total) }}</span>
            de
            <span class="font-medium">{{ pagination.total }}</span>
            resultados
          </p>
        </div>
        <div>
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button
              @click="previousPage"
              :disabled="pagination.page === 1"
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
            </button>
            
            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :class="[
                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                page === pagination.page
                  ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                  : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            
            <button
              @click="nextPage"
              :disabled="pagination.page >= Math.ceil(pagination.total / 12)"
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import {
  PlusIcon,
  CpuChipIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  PencilIcon,
  PlayIcon,
  PauseIcon,
  EllipsisVerticalIcon,
  ChartBarIcon,
  CodeBracketIcon,
  DocumentDuplicateIcon,
  TrashIcon,
  XMarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'
import { useChatbotsStore } from '@/stores/chatbots'
import { useToast } from 'vue-toastification'
import { formatDistanceToNow } from 'date-fns'
import { es } from 'date-fns/locale'

const chatbotsStore = useChatbotsStore()
const toast = useToast()

const loading = computed(() => chatbotsStore.isLoading)
const activeDropdown = ref(null)
const statusLoading = ref({})

const filters = reactive({
  search: '',
  status: '',
  sort: 'created_at'
})

const pagination = computed(() => chatbotsStore.pagination)

const chatbots = computed(() => chatbotsStore.chatbots)

const visiblePages = computed(() => {
  const totalPages = Math.ceil(pagination.value.total / 12)
  const current = pagination.value.page
  const pages = []
  
  let start = Math.max(1, current - 2)
  let end = Math.min(totalPages, current + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})



const formatDate = (date) => {
  return formatDistanceToNow(new Date(date), {
    addSuffix: true,
    locale: es
  })
}

const loadChatbots = async () => {
  try {
    const params = {
      page: pagination.value.page,
      per_page: 12,
      sort_by: filters.sort,
      sort_order: 'desc'
    }
    
    if (filters.search) {
      params.search = filters.search
    }
    
    if (filters.status) {
      params.status = filters.status
    }
    
    const response = await chatbotsStore.fetchChatbots(params)
    
    if (!response.success) {
      toast.error(response.error || 'Error al cargar los chatbots')
    }
  } catch (error) {
    console.error('Error loading chatbots:', error)
    toast.error('Error al cargar los chatbots')
  }
}

const resetFilters = () => {
  filters.search = ''
  filters.status = ''
  filters.sort = 'created_at'
  chatbotsStore.setPage(1)
  loadChatbots()
}

const toggleDropdown = (chatbotId) => {
  activeDropdown.value = activeDropdown.value === chatbotId ? null : chatbotId
}

const toggleChatbotStatus = async (chatbot) => {
  try {
    statusLoading.value[chatbot.id] = true
    
    const response = await chatbotsStore.toggleChatbotStatus(chatbot.id)
    
    if (!response.success) {
      toast.error(response.error || 'Error al cambiar el estado del chatbot')
    }
  } catch (error) {
    console.error('Error toggling chatbot status:', error)
    toast.error('Error al cambiar el estado del chatbot')
  } finally {
    statusLoading.value[chatbot.id] = false
  }
}

const viewAnalytics = (chatbot) => {
  activeDropdown.value = null
  // Navigate to analytics with chatbot filter
  // router.push(`/dashboard/analytics?chatbot=${chatbot.id}`)
}

const getEmbedCode = async (chatbot) => {
  try {
    activeDropdown.value = null
    const response = await chatbotsStore.getChatbotEmbedCode(chatbot.id)
    
    if (response.success) {
      // Copy to clipboard
      await navigator.clipboard.writeText(response.data.embed_code || response.data)
      toast.success('Código de embed copiado al portapapeles')
    } else {
      toast.error(response.error || 'Error al obtener el código de embed')
    }
  } catch (error) {
    console.error('Error getting embed code:', error)
    toast.error('Error al obtener el código de embed')
  }
}

const duplicateChatbot = async (chatbot) => {
  try {
    activeDropdown.value = null
    
    // Create a copy of the chatbot with modified name
    const duplicatedData = {
      name: `${chatbot.name} (Copia)`,
      description: chatbot.description,
      prompt: chatbot.prompt,
      model: chatbot.model,
      temperature: chatbot.temperature,
      max_tokens: chatbot.max_tokens,
      status: 'draft'
    }
    
    const response = await chatbotsStore.createChatbot(duplicatedData)
    
    if (response.success) {
      toast.success('Chatbot duplicado exitosamente')
      loadChatbots()
    } else {
      toast.error(response.error || 'Error al duplicar el chatbot')
    }
  } catch (error) {
    console.error('Error duplicating chatbot:', error)
    toast.error('Error al duplicar el chatbot')
  }
}

const deleteChatbot = async (chatbot) => {
  if (!confirm(`¿Estás seguro de que quieres eliminar el chatbot "${chatbot.name}"?`)) {
    return
  }
  
  try {
    activeDropdown.value = null
    const response = await chatbotsStore.deleteChatbot(chatbot.id)
    
    if (response.success) {
      toast.success('Chatbot eliminado exitosamente')
      loadChatbots()
    } else {
      toast.error(response.error || 'Error al eliminar el chatbot')
    }
  } catch (error) {
    console.error('Error deleting chatbot:', error)
    toast.error('Error al eliminar el chatbot')
  }
}

const previousPage = () => {
  if (pagination.value.page > 1) {
    chatbotsStore.setPage(pagination.value.page - 1)
    loadChatbots()
  }
}

const nextPage = () => {
  const totalPages = Math.ceil(pagination.value.total / pagination.value.per_page)
  if (pagination.value.page < totalPages) {
    chatbotsStore.setPage(pagination.value.page + 1)
    loadChatbots()
  }
}

const goToPage = (page) => {
  chatbotsStore.setPage(page)
  loadChatbots()
}

// Watch for filter changes
watch(
  () => [filters.search, filters.status, filters.sort],
  () => {
    chatbotsStore.setPage(1)
    loadChatbots()
  },
  { deep: true }
)

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeDropdown.value = null
  }
}

onMounted(() => {
  // Set initial per_page for this component
  chatbotsStore.setPerPage(12)
  loadChatbots()
  document.addEventListener('click', handleClickOutside)
})

// Cleanup
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>