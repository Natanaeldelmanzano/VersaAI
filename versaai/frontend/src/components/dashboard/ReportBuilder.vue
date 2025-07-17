<template>
  <div class="report-builder">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Constructor de Reportes</h2>
        <p class="text-gray-600 mt-2">Crea reportes personalizados con métricas específicas</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="saveTemplate"
          :disabled="!canSaveTemplate"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          <BookmarkIcon class="w-4 h-4 mr-2" />
          Guardar Plantilla
        </button>
        
        <button
          @click="generateReport"
          :disabled="!canGenerateReport || isGenerating"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
        >
          <DocumentChartBarIcon :class="['w-4 h-4 mr-2', { 'animate-spin': isGenerating }]" />
          Generar Reporte
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Panel de Configuración -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Información Básica -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Información del Reporte</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Reporte</label>
              <input
                v-model="reportConfig.name"
                type="text"
                placeholder="Ej: Reporte Mensual de Ventas"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
              <textarea
                v-model="reportConfig.description"
                rows="3"
                placeholder="Describe el propósito de este reporte..."
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Reporte</label>
              <select
                v-model="reportConfig.type"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="executive">Ejecutivo</option>
                <option value="operational">Operacional</option>
                <option value="financial">Financiero</option>
                <option value="performance">Rendimiento</option>
                <option value="custom">Personalizado</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Período de Tiempo -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Período de Tiempo</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Rango de Fechas</label>
              <select
                v-model="reportConfig.dateRange"
                @change="updateDateRange"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="last_7_days">Últimos 7 días</option>
                <option value="last_30_days">Últimos 30 días</option>
                <option value="last_90_days">Últimos 90 días</option>
                <option value="last_year">Último año</option>
                <option value="custom">Personalizado</option>
              </select>
            </div>
            
            <div v-if="reportConfig.dateRange === 'custom'" class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Desde</label>
                <input
                  v-model="reportConfig.startDate"
                  type="date"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Hasta</label>
                <input
                  v-model="reportConfig.endDate"
                  type="date"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Frecuencia</label>
              <select
                v-model="reportConfig.frequency"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="once">Una vez</option>
                <option value="daily">Diario</option>
                <option value="weekly">Semanal</option>
                <option value="monthly">Mensual</option>
                <option value="quarterly">Trimestral</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Filtros -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Filtros</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Organizaciones</label>
              <div class="space-y-2 max-h-32 overflow-y-auto">
                <label v-for="org in availableOrganizations" :key="org.id" class="flex items-center">
                  <input
                    v-model="reportConfig.filters.organizations"
                    :value="org.id"
                    type="checkbox"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">{{ org.name }}</span>
                </label>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Chatbots</label>
              <div class="space-y-2 max-h-32 overflow-y-auto">
                <label v-for="bot in availableChatbots" :key="bot.id" class="flex items-center">
                  <input
                    v-model="reportConfig.filters.chatbots"
                    :value="bot.id"
                    type="checkbox"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">{{ bot.name }}</span>
                </label>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Usuarios</label>
              <select
                v-model="reportConfig.filters.userType"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="all">Todos los usuarios</option>
                <option value="new">Usuarios nuevos</option>
                <option value="returning">Usuarios recurrentes</option>
                <option value="premium">Usuarios premium</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Formato de Exportación -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Formato de Exportación</h3>
          
          <div class="space-y-3">
            <label class="flex items-center">
              <input
                v-model="reportConfig.exportFormats"
                value="pdf"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-gray-700">PDF</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="reportConfig.exportFormats"
                value="excel"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-gray-700">Excel</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="reportConfig.exportFormats"
                value="csv"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-gray-700">CSV</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="reportConfig.exportFormats"
                value="json"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span class="ml-2 text-sm text-gray-700">JSON</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Panel de Métricas y Vista Previa -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Selección de Métricas -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Métricas a Incluir</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="category in metricCategories" :key="category.name" class="space-y-3">
              <h4 class="text-sm font-semibold text-gray-700 uppercase tracking-wide">{{ category.name }}</h4>
              <div class="space-y-2">
                <label v-for="metric in category.metrics" :key="metric.key" class="flex items-center">
                  <input
                    v-model="reportConfig.selectedMetrics"
                    :value="metric.key"
                    type="checkbox"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span class="ml-2 text-sm text-gray-700">{{ metric.name }}</span>
                  <span v-if="metric.description" class="ml-1 text-xs text-gray-500">({{ metric.description }})</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Vista Previa del Reporte -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Vista Previa</h3>
            <button
              @click="refreshPreview"
              :disabled="isLoadingPreview"
              class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-lg shadow-sm text-xs font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              <ArrowPathIcon :class="['w-3 h-3 mr-1', { 'animate-spin': isLoadingPreview }]" />
              Actualizar
            </button>
          </div>
          
          <div v-if="isLoadingPreview" class="flex items-center justify-center h-64">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
          
          <div v-else-if="previewData" class="space-y-6">
            <!-- Resumen de Configuración -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-900 mb-2">Configuración del Reporte</h4>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-600">Nombre:</span>
                  <span class="ml-2 font-medium">{{ reportConfig.name || 'Sin nombre' }}</span>
                </div>
                <div>
                  <span class="text-gray-600">Tipo:</span>
                  <span class="ml-2 font-medium">{{ reportConfig.type }}</span>
                </div>
                <div>
                  <span class="text-gray-600">Período:</span>
                  <span class="ml-2 font-medium">{{ formatDateRange }}</span>
                </div>
                <div>
                  <span class="text-gray-600">Métricas:</span>
                  <span class="ml-2 font-medium">{{ reportConfig.selectedMetrics.length }} seleccionadas</span>
                </div>
              </div>
            </div>
            
            <!-- Métricas Seleccionadas -->
            <div v-if="reportConfig.selectedMetrics.length > 0">
              <h4 class="text-sm font-semibold text-gray-900 mb-3">Métricas Incluidas</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div 
                  v-for="metric in selectedMetricsPreview" 
                  :key="metric.key"
                  class="bg-gray-50 rounded-lg p-4 text-center"
                >
                  <div class="text-2xl font-bold text-gray-900">{{ metric.value }}</div>
                  <div class="text-sm text-gray-600 mt-1">{{ metric.name }}</div>
                  <div v-if="metric.change" class="text-xs mt-1" :class="metric.changeColor">
                    {{ metric.change }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Gráfico de Muestra -->
            <div v-if="reportConfig.selectedMetrics.length > 0">
              <h4 class="text-sm font-semibold text-gray-900 mb-3">Gráfico de Muestra</h4>
              <div class="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                <div class="text-center text-gray-500">
                  <ChartBarIcon class="w-12 h-12 mx-auto mb-2" />
                  <p class="text-sm">Vista previa del gráfico se generará aquí</p>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else class="flex items-center justify-center h-64 text-gray-500">
            <div class="text-center">
              <DocumentChartBarIcon class="w-12 h-12 mx-auto mb-2" />
              <p class="text-sm">Selecciona métricas para ver la vista previa</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Plantillas Guardadas -->
    <div v-if="savedTemplates.length > 0" class="mt-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Plantillas Guardadas</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="template in savedTemplates" 
            :key="template.id"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
            @click="loadTemplate(template)"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-sm font-semibold text-gray-900">{{ template.name }}</h4>
              <button
                @click.stop="deleteTemplate(template.id)"
                class="text-gray-400 hover:text-red-500"
              >
                <TrashIcon class="w-4 h-4" />
              </button>
            </div>
            <p class="text-xs text-gray-600 mb-2">{{ template.description }}</p>
            <div class="flex items-center justify-between text-xs text-gray-500">
              <span>{{ template.type }}</span>
              <span>{{ template.metricsCount }} métricas</span>
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
  BookmarkIcon,
  DocumentChartBarIcon,
  ArrowPathIcon,
  ChartBarIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

// Stores
const analyticsStore = useAnalyticsStore()
const dashboardStore = useDashboardStore()

// State
const isGenerating = ref(false)
const isLoadingPreview = ref(false)
const previewData = ref(null)

const reportConfig = ref({
  name: '',
  description: '',
  type: 'executive',
  dateRange: 'last_30_days',
  startDate: '',
  endDate: '',
  frequency: 'once',
  selectedMetrics: [],
  filters: {
    organizations: [],
    chatbots: [],
    userType: 'all'
  },
  exportFormats: ['pdf']
})

const savedTemplates = ref([
  {
    id: 1,
    name: 'Reporte Ejecutivo Mensual',
    description: 'KPIs principales y métricas de rendimiento',
    type: 'executive',
    metricsCount: 8,
    config: {
      selectedMetrics: ['revenue', 'users', 'conversations', 'satisfaction'],
      dateRange: 'last_30_days',
      type: 'executive'
    }
  },
  {
    id: 2,
    name: 'Análisis de Rendimiento',
    description: 'Métricas técnicas y de performance',
    type: 'performance',
    metricsCount: 6,
    config: {
      selectedMetrics: ['response_time', 'uptime', 'error_rate', 'throughput'],
      dateRange: 'last_7_days',
      type: 'performance'
    }
  }
])

// Mock data
const availableOrganizations = ref([
  { id: 1, name: 'Organización Principal' },
  { id: 2, name: 'Sucursal Norte' },
  { id: 3, name: 'Sucursal Sur' }
])

const availableChatbots = ref([
  { id: 1, name: 'Chatbot Ventas' },
  { id: 2, name: 'Chatbot Soporte' },
  { id: 3, name: 'Chatbot Marketing' }
])

const metricCategories = ref([
  {
    name: 'Financieras',
    metrics: [
      { key: 'revenue', name: 'Ingresos Totales', description: 'Ingresos generados' },
      { key: 'revenue_growth', name: 'Crecimiento de Ingresos', description: '% de crecimiento' },
      { key: 'arpu', name: 'ARPU', description: 'Ingreso promedio por usuario' },
      { key: 'ltv', name: 'LTV', description: 'Valor de vida del cliente' }
    ]
  },
  {
    name: 'Usuarios',
    metrics: [
      { key: 'total_users', name: 'Usuarios Totales', description: 'Usuarios registrados' },
      { key: 'active_users', name: 'Usuarios Activos', description: 'Usuarios activos en el período' },
      { key: 'new_users', name: 'Usuarios Nuevos', description: 'Nuevos registros' },
      { key: 'user_retention', name: 'Retención de Usuarios', description: '% de usuarios que regresan' }
    ]
  },
  {
    name: 'Conversaciones',
    metrics: [
      { key: 'total_conversations', name: 'Conversaciones Totales', description: 'Total de conversaciones' },
      { key: 'avg_conversation_length', name: 'Duración Promedio', description: 'Duración promedio de conversaciones' },
      { key: 'resolution_rate', name: 'Tasa de Resolución', description: '% de conversaciones resueltas' },
      { key: 'satisfaction_score', name: 'Puntuación de Satisfacción', description: 'Promedio de satisfacción' }
    ]
  },
  {
    name: 'Rendimiento',
    metrics: [
      { key: 'response_time', name: 'Tiempo de Respuesta', description: 'Tiempo promedio de respuesta' },
      { key: 'uptime', name: 'Tiempo de Actividad', description: '% de tiempo activo' },
      { key: 'error_rate', name: 'Tasa de Errores', description: '% de errores' },
      { key: 'throughput', name: 'Rendimiento', description: 'Mensajes procesados por minuto' }
    ]
  }
])

// Computed
const canSaveTemplate = computed(() => {
  return reportConfig.value.name && reportConfig.value.selectedMetrics.length > 0
})

const canGenerateReport = computed(() => {
  return reportConfig.value.selectedMetrics.length > 0 && reportConfig.value.exportFormats.length > 0
})

const formatDateRange = computed(() => {
  switch (reportConfig.value.dateRange) {
    case 'last_7_days': return 'Últimos 7 días'
    case 'last_30_days': return 'Últimos 30 días'
    case 'last_90_days': return 'Últimos 90 días'
    case 'last_year': return 'Último año'
    case 'custom': return `${reportConfig.value.startDate} - ${reportConfig.value.endDate}`
    default: return 'No definido'
  }
})

const selectedMetricsPreview = computed(() => {
  const mockValues = {
    revenue: { value: '$125,430', change: '+12.5%', changeColor: 'text-green-600' },
    users: { value: '2,847', change: '+8.3%', changeColor: 'text-green-600' },
    conversations: { value: '15,692', change: '+15.7%', changeColor: 'text-green-600' },
    satisfaction: { value: '4.8/5', change: '+0.2', changeColor: 'text-green-600' },
    response_time: { value: '1.2s', change: '-0.3s', changeColor: 'text-green-600' },
    uptime: { value: '99.9%', change: '+0.1%', changeColor: 'text-green-600' }
  }
  
  return reportConfig.value.selectedMetrics.map(metricKey => {
    const metric = metricCategories.value
      .flatMap(cat => cat.metrics)
      .find(m => m.key === metricKey)
    
    return {
      key: metricKey,
      name: metric?.name || metricKey,
      ...mockValues[metricKey] || { value: 'N/A', change: null }
    }
  })
})

// Methods
const updateDateRange = () => {
  if (reportConfig.value.dateRange !== 'custom') {
    reportConfig.value.startDate = ''
    reportConfig.value.endDate = ''
  }
}

const refreshPreview = async () => {
  if (reportConfig.value.selectedMetrics.length === 0) {
    previewData.value = null
    return
  }
  
  isLoadingPreview.value = true
  
  try {
    // Simular carga de datos
    await new Promise(resolve => setTimeout(resolve, 1000))
    previewData.value = {
      metrics: selectedMetricsPreview.value,
      config: { ...reportConfig.value }
    }
  } catch (error) {
    console.error('Error loading preview:', error)
  } finally {
    isLoadingPreview.value = false
  }
}

const generateReport = async () => {
  isGenerating.value = true
  
  try {
    // Simular generación de reporte
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Aquí iría la lógica real de generación
    console.log('Generating report with config:', reportConfig.value)
    
    // Notificar éxito
    alert('Reporte generado exitosamente')
  } catch (error) {
    console.error('Error generating report:', error)
    alert('Error al generar el reporte')
  } finally {
    isGenerating.value = false
  }
}

const saveTemplate = () => {
  const newTemplate = {
    id: Date.now(),
    name: reportConfig.value.name,
    description: reportConfig.value.description || 'Plantilla personalizada',
    type: reportConfig.value.type,
    metricsCount: reportConfig.value.selectedMetrics.length,
    config: { ...reportConfig.value }
  }
  
  savedTemplates.value.push(newTemplate)
  alert('Plantilla guardada exitosamente')
}

const loadTemplate = (template) => {
  reportConfig.value = { ...template.config }
  refreshPreview()
}

const deleteTemplate = (templateId) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta plantilla?')) {
    savedTemplates.value = savedTemplates.value.filter(t => t.id !== templateId)
  }
}

// Watchers
watch(() => reportConfig.value.selectedMetrics, () => {
  refreshPreview()
}, { deep: true })

watch(() => reportConfig.value.dateRange, () => {
  refreshPreview()
})

// Lifecycle
onMounted(() => {
  // Cargar datos iniciales
  refreshPreview()
})
</script>

<style scoped>
.report-builder {
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