<template>
  <div class="widget-chart">
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
  ArcElement,
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
  ArcElement,
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
    validator: (value) => ['line', 'bar', 'doughnut', 'pie'].includes(value)
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
          
          const value = context.parsed.y !== undefined ? context.parsed.y : context.parsed
          
          // Format based on chart type and data
          if (props.type === 'doughnut' || props.type === 'pie') {
            const total = context.dataset.data.reduce((a, b) => a + b, 0)
            const percentage = ((value / total) * 100).toFixed(1)
            label += `${value} (${percentage}%)`
          } else {
            // Format numbers with locale
            label += value.toLocaleString()
          }
          
          return label
        }
      }
    },
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12
        }
      }
    }
  },
  scales: {
    x: {
      display: props.type !== 'doughnut' && props.type !== 'pie',
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
      display: props.type !== 'doughnut' && props.type !== 'pie',
      grid: {
        display: true,
        color: 'rgba(0, 0, 0, 0.05)'
      },
      ticks: {
        color: '#6B7280',
        font: {
          size: 12
        },
        callback: function(value) {
          return value.toLocaleString()
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
    },
    arc: {
      borderWidth: 2,
      hoverBorderWidth: 3
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
  
  // Process data based on chart type
  const processedData = {
    ...props.data,
    datasets: props.data.datasets.map((dataset, index) => {
      const baseColors = [
        '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
        '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
      ]
      
      if (props.type === 'doughnut' || props.type === 'pie') {
        return {
          ...dataset,
          backgroundColor: dataset.backgroundColor || baseColors.slice(0, dataset.data.length),
          borderColor: '#fff',
          borderWidth: 2
        }
      } else if (props.type === 'line') {
        return {
          ...dataset,
          fill: 'origin',
          backgroundColor: dataset.backgroundColor || `${baseColors[index % baseColors.length]}20`,
          borderColor: dataset.borderColor || baseColors[index % baseColors.length],
          pointBackgroundColor: dataset.borderColor || baseColors[index % baseColors.length],
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: dataset.borderColor || baseColors[index % baseColors.length]
        }
      } else {
        return {
          ...dataset,
          backgroundColor: dataset.backgroundColor || `${baseColors[index % baseColors.length]}80`,
          borderColor: dataset.borderColor || baseColors[index % baseColors.length],
          borderWidth: 1
        }
      }
    })
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
  
  // Process data based on chart type
  const processedData = {
    ...props.data,
    datasets: props.data.datasets.map((dataset, index) => {
      const baseColors = [
        '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
        '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
      ]
      
      if (props.type === 'doughnut' || props.type === 'pie') {
        return {
          ...dataset,
          backgroundColor: dataset.backgroundColor || baseColors.slice(0, dataset.data.length),
          borderColor: '#fff',
          borderWidth: 2
        }
      } else if (props.type === 'line') {
        return {
          ...dataset,
          fill: 'origin',
          backgroundColor: dataset.backgroundColor || `${baseColors[index % baseColors.length]}20`,
          borderColor: dataset.borderColor || baseColors[index % baseColors.length],
          pointBackgroundColor: dataset.borderColor || baseColors[index % baseColors.length],
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: dataset.borderColor || baseColors[index % baseColors.length]
        }
      } else {
        return {
          ...dataset,
          backgroundColor: dataset.backgroundColor || `${baseColors[index % baseColors.length]}80`,
          borderColor: dataset.borderColor || baseColors[index % baseColors.length],
          borderWidth: 1
        }
      }
    })
  }
  
  // Update chart data
  chartInstance.value.data = processedData
  
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
.widget-chart {
  position: relative;
  width: 100%;
  height: 100%;
}

canvas {
  display: block;
}
</style>