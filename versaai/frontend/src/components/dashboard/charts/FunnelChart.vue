<template>
  <div class="funnel-chart">
    <div class="space-y-3">
      <div 
        v-for="(stage, index) in data" 
        :key="stage.stage"
        class="relative"
      >
        <!-- Funnel Stage -->
        <div class="flex items-center space-x-4">
          <!-- Stage Number -->
          <div class="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
            {{ index + 1 }}
          </div>
          
          <!-- Funnel Bar -->
          <div class="flex-1">
            <div class="flex items-center justify-between mb-1">
              <span class="text-sm font-medium text-gray-900">{{ stage.stage }}</span>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-600">{{ stage.value.toLocaleString() }}</span>
                <span class="text-xs text-gray-500">({{ stage.percentage }}%)</span>
              </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 rounded-full h-8 relative overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-500 ease-out"
                :class="getStageColor(index)"
                :style="{ width: stage.percentage + '%' }"
              >
                <!-- Gradient overlay -->
                <div class="absolute inset-0 bg-gradient-to-r from-transparent to-white opacity-20"></div>
              </div>
              
              <!-- Value label inside bar -->
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-xs font-medium text-white drop-shadow-sm">
                  {{ stage.value.toLocaleString() }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Drop-off indicator -->
        <div v-if="index < data.length - 1" class="flex items-center justify-center mt-2 mb-1">
          <div class="flex items-center space-x-2 text-xs text-gray-500">
            <div class="w-4 h-px bg-gray-300"></div>
            <span>{{ getDropOffPercentage(index) }}% abandono</span>
            <div class="w-4 h-px bg-gray-300"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Summary Stats -->
    <div class="mt-6 pt-4 border-t border-gray-200">
      <div class="grid grid-cols-3 gap-4 text-center">
        <div>
          <p class="text-2xl font-semibold text-gray-900">{{ conversionRate }}%</p>
          <p class="text-sm text-gray-600">Tasa de Conversión</p>
        </div>
        <div>
          <p class="text-2xl font-semibold text-gray-900">{{ totalDropOff }}%</p>
          <p class="text-sm text-gray-600">Abandono Total</p>
        </div>
        <div>
          <p class="text-2xl font-semibold text-gray-900">{{ avgStageConversion }}%</p>
          <p class="text-sm text-gray-600">Conversión Promedio</p>
        </div>
      </div>
    </div>
    
    <!-- Insights -->
    <div class="mt-4 p-4 bg-blue-50 rounded-lg">
      <h4 class="text-sm font-medium text-blue-900 mb-2">💡 Insights</h4>
      <ul class="text-sm text-blue-800 space-y-1">
        <li v-for="insight in insights" :key="insight">• {{ insight }}</li>
      </ul>
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

const conversionRate = computed(() => {
  if (props.data.length === 0) return 0
  const first = props.data[0]?.value || 0
  const last = props.data[props.data.length - 1]?.value || 0
  return first > 0 ? ((last / first) * 100).toFixed(1) : 0
})

const totalDropOff = computed(() => {
  return (100 - parseFloat(conversionRate.value)).toFixed(1)
})

const avgStageConversion = computed(() => {
  if (props.data.length <= 1) return 0
  
  let totalConversion = 0
  for (let i = 1; i < props.data.length; i++) {
    const current = props.data[i].value
    const previous = props.data[i - 1].value
    if (previous > 0) {
      totalConversion += (current / previous) * 100
    }
  }
  
  return (totalConversion / (props.data.length - 1)).toFixed(1)
})

const insights = computed(() => {
  const insights = []
  
  // Find biggest drop-off
  let maxDropOff = 0
  let maxDropOffStage = ''
  
  for (let i = 1; i < props.data.length; i++) {
    const dropOff = getDropOffPercentage(i - 1)
    if (dropOff > maxDropOff) {
      maxDropOff = dropOff
      maxDropOffStage = props.data[i - 1].stage
    }
  }
  
  if (maxDropOff > 0) {
    insights.push(`Mayor abandono en "${maxDropOffStage}" (${maxDropOff}%)`)
  }
  
  // Conversion rate insight
  const rate = parseFloat(conversionRate.value)
  if (rate > 15) {
    insights.push('Excelente tasa de conversión general')
  } else if (rate > 10) {
    insights.push('Buena tasa de conversión, hay oportunidades de mejora')
  } else {
    insights.push('Tasa de conversión baja, revisar proceso')
  }
  
  return insights
})

const getStageColor = (index) => {
  const colors = [
    'bg-blue-500',
    'bg-blue-600',
    'bg-indigo-500',
    'bg-indigo-600',
    'bg-purple-500',
    'bg-purple-600'
  ]
  return colors[index % colors.length]
}

const getDropOffPercentage = (index) => {
  if (index >= props.data.length - 1) return 0
  
  const current = props.data[index].value
  const next = props.data[index + 1].value
  
  if (current === 0) return 0
  
  return ((current - next) / current * 100).toFixed(1)
}
</script>

<style scoped>
.funnel-chart {
  @apply w-full;
}
</style>