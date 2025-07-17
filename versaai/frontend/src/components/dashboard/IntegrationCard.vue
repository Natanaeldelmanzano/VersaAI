<template>
  <div class="integration-card group relative bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-300 hover:shadow-lg dark:hover:shadow-blue-500/10">
    <!-- Premium Badge -->
    <div v-if="integration.isPremium" class="absolute -top-2 -right-2 z-10">
      <div class="bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg">
        <StarIcon class="w-3 h-3 inline mr-1" />
        PRO
      </div>
    </div>

    <!-- Popular Badge -->
    <div v-if="integration.isPopular && !integration.isPremium" class="absolute -top-2 -right-2 z-10">
      <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs font-bold px-2 py-1 rounded-full shadow-lg">
        <TrendingUp class="w-3 h-3 inline mr-1" />
        Popular
      </div>
    </div>

    <div class="p-6">
      <!-- Header -->
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center space-x-3">
          <!-- Icon -->
          <div class="flex-shrink-0">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-700 dark:to-gray-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <component :is="getIcon(integration.icon)" class="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          
          <!-- Name and Status -->
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {{ integration.name }}
            </h3>
            <div class="flex items-center space-x-2 mt-1">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium" :class="statusClasses">
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="statusDotClasses"></span>
                {{ statusText }}
              </span>
              <span class="text-xs text-gray-500 dark:text-gray-400 capitalize">
                {{ integration.category }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Actions Dropdown -->
        <div class="relative" ref="dropdownRef">
          <button
            @click="toggleDropdown"
            class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            :class="{ 'text-blue-600 dark:text-blue-400': showDropdown }"
          >
            <EllipsisVerticalIcon class="w-5 h-5" />
          </button>
          
          <!-- Dropdown Menu -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div
              v-if="showDropdown"
              class="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-20"
            >
              <button
                @click="handleConfigure"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2"
              >
                <CogIcon class="w-4 h-4" />
                <span>Configurar</span>
              </button>
              
              <button
                @click="handleTest"
                :disabled="isTestingIntegration"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <PlayIcon class="w-4 h-4" :class="{ 'animate-spin': isTestingIntegration }" />
                <span>{{ isTestingIntegration ? 'Probando...' : 'Probar' }}</span>
              </button>
              
              <button
                @click="handleToggle"
                :disabled="isTogglingIntegration"
                class="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                :class="integration.status === 'active' ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'"
              >
                <component :is="integration.status === 'active' ? PauseIcon : PlayIcon" class="w-4 h-4" />
                <span>
                  {{ isTogglingIntegration ? 'Cambiando...' : (integration.status === 'active' ? 'Desactivar' : 'Activar') }}
                </span>
              </button>
              
              <hr class="my-1 border-gray-200 dark:border-gray-700" />
              
              <button
                @click="handleViewDetails"
                class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center space-x-2"
              >
                <EyeIcon class="w-4 h-4" />
                <span>Ver detalles</span>
              </button>
            </div>
          </Transition>
        </div>
      </div>
    
      <!-- Description -->
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
        {{ integration.description }}
      </p>

      <!-- Metrics -->
      <div v-if="integration.metrics" class="grid grid-cols-2 gap-4 mb-4">
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ formatNumber(integration.metrics.totalRequests) }}
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Requests</div>
        </div>
        
        <div class="text-center">
          <div class="text-lg font-semibold" :class="getSuccessRateColor(integration.metrics.successRate)">
            {{ integration.metrics.successRate }}%
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Success Rate</div>
        </div>
        
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ integration.metrics.avgResponseTime }}ms
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Avg Response</div>
        </div>
        
        <div class="text-center">
          <div class="text-lg font-semibold" :class="getUptimeColor(integration.metrics.uptime)">
            {{ integration.metrics.uptime }}%
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Uptime</div>
        </div>
      </div>

      <!-- Last Used -->
      <div v-if="integration.metrics?.lastUsed" class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-4">
        <span>Último uso:</span>
        <span>{{ formatTimeAgo(integration.metrics.lastUsed) }}</span>
      </div>

      <!-- Quick Actions -->
      <div class="flex space-x-2">
        <button
          @click="handleConfigure"
          class="flex-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors flex items-center justify-center space-x-1"
        >
          <CogIcon class="w-4 h-4" />
          <span>Configurar</span>
        </button>
        
        <button
          @click="handleTest"
          :disabled="isTestingIntegration"
          class="flex-1 bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors flex items-center justify-center space-x-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <PlayIcon class="w-4 h-4" :class="{ 'animate-spin': isTestingIntegration }" />
          <span>{{ isTestingIntegration ? 'Probando...' : 'Probar' }}</span>
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isTogglingIntegration" class="absolute inset-0 bg-white/80 dark:bg-gray-800/80 rounded-xl flex items-center justify-center">
      <div class="flex items-center space-x-2 text-blue-600 dark:text-blue-400">
        <div class="w-5 h-5 border-2 border-blue-600 dark:border-blue-400 border-t-transparent rounded-full animate-spin"></div>
        <span class="text-sm font-medium">Actualizando...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  EllipsisVerticalIcon,
  CogIcon,
  PlayIcon,
  PauseIcon,
  EyeIcon,
  StarIcon,
  TrendingUp,
  MessageSquare,
  Users,
  MessageCircle,
  Building,
  Target,
  Zap,
  Settings,
  BarChart3,
  PieChart,
  CreditCard,
  Wallet
} from 'lucide-vue-next'
import { useIntegrations } from '@/composables/useIntegrations'

// Props
const props = defineProps({
  integration: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits([
  'configure',
  'test',
  'toggle',
  'view-details'
])

// Composables
const { toggleIntegration, testIntegration } = useIntegrations()

// State
const showDropdown = ref(false)
const dropdownRef = ref(null)
const isTestingIntegration = ref(false)
const isTogglingIntegration = ref(false)

// Icon mapping
const iconComponents = {
  MessageSquare,
  Users,
  MessageCircle,
  Building,
  Target,
  TrendingUp,
  Zap,
  Settings,
  BarChart3,
  PieChart,
  CreditCard,
  Wallet
}

// Computed
const statusClasses = computed(() => {
  switch (props.integration.status) {
    case 'active':
      return 'bg-green-100 dark:bg-green-900/20 text-green-800 dark:text-green-400'
    case 'inactive':
      return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-400'
    case 'error':
      return 'bg-red-100 dark:bg-red-900/20 text-red-800 dark:text-red-400'
    case 'warning':
      return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-400'
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-400'
  }
})

const statusDotClasses = computed(() => {
  switch (props.integration.status) {
    case 'active':
      return 'bg-green-500'
    case 'inactive':
      return 'bg-gray-400'
    case 'error':
      return 'bg-red-500'
    case 'warning':
      return 'bg-yellow-500'
    default:
      return 'bg-gray-400'
  }
})

const statusText = computed(() => {
  switch (props.integration.status) {
    case 'active':
      return 'Activo'
    case 'inactive':
      return 'Inactivo'
    case 'error':
      return 'Error'
    case 'warning':
      return 'Advertencia'
    default:
      return 'Desconocido'
  }
})

// Methods
const getIcon = (iconName) => {
  return iconComponents[iconName] || Settings
}

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const closeDropdown = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

const handleConfigure = () => {
  showDropdown.value = false
  emit('configure', props.integration)
}

const handleTest = async () => {
  if (isTestingIntegration.value) return
  
  showDropdown.value = false
  isTestingIntegration.value = true
  
  try {
    await testIntegration(props.integration.id)
    emit('test', props.integration)
  } catch (error) {
    console.error('Error testing integration:', error)
  } finally {
    isTestingIntegration.value = false
  }
}

const handleToggle = async () => {
  if (isTogglingIntegration.value) return
  
  showDropdown.value = false
  isTogglingIntegration.value = true
  
  try {
    await toggleIntegration(props.integration.id)
    emit('toggle', props.integration)
  } catch (error) {
    console.error('Error toggling integration:', error)
  } finally {
    isTogglingIntegration.value = false
  }
}

const handleViewDetails = () => {
  showDropdown.value = false
  emit('view-details', props.integration)
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatTimeAgo = (date) => {
  const now = new Date()
  const diff = now - new Date(date)
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (days > 0) {
    return `hace ${days} día${days > 1 ? 's' : ''}`
  } else if (hours > 0) {
    return `hace ${hours} hora${hours > 1 ? 's' : ''}`
  } else if (minutes > 0) {
    return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
  } else {
    return 'hace un momento'
  }
}

const getSuccessRateColor = (rate) => {
  if (rate >= 99) return 'text-green-600 dark:text-green-400'
  if (rate >= 95) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}

const getUptimeColor = (uptime) => {
  if (uptime >= 99) return 'text-green-600 dark:text-green-400'
  if (uptime >= 95) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>