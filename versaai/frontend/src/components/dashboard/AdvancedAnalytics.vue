<template>
  <div class="advanced-analytics">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold text-gray-900">Analytics Avanzados</h2>
            <p class="text-sm text-gray-600 mt-1">Análisis profundo de comportamiento y rendimiento</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="refreshData"
              :disabled="loading"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <ArrowPathIcon :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
              Actualizar
            </button>
            <button
              @click="exportData"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <ArrowDownTrayIcon class="h-4 w-4 mr-2" />
              Exportar
            </button>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Período</label>
            <select v-model="filters.period" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              <option value="7d">Últimos 7 días</option>
              <option value="30d">Últimos 30 días</option>
              <option value="90d">Últimos 90 días</option>
              <option value="1y">Último año</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Segmento</label>
            <select v-model="filters.segment" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              <option value="all">Todos los usuarios</option>
              <option value="new">Usuarios nuevos</option>
              <option value="returning">Usuarios recurrentes</option>
              <option value="premium">Usuarios premium</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Canal</label>
            <select v-model="filters.channel" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              <option value="all">Todos los canales</option>
              <option value="web">Web</option>
              <option value="mobile">Móvil</option>
              <option value="api">API</option>
              <option value="widget">Widget</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Métrica</label>
            <select v-model="filters.metric" class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
              <option value="engagement">Engagement</option>
              <option value="satisfaction">Satisfacción</option>
              <option value="conversion">Conversión</option>
              <option value="retention">Retención</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <ChartBarIcon class="h-5 w-5 text-blue-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Engagement Score</p>
            <p class="text-2xl font-semibold text-gray-900">{{ metrics.engagement }}%</p>
            <p class="text-sm text-green-600">+12% vs período anterior</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <FaceSmileIcon class="h-5 w-5 text-green-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Satisfacción</p>
            <p class="text-2xl font-semibold text-gray-900">{{ metrics.satisfaction }}/5</p>
            <p class="text-sm text-green-600">+0.3 vs período anterior</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <ArrowTrendingUpIcon class="h-5 w-5 text-purple-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Conversión</p>
            <p class="text-2xl font-semibold text-gray-900">{{ metrics.conversion }}%</p>
            <p class="text-sm text-green-600">+5.2% vs período anterior</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
              <UserGroupIcon class="h-5 w-5 text-orange-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Retención</p>
            <p class="text-2xl font-semibold text-gray-900">{{ metrics.retention }}%</p>
            <p class="text-sm text-red-600">-2.1% vs período anterior</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Sentiment Analysis -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Análisis de Sentimientos</h3>
          <p class="text-sm text-gray-600">Distribución de sentimientos en conversaciones</p>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <span class="text-sm font-medium text-gray-700">Positivo</span>
              </div>
              <span class="text-sm text-gray-900">{{ sentimentData.positive }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-green-500 h-2 rounded-full" :style="{ width: sentimentData.positive + '%' }"></div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                <span class="text-sm font-medium text-gray-700">Neutral</span>
              </div>
              <span class="text-sm text-gray-900">{{ sentimentData.neutral }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: sentimentData.neutral + '%' }"></div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-red-500 rounded-full mr-3"></div>
                <span class="text-sm font-medium text-gray-700">Negativo</span>
              </div>
              <span class="text-sm text-gray-900">{{ sentimentData.negative }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-red-500 h-2 rounded-full" :style="{ width: sentimentData.negative + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Segmentation -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Segmentación de Usuarios</h3>
          <p class="text-sm text-gray-600">Distribución por tipo de usuario</p>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center">
              <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <UserIcon class="h-8 w-8 text-blue-600" />
              </div>
              <p class="text-2xl font-semibold text-gray-900">{{ segmentData.new }}</p>
              <p class="text-sm text-gray-600">Nuevos</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <ArrowPathIcon class="h-8 w-8 text-green-600" />
              </div>
              <p class="text-2xl font-semibold text-gray-900">{{ segmentData.returning }}</p>
              <p class="text-sm text-gray-600">Recurrentes</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <StarIcon class="h-8 w-8 text-purple-600" />
              </div>
              <p class="text-2xl font-semibold text-gray-900">{{ segmentData.premium }}</p>
              <p class="text-sm text-gray-600">Premium</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-2">
                <ClockIcon class="h-8 w-8 text-gray-600" />
              </div>
              <p class="text-2xl font-semibold text-gray-900">{{ segmentData.inactive }}</p>
              <p class="text-sm text-gray-600">Inactivos</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Heatmap and Funnel -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Interaction Heatmap -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Mapa de Calor de Interacciones</h3>
          <p class="text-sm text-gray-600">Actividad por hora del día</p>
        </div>
        <div class="p-6">
          <HeatmapChart :data="heatmapData" />
        </div>
      </div>

      <!-- Conversion Funnel -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Embudo de Conversión</h3>
          <p class="text-sm text-gray-600">Flujo de usuarios a través del proceso</p>
        </div>
        <div class="p-6">
          <FunnelChart :data="funnelData" />
        </div>
      </div>
    </div>

    <!-- Predictive Analytics -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Análisis Predictivo</h3>
        <p class="text-sm text-gray-600">Proyecciones basadas en tendencias actuales</p>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <TrendingUpIcon class="h-6 w-6 text-blue-600" />
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-2">Crecimiento Proyectado</h4>
            <p class="text-3xl font-bold text-blue-600 mb-1">+{{ predictions.growth }}%</p>
            <p class="text-sm text-gray-600">Próximos 30 días</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <CurrencyDollarIcon class="h-6 w-6 text-green-600" />
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-2">Revenue Estimado</h4>
            <p class="text-3xl font-bold text-green-600 mb-1">${{ predictions.revenue }}</p>
            <p class="text-sm text-gray-600">Próximos 30 días</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <ExclamationTriangleIcon class="h-6 w-6 text-orange-600" />
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-2">Riesgo de Churn</h4>
            <p class="text-3xl font-bold text-orange-600 mb-1">{{ predictions.churnRisk }}%</p>
            <p class="text-sm text-gray-600">Usuarios en riesgo</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import {
  ArrowPathIcon,
  ArrowDownTrayIcon,
  ChartBarIcon,
  FaceSmileIcon,
  ArrowTrendingUpIcon,
  UserGroupIcon,
  UserIcon,
  StarIcon,
  ClockIcon,
  TrendingUpIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import HeatmapChart from './charts/HeatmapChart.vue'
import FunnelChart from './charts/FunnelChart.vue'

// Reactive data
const loading = ref(false)

const filters = reactive({
  period: '30d',
  segment: 'all',
  channel: 'all',
  metric: 'engagement'
})

const metrics = reactive({
  engagement: 78,
  satisfaction: 4.2,
  conversion: 12.5,
  retention: 85
})

const sentimentData = reactive({
  positive: 65,
  neutral: 25,
  negative: 10
})

const segmentData = reactive({
  new: 1250,
  returning: 3420,
  premium: 890,
  inactive: 340
})

const predictions = reactive({
  growth: 15,
  revenue: '45,200',
  churnRisk: 8
})

const heatmapData = ref([])
const funnelData = ref([])

// Methods
const refreshData = async () => {
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    await loadAnalyticsData()
  } catch (error) {
    console.error('Error refreshing data:', error)
  } finally {
    loading.value = false
  }
}

const exportData = () => {
  // Simulate export functionality
  const data = {
    metrics: metrics,
    sentiment: sentimentData,
    segments: segmentData,
    predictions: predictions,
    exportDate: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `advanced-analytics-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const loadAnalyticsData = async () => {
  // Generate sample heatmap data
  const hours = Array.from({ length: 24 }, (_, i) => i)
  const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
  
  heatmapData.value = days.map(day => 
    hours.map(hour => ({
      day,
      hour,
      value: Math.floor(Math.random() * 100)
    }))
  ).flat()

  // Generate sample funnel data
  funnelData.value = [
    { stage: 'Visitantes', value: 10000, percentage: 100 },
    { stage: 'Interacciones', value: 7500, percentage: 75 },
    { stage: 'Conversaciones', value: 5000, percentage: 50 },
    { stage: 'Leads', value: 2500, percentage: 25 },
    { stage: 'Conversiones', value: 1250, percentage: 12.5 }
  ]
}

// Watch for filter changes
watch(filters, () => {
  loadAnalyticsData()
}, { deep: true })

// Lifecycle
onMounted(() => {
  loadAnalyticsData()
})
</script>

<style scoped>
.advanced-analytics {
  @apply space-y-6;
}
</style>