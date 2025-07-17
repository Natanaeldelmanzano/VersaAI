<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Bases de Conocimiento</h1>
        <p class="text-gray-600">Gestiona documentos y contenido para entrenar tus chatbots</p>
      </div>
      <button
        @click="showCreateModal = true"
        class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
      >
        Nueva Base de Conocimiento
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <DocumentTextIcon class="h-8 w-8 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Total Documentos</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalDocuments }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <FolderIcon class="h-8 w-8 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Bases Activas</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.activeBases }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <CloudArrowUpIcon class="h-8 w-8 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Almacenamiento</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.storageUsed }}MB</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <CpuChipIcon class="h-8 w-8 text-orange-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Procesando</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.processing }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Buscar
          </label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Buscar bases de conocimiento..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Estado
          </label>
          <select
            v-model="filters.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activa</option>
            <option value="processing">Procesando</option>
            <option value="error">Error</option>
            <option value="inactive">Inactiva</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Ordenar por
          </label>
          <select
            v-model="filters.sortBy"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="created_at">Fecha de creación</option>
            <option value="name">Nombre</option>
            <option value="documents_count">Número de documentos</option>
            <option value="size">Tamaño</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Knowledge Bases Grid -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
      <p class="text-gray-500 mt-2">Cargando bases de conocimiento...</p>
    </div>
    
    <div v-else-if="filteredKnowledgeBases.length === 0" class="text-center py-12">
      <FolderIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <p class="text-gray-500">No se encontraron bases de conocimiento</p>
      <button
        @click="showCreateModal = true"
        class="mt-4 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
      >
        Crear la primera base
      </button>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="kb in filteredKnowledgeBases"
        :key="kb.id"
        class="bg-white rounded-lg shadow hover:shadow-lg transition-shadow duration-200 cursor-pointer"
        @click="viewKnowledgeBase(kb)"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <FolderIcon class="h-8 w-8 text-primary-600" />
              </div>
              <div class="ml-3">
                <h3 class="text-lg font-semibold text-gray-900">{{ kb.name }}</h3>
                <p class="text-sm text-gray-500">{{ kb.documentsCount }} documentos</p>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <span
                :class="[
                  'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                  kb.status === 'active' ? 'bg-green-100 text-green-800' :
                  kb.status === 'processing' ? 'bg-yellow-100 text-yellow-800' :
                  kb.status === 'error' ? 'bg-red-100 text-red-800' :
                  'bg-gray-100 text-gray-800'
                ]"
              >
                {{ getStatusLabel(kb.status) }}
              </span>
              
              <div class="relative">
                <button
                  @click.stop="toggleDropdown(kb.id)"
                  class="text-gray-400 hover:text-gray-600"
                >
                  <EllipsisVerticalIcon class="h-5 w-5" />
                </button>
                
                <div
                  v-if="activeDropdown === kb.id"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
                >
                  <div class="py-1">
                    <button
                      @click="editKnowledgeBase(kb)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Editar
                    </button>
                    <button
                      @click="uploadDocuments(kb)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Subir documentos
                    </button>
                    <button
                      @click="reprocessKnowledgeBase(kb)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Reprocesar
                    </button>
                    <button
                      @click="duplicateKnowledgeBase(kb)"
                      class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Duplicar
                    </button>
                    <hr class="my-1" />
                    <button
                      @click="deleteKnowledgeBase(kb)"
                      class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ kb.description }}</p>
          
          <div class="flex items-center justify-between text-sm text-gray-500">
            <span>{{ formatFileSize(kb.size) }}</span>
            <span>{{ formatDate(kb.updatedAt) }}</span>
          </div>
          
          <!-- Progress bar for processing -->
          <div v-if="kb.status === 'processing'" class="mt-4">
            <div class="flex justify-between text-xs text-gray-600 mb-1">
              <span>Procesando...</span>
              <span>{{ kb.progress || 0 }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${kb.progress || 0}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Knowledge Base Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showCreateModal = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Nueva Base de Conocimiento</h3>
          
          <form @submit.prevent="createKnowledgeBase" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nombre
              </label>
              <input
                v-model="createForm.name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Descripción
              </label>
              <textarea
                v-model="createForm.description"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Describe el contenido de esta base de conocimiento..."
              ></textarea>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="createLoading"
                class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 disabled:opacity-50"
              >
                {{ createLoading ? 'Creando...' : 'Crear Base' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Upload Documents Modal -->
    <div
      v-if="showUploadModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showUploadModal = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            Subir Documentos a {{ selectedKB?.name }}
          </h3>
          
          <div class="space-y-4">
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-primary-500 transition-colors duration-200"
              @drop="handleDrop"
              @dragover.prevent
              @dragenter.prevent
            >
              <CloudArrowUpIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p class="text-gray-600 mb-2">Arrastra archivos aquí o</p>
              <input
                ref="fileInput"
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.txt,.md"
                @change="handleFileSelect"
                class="hidden"
              />
              <button
                @click="$refs.fileInput.click()"
                class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Seleccionar archivos
              </button>
              <p class="text-xs text-gray-500 mt-2">
                Formatos soportados: PDF, DOC, DOCX, TXT, MD
              </p>
            </div>
            
            <div v-if="uploadFiles.length > 0" class="space-y-2">
              <h4 class="text-sm font-medium text-gray-900">Archivos seleccionados:</h4>
              <div class="max-h-32 overflow-y-auto">
                <div
                  v-for="(file, index) in uploadFiles"
                  :key="index"
                  class="flex items-center justify-between p-2 bg-gray-50 rounded"
                >
                  <span class="text-sm text-gray-700 truncate">{{ file.name }}</span>
                  <button
                    @click="removeFile(index)"
                    class="text-red-500 hover:text-red-700"
                  >
                    <XMarkIcon class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showUploadModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
              >
                Cancelar
              </button>
              <button
                @click="uploadDocumentsToKB"
                :disabled="uploadFiles.length === 0 || uploadLoading"
                class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 disabled:opacity-50"
              >
                {{ uploadLoading ? 'Subiendo...' : 'Subir Documentos' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  DocumentTextIcon,
  FolderIcon,
  CloudArrowUpIcon,
  CpuChipIcon,
  EllipsisVerticalIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/api'

const toast = useToast()

const loading = ref(false)
const createLoading = ref(false)
const uploadLoading = ref(false)
const knowledgeBases = ref([])
const activeDropdown = ref(null)
const showCreateModal = ref(false)
const showUploadModal = ref(false)
const selectedKB = ref(null)
const uploadFiles = ref([])
const fileInput = ref(null)

const filters = ref({
  search: '',
  status: '',
  sortBy: 'created_at'
})

const stats = ref({
  totalDocuments: 0,
  activeBases: 0,
  storageUsed: 0,
  processing: 0
})

const createForm = ref({
  name: '',
  description: ''
})

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activa',
    processing: 'Procesando',
    error: 'Error',
    inactive: 'Inactiva'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  return format(new Date(date), 'dd MMM yyyy', { locale: es })
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const filteredKnowledgeBases = computed(() => {
  let filtered = knowledgeBases.value
  
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(kb => 
      kb.name.toLowerCase().includes(search) ||
      kb.description.toLowerCase().includes(search)
    )
  }
  
  if (filters.value.status) {
    filtered = filtered.filter(kb => kb.status === filters.value.status)
  }
  
  // Sort
  filtered.sort((a, b) => {
    switch (filters.value.sortBy) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'documents_count':
        return b.documentsCount - a.documentsCount
      case 'size':
        return b.size - a.size
      default:
        return new Date(b.createdAt) - new Date(a.createdAt)
    }
  })
  
  return filtered
})

const fetchKnowledgeBases = async () => {
  loading.value = true
  try {
    const response = await api.get('/knowledge-bases')
    knowledgeBases.value = response.data
  } catch (error) {
    console.error('Error fetching knowledge bases:', error)
    toast.error('Error al cargar las bases de conocimiento')
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    const response = await api.get('/knowledge-bases/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

const createKnowledgeBase = async () => {
  createLoading.value = true
  try {
    await api.post('/knowledge-bases', createForm.value)
    toast.success('Base de conocimiento creada correctamente')
    showCreateModal.value = false
    createForm.value = { name: '', description: '' }
    await fetchKnowledgeBases()
    await fetchStats()
  } catch (error) {
    console.error('Error creating knowledge base:', error)
    toast.error('Error al crear la base de conocimiento')
  } finally {
    createLoading.value = false
  }
}

const toggleDropdown = (id) => {
  activeDropdown.value = activeDropdown.value === id ? null : id
}

const viewKnowledgeBase = (kb) => {
  // TODO: Navigate to knowledge base detail view
  toast.info('Vista detallada próximamente')
}

const editKnowledgeBase = (kb) => {
  // TODO: Implement edit functionality
  toast.info('Funcionalidad de edición próximamente')
}

const uploadDocuments = (kb) => {
  selectedKB.value = kb
  showUploadModal.value = true
  activeDropdown.value = null
}

const reprocessKnowledgeBase = async (kb) => {
  try {
    await api.post(`/knowledge-bases/${kb.id}/reprocess`)
    toast.success('Reprocesamiento iniciado')
    await fetchKnowledgeBases()
  } catch (error) {
    console.error('Error reprocessing knowledge base:', error)
    toast.error('Error al reprocesar la base de conocimiento')
  }
  activeDropdown.value = null
}

const duplicateKnowledgeBase = async (kb) => {
  try {
    await api.post(`/knowledge-bases/${kb.id}/duplicate`)
    toast.success('Base de conocimiento duplicada correctamente')
    await fetchKnowledgeBases()
  } catch (error) {
    console.error('Error duplicating knowledge base:', error)
    toast.error('Error al duplicar la base de conocimiento')
  }
  activeDropdown.value = null
}

const deleteKnowledgeBase = async (kb) => {
  if (!confirm(`¿Estás seguro de que quieres eliminar "${kb.name}"?`)) {
    activeDropdown.value = null
    return
  }
  
  try {
    await api.delete(`/knowledge-bases/${kb.id}`)
    toast.success('Base de conocimiento eliminada correctamente')
    await fetchKnowledgeBases()
    await fetchStats()
  } catch (error) {
    console.error('Error deleting knowledge base:', error)
    toast.error('Error al eliminar la base de conocimiento')
  }
  activeDropdown.value = null
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  uploadFiles.value = [...uploadFiles.value, ...files]
}

const handleDrop = (event) => {
  event.preventDefault()
  const files = Array.from(event.dataTransfer.files)
  uploadFiles.value = [...uploadFiles.value, ...files]
}

const removeFile = (index) => {
  uploadFiles.value.splice(index, 1)
}

const uploadDocumentsToKB = async () => {
  if (uploadFiles.value.length === 0) return
  
  uploadLoading.value = true
  try {
    const formData = new FormData()
    uploadFiles.value.forEach(file => {
      formData.append('documents', file)
    })
    
    await api.post(`/knowledge-bases/${selectedKB.value.id}/documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    toast.success('Documentos subidos correctamente')
    showUploadModal.value = false
    uploadFiles.value = []
    selectedKB.value = null
    await fetchKnowledgeBases()
    await fetchStats()
  } catch (error) {
    console.error('Error uploading documents:', error)
    toast.error('Error al subir los documentos')
  } finally {
    uploadLoading.value = false
  }
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeDropdown.value = null
  }
}

onMounted(async () => {
  await Promise.all([
    fetchKnowledgeBases(),
    fetchStats()
  ])
  
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