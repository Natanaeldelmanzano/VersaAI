<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Dashboard
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          Bienvenido de vuelta, {{ authStore.user?.full_name }}
        </p>
      </div>
      <div class="mt-4 flex md:mt-0 md:ml-4 space-x-3">
        <!-- Role Switcher for Demo Mode -->
        <RoleSwitcher />
        
        <router-link
          to="/dashboard/chatbots/new"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PlusIcon class="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
          Nuevo Chatbot
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="stat in stats" :key="stat.name" class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <component :is="stat.icon" class="h-6 w-6 text-gray-400" aria-hidden="true" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ stat.name }}</dt>
                <dd>
                  <div class="text-lg font-medium text-gray-900">{{ stat.value }}</div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-5 py-3">
          <div class="text-sm">
            <span :class="[
              stat.change >= 0 ? 'text-green-600' : 'text-red-600',
              'font-medium'
            ]">
              {{ stat.change >= 0 ? '+' : '' }}{{ stat.change }}%
            </span>
            <span class="text-gray-500"> desde el mes pasado</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Messages Chart -->
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Mensajes por día</h3>
          <select id="messages-time-range" name="messages-time-range" v-model="messagesTimeRange" class="text-sm border-gray-300 rounded-md">
            <option value="7">Últimos 7 días</option>
            <option value="30">Últimos 30 días</option>
            <option value="90">Últimos 90 días</option>
          </select>
        </div>
        <div class="h-64">
          <Line :data="messagesChartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Chatbots Performance -->
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Rendimiento de Chatbots</h3>
        </div>
        <div class="h-64">
          <Doughnut :data="chatbotsChartData" :options="doughnutOptions" />
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Conversations -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Conversaciones Recientes</h3>
        </div>
        <div class="divide-y divide-gray-200">
          <div v-for="conversation in recentConversations" :key="conversation.id" class="px-6 py-4 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                    <ChatBubbleLeftRightIcon class="h-4 w-4 text-primary-600" />
                  </div>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">{{ conversation.chatbot_name }}</p>
                  <p class="text-sm text-gray-500">{{ conversation.last_message }}</p>
                </div>
              </div>
              <div class="text-sm text-gray-500">
                {{ formatDate(conversation.updated_at) }}
              </div>
            </div>
          </div>
        </div>
        <div class="px-6 py-3 bg-gray-50">
          <router-link to="/dashboard/conversations" class="text-sm font-medium text-primary-600 hover:text-primary-500">
            Ver todas las conversaciones →
          </router-link>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Acciones Rápidas</h3>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <router-link
              to="/dashboard/chatbots/new"
              class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              <PlusIcon class="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p class="text-sm font-medium text-gray-900">Crear Nuevo Chatbot</p>
                <p class="text-sm text-gray-500">Configura un chatbot en minutos</p>
              </div>
            </router-link>
            
            <router-link
              to="/dashboard/knowledge-bases/new"
              class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              <DocumentTextIcon class="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p class="text-sm font-medium text-gray-900">Subir Documentos</p>
                <p class="text-sm text-gray-500">Añade conocimiento a tus chatbots</p>
              </div>
            </router-link>
            
            <router-link
              to="/dashboard/analytics"
              class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              <ChartBarIcon class="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p class="text-sm font-medium text-gray-900">Ver Analytics</p>
                <p class="text-sm text-gray-500">Analiza el rendimiento detallado</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import {
  PlusIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  ChartBarIcon,
  UserGroupIcon,
  CpuChipIcon
} from '@heroicons/vue/24/outline'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'
import RoleSwitcher from '@/components/demo/RoleSwitcher.vue'
import api from '@/api'
import { formatDistanceToNow } from 'date-fns'
import { es } from 'date-fns/locale'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const authStore = useAuthStore()

const loading = ref(true)
const messagesTimeRange = ref('30')
const recentConversations = ref([])

const stats = ref([
  {
    name: 'Total Chatbots',
    value: '0',
    change: 0,
    icon: CpuChipIcon
  },
  {
    name: 'Mensajes Hoy',
    value: '0',
    change: 0,
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: 'Conversaciones Activas',
    value: '0',
    change: 0,
    icon: UserGroupIcon
  },
  {
    name: 'Documentos',
    value: '0',
    change: 0,
    icon: DocumentTextIcon
  }
])

const messagesChartData = computed(() => ({
  labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  datasets: [
    {
      label: 'Mensajes',
      data: [12, 19, 3, 5, 2, 3, 9],
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    }
  ]
}))

const chatbotsChartData = computed(() => ({
  labels: ['Activos', 'Inactivos', 'En Desarrollo'],
  datasets: [
    {
      data: [65, 25, 10],
      backgroundColor: [
        'rgb(34, 197, 94)',
        'rgb(239, 68, 68)',
        'rgb(245, 158, 11)'
      ],
      borderWidth: 0
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}

const formatDate = (date) => {
  return formatDistanceToNow(new Date(date), {
    addSuffix: true,
    locale: es
  })
}

const loadDashboardData = async () => {
  try {
    loading.value = true
    
    // Use dashboard store
    const dashboardStore = useDashboardStore()
    await dashboardStore.refreshAllData()
    
    // Update stats from store
    const storeStats = dashboardStore.formattedStats
    stats.value[0].value = storeStats.chatbots.value.toString()
    stats.value[1].value = dashboardStore.analytics.daily_conversations.reduce((sum, day) => sum + day.conversations, 0).toString()
    stats.value[2].value = storeStats.conversations.value.toString()
    stats.value[3].value = storeStats.knowledgeBases.value.toString()
    
    // Update changes (mock data for now)
    stats.value[0].change = Math.floor(Math.random() * 20) - 10
    stats.value[1].change = Math.floor(Math.random() * 30) - 15
    stats.value[2].change = Math.floor(Math.random() * 25) - 12
    stats.value[3].change = Math.floor(Math.random() * 15) - 7
    
    // Update recent conversations from store
    recentConversations.value = dashboardStore.recentConversations
    
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>