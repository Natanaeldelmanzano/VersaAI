<template>
  <div class="conversation-chart h-full">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else class="h-full">
      <canvas ref="chartCanvas" class="w-full h-full"></canvas>
    </div>
    
    <!-- Leyenda personalizada -->
    <div class="flex items-center justify-center space-x-6 mt-4">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
        <span class="text-sm text-gray-600">Conversaciones</span>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
        <span class="text-sm text-gray-600">Mensajes</span>
      </div>
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
        <span class="text-sm text-gray-600">Usuarios Únicos</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  period: {
    type: String,
    default: '24h'
  }
})

// Refs
const chartCanvas = ref(null)
const chartInstance = ref(null)

// Methods
const createChart = async () => {
  if (!chartCanvas.value || props.loading) return
  
  await nextTick()
  
  const ctx = chartCanvas.value.getContext('2d')
  
  // Destroy existing chart
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  
  const chartData = processData()
  
  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: 'Conversaciones',
          data: chartData.conversations,
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#3B82F6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: 'Mensajes',
          data: chartData.messages,
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#10B981',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        },
        {
          label: 'Usuarios Únicos',
          data: chartData.uniqueUsers,
          borderColor: '#8B5CF6',
          backgroundColor: 'rgba(139, 92, 246, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#8B5CF6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false // Using custom legend
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#374151',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            title: function(context) {
              return formatTooltipTitle(context[0].label)
            },
            label: function(context) {
              const value = context.parsed.y
              return `${context.dataset.label}: ${value.toLocaleString()}`
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          border: {
            display: false
          },
          ticks: {
            color: '#6B7280',
            font: {
              size: 12
            },
            maxTicksLimit: 8
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(107, 114, 128, 0.1)',
            drawBorder: false
          },
          border: {
            display: false
          },
          ticks: {
            color: '#6B7280',
            font: {
              size: 12
            },
            callback: function(value) {
              if (value >= 1000) {
                return (value / 1000).toFixed(1) + 'K'
              }
              return value
            }
          }
        }
      },
      elements: {
        point: {
          hoverBackgroundColor: '#ffffff'
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  })
}

const processData = () => {
  if (!props.data || props.data.length === 0) {
    return generateMockData()
  }
  
  // Process real data
  const labels = props.data.map(item => formatLabel(item.date || item.timestamp))
  const conversations = props.data.map(item => item.conversations || 0)
  const messages = props.data.map(item => item.messages || item.conversations * 3.5) // Estimate
  const uniqueUsers = props.data.map(item => item.unique_users || Math.floor(item.conversations * 0.7)) // Estimate
  
  return {
    labels,
    conversations,
    messages,
    uniqueUsers
  }
}

const generateMockData = () => {
  const now = new Date()
  const labels = []
  const conversations = []
  const messages = []
  const uniqueUsers = []
  
  const dataPoints = getDataPointsForPeriod()
  
  for (let i = dataPoints - 1; i >= 0; i--) {
    const date = new Date(now)
    
    if (props.period === '1h') {
      date.setMinutes(date.getMinutes() - i * 5)
      labels.push(date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }))
    } else if (props.period === '24h') {
      date.setHours(date.getHours() - i)
      labels.push(date.toLocaleTimeString('es-ES', { hour: '2-digit' }) + 'h')
    } else {
      date.setDate(date.getDate() - i)
      labels.push(date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }))
    }
    
    // Generate realistic data with trends
    const baseConversations = 50 + Math.random() * 100
    const trend = Math.sin((i / dataPoints) * Math.PI * 2) * 20
    const noise = (Math.random() - 0.5) * 30
    
    const convValue = Math.max(0, Math.floor(baseConversations + trend + noise))
    conversations.push(convValue)
    messages.push(Math.floor(convValue * (3 + Math.random() * 2)))
    uniqueUsers.push(Math.floor(convValue * (0.6 + Math.random() * 0.3)))
  }
  
  return {
    labels,
    conversations,
    messages,
    uniqueUsers
  }
}

const getDataPointsForPeriod = () => {
  switch (props.period) {
    case '1h':
      return 12 // 5-minute intervals
    case '24h':
      return 24 // hourly
    case '7d':
      return 7 // daily
    case '30d':
      return 30 // daily
    case '90d':
      return 12 // weekly
    default:
      return 24
  }
}

const formatLabel = (dateString) => {
  const date = new Date(dateString)
  
  switch (props.period) {
    case '1h':
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    case '24h':
      return date.toLocaleTimeString('es-ES', { hour: '2-digit' }) + 'h'
    case '7d':
    case '30d':
      return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
    case '90d':
      return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
    default:
      return date.toLocaleDateString('es-ES')
  }
}

const formatTooltipTitle = (label) => {
  switch (props.period) {
    case '1h':
      return `Hora: ${label}`
    case '24h':
      return `Hora: ${label}`
    default:
      return `Fecha: ${label}`
  }
}

// Watchers
watch(
  () => [props.data, props.period, props.loading],
  () => {
    if (!props.loading) {
      createChart()
    }
  },
  { deep: true }
)

// Lifecycle
onMounted(() => {
  if (!props.loading) {
    createChart()
  }
})

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
})
</script>

<style scoped>
.conversation-chart {
  position: relative;
}

canvas {
  max-height: 100%;
}
</style>