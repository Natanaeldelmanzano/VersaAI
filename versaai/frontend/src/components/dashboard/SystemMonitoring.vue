<template>
  <div class="system-monitoring">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Monitoreo del Sistema</h2>
        <p class="text-gray-600 mt-2">Supervisión en tiempo real del rendimiento y estado del sistema</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-2">
          <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-sm text-gray-600">Sistema Operativo</span>
        </div>
        
        <select 
          v-model="refreshInterval"
          @change="updateRefreshInterval"
          class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          <option value="5">5 segundos</option>
          <option value="10">10 segundos</option>
          <option value="30">30 segundos</option>
          <option value="60">1 minuto</option>
        </select>
        
        <button
          @click="refreshMetrics"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
        >
          <ArrowPathIcon :class="['w-4 h-4 mr-2', { 'animate-spin': isLoading }]" />
          Actualizar
        </button>
      </div>
    </div>

    <!-- System Health Overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">CPU Usage</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ systemMetrics.cpu }}%</p>
            <div class="w-full bg-gray-200 rounded-full h-2 mt-3">
              <div 
                class="h-2 rounded-full transition-all duration-500"
                :class="getCpuColorClass(systemMetrics.cpu)"
                :style="{ width: systemMetrics.cpu + '%' }"
              ></div>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <CpuChipIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Memory Usage</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ systemMetrics.memory }}%</p>
            <div class="w-full bg-gray-200 rounded-full h-2 mt-3">
              <div 
                class="h-2 rounded-full transition-all duration-500"
                :class="getMemoryColorClass(systemMetrics.memory)"
                :style="{ width: systemMetrics.memory + '%' }"
              ></div>
            </div>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <CircuitBoardIcon class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Disk Usage</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ systemMetrics.disk }}%</p>
            <div class="w-full bg-gray-200 rounded-full h-2 mt-3">
              <div 
                class="h-2 rounded-full transition-all duration-500"
                :class="getDiskColorClass(systemMetrics.disk)"
                :style="{ width: systemMetrics.disk + '%' }"
              ></div>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <ServerIcon class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Active Connections</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ systemMetrics.activeConnections }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+5.2%</span>
              <span class="text-sm text-gray-500 ml-2">vs última hora</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <SignalIcon class="w-6 h-6 text-orange-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Real-time Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- CPU & Memory Chart -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">CPU & Memory Usage</h3>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span class="text-sm text-gray-600">CPU</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-green-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Memory</span>
            </div>
          </div>
        </div>
        <div class="h-64">
          <SystemChart 
            :data="cpuMemoryChartData" 
            :loading="isLoading"
            type="line"
            :options="cpuMemoryChartOptions"
          />
        </div>
      </div>

      <!-- Network Traffic Chart -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-gray-900">Network Traffic</h3>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Inbound</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 bg-orange-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Outbound</span>
            </div>
          </div>
        </div>
        <div class="h-64">
          <SystemChart 
            :data="networkChartData" 
            :loading="isLoading"
            type="line"
            :options="networkChartOptions"
          />
        </div>
      </div>
    </div>

    <!-- Services Status -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Estado de Servicios</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="service in services" 
            :key="service.name"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <component :is="service.icon" class="w-6 h-6 text-gray-600" />
                <h4 class="font-medium text-gray-900">{{ service.name }}</h4>
              </div>
              <span :class="[
                'w-3 h-3 rounded-full',
                service.status === 'running' ? 'bg-green-500' :
                service.status === 'stopped' ? 'bg-red-500' :
                service.status === 'warning' ? 'bg-yellow-500' : 'bg-gray-500'
              ]"></span>
            </div>
            
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Estado:</span>
                <span :class="[
                  'font-medium',
                  service.status === 'running' ? 'text-green-600' :
                  service.status === 'stopped' ? 'text-red-600' :
                  service.status === 'warning' ? 'text-yellow-600' : 'text-gray-600'
                ]">{{ getStatusLabel(service.status) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Uptime:</span>
                <span class="font-medium">{{ service.uptime }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">CPU:</span>
                <span class="font-medium">{{ service.cpu }}%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Memory:</span>
                <span class="font-medium">{{ service.memory }}MB</span>
              </div>
            </div>
            
            <div class="mt-4 flex space-x-2">
              <button
                v-if="service.status === 'stopped'"
                @click="startService(service)"
                class="flex-1 px-3 py-1 bg-green-600 text-white rounded text-xs font-medium hover:bg-green-700"
              >
                Iniciar
              </button>
              <button
                v-if="service.status === 'running'"
                @click="stopService(service)"
                class="flex-1 px-3 py-1 bg-red-600 text-white rounded text-xs font-medium hover:bg-red-700"
              >
                Detener
              </button>
              <button
                @click="restartService(service)"
                class="flex-1 px-3 py-1 bg-blue-600 text-white rounded text-xs font-medium hover:bg-blue-700"
              >
                Reiniciar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Logs -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Logs del Sistema</h3>
          <div class="flex items-center space-x-4">
            <select 
              v-model="logLevel"
              class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option value="all">Todos los niveles</option>
              <option value="error">Error</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
              <option value="debug">Debug</option>
            </select>
            
            <button
              @click="clearLogs"
              class="px-3 py-1 text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Limpiar
            </button>
          </div>
        </div>
      </div>
      <div class="p-6">
        <div class="bg-gray-900 rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
          <div 
            v-for="log in filteredLogs" 
            :key="log.id"
            class="flex items-start space-x-3 mb-2"
          >
            <span class="text-gray-400 text-xs whitespace-nowrap">{{ formatLogTime(log.timestamp) }}</span>
            <span :class="[
              'px-2 py-1 rounded text-xs font-medium whitespace-nowrap',
              log.level === 'error' ? 'bg-red-900 text-red-200' :
              log.level === 'warning' ? 'bg-yellow-900 text-yellow-200' :
              log.level === 'info' ? 'bg-blue-900 text-blue-200' :
              log.level === 'debug' ? 'bg-gray-700 text-gray-300' : 'bg-gray-700 text-gray-300'
            ]">{{ log.level.toUpperCase() }}</span>
            <span class="text-gray-300 flex-1">{{ log.message }}</span>
          </div>
          
          <div v-if="filteredLogs.length === 0" class="text-gray-500 text-center py-8">
            No hay logs disponibles
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Alerts -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Alertas de Rendimiento</h3>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div 
            v-for="alert in performanceAlerts" 
            :key="alert.id"
            class="flex items-start space-x-4 p-4 rounded-lg"
            :class="[
              alert.severity === 'critical' ? 'bg-red-50 border border-red-200' :
              alert.severity === 'warning' ? 'bg-yellow-50 border border-yellow-200' :
              alert.severity === 'info' ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50 border border-gray-200'
            ]"
          >
            <div :class="[
              'w-8 h-8 rounded-full flex items-center justify-center',
              alert.severity === 'critical' ? 'bg-red-100' :
              alert.severity === 'warning' ? 'bg-yellow-100' :
              alert.severity === 'info' ? 'bg-blue-100' : 'bg-gray-100'
            ]">
              <component :is="alert.icon" :class="[
                'w-4 h-4',
                alert.severity === 'critical' ? 'text-red-600' :
                alert.severity === 'warning' ? 'text-yellow-600' :
                alert.severity === 'info' ? 'text-blue-600' : 'text-gray-600'
              ]" />
            </div>
            <div class="flex-1">
              <h4 class="text-sm font-semibold text-gray-900">{{ alert.title }}</h4>
              <p class="text-sm text-gray-600 mt-1">{{ alert.description }}</p>
              <div class="flex items-center mt-2">
                <span :class="[
                  'text-xs font-medium px-2 py-1 rounded-full',
                  alert.severity === 'critical' ? 'bg-red-100 text-red-800' :
                  alert.severity === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                  alert.severity === 'info' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                ]">
                  {{ alert.severity.toUpperCase() }}
                </span>
                <span class="text-xs text-gray-500 ml-2">{{ alert.time }}</span>
              </div>
            </div>
            <button
              @click="dismissAlert(alert.id)"
              class="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
          
          <div v-if="performanceAlerts.length === 0" class="text-center py-8">
            <ShieldCheckIcon class="w-12 h-12 text-green-500 mx-auto mb-2" />
            <p class="text-gray-500">No hay alertas activas. El sistema funciona correctamente.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import {
  ArrowPathIcon,
  CpuChipIcon,
  CircuitBoardIcon,
  ServerIcon,
  SignalIcon,
  ArrowUpIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  XMarkIcon,
  CloudIcon,
  CommandLineIcon,
  CogIcon
} from '@heroicons/vue/24/outline'
import SystemChart from './charts/SystemChart.vue'

// Store
const dashboardStore = useDashboardStore()

// State
const isLoading = ref(false)
const refreshInterval = ref(10)
const logLevel = ref('all')
const refreshTimer = ref(null)

// Mock data
const systemMetrics = ref({
  cpu: 45,
  memory: 68,
  disk: 32,
  activeConnections: 1247
})

const services = ref([
  {
    name: 'API Server',
    status: 'running',
    uptime: '15d 4h 23m',
    cpu: 12.5,
    memory: 256,
    icon: ServerIcon
  },
  {
    name: 'Database',
    status: 'running',
    uptime: '15d 4h 23m',
    cpu: 8.2,
    memory: 512,
    icon: CircuitBoardIcon
  },
  {
    name: 'Redis Cache',
    status: 'running',
    uptime: '15d 4h 23m',
    cpu: 2.1,
    memory: 128,
    icon: CloudIcon
  },
  {
    name: 'Background Jobs',
    status: 'warning',
    uptime: '2h 15m',
    cpu: 5.8,
    memory: 64,
    icon: CogIcon
  },
  {
    name: 'Log Processor',
    status: 'running',
    uptime: '15d 4h 23m',
    cpu: 1.2,
    memory: 32,
    icon: CommandLineIcon
  },
  {
    name: 'Monitoring Agent',
    status: 'stopped',
    uptime: '0m',
    cpu: 0,
    memory: 0,
    icon: SignalIcon
  }
])

const systemLogs = ref([
  {
    id: 1,
    timestamp: new Date(),
    level: 'info',
    message: 'Sistema iniciado correctamente'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 60000),
    level: 'warning',
    message: 'Alto uso de CPU detectado en el servicio API Server'
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 120000),
    level: 'error',
    message: 'Fallo en la conexión con la base de datos secundaria'
  },
  {
    id: 4,
    timestamp: new Date(Date.now() - 180000),
    level: 'info',
    message: 'Backup automático completado exitosamente'
  },
  {
    id: 5,
    timestamp: new Date(Date.now() - 240000),
    level: 'debug',
    message: 'Cache invalidado para el usuario ID: 12345'
  }
])

const performanceAlerts = ref([
  {
    id: 1,
    title: 'Alto uso de CPU',
    description: 'El uso de CPU ha superado el 80% durante los últimos 5 minutos',
    severity: 'warning',
    time: 'Hace 2 minutos',
    icon: CpuChipIcon
  },
  {
    id: 2,
    title: 'Espacio en disco bajo',
    description: 'El disco principal tiene menos del 15% de espacio libre',
    severity: 'critical',
    time: 'Hace 10 minutos',
    icon: ServerIcon
  }
])

// Computed
const filteredLogs = computed(() => {
  if (logLevel.value === 'all') {
    return systemLogs.value
  }
  return systemLogs.value.filter(log => log.level === logLevel.value)
})

const cpuMemoryChartData = computed(() => ({
  labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30'],
  datasets: [
    {
      label: 'CPU Usage',
      data: [35, 42, 38, 45, 52, 48, 45],
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    },
    {
      label: 'Memory Usage',
      data: [60, 65, 63, 68, 72, 70, 68],
      borderColor: '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4
    }
  ]
}))

const networkChartData = computed(() => ({
  labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30'],
  datasets: [
    {
      label: 'Inbound (MB/s)',
      data: [12, 15, 18, 22, 19, 16, 14],
      borderColor: '#8B5CF6',
      backgroundColor: 'rgba(139, 92, 246, 0.1)',
      tension: 0.4
    },
    {
      label: 'Outbound (MB/s)',
      data: [8, 11, 14, 18, 15, 12, 10],
      borderColor: '#F59E0B',
      backgroundColor: 'rgba(245, 158, 11, 0.1)',
      tension: 0.4
    }
  ]
}))

const cpuMemoryChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: function(value) {
          return value + '%'
        }
      }
    }
  }
}

const networkChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: function(value) {
          return value + ' MB/s'
        }
      }
    }
  }
}

// Methods
const getCpuColorClass = (value) => {
  if (value >= 80) return 'bg-red-500'
  if (value >= 60) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getMemoryColorClass = (value) => {
  if (value >= 85) return 'bg-red-500'
  if (value >= 70) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getDiskColorClass = (value) => {
  if (value >= 90) return 'bg-red-500'
  if (value >= 75) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getStatusLabel = (status) => {
  const labels = {
    running: 'Ejecutándose',
    stopped: 'Detenido',
    warning: 'Advertencia',
    error: 'Error'
  }
  return labels[status] || status
}

const formatLogTime = (timestamp) => {
  return new Intl.DateTimeFormat('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(timestamp)
}

const refreshMetrics = async () => {
  isLoading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update metrics with random values
    systemMetrics.value = {
      cpu: Math.floor(Math.random() * 100),
      memory: Math.floor(Math.random() * 100),
      disk: Math.floor(Math.random() * 100),
      activeConnections: Math.floor(Math.random() * 2000) + 500
    }
  } catch (error) {
    console.error('Error refreshing metrics:', error)
  } finally {
    isLoading.value = false
  }
}

const updateRefreshInterval = () => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
  
  refreshTimer.value = setInterval(() => {
    refreshMetrics()
  }, refreshInterval.value * 1000)
}

const startService = (service) => {
  service.status = 'running'
  service.uptime = '0m'
  console.log(`Starting service: ${service.name}`)
}

const stopService = (service) => {
  service.status = 'stopped'
  service.uptime = '0m'
  service.cpu = 0
  service.memory = 0
  console.log(`Stopping service: ${service.name}`)
}

const restartService = (service) => {
  service.status = 'running'
  service.uptime = '0m'
  console.log(`Restarting service: ${service.name}`)
}

const clearLogs = () => {
  systemLogs.value = []
}

const dismissAlert = (alertId) => {
  const index = performanceAlerts.value.findIndex(alert => alert.id === alertId)
  if (index > -1) {
    performanceAlerts.value.splice(index, 1)
  }
}

// Lifecycle
onMounted(() => {
  refreshMetrics()
  updateRefreshInterval()
})

onUnmounted(() => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
})
</script>

<style scoped>
.system-monitoring {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom scrollbar for logs */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #374151;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #6B7280;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}
</style>