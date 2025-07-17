<template>
  <div class="revenue-chart">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <!-- Chart Container -->
    <div v-else class="relative h-full">
      <canvas ref="chartCanvas" class="w-full h-full"></canvas>
      
      <!-- No Data State -->
      <div 
        v-if="!hasData" 
        class="absolute inset-0 flex items-center justify-center bg-gray-50 rounded-lg"
      >
        <div class="text-center">
          <CurrencyDollarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p class="text-gray-500 text-sm">No hay datos de ingresos disponibles</p>
        </div>
      </div>
      
      <!-- Chart Legend -->
      <div class="absolute top-4 right-4 bg-white rounded-lg shadow-sm border border-gray-200 p-3">
        <div class="space-y-2">
          <div 
            v-for="(dataset, index) in data.datasets" 
            :key="index"
            class="flex items-center space-x-2"
          >
            <div 
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: dataset.borderColor }"
            ></div>
            <span class="text-sm text-gray-700">{{ dataset.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import { CurrencyDollarIcon } from '@heroicons/vue/24/outline'
import {
  Chart as ChartJS,
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
ChartJS.register(
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
    type: Object,
    required: true,
    default: () => ({ labels: [], datasets: [] })
  },
  loading: {
    type: Boolean,
    default: false
  },
  period: {
    type: String,
    default: '30d'
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  height: {
    type: [String, Number],
    default: '100%'
  }
})

// Refs
const chartCanvas = ref(null)
const chartInstance = ref(null)

// Computed
const hasData = computed(() => {
  return props.data?.datasets?.length > 0 && 
         props.data.datasets.some(dataset => dataset.data?.length > 0)
})

const chartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        display: false // We use custom legend
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        displayColors: true,
        callbacks: {
          title: function(context) {
            return context[0].label
          },
          label: function(context) {
            let label = context.dataset.label || ''
            if (label) {
              label += ': '
            }
            
            const value = context.parsed.y
            label += formatCurrency(value)
            
            return label
          },
          footer: function(tooltipItems) {
            let total = 0
            tooltipItems.forEach(item => {
              total += item.parsed.y
            })
            return `Total: ${formatCurrency(total)}`
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          font: {
            size: 11,
            family: 'Inter, sans-serif'
          },
          color: '#6B7280',
          maxTicksLimit: 8
        }
      },
      y: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)',
          drawBorder: false
        },
        ticks: {
          font: {
            size: 11,
            family: 'Inter, sans-serif'
          },
          color: '#6B7280',
          callback: function(value) {
            return formatCurrency(value)
          }
        },
        beginAtZero: true
      }
    },
    elements: {
      point: {
        radius: 4,
        hoverRadius: 6,
        borderWidth: 2,
        backgroundColor: '#fff'
      },
      line: {
        borderWidth: 3,
        tension: 0.4,
        fill: true
      }
    },
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart'
    }
  }
})

// Methods
const formatCurrency = (value) => {
  if (value >= 1000000) {
    return '$' + (value / 1000000).toFixed(1) + 'M'
  } else if (value >= 1000) {
    return '$' + (value / 1000).toFixed(1) + 'K'
  }
  return '$' + value.toLocaleString()
}

const createChart = async () => {
  if (!chartCanvas.value || !hasData.value) return

  await nextTick()

  try {
    const ctx = chartCanvas.value.getContext('2d')
    
    // Create gradient backgrounds for datasets
    const gradients = props.data.datasets.map((dataset, index) => {
      const gradient = ctx.createLinearGradient(0, 0, 0, 400)
      const color = dataset.borderColor
      
      if (color.includes('#')) {
        // Convert hex to rgba
        const r = parseInt(color.slice(1, 3), 16)
        const g = parseInt(color.slice(3, 5), 16)
        const b = parseInt(color.slice(5, 7), 16)
        
        gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0.3)`)
        gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0.05)`)
      } else {
        gradient.addColorStop(0, color.replace('rgb', 'rgba').replace(')', ', 0.3)'))
        gradient.addColorStop(1, color.replace('rgb', 'rgba').replace(')', ', 0.05)'))
      }
      
      return gradient
    })

    // Apply gradients to datasets
    const dataWithGradients = {
      ...props.data,
      datasets: props.data.datasets.map((dataset, index) => ({
        ...dataset,
        backgroundColor: gradients[index]
      }))
    }
    
    chartInstance.value = new ChartJS(ctx, {
      type: 'line',
      data: dataWithGradients,
      options: chartOptions.value
    })
  } catch (error) {
    console.error('Error creating revenue chart:', error)
  }
}

const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
}

const updateChart = async () => {
  if (!chartInstance.value) {
    await createChart()
    return
  }

  try {
    // Update data with new gradients
    const ctx = chartCanvas.value.getContext('2d')
    const gradients = props.data.datasets.map((dataset, index) => {
      const gradient = ctx.createLinearGradient(0, 0, 0, 400)
      const color = dataset.borderColor
      
      if (color.includes('#')) {
        const r = parseInt(color.slice(1, 3), 16)
        const g = parseInt(color.slice(3, 5), 16)
        const b = parseInt(color.slice(5, 7), 16)
        
        gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0.3)`)
        gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0.05)`)
      } else {
        gradient.addColorStop(0, color.replace('rgb', 'rgba').replace(')', ', 0.3)'))
        gradient.addColorStop(1, color.replace('rgb', 'rgba').replace(')', ', 0.05)'))
      }
      
      return gradient
    })

    const dataWithGradients = {
      ...props.data,
      datasets: props.data.datasets.map((dataset, index) => ({
        ...dataset,
        backgroundColor: gradients[index]
      }))
    }

    chartInstance.value.data = dataWithGradients
    chartInstance.value.options = chartOptions.value
    chartInstance.value.update('active')
  } catch (error) {
    console.error('Error updating revenue chart:', error)
    // Recreate chart if update fails
    destroyChart()
    await createChart()
  }
}

const resizeChart = () => {
  if (chartInstance.value) {
    chartInstance.value.resize()
  }
}

// Watchers
watch(
  () => props.data,
  async () => {
    if (!props.loading) {
      await updateChart()
    }
  },
  { deep: true }
)

watch(
  () => props.period,
  async () => {
    if (!props.loading && chartInstance.value) {
      await updateChart()
    }
  }
)

watch(
  () => props.loading,
  async (newLoading) => {
    if (!newLoading && hasData.value) {
      await nextTick()
      await createChart()
    } else if (newLoading) {
      destroyChart()
    }
  }
)

// Lifecycle
onMounted(async () => {
  if (!props.loading && hasData.value) {
    await createChart()
  }

  // Add resize listener
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  destroyChart()
  window.removeEventListener('resize', resizeChart)
})

// Expose methods for parent components
defineExpose({
  chart: chartInstance,
  updateChart,
  resizeChart
})
</script>

<style scoped>
.revenue-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

.revenue-chart canvas {
  max-width: 100%;
  height: auto;
}

/* Animation for loading state */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Custom legend styles */
.revenue-chart .legend {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .revenue-chart {
    font-size: 0.875rem;
  }
  
  .revenue-chart .legend {
    position: static;
    margin-top: 1rem;
  }
}
</style>