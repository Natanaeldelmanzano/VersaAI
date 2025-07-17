<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-10 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900">Historial de Backups</h3>
          <p class="text-sm text-gray-600 mt-1">Gestiona y restaura backups de la base de datos</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-blue-50 rounded-lg p-4">
          <div class="flex items-center">
            <CircleStackIcon class="h-8 w-8 text-blue-600 mr-3" />
            <div>
              <p class="text-2xl font-bold text-blue-600">{{ stats.totalBackups }}</p>
              <p class="text-sm text-blue-600">Total Backups</p>
            </div>
          </div>
        </div>
        
        <div class="bg-green-50 rounded-lg p-4">
          <div class="flex items-center">
            <CheckCircleIcon class="h-8 w-8 text-green-600 mr-3" />
            <div>
              <p class="text-2xl font-bold text-green-600">{{ stats.successfulBackups }}</p>
              <p class="text-sm text-green-600">Exitosos</p>
            </div>
          </div>
        </div>
        
        <div class="bg-yellow-50 rounded-lg p-4">
          <div class="flex items-center">
            <ClockIcon class="h-8 w-8 text-yellow-600 mr-3" />
            <div>
              <p class="text-2xl font-bold text-yellow-600">{{ stats.totalSize }}</p>
              <p class="text-sm text-yellow-600">Tamaño Total</p>
            </div>
          </div>
        </div>
        
        <div class="bg-purple-50 rounded-lg p-4">
          <div class="flex items-center">
            <CalendarIcon class="h-8 w-8 text-purple-600 mr-3" />
            <div>
              <p class="text-2xl font-bold text-purple-600">{{ stats.lastBackup }}</p>
              <p class="text-sm text-purple-600">Último Backup</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="flex flex-col sm:flex-row gap-4 mb-6">
        <div class="flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar backups..."
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="flex gap-2">
          <select
            v-model="filterType"
            class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Todos los tipos</option>
            <option value="automatic">Automático</option>
            <option value="manual">Manual</option>
            <option value="scheduled">Programado</option>
          </select>
          
          <select
            v-model="filterStatus"
            class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Todos los estados</option>
            <option value="completed">Completado</option>
            <option value="failed">Fallido</option>
            <option value="in_progress">En progreso</option>
          </select>
          
          <button
            @click="createManualBackup"
            :disabled="creatingBackup"
            class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 whitespace-nowrap"
          >
            {{ creatingBackup ? 'Creando...' : 'Nuevo Backup' }}
          </button>
        </div>
      </div>

      <!-- Backup List -->
      <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Backup
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tamaño
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duración
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fecha
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="backup in filteredBackups"
                :key="backup.id"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <CircleStackIcon class="h-5 w-5 text-gray-400 mr-3" />
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ backup.name }}</div>
                      <div class="text-sm text-gray-500">{{ backup.description }}</div>
                    </div>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getTypeClass(backup.type)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ getTypeLabel(backup.type) }}
                  </span>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <component :is="getStatusIcon(backup.status)" :class="getStatusIconClass(backup.status)" class="h-4 w-4 mr-2" />
                    <span :class="getStatusClass(backup.status)" class="text-sm font-medium">
                      {{ getStatusLabel(backup.status) }}
                    </span>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ backup.size }}
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ backup.duration }}
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div>
                    <div>{{ formatDate(backup.createdAt) }}</div>
                    <div class="text-xs text-gray-500">{{ formatTime(backup.createdAt) }}</div>
                  </div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end space-x-2">
                    <button
                      v-if="backup.status === 'completed'"
                      @click="downloadBackup(backup)"
                      class="text-blue-600 hover:text-blue-900 p-1 rounded"
                      title="Descargar"
                    >
                      <ArrowDownTrayIcon class="h-4 w-4" />
                    </button>
                    
                    <button
                      v-if="backup.status === 'completed'"
                      @click="restoreBackup(backup)"
                      class="text-green-600 hover:text-green-900 p-1 rounded"
                      title="Restaurar"
                    >
                      <ArrowUturnLeftIcon class="h-4 w-4" />
                    </button>
                    
                    <button
                      @click="viewBackupDetails(backup)"
                      class="text-gray-600 hover:text-gray-900 p-1 rounded"
                      title="Ver detalles"
                    >
                      <EyeIcon class="h-4 w-4" />
                    </button>
                    
                    <button
                      @click="deleteBackup(backup)"
                      class="text-red-600 hover:text-red-900 p-1 rounded"
                      title="Eliminar"
                    >
                      <TrashIcon class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="filteredBackups.length === 0" class="text-center py-12">
          <CircleStackIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-500">No se encontraron backups</p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-between mt-6">
        <div class="text-sm text-gray-700">
          Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredBackups.length) }} de {{ filteredBackups.length }} backups
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

      <!-- Actions -->
      <div class="flex items-center justify-end space-x-3 mt-8 pt-6 border-t border-gray-200">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cerrar
        </button>
      </div>
    </div>
    
    <!-- Backup Details Modal -->
    <BackupDetailsModal
      v-if="showDetailsModal"
      :backup="selectedBackup"
      @close="showDetailsModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  CircleStackIcon,
  CheckCircleIcon,
  ClockIcon,
  CalendarIcon,
  ArrowDownTrayIcon,
  ArrowUturnLeftIcon,
  EyeIcon,
  TrashIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import BackupDetailsModal from './BackupDetailsModal.vue'

// Emits
const emit = defineEmits(['close'])

// Reactive state
const searchQuery = ref('')
const filterType = ref('all')
const filterStatus = ref('all')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const creatingBackup = ref(false)
const showDetailsModal = ref(false)
const selectedBackup = ref(null)

const stats = ref({
  totalBackups: 24,
  successfulBackups: 22,
  totalSize: '2.4 GB',
  lastBackup: '2h ago'
})

const backups = ref([
  {
    id: 1,
    name: 'backup_2024_01_15_14_30',
    description: 'Backup automático diario',
    type: 'automatic',
    status: 'completed',
    size: '156 MB',
    duration: '2m 34s',
    createdAt: '2024-01-15T14:30:00Z',
    completedAt: '2024-01-15T14:32:34Z'
  },
  {
    id: 2,
    name: 'backup_manual_2024_01_14',
    description: 'Backup manual antes de actualización',
    type: 'manual',
    status: 'completed',
    size: '148 MB',
    duration: '2m 12s',
    createdAt: '2024-01-14T10:15:00Z',
    completedAt: '2024-01-14T10:17:12Z'
  },
  {
    id: 3,
    name: 'backup_2024_01_14_14_30',
    description: 'Backup automático diario',
    type: 'automatic',
    status: 'completed',
    size: '152 MB',
    duration: '2m 45s',
    createdAt: '2024-01-14T14:30:00Z',
    completedAt: '2024-01-14T14:32:45Z'
  },
  {
    id: 4,
    name: 'backup_2024_01_13_14_30',
    description: 'Backup automático diario',
    type: 'automatic',
    status: 'failed',
    size: '0 MB',
    duration: '0m 15s',
    createdAt: '2024-01-13T14:30:00Z',
    error: 'Insufficient disk space'
  },
  {
    id: 5,
    name: 'backup_scheduled_weekly',
    description: 'Backup semanal programado',
    type: 'scheduled',
    status: 'in_progress',
    size: '89 MB',
    duration: '1m 23s',
    createdAt: '2024-01-15T15:00:00Z'
  }
])

// Computed
const filteredBackups = computed(() => {
  let filtered = backups.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(backup => 
      backup.name.toLowerCase().includes(query) ||
      backup.description.toLowerCase().includes(query)
    )
  }
  
  if (filterType.value !== 'all') {
    filtered = filtered.filter(backup => backup.type === filterType.value)
  }
  
  if (filterStatus.value !== 'all') {
    filtered = filtered.filter(backup => backup.status === filterStatus.value)
  }
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredBackups.value.length / itemsPerPage.value)
})

// Methods
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
    in_progress: 'text-yellow-500'
  }
  return classes[status] || 'text-gray-500'
}

const getStatusClass = (status) => {
  const classes = {
    completed: 'text-green-600',
    failed: 'text-red-600',
    in_progress: 'text-yellow-600'
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
    minute: '2-digit'
  })
}

const createManualBackup = async () => {
  creatingBackup.value = true
  
  try {
    // TODO: Create manual backup
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const newBackup = {
      id: Date.now(),
      name: `backup_manual_${new Date().toISOString().split('T')[0]}`,
      description: 'Backup manual creado por usuario',
      type: 'manual',
      status: 'completed',
      size: '145 MB',
      duration: '2m 18s',
      createdAt: new Date().toISOString(),
      completedAt: new Date().toISOString()
    }
    
    backups.value.unshift(newBackup)
    stats.value.totalBackups++
    stats.value.successfulBackups++
    
    alert('Backup creado exitosamente')
  } catch (error) {
    console.error('Error creating backup:', error)
    alert('Error al crear el backup')
  } finally {
    creatingBackup.value = false
  }
}

const downloadBackup = (backup) => {
  // TODO: Implement backup download
  console.log('Downloading backup:', backup.name)
  alert(`Descargando backup: ${backup.name}`)
}

const restoreBackup = (backup) => {
  if (confirm(`¿Estás seguro de que quieres restaurar el backup "${backup.name}"? Esta acción no se puede deshacer.`)) {
    // TODO: Implement backup restore
    console.log('Restoring backup:', backup.name)
    alert(`Restaurando backup: ${backup.name}`)
  }
}

const viewBackupDetails = (backup) => {
  selectedBackup.value = backup
  showDetailsModal.value = true
}

const deleteBackup = (backup) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el backup "${backup.name}"?`)) {
    const index = backups.value.findIndex(b => b.id === backup.id)
    if (index !== -1) {
      backups.value.splice(index, 1)
      stats.value.totalBackups--
      if (backup.status === 'completed') {
        stats.value.successfulBackups--
      }
    }
  }
}

// Initialize
onMounted(() => {
  console.log('BackupHistoryModal mounted')
})
</script>