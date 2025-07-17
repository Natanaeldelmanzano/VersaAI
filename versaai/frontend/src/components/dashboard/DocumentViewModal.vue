<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-4 mx-auto p-5 border w-11/12 max-w-6xl shadow-lg rounded-md bg-white min-h-[90vh]">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div class="flex items-center space-x-4">
          <div :class="[
            'w-12 h-12 rounded-lg flex items-center justify-center',
            getTypeColor(document.type)
          ]">
            <component :is="getTypeIcon(document.type)" class="h-6 w-6" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ document.name }}</h3>
            <div class="flex items-center space-x-3 mt-1">
              <span :class="[
                'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                getCategoryColor(document.categoryId)
              ]">
                {{ getCategoryName(document.categoryId) }}
              </span>
              <span class="text-sm text-gray-500">{{ formatFileSize(document.size) }}</span>
              <span class="text-sm text-gray-500">{{ document.views }} vistas</span>
            </div>
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Actions -->
          <button
            @click="downloadDocument"
            class="p-2 text-gray-400 hover:text-green-600 transition-colors"
            title="Descargar"
          >
            <ArrowDownTrayIcon class="h-5 w-5" />
          </button>
          <button
            @click="shareDocument"
            class="p-2 text-gray-400 hover:text-blue-600 transition-colors"
            title="Compartir"
          >
            <ShareIcon class="h-5 w-5" />
          </button>
          <button
            @click="printDocument"
            class="p-2 text-gray-400 hover:text-purple-600 transition-colors"
            title="Imprimir"
          >
            <PrinterIcon class="h-5 w-5" />
          </button>
          <button
            @click="$emit('close')"
            class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            title="Cerrar"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Content Area -->
      <div class="flex h-[calc(90vh-120px)] mt-4">
        <!-- Document Viewer -->
        <div class="flex-1 bg-gray-50 rounded-lg overflow-hidden">
          <!-- PDF Viewer -->
          <div v-if="document.type === 'pdf'" class="h-full flex flex-col">
            <div class="bg-white border-b border-gray-200 p-3 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <button
                  @click="zoomOut"
                  :disabled="zoomLevel <= 0.5"
                  class="p-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50"
                >
                  <MinusIcon class="h-4 w-4" />
                </button>
                <span class="text-sm text-gray-600">{{ Math.round(zoomLevel * 100) }}%</span>
                <button
                  @click="zoomIn"
                  :disabled="zoomLevel >= 2"
                  class="p-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50"
                >
                  <PlusIcon class="h-4 w-4" />
                </button>
              </div>
              
              <div class="flex items-center space-x-3">
                <button
                  @click="previousPage"
                  :disabled="currentPage <= 1"
                  class="p-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50"
                >
                  <ChevronLeftIcon class="h-4 w-4" />
                </button>
                <span class="text-sm text-gray-600">
                  {{ currentPage }} / {{ totalPages }}
                </span>
                <button
                  @click="nextPage"
                  :disabled="currentPage >= totalPages"
                  class="p-1 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50"
                >
                  <ChevronRightIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
            
            <div class="flex-1 overflow-auto p-4 flex justify-center">
              <div class="bg-white shadow-lg" :style="{ transform: `scale(${zoomLevel})` }">
                <!-- PDF content would be rendered here -->
                <div class="w-[595px] h-[842px] bg-white border border-gray-200 p-8">
                  <div class="text-center text-gray-500">
                    <DocumentTextIcon class="h-16 w-16 mx-auto mb-4" />
                    <p>Vista previa del PDF</p>
                    <p class="text-sm mt-2">{{ document.name }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Text/Markdown Viewer -->
          <div v-else-if="['txt', 'md'].includes(document.type)" class="h-full overflow-auto">
            <div class="p-6">
              <div v-if="document.type === 'md'" class="prose max-w-none">
                <!-- Markdown content would be rendered here -->
                <div v-html="renderedMarkdown"></div>
              </div>
              <div v-else class="whitespace-pre-wrap font-mono text-sm">
                {{ documentContent }}
              </div>
            </div>
          </div>
          
          <!-- URL Preview -->
          <div v-else-if="document.type === 'url'" class="h-full">
            <iframe
              :src="document.url"
              class="w-full h-full border-0"
              sandbox="allow-scripts allow-same-origin"
            ></iframe>
          </div>
          
          <!-- Other Document Types -->
          <div v-else class="h-full flex items-center justify-center">
            <div class="text-center text-gray-500">
              <component :is="getTypeIcon(document.type)" class="h-16 w-16 mx-auto mb-4" />
              <p class="text-lg font-medium">{{ document.name }}</p>
              <p class="text-sm mt-2">{{ document.description }}</p>
              <button
                @click="downloadDocument"
                class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2 mx-auto"
              >
                <ArrowDownTrayIcon class="h-4 w-4" />
                <span>Descargar para ver</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="w-80 ml-4 space-y-4">
          <!-- Document Info -->
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h4 class="text-sm font-medium text-gray-900 mb-3">Información del Documento</h4>
            <div class="space-y-3 text-sm">
              <div>
                <span class="text-gray-600">Descripción:</span>
                <p class="text-gray-900 mt-1">{{ document.description || 'Sin descripción' }}</p>
              </div>
              <div>
                <span class="text-gray-600">Tipo:</span>
                <span class="ml-2 text-gray-900">{{ document.type.toUpperCase() }}</span>
              </div>
              <div>
                <span class="text-gray-600">Tamaño:</span>
                <span class="ml-2 text-gray-900">{{ formatFileSize(document.size) }}</span>
              </div>
              <div>
                <span class="text-gray-600">Creado:</span>
                <span class="ml-2 text-gray-900">{{ formatDate(document.createdAt) }}</span>
              </div>
              <div>
                <span class="text-gray-600">Actualizado:</span>
                <span class="ml-2 text-gray-900">{{ formatDate(document.updatedAt) }}</span>
              </div>
              <div>
                <span class="text-gray-600">Vistas:</span>
                <span class="ml-2 text-gray-900">{{ document.views }}</span>
              </div>
            </div>
          </div>
          
          <!-- Tags -->
          <div v-if="document.tags && document.tags.length" class="bg-white rounded-lg border border-gray-200 p-4">
            <h4 class="text-sm font-medium text-gray-900 mb-3">Etiquetas</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in document.tags"
                :key="tag"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                {{ tag }}
              </span>
            </div>
          </div>
          
          <!-- Recent Activity -->
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h4 class="text-sm font-medium text-gray-900 mb-3">Actividad Reciente</h4>
            <div class="space-y-3">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center',
                    activity.type === 'view' ? 'bg-blue-100 text-blue-600' :
                    activity.type === 'download' ? 'bg-green-100 text-green-600' :
                    'bg-gray-100 text-gray-600'
                  ]">
                    <component :is="getActivityIcon(activity.type)" class="h-4 w-4" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs text-gray-900">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500">{{ formatDate(activity.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Share Options -->
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h4 class="text-sm font-medium text-gray-900 mb-3">Compartir</h4>
            <div class="space-y-2">
              <button
                @click="copyLink"
                class="w-full flex items-center justify-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                <LinkIcon class="h-4 w-4 mr-2" />
                Copiar enlace
              </button>
              <button
                @click="shareByEmail"
                class="w-full flex items-center justify-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                <EnvelopeIcon class="h-4 w-4 mr-2" />
                Enviar por email
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ShareIcon,
  PrinterIcon,
  MinusIcon,
  PlusIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  EyeIcon,
  LinkIcon,
  EnvelopeIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  document: {
    type: Object,
    required: true
  },
  categories: {
    type: Array,
    default: () => [
      { id: 1, name: 'Políticas', color: 'blue' },
      { id: 2, name: 'Procedimientos', color: 'green' },
      { id: 3, name: 'Manuales', color: 'yellow' },
      { id: 4, name: 'FAQ', color: 'purple' },
      { id: 5, name: 'Capacitación', color: 'red' },
      { id: 6, name: 'Legal', color: 'gray' }
    ]
  }
})

// Emits
const emit = defineEmits(['close'])

// Reactive state
const zoomLevel = ref(1)
const currentPage = ref(1)
const totalPages = ref(1)
const documentContent = ref('')
const renderedMarkdown = ref('')

const recentActivity = ref([
  {
    id: 1,
    type: 'view',
    description: 'Juan Pérez vio el documento',
    timestamp: new Date(Date.now() - 1000 * 60 * 30)
  },
  {
    id: 2,
    type: 'download',
    description: 'María García descargó el documento',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2)
  },
  {
    id: 3,
    type: 'view',
    description: 'Carlos López vio el documento',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4)
  }
])

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const getCategoryName = (categoryId) => {
  const category = props.categories.find(c => c.id === categoryId)
  return category ? category.name : 'Sin categoría'
}

const getCategoryColor = (categoryId) => {
  const category = props.categories.find(c => c.id === categoryId)
  if (!category) return 'bg-gray-100 text-gray-800'
  
  const colors = {
    blue: 'bg-blue-100 text-blue-800',
    green: 'bg-green-100 text-green-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    purple: 'bg-purple-100 text-purple-800',
    red: 'bg-red-100 text-red-800',
    gray: 'bg-gray-100 text-gray-800'
  }
  
  return colors[category.color] || 'bg-gray-100 text-gray-800'
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
    pdf: 'bg-red-50 text-red-600',
    doc: 'bg-blue-50 text-blue-600',
    txt: 'bg-gray-50 text-gray-600',
    md: 'bg-green-50 text-green-600',
    url: 'bg-purple-50 text-purple-600'
  }
  return colors[type] || 'bg-gray-50 text-gray-600'
}

const getActivityIcon = (type) => {
  const icons = {
    view: EyeIcon,
    download: ArrowDownTrayIcon,
    share: ShareIcon
  }
  return icons[type] || EyeIcon
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
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// PDF Controls
const zoomIn = () => {
  if (zoomLevel.value < 2) {
    zoomLevel.value += 0.25
  }
}

const zoomOut = () => {
  if (zoomLevel.value > 0.5) {
    zoomLevel.value -= 0.25
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// Actions
const downloadDocument = () => {
  // TODO: Implement download functionality
  console.log('Download document:', props.document)
  const link = document.createElement('a')
  link.href = props.document.url || '#'
  link.download = props.document.name
  link.click()
}

const shareDocument = () => {
  // TODO: Implement share functionality
  console.log('Share document:', props.document)
}

const printDocument = () => {
  window.print()
}

const copyLink = async () => {
  try {
    const url = `${window.location.origin}/documents/${props.document.id}`
    await navigator.clipboard.writeText(url)
    alert('Enlace copiado al portapapeles')
  } catch (error) {
    console.error('Error copying link:', error)
  }
}

const shareByEmail = () => {
  const subject = encodeURIComponent(`Documento: ${props.document.name}`)
  const body = encodeURIComponent(`Te comparto este documento: ${props.document.name}\n\n${props.document.description || ''}\n\nVer documento: ${window.location.origin}/documents/${props.document.id}`)
  window.open(`mailto:?subject=${subject}&body=${body}`)
}

// Initialize
onMounted(() => {
  // Load document content based on type
  if (['txt', 'md'].includes(props.document.type)) {
    // TODO: Load actual content from API
    documentContent.value = 'Contenido del documento...\n\nEste es un ejemplo de contenido de texto.'
    
    if (props.document.type === 'md') {
      // TODO: Render markdown
      renderedMarkdown.value = '<h1>Documento Markdown</h1><p>Este es un ejemplo de contenido markdown renderizado.</p>'
    }
  }
  
  if (props.document.type === 'pdf') {
    totalPages.value = 5 // TODO: Get actual page count
  }
})
</script>