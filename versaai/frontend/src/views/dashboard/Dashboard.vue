<template>
<div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100">
  <!-- Header -->
  <div class="glass border-b border-white/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-6">
        <div class="animate-fade-in">
          <h1 class="text-3xl font-bold text-gradient bg-gradient-primary bg-clip-text">
            Dashboard VersaAI
          </h1>
          <p class="mt-1 text-sm text-gray-600 animate-slide-up">
            Bienvenido de vuelta, gestiona tu asistente de IA
          </p>
        </div>
        <div class="flex items-center space-x-4 animate-fade-in">
          <EnhancedButton 
            variant="gradient" 
            size="md" 
            animation="glow"
            @click="startNewConversation"
          >
            Nueva Conversación
          </EnhancedButton>
          <EnhancedButton 
            variant="ghost" 
            size="md" 
            @click="openSettings"
          >
            Configuración
          </EnhancedButton>
        </div>
      </div>
    </div>
  </div>

  <div class="dashboard space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Stats Header -->
    <div class="glass-card rounded-xl p-8 text-white bg-gradient-primary animate-fade-in">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-2xl font-bold">Panel de Control</h2>
          <p class="mt-2 text-white/80">Resumen de tu actividad</p>
        </div>
        <div class="hidden md:block">
          <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4">
            <div class="text-sm text-white/70">Última actualización</div>
            <div class="text-lg font-semibold">{{ lastUpdated }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="dashboardStore.isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <!-- Stats Grid with enhanced interactivity -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-slide-up">
      <EnhancedCard 
        v-for="(stat, key) in dashboardStore.formattedStats" 
        :key="key"
        variant="stat"
        shadow="soft"
        :animated="true"
        class="stat-card hover:shadow-glow transition-all duration-300 cursor-pointer group"
        @click="navigateToSection(key)"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div :class="[
              'flex-shrink-0 p-4 rounded-xl transition-all duration-300 group-hover:scale-110',
              stat.color === 'blue' ? 'bg-blue-100 text-blue-600 group-hover:bg-blue-200' :
              stat.color === 'green' ? 'bg-green-100 text-green-600 group-hover:bg-green-200' :
              stat.color === 'purple' ? 'bg-purple-100 text-purple-600 group-hover:bg-purple-200' :
              'bg-orange-100 text-orange-600 group-hover:bg-orange-200'
            ]">
              <component :is="getIcon(stat.icon)" class="h-8 w-8" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500 group-hover:text-gray-700 transition-colors">{{ stat.label }}</p>
              <p class="text-3xl font-bold text-gray-900 mt-2 group-hover:text-primary-600 transition-colors">{{ stat.value }}</p>
              <div class="mt-2">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    :class="[
                      'h-2 rounded-full transition-all duration-1000',
                      stat.color === 'blue' ? 'bg-blue-500' :
                      stat.color === 'green' ? 'bg-green-500' :
                      stat.color === 'purple' ? 'bg-purple-500' :
                      'bg-orange-500'
                    ]"
                    :style="{ width: getProgressWidth(stat.value) }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm text-success-600 flex items-center group-hover:text-success-700 transition-colors">
              <ArrowTrendingUpIcon class="w-4 h-4 mr-1" />
              +{{ getGrowthPercentage(key) }}%
            </div>
            <div class="text-xs text-gray-400 mt-1 group-hover:text-gray-500 transition-colors">vs mes anterior</div>
            <ChevronRightIcon class="w-4 h-4 text-gray-400 mt-2 group-hover:text-primary-600 group-hover:translate-x-1 transition-all duration-300" />
          </div>
        </div>
      </EnhancedCard>
    </div>

    <!-- Recent Activity with enhanced design -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Conversations -->
      <EnhancedCard 
        title="Conversaciones Recientes"
        shadow="soft"
        class="animate-fade-in"
      >
        <template #actions>
          <EnhancedButton 
            variant="link" 
            size="sm"
            @click="viewAllConversations"
          >
            Ver todas
          </EnhancedButton>
        </template>
        
        <div class="space-y-4">
          <div 
            v-for="conversation in dashboardStore.recentConversations.slice(0, 5)" 
            :key="conversation.id"
            class="glass-light rounded-xl p-4 hover:shadow-soft transition-all duration-300 cursor-pointer group"
            @click="openConversation(conversation.id)"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-soft">
                  <ChatBubbleLeftRightIcon class="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{{ conversation.chatbot_name || 'Chatbot' }}</h3>
                  <p class="text-sm text-gray-600 mt-1">{{ conversation.last_message || 'Nueva conversación iniciada' }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-500">{{ formatTimeAgo(conversation.created_at) }}</p>
                <div class="flex items-center justify-end mt-2">
                  <span class="badge" 
                        :class="conversation.status === 'active' ? 'badge-success' : 'badge-secondary'">
                    {{ conversation.status === 'active' ? 'Activa' : 'Finalizada' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <template #footer>
          <router-link 
            to="/dashboard/conversations" 
            class="text-sm font-medium text-primary-600 hover:text-primary-700 flex items-center"
          >
            Ver todas las conversaciones
            <ChevronRightIcon class="ml-1 h-4 w-4" />
          </router-link>
        </template>
      </EnhancedCard>

      <!-- Quick Actions with enhanced design -->
      <EnhancedCard 
        title="Acciones Rápidas"
        subtitle="Accesos directos a funciones principales"
        shadow="soft"
        class="animate-fade-in"
      >
        <div class="space-y-4">
          <router-link
            to="/dashboard/chatbots/new"
            class="glass-light rounded-xl p-4 hover:shadow-soft transition-all duration-300 cursor-pointer group border border-gray-100 hover:border-primary-200 flex items-center"
          >
            <div class="flex items-center justify-between w-full">
              <div class="flex items-center space-x-4">
                <div class="p-3 rounded-xl shadow-soft transition-all duration-300 bg-gradient-to-br from-blue-400 to-blue-600 text-white group-hover:shadow-glow">
                  <PlusIcon class="h-6 w-6" />
                </div>
                <div class="text-left">
                  <p class="font-semibold text-gray-900 group-hover:text-primary-700 transition-colors">Crear Nuevo Chatbot</p>
                  <p class="text-sm text-gray-600 mt-1">Configura un chatbot en minutos</p>
                </div>
              </div>
              <div class="flex items-center">
                <ChevronRightIcon class="h-5 w-5 text-gray-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all duration-300" />
              </div>
            </div>
          </router-link>

          <router-link
            to="/dashboard/knowledge-bases/new"
            class="glass-light rounded-xl p-4 hover:shadow-soft transition-all duration-300 cursor-pointer group border border-gray-100 hover:border-green-200 flex items-center"
          >
            <div class="flex items-center justify-between w-full">
              <div class="flex items-center space-x-4">
                <div class="p-3 rounded-xl shadow-soft transition-all duration-300 bg-gradient-to-br from-green-400 to-green-600 text-white group-hover:shadow-glow">
                  <DocumentPlusIcon class="h-6 w-6" />
                </div>
                <div class="text-left">
                  <p class="font-semibold text-gray-900 group-hover:text-green-700 transition-colors">Subir Documentos</p>
                  <p class="text-sm text-gray-600 mt-1">Añade conocimiento a tus chatbots</p>
                </div>
              </div>
              <div class="flex items-center">
                <ChevronRightIcon class="h-5 w-5 text-gray-400 group-hover:text-green-600 group-hover:translate-x-1 transition-all duration-300" />
              </div>
            </div>
          </router-link>

          <router-link
            to="/dashboard/analytics"
            class="glass-light rounded-xl p-4 hover:shadow-soft transition-all duration-300 cursor-pointer group border border-gray-100 hover:border-purple-200 flex items-center"
          >
            <div class="flex items-center justify-between w-full">
              <div class="flex items-center space-x-4">
                <div class="p-3 rounded-xl shadow-soft transition-all duration-300 bg-gradient-to-br from-purple-400 to-purple-600 text-white group-hover:shadow-glow">
                  <ChartBarIcon class="h-6 w-6" />
                </div>
                <div class="text-left">
                  <p class="font-semibold text-gray-900 group-hover:text-purple-700 transition-colors">Ver Analytics</p>
                  <p class="text-sm text-gray-600 mt-1">Analiza el rendimiento detallado</p>
                </div>
              </div>
              <div class="flex items-center">
                <ChevronRightIcon class="h-5 w-5 text-gray-400 group-hover:text-purple-600 group-hover:translate-x-1 transition-all duration-300" />
              </div>
            </div>
          </router-link>
        </div>
      </EnhancedCard>
    </div>
  </div>
</div> <!-- ✅ Este es el cierre del div principal que faltaba -->
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboard'
import EnhancedCard from '@/components/ui/EnhancedCard.vue'
import EnhancedButton from '@/components/ui/EnhancedButton.vue'
import {
ChatBubbleLeftRightIcon,
UserGroupIcon,
CircleStackIcon,
ChartBarIcon,
PlusIcon,
DocumentPlusIcon,
ChevronRightIcon,
ArrowTrendingUpIcon,
EyeIcon,
CogIcon
} from '@heroicons/vue/24/outline'

// Router and Store
const router = useRouter()
const dashboardStore = useDashboardStore()

// Methods
const startNewConversation = () => {
router.push('/dashboard/conversations/new')
}

const openSettings = () => {
router.push('/dashboard/settings')
}

const viewAllConversations = () => {
router.push('/dashboard/conversations')
}

const openConversation = (id) => {
router.push(`/dashboard/conversations/${id}`)
}

// Navegación por secciones del dashboard
const navigateToSection = (section) => {
  const routes = {
    conversations: '/dashboard/conversations',
    users: '/dashboard/users',
    chatbots: '/dashboard/chatbots',
    tokens: '/dashboard/analytics'
  }
  if (routes[section]) {
    router.push(routes[section])
  }
}

// Cálculo de porcentajes de crecimiento
const getGrowthPercentage = (key) => {
  const growthData = {
    conversations: 15,
    users: 8,
    chatbots: 23,
    tokens: 12
  }
  return growthData[key] || 0
}

// Cálculo del ancho de la barra de progreso
const getProgressWidth = (value) => {
  const numValue = parseInt(value.toString().replace(/[^0-9]/g, '')) || 0
  const maxValues = {
    conversations: 1000,
    users: 500,
    chatbots: 50,
    tokens: 100000
  }
  const maxValue = Math.max(...Object.values(maxValues))
  return `${Math.min((numValue / maxValue) * 100, 100)}%`
}

// Computed properties
const lastUpdated = computed(() => {
const now = new Date()
return now.toLocaleString('es-ES', {
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit'
})
})

// Utility functions
const formatTimeAgo = (dateString) => {
if (!dateString) return 'Hace un momento'

const date = new Date(dateString)
const now = new Date()
const diffInSeconds = Math.floor((now - date) / 1000)

if (diffInSeconds < 60) return 'Hace un momento'
if (diffInSeconds < 3600) return `Hace ${Math.floor(diffInSeconds / 60)} minutos`
if (diffInSeconds < 86400) return `Hace ${Math.floor(diffInSeconds / 3600)} horas`
return `Hace ${Math.floor(diffInSeconds / 86400)} días`
}

const getIcon = (iconName) => {
const icons = {
  'chat': ChatBubbleLeftRightIcon,
  'users': UserGroupIcon,
  'conversations': ChatBubbleLeftRightIcon,
  'knowledge': CircleStackIcon
}
return icons[iconName] || ChatBubbleLeftRightIcon
}

// Load dashboard data
const loadDashboardData = async () => {
try {
  await dashboardStore.refreshAllData()
} catch (error) {
  console.error('Error loading dashboard data:', error)
}
}

onMounted(() => {
loadDashboardData()
})
</script>