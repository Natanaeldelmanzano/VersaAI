<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Logs del Sistema</h1>
        <p class="text-gray-600 mt-1">Monitorea y analiza la actividad del sistema</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button
          @click="exportLogs"
          class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2"
        >
          <ArrowDownTrayIcon class="h-4 w-4" />
          <span>Exportar</span>
        </button>
        <button
          @click="clearLogs"
          class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 flex items-center space-x-2"
        >
          <TrashIcon class="h-4 w-4" />
          <span>Limpiar</span>
        </button>
        <button
          @click="refreshLogs"
          :disabled="loading"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2 disabled:opacity-50"
        >
          <ArrowPathIcon :class="{ 'animate-spin': loading }" class="h-4 w-4" />
          <span>{{ loading ? 'Cargando...' : 'Actualizar' }}</span>
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 rounded-lg p-4">
        <div class="flex items-center">
          <DocumentTextIcon class="h-8 w-8 text-blue-600 mr-3" />
          <div>
            <p class="text-2xl font-bold text-blue-600">{{ stats.totalLogs }}</p>
            <p class="text-sm text-blue-600">Total Logs</p>
          </div>
        </div>
      </div>
      
      <div class="bg-red-50 rounded-lg p-4">
        <div class="flex items-center">
          <ExclamationCircleIcon class="h-8 w-8 text-red-600 mr-3" />
          <div>
            <p class="text-2xl font-bold text-red-600">{{ stats.errorLogs }}</p>
            <p class="text-sm text-red-600">Errores</p>
          </div>
        </div>
      </div>
      
      <div class="bg-yellow-50 rounded-lg p-4">
        <div class="flex items-center">
          <ExclamationTriangleIcon class="h-8 w-8 text-yellow-600 mr-3" />
          <div>
            <p class="text-2xl font-bold text-yellow-600">{{ stats.warningLogs }}</p>
            <p class="text-sm text-yellow-600">Advertencias</p>
          </div>
        </div>
      </div>
      
      <div class="bg-green-50 rounded-lg p-4">
        <div class="flex items-center">
          <ClockIcon class="h-8 w-8 text-green-600 mr-3" />
          <div>
            <p class="text-2xl font-bold text-green-600">{{ stats.lastUpdate }}</p>
            <p class="text-sm text-green-600">Última actualización</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Buscar en logs..."
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Nivel</label>
          <select
            v-model="filters.level"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Todos los niveles</option>
            <option value="DEBUG">Debug</option>
            <option value="INFO">Info</option>
            <option value="WARNING">Warning</option>
            <option value="ERROR">Error</option>
            <option value="CRITICAL">Critical</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Categoría</label>
          <select
            v-model="filters.category"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Todas las categorías</option>
            <option value="api">API</option>
            <option value="database">Base de Datos</option>
            <option value="auth">Autenticación</option>
            <option value="chatbot">Chatbot</option>
            <option value="system">Sistema</option>
            <option value="security">Seguridad</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Fecha</label>
          <select
            v-model="filters.timeRange"
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Todo el tiempo</option>
            <option value="1h">Última hora</option>
            <option value="24h">Últimas 24 horas</option>
            <option value="7d">Últimos 7 días</option>
            <option value="30d">Últimos 30 días</option>
          </select>
        </div>
      </div>
      
      <div class="flex items-center justify-between mt-4 pt-4 border-t border-gray-200">
        <div class="flex items-center space-x-4">
          <label class="flex items-center space-x-2">
            <input
              v-model="autoRefresh"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Auto-actualizar</span>
          </label>
          
          <div v-if="autoRefresh" class="flex items-center space-x-2">
            <span class="text-sm text-gray-600">cada</span>
            <select
              v-model="refreshInterval"
              class="border border-gray-300 rounded-md px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="5">5s</option>
              <option value="10">10s</option>
              <option value="30">30s</option>
              <option value="60">1m</option>
            </select>
          </div>
        </div>
        
        <div class="text-sm text-gray-600">
          Mostrando {{ filteredLogs.length }} de {{ logs.length }} logs
        </div>
      </div>
    </div>

    <!-- Logs Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Timestamp
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nivel
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Categoría
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Mensaje
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usuario
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="log in paginatedLogs"
              :key="log.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div>
                  <div>{{ formatDate(log.timestamp) }}</div>
                  <div class="text-xs text-gray-500">{{ formatTime(log.timestamp) }}</div>
                </div>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getLevelClass(log.level)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                  {{ log.level }}
                </span>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getCategoryClass(log.category)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                  {{ getCategoryLabel(log.category) }}
                </span>
              </td>
              
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  <div class="truncate max-w-md" :title="log.message">{{ log.message }}</div>
                  <div v-if="log.details" class="text-xs text-gray-500 mt-1 truncate max-w-md" :title="log.details">
                    {{ log.details }}
                  </div>
                </div>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div v-if="log.user">
                  <div>{{ log.user.name }}</div>
                  <div class="text-xs text-gray-500">{{ log.user.email }}</div>
                </div>
                <span v-else class="text-gray-400">Sistema</span>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  @click="viewLogDetails(log)"
                  class="text-blue-600 hover:text-blue-900 p-1 rounded"
                  title="Ver detalles"
                >
                  <EyeIcon class="h-4 w-4" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="filteredLogs.length === 0" class="text-center py-12">
        <DocumentTextIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p class="text-gray-500">No se encontraron logs</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between mt-6">
      <div class="text-sm text-gray-700">
        Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredLogs.length) }} de {{ filteredLogs.length }} logs
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Anterior
        </button>
        
        <span class="px-3 py-1 text-sm text-gray-700">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Siguiente
        </button>
      </div>
    </div>

    <!-- Log Details Modal -->
    <LogDetailsModal
      v-if="showDetailsModal"
      :log="selectedLog"
      @close="showDetailsModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import {
  ArrowDownTrayIcon,
  TrashIcon,
  ArrowPathIcon,
  DocumentTextIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  EyeIcon
} from '@heroicons/vue/24/outline'
import LogDetailsModal from '@/components/dashboard/LogDetailsModal.vue'

// Reactive state
const loading = ref(false)
const autoRefresh = ref(false)
const refreshInterval = ref(30)
const currentPage = ref(1)
const itemsPerPage = ref(50)
const showDetailsModal = ref(false)
const selectedLog = ref(null)
const refreshTimer = ref(null)

const filters = ref({
  search: '',
  level: 'all',
  category: 'all',
  timeRange: 'all'
})

const stats = ref({
  totalLogs: 15420,
  errorLogs: 23,
  warningLogs: 156,
  lastUpdate: '2m ago'
})

const logs = ref([
  {
    id: 1,
    timestamp: '2024-01-15T15:30:25Z',
    level: 'ERROR',
    category: 'api',
    message: 'Failed to process chatbot request',
    details: 'Connection timeout to OpenAI API after 30 seconds',
    user: {
      name: 'Juan Pérez',
      email: 'juan@example.com'
    },
    metadata: {
      requestId: 'req_123456',
      endpoint: '/api/v1/chatbot/message',
      statusCode: 500,
      duration: 30000
    }
  },
  {
    id: 2,
    timestamp: '2024-01-15T15:29:45Z',
    level: 'WARNING',
    category: 'database',
    message: 'Slow query detected',
    details: 'Query took 2.5 seconds to execute: SELECT * FROM conversations WHERE...',
    user: null,
    metadata: {
      queryTime: 2500,
      table: 'conversations',
      rowsAffected: 15000
    }
  },
  {
    id: 3,
    timestamp: '2024-01-15T15:28:12Z',
    level: 'INFO',
    category: 'auth',
    message: 'User login successful',
    details: 'User authenticated via email/password',
    user: {
      name: 'María García',
      email: 'maria@example.com'
    },
    metadata: {
      loginMethod: 'email',
      ipAddress: '192.168.1.100',
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
  },
  {
    id: 4,
    timestamp: '2024-01-15T15:27:33Z',
    level: 'DEBUG',
    category: 'chatbot',
    message: 'Processing chatbot message',
    details: 'Analyzing user intent and generating response',
    user: {
      name: 'Carlos López',
      email: 'carlos@example.com'
    },
    metadata: {
      messageId: 'msg_789012',
      intent: 'product_inquiry',
      confidence: 0.95
    }
  },
  {
    id: 5,
    timestamp: '2024-01-15T15:26:18Z',
    level: 'CRITICAL',
    category: 'system',
    message: 'High memory usage detected',
    details: 'System memory usage exceeded 90% threshold',
    user: null,
    metadata: {
      memoryUsage: 92,
      availableMemory: '1.2 GB',
      totalMemory: '16 GB'
    }
  }
])

// Computed
const filteredLogs = computed(() => {
  let filtered = logs.value
  
  if (filters.value.search) {
    const query = filters.value.search.toLowerCase()
    filtered = filtered.filter(log => 
      log.message.toLowerCase().includes(query) ||
      (log.details && log.details.toLowerCase().includes(query)) ||
      (log.user && log.user.name.toLowerCase().includes(query))
    )
  }
  
  if (filters.value.level !== 'all') {
    filtered = filtered.filter(log => log.level === filters.value.level)
  }
  
  if (filters.value.category !== 'all') {
    filtered = filtered.filter(log => log.category === filters.value.category)
  }
  
  if (filters.value.timeRange !== 'all') {
    const now = new Date()
    const timeRanges = {
      '1h': 1 * 60 * 60 * 1000,
      '24h': 24 * 60 * 60 * 1000,
      '7d': 7 * 24 * 60 * 60 * 1000,
      '30d': 30 * 24 * 60 * 60 * 1000
    }
    
    const range = timeRanges[filters.value.timeRange]
    if (range) {
      const cutoff = new Date(now.getTime() - range)
      filtered = filtered.filter(log => new Date(log.timestamp) >= cutoff)
    }
  }
  
  return filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
})

const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredLogs.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredLogs.value.length / itemsPerPage.value)
})

// Watchers
watch([filters], () => {
  currentPage.value = 1
}, { deep: true })

watch(autoRefresh, (enabled) => {
  if (enabled) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
})

watch(refreshInterval, () => {
  if (autoRefresh.value) {
    stopAutoRefresh()
    startAutoRefresh()
  }
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

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const refreshLogs = async () => {
  loading.value = true
  
  try {
    // TODO: Fetch logs from API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update stats
    stats.value.lastUpdate = 'Ahora'
    
    console.log('Logs refreshed')
  } catch (error) {
    console.error('Error refreshing logs:', error)
    alert('Error al actualizar los logs')
  } finally {
    loading.value = false
  }
}

const exportLogs = () => {
  const dataStr = JSON.stringify(filteredLogs.value, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `versaai-logs-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const clearLogs = () => {
  if (confirm('¿Estás seguro de que quieres limpiar todos los logs? Esta acción no se puede deshacer.')) {
    // TODO: Clear logs via API
    logs.value = []
    stats.value.totalLogs = 0
    stats.value.errorLogs = 0
    stats.value.warningLogs = 0
    alert('Logs limpiados exitosamente')
  }
}

const viewLogDetails = (log) => {
  selectedLog.value = log
  showDetailsModal.value = true
}

const startAutoRefresh = () => {
  refreshTimer.value = setInterval(() => {
    refreshLogs()
  }, refreshInterval.value * 1000)
}

const stopAutoRefresh = () => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
    refreshTimer.value = null
  }
}

// Initialize
onMounted(() => {
  console.log('SystemLogs mounted')
  refreshLogs()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>