<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Sesiones Activas</h2>
          <p class="text-sm text-gray-600 mt-1">Gestiona tus sesiones activas en diferentes dispositivos</p>
        </div>
        
        <div class="flex items-center space-x-3">
          <button
            @click="refreshSessions"
            :disabled="loading"
            class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50"
            title="Actualizar sesiones"
          >
            <ArrowPathIcon :class="{ 'animate-spin': loading }" class="h-5 w-5" />
          </button>
          
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-blue-50 rounded-lg p-4">
            <div class="flex items-center">
              <ComputerDesktopIcon class="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <p class="text-2xl font-bold text-blue-600">{{ stats.totalSessions }}</p>
                <p class="text-sm text-blue-600">Total Sesiones</p>
              </div>
            </div>
          </div>
          
          <div class="bg-green-50 rounded-lg p-4">
            <div class="flex items-center">
              <CheckCircleIcon class="h-8 w-8 text-green-600 mr-3" />
              <div>
                <p class="text-2xl font-bold text-green-600">{{ stats.activeSessions }}</p>
                <p class="text-sm text-green-600">Activas</p>
              </div>
            </div>
          </div>
          
          <div class="bg-yellow-50 rounded-lg p-4">
            <div class="flex items-center">
              <ClockIcon class="h-8 w-8 text-yellow-600 mr-3" />
              <div>
                <p class="text-2xl font-bold text-yellow-600">{{ stats.lastActivity }}</p>
                <p class="text-sm text-yellow-600">Última actividad</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Current Session Alert -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div class="flex items-start">
            <InformationCircleIcon class="h-5 w-5 text-blue-600 mt-0.5 mr-3" />
            <div>
              <h3 class="text-sm font-medium text-blue-900">Sesión Actual</h3>
              <p class="text-sm text-blue-800 mt-1">
                Esta es tu sesión actual. No puedes cerrarla desde aquí. Para cerrar esta sesión, cierra sesión normalmente.
              </p>
            </div>
          </div>
        </div>

        <!-- Sessions List -->
        <div class="space-y-4">
          <div
            v-for="session in sessions"
            :key="session.id"
            class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            :class="{ 'ring-2 ring-blue-500 bg-blue-50': session.isCurrent }"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-start space-x-4">
                <!-- Device Icon -->
                <div class="flex-shrink-0">
                  <div class="h-12 w-12 rounded-lg flex items-center justify-center"
                       :class="getDeviceIconClass(session.device.type)">
                    <component :is="getDeviceIcon(session.device.type)" class="h-6 w-6" />
                  </div>
                </div>
                
                <!-- Session Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-2 mb-1">
                    <h3 class="text-sm font-medium text-gray-900 truncate">
                      {{ session.device.name || getDeviceTypeName(session.device.type) }}
                    </h3>
                    
                    <span v-if="session.isCurrent" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      Actual
                    </span>
                    
                    <span :class="getStatusClass(session.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                      {{ getStatusLabel(session.status) }}
                    </span>
                  </div>
                  
                  <div class="space-y-1">
                    <div class="flex items-center text-sm text-gray-600">
                      <GlobeAltIcon class="h-4 w-4 mr-2" />
                      <span>{{ session.browser.name }} {{ session.browser.version }}</span>
                    </div>
                    
                    <div class="flex items-center text-sm text-gray-600">
                      <MapPinIcon class="h-4 w-4 mr-2" />
                      <span>{{ session.location.city }}, {{ session.location.country }}</span>
                      <span class="mx-2">•</span>
                      <span class="font-mono text-xs">{{ session.ipAddress }}</span>
                    </div>
                    
                    <div class="flex items-center text-sm text-gray-600">
                      <ClockIcon class="h-4 w-4 mr-2" />
                      <span>Iniciada: {{ formatDateTime(session.createdAt) }}</span>
                    </div>
                    
                    <div class="flex items-center text-sm text-gray-600">
                      <ArrowPathIcon class="h-4 w-4 mr-2" />
                      <span>Última actividad: {{ formatRelativeTime(session.lastActivity) }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex items-center space-x-2">
                <button
                  @click="viewSessionDetails(session)"
                  class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
                  title="Ver detalles"
                >
                  <EyeIcon class="h-4 w-4" />
                </button>
                
                <button
                  v-if="!session.isCurrent"
                  @click="terminateSession(session)"
                  :disabled="terminating.includes(session.id)"
                  class="text-red-400 hover:text-red-600 p-2 rounded-lg hover:bg-red-50 disabled:opacity-50"
                  title="Cerrar sesión"
                >
                  <XMarkIcon v-if="!terminating.includes(session.id)" class="h-4 w-4" />
                  <ArrowPathIcon v-else class="h-4 w-4 animate-spin" />
                </button>
              </div>
            </div>
            
            <!-- Security Alert -->
            <div v-if="session.securityAlert" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div class="flex items-start">
                <ExclamationTriangleIcon class="h-4 w-4 text-red-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-red-900">Alerta de Seguridad</p>
                  <p class="text-sm text-red-800 mt-1">{{ session.securityAlert }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-if="sessions.length === 0" class="text-center py-12">
          <ComputerDesktopIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-500">No se encontraron sesiones activas</p>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
        <div class="text-sm text-gray-600">
          <p>Las sesiones inactivas se cierran automáticamente después de 30 días.</p>
        </div>
        
        <div class="flex items-center space-x-3">
          <button
            @click="terminateAllOtherSessions"
            :disabled="terminatingAll || sessions.filter(s => !s.isCurrent).length === 0"
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <ArrowPathIcon v-if="terminatingAll" class="h-4 w-4 animate-spin" />
            <XMarkIcon v-else class="h-4 w-4" />
            <span>{{ terminatingAll ? 'Cerrando...' : 'Cerrar Todas las Otras' }}</span>
          </button>
          
          <button
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>

    <!-- Session Details Modal -->
    <SessionDetailsModal
      v-if="showDetailsModal"
      :session="selectedSession"
      @close="showDetailsModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  ArrowPathIcon,
  ComputerDesktopIcon,
  CheckCircleIcon,
  ClockIcon,
  InformationCircleIcon,
  GlobeAltIcon,
  MapPinIcon,
  EyeIcon,
  ExclamationTriangleIcon,
  DevicePhoneMobileIcon,
  DeviceTabletIcon
} from '@heroicons/vue/24/outline'
import SessionDetailsModal from './SessionDetailsModal.vue'

// Emits
const emit = defineEmits(['close'])

// Reactive state
const loading = ref(false)
const terminating = ref([])
const terminatingAll = ref(false)
const showDetailsModal = ref(false)
const selectedSession = ref(null)

const stats = ref({
  totalSessions: 5,
  activeSessions: 4,
  lastActivity: '2m ago'
})

const sessions = ref([
  {
    id: '1',
    isCurrent: true,
    status: 'active',
    device: {
      type: 'desktop',
      name: 'Windows PC',
      os: 'Windows 11'
    },
    browser: {
      name: 'Chrome',
      version: '120.0.0.0'
    },
    location: {
      city: 'Madrid',
      country: 'España',
      coordinates: { lat: 40.4168, lng: -3.7038 }
    },
    ipAddress: '192.168.1.100',
    createdAt: '2024-01-15T09:30:00Z',
    lastActivity: '2024-01-15T15:28:00Z',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  },
  {
    id: '2',
    isCurrent: false,
    status: 'active',
    device: {
      type: 'mobile',
      name: 'iPhone 15 Pro',
      os: 'iOS 17.2'
    },
    browser: {
      name: 'Safari',
      version: '17.2'
    },
    location: {
      city: 'Barcelona',
      country: 'España',
      coordinates: { lat: 41.3851, lng: 2.1734 }
    },
    ipAddress: '10.0.0.45',
    createdAt: '2024-01-15T08:15:00Z',
    lastActivity: '2024-01-15T14:45:00Z',
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
  },
  {
    id: '3',
    isCurrent: false,
    status: 'idle',
    device: {
      type: 'tablet',
      name: 'iPad Air',
      os: 'iPadOS 17.2'
    },
    browser: {
      name: 'Safari',
      version: '17.2'
    },
    location: {
      city: 'Valencia',
      country: 'España',
      coordinates: { lat: 39.4699, lng: -0.3763 }
    },
    ipAddress: '192.168.0.25',
    createdAt: '2024-01-14T16:20:00Z',
    lastActivity: '2024-01-15T11:30:00Z',
    userAgent: 'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
  },
  {
    id: '4',
    isCurrent: false,
    status: 'suspicious',
    device: {
      type: 'desktop',
      name: 'Unknown Device',
      os: 'Linux'
    },
    browser: {
      name: 'Firefox',
      version: '121.0'
    },
    location: {
      city: 'Unknown',
      country: 'Rusia',
      coordinates: { lat: 55.7558, lng: 37.6176 }
    },
    ipAddress: '185.220.101.42',
    createdAt: '2024-01-15T13:45:00Z',
    lastActivity: '2024-01-15T14:15:00Z',
    securityAlert: 'Ubicación inusual detectada. Esta sesión se inició desde una ubicación que no reconocemos.',
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'
  }
])

// Computed
const activeSessions = computed(() => {
  return sessions.value.filter(session => session.status === 'active')
})

// Methods
const getDeviceIcon = (type) => {
  const icons = {
    desktop: ComputerDesktopIcon,
    mobile: DevicePhoneMobileIcon,
    tablet: DeviceTabletIcon
  }
  return icons[type] || ComputerDesktopIcon
}

const getDeviceIconClass = (type) => {
  const classes = {
    desktop: 'bg-blue-100 text-blue-600',
    mobile: 'bg-green-100 text-green-600',
    tablet: 'bg-purple-100 text-purple-600'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

const getDeviceTypeName = (type) => {
  const names = {
    desktop: 'Computadora',
    mobile: 'Móvil',
    tablet: 'Tablet'
  }
  return names[type] || 'Dispositivo'
}

const getStatusClass = (status) => {
  const classes = {
    active: 'bg-green-100 text-green-800',
    idle: 'bg-yellow-100 text-yellow-800',
    suspicious: 'bg-red-100 text-red-800',
    expired: 'bg-gray-100 text-gray-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activa',
    idle: 'Inactiva',
    suspicious: 'Sospechosa',
    expired: 'Expirada'
  }
  return labels[status] || status
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRelativeTime = (dateString) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  
  if (diffMins < 1) return 'Ahora'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  return `${diffDays}d ago`
}

const refreshSessions = async () => {
  loading.value = true
  
  try {
    // TODO: Fetch sessions from API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('Sessions refreshed')
  } catch (error) {
    console.error('Error refreshing sessions:', error)
    alert('Error al actualizar las sesiones')
  } finally {
    loading.value = false
  }
}

const viewSessionDetails = (session) => {
  selectedSession.value = session
  showDetailsModal.value = true
}

const terminateSession = async (session) => {
  if (session.isCurrent) {
    alert('No puedes cerrar tu sesión actual desde aquí')
    return
  }
  
  if (!confirm(`¿Estás seguro de que quieres cerrar la sesión en ${session.device.name || getDeviceTypeName(session.device.type)}?`)) {
    return
  }
  
  terminating.value.push(session.id)
  
  try {
    // TODO: Terminate session via API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Remove session from list
    const index = sessions.value.findIndex(s => s.id === session.id)
    if (index > -1) {
      sessions.value.splice(index, 1)
    }
    
    // Update stats
    stats.value.totalSessions--
    if (session.status === 'active') {
      stats.value.activeSessions--
    }
    
    alert('Sesión cerrada exitosamente')
  } catch (error) {
    console.error('Error terminating session:', error)
    alert('Error al cerrar la sesión')
  } finally {
    terminating.value = terminating.value.filter(id => id !== session.id)
  }
}

const terminateAllOtherSessions = async () => {
  const otherSessions = sessions.value.filter(s => !s.isCurrent)
  
  if (otherSessions.length === 0) {
    return
  }
  
  if (!confirm(`¿Estás seguro de que quieres cerrar todas las otras ${otherSessions.length} sesiones?`)) {
    return
  }
  
  terminatingAll.value = true
  
  try {
    // TODO: Terminate all other sessions via API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Remove all other sessions
    sessions.value = sessions.value.filter(s => s.isCurrent)
    
    // Update stats
    stats.value.totalSessions = 1
    stats.value.activeSessions = 1
    
    alert('Todas las otras sesiones han sido cerradas exitosamente')
  } catch (error) {
    console.error('Error terminating all sessions:', error)
    alert('Error al cerrar las sesiones')
  } finally {
    terminatingAll.value = false
  }
}

// Initialize
onMounted(() => {
  console.log('ActiveSessionsModal mounted')
  refreshSessions()
})
</script>