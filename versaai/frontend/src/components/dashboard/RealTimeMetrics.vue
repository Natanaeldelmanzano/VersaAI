<template>
  <div class="real-time-metrics">
    <!-- Header -->
    <div class="metrics-header">
      <div class="header-info">
        <h2 class="title">
          <ChartBarIcon class="icon" />
          Métricas en Tiempo Real
        </h2>
        <div class="connection-status">
          <div class="status-indicator" :class="connectionStatusClass">
            <div class="pulse"></div>
          </div>
          <span class="status-text">{{ connectionStatusText }}</span>
          <span v-if="latency > 0" class="latency">{{ latency }}ms</span>
        </div>
      </div>
      
      <div class="header-actions">
        <button 
          @click="toggleAutoRefresh" 
          class="action-btn"
          :class="{ active: autoRefresh }"
        >
          <ArrowPathIcon class="icon" :class="{ 'animate-spin': autoRefresh }" />
          Auto-actualizar
        </button>
        
        <button @click="refreshMetrics" class="action-btn">
          <ArrowPathIcon class="icon" />
          Actualizar
        </button>
        
        <div class="dropdown" ref="settingsDropdown">
          <button @click="toggleSettings" class="action-btn">
            <Cog6ToothIcon class="icon" />
            Configurar
          </button>
          
          <div v-if="showSettings" class="dropdown-menu">
            <div class="dropdown-header">
              <h3>Configuración de Métricas</h3>
            </div>
            
            <div class="metric-toggles">
              <label v-for="metric in availableMetrics" :key="metric.key" class="metric-toggle">
                <input 
                  type="checkbox" 
                  :checked="selectedMetrics.includes(metric.key)"
                  @change="toggleMetric(metric.key)"
                >
                <span class="checkmark"></span>
                <span class="label">{{ metric.label }}</span>
              </label>
            </div>
            
            <div class="refresh-interval">
              <label>Intervalo de actualización:</label>
              <select v-model="refreshInterval" @change="updateRefreshInterval">
                <option value="1000">1 segundo</option>
                <option value="5000">5 segundos</option>
                <option value="10000">10 segundos</option>
                <option value="30000">30 segundos</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Métricas principales -->
    <div class="metrics-grid">
      <!-- Usuarios activos -->
      <div class="metric-card" v-if="selectedMetrics.includes('activeUsers')">
        <div class="metric-header">
          <div class="metric-icon users">
            <UsersIcon />
          </div>
          <div class="metric-info">
            <h3>Usuarios Activos</h3>
            <p class="metric-subtitle">En línea ahora</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatNumber(metrics.activeUsers?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(metrics.activeUsers?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.activeUsers?.trend > 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.activeUsers?.trend < 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(metrics.activeUsers?.trend) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="activeUsersChart" width="200" height="60"></canvas>
        </div>
      </div>

      <!-- Conversaciones activas -->
      <div class="metric-card" v-if="selectedMetrics.includes('activeConversations')">
        <div class="metric-header">
          <div class="metric-icon conversations">
            <ChatBubbleLeftRightIcon />
          </div>
          <div class="metric-info">
            <h3>Conversaciones</h3>
            <p class="metric-subtitle">Activas</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatNumber(metrics.activeConversations?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(metrics.activeConversations?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.activeConversations?.trend > 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.activeConversations?.trend < 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(metrics.activeConversations?.trend) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="conversationsChart" width="200" height="60"></canvas>
        </div>
      </div>

      <!-- Mensajes por minuto -->
      <div class="metric-card" v-if="selectedMetrics.includes('messagesPerMinute')">
        <div class="metric-header">
          <div class="metric-icon messages">
            <PaperAirplaneIcon />
          </div>
          <div class="metric-info">
            <h3>Mensajes/min</h3>
            <p class="metric-subtitle">Tasa actual</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatNumber(metrics.messagesPerMinute?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(metrics.messagesPerMinute?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.messagesPerMinute?.trend > 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.messagesPerMinute?.trend < 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(metrics.messagesPerMinute?.trend) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="messagesChart" width="200" height="60"></canvas>
        </div>
      </div>

      <!-- Tiempo de respuesta -->
      <div class="metric-card" v-if="selectedMetrics.includes('responseTime')">
        <div class="metric-header">
          <div class="metric-icon response-time">
            <ClockIcon />
          </div>
          <div class="metric-info">
            <h3>Tiempo Respuesta</h3>
            <p class="metric-subtitle">Promedio</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatDuration(metrics.responseTime?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(-metrics.responseTime?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.responseTime?.trend < 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.responseTime?.trend > 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(Math.abs(metrics.responseTime?.trend)) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="responseTimeChart" width="200" height="60"></canvas>
        </div>
      </div>

      <!-- CPU Usage -->
      <div class="metric-card" v-if="selectedMetrics.includes('cpuUsage')">
        <div class="metric-header">
          <div class="metric-icon cpu">
            <CpuChipIcon />
          </div>
          <div class="metric-info">
            <h3>CPU</h3>
            <p class="metric-subtitle">Uso actual</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatPercentage(metrics.cpuUsage?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(-metrics.cpuUsage?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.cpuUsage?.trend < 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.cpuUsage?.trend > 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(Math.abs(metrics.cpuUsage?.trend)) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="cpuChart" width="200" height="60"></canvas>
        </div>
      </div>

      <!-- Memory Usage -->
      <div class="metric-card" v-if="selectedMetrics.includes('memoryUsage')">
        <div class="metric-header">
          <div class="metric-icon memory">
            <CircuitBoardIcon />
          </div>
          <div class="metric-info">
            <h3>Memoria</h3>
            <p class="metric-subtitle">Uso actual</p>
          </div>
        </div>
        
        <div class="metric-value">
          <span class="value">{{ formatPercentage(metrics.memoryUsage?.current || 0) }}</span>
          <div class="trend" :class="getTrendClass(-metrics.memoryUsage?.trend)">
            <ArrowTrendingUpIcon v-if="metrics.memoryUsage?.trend < 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else-if="metrics.memoryUsage?.trend > 0" class="trend-icon" />
            <span class="trend-value">{{ formatTrend(Math.abs(metrics.memoryUsage?.trend)) }}</span>
          </div>
        </div>
        
        <div class="metric-chart">
          <canvas ref="memoryChart" width="200" height="60"></canvas>
        </div>
      </div>
    </div>

    <!-- Alertas en tiempo real -->
    <div v-if="alerts.length > 0" class="alerts-section">
      <h3 class="alerts-title">
        <ExclamationTriangleIcon class="icon" />
        Alertas del Sistema
      </h3>
      
      <div class="alerts-list">
        <div 
          v-for="alert in alerts" 
          :key="alert.id"
          class="alert-item"
          :class="alert.severity"
        >
          <div class="alert-icon">
            <ExclamationTriangleIcon v-if="alert.severity === 'warning'" />
            <XCircleIcon v-else-if="alert.severity === 'error'" />
            <InformationCircleIcon v-else />
          </div>
          
          <div class="alert-content">
            <h4 class="alert-title">{{ alert.title }}</h4>
            <p class="alert-message">{{ alert.message }}</p>
            <span class="alert-time">{{ formatTime(alert.timestamp) }}</span>
          </div>
          
          <button @click="dismissAlert(alert.id)" class="alert-dismiss">
            <XMarkIcon />
          </button>
        </div>
      </div>
    </div>

    <!-- Última actualización -->
    <div class="last-update">
      <span>Última actualización: {{ formatTime(lastUpdate) }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import {
  ChartBarIcon,
  UsersIcon,
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  ClockIcon,
  CpuChipIcon,
  CircuitBoardIcon,
  ArrowPathIcon,
  Cog6ToothIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useRealTimeMetrics } from '@/composables/useWebSocket'

// Composables
const { metrics, lastUpdate, subscribeToMetrics, unsubscribeFromMetrics, isConnected } = useRealTimeMetrics()

// Estado reactivo
const autoRefresh = ref(true)
const showSettings = ref(false)
const refreshInterval = ref(5000)
const settingsDropdown = ref(null)
const alerts = ref([])

// Métricas disponibles
const availableMetrics = ref([
  { key: 'activeUsers', label: 'Usuarios Activos' },
  { key: 'activeConversations', label: 'Conversaciones Activas' },
  { key: 'messagesPerMinute', label: 'Mensajes por Minuto' },
  { key: 'responseTime', label: 'Tiempo de Respuesta' },
  { key: 'cpuUsage', label: 'Uso de CPU' },
  { key: 'memoryUsage', label: 'Uso de Memoria' }
])

// Métricas seleccionadas
const selectedMetrics = ref([
  'activeUsers',
  'activeConversations', 
  'messagesPerMinute',
  'responseTime'
])

// Referencias a canvas para gráficos
const activeUsersChart = ref(null)
const conversationsChart = ref(null)
const messagesChart = ref(null)
const responseTimeChart = ref(null)
const cpuChart = ref(null)
const memoryChart = ref(null)

// Datos históricos para gráficos
const chartData = ref({
  activeUsers: [],
  activeConversations: [],
  messagesPerMinute: [],
  responseTime: [],
  cpuUsage: [],
  memoryUsage: []
})

// Timers
let refreshTimer = null

// Computed
const connectionStatusClass = computed(() => {
  if (isConnected.value) return 'connected'
  return 'disconnected'
})

const connectionStatusText = computed(() => {
  if (isConnected.value) return 'Conectado'
  return 'Desconectado'
})

const latency = computed(() => {
  // Obtener latencia del composable WebSocket
  return 0 // Placeholder
})

// Métodos
const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  
  if (autoRefresh.value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const refreshMetrics = () => {
  subscribeToMetrics(selectedMetrics.value)
}

const toggleSettings = () => {
  showSettings.value = !showSettings.value
}

const toggleMetric = (metricKey) => {
  const index = selectedMetrics.value.indexOf(metricKey)
  if (index > -1) {
    selectedMetrics.value.splice(index, 1)
    unsubscribeFromMetrics([metricKey])
  } else {
    selectedMetrics.value.push(metricKey)
    subscribeToMetrics([metricKey])
  }
}

const updateRefreshInterval = () => {
  if (autoRefresh.value) {
    stopAutoRefresh()
    startAutoRefresh()
  }
}

const startAutoRefresh = () => {
  if (refreshTimer) clearInterval(refreshTimer)
  
  refreshTimer = setInterval(() => {
    if (isConnected.value) {
      subscribeToMetrics(selectedMetrics.value)
    }
  }, refreshInterval.value)
}

const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

const dismissAlert = (alertId) => {
  const index = alerts.value.findIndex(alert => alert.id === alertId)
  if (index > -1) {
    alerts.value.splice(index, 1)
  }
}

// Formatters
const formatNumber = (value) => {
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M'
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K'
  }
  return value.toString()
}

const formatPercentage = (value) => {
  return value.toFixed(1) + '%'
}

const formatDuration = (ms) => {
  if (ms >= 1000) {
    return (ms / 1000).toFixed(1) + 's'
  }
  return ms.toFixed(0) + 'ms'
}

const formatTrend = (value) => {
  if (value === 0) return '0%'
  const sign = value > 0 ? '+' : ''
  return sign + value.toFixed(1) + '%'
}

const getTrendClass = (trend) => {
  if (trend > 0) return 'positive'
  if (trend < 0) return 'negative'
  return 'neutral'
}

const formatTime = (timestamp) => {
  if (!timestamp) return 'Nunca'
  return new Date(timestamp).toLocaleTimeString()
}

// Gráficos
const updateCharts = () => {
  nextTick(() => {
    Object.keys(chartData.value).forEach(metricKey => {
      if (selectedMetrics.value.includes(metricKey)) {
        drawMiniChart(metricKey)
      }
    })
  })
}

const drawMiniChart = (metricKey) => {
  const canvasRef = {
    activeUsers: activeUsersChart,
    activeConversations: conversationsChart,
    messagesPerMinute: messagesChart,
    responseTime: responseTimeChart,
    cpuUsage: cpuChart,
    memoryUsage: memoryChart
  }[metricKey]
  
  if (!canvasRef?.value) return
  
  const canvas = canvasRef.value
  const ctx = canvas.getContext('2d')
  const data = chartData.value[metricKey]
  
  if (!data || data.length === 0) return
  
  // Limpiar canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // Configuración
  const padding = 5
  const width = canvas.width - padding * 2
  const height = canvas.height - padding * 2
  
  // Calcular escalas
  const maxValue = Math.max(...data)
  const minValue = Math.min(...data)
  const range = maxValue - minValue || 1
  
  // Dibujar línea
  ctx.strokeStyle = '#3B82F6'
  ctx.lineWidth = 2
  ctx.beginPath()
  
  data.forEach((value, index) => {
    const x = padding + (index / (data.length - 1)) * width
    const y = padding + height - ((value - minValue) / range) * height
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  
  ctx.stroke()
  
  // Área bajo la curva
  ctx.fillStyle = 'rgba(59, 130, 246, 0.1)'
  ctx.beginPath()
  
  data.forEach((value, index) => {
    const x = padding + (index / (data.length - 1)) * width
    const y = padding + height - ((value - minValue) / range) * height
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  
  ctx.lineTo(padding + width, padding + height)
  ctx.lineTo(padding, padding + height)
  ctx.closePath()
  ctx.fill()
}

// Watchers
watch(metrics, (newMetrics) => {
  // Actualizar datos de gráficos
  Object.keys(newMetrics).forEach(key => {
    if (chartData.value[key]) {
      chartData.value[key].push(newMetrics[key]?.current || 0)
      
      // Mantener solo los últimos 20 puntos
      if (chartData.value[key].length > 20) {
        chartData.value[key] = chartData.value[key].slice(-20)
      }
    }
  })
  
  updateCharts()
}, { deep: true })

watch(selectedMetrics, (newMetrics) => {
  subscribeToMetrics(newMetrics)
}, { deep: true })

// Lifecycle
onMounted(() => {
  // Suscribirse a métricas iniciales
  subscribeToMetrics(selectedMetrics.value)
  
  // Iniciar auto-refresh
  if (autoRefresh.value) {
    startAutoRefresh()
  }
  
  // Cerrar dropdown al hacer clic fuera
  document.addEventListener('click', (e) => {
    if (settingsDropdown.value && !settingsDropdown.value.contains(e.target)) {
      showSettings.value = false
    }
  })
  
  // Simular algunas alertas para demo
  setTimeout(() => {
    alerts.value.push({
      id: 1,
      severity: 'warning',
      title: 'Alto uso de CPU',
      message: 'El uso de CPU ha superado el 80%',
      timestamp: Date.now()
    })
  }, 5000)
})

onUnmounted(() => {
  stopAutoRefresh()
  unsubscribeFromMetrics(selectedMetrics.value)
})
</script>

<style scoped>
.real-time-metrics {
  @apply space-y-6;
}

.metrics-header {
  @apply flex items-center justify-between bg-white rounded-lg shadow-sm border p-6;
}

.header-info {
  @apply flex items-center space-x-4;
}

.title {
  @apply text-xl font-semibold text-gray-900 flex items-center;
}

.title .icon {
  @apply w-6 h-6 mr-2 text-blue-600;
}

.connection-status {
  @apply flex items-center space-x-2 text-sm;
}

.status-indicator {
  @apply relative w-3 h-3 rounded-full;
}

.status-indicator.connected {
  @apply bg-green-500;
}

.status-indicator.disconnected {
  @apply bg-red-500;
}

.pulse {
  @apply absolute inset-0 rounded-full animate-ping;
}

.status-indicator.connected .pulse {
  @apply bg-green-400;
}

.status-indicator.disconnected .pulse {
  @apply bg-red-400;
}

.status-text {
  @apply text-gray-600;
}

.latency {
  @apply text-gray-500 text-xs;
}

.header-actions {
  @apply flex items-center space-x-3;
}

.action-btn {
  @apply flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}

.action-btn.active {
  @apply bg-blue-50 text-blue-700 border-blue-300;
}

.action-btn .icon {
  @apply w-4 h-4;
}

.dropdown {
  @apply relative;
}

.dropdown-menu {
  @apply absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-lg border z-50;
}

.dropdown-header {
  @apply px-4 py-3 border-b;
}

.dropdown-header h3 {
  @apply text-sm font-medium text-gray-900;
}

.metric-toggles {
  @apply p-4 space-y-3;
}

.metric-toggle {
  @apply flex items-center space-x-3 cursor-pointer;
}

.metric-toggle input[type="checkbox"] {
  @apply sr-only;
}

.checkmark {
  @apply w-4 h-4 border-2 border-gray-300 rounded flex-shrink-0 relative;
}

.metric-toggle input:checked + .checkmark {
  @apply bg-blue-600 border-blue-600;
}

.metric-toggle input:checked + .checkmark::after {
  content: '';
  @apply absolute top-0.5 left-1 w-1.5 h-2.5 border-white border-r-2 border-b-2 transform rotate-45;
}

.metric-toggle .label {
  @apply text-sm text-gray-700;
}

.refresh-interval {
  @apply px-4 py-3 border-t;
}

.refresh-interval label {
  @apply block text-sm font-medium text-gray-700 mb-2;
}

.refresh-interval select {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

.metrics-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6;
}

.metric-card {
  @apply bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow;
}

.metric-header {
  @apply flex items-center space-x-3 mb-4;
}

.metric-icon {
  @apply w-10 h-10 rounded-lg flex items-center justify-center;
}

.metric-icon.users {
  @apply bg-blue-100 text-blue-600;
}

.metric-icon.conversations {
  @apply bg-green-100 text-green-600;
}

.metric-icon.messages {
  @apply bg-purple-100 text-purple-600;
}

.metric-icon.response-time {
  @apply bg-yellow-100 text-yellow-600;
}

.metric-icon.cpu {
  @apply bg-red-100 text-red-600;
}

.metric-icon.memory {
  @apply bg-indigo-100 text-indigo-600;
}

.metric-icon svg {
  @apply w-5 h-5;
}

.metric-info h3 {
  @apply text-sm font-medium text-gray-900;
}

.metric-subtitle {
  @apply text-xs text-gray-500;
}

.metric-value {
  @apply flex items-center justify-between mb-4;
}

.value {
  @apply text-2xl font-bold text-gray-900;
}

.trend {
  @apply flex items-center space-x-1 text-sm;
}

.trend.positive {
  @apply text-green-600;
}

.trend.negative {
  @apply text-red-600;
}

.trend.neutral {
  @apply text-gray-500;
}

.trend-icon {
  @apply w-4 h-4;
}

.metric-chart {
  @apply h-15;
}

.metric-chart canvas {
  @apply w-full h-full;
}

.alerts-section {
  @apply bg-white rounded-lg shadow-sm border p-6;
}

.alerts-title {
  @apply text-lg font-semibold text-gray-900 flex items-center mb-4;
}

.alerts-title .icon {
  @apply w-5 h-5 mr-2 text-yellow-600;
}

.alerts-list {
  @apply space-y-3;
}

.alert-item {
  @apply flex items-start space-x-3 p-4 rounded-lg border;
}

.alert-item.warning {
  @apply bg-yellow-50 border-yellow-200;
}

.alert-item.error {
  @apply bg-red-50 border-red-200;
}

.alert-item.info {
  @apply bg-blue-50 border-blue-200;
}

.alert-icon {
  @apply flex-shrink-0;
}

.alert-icon svg {
  @apply w-5 h-5;
}

.alert-item.warning .alert-icon svg {
  @apply text-yellow-600;
}

.alert-item.error .alert-icon svg {
  @apply text-red-600;
}

.alert-item.info .alert-icon svg {
  @apply text-blue-600;
}

.alert-content {
  @apply flex-1;
}

.alert-title {
  @apply text-sm font-medium text-gray-900;
}

.alert-message {
  @apply text-sm text-gray-600 mt-1;
}

.alert-time {
  @apply text-xs text-gray-500 mt-2;
}

.alert-dismiss {
  @apply flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors;
}

.alert-dismiss svg {
  @apply w-4 h-4;
}

.last-update {
  @apply text-center text-sm text-gray-500;
}

@media (max-width: 768px) {
  .metrics-header {
    @apply flex-col space-y-4;
  }
  
  .header-info {
    @apply flex-col space-y-2 space-x-0;
  }
  
  .header-actions {
    @apply flex-wrap;
  }
  
  .metrics-grid {
    @apply grid-cols-1;
  }
  
  .dropdown-menu {
    @apply w-full;
  }
}
</style>