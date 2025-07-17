<template>
  <div class="executive-reports">
    <!-- Header con controles -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Reportes Ejecutivos</h2>
        <p class="text-gray-600 mt-2">Análisis completo del rendimiento empresarial</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Selector de período -->
        <select 
          v-model="selectedPeriod" 
          @change="refreshReports"
          class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          <option value="7d">Últimos 7 días</option>
          <option value="30d">Últimos 30 días</option>
          <option value="90d">Últimos 90 días</option>
          <option value="1y">Último año</option>
          <option value="custom">Período personalizado</option>
        </select>
        
        <!-- Selector de comparación -->
        <select 
          v-model="comparisonPeriod"
          class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          <option value="previous">Período anterior</option>
          <option value="year_ago">Mismo período año anterior</option>
          <option value="none">Sin comparación</option>
        </select>
        
        <!-- Botones de acción -->
        <button
          @click="exportToPDF"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          <DocumentArrowDownIcon class="w-4 h-4 mr-2" />
          PDF
        </button>
        
        <button
          @click="exportToExcel"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          <TableCellsIcon class="w-4 h-4 mr-2" />
          Excel
        </button>
        
        <button
          @click="refreshReports"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
        >
          <ArrowPathIcon :class="['w-4 h-4 mr-2', { 'animate-spin': isLoading }]" />
          Actualizar
        </button>
      </div>
    </div>

    <!-- Selector de fecha personalizado -->
    <div v-if="selectedPeriod === 'custom'" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Período Personalizado</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Fecha de inicio</label>
          <input
            v-model="customDateRange.start"
            type="date"
            class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Fecha de fin</label>
          <input
            v-model="customDateRange.end"
            type="date"
            class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          />
        </div>
      </div>
      <button
        @click="applyCustomRange"
        class="mt-4 inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
      >
        Aplicar Período
      </button>
    </div>

    <!-- KPIs Ejecutivos -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div 
        v-for="kpi in executiveKPIs" 
        :key="kpi.key"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">{{ kpi.title }}</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ kpi.value }}</p>
            <div class="flex items-center mt-2">
              <span 
                :class="[
                  'inline-flex items-center text-sm font-medium',
                  kpi.trend === 'up' ? 'text-green-600' : kpi.trend === 'down' ? 'text-red-600' : 'text-gray-600'
                ]"
              >
                <ArrowUpIcon v-if="kpi.trend === 'up'" class="w-4 h-4 mr-1" />
                <ArrowDownIcon v-if="kpi.trend === 'down'" class="w-4 h-4 mr-1" />
                <MinusIcon v-if="kpi.trend === 'neutral'" class="w-4 h-4 mr-1" />
                {{ kpi.change }}
              </span>
              <span class="text-sm text-gray-500 ml-2">vs {{ comparisonLabel }}</span>
            </div>
          </div>
          <div :class="['w-12 h-12 rounded-lg flex items-center justify-center', kpi.bgColor]">
            <component :is="kpi.icon" :class="['w-6 h-6', kpi.iconColor]" />
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficos Ejecutivos -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Revenue Trend -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Tendencia de Ingresos</h3>
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-sm text-gray-600">Ingresos</span>
          </div>
        </div>
        <div class="h-80">
          <ExecutiveChart 
            :data="revenueData" 
            :loading="isLoading"
            type="line"
            :options="revenueChartOptions"
          />
        </div>
      </div>

      <!-- User Growth -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Crecimiento de Usuarios</h3>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Nuevos</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Activos</span>
            </div>
          </div>
        </div>
        <div class="h-80">
          <ExecutiveChart 
            :data="userGrowthData" 
            :loading="isLoading"
            type="bar"
            :options="userGrowthChartOptions"
          />
        </div>
      </div>
    </div>

    <!-- Métricas de Rendimiento -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Métricas de Rendimiento</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Satisfacción del Cliente -->
          <div class="text-center">
            <div class="relative w-32 h-32 mx-auto mb-4">
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-200"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  class="text-green-500"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${customerSatisfaction}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-900">{{ customerSatisfaction }}%</span>
              </div>
            </div>
            <h4 class="text-lg font-semibold text-gray-900">Satisfacción del Cliente</h4>
            <p class="text-sm text-gray-600 mt-1">Promedio de calificaciones</p>
          </div>

          <!-- Tiempo de Respuesta -->
          <div class="text-center">
            <div class="relative w-32 h-32 mx-auto mb-4">
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-200"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  class="text-blue-500"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${responseTimeScore}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-900">{{ averageResponseTime }}ms</span>
              </div>
            </div>
            <h4 class="text-lg font-semibold text-gray-900">Tiempo de Respuesta</h4>
            <p class="text-sm text-gray-600 mt-1">Promedio de respuesta</p>
          </div>

          <!-- Tasa de Resolución -->
          <div class="text-center">
            <div class="relative w-32 h-32 mx-auto mb-4">
              <svg class="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  class="text-gray-200"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  class="text-purple-500"
                  stroke="currentColor"
                  stroke-width="3"
                  fill="none"
                  stroke-linecap="round"
                  :stroke-dasharray="`${resolutionRate}, 100`"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-2xl font-bold text-gray-900">{{ resolutionRate }}%</span>
              </div>
            </div>
            <h4 class="text-lg font-semibold text-gray-900">Tasa de Resolución</h4>
            <p class="text-sm text-gray-600 mt-1">Conversaciones resueltas</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Insights -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Insights Ejecutivos</h3>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div 
            v-for="insight in topInsights" 
            :key="insight.id"
            class="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg"
          >
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center', insight.bgColor]">
              <component :is="insight.icon" :class="['w-4 h-4', insight.iconColor]" />
            </div>
            <div class="flex-1">
              <h4 class="text-sm font-semibold text-gray-900">{{ insight.title }}</h4>
              <p class="text-sm text-gray-600 mt-1">{{ insight.description }}</p>
              <div class="flex items-center mt-2">
                <span :class="['text-xs font-medium px-2 py-1 rounded-full', insight.badgeColor]">
                  {{ insight.impact }}
                </span>
                <span class="text-xs text-gray-500 ml-2">{{ insight.timeframe }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import { useDashboardStore } from '@/stores/dashboard'
import {
  DocumentArrowDownIcon,
  TableCellsIcon,
  ArrowPathIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MinusIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
  TrendingUpIcon
} from '@heroicons/vue/24/outline'
import ExecutiveChart from './charts/ExecutiveChart.vue'
import jsPDF from 'jspdf'
import * as XLSX from 'xlsx'

// Stores
const analyticsStore = useAnalyticsStore()
const dashboardStore = useDashboardStore()

// State
const isLoading = ref(false)
const selectedPeriod = ref('30d')
const comparisonPeriod = ref('previous')
const customDateRange = ref({
  start: '',
  end: ''
})

// Computed
const comparisonLabel = computed(() => {
  switch (comparisonPeriod.value) {
    case 'previous': return 'período anterior'
    case 'year_ago': return 'año anterior'
    default: return 'sin comparación'
  }
})

const executiveKPIs = computed(() => [
  {
    key: 'revenue',
    title: 'Ingresos Totales',
    value: '$' + (analyticsStore.overview.total_revenue || 0).toLocaleString(),
    change: '+12.5%',
    trend: 'up',
    icon: CurrencyDollarIcon,
    bgColor: 'bg-green-100',
    iconColor: 'text-green-600'
  },
  {
    key: 'users',
    title: 'Usuarios Activos',
    value: (analyticsStore.overview.active_users || 0).toLocaleString(),
    change: '+8.3%',
    trend: 'up',
    icon: UsersIcon,
    bgColor: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    key: 'conversations',
    title: 'Conversaciones',
    value: (analyticsStore.overview.total_conversations || 0).toLocaleString(),
    change: '+15.7%',
    trend: 'up',
    icon: ChatBubbleLeftRightIcon,
    bgColor: 'bg-purple-100',
    iconColor: 'text-purple-600'
  },
  {
    key: 'efficiency',
    title: 'Eficiencia',
    value: '94.2%',
    change: '+2.1%',
    trend: 'up',
    icon: ChartBarIcon,
    bgColor: 'bg-orange-100',
    iconColor: 'text-orange-600'
  }
])

const customerSatisfaction = computed(() => Math.round((analyticsStore.overview.average_satisfaction || 0) * 100))
const averageResponseTime = computed(() => Math.round(analyticsStore.overview.average_response_time || 0))
const responseTimeScore = computed(() => Math.max(0, 100 - (averageResponseTime.value / 10)))
const resolutionRate = computed(() => Math.round((analyticsStore.overview.resolution_rate || 0) * 100))

const revenueData = computed(() => ({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [{
    label: 'Ingresos',
    data: [12000, 15000, 18000, 22000, 25000, 28000],
    borderColor: '#10B981',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    tension: 0.4
  }]
}))

const userGrowthData = computed(() => ({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Nuevos Usuarios',
      data: [120, 150, 180, 220, 250, 280],
      backgroundColor: '#3B82F6'
    },
    {
      label: 'Usuarios Activos',
      data: [800, 920, 1050, 1200, 1350, 1500],
      backgroundColor: '#8B5CF6'
    }
  ]
}))

const topInsights = computed(() => [
  {
    id: 1,
    title: 'Pico de actividad detectado',
    description: 'Las conversaciones aumentaron 35% en las últimas 2 semanas, principalmente en horario nocturno.',
    impact: 'Alto Impacto',
    timeframe: 'Últimas 2 semanas',
    icon: TrendingUpIcon,
    bgColor: 'bg-green-100',
    iconColor: 'text-green-600',
    badgeColor: 'bg-green-100 text-green-800'
  },
  {
    id: 2,
    title: 'Oportunidad de optimización',
    description: 'El tiempo de respuesta promedio puede reducirse 20% optimizando los chatbots más utilizados.',
    impact: 'Medio Impacto',
    timeframe: 'Análisis continuo',
    icon: LightBulbIcon,
    bgColor: 'bg-yellow-100',
    iconColor: 'text-yellow-600',
    badgeColor: 'bg-yellow-100 text-yellow-800'
  },
  {
    id: 3,
    title: 'Alerta de capacidad',
    description: 'Se recomienda aumentar la capacidad del servidor para manejar el crecimiento proyectado.',
    impact: 'Crítico',
    timeframe: 'Próximos 30 días',
    icon: ExclamationTriangleIcon,
    bgColor: 'bg-red-100',
    iconColor: 'text-red-600',
    badgeColor: 'bg-red-100 text-red-800'
  }
])

const revenueChartOptions = {
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
      ticks: {
        callback: function(value) {
          return '$' + value.toLocaleString()
        }
      }
    }
  }
}

const userGrowthChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

// Methods
const refreshReports = async () => {
  isLoading.value = true
  try {
    await Promise.all([
      analyticsStore.fetchOverview({ period: selectedPeriod.value }),
      analyticsStore.fetchConversationMetrics({ period: selectedPeriod.value }),
      analyticsStore.fetchChatbotPerformance({ period: selectedPeriod.value })
    ])
  } catch (error) {
    console.error('Error refreshing reports:', error)
  } finally {
    isLoading.value = false
  }
}

const applyCustomRange = () => {
  if (customDateRange.value.start && customDateRange.value.end) {
    refreshReports()
  }
}

const exportToPDF = () => {
  const doc = new jsPDF()
  
  // Header
  doc.setFontSize(20)
  doc.text('Reporte Ejecutivo VersaAI', 20, 30)
  
  // Date
  doc.setFontSize(12)
  doc.text(`Período: ${selectedPeriod.value}`, 20, 45)
  doc.text(`Generado: ${new Date().toLocaleDateString()}`, 20, 55)
  
  // KPIs
  doc.setFontSize(16)
  doc.text('KPIs Principales', 20, 75)
  
  let yPos = 90
  executiveKPIs.value.forEach((kpi, index) => {
    doc.setFontSize(12)
    doc.text(`${kpi.title}: ${kpi.value} (${kpi.change})`, 20, yPos)
    yPos += 15
  })
  
  // Insights
  doc.setFontSize(16)
  doc.text('Insights Principales', 20, yPos + 20)
  
  yPos += 35
  topInsights.value.forEach((insight, index) => {
    doc.setFontSize(12)
    doc.text(`${index + 1}. ${insight.title}`, 20, yPos)
    yPos += 10
    doc.setFontSize(10)
    const splitDescription = doc.splitTextToSize(insight.description, 170)
    doc.text(splitDescription, 25, yPos)
    yPos += splitDescription.length * 5 + 10
  })
  
  doc.save('reporte-ejecutivo-versaai.pdf')
}

const exportToExcel = () => {
  const workbook = XLSX.utils.book_new()
  
  // KPIs Sheet
  const kpiData = executiveKPIs.value.map(kpi => ({
    'Métrica': kpi.title,
    'Valor': kpi.value,
    'Cambio': kpi.change,
    'Tendencia': kpi.trend
  }))
  
  const kpiSheet = XLSX.utils.json_to_sheet(kpiData)
  XLSX.utils.book_append_sheet(workbook, kpiSheet, 'KPIs')
  
  // Insights Sheet
  const insightData = topInsights.value.map(insight => ({
    'Título': insight.title,
    'Descripción': insight.description,
    'Impacto': insight.impact,
    'Período': insight.timeframe
  }))
  
  const insightSheet = XLSX.utils.json_to_sheet(insightData)
  XLSX.utils.book_append_sheet(workbook, insightSheet, 'Insights')
  
  XLSX.writeFile(workbook, 'reporte-ejecutivo-versaai.xlsx')
}

// Watchers
watch(selectedPeriod, () => {
  if (selectedPeriod.value !== 'custom') {
    refreshReports()
  }
})

watch([() => customDateRange.value.start, () => customDateRange.value.end], () => {
  if (selectedPeriod.value === 'custom' && customDateRange.value.start && customDateRange.value.end) {
    refreshReports()
  }
})

// Lifecycle
onMounted(() => {
  refreshReports()
})
</script>

<style scoped>
.executive-reports {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>