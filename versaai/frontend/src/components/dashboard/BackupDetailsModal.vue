<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900">Detalles del Backup</h3>
          <p class="text-sm text-gray-600 mt-1">{{ backup.name }}</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Status Banner -->
      <div :class="getStatusBannerClass(backup.status)" class="rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <component :is="getStatusIcon(backup.status)" class="h-6 w-6 mr-3" />
          <div class="flex-1">
            <h4 class="font-medium">{{ getStatusTitle(backup.status) }}</h4>
            <p class="text-sm mt-1">{{ getStatusDescription(backup.status) }}</p>
          </div>
        </div>
      </div>

      <!-- Basic Information -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h4 class="text-lg font-medium text-gray-900 mb-4">Información General</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Nombre</label>
              <p class="mt-1 text-sm text-gray-900">{{ backup.name }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Descripción</label>
              <p class="mt-1 text-sm text-gray-900">{{ backup.description }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo</label>
              <span :class="getTypeClass(backup.type)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full mt-1">
                {{ getTypeLabel(backup.type) }}
              </span>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Estado</label>
              <div class="flex items-center mt-1">
                <component :is="getStatusIcon(backup.status)" :class="getStatusIconClass(backup.status)" class="h-4 w-4 mr-2" />
                <span :class="getStatusClass(backup.status)" class="text-sm font-medium">
                  {{ getStatusLabel(backup.status) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Tamaño</label>
              <p class="mt-1 text-sm text-gray-900">{{ backup.size }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Duración</label>
              <p class="mt-1 text-sm text-gray-900">{{ backup.duration }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Fecha de inicio</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(backup.createdAt) }}</p>
            </div>
            
            <div v-if="backup.completedAt">
              <label class="block text-sm font-medium text-gray-700">Fecha de finalización</label>
              <p class="mt-1 text-sm text-gray-900">{{ formatDateTime(backup.completedAt) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Technical Details -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h4 class="text-lg font-medium text-gray-900 mb-4">Detalles Técnicos</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Método de compresión</label>
              <p class="mt-1 text-sm text-gray-900">{{ technicalDetails.compression }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Algoritmo de hash</label>
              <p class="mt-1 text-sm text-gray-900">{{ technicalDetails.hashAlgorithm }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Checksum</label>
              <p class="mt-1 text-sm text-gray-900 font-mono break-all">{{ technicalDetails.checksum }}</p>
            </div>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Versión de PostgreSQL</label>
              <p class="mt-1 text-sm text-gray-900">{{ technicalDetails.postgresVersion }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Formato</label>
              <p class="mt-1 text-sm text-gray-900">{{ technicalDetails.format }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700">Ubicación</label>
              <p class="mt-1 text-sm text-gray-900 font-mono break-all">{{ technicalDetails.location }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Database Statistics -->
      <div class="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h4 class="text-lg font-medium text-gray-900 mb-4">Estadísticas de la Base de Datos</h4>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{{ dbStats.tables }}</div>
            <div class="text-sm text-gray-600">Tablas</div>
          </div>
          
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">{{ dbStats.records }}</div>
            <div class="text-sm text-gray-600">Registros</div>
          </div>
          
          <div class="text-center">
            <div class="text-2xl font-bold text-yellow-600">{{ dbStats.indexes }}</div>
            <div class="text-sm text-gray-600">Índices</div>
          </div>
          
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ dbStats.size }}</div>
            <div class="text-sm text-gray-600">Tamaño DB</div>
          </div>
        </div>
      </div>

      <!-- Error Details (if failed) -->
      <div v-if="backup.status === 'failed' && backup.error" class="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
        <h4 class="text-lg font-medium text-red-900 mb-4">Detalles del Error</h4>
        
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-red-700">Mensaje de error</label>
            <p class="mt-1 text-sm text-red-900 bg-red-100 p-3 rounded font-mono">{{ backup.error }}</p>
          </div>
          
          <div v-if="errorDetails.stackTrace">
            <label class="block text-sm font-medium text-red-700">Stack trace</label>
            <pre class="mt-1 text-xs text-red-900 bg-red-100 p-3 rounded overflow-x-auto">{{ errorDetails.stackTrace }}</pre>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-red-700">Código de error</label>
              <p class="mt-1 text-sm text-red-900">{{ errorDetails.errorCode }}</p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-red-700">Momento del error</label>
              <p class="mt-1 text-sm text-red-900">{{ formatDateTime(errorDetails.errorTime) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress (if in progress) -->
      <div v-if="backup.status === 'in_progress'" class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h4 class="text-lg font-medium text-blue-900 mb-4">Progreso del Backup</h4>
        
        <div class="space-y-4">
          <div>
            <div class="flex justify-between text-sm text-blue-700 mb-1">
              <span>Progreso general</span>
              <span>{{ progress.percentage }}%</span>
            </div>
            <div class="w-full bg-blue-200 rounded-full h-2">
              <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: progress.percentage + '%' }"></div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <label class="block font-medium text-blue-700">Etapa actual</label>
              <p class="text-blue-900">{{ progress.currentStage }}</p>
            </div>
            
            <div>
              <label class="block font-medium text-blue-700">Tiempo estimado restante</label>
              <p class="text-blue-900">{{ progress.estimatedTimeRemaining }}</p>
            </div>
            
            <div>
              <label class="block font-medium text-blue-700">Tablas procesadas</label>
              <p class="text-blue-900">{{ progress.tablesProcessed }} / {{ progress.totalTables }}</p>
            </div>
            
            <div>
              <label class="block font-medium text-blue-700">Velocidad</label>
              <p class="text-blue-900">{{ progress.speed }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end space-x-3 pt-6 border-t border-gray-200">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cerrar
        </button>
        
        <button
          v-if="backup.status === 'completed'"
          @click="downloadBackup"
          class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 flex items-center space-x-2"
        >
          <ArrowDownTrayIcon class="h-4 w-4" />
          <span>Descargar</span>
        </button>
        
        <button
          v-if="backup.status === 'completed'"
          @click="restoreBackup"
          class="px-4 py-2 bg-green-600 text-white rounded-md text-sm font-medium hover:bg-green-700 flex items-center space-x-2"
        >
          <ArrowUturnLeftIcon class="h-4 w-4" />
          <span>Restaurar</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  XMarkIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  ArrowUturnLeftIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  backup: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['close'])

// Reactive state
const progressInterval = ref(null)

const technicalDetails = ref({
  compression: 'gzip',
  hashAlgorithm: 'SHA-256',
  checksum: 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
  postgresVersion: '15.4',
  format: 'Custom (pg_dump)',
  location: '/backups/versaai/backup_2024_01_15_14_30.dump'
})

const dbStats = ref({
  tables: 42,
  records: '1.2M',
  indexes: 156,
  size: '145 MB'
})

const errorDetails = ref({
  errorCode: 'DISK_FULL',
  errorTime: '2024-01-13T14:30:15Z',
  stackTrace: `Traceback (most recent call last):
  File "/app/backup/manager.py", line 123, in create_backup
    self._write_backup_file(data)
  File "/app/backup/manager.py", line 89, in _write_backup_file
    file.write(chunk)
OSError: [Errno 28] No space left on device`
})

const progress = ref({
  percentage: 65,
  currentStage: 'Exportando tabla conversations',
  estimatedTimeRemaining: '1m 23s',
  tablesProcessed: 27,
  totalTables: 42,
  speed: '2.3 MB/s'
})

// Methods
const getStatusIcon = (status) => {
  const icons = {
    completed: CheckCircleIcon,
    failed: ExclamationCircleIcon,
    in_progress: ClockIcon
  }
  return icons[status] || ClockIcon
}

const getStatusIconClass = (status) => {
  const classes = {
    completed: 'text-green-500',
    failed: 'text-red-500',
    in_progress: 'text-blue-500'
  }
  return classes[status] || 'text-gray-500'
}

const getStatusClass = (status) => {
  const classes = {
    completed: 'text-green-600',
    failed: 'text-red-600',
    in_progress: 'text-blue-600'
  }
  return classes[status] || 'text-gray-600'
}

const getStatusLabel = (status) => {
  const labels = {
    completed: 'Completado',
    failed: 'Fallido',
    in_progress: 'En progreso'
  }
  return labels[status] || status
}

const getStatusBannerClass = (status) => {
  const classes = {
    completed: 'bg-green-50 border border-green-200 text-green-800',
    failed: 'bg-red-50 border border-red-200 text-red-800',
    in_progress: 'bg-blue-50 border border-blue-200 text-blue-800'
  }
  return classes[status] || 'bg-gray-50 border border-gray-200 text-gray-800'
}

const getStatusTitle = (status) => {
  const titles = {
    completed: 'Backup Completado Exitosamente',
    failed: 'Backup Falló',
    in_progress: 'Backup en Progreso'
  }
  return titles[status] || 'Estado Desconocido'
}

const getStatusDescription = (status) => {
  const descriptions = {
    completed: 'El backup se ha completado sin errores y está listo para usar.',
    failed: 'El backup falló durante la ejecución. Revisa los detalles del error.',
    in_progress: 'El backup está siendo procesado. Por favor espera a que termine.'
  }
  return descriptions[status] || 'Estado no reconocido'
}

const getTypeClass = (type) => {
  const classes = {
    automatic: 'bg-blue-100 text-blue-800',
    manual: 'bg-green-100 text-green-800',
    scheduled: 'bg-purple-100 text-purple-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getTypeLabel = (type) => {
  const labels = {
    automatic: 'Automático',
    manual: 'Manual',
    scheduled: 'Programado'
  }
  return labels[type] || type
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

const downloadBackup = () => {
  // TODO: Implement backup download
  console.log('Downloading backup:', props.backup.name)
  alert(`Descargando backup: ${props.backup.name}`)
}

const restoreBackup = () => {
  if (confirm(`¿Estás seguro de que quieres restaurar el backup "${props.backup.name}"? Esta acción no se puede deshacer.`)) {
    // TODO: Implement backup restore
    console.log('Restoring backup:', props.backup.name)
    alert(`Restaurando backup: ${props.backup.name}`)
  }
}

const updateProgress = () => {
  if (props.backup.status === 'in_progress') {
    // Simulate progress updates
    progress.value.percentage = Math.min(progress.value.percentage + Math.random() * 5, 95)
    progress.value.tablesProcessed = Math.min(
      Math.floor((progress.value.percentage / 100) * progress.value.totalTables),
      progress.value.totalTables
    )
    
    const remainingTime = Math.max(0, Math.floor((100 - progress.value.percentage) * 2))
    progress.value.estimatedTimeRemaining = `${Math.floor(remainingTime / 60)}m ${remainingTime % 60}s`
  }
}

// Initialize
onMounted(() => {
  console.log('BackupDetailsModal mounted for backup:', props.backup.name)
  
  // Start progress updates for in-progress backups
  if (props.backup.status === 'in_progress') {
    progressInterval.value = setInterval(updateProgress, 2000)
  }
})

onUnmounted(() => {
  if (progressInterval.value) {
    clearInterval(progressInterval.value)
  }
})
</script>