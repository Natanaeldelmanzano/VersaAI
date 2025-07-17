<template>
  <div class="bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow duration-200">
    <!-- Document Preview -->
    <div class="relative">
      <div :class="[
        'h-32 rounded-t-lg flex items-center justify-center',
        getTypeColor(document.type)
      ]">
        <component :is="getTypeIcon(document.type)" class="h-12 w-12" />
      </div>
      
      <!-- Category Badge -->
      <div class="absolute top-2 left-2">
        <span :class="[
          'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
          getCategoryColor(document.categoryId)
        ]">
          {{ getCategoryName(document.categoryId) }}
        </span>
      </div>
      
      <!-- Actions Dropdown -->
      <div class="absolute top-2 right-2">
        <div class="relative">
          <button
            @click="showDropdown = !showDropdown"
            class="p-1 bg-white rounded-full shadow-sm hover:bg-gray-50 transition-colors"
          >
            <EllipsisVerticalIcon class="h-5 w-5 text-gray-600" />
          </button>
          
          <div
            v-if="showDropdown"
            v-click-outside="() => showDropdown = false"
            class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
          >
            <div class="py-1">
              <button
                @click="handleView"
                class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <EyeIcon class="h-4 w-4 mr-3" />
                Ver documento
              </button>
              <button
                @click="handleDownload"
                class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <ArrowDownTrayIcon class="h-4 w-4 mr-3" />
                Descargar
              </button>
              <button
                @click="handleEdit"
                class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <PencilIcon class="h-4 w-4 mr-3" />
                Editar
              </button>
              <button
                @click="handleShare"
                class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                <ShareIcon class="h-4 w-4 mr-3" />
                Compartir
              </button>
              <hr class="my-1" />
              <button
                @click="handleDelete"
                class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                <TrashIcon class="h-4 w-4 mr-3" />
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Document Info -->
    <div class="p-4">
      <div class="mb-2">
        <h3 class="text-sm font-semibold text-gray-900 truncate" :title="document.name">
          {{ document.name }}
        </h3>
        <p class="text-xs text-gray-600 mt-1 line-clamp-2" :title="document.description">
          {{ document.description }}
        </p>
      </div>
      
      <!-- Document Stats -->
      <div class="flex items-center justify-between text-xs text-gray-500">
        <div class="flex items-center space-x-3">
          <span class="flex items-center">
            <EyeIcon class="h-3 w-3 mr-1" />
            {{ document.views }}
          </span>
          <span>{{ formatFileSize(document.size) }}</span>
        </div>
        <span>{{ formatDate(document.updatedAt) }}</span>
      </div>
      
      <!-- Document Type -->
      <div class="mt-3 flex items-center justify-between">
        <span :class="[
          'inline-flex items-center px-2 py-1 rounded text-xs font-medium',
          getTypeColor(document.type, true)
        ]">
          {{ document.type.toUpperCase() }}
        </span>
        
        <!-- Quick Actions -->
        <div class="flex items-center space-x-1">
          <button
            @click="handleView"
            class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
            title="Ver documento"
          >
            <EyeIcon class="h-4 w-4" />
          </button>
          <button
            @click="handleDownload"
            class="p-1 text-gray-400 hover:text-green-600 transition-colors"
            title="Descargar"
          >
            <ArrowDownTrayIcon class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Progress Bar (for uploads) -->
    <div v-if="document.uploading" class="px-4 pb-4">
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-600 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${document.uploadProgress || 0}%` }"
        ></div>
      </div>
      <p class="text-xs text-gray-600 mt-1">
        Subiendo... {{ document.uploadProgress || 0 }}%
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  DocumentTextIcon,
  EyeIcon,
  ArrowDownTrayIcon,
  PencilIcon,
  TrashIcon,
  ShareIcon,
  EllipsisVerticalIcon
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
const emit = defineEmits(['view', 'edit', 'delete', 'download', 'share'])

// Reactive state
const showDropdown = ref(false)

// Methods
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

const getTypeColor = (type, isText = false) => {
  if (isText) {
    const textColors = {
      pdf: 'bg-red-100 text-red-800',
      doc: 'bg-blue-100 text-blue-800',
      txt: 'bg-gray-100 text-gray-800',
      md: 'bg-green-100 text-green-800',
      url: 'bg-purple-100 text-purple-800'
    }
    return textColors[type] || 'bg-gray-100 text-gray-800'
  }
  
  const bgColors = {
    pdf: 'bg-red-50 text-red-600',
    doc: 'bg-blue-50 text-blue-600',
    txt: 'bg-gray-50 text-gray-600',
    md: 'bg-green-50 text-green-600',
    url: 'bg-purple-50 text-purple-600'
  }
  return bgColors[type] || 'bg-gray-50 text-gray-600'
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const formatDate = (date) => {
  const now = new Date()
  const docDate = new Date(date)
  const diffTime = Math.abs(now - docDate)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) {
    return 'Ayer'
  } else if (diffDays < 7) {
    return `Hace ${diffDays} días`
  } else {
    return new Intl.DateTimeFormat('es-ES', {
      month: 'short',
      day: 'numeric'
    }).format(docDate)
  }
}

// Event handlers
const handleView = () => {
  showDropdown.value = false
  emit('view', props.document)
}

const handleEdit = () => {
  showDropdown.value = false
  emit('edit', props.document)
}

const handleDelete = () => {
  showDropdown.value = false
  emit('delete', props.document)
}

const handleDownload = () => {
  showDropdown.value = false
  emit('download', props.document)
}

const handleShare = () => {
  showDropdown.value = false
  emit('share', props.document)
}

// Click outside directive
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>