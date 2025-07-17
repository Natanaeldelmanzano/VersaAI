<template>
  <div class="metric-card bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-300">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <div class="flex items-center space-x-3">
          <div 
            :class="[
              'w-12 h-12 rounded-lg flex items-center justify-center',
              colorClasses.bg
            ]"
          >
            <component 
              :is="iconComponent" 
              :class="['w-6 h-6', colorClasses.text]"
            />
          </div>
          <div>
            <p class="text-sm font-medium text-gray-600">{{ title }}</p>
            <div class="flex items-baseline space-x-2">
              <p 
                v-if="!loading"
                class="text-2xl font-bold text-gray-900 animate-fade-in"
              >
                {{ formattedValue }}
              </p>
              <div 
                v-else
                class="h-8 w-20 bg-gray-200 rounded animate-pulse"
              ></div>
              
              <div 
                v-if="change && !loading"
                :class="[
                  'flex items-center text-sm font-medium',
                  trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600'
                ]"
              >
                <component 
                  :is="trendIcon"
                  class="w-4 h-4 mr-1"
                />
                {{ change }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mini chart o indicador visual -->
      <div class="ml-4">
        <div 
          v-if="!loading"
          class="w-16 h-8 relative"
        >
          <!-- Mini sparkline simulado -->
          <svg class="w-full h-full" viewBox="0 0 64 32">
            <path
              :d="sparklinePath"
              :stroke="colorClasses.stroke"
              stroke-width="2"
              fill="none"
              class="animate-draw"
            />
            <defs>
              <linearGradient :id="`gradient-${color}`" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" :stop-color="colorClasses.stroke" stop-opacity="0.3"/>
                <stop offset="100%" :stop-color="colorClasses.stroke" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <path
              :d="sparklineAreaPath"
              :fill="`url(#gradient-${color})`"
              class="animate-fade-in"
            />
          </svg>
        </div>
        <div 
          v-else
          class="w-16 h-8 bg-gray-200 rounded animate-pulse"
        ></div>
      </div>
    </div>
    
    <!-- Progress bar para métricas de porcentaje -->
    <div 
      v-if="showProgress && !loading"
      class="mt-4"
    >
      <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
        <span>Progreso</span>
        <span>{{ progressPercentage }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          :class="['h-2 rounded-full transition-all duration-1000 ease-out', colorClasses.progress]"
          :style="{ width: progressPercentage + '%' }"
        ></div>
      </div>
    </div>
    
    <!-- Información adicional -->
    <div 
      v-if="subtitle && !loading"
      class="mt-3 text-xs text-gray-500"
    >
      {{ subtitle }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  ChatBubbleLeftRightIcon,
  UsersIcon,
  HeartIcon,
  ClockIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  MinusIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  change: {
    type: String,
    default: null
  },
  trend: {
    type: String,
    default: 'neutral',
    validator: (value) => ['up', 'down', 'neutral'].includes(value)
  },
  icon: {
    type: String,
    default: 'ChartBarIcon'
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'green', 'purple', 'orange', 'red', 'gray'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progressValue: {
    type: Number,
    default: 0
  },
  subtitle: {
    type: String,
    default: null
  }
})

// Computed
const iconComponent = computed(() => {
  const iconMap = {
    ChatBubbleLeftRightIcon,
    UsersIcon,
    HeartIcon,
    ClockIcon,
    CurrencyDollarIcon,
    ChartBarIcon
  }
  return iconMap[props.icon] || ChartBarIcon
})

const trendIcon = computed(() => {
  switch (props.trend) {
    case 'up':
      return ArrowTrendingUpIcon
    case 'down':
      return ArrowTrendingDownIcon
    default:
      return MinusIcon
  }
})

const colorClasses = computed(() => {
  const colorMap = {
    blue: {
      bg: 'bg-blue-100',
      text: 'text-blue-600',
      stroke: '#3B82F6',
      progress: 'bg-blue-500'
    },
    green: {
      bg: 'bg-green-100',
      text: 'text-green-600',
      stroke: '#10B981',
      progress: 'bg-green-500'
    },
    purple: {
      bg: 'bg-purple-100',
      text: 'text-purple-600',
      stroke: '#8B5CF6',
      progress: 'bg-purple-500'
    },
    orange: {
      bg: 'bg-orange-100',
      text: 'text-orange-600',
      stroke: '#F59E0B',
      progress: 'bg-orange-500'
    },
    red: {
      bg: 'bg-red-100',
      text: 'text-red-600',
      stroke: '#EF4444',
      progress: 'bg-red-500'
    },
    gray: {
      bg: 'bg-gray-100',
      text: 'text-gray-600',
      stroke: '#6B7280',
      progress: 'bg-gray-500'
    }
  }
  return colorMap[props.color] || colorMap.blue
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    // Format large numbers
    if (props.value >= 1000000) {
      return (props.value / 1000000).toFixed(1) + 'M'
    } else if (props.value >= 1000) {
      return (props.value / 1000).toFixed(1) + 'K'
    }
    return props.value.toLocaleString()
  }
  return props.value
})

const progressPercentage = computed(() => {
  if (props.showProgress) {
    return Math.min(Math.max(props.progressValue, 0), 100)
  }
  // Auto-calculate from value if it's a percentage
  if (typeof props.value === 'string' && props.value.includes('%')) {
    return parseInt(props.value.replace('%', ''))
  }
  return 0
})

// Generate sparkline path (simulated data)
const sparklinePath = computed(() => {
  const points = generateSparklineData()
  let path = `M 0 ${points[0]}`
  for (let i = 1; i < points.length; i++) {
    path += ` L ${(i * 64) / (points.length - 1)} ${points[i]}`
  }
  return path
})

const sparklineAreaPath = computed(() => {
  const points = generateSparklineData()
  let path = `M 0 32`
  path += ` L 0 ${points[0]}`
  for (let i = 1; i < points.length; i++) {
    path += ` L ${(i * 64) / (points.length - 1)} ${points[i]}`
  }
  path += ` L 64 32 Z`
  return path
})

// Methods
const generateSparklineData = () => {
  // Generate trend-based sparkline data
  const baseValue = 16
  const points = []
  let currentValue = baseValue
  
  for (let i = 0; i < 8; i++) {
    if (props.trend === 'up') {
      currentValue += Math.random() * 4 - 1
    } else if (props.trend === 'down') {
      currentValue += Math.random() * 2 - 3
    } else {
      currentValue += Math.random() * 6 - 3
    }
    
    // Keep within bounds
    currentValue = Math.max(4, Math.min(28, currentValue))
    points.push(currentValue)
  }
  
  return points
}
</script>

<style scoped>
.metric-card {
  @apply transform transition-all duration-300;
}

.metric-card:hover {
  @apply scale-105;
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

.animate-draw {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: draw 1.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>