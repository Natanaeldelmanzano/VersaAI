<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Gestión de Conocimiento</h1>
          <p class="text-gray-600 mt-2">Administra la base de conocimientos y documentación</p>
        </div>
        <div class="flex space-x-3">
          <button
            @click="showUploadModal = true"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
          >
            <DocumentPlusIcon class="h-5 w-5" />
            <span>Subir Documento</span>
          </button>
          <button
            @click="showCategoryModal = true"
            class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2"
          >
            <FolderPlusIcon class="h-5 w-5" />
            <span>Nueva Categoría</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-blue-100 rounded-lg">
            <DocumentTextIcon class="h-6 w-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Documentos</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.totalDocuments }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-green-100 rounded-lg">
            <FolderIcon class="h-6 w-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Categorías</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.categories }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-yellow-100 rounded-lg">
            <EyeIcon class="h-6 w-6 text-yellow-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Vistas Este Mes</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.monthlyViews }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-purple-100 rounded-lg">
            <MagnifyingGlassIcon class="h-6 w-6 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Búsquedas</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.searches }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white rounded-lg shadow mb-6">
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="md:col-span-2">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar documentos..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <!-- Category Filter -->
          <div>
            <select
              v-model="selectedCategory"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todas las categorías</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          
          <!-- Type Filter -->
          <div>
            <select
              v-model="selectedType"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Todos los tipos</option>
              <option value="pdf">PDF</option>
              <option value="doc">Word</option>
              <option value="txt">Texto</option>
              <option value="md">Markdown</option>
              <option value="url">Enlaces</option>
            </select>
          </div>
        </div>
        
        <!-- View Toggle -->
        <div class="flex items-center justify-between mt-4">
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">{{ filteredDocuments.length }} documentos encontrados</span>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">Ordenar por:</span>
              <select
                v-model="sortBy"
                class="text-sm border border-gray-300 rounded px-2 py-1 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="name">Nombre</option>
                <option value="date">Fecha</option>
                <option value="views">Vistas</option>
                <option value="size">Tamaño</option>
              </select>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'p-2 rounded',
                viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
              ]"
            >
              <Squares2X2Icon class="h-5 w-5" />
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'p-2 rounded',
                viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
              ]"
            >
              <ListBulletIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Documents Grid/List -->
    <div class="bg-white rounded-lg shadow">
      <div class="p-6">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <DocumentCard
            v-for="document in paginatedDocuments"
            :key="document.id"
            :document="document"
            @view="viewDocument"
            @edit="editDocument"
            @delete="deleteDocument"
            @download="downloadDocument"
          />
        </div>
        
        <!-- List View -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Documento
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Categoría
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tamaño
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vistas
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
              <tr v-for="document in paginatedDocuments" :key="document.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div :class="[
                        'h-10 w-10 rounded-lg flex items-center justify-center',
                        getTypeColor(document.type)
                      ]">
                        <component :is="getTypeIcon(document.type)" class="h-6 w-6" />
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ document.name }}</div>
                      <div class="text-sm text-gray-500">{{ document.description }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ getCategoryName(document.categoryId) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ document.type.toUpperCase() }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatFileSize(document.size) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ document.views }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(document.updatedAt) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end space-x-2">
                    <button
                      @click="viewDocument(document)"
                      class="text-blue-600 hover:text-blue-900"
                    >
                      <EyeIcon class="h-4 w-4" />
                    </button>
                    <button
                      @click="downloadDocument(document)"
                      class="text-green-600 hover:text-green-900"
                    >
                      <ArrowDownTrayIcon class="h-4 w-4" />
                    </button>
                    <button
                      @click="editDocument(document)"
                      class="text-yellow-600 hover:text-yellow-900"
                    >
                      <PencilIcon class="h-4 w-4" />
                    </button>
                    <button
                      @click="deleteDocument(document)"
                      class="text-red-600 hover:text-red-900"
                    >
                      <TrashIcon class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-between mt-6">
          <div class="text-sm text-gray-700">
            Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredDocuments.length) }} de {{ filteredDocuments.length }} documentos
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <span class="px-3 py-1 text-sm">{{ currentPage }} de {{ totalPages }}</span>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <DocumentUploadModal
      v-if="showUploadModal"
      :categories="categories"
      @close="showUploadModal = false"
      @upload="handleDocumentUpload"
    />
    
    <CategoryModal
      v-if="showCategoryModal"
      @close="showCategoryModal = false"
      @save="handleCategoryCreate"
    />
    
    <DocumentViewModal
      v-if="showViewModal"
      :document="selectedDocument"
      @close="showViewModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  DocumentTextIcon,
  DocumentPlusIcon,
  FolderIcon,
  FolderPlusIcon,
  EyeIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  ArrowDownTrayIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import DocumentCard from '@/components/dashboard/DocumentCard.vue'
import DocumentUploadModal from '@/components/dashboard/DocumentUploadModal.vue'
import CategoryModal from '@/components/dashboard/CategoryModal.vue'
import DocumentViewModal from '@/components/dashboard/DocumentViewModal.vue'

// Reactive state
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedType = ref('')
const sortBy = ref('date')
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = ref(12)
const showUploadModal = ref(false)
const showCategoryModal = ref(false)
const showViewModal = ref(false)
const selectedDocument = ref(null)

const stats = ref({
  totalDocuments: 156,
  categories: 12,
  monthlyViews: 2847,
  searches: 1293
})

const categories = ref([
  { id: 1, name: 'Políticas', color: 'blue' },
  { id: 2, name: 'Procedimientos', color: 'green' },
  { id: 3, name: 'Manuales', color: 'yellow' },
  { id: 4, name: 'FAQ', color: 'purple' },
  { id: 5, name: 'Capacitación', color: 'red' },
  { id: 6, name: 'Legal', color: 'gray' }
])

const documents = ref([
  {
    id: 1,
    name: 'Manual de Usuario v2.1',
    description: 'Guía completa para usuarios finales',
    type: 'pdf',
    categoryId: 3,
    size: 2048000,
    views: 245,
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-20'),
    url: '/documents/manual-usuario.pdf'
  },
  {
    id: 2,
    name: 'Política de Privacidad',
    description: 'Términos y condiciones de privacidad',
    type: 'doc',
    categoryId: 1,
    size: 512000,
    views: 189,
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-18'),
    url: '/documents/politica-privacidad.docx'
  },
  {
    id: 3,
    name: 'Preguntas Frecuentes',
    description: 'Respuestas a las consultas más comunes',
    type: 'md',
    categoryId: 4,
    size: 128000,
    views: 567,
    createdAt: new Date('2024-01-05'),
    updatedAt: new Date('2024-01-22'),
    url: '/documents/faq.md'
  }
])

// Computed properties
const filteredDocuments = computed(() => {
  let filtered = documents.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(doc => 
      doc.name.toLowerCase().includes(query) ||
      doc.description.toLowerCase().includes(query)
    )
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(doc => doc.categoryId === parseInt(selectedCategory.value))
  }
  
  if (selectedType.value) {
    filtered = filtered.filter(doc => doc.type === selectedType.value)
  }
  
  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'date':
        return new Date(b.updatedAt) - new Date(a.updatedAt)
      case 'views':
        return b.views - a.views
      case 'size':
        return b.size - a.size
      default:
        return 0
    }
  })
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredDocuments.value.length / itemsPerPage.value)
})

const paginatedDocuments = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredDocuments.value.slice(start, end)
})

// Methods
const getCategoryName = (categoryId) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : 'Sin categoría'
}

const getTypeIcon = (type) => {
  const icons = {
    pdf: DocumentTextIcon,
    doc: DocumentTextIcon,
    txt: DocumentTextIcon,
    md: DocumentTextIcon,
    url: DocumentTextIcon
  }
  return icons[type] || DocumentTextIcon
}

const getTypeColor = (type) => {
  const colors = {
    pdf: 'bg-red-100 text-red-600',
    doc: 'bg-blue-100 text-blue-600',
    txt: 'bg-gray-100 text-gray-600',
    md: 'bg-green-100 text-green-600',
    url: 'bg-purple-100 text-purple-600'
  }
  return colors[type] || 'bg-gray-100 text-gray-600'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const viewDocument = (document) => {
  selectedDocument.value = document
  showViewModal.value = true
  // Increment view count
  document.views++
}

const editDocument = (document) => {
  // TODO: Implement edit functionality
  console.log('Edit document:', document)
}

const deleteDocument = (document) => {
  if (confirm(`¿Estás seguro de que quieres eliminar "${document.name}"?`)) {
    const index = documents.value.findIndex(d => d.id === document.id)
    if (index > -1) {
      documents.value.splice(index, 1)
      stats.value.totalDocuments--
    }
  }
}

const downloadDocument = (document) => {
  // TODO: Implement download functionality
  console.log('Download document:', document)
  // Simulate download
  const link = document.createElement('a')
  link.href = document.url
  link.download = document.name
  link.click()
}

const handleDocumentUpload = (documentData) => {
  const newDocument = {
    id: documents.value.length + 1,
    ...documentData,
    views: 0,
    createdAt: new Date(),
    updatedAt: new Date()
  }
  
  documents.value.unshift(newDocument)
  stats.value.totalDocuments++
  showUploadModal.value = false
}

const handleCategoryCreate = (categoryData) => {
  const newCategory = {
    id: categories.value.length + 1,
    ...categoryData
  }
  
  categories.value.push(newCategory)
  stats.value.categories++
  showCategoryModal.value = false
}

// Watch for filter changes to reset pagination
const resetPagination = () => {
  currentPage.value = 1
}

// Initialize
onMounted(() => {
  // Load initial data
})
</script>