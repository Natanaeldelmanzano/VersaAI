<template>
  <div class="knowledge-bases-page">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Base de Conocimiento</h1>
            <p class="text-gray-600 mt-1">Gestiona documentos y fuentes de información para tus chatbots</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="showUploadModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Subir Documento
            </button>
            <button
              @click="refreshDocuments"
              :disabled="isLoading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-blue-100">Total Documentos</p>
                <p class="text-2xl font-bold">{{ stats.totalDocuments }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-green-100">Procesados</p>
                <p class="text-2xl font-bold">{{ stats.processedDocuments }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-yellow-100">En Proceso</p>
                <p class="text-2xl font-bold">{{ stats.processingDocuments }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-purple-100">Tamaño Total</p>
                <p class="text-2xl font-bold">{{ formatFileSize(stats.totalSize) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Buscar documentos..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @input="debouncedSearch"
            >
          </div>

          <!-- Type Filter -->
          <select
            v-model="filters.type"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los tipos</option>
            <option value="pdf">PDF</option>
            <option value="docx">Word</option>
            <option value="txt">Texto</option>
            <option value="csv">CSV</option>
            <option value="url">URL</option>
          </select>

          <!-- Status Filter -->
          <select
            v-model="filters.status"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="processed">Procesado</option>
            <option value="processing">Procesando</option>
            <option value="failed">Error</option>
          </select>

          <!-- Sort -->
          <select
            v-model="filters.sort"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="created_at_desc">Más recientes</option>
            <option value="created_at_asc">Más antiguos</option>
            <option value="name_asc">Nombre A-Z</option>
            <option value="name_desc">Nombre Z-A</option>
            <option value="size_desc">Tamaño mayor</option>
            <option value="size_asc">Tamaño menor</option>
          </select>
        </div>

        <!-- Clear Filters -->
        <div class="mt-4 flex items-center justify-between">
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Limpiar filtros
          </button>
          <div class="text-sm text-gray-500">
            {{ filteredDocuments.length }} documentos encontrados
          </div>
        </div>
      </div>
    </div>

    <!-- Documents Grid -->
    <div class="flex-1 overflow-y-auto bg-gray-50">
      <div class="p-6">
        <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="animate-pulse">
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div class="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
              <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
              <div class="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>
          </div>
        </div>

        <div v-else-if="filteredDocuments.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No hay documentos</h3>
          <p class="mt-1 text-sm text-gray-500">Comienza subiendo tu primer documento.</p>
          <div class="mt-6">
            <button
              @click="showUploadModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Subir Documento
            </button>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="document in filteredDocuments"
            :key="document.id"
            class="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div class="p-6">
              <div class="flex items-start justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <div :class="getFileTypeIcon(document.type)" class="w-10 h-10 rounded-lg flex items-center justify-center">
                      <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                      </svg>
                    </div>
                  </div>
                  <div class="ml-4 flex-1">
                    <h3 class="text-sm font-medium text-gray-900 truncate">{{ document.name }}</h3>
                    <p class="text-xs text-gray-500 mt-1">{{ document.type.toUpperCase() }} • {{ formatFileSize(document.size) }}</p>
                  </div>
                </div>
                <div class="relative">
                  <button
                    @click="toggleDocumentMenu(document.id)"
                    class="p-1 text-gray-400 hover:text-gray-600 rounded"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                  <div
                    v-if="activeDocumentMenu === document.id"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
                  >
                    <div class="py-1">
                      <button
                        @click="viewDocument(document)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Ver contenido
                      </button>
                      <button
                        @click="downloadDocument(document)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Descargar
                      </button>
                      <button
                        @click="reprocessDocument(document.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Reprocesar
                      </button>
                      <button
                        @click="deleteDocument(document.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-4">
                <div class="flex items-center justify-between">
                  <span :class="getStatusBadgeClass(document.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
                    {{ getStatusText(document.status) }}
                  </span>
                  <span class="text-xs text-gray-500">{{ formatDate(document.created_at) }}</span>
                </div>
                
                <div v-if="document.status === 'processing'" class="mt-3">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: document.progress + '%' }"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">{{ document.progress }}% completado</p>
                </div>
                
                <div v-if="document.chunks" class="mt-3">
                  <p class="text-xs text-gray-500">{{ document.chunks }} fragmentos procesados</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-lg bg-white">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Subir Documento</h3>
          <button
            @click="closeUploadModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <!-- Upload Type Tabs -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button
                @click="uploadType = 'file'"
                :class="[
                  'py-2 px-1 border-b-2 font-medium text-sm',
                  uploadType === 'file'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                Archivo
              </button>
              <button
                @click="uploadType = 'url'"
                :class="[
                  'py-2 px-1 border-b-2 font-medium text-sm',
                  uploadType === 'url'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                URL
              </button>
              <button
                @click="uploadType = 'text'"
                :class="[
                  'py-2 px-1 border-b-2 font-medium text-sm',
                  uploadType === 'text'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                Texto
              </button>
            </nav>
          </div>
          
          <!-- File Upload -->
          <div v-if="uploadType === 'file'" class="space-y-4">
            <div
              @drop="handleFileDrop"
              @dragover.prevent
              @dragenter.prevent
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors"
            >
              <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="mt-4">
                <label for="file-upload" class="cursor-pointer">
                  <span class="mt-2 block text-sm font-medium text-gray-900">
                    Arrastra archivos aquí o 
                    <span class="text-blue-600">selecciona archivos</span>
                  </span>
                  <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple @change="handleFileSelect" accept=".pdf,.docx,.txt,.csv">
                </label>
                <p class="mt-2 text-xs text-gray-500">
                  PDF, DOCX, TXT, CSV hasta 10MB
                </p>
              </div>
            </div>
            
            <!-- Selected Files -->
            <div v-if="selectedFiles.length > 0" class="space-y-2">
              <h4 class="text-sm font-medium text-gray-900">Archivos seleccionados:</h4>
              <div class="space-y-2">
                <div v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between p-2 bg-gray-50 rounded">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 text-gray-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-sm text-gray-900">{{ file.name }}</span>
                    <span class="text-xs text-gray-500 ml-2">({{ formatFileSize(file.size) }})</span>
                  </div>
                  <button @click="removeFile(index)" class="text-red-500 hover:text-red-700">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- URL Upload -->
          <div v-if="uploadType === 'url'" class="space-y-4">
            <div>
              <label for="url-input" class="block text-sm font-medium text-gray-700">URL del documento</label>
              <input
                id="url-input"
                v-model="urlInput"
                type="url"
                placeholder="https://ejemplo.com/documento.pdf"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
          </div>
          
          <!-- Text Upload -->
          <div v-if="uploadType === 'text'" class="space-y-4">
            <div>
              <label for="text-name" class="block text-sm font-medium text-gray-700">Nombre del documento</label>
              <input
                id="text-name"
                v-model="textName"
                type="text"
                placeholder="Mi documento de texto"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
            <div>
              <label for="text-content" class="block text-sm font-medium text-gray-700">Contenido</label>
              <textarea
                id="text-content"
                v-model="textContent"
                rows="8"
                placeholder="Escribe o pega el contenido del documento aquí..."
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              ></textarea>
            </div>
          </div>
          
          <!-- Upload Progress -->
          <div v-if="uploadProgress > 0" class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-700">Subiendo...</span>
              <span class="text-gray-500">{{ uploadProgress }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: uploadProgress + '%' }"></div>
            </div>
          </div>
        </div>
        
        <!-- Modal Actions -->
        <div class="flex items-center justify-end space-x-3 mt-6">
          <button
            @click="closeUploadModal"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            @click="uploadDocument"
            :disabled="!canUpload || uploadProgress > 0"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ uploadProgress > 0 ? 'Subiendo...' : 'Subir' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { debounce } from 'lodash-es'

export default {
  name: 'KnowledgeBases',
  setup() {
    const toast = useToast()
    
    // State
    const isLoading = ref(false)
    const documents = ref([])
    const showUploadModal = ref(false)
    const uploadType = ref('file')
    const selectedFiles = ref([])
    const urlInput = ref('')
    const textName = ref('')
    const textContent = ref('')
    const uploadProgress = ref(0)
    const activeDocumentMenu = ref(null)
    
    // Filters
    const filters = ref({
      search: '',
      type: '',
      status: '',
      sort: 'created_at_desc'
    })
    
    // Stats
    const stats = ref({
      totalDocuments: 0,
      processedDocuments: 0,
      processingDocuments: 0,
      totalSize: 0
    })
    
    // Computed
    const hasActiveFilters = computed(() => {
      return filters.value.search || filters.value.type || filters.value.status
    })
    
    const filteredDocuments = computed(() => {
      let filtered = [...documents.value]
      
      if (filters.value.search) {
        filtered = filtered.filter(doc => 
          doc.name.toLowerCase().includes(filters.value.search.toLowerCase())
        )
      }
      
      if (filters.value.type) {
        filtered = filtered.filter(doc => doc.type === filters.value.type)
      }
      
      if (filters.value.status) {
        filtered = filtered.filter(doc => doc.status === filters.value.status)
      }
      
      // Sort
      const [field, direction] = filters.value.sort.split('_')
      filtered.sort((a, b) => {
        let aVal = a[field]
        let bVal = b[field]
        
        if (field === 'created_at') {
          aVal = new Date(aVal)
          bVal = new Date(bVal)
        }
        
        if (direction === 'desc') {
          return bVal > aVal ? 1 : -1
        } else {
          return aVal > bVal ? 1 : -1
        }
      })
      
      return filtered
    })
    
    const canUpload = computed(() => {
      if (uploadType.value === 'file') {
        return selectedFiles.value.length > 0
      } else if (uploadType.value === 'url') {
        return urlInput.value.trim() !== ''
      } else if (uploadType.value === 'text') {
        return textName.value.trim() !== '' && textContent.value.trim() !== ''
      }
      return false
    })
    
    // Mock data
    const mockDocuments = [
      {
        id: 1,
        name: 'Manual de Usuario.pdf',
        type: 'pdf',
        status: 'processed',
        size: 2048576,
        chunks: 45,
        created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        progress: 100
      },
      {
        id: 2,
        name: 'Políticas de la Empresa.docx',
        type: 'docx',
        status: 'processing',
        size: 1024000,
        chunks: 0,
        created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        progress: 65
      },
      {
        id: 3,
        name: 'FAQ Productos.txt',
        type: 'txt',
        status: 'processed',
        size: 512000,
        chunks: 23,
        created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
        progress: 100
      },
      {
        id: 4,
        name: 'Datos de Ventas.csv',
        type: 'csv',
        status: 'failed',
        size: 256000,
        chunks: 0,
        created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        progress: 0
      },
      {
        id: 5,
        name: 'Documentación API',
        type: 'url',
        status: 'processed',
        size: 0,
        chunks: 78,
        created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        progress: 100
      }
    ]
    
    // Methods
    const loadDocuments = async () => {
      try {
        isLoading.value = true
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        documents.value = mockDocuments
        
        // Calculate stats
        stats.value = {
          totalDocuments: documents.value.length,
          processedDocuments: documents.value.filter(doc => doc.status === 'processed').length,
          processingDocuments: documents.value.filter(doc => doc.status === 'processing').length,
          totalSize: documents.value.reduce((sum, doc) => sum + doc.size, 0)
        }
        
      } catch (error) {
        console.error('Error loading documents:', error)
        toast.error('Error al cargar los documentos')
      } finally {
        isLoading.value = false
      }
    }
    
    const refreshDocuments = () => {
      loadDocuments()
    }
    
    const applyFilters = () => {
      // Filters are applied via computed property
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        type: '',
        status: '',
        sort: 'created_at_desc'
      }
    }
    
    const debouncedSearch = debounce(() => {
      applyFilters()
    }, 300)
    
    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      selectedFiles.value = [...selectedFiles.value, ...files]
    }
    
    const handleFileDrop = (event) => {
      event.preventDefault()
      const files = Array.from(event.dataTransfer.files)
      selectedFiles.value = [...selectedFiles.value, ...files]
    }
    
    const removeFile = (index) => {
      selectedFiles.value.splice(index, 1)
    }
    
    const uploadDocument = async () => {
      try {
        uploadProgress.value = 0
        
        // Simulate upload progress
        const interval = setInterval(() => {
          uploadProgress.value += 10
          if (uploadProgress.value >= 100) {
            clearInterval(interval)
            
            // Add new document to list
            const newDoc = {
              id: Date.now(),
              name: uploadType.value === 'file' ? selectedFiles.value[0]?.name : 
                    uploadType.value === 'url' ? 'Documento desde URL' : textName.value,
              type: uploadType.value === 'file' ? selectedFiles.value[0]?.name.split('.').pop() : uploadType.value,
              status: 'processing',
              size: uploadType.value === 'file' ? selectedFiles.value[0]?.size : textContent.value.length,
              chunks: 0,
              created_at: new Date().toISOString(),
              progress: 0
            }
            
            documents.value.unshift(newDoc)
            
            toast.success('Documento subido exitosamente')
            closeUploadModal()
            
            // Simulate processing
            setTimeout(() => {
              const doc = documents.value.find(d => d.id === newDoc.id)
              if (doc) {
                doc.status = 'processed'
                doc.progress = 100
                doc.chunks = Math.floor(Math.random() * 50) + 10
              }
            }, 3000)
          }
        }, 200)
        
      } catch (error) {
        console.error('Upload error:', error)
        toast.error('Error al subir el documento')
        uploadProgress.value = 0
      }
    }
    
    const closeUploadModal = () => {
      showUploadModal.value = false
      uploadType.value = 'file'
      selectedFiles.value = []
      urlInput.value = ''
      textName.value = ''
      textContent.value = ''
      uploadProgress.value = 0
    }
    
    const toggleDocumentMenu = (id) => {
      activeDocumentMenu.value = activeDocumentMenu.value === id ? null : id
    }
    
    const viewDocument = (document) => {
      toast.info(`Viendo contenido de: ${document.name}`)
      activeDocumentMenu.value = null
    }
    
    const downloadDocument = (document) => {
      toast.info(`Descargando: ${document.name}`)
      activeDocumentMenu.value = null
    }
    
    const reprocessDocument = (id) => {
      const doc = documents.value.find(d => d.id === id)
      if (doc) {
        doc.status = 'processing'
        doc.progress = 0
        toast.info('Reprocesando documento...')
        
        // Simulate reprocessing
        setTimeout(() => {
          doc.status = 'processed'
          doc.progress = 100
          toast.success('Documento reprocesado exitosamente')
        }, 3000)
      }
      activeDocumentMenu.value = null
    }
    
    const deleteDocument = (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar este documento?')) {
        documents.value = documents.value.filter(doc => doc.id !== id)
        toast.success('Documento eliminado')
      }
      activeDocumentMenu.value = null
    }
    
    // Utility functions
    const getFileTypeIcon = (type) => {
      const icons = {
        pdf: 'bg-red-500',
        docx: 'bg-blue-500',
        txt: 'bg-gray-500',
        csv: 'bg-green-500',
        url: 'bg-purple-500'
      }
      return icons[type] || 'bg-gray-500'
    }
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        processed: 'bg-green-100 text-green-800',
        processing: 'bg-yellow-100 text-yellow-800',
        failed: 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
    
    const getStatusText = (status) => {
      const texts = {
        processed: 'Procesado',
        processing: 'Procesando',
        failed: 'Error'
      }
      return texts[status] || 'Desconocido'
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInHours = (now - date) / (1000 * 60 * 60)
      
      if (diffInHours < 1) {
        return 'Hace unos minutos'
      } else if (diffInHours < 24) {
        return `Hace ${Math.floor(diffInHours)} horas`
      } else if (diffInHours < 48) {
        return 'Ayer'
      } else {
        return date.toLocaleDateString('es-ES', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        })
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadDocuments()
    })
    
    // Close menu when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        activeDocumentMenu.value = null
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })
    
    return {
      // State
      isLoading,
      documents,
      showUploadModal,
      uploadType,
      selectedFiles,
      urlInput,
      textName,
      textContent,
      uploadProgress,
      activeDocumentMenu,
      filters,
      stats,
      
      // Computed
      hasActiveFilters,
      filteredDocuments,
      canUpload,
      
      // Methods
      refreshDocuments,
      applyFilters,
      clearFilters,
      debouncedSearch,
      handleFileSelect,
      handleFileDrop,
      removeFile,
      uploadDocument,
      closeUploadModal,
      toggleDocumentMenu,
      viewDocument,
      downloadDocument,
      reprocessDocument,
      deleteDocument,
      
      // Utilities
      getFileTypeIcon,
      getStatusBadgeClass,
      getStatusText,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.knowledge-bases-page {
  @apply h-full flex flex-col;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>