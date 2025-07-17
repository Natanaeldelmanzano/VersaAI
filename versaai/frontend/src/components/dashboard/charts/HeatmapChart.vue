<template>
  <div class="heatmap-chart">
    <div class="grid grid-cols-24 gap-1">
      <!-- Hour labels -->
      <div class="col-span-24 grid grid-cols-24 gap-1 mb-2">
        <div v-for="hour in 24" :key="hour" class="text-xs text-gray-500 text-center">
          {{ hour - 1 }}
        </div>
      </div>
      
      <!-- Heatmap grid -->
      <div v-for="(day, dayIndex) in days" :key="day" class="col-span-24 grid grid-cols-24 gap-1 mb-1">
        <div 
          v-for="hour in 24" 
          :key="`${day}-${hour}`"
          :class="getHeatmapCellClass(dayIndex, hour - 1)"
          :title="`${day} ${hour - 1}:00 - ${getValueForCell(dayIndex, hour - 1)} interacciones`"
          class="h-6 rounded cursor-pointer transition-all duration-200 hover:scale-110"
        >
        </div>
      </div>
    </div>
    
    <!-- Day labels -->
    <div class="flex justify-between mt-2">
      <div v-for="day in days" :key="day" class="text-xs text-gray-500">
        {{ day }}
      </div>
    </div>
    
    <!-- Legend -->
    <div class="flex items-center justify-center mt-4 space-x-2">
      <span class="text-xs text-gray-500">Menos</span>
      <div class="flex space-x-1">
        <div class="w-3 h-3 bg-gray-100 rounded"></div>
        <div class="w-3 h-3 bg-blue-100 rounded"></div>
        <div class="w-3 h-3 bg-blue-200 rounded"></div>
        <div class="w-3 h-3 bg-blue-400 rounded"></div>
        <div class="w-3 h-3 bg-blue-600 rounded"></div>
      </div>
      <span class="text-xs text-gray-500">Más</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

// Create a matrix for easier access
const dataMatrix = computed(() => {
  const matrix = Array(7).fill().map(() => Array(24).fill(0))
  
  props.data.forEach(item => {
    const dayIndex = days.indexOf(item.day)
    if (dayIndex !== -1 && item.hour >= 0 && item.hour < 24) {
      matrix[dayIndex][item.hour] = item.value
    }
  })
  
  return matrix
})

// Get max value for normalization
const maxValue = computed(() => {
  return Math.max(...props.data.map(item => item.value), 1)
})

const getValueForCell = (dayIndex, hour) => {
  return dataMatrix.value[dayIndex]?.[hour] || 0
}

const getHeatmapCellClass = (dayIndex, hour) => {
  const value = getValueForCell(dayIndex, hour)
  const intensity = value / maxValue.value
  
  if (intensity === 0) return 'bg-gray-100'
  if (intensity <= 0.2) return 'bg-blue-100'
  if (intensity <= 0.4) return 'bg-blue-200'
  if (intensity <= 0.6) return 'bg-blue-300'
  if (intensity <= 0.8) return 'bg-blue-400'
  return 'bg-blue-600'
}
</script>

<style scoped>
.heatmap-chart {
  @apply w-full;
}
</style>