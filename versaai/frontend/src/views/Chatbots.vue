<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 chatbots-container">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow sticky top-0 z-10">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">🤖 Gestión de Chatbots</h1>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Crea y administra tus asistentes de IA</p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="scrollToTop"
              class="text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              title="Ir al inicio"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
              </svg>
            </button>
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Crear Chatbot
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 scroll-smooth">
      <div class="px-4 py-6 sm:px-0">
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600 dark:text-gray-400">Cargando chatbots...</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-600 dark:text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-red-800 dark:text-red-200">{{ error }}</span>
          </div>
        </div>

        <!-- Stats Cards -->
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div class="flex items-center">
              <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Chatbots Totales</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ chatbots.length }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div class="flex items-center">
              <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Activos</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ activeChatbots }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div class="flex items-center">
              <div class="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Conversaciones Hoy</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ todayConversations }}</p>
              </div>
            </div>
          </div>
        </div>
        </div>

        <!-- Chatbots Grid -->
        <div v-if="chatbots.length > 0" class="chatbots-grid max-h-screen overflow-y-auto scrollable">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-8">
            <div
              v-for="chatbot in chatbots"
              :key="chatbot.id"
              class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            >
            <div class="p-6">
              <!-- Chatbot Header -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                  <div class="text-3xl mr-3">{{ chatbot.avatar }}</div>
                  <div>
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ chatbot.name }}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ chatbot.description }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      chatbot.status === 'active'
                        ? 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100'
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
                    ]"
                  >
                    {{ chatbot.status === 'active' ? 'Activo' : 'Inactivo' }}
                  </span>
                </div>
              </div>

              <!-- Chatbot Stats -->
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Conversaciones</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ chatbot.conversations }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Satisfacción</p>
                  <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ chatbot.satisfaction }}%</p>
                </div>
              </div>

              <!-- Actions -->
              <div class="flex flex-wrap gap-2">
                <button
                  @click="editChatbot(chatbot)"
                  class="flex-1 min-w-0 bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium py-2 px-2 rounded transition-colors"
                >
                  Editar
                </button>
                <button
                  @click="testChatbot(chatbot)"
                  class="flex-1 min-w-0 bg-green-600 hover:bg-green-700 text-white text-xs font-medium py-2 px-2 rounded transition-colors"
                >
                  Probar
                </button>
                <button
                  @click="trainChatbotAction(chatbot)"
                  class="flex-1 min-w-0 bg-purple-600 hover:bg-purple-700 text-white text-xs font-medium py-2 px-2 rounded transition-colors"
                >
                  Entrenar
                </button>
                <button
                  @click="toggleChatbot(chatbot)"
                  :class="[
                    'flex-1 min-w-0 text-white text-xs font-medium py-2 px-2 rounded transition-colors',
                    chatbot.status === 'active'
                      ? 'bg-orange-600 hover:bg-orange-700'
                      : 'bg-gray-600 hover:bg-gray-700'
                  ]"
                >
                  {{ chatbot.status === 'active' ? 'Pausar' : 'Activar' }}
                </button>
                <button
                  @click="confirmDeleteChatbot(chatbot)"
                  class="flex-1 min-w-0 bg-red-600 hover:bg-red-700 text-white text-xs font-medium py-2 px-2 rounded transition-colors"
                >
                  Eliminar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <div class="text-6xl mb-4">🤖</div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No tienes chatbots aún
          </h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">
            Crea tu primer chatbot para comenzar a automatizar conversaciones
          </p>
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Crear Mi Primer Chatbot
          </button>
        </div>
      </div>
    </main>

    <!-- Create Chatbot Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800">
        <div class="mt-3">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Crear Nuevo Chatbot</h3>
            <button
              @click="showCreateModal = false"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="createChatbot" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Nombre del Chatbot
              </label>
              <input
                v-model="newChatbot.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                placeholder="Ej: Asistente de Ventas"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Descripción
              </label>
              <textarea
                v-model="newChatbot.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                placeholder="Describe la función de tu chatbot..."
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Avatar (Emoji)
              </label>
              <div class="grid grid-cols-6 gap-2">
                <button
                  v-for="emoji in availableEmojis"
                  :key="emoji"
                  type="button"
                  @click="newChatbot.avatar = emoji"
                  :class="[
                    'text-2xl p-2 rounded border-2 hover:bg-gray-100 dark:hover:bg-gray-700',
                    newChatbot.avatar === emoji
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900'
                      : 'border-gray-300 dark:border-gray-600'
                  ]"
                >
                  {{ emoji }}
                </button>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 rounded-md"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="!newChatbot.name.trim()"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Crear Chatbot
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white dark:bg-gray-800">
        <div class="mt-3">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Confirmar Eliminación</h3>
            <button
              @click="showDeleteModal = false"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="mb-6">
            <div class="flex items-center mb-4">
              <div class="p-3 bg-red-100 dark:bg-red-900 rounded-full mr-4">
                <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div>
                <h4 class="text-lg font-medium text-gray-900 dark:text-white">¿Estás seguro?</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  Esta acción no se puede deshacer. El chatbot "{{ chatbotToDelete?.name }}" será eliminado permanentemente.
                </p>
              </div>
            </div>
          </div>

          <div class="flex justify-end space-x-3">
            <button
              @click="showDeleteModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 rounded-md"
            >
              Cancelar
            </button>
            <button
              @click="deleteChatbotConfirmed"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-md"
            >
              Eliminar Chatbot
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatbots } from '@/composables/useChatbots'

const router = useRouter()

// Use chatbots composable
const {
  chatbots,
  loading,
  error,
  metrics,
  filteredChatbots,
  loadChatbots,
  createChatbot: createChatbotAPI,
  updateChatbot,
  deleteChatbot,
  toggleChatbotStatus,
  trainChatbot
} = useChatbots()

// Local reactive data
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const chatbotToDelete = ref(null)

// New chatbot form
const newChatbot = ref({
  name: '',
  description: '',
  avatar: '🤖',
  model: 'groq-llama',
  temperature: 0.7,
  max_tokens: 1000
})

const availableEmojis = [
  '🤖', '👨‍💼', '👩‍💼', '🎯', '💼', '🛍️',
  '📞', '💬', '🎓', '🏥', '🏪', '🍕'
]

// Computed properties
const activeChatbots = computed(() => {
  return metrics.value.active_chatbots || 0
})

const todayConversations = computed(() => {
  return metrics.value.total_conversations || 0
})

const averageSatisfaction = computed(() => {
  return metrics.value.average_satisfaction || 0
})

// Methods
const createChatbot = async () => {
  try {
    await createChatbotAPI({
      name: newChatbot.value.name,
      description: newChatbot.value.description || 'Sin descripción',
      avatar: newChatbot.value.avatar,
      model: newChatbot.value.model,
      temperature: newChatbot.value.temperature,
      max_tokens: newChatbot.value.max_tokens,
      status: 'active'
    })
    
    // Reset form
    newChatbot.value = {
      name: '',
      description: '',
      avatar: '🤖',
      model: 'groq-llama',
      temperature: 0.7,
      max_tokens: 1000
    }
    
    showCreateModal.value = false
  } catch (error) {
    console.error('Error creating chatbot:', error)
  }
}

const editChatbot = (chatbot) => {
  // TODO: Implement edit modal
  alert(`🔧 Función de edición para "${chatbot.name}" estará disponible próximamente`)
}

const testChatbot = (chatbot) => {
  // Redirect to chat with specific bot context
  router.push({
    path: '/chat',
    query: { bot: chatbot.id, name: chatbot.name }
  })
}

const toggleChatbot = async (chatbot) => {
  try {
    await toggleChatbotStatus(chatbot.id)
  } catch (error) {
    console.error('Error toggling chatbot status:', error)
  }
}

const confirmDeleteChatbot = (chatbot) => {
  chatbotToDelete.value = chatbot
  showDeleteModal.value = true
}

const deleteChatbotConfirmed = async () => {
  if (chatbotToDelete.value) {
    try {
      await deleteChatbot(chatbotToDelete.value.id)
      showDeleteModal.value = false
      chatbotToDelete.value = null
    } catch (error) {
      console.error('Error deleting chatbot:', error)
    }
  }
}

const trainChatbotAction = async (chatbot) => {
  try {
    await trainChatbot(chatbot.id)
  } catch (error) {
    console.error('Error training chatbot:', error)
  }
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// Lifecycle
onMounted(async () => {
  await loadChatbots()
  console.log('🤖 Chatbots component loaded')
})

// Export functions for template usage
defineExpose({
  scrollToTop
})
</script>

<style scoped>
/* Custom styles for modal backdrop */
.fixed {
  backdrop-filter: blur(4px);
}

/* Chatbots container styles */
.chatbots-container {
  scroll-behavior: smooth;
}

.chatbots-grid {
  scroll-behavior: smooth;
}

.scrollable {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.scrollable::-webkit-scrollbar {
  width: 8px;
}

.scrollable::-webkit-scrollbar-track {
  background: #f7fafc;
  border-radius: 4px;
}

.scrollable::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 4px;
}

.scrollable::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* Dark mode scrollbar */
.dark .scrollable {
  scrollbar-color: #4a5568 #2d3748;
}

.dark .scrollable::-webkit-scrollbar-track {
  background: #2d3748;
}

.dark .scrollable::-webkit-scrollbar-thumb {
  background: #4a5568;
}

.dark .scrollable::-webkit-scrollbar-thumb:hover {
  background: #718096;
}
</style>