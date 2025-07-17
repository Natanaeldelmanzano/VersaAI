<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full mx-4 max-h-[90vh] overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Detalles de la Sesión</h2>
          <p class="text-sm text-gray-600 mt-1">{{ session.device.name || getDeviceTypeName(session.device.type) }}</p>
        </div>
        
        <div class="flex items-center space-x-3">
          <span :class="getStatusClass(session.status)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
            {{ getStatusLabel(session.status) }}
          </span>
          
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
        <!-- Current Session Alert -->
        <div v-if="session.isCurrent" class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div class="flex items-start">
            <InformationCircleIcon class="h-5 w-5 text-blue-600 mt-0.5 mr-3" />
            <div>
              <h3 class="text-sm font-medium text-blue-900">Sesión Actual</h3>
              <p class="text-sm text-blue-800 mt-1">
                Esta es tu sesión actual desde la cual estás viendo estos detalles.
              </p>
            </div>
          </div>
        </div>

        <!-- Security Alert -->
        <div v-if="session.securityAlert" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div class="flex items-start">
            <ExclamationTriangleIcon class="h-5 w-5 text-red-600 mt-0.5 mr-3" />
            <div>
              <h3 class="text-sm font-medium text-red-900">Alerta de Seguridad</h3>
              <p class="text-sm text-red-800 mt-1">{{ session.securityAlert }}</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Device Information -->
          <div class="space-y-6">
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <component :is="getDeviceIcon(session.device.type)" class="h-5 w-5 mr-2" />
                Información del Dispositivo
              </h3>
              
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Tipo:</span>
                  <span class="text-sm text-gray-900">{{ getDeviceTypeName(session.device.type) }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Nombre:</span>
                  <span class="text-sm text-gray-900">{{ session.device.name || 'Desconocido' }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Sistema Operativo:</span>
                  <span class="text-sm text-gray-900">{{ session.device.os }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Navegador:</span>
                  <span class="text-sm text-gray-900">{{ session.browser.name }} {{ session.browser.version }}</span>
                </div>
              </div>
            </div>

            <!-- Location Information -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <MapPinIcon class="h-5 w-5 mr-2" />
                Ubicación
              </h3>
              
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Ciudad:</span>
                  <span class="text-sm text-gray-900">{{ session.location.city }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">País:</span>
                  <span class="text-sm text-gray-900">{{ session.location.country }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Coordenadas:</span>
                  <span class="text-sm text-gray-900 font-mono">
                    {{ session.location.coordinates.lat.toFixed(4) }}, {{ session.location.coordinates.lng.toFixed(4) }}
                  </span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Dirección IP:</span>
                  <span class="text-sm text-gray-900 font-mono">{{ session.ipAddress }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Session Information -->
          <div class="space-y-6">
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <ClockIcon class="h-5 w-5 mr-2" />
                Información de la Sesión
              </h3>
              
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">ID de Sesión:</span>
                  <span class="text-sm text-gray-900 font-mono">{{ session.id }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Estado:</span>
                  <span :class="getStatusClass(session.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ getStatusLabel(session.status) }}
                  </span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Iniciada:</span>
                  <span class="text-sm text-gray-900">{{ formatDateTime(session.createdAt) }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Última Actividad:</span>
                  <span class="text-sm text-gray-900">{{ formatDateTime(session.lastActivity) }}</span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Duración:</span>
                  <span class="text-sm text-gray-900">{{ getSessionDuration() }}</span>
                </div>
              </div>
            </div>

            <!-- Security Information -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <ShieldCheckIcon class="h-5 w-5 mr-2" />
                Información de Seguridad
              </h3>
              
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Autenticación:</span>
                  <span class="text-sm text-gray-900 flex items-center">
                    <CheckCircleIcon class="h-4 w-4 text-green-500 mr-1" />
                    Verificada
                  </span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">2FA:</span>
                  <span class="text-sm text-gray-900 flex items-center">
                    <CheckCircleIcon class="h-4 w-4 text-green-500 mr-1" />
                    Activado
                  </span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Conexión:</span>
                  <span class="text-sm text-gray-900 flex items-center">
                    <LockClosedIcon class="h-4 w-4 text-green-500 mr-1" />
                    HTTPS Segura
                  </span>
                </div>
                
                <div class="flex justify-between">
                  <span class="text-sm font-medium text-gray-600">Riesgo:</span>
                  <span :class="getRiskClass()" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ getRiskLevel() }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- User Agent -->
        <div class="mt-6 bg-gray-50 rounded-lg p-4">
          <h3 class="text-lg font-medium text-gray-900 mb-3 flex items-center">
            <GlobeAltIcon class="h-5 w-5 mr-2" />
            User Agent
          </h3>
          <p class="text-sm text-gray-700 font-mono break-all bg-white p-3 rounded border">
            {{ session.userAgent }}
          </p>
        </div>

        <!-- Activity Timeline -->
        <div class="mt-6 bg-gray-50 rounded-lg p-4">
          <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
            <ClockIcon class="h-5 w-5 mr-2" />
            Actividad Reciente
          </h3>
          
          <div class="space-y-3">
            <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
              <div class="flex-shrink-0">
                <div class="h-2 w-2 bg-blue-500 rounded-full mt-2"></div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm text-gray-900">{{ activity.action }}</p>
                <p class="text-xs text-gray-500">{{ formatDateTime(activity.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
        <div class="text-sm text-gray-600">
          <p>ID de Sesión: <span class="font-mono">{{ session.id }}</span></p>
        </div>
        
        <div class="flex items-center space-x-3">
          <button
            v-if="!session.isCurrent"
            @click="terminateSession"
            :disabled="terminating"
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <ArrowPathIcon v-if="terminating" class="h-4 w-4 animate-spin" />
            <XMarkIcon v-else class="h-4 w-4" />
            <span>{{ terminating ? 'Cerrando...' : 'Cerrar Sesión' }}</span>
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  XMarkIcon,
  ArrowPathIcon,
  ComputerDesktopIcon,
  DevicePhoneMobileIcon,
  DeviceTabletIcon,
  MapPinIcon,
  ClockIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
  LockClosedIcon,
  GlobeAltIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  session: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'sessionTerminated'])

// Reactive state
const terminating = ref(false)

const recentActivity = ref([
  {
    id: 1,
    action: 'Inicio de sesión exitoso',
    timestamp: props.session.createdAt
  },
  {
    id: 2,
    action: 'Acceso al dashboard',
    timestamp: '2024-01-15T09:35:00Z'
  },
  {
    id: 3,
    action: 'Visualización de documentos',
    timestamp: '2024-01-15T10:15:00Z'
  },
  {
    id: 4,
    action: 'Configuración de perfil actualizada',
    timestamp: '2024-01-15T11:30:00Z'
  },
  {
    id: 5,
    action: 'Última actividad registrada',
    timestamp: props.session.lastActivity
  }
])

// Methods
const getDeviceIcon = (type) => {
  const icons = {
    desktop: ComputerDesktopIcon,
    mobile: DevicePhoneMobileIcon,
    tablet: DeviceTabletIcon
  }
  return icons[type] || ComputerDesktopIcon
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

const getRiskClass = () => {
  if (props.session.securityAlert) {
    return 'bg-red-100 text-red-800'
  }
  if (props.session.status === 'suspicious') {
    return 'bg-yellow-100 text-yellow-800'
  }
  return 'bg-green-100 text-green-800'
}

const getRiskLevel = () => {
  if (props.session.securityAlert) {
    return 'Alto'
  }
  if (props.session.status === 'suspicious') {
    return 'Medio'
  }
  return 'Bajo'
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getSessionDuration = () => {
  const start = new Date(props.session.createdAt)
  const end = new Date(props.session.lastActivity)
  const diffMs = end - start
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
  
  if (diffHours > 0) {
    return `${diffHours}h ${diffMins}m`
  }
  return `${diffMins}m`
}

const terminateSession = async () => {
  if (props.session.isCurrent) {
    alert('No puedes cerrar tu sesión actual desde aquí')
    return
  }
  
  if (!confirm(`¿Estás seguro de que quieres cerrar esta sesión?`)) {
    return
  }
  
  terminating.value = true
  
  try {
    // TODO: Terminate session via API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    emit('sessionTerminated', props.session)
    emit('close')
    
    alert('Sesión cerrada exitosamente')
  } catch (error) {
    console.error('Error terminating session:', error)
    alert('Error al cerrar la sesión')
  } finally {
    terminating.value = false
  }
}
</script>