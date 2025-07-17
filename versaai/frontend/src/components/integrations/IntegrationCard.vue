<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 relative overflow-hidden">
    <!-- Premium/Popular Badge -->
    <div v-if="integration.isPremium || integration.isPopular" class="absolute top-3 right-3 z-10">
      <span 
        v-if="integration.isPremium" 
        class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-purple-500 to-pink-500 text-white"
      >
        Premium
      </span>
      <span 
        v-else-if="integration.isPopular" 
        class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-orange-500 to-red-500 text-white"
      >
        Popular
      </span>
    </div>

    <!-- Header -->
    <div class="p-6 pb-4">
      <div class="flex items-start justify-between">
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <img 
              :src="integration.icon" 
              :alt="integration.name" 
              class="h-12 w-12 rounded-lg object-cover"
              @error="handleImageError"
            >
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-semibold text-gray-900 truncate">
              {{ integration.name }}
            </h3>
            <p class="text-sm text-gray-500 truncate">
              {{ integration.category }}
            </p>
          </div>
        </div>
        
        <!-- Actions Dropdown -->
        <div class="relative" ref="dropdownRef">
          <button
            @click="toggleDropdown"
            class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <EllipsisVerticalIcon class="h-5 w-5" />
          </button>
          
          <div 
            v-if="showDropdown" 
            class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-20"
          >
            <div class="py-1">
              <button
                @click="handleConfigure"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <CogIcon class="h-4 w-4" />
                <span>Configurar</span>
              </button>
              <button
                @click="handleTest"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <PlayIcon class="h-4 w-4" />
                <span>Probar conexión</span>
              </button>
              <button
                @click="handleViewDetails"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <EyeIcon class="h-4 w-4" />
                <span>Ver detalles</span>
              </button>
              <hr class="my-1">
              <button
                @click="handleToggle"
                class="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 flex items-center space-x-2"
                :class="integration.status === 'active' ? 'text-red-600' : 'text-green-600'"
              >
                <component :is="integration.status === 'active' ? StopIcon : PlayIcon" class="h-4 w-4" />
                <span>{{ integration.status === 'active' ? 'Desactivar' : 'Activar' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Status -->
      <div class="mt-4 flex items-center space-x-2">
        <div class="flex items-center space-x-1">
          <div 
            class="h-2 w-2 rounded-full"
            :class="{
              'bg-green-500': integration.status === 'active',
              'bg-yellow-500': integration.status === 'pending',
              'bg-red-500': integration.status === 'error',
              'bg-gray-400': integration.status === 'inactive'
            }"
          ></div>
          <span 
            class="text-sm font-medium capitalize"
            :class="{
              'text-green-600': integration.status === 'active',
              'text-yellow-600': integration.status === 'pending',
              'text-red-600': integration.status === 'error',
              'text-gray-500': integration.status === 'inactive'
            }"
          >
            {{ getStatusText(integration.status) }}
          </span>
        </div>
      </div>

      <!-- Description -->
      <p class="mt-3 text-sm text-gray-600 line-clamp-2">
        {{ integration.description }}
      </p>
    </div>

    <!-- Metrics -->
    <div v-if="integration.metrics" class="px-6 py-4 bg-gray-50 border-t border-gray-100">
      <div class="grid grid-cols-2 gap-4">
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900">
            {{ formatNumber(integration.metrics.requests || 0) }}
          </div>
          <div class="text-xs text-gray-500">Requests</div>
        </div>
        <div class="text-center">
          <div class="text-lg font-semibold text-gray-900">
            {{ integration.metrics.uptime || '99.9' }}%
          </div>
          <div class="text-xs text-gray-500">Uptime</div>
        </div>
      </div>
    </div>

    <!-- Last Used -->
    <div v-if="integration.lastUsed" class="px-6 py-3 border-t border-gray-100">
      <div class="flex items-center justify-between text-xs text-gray-500">
        <span>Último uso:</span>
        <span>{{ formatTimeAgo(integration.lastUsed) }}</span>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="px-6 py-4 border-t border-gray-100">
      <div class="flex space-x-2">
        <button
          @click="handleConfigure"
          :disabled="isLoading"
          class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-1"
        >
          <CogIcon v-if="!isLoading" class="h-4 w-4" />
          <ArrowPathIcon v-else class="h-4 w-4 animate-spin" />
          <span>{{ isLoading ? 'Cargando...' : 'Configurar' }}</span>
        </button>
        
        <button
          @click="handleTest"
          :disabled="isLoading || integration.status === 'inactive'"
          class="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <PlayIcon class="h-4 w-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  EllipsisVerticalIcon,
  CogIcon,
  PlayIcon,
  StopIcon,
  EyeIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

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
  'toggle',
  'test',
  'view-details'
])

// Reactive state
const showDropdown = ref(false)
const isLoading = ref(false)
const dropdownRef = ref(null)

// Methods
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const closeDropdown = () => {
  showDropdown.value = false
}

const handleConfigure = () => {
  closeDropdown()
  emit('configure', props.integration)
}

const handleToggle = () => {
  closeDropdown()
  emit('toggle', props.integration)
}

const handleTest = () => {
  closeDropdown()
  emit('test', props.integration)
}

const handleViewDetails = () => {
  closeDropdown()
  emit('view-details', props.integration)
}

const handleImageError = (event) => {
  // Fallback to a default icon if image fails to load
  event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQ4IiBoZWlnaHQ9IjQ4IiByeD0iOCIgZmlsbD0iIzM3NDE1MSIvPgo8cGF0aCBkPSJNMjQgMTJDMTcuMzczIDEyIDEyIDE3LjM3MyAxMiAyNEMxMiAzMC42MjcgMTcuMzczIDM2IDI0IDM2QzMwLjYyNyAzNiAzNiAzMC42MjcgMzYgMjRDMzYgMTcuMzczIDMwLjYyNyAxMiAyNCAxMlpNMjQgMzBDMjAuNjg2IDMwIDE4IDI3LjMxNCAxOCAyNEMxOCAyMC42ODYgMjAuNjg2IDE4IDI0IDE4QzI3LjMxNCAxOCAzMCAyMC42ODYgMzAgMjRDMzAgMjcuMzE0IDI3LjMxNCAzMCAyNCAzMFoiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo='
}

const getStatusText = (status) => {
  const statusMap = {
    active: 'Activo',
    inactive: 'Inactivo',
    pending: 'Pendiente',
    error: 'Error'
  }
  return statusMap[status] || status
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
  const past = new Date(date)
  const diffInSeconds = Math.floor((now - past) / 1000)
  
  if (diffInSeconds < 60) {
    return 'Hace un momento'
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60)
    return `Hace ${minutes} min`
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600)
    return `Hace ${hours} h`
  } else {
    const days = Math.floor(diffInSeconds / 86400)
    return `Hace ${days} días`
  }
}

// Click outside handler
const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    closeDropdown()
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>