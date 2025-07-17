<template>
  <div class="knowledge-base-detail">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            @click="$router.go(-1)"
            class="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ knowledgeBase.name || 'Base de Conocimiento' }}</h1>
            <p class="text-sm text-gray-500 mt-1">{{ knowledgeBase.description || 'Cargando...' }}</p>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="statusClasses">
            {{ knowledgeBase.status || 'Activa' }}
          </span>
          <button 
            @click="showAddDocumentModal = true"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Agregar Documento
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="text-center">
          <p class="text-2xl font-bold text-gray-900">{{ stats.totalDocuments }}</p>
          <p class="text-sm text-gray-500">Documentos</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-gray-900">{{ stats.totalSize }}</p>
          <p class="text-sm text-gray-500">Tamaño Total</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-gray-900">{{ stats.lastUpdated }}</p>
          <p class="text-sm text-gray-500">Última Actualización</p>
        </div>
        <div class="text-center">
          <p class="text-2xl font-bold text-gray-900">{{ stats.usage }}</p>
          <p class="text-sm text-gray-500">Consultas Este Mes</p>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-hidden">
      <div class="h-full flex">
        <!-- Documents List -->
        <div class="flex-1 flex flex-col">
          <!-- Search and Filters -->
          <div class="bg-white border-b border-gray-200 px-6 py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="relative">
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Buscar documentos..."
                    class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                  <svg class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <select id="document-type-filter" name="document-type-filter" v-model="selectedType" class="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                  <option value="">Todos los tipos</option>
                  <option value="pdf">PDF</option>
                  <option value="txt">Texto</option>
                  <option value="docx">Word</option>
                  <option value="url">URL</option>
                </select>
              </div>
              <div class="flex items-center space-x-2">
                <button class="text-gray-500 hover:text-gray-700">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                </button>
                <button class="text-gray-500 hover:text-gray-700">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Documents -->
          <div class="flex-1 overflow-y-auto p-6">
            <div class="space-y-4">
              <div 
                v-for="document in filteredDocuments" 
                :key="document.id"
                class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div class="flex items-start justify-between">
                  <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                      <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1">
                      <h3 class="text-sm font-medium text-gray-900">{{ document.name }}</h3>
                      <p class="text-sm text-gray-500 mt-1">{{ document.description }}</p>
                      <div class="flex items-center space-x-4 mt-2">
                        <span class="text-xs text-gray-500">{{ document.size }}</span>
                        <span class="text-xs text-gray-500">{{ formatDate(document.updated_at) }}</span>
                        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" :class="getTypeClasses(document.type)">
                          {{ document.type.toUpperCase() }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="editDocument(document)"
                      class="text-gray-400 hover:text-gray-600"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button 
                      @click="deleteDocument(document)"
                      class="text-gray-400 hover:text-red-600"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="w-80 bg-gray-50 border-l border-gray-200 p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración</h3>
          
          <!-- Knowledge Base Settings -->
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Información General</h4>
              <div class="space-y-2">
                <div>
                  <label class="block text-xs font-medium text-gray-700">Nombre</label>
                  <input 
                    v-model="knowledgeBase.name" 
                    type="text" 
                    class="mt-1 block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  >
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700">Descripción</label>
                  <textarea 
                    v-model="knowledgeBase.description" 
                    rows="3" 
                    class="mt-1 block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- Processing Settings -->
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Configuración de Procesamiento</h4>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Auto-indexar</span>
                  <input id="auto-index" name="auto-index" type="checkbox" v-model="knowledgeBase.auto_index" class="rounded">
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Chunking inteligente</span>
                  <input id="smart-chunking" name="smart-chunking" type="checkbox" v-model="knowledgeBase.smart_chunking" class="rounded">
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="bg-white p-4 rounded-lg border border-gray-200">
              <h4 class="text-sm font-medium text-gray-900 mb-2">Acciones</h4>
              <div class="space-y-2">
                <button class="w-full text-left text-sm text-blue-600 hover:text-blue-700 py-1">
                  Reindexar todo
                </button>
                <button class="w-full text-left text-sm text-gray-700 hover:text-gray-900 py-1">
                  Exportar base
                </button>
                <button class="w-full text-left text-sm text-red-600 hover:text-red-700 py-1">
                  Eliminar base
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Document Modal -->
    <div v-if="showAddDocumentModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Agregar Documento</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Tipo de documento</label>
              <select id="new-document-type" name="new-document-type" v-model="newDocument.type" class="mt-1 block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
                <option value="file">Archivo</option>
                <option value="url">URL</option>
                <option value="text">Texto</option>
              </select>
            </div>
            <div v-if="newDocument.type === 'file'">
              <label class="block text-sm font-medium text-gray-700">Archivo</label>
              <input id="document-file" name="document-file" type="file" class="mt-1 block w-full">
            </div>
            <div v-if="newDocument.type === 'url'">
              <label class="block text-sm font-medium text-gray-700">URL</label>
              <input id="document-url" name="document-url" v-model="newDocument.url" type="url" class="mt-1 block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
            </div>
            <div v-if="newDocument.type === 'text'">
              <label class="block text-sm font-medium text-gray-700">Contenido</label>
              <textarea id="document-content" name="document-content" v-model="newDocument.content" rows="4" class="mt-1 block w-full border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"></textarea>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button 
              @click="showAddDocumentModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
            >
              Cancelar
            </button>
            <button 
              @click="addDocument"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
            >
              Agregar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

const route = useRoute()
const toast = useToast()

const knowledgeBaseId = computed(() => route.params.id)
const knowledgeBase = ref({})
const documents = ref([])
const searchQuery = ref('')
const selectedType = ref('')
const showAddDocumentModal = ref(false)
const newDocument = ref({ type: 'file', url: '', content: '' })
const loading = ref(true)

const stats = ref({
  totalDocuments: 0,
  totalSize: '0 MB',
  lastUpdated: 'Hoy',
  usage: 0
})

const statusClasses = computed(() => {
  const status = knowledgeBase.value.status || 'active'
  return {
    'bg-green-100 text-green-800': status === 'active',
    'bg-yellow-100 text-yellow-800': status === 'processing',
    'bg-red-100 text-red-800': status === 'error'
  }
})

const filteredDocuments = computed(() => {
  let filtered = documents.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(doc => 
      doc.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  if (selectedType.value) {
    filtered = filtered.filter(doc => doc.type === selectedType.value)
  }
  
  return filtered
})

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getTypeClasses = (type) => {
  const classes = {
    'pdf': 'bg-red-100 text-red-800',
    'txt': 'bg-gray-100 text-gray-800',
    'docx': 'bg-blue-100 text-blue-800',
    'url': 'bg-green-100 text-green-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const loadKnowledgeBase = async () => {
  try {
    loading.value = true
    // Simulated data - replace with actual API call
    knowledgeBase.value = {
      id: knowledgeBaseId.value,
      name: 'Base de Conocimiento Principal',
      description: 'Documentación y recursos principales de la empresa',
      status: 'active',
      auto_index: true,
      smart_chunking: true
    }
    
    documents.value = [
      {
        id: 1,
        name: 'Manual de Usuario.pdf',
        description: 'Guía completa para usuarios',
        type: 'pdf',
        size: '2.5 MB',
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        name: 'FAQ Productos',
        description: 'Preguntas frecuentes sobre productos',
        type: 'txt',
        size: '150 KB',
        updated_at: new Date(Date.now() - 86400000).toISOString()
      },
      {
        id: 3,
        name: 'Políticas de la Empresa',
        description: 'Documento de políticas internas',
        type: 'docx',
        size: '800 KB',
        updated_at: new Date(Date.now() - 172800000).toISOString()
      }
    ]
    
    stats.value = {
      totalDocuments: documents.value.length,
      totalSize: '3.4 MB',
      lastUpdated: 'Hoy',
      usage: 1247
    }
  } catch (error) {
    console.error('Error loading knowledge base:', error)
    toast.error('Error al cargar la base de conocimiento')
  } finally {
    loading.value = false
  }
}

const addDocument = () => {
  // Implement add document functionality
  toast.success('Documento agregado exitosamente')
  showAddDocumentModal.value = false
  newDocument.value = { type: 'file', url: '', content: '' }
}

const editDocument = (document) => {
  // Implement edit document functionality
  toast.info('Función de edición en desarrollo')
}

const deleteDocument = (document) => {
  // Implement delete document functionality
  if (confirm('¿Estás seguro de que quieres eliminar este documento?')) {
    documents.value = documents.value.filter(d => d.id !== document.id)
    toast.success('Documento eliminado exitosamente')
  }
}

onMounted(() => {
  loadKnowledgeBase()
})
</script>

<style scoped>
.knowledge-base-detail {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
}
</style>