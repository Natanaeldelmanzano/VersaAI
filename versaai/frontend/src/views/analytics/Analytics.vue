<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Analytics & Reportes</h1>
            <p class="mt-2 text-gray-600">Análisis detallado del rendimiento de tus chatbots</p>
          </div>
          <div class="flex space-x-4">
            <EnhancedButton
              @click="exportData"
              variant="secondary"
              size="lg"
            >
              <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
              Exportar
            </EnhancedButton>
            <EnhancedButton
              @click="refreshData"
              variant="primary"
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

    <!-- Filters Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-6 shadow-soft border border-white/20">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
            <select
              v-model="selectedPeriod"
              @change="updateData"
              class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            >
              <option value="7d">Últimos 7 días</option>
              <option value="30d">Últimos 30 días</option>
              <option value="90d">Últimos 90 días</option>
              <option value="1y">Último año</option>
            </select>
            <select
              v-model="selectedChatbot"
              @change="updateData"
              class="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            >
              <option value="">Todos los chatbots</option>
              <option value="1">Asistente de Ventas</option>
              <option value="2">Soporte Técnico</option>
              <option value="3">Asistente General</option>
              <option value="4">Atención al Cliente</option>
            </select>
          </div>
          <div class="flex items-center space-x-2">
            <CalendarIcon class="w-5 h-5 text-gray-400" />
            <span class="text-sm text-gray-600">Última actualización: {{ lastUpdated }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <EnhancedCard
          v-for="kpi in kpiData"
          :key="kpi.id"
          variant="stat"
          shadow="soft"
          :animated="true"
          class="group hover:shadow-glow transition-all duration-300"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div :class="[
                'flex-shrink-0 p-4 rounded-xl transition-all duration-300 group-hover:scale-110',
                kpi.color
              ]">
                <component :is="kpi.icon" class="h-8 w-8" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500 group-hover:text-gray-700 transition-colors">{{ kpi.label }}</p>
                <p class="text-3xl font-bold text-gray-900 mt-2 group-hover:text-primary-600 transition-colors">{{ kpi.value }}</p>
                <div class="flex items-center mt-2">
                  <component 
                    :is="kpi.trend === 'up' ? ArrowTrendingUpIcon : ArrowTrendingDownIcon" 
                    :class="[
                      'w-4 h-4 mr-1',
                      kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    ]"
                  />
                  <span :class="[
                    'text-sm font-medium',
                    kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'
                  ]">
                    {{ kpi.change }}%
                  </span>
                  <span class="text-sm text-gray-500 ml-1">vs período anterior</span>
                </div>
              </div>
            </div>
          </div>
        </EnhancedCard>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Conversaciones por Día -->
        <EnhancedCard
          variant="glass"
          shadow="soft"
          class="p-6"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Conversaciones por Día</h3>
              <ChartBarIcon class="w-6 h-6 text-gray-400" />
            </div>
          </template>
          <template #body>
            <div class="h-64 flex items-end justify-between space-x-2 mt-4">
              <div 
                v-for="(day, index) in conversationChart"
                :key="index"
                class="flex-1 bg-gradient-to-t from-primary-500 to-primary-300 rounded-t-lg transition-all duration-500 hover:from-primary-600 hover:to-primary-400 cursor-pointer group relative"
                :style="{ height: `${(day.value / Math.max(...conversationChart.map(d => d.value))) * 100}%` }"
                :title="`${day.label}: ${day.value} conversaciones`"
              >
                <div class="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                  {{ day.value }}
                </div>
              </div>
            </div>
            <div class="flex justify-between mt-4 text-xs text-gray-500">
              <span v-for="(day, index) in conversationChart" :key="index">
                {{ day.label }}
              </span>
            </div>
          </template>
        </EnhancedCard>

        <!-- Distribución por Chatbot -->
        <EnhancedCard
          variant="glass"
          shadow="soft"
          class="p-6"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Distribución por Chatbot</h3>
              <ChartPieIcon class="w-6 h-6 text-gray-400" />
            </div>
          </template>
          <template #body>
            <div class="mt-4">
              <div class="space-y-4">
                <div 
                  v-for="(bot, index) in chatbotDistribution"
                  :key="index"
                  class="flex items-center justify-between"
                >
                  <div class="flex items-center space-x-3">
                    <div 
                      :class="[
                        'w-4 h-4 rounded-full',
                        bot.color
                      ]"
                    ></div>
                    <span class="text-sm font-medium text-gray-700">{{ bot.name }}</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-24 bg-gray-200 rounded-full h-2">
                      <div 
                        :class="[
                          'h-2 rounded-full transition-all duration-1000',
                          bot.color.replace('bg-', 'bg-')
                        ]"
                        :style="{ width: `${bot.percentage}%` }"
                      ></div>
                    </div>
                    <span class="text-sm font-bold text-gray-900 w-12 text-right">{{ bot.percentage }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>
    </div>

    <!-- Detailed Analytics -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Métricas de Satisfacción -->
        <EnhancedCard
          variant="glass"
          shadow="soft"
          class="p-6"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Satisfacción del Usuario</h3>
              <FaceSmileIcon class="w-6 h-6 text-gray-400" />
            </div>
          </template>
          <template #body>
            <div class="mt-4 space-y-4">
              <div class="text-center">
                <div class="text-4xl font-bold text-green-600">4.7</div>
                <div class="text-sm text-gray-500">Puntuación promedio</div>
                <div class="flex justify-center mt-2">
                  <div class="flex space-x-1">
                    <StarIcon v-for="i in 5" :key="i" class="w-5 h-5 text-yellow-400 fill-current" />
                  </div>
                </div>
              </div>
              <div class="space-y-2">
                <div v-for="(rating, index) in satisfactionData" :key="index" class="flex items-center space-x-2">
                  <span class="text-sm w-8">{{ rating.stars }}★</span>
                  <div class="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      class="bg-yellow-400 h-2 rounded-full transition-all duration-1000"
                      :style="{ width: `${rating.percentage}%` }"
                    ></div>
                  </div>
                  <span class="text-sm text-gray-600 w-12 text-right">{{ rating.percentage }}%</span>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>

        <!-- Tiempo de Respuesta -->
        <EnhancedCard
          variant="glass"
          shadow="soft"
          class="p-6"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Tiempo de Respuesta</h3>
              <ClockIcon class="w-6 h-6 text-gray-400" />
            </div>
          </template>
          <template #body>
            <div class="mt-4 space-y-4">
              <div class="text-center">
                <div class="text-4xl font-bold text-blue-600">1.2s</div>
                <div class="text-sm text-gray-500">Tiempo promedio</div>
              </div>
              <div class="space-y-3">
                <div v-for="metric in responseTimeMetrics" :key="metric.label" class="flex justify-between">
                  <span class="text-sm text-gray-600">{{ metric.label }}</span>
                  <span class="text-sm font-medium text-gray-900">{{ metric.value }}</span>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>

        <!-- Temas Más Consultados -->
        <EnhancedCard
          variant="glass"
          shadow="soft"
          class="p-6"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Temas Populares</h3>
              <HashtagIcon class="w-6 h-6 text-gray-400" />
            </div>
          </template>
          <template #body>
            <div class="mt-4 space-y-3">
              <div 
                v-for="(topic, index) in popularTopics"
                :key="index"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-primary-100 text-primary-600 rounded-lg flex items-center justify-center text-sm font-bold">
                    {{ index + 1 }}
                  </div>
                  <span class="text-sm font-medium text-gray-900">{{ topic.name }}</span>
                </div>
                <div class="text-right">
                  <div class="text-sm font-bold text-gray-900">{{ topic.count }}</div>
                  <div class="text-xs text-gray-500">consultas</div>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  ArrowDownTrayIcon,
  ArrowPathIcon,
  CalendarIcon,
  ChartBarIcon,
  ChartPieIcon,
  FaceSmileIcon,
  ClockIcon,
  HashtagIcon,
  StarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  EyeIcon,
  CpuChipIcon
} from '@heroicons/vue/24/outline'
import EnhancedCard from '@/components/ui/EnhancedCard.vue'
import EnhancedButton from '@/components/ui/EnhancedButton.vue'

// Estado reactivo
const isLoading = ref(false)
const selectedPeriod = ref('30d')
const selectedChatbot = ref('')
const lastUpdated = ref(new Date().toLocaleString())

// Datos de KPIs
const kpiData = ref([
  {
    id: 1,
    label: 'Total Conversaciones',
    value: '12,847',
    change: 15.3,
    trend: 'up',
    icon: ChatBubbleLeftRightIcon,
    color: 'bg-blue-100 text-blue-600'
  },
  {
    id: 2,
    label: 'Usuarios Activos',
    value: '3,421',
    change: 8.7,
    trend: 'up',
    icon: UserGroupIcon,
    color: 'bg-green-100 text-green-600'
  },
  {
    id: 3,
    label: 'Tasa de Resolución',
    value: '94.2%',
    change: 2.1,
    trend: 'up',
    icon: EyeIcon,
    color: 'bg-purple-100 text-purple-600'
  },
  {
    id: 4,
    label: 'Tokens Procesados',
    value: '2.1M',
    change: -3.2,
    trend: 'down',
    icon: CpuChipIcon,
    color: 'bg-orange-100 text-orange-600'
  }
])

// Datos del gráfico de conversaciones
const conversationChart = ref([
  { label: 'Lun', value: 245 },
  { label: 'Mar', value: 312 },
  { label: 'Mié', value: 189 },
  { label: 'Jue', value: 421 },
  { label: 'Vie', value: 387 },
  { label: 'Sáb', value: 156 },
  { label: 'Dom', value: 98 }
])

// Distribución por chatbot
const chatbotDistribution = ref([
  { name: 'Asistente de Ventas', percentage: 45, color: 'bg-blue-500' },
  { name: 'Soporte Técnico', percentage: 28, color: 'bg-green-500' },
  { name: 'Atención al Cliente', percentage: 18, color: 'bg-purple-500' },
  { name: 'Asistente General', percentage: 9, color: 'bg-orange-500' }
])

// Datos de satisfacción
const satisfactionData = ref([
  { stars: 5, percentage: 68 },
  { stars: 4, percentage: 22 },
  { stars: 3, percentage: 7 },
  { stars: 2, percentage: 2 },
  { stars: 1, percentage: 1 }
])

// Métricas de tiempo de respuesta
const responseTimeMetrics = ref([
  { label: 'Tiempo mínimo', value: '0.3s' },
  { label: 'Tiempo máximo', value: '4.2s' },
  { label: 'Percentil 95', value: '2.1s' },
  { label: 'Mediana', value: '1.0s' }
])

// Temas populares
const popularTopics = ref([
  { name: 'Información de productos', count: 1247 },
  { name: 'Soporte técnico', count: 892 },
  { name: 'Facturación', count: 634 },
  { name: 'Devoluciones', count: 421 },
  { name: 'Horarios de atención', count: 312 }
])

// Métodos
const refreshData = async () => {
  isLoading.value = true
  try {
    // Simular carga de datos
    await new Promise(resolve => setTimeout(resolve, 1500))
    lastUpdated.value = new Date().toLocaleString()
  } catch (error) {
    console.error('Error al actualizar datos:', error)
  } finally {
    isLoading.value = false
  }
}

const updateData = () => {
  // Actualizar datos basado en filtros
  console.log('Actualizando datos para:', selectedPeriod.value, selectedChatbot.value)
}

const exportData = () => {
  // Implementar exportación de datos
  console.log('Exportando datos...')
  // Aquí iría la lógica para generar y descargar un archivo CSV/PDF
}

// Lifecycle
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
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