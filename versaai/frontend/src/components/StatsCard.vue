<template>
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div class="w-8 h-8 rounded-md flex items-center justify-center" :class="iconBgClass">
            <span class="text-white text-sm">{{ icon }}</span>
          </div>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">
              {{ title }}
            </dt>
            <dd class="flex items-baseline">
              <div class="text-2xl font-semibold text-gray-900">
                {{ formattedValue }}
              </div>
              <div v-if="change" class="ml-2 flex items-baseline text-sm font-semibold" :class="changeClass">
                <svg class="self-center flex-shrink-0 h-5 w-5" :class="changeIconClass" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path v-if="change > 0" fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 6.414 6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  <path v-else fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L10 13.586l3.293-3.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span class="sr-only"> {{ change > 0 ? 'Increased' : 'Decreased' }} by </span>
                {{ Math.abs(change) }}%
              </div>
            </dd>
          </dl>
        </div>
      </div>
      <div v-if="description" class="mt-3">
        <p class="text-xs text-gray-500">{{ description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  icon: {
    type: String,
    required: true
  },
  iconColor: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'green', 'yellow', 'purple', 'red', 'indigo', 'pink', 'gray'].includes(value)
  },
  change: {
    type: Number,
    default: null
  },
  description: {
    type: String,
    default: ''
  },
  format: {
    type: String,
    default: 'number',
    validator: (value) => ['number', 'currency', 'percentage', 'time'].includes(value)
  }
})

const iconBgClass = computed(() => {
  const colorMap = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500',
    red: 'bg-red-500',
    indigo: 'bg-indigo-500',
    pink: 'bg-pink-500',
    gray: 'bg-gray-500'
  }
  return colorMap[props.iconColor] || 'bg-blue-500'
})

const formattedValue = computed(() => {
  const value = props.value
  
  switch (props.format) {
    case 'currency':
      return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
      }).format(value)
    
    case 'percentage':
      return `${value}%`
    
    case 'time':
      return `${value}ms`
    
    case 'number':
    default:
      if (typeof value === 'number') {
        return new Intl.NumberFormat('es-ES').format(value)
      }
      return value
  }
})

const changeClass = computed(() => {
  if (props.change === null) return ''
  return props.change > 0 ? 'text-green-600' : 'text-red-600'
})

const changeIconClass = computed(() => {
  if (props.change === null) return ''
  return props.change > 0 ? 'text-green-500' : 'text-red-500'
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>