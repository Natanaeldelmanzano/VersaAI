<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Detalles del Log</h2>
          <p class="text-sm text-gray-600 mt-1">{{ formatDateTime(log.timestamp) }}</p>
        </div>
        
        <div class="flex items-center space-x-3">
          <button
            @click="copyToClipboard"
            class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
            title="Copiar al portapapeles"
          >
            <ClipboardDocumentIcon class="h-5 w-5" />
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
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Main Info -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Basic Info -->
            <div class="bg-gray-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Información Básica</h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">ID del Log</label>
                  <p class="text-sm text-gray-900 font-mono bg-white px-3 py-2 rounded border">{{ log.id }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Timestamp</label>
                  <p class="text-sm text-gray-900 font-mono bg-white px-3 py-2 rounded border">{{ log.timestamp }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nivel</label>
                  <span :class="getLevelClass(log.level)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                    {{ log.level }}
                  </span>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
                  <span :class="getCategoryClass(log.category)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                    {{ getCategoryLabel(log.category) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Message -->
            <div class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Mensaje</h3>
              <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ log.message }}</p>
              </div>
            </div>

            <!-- Details -->
            <div v-if="log.details" class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Detalles</h3>
              <div class="bg-gray-50 rounded-lg p-4">
                <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ log.details }}</p>
              </div>
            </div>

            <!-- Stack Trace -->
            <div v-if="log.stackTrace" class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Stack Trace</h3>
              <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre class="text-sm text-green-400 font-mono whitespace-pre-wrap">{{ log.stackTrace }}</pre>
              </div>
            </div>

            <!-- Metadata -->
            <div v-if="log.metadata" class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Metadatos</h3>
              <div class="bg-gray-50 rounded-lg p-4">
                <pre class="text-sm text-gray-900 font-mono whitespace-pre-wrap">{{ JSON.stringify(log.metadata, null, 2) }}</pre>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- User Info -->
            <div class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Usuario</h3>
              
              <div v-if="log.user" class="space-y-3">
                <div class="flex items-center space-x-3">
                  <div class="h-10 w-10 bg-blue-500 rounded-full flex items-center justify-center">
                    <span class="text-white font-medium text-sm">{{ getUserInitials(log.user.name) }}</span>
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ log.user.name }}</p>
                    <p class="text-sm text-gray-600">{{ log.user.email }}</p>
                  </div>
                </div>
                
                <div v-if="log.user.role" class="pt-2 border-t border-gray-200">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Rol</label>
                  <p class="text-sm text-gray-900">{{ log.user.role }}</p>
                </div>
                
                <div v-if="log.user.department" class="pt-2 border-t border-gray-200">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Departamento</label>
                  <p class="text-sm text-gray-900">{{ log.user.department }}</p>
                </div>
              </div>
              
              <div v-else class="text-center py-4">
                <ComputerDesktopIcon class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p class="text-sm text-gray-600">Acción del sistema</p>
              </div>
            </div>

            <!-- Context -->
            <div class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Contexto</h3>
              
              <div class="space-y-3">
                <div v-if="log.metadata?.requestId">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Request ID</label>
                  <p class="text-sm text-gray-900 font-mono bg-gray-50 px-2 py-1 rounded">{{ log.metadata.requestId }}</p>
                </div>
                
                <div v-if="log.metadata?.endpoint">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Endpoint</label>
                  <p class="text-sm text-gray-900 font-mono bg-gray-50 px-2 py-1 rounded">{{ log.metadata.endpoint }}</p>
                </div>
                
                <div v-if="log.metadata?.statusCode">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Status Code</label>
                  <span :class="getStatusCodeClass(log.metadata.statusCode)" class="inline-flex px-2 py-1 text-xs font-semibold rounded">
                    {{ log.metadata.statusCode }}
                  </span>
                </div>
                
                <div v-if="log.metadata?.duration">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Duración</label>
                  <p class="text-sm text-gray-900">{{ formatDuration(log.metadata.duration) }}</p>
                </div>
                
                <div v-if="log.metadata?.ipAddress">
                  <label class="block text-xs font-medium text-gray-700 mb-1">IP Address</label>
                  <p class="text-sm text-gray-900 font-mono bg-gray-50 px-2 py-1 rounded">{{ log.metadata.ipAddress }}</p>
                </div>
                
                <div v-if="log.metadata?.userAgent">
                  <label class="block text-xs font-medium text-gray-700 mb-1">User Agent</label>
                  <p class="text-xs text-gray-900 bg-gray-50 px-2 py-1 rounded break-all">{{ log.metadata.userAgent }}</p>
                </div>
              </div>
            </div>

            <!-- Performance -->
            <div v-if="hasPerformanceData" class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Rendimiento</h3>
              
              <div class="space-y-3">
                <div v-if="log.metadata?.memoryUsage">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Uso de Memoria</label>
                  <div class="flex items-center space-x-2">
                    <div class="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        class="h-2 rounded-full transition-all duration-300"
                        :class="log.metadata.memoryUsage > 80 ? 'bg-red-500' : log.metadata.memoryUsage > 60 ? 'bg-yellow-500' : 'bg-green-500'"
                        :style="{ width: log.metadata.memoryUsage + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm text-gray-900">{{ log.metadata.memoryUsage }}%</span>
                  </div>
                </div>
                
                <div v-if="log.metadata?.queryTime">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Tiempo de Query</label>
                  <p class="text-sm text-gray-900">{{ formatDuration(log.metadata.queryTime) }}</p>
                </div>
                
                <div v-if="log.metadata?.rowsAffected">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Filas Afectadas</label>
                  <p class="text-sm text-gray-900">{{ log.metadata.rowsAffected.toLocaleString() }}</p>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="bg-white border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-3">Acciones</h3>
              
              <div class="space-y-2">
                <button
                  @click="copyLogId"
                  class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
                >
                  <ClipboardDocumentIcon class="h-4 w-4" />
                  <span>Copiar ID del Log</span>
                </button>
                
                <button
                  @click="copyTimestamp"
                  class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
                >
                  <ClockIcon class="h-4 w-4" />
                  <span>Copiar Timestamp</span>
                </button>
                
                <button
                  v-if="log.metadata?.requestId"
                  @click="searchRelatedLogs"
                  class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
                >
                  <MagnifyingGlassIcon class="h-4 w-4" />
                  <span>Buscar Logs Relacionados</span>
                </button>
                
                <button
                  @click="exportLog"
                  class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
                >
                  <ArrowDownTrayIcon class="h-4 w-4" />
                  <span>Exportar Log</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  XMarkIcon,
  ClipboardDocumentIcon,
  ComputerDesktopIcon,
  ClockIcon,
  MagnifyingGlassIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  log: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'searchRelated'])

// Computed
const hasPerformanceData = computed(() => {
  return props.log.metadata && (
    props.log.metadata.memoryUsage ||
    props.log.metadata.queryTime ||
    props.log.metadata.rowsAffected
  )
})

// Methods
const getLevelClass = (level) => {
  const classes = {
    DEBUG: 'bg-gray-100 text-gray-800',
    INFO: 'bg-blue-100 text-blue-800',
    WARNING: 'bg-yellow-100 text-yellow-800',
    ERROR: 'bg-red-100 text-red-800',
    CRITICAL: 'bg-red-200 text-red-900'
  }
  return classes[level] || 'bg-gray-100 text-gray-800'
}

const getCategoryClass = (category) => {
  const classes = {
    api: 'bg-blue-100 text-blue-800',
    database: 'bg-green-100 text-green-800',
    auth: 'bg-purple-100 text-purple-800',
    chatbot: 'bg-indigo-100 text-indigo-800',
    system: 'bg-gray-100 text-gray-800',
    security: 'bg-red-100 text-red-800'
  }
  return classes[category] || 'bg-gray-100 text-gray-800'
}

const getCategoryLabel = (category) => {
  const labels = {
    api: 'API',
    database: 'Base de Datos',
    auth: 'Autenticación',
    chatbot: 'Chatbot',
    system: 'Sistema',
    security: 'Seguridad'
  }
  return labels[category] || category
}

const getStatusCodeClass = (statusCode) => {
  if (statusCode >= 200 && statusCode < 300) {
    return 'bg-green-100 text-green-800'
  } else if (statusCode >= 300 && statusCode < 400) {
    return 'bg-blue-100 text-blue-800'
  } else if (statusCode >= 400 && statusCode < 500) {
    return 'bg-yellow-100 text-yellow-800'
  } else if (statusCode >= 500) {
    return 'bg-red-100 text-red-800'
  }
  return 'bg-gray-100 text-gray-800'
}

const getUserInitials = (name) => {
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const formatDuration = (ms) => {
  if (ms < 1000) {
    return `${ms}ms`
  } else if (ms < 60000) {
    return `${(ms / 1000).toFixed(2)}s`
  } else {
    const minutes = Math.floor(ms / 60000)
    const seconds = ((ms % 60000) / 1000).toFixed(0)
    return `${minutes}m ${seconds}s`
  }
}

const copyToClipboard = async () => {
  try {
    const logData = JSON.stringify(props.log, null, 2)
    await navigator.clipboard.writeText(logData)
    alert('Log copiado al portapapeles')
  } catch (error) {
    console.error('Error copying to clipboard:', error)
    alert('Error al copiar al portapapeles')
  }
}

const copyLogId = async () => {
  try {
    await navigator.clipboard.writeText(props.log.id.toString())
    alert('ID del log copiado al portapapeles')
  } catch (error) {
    console.error('Error copying log ID:', error)
    alert('Error al copiar el ID del log')
  }
}

const copyTimestamp = async () => {
  try {
    await navigator.clipboard.writeText(props.log.timestamp)
    alert('Timestamp copiado al portapapeles')
  } catch (error) {
    console.error('Error copying timestamp:', error)
    alert('Error al copiar el timestamp')
  }
}

const searchRelatedLogs = () => {
  if (props.log.metadata?.requestId) {
    emit('searchRelated', props.log.metadata.requestId)
    emit('close')
  }
}

const exportLog = () => {
  const dataStr = JSON.stringify(props.log, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `log-${props.log.id}-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
}
</script>