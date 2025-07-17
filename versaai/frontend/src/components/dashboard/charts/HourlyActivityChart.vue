<template>
  <div class="hourly-activity-chart h-full">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else class="h-full flex flex-col">
      <!-- Chart container -->
      <div class="flex-1">
        <canvas ref="chartCanvas" class="w-full h-full"></canvas>
      </div>
      
      <!-- Peak hours info -->
      <div class="mt-3 flex items-center justify-between text-xs text-gray-500">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-1">
            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Pico: {{ peakHour }}</span>
          </div>
          <div class="flex items-center space-x-1">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Valle: {{ valleyHour }}</span>
          </div>
        </div>
        <div>
          Promedio: {{ averageActivity }}
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
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
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

// Computed
const processedData = computed(() => {
  if (!props.data || props.data.length === 0) {
    return generateMockData()
  }
  return props.data
})

const peakHour = computed(() => {
  const data = processedData.value
  const maxValue = Math.max(...data.map(item => item.value || item.activity || 0))
  const peakIndex = data.findIndex(item => (item.value || item.activity || 0) === maxValue)
  return `${peakIndex}:00`
})

const valleyHour = computed(() => {
  const data = processedData.value
  const minValue = Math.min(...data.map(item => item.value || item.activity || 0))
  const valleyIndex = data.findIndex(item => (item.value || item.activity || 0) === minValue)
  return `${valleyIndex}:00`
})

const averageActivity = computed(() => {
  const data = processedData.value
  const total = data.reduce((sum, item) => sum + (item.value || item.activity || 0), 0)
  return Math.round(total / data.length)
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
  
  const data = processedData.value
  const labels = data.map((_, index) => `${index.toString().padStart(2, '0')}:00`)
  const values = data.map(item => item.value || item.activity || 0)
  
  // Create gradient colors based on activity level
  const backgroundColors = values.map(value => {
    const maxValue = Math.max(...values)
    const intensity = value / maxValue
    
    if (intensity > 0.8) {
      return '#EF4444' // High activity - Red
    } else if (intensity > 0.6) {
      return '#F59E0B' // Medium-high activity - Orange
    } else if (intensity > 0.4) {
      return '#10B981' // Medium activity - Green
    } else if (intensity > 0.2) {
      return '#3B82F6' // Low-medium activity - Blue
    } else {
      return '#6B7280' // Low activity - Gray
    }
  })
  
  const borderColors = backgroundColors.map(color => {
    // Darker version of background color
    const colorMap = {
      '#EF4444': '#DC2626',
      '#F59E0B': '#D97706',
      '#10B981': '#059669',
      '#3B82F6': '#2563EB',
      '#6B7280': '#4B5563'
    }
    return colorMap[color] || color
  })
  
  chartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Actividad',
        data: values,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1,
        borderRadius: {
          topLeft: 4,
          topRight: 4,
          bottomLeft: 0,
          bottomRight: 0
        },
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
            title: function(context) {
              const hour = context[0].label
              return `Hora: ${hour}`
            },
            label: function(context) {
              const value = context.parsed.y
              const maxValue = Math.max(...values)
              const percentage = Math.round((value / maxValue) * 100)
              return [
                `Actividad: ${value}`,
                `Intensidad: ${percentage}%`
              ]
            },
            afterLabel: function(context) {
              const value = context.parsed.y
              const maxValue = Math.max(...values)
              const minValue = Math.min(...values)
              
              if (value === maxValue) {
                return '🔥 Hora pico'
              } else if (value === minValue) {
                return '😴 Hora valle'
              } else if (value > maxValue * 0.8) {
                return '📈 Alta actividad'
              } else if (value < maxValue * 0.3) {
                return '📉 Baja actividad'
              }
              return ''
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
              size: 10
            },
            maxRotation: 0,
            callback: function(value, index) {
              // Show every 4th hour to avoid crowding
              return index % 4 === 0 ? this.getLabelForValue(value) : ''
            }
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
              size: 10
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
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart',
        delay: (context) => {
          // Stagger animation for each bar
          return context.dataIndex * 50
        }
      },
      onHover: (event, activeElements) => {
        event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default'
      }
    }
  })
}

const generateMockData = () => {
  const data = []
  
  // Generate realistic hourly activity data
  for (let hour = 0; hour < 24; hour++) {
    let activity
    
    if (hour >= 0 && hour < 6) {
      // Night hours - very low activity
      activity = Math.floor(Math.random() * 20) + 5
    } else if (hour >= 6 && hour < 9) {
      // Early morning - increasing activity
      activity = Math.floor(Math.random() * 40) + 20
    } else if (hour >= 9 && hour < 12) {
      // Morning peak - high activity
      activity = Math.floor(Math.random() * 60) + 80
    } else if (hour >= 12 && hour < 14) {
      // Lunch time - medium activity
      activity = Math.floor(Math.random() * 40) + 50
    } else if (hour >= 14 && hour < 18) {
      // Afternoon peak - highest activity
      activity = Math.floor(Math.random() * 80) + 100
    } else if (hour >= 18 && hour < 21) {
      // Evening - decreasing activity
      activity = Math.floor(Math.random() * 50) + 40
    } else {
      // Late evening - low activity
      activity = Math.floor(Math.random() * 30) + 15
    }
    
    data.push({
      hour,
      value: activity,
      activity
    })
  }
  
  return data
}

// Watchers
watch(
  () => [props.data, props.loading],
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
.hourly-activity-chart {
  position: relative;
}

canvas {
  max-height: 100%;
}
</style>