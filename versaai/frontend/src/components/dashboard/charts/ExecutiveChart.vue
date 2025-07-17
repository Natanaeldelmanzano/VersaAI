<template>
  <div class="executive-chart">
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
          <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p class="text-gray-500 text-sm">No hay datos disponibles</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
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
  BarElement,
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
  type: {
    type: String,
    default: 'line',
    validator: (value) => ['line', 'bar', 'doughnut', 'pie', 'radar'].includes(value)
  },
  options: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
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

const defaultOptions = computed(() => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12,
            family: 'Inter, sans-serif'
          }
        }
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
            
            // Format numbers based on type
            const value = context.parsed.y || context.parsed
            if (typeof value === 'number') {
              if (value >= 1000000) {
                label += (value / 1000000).toFixed(1) + 'M'
              } else if (value >= 1000) {
                label += (value / 1000).toFixed(1) + 'K'
              } else {
                label += value.toLocaleString()
              }
            } else {
              label += value
            }
            
            return label
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)'
        },
        ticks: {
          font: {
            size: 11,
            family: 'Inter, sans-serif'
          },
          color: '#6B7280'
        }
      },
      y: {
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)'
        },
        ticks: {
          font: {
            size: 11,
            family: 'Inter, sans-serif'
          },
          color: '#6B7280',
          callback: function(value) {
            if (value >= 1000000) {
              return (value / 1000000).toFixed(1) + 'M'
            } else if (value >= 1000) {
              return (value / 1000).toFixed(1) + 'K'
            }
            return value.toLocaleString()
          }
        }
      }
    },
    elements: {
      point: {
        radius: 4,
        hoverRadius: 6,
        borderWidth: 2
      },
      line: {
        borderWidth: 3,
        tension: 0.4
      },
      bar: {
        borderRadius: 4,
        borderSkipped: false
      }
    }
  }

  // Type-specific options
  if (props.type === 'doughnut' || props.type === 'pie') {
    delete baseOptions.scales
    baseOptions.plugins.legend.position = 'right'
  }

  if (props.type === 'radar') {
    delete baseOptions.scales
    baseOptions.scales = {
      r: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        pointLabels: {
          font: {
            size: 11,
            family: 'Inter, sans-serif'
          },
          color: '#6B7280'
        }
      }
    }
  }

  return baseOptions
})

const mergedOptions = computed(() => {
  return {
    ...defaultOptions.value,
    ...props.options
  }
})

// Methods
const createChart = async () => {
  if (!chartCanvas.value || !hasData.value) return

  await nextTick()

  try {
    const ctx = chartCanvas.value.getContext('2d')
    
    chartInstance.value = new ChartJS(ctx, {
      type: props.type,
      data: props.data,
      options: mergedOptions.value
    })
  } catch (error) {
    console.error('Error creating chart:', error)
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
    // Update data
    chartInstance.value.data = props.data
    chartInstance.value.options = mergedOptions.value
    chartInstance.value.update('active')
  } catch (error) {
    console.error('Error updating chart:', error)
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
  () => props.options,
  async () => {
    if (!props.loading && chartInstance.value) {
      await updateChart()
    }
  },
  { deep: true }
)

watch(
  () => props.type,
  async () => {
    destroyChart()
    if (!props.loading) {
      await createChart()
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
.executive-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

.executive-chart canvas {
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

/* Responsive adjustments */
@media (max-width: 640px) {
  .executive-chart {
    font-size: 0.875rem;
  }
}
</style>