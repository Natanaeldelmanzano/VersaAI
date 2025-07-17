<template>
  <div class="system-chart">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <canvas 
      v-else
      ref="chartCanvas" 
      class="w-full h-full"
    ></canvas>
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
  BarElement,
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
    required: true
  },
  type: {
    type: String,
    default: 'line',
    validator: (value) => ['line', 'bar'].includes(value)
  },
  options: {
    type: Object,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Refs
const chartCanvas = ref(null)
const chartInstance = ref(null)

// Default options
const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    intersect: false,
    mode: 'index'
  },
  plugins: {
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      cornerRadius: 8,
      displayColors: true,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || ''
          if (label) {
            label += ': '
          }
          
          const value = context.parsed.y
          
          // Format based on dataset label
          if (label.includes('CPU') || label.includes('Memory')) {
            label += value + '%'
          } else if (label.includes('MB/s')) {
            label += value + ' MB/s'
          } else if (label.includes('Connections')) {
            label += value.toLocaleString()
          } else {
            label += value
          }
          
          return label
        }
      }
    },
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.05)'
      },
      ticks: {
        color: '#6B7280',
        font: {
          size: 12
        }
      }
    },
    y: {
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.05)'
      },
      ticks: {
        color: '#6B7280',
        font: {
          size: 12
        }
      }
    }
  },
  elements: {
    point: {
      radius: 4,
      hoverRadius: 6,
      borderWidth: 2,
      hoverBorderWidth: 3
    },
    line: {
      borderWidth: 2,
      tension: 0.4
    },
    bar: {
      borderRadius: 4,
      borderSkipped: false
    }
  },
  animation: {
    duration: 750,
    easing: 'easeInOutQuart'
  }
}

// Methods
const createChart = () => {
  if (!chartCanvas.value || !props.data) return
  
  const ctx = chartCanvas.value.getContext('2d')
  
  // Merge default options with provided options
  const mergedOptions = {
    ...defaultOptions,
    ...props.options
  }
  
  // Process data for better visualization
  const processedData = {
    ...props.data,
    datasets: props.data.datasets.map(dataset => ({
      ...dataset,
      fill: props.type === 'line' ? 'origin' : false,
      backgroundColor: props.type === 'line' 
        ? dataset.backgroundColor || 'rgba(59, 130, 246, 0.1)'
        : dataset.backgroundColor || 'rgba(59, 130, 246, 0.8)',
      borderColor: dataset.borderColor || '#3B82F6',
      pointBackgroundColor: dataset.borderColor || '#3B82F6',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: dataset.borderColor || '#3B82F6'
    }))
  }
  
  chartInstance.value = new Chart(ctx, {
    type: props.type,
    data: processedData,
    options: mergedOptions
  })
}

const destroyChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
}

const updateChart = () => {
  if (!chartInstance.value || !props.data) return
  
  // Update chart data
  chartInstance.value.data = {
    ...props.data,
    datasets: props.data.datasets.map(dataset => ({
      ...dataset,
      fill: props.type === 'line' ? 'origin' : false,
      backgroundColor: props.type === 'line' 
        ? dataset.backgroundColor || 'rgba(59, 130, 246, 0.1)'
        : dataset.backgroundColor || 'rgba(59, 130, 246, 0.8)',
      borderColor: dataset.borderColor || '#3B82F6',
      pointBackgroundColor: dataset.borderColor || '#3B82F6',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: dataset.borderColor || '#3B82F6'
    }))
  }
  
  // Update chart options if needed
  const mergedOptions = {
    ...defaultOptions,
    ...props.options
  }
  
  chartInstance.value.options = mergedOptions
  chartInstance.value.update('active')
}

// Watchers
watch(
  () => props.data,
  () => {
    if (chartInstance.value) {
      updateChart()
    } else {
      nextTick(() => {
        createChart()
      })
    }
  },
  { deep: true }
)

watch(
  () => props.options,
  () => {
    if (chartInstance.value) {
      updateChart()
    }
  },
  { deep: true }
)

watch(
  () => props.type,
  () => {
    destroyChart()
    nextTick(() => {
      createChart()
    })
  }
)

// Lifecycle
onMounted(() => {
  if (!props.loading && props.data) {
    nextTick(() => {
      createChart()
    })
  }
})

onUnmounted(() => {
  destroyChart()
})
</script>

<style scoped>
.system-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

canvas {
  display: block;
}
</style>