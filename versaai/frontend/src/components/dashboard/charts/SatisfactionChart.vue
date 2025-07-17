<template>
  <div class="satisfaction-chart h-full">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else class="h-full flex flex-col">
      <!-- Chart container -->
      <div class="flex-1 relative">
        <canvas ref="chartCanvas" class="w-full h-full"></canvas>
        
        <!-- Center score display for doughnut chart -->
        <div 
          v-if="chartType === 'doughnut'"
          class="absolute inset-0 flex items-center justify-center pointer-events-none"
        >
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ overallScore }}%</div>
            <div class="text-sm text-gray-500">Satisfacción</div>
          </div>
        </div>
      </div>
      
      <!-- Chart type toggle -->
      <div class="flex items-center justify-center space-x-4 mt-4">
        <button
          @click="chartType = 'doughnut'"
          :class="[
            'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
            chartType === 'doughnut'
              ? 'bg-primary-100 text-primary-700'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          Distribución
        </button>
        <button
          @click="chartType = 'line'"
          :class="[
            'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
            chartType === 'line'
              ? 'bg-primary-100 text-primary-700'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          Tendencia
        </button>
        <button
          @click="chartType = 'bar'"
          :class="[
            'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
            chartType === 'bar'
              ? 'bg-primary-100 text-primary-700'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          Comparación
        </button>
      </div>
      
      <!-- Satisfaction metrics -->
      <div class="grid grid-cols-3 gap-4 mt-4">
        <div class="text-center">
          <div class="text-lg font-semibold text-green-600">{{ positivePercentage }}%</div>
          <div class="text-xs text-gray-500">Positiva</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-yellow-600">{{ neutralPercentage }}%</div>
          <div class="text-xs text-gray-500">Neutral</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-red-600">{{ negativePercentage }}%</div>
          <div class="text-xs text-gray-500">Negativa</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
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
  }
})

// Refs
const chartCanvas = ref(null)
const chartInstance = ref(null)
const chartType = ref('doughnut')

// Computed
const processedData = computed(() => {
  if (!props.data || props.data.length === 0) {
    return generateMockData()
  }
  return props.data
})

const overallScore = computed(() => {
  const data = processedData.value
  if (chartType.value === 'doughnut') {
    const total = data.reduce((sum, item) => sum + item.value, 0)
    const weighted = data.reduce((sum, item, index) => {
      const weight = index === 0 ? 1 : index === 1 ? 0.5 : 0 // Positive: 1, Neutral: 0.5, Negative: 0
      return sum + (item.value * weight)
    }, 0)
    return Math.round((weighted / total) * 100)
  }
  
  // For line/bar charts, calculate average
  const avg = data.reduce((sum, item) => sum + (item.satisfaction || item.value || 0), 0) / data.length
  return Math.round(avg)
})

const positivePercentage = computed(() => {
  const data = processedData.value
  if (chartType.value === 'doughnut') {
    const total = data.reduce((sum, item) => sum + item.value, 0)
    return Math.round((data[0]?.value || 0) / total * 100)
  }
  return 85 // Mock for other chart types
})

const neutralPercentage = computed(() => {
  const data = processedData.value
  if (chartType.value === 'doughnut') {
    const total = data.reduce((sum, item) => sum + item.value, 0)
    return Math.round((data[1]?.value || 0) / total * 100)
  }
  return 12 // Mock for other chart types
})

const negativePercentage = computed(() => {
  const data = processedData.value
  if (chartType.value === 'doughnut') {
    const total = data.reduce((sum, item) => sum + item.value, 0)
    return Math.round((data[2]?.value || 0) / total * 100)
  }
  return 3 // Mock for other chart types
})

// Methods
const createChart = async () => {
  if (!chartCanvas.value || props.loading) return
  
  await nextTick()
  
  const ctx = chartCanvas.value.getContext('2d')
  
  // Destroy existing chart
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
  
  const config = getChartConfig()
  chartInstance.value = new Chart(ctx, config)
}

const getChartConfig = () => {
  switch (chartType.value) {
    case 'doughnut':
      return getDoughnutConfig()
    case 'line':
      return getLineConfig()
    case 'bar':
      return getBarConfig()
    default:
      return getDoughnutConfig()
  }
}

const getDoughnutConfig = () => {
  const data = processedData.value
  
  return {
    type: 'doughnut',
    data: {
      labels: ['Positiva', 'Neutral', 'Negativa'],
      datasets: [{
        data: data.map(item => item.value),
        backgroundColor: [
          '#10B981', // Green for positive
          '#F59E0B', // Yellow for neutral
          '#EF4444'  // Red for negative
        ],
        borderColor: [
          '#059669',
          '#D97706',
          '#DC2626'
        ],
        borderWidth: 2,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#374151',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = Math.round((context.parsed / total) * 100)
              return `${context.label}: ${percentage}% (${context.parsed})`
            }
          }
        }
      },
      animation: {
        animateRotate: true,
        duration: 1000
      }
    }
  }
}

const getLineConfig = () => {
  const data = generateTimeSeriesData()
  
  return {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Satisfacción Promedio',
        data: data.values,
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
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#374151',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return `Satisfacción: ${context.parsed.y}%`
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
            }
          }
        },
        y: {
          min: 0,
          max: 100,
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
              return value + '%'
            }
          }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  }
}

const getBarConfig = () => {
  const data = generateChatbotComparisonData()
  
  return {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Satisfacción por Chatbot',
        data: data.values,
        backgroundColor: [
          '#3B82F6',
          '#10B981',
          '#8B5CF6',
          '#F59E0B',
          '#EF4444'
        ],
        borderColor: [
          '#2563EB',
          '#059669',
          '#7C3AED',
          '#D97706',
          '#DC2626'
        ],
        borderWidth: 2,
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          borderColor: '#374151',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return `Satisfacción: ${context.parsed.y}%`
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
            }
          }
        },
        y: {
          min: 0,
          max: 100,
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
              return value + '%'
            }
          }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  }
}

const generateMockData = () => {
  return [
    { label: 'Positiva', value: 850 },
    { label: 'Neutral', value: 120 },
    { label: 'Negativa', value: 30 }
  ]
}

const generateTimeSeriesData = () => {
  const labels = []
  const values = []
  const now = new Date()
  
  for (let i = 6; i >= 0; i--) {
    const date = new Date(now)
    date.setDate(date.getDate() - i)
    labels.push(date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }))
    
    // Generate realistic satisfaction data (80-95%)
    const baseValue = 85
    const variation = (Math.random() - 0.5) * 10
    values.push(Math.max(75, Math.min(95, Math.round(baseValue + variation))))
  }
  
  return { labels, values }
}

const generateChatbotComparisonData = () => {
  return {
    labels: ['Ventas', 'Soporte', 'FAQ', 'Técnico', 'General'],
    values: [94, 91, 88, 85, 82]
  }
}

// Watchers
watch(
  () => [props.data, props.loading, chartType.value],
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
.satisfaction-chart {
  position: relative;
}

canvas {
  max-height: 100%;
}
</style>