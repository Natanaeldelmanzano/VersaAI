<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Gestión de Chatbots</h1>
            <p class="mt-2 text-gray-600">Crea, configura y gestiona tus asistentes de IA</p>
          </div>
          <div class="flex space-x-4">
            <EnhancedButton
              @click="showCreateModal = true"
              variant="primary"
              size="lg"
              class="shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <PlusIcon class="w-5 h-5 mr-2" />
              Nuevo Chatbot
            </EnhancedButton>
            <EnhancedButton
              @click="refreshChatbots"
              variant="secondary"
              size="lg"
              :loading="isLoading"
            >
              <ArrowPathIcon class="w-5 h-5 mr-2" />
              Actualizar
            </EnhancedButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-soft border border-white/20">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div class="flex-1 max-w-lg">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar chatbots..."
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
              />
            </div>
          </div>
          <div class="flex space-x-4">
            <select
              v-model="selectedStatus"
              class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            >
              <option value="">Todos los estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
              <option value="training">En entrenamiento</option>
            </select>
            <select
              v-model="selectedCategory"
              class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            >
              <option value="">Todas las categorías</option>
              <option value="customer-service">Atención al Cliente</option>
              <option value="sales">Ventas</option>
              <option value="support">Soporte Técnico</option>
              <option value="general">General</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Chatbots Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="animate-pulse">
          <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 h-64">
            <div class="h-4 bg-gray-300 rounded w-3/4 mb-4"></div>
            <div class="h-3 bg-gray-300 rounded w-1/2 mb-6"></div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-300 rounded"></div>
              <div class="h-3 bg-gray-300 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="filteredChatbots.length === 0" class="text-center py-12">
        <ChatBubbleLeftRightIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">No hay chatbots</h3>
        <p class="mt-2 text-gray-500">Comienza creando tu primer chatbot</p>
        <EnhancedButton
          @click="showCreateModal = true"
          variant="primary"
          class="mt-4"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Crear Chatbot
        </EnhancedButton>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-slide-up">
        <EnhancedCard
          v-for="chatbot in filteredChatbots"
          :key="chatbot.id"
          variant="glass"
          shadow="soft"
          :animated="true"
          class="group hover:shadow-glow transition-all duration-300 cursor-pointer"
          @click="openChatbot(chatbot.id)"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div :class="[
                  'w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-lg',
                  getStatusColor(chatbot.status)
                ]">
                  {{ chatbot.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                    {{ chatbot.name }}
                  </h3>
                  <p class="text-sm text-gray-500">{{ chatbot.category }}</p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span :class="[
                  'px-2 py-1 text-xs font-medium rounded-full',
                  getStatusBadgeColor(chatbot.status)
                ]">
                  {{ getStatusText(chatbot.status) }}
                </span>
                <button
                  @click.stop="toggleChatbotMenu(chatbot.id)"
                  class="p-1 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <EllipsisVerticalIcon class="w-5 h-5 text-gray-400" />
                </button>
              </div>
            </div>
          </template>

          <template #body>
            <div class="space-y-4">
              <p class="text-gray-600 text-sm line-clamp-2">{{ chatbot.description }}</p>
              
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                  <div class="text-2xl font-bold text-primary-600">{{ chatbot.conversations }}</div>
                  <div class="text-xs text-gray-500">Conversaciones</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-bold text-green-600">{{ chatbot.accuracy }}%</div>
                  <div class="text-xs text-gray-500">Precisión</div>
                </div>
              </div>

              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Entrenamiento</span>
                  <span class="font-medium">{{ chatbot.training_progress }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-500 h-2 rounded-full transition-all duration-1000"
                    :style="{ width: `${chatbot.training_progress}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </template>

          <template #footer>
            <div class="flex items-center justify-between pt-4 border-t border-gray-200">
              <div class="text-xs text-gray-500">
                Actualizado {{ formatTimeAgo(chatbot.updated_at) }}
              </div>
              <div class="flex space-x-2">
                <button
                  @click.stop="testChatbot(chatbot.id)"
                  class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-300"
                  title="Probar chatbot"
                >
                  <PlayIcon class="w-4 h-4" />
                </button>
                <button
                  @click.stop="editChatbot(chatbot.id)"
                  class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300"
                  title="Editar chatbot"
                >
                  <PencilIcon class="w-4 h-4" />
                </button>
                <button
                  @click.stop="duplicateChatbot(chatbot.id)"
                  class="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-all duration-300"
                  title="Duplicar chatbot"
                >
                  <DocumentDuplicateIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>
    </div>

    <!-- Create Chatbot Modal -->
    <EnhancedModal
      v-model="showCreateModal"
      title="Crear Nuevo Chatbot"
      size="lg"
    >
      <CreateChatbotForm
        @created="handleChatbotCreated"
        @cancel="showCreateModal = false"
      />
    </EnhancedModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  ChatBubbleLeftRightIcon,
  EllipsisVerticalIcon,
  PlayIcon,
  PencilIcon,
  DocumentDuplicateIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'
import EnhancedCard from '@/components/ui/EnhancedCard.vue'
import EnhancedButton from '@/components/ui/EnhancedButton.vue'
import EnhancedModal from '@/components/ui/EnhancedModal.vue'
import CreateChatbotForm from '@/components/chatbots/CreateChatbotForm.vue'

const router = useRouter()

// Estado reactivo
const isLoading = ref(false)
const showCreateModal = ref(false)
const searchQuery = ref('')
const selectedStatus = ref('')
const selectedCategory = ref('')
const chatbots = ref([])

// Datos de ejemplo
const mockChatbots = [
  {
    id: 1,
    name: 'Asistente de Ventas',
    description: 'Chatbot especializado en atención al cliente y ventas. Ayuda a los usuarios con consultas sobre productos y servicios.',
    status: 'active',
    category: 'sales',
    conversations: 1247,
    accuracy: 94,
    training_progress: 100,
    updated_at: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 horas atrás
  },
  {
    id: 2,
    name: 'Soporte Técnico',
    description: 'Asistente para resolver problemas técnicos y guiar a los usuarios en el uso de la plataforma.',
    status: 'active',
    category: 'support',
    conversations: 856,
    accuracy: 89,
    training_progress: 100,
    updated_at: new Date(Date.now() - 5 * 60 * 60 * 1000) // 5 horas atrás
  },
  {
    id: 3,
    name: 'Asistente General',
    description: 'Chatbot de propósito general para consultas básicas y direccionamiento de usuarios.',
    status: 'training',
    category: 'general',
    conversations: 234,
    accuracy: 76,
    training_progress: 65,
    updated_at: new Date(Date.now() - 30 * 60 * 1000) // 30 minutos atrás
  },
  {
    id: 4,
    name: 'Atención al Cliente',
    description: 'Especializado en resolver dudas sobre facturación, cuentas y servicios al cliente.',
    status: 'inactive',
    category: 'customer-service',
    conversations: 2103,
    accuracy: 92,
    training_progress: 100,
    updated_at: new Date(Date.now() - 24 * 60 * 60 * 1000) // 1 día atrás
  }
]

// Computed properties
const filteredChatbots = computed(() => {
  let filtered = chatbots.value

  if (searchQuery.value) {
    filtered = filtered.filter(chatbot => 
      chatbot.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      chatbot.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(chatbot => chatbot.status === selectedStatus.value)
  }

  if (selectedCategory.value) {
    filtered = filtered.filter(chatbot => chatbot.category === selectedCategory.value)
  }

  return filtered
})

// Métodos
const refreshChatbots = async () => {
  isLoading.value = true
  try {
    // Simular llamada a la API
    await new Promise(resolve => setTimeout(resolve, 1000))
    chatbots.value = [...mockChatbots]
  } catch (error) {
    console.error('Error al cargar chatbots:', error)
  } finally {
    isLoading.value = false
  }
}

const openChatbot = (chatbotId) => {
  router.push(`/chatbots/${chatbotId}`)
}

const testChatbot = (chatbotId) => {
  router.push(`/chat?bot=${chatbotId}`)
}

const editChatbot = (chatbotId) => {
  router.push(`/chatbots/${chatbotId}/edit`)
}

const duplicateChatbot = async (chatbotId) => {
  try {
    // Simular duplicación
    const originalBot = chatbots.value.find(bot => bot.id === chatbotId)
    if (originalBot) {
      const newBot = {
        ...originalBot,
        id: Date.now(),
        name: `${originalBot.name} (Copia)`,
        status: 'inactive',
        conversations: 0,
        training_progress: 0
      }
      chatbots.value.push(newBot)
    }
  } catch (error) {
    console.error('Error al duplicar chatbot:', error)
  }
}

const toggleChatbotMenu = (chatbotId) => {
  // Implementar menú contextual
  console.log('Toggle menu for chatbot:', chatbotId)
}

const handleChatbotCreated = (newChatbot) => {
  chatbots.value.unshift(newChatbot)
  showCreateModal.value = false
}

// Utilidades
const getStatusColor = (status) => {
  const colors = {
    active: 'bg-green-500',
    inactive: 'bg-gray-500',
    training: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusBadgeColor = (status) => {
  const colors = {
    active: 'bg-green-100 text-green-800',
    inactive: 'bg-gray-100 text-gray-800',
    training: 'bg-yellow-100 text-yellow-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    active: 'Activo',
    inactive: 'Inactivo',
    training: 'Entrenando'
  }
  return texts[status] || 'Desconocido'
}

const formatTimeAgo = (date) => {
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (days > 0) return `hace ${days} día${days > 1 ? 's' : ''}`
  if (hours > 0) return `hace ${hours} hora${hours > 1 ? 's' : ''}`
  if (minutes > 0) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  return 'hace un momento'
}

// Lifecycle
onMounted(() => {
  refreshChatbots()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>