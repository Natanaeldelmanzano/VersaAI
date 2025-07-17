<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Subir Documento</h3>
          <p class="text-sm text-gray-600 mt-1">Añade un nuevo documento a la base de conocimientos</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Upload Form -->
      <form @submit.prevent="handleUpload" class="mt-6 space-y-6">
        <!-- Upload Method Tabs -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              type="button"
              @click="uploadMethod = 'file'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                uploadMethod === 'file'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Subir Archivo
            </button>
            <button
              type="button"
              @click="uploadMethod = 'url'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                uploadMethod === 'url'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Enlace Web
            </button>
            <button
              type="button"
              @click="uploadMethod = 'text'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                uploadMethod === 'text'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Texto Directo
            </button>
          </nav>
        </div>

        <!-- File Upload -->
        <div v-if="uploadMethod === 'file'" class="space-y-4">
          <div
            @drop="handleDrop"
            @dragover.prevent
            @dragenter.prevent
            :class="[
              'border-2 border-dashed rounded-lg p-6 text-center transition-colors',
              isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            ]"
          >
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.txt,.md"
              @change="handleFileSelect"
              class="hidden"
            />
            
            <div v-if="selectedFiles.length === 0">
              <DocumentPlusIcon class="mx-auto h-12 w-12 text-gray-400" />
              <div class="mt-4">
                <button
                  type="button"
                  @click="$refs.fileInput.click()"
                  class="text-blue-600 hover:text-blue-500 font-medium"
                >
                  Seleccionar archivos
                </button>
                <span class="text-gray-600"> o arrastra y suelta aquí</span>
              </div>
              <p class="text-xs text-gray-500 mt-2">
                PDF, DOC, DOCX, TXT, MD hasta 10MB cada uno
              </p>
            </div>
            
            <!-- Selected Files -->
            <div v-else class="space-y-2">
              <div
                v-for="(file, index) in selectedFiles"
                :key="index"
                class="flex items-center justify-between p-3 bg-gray-50 rounded border"
              >
                <div class="flex items-center space-x-3">
                  <DocumentTextIcon class="h-8 w-8 text-gray-400" />
                  <div class="text-left">
                    <p class="text-sm font-medium text-gray-900">{{ file.name }}</p>
                    <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
                  </div>
                </div>
                <button
                  type="button"
                  @click="removeFile(index)"
                  class="text-red-500 hover:text-red-700"
                >
                  <XMarkIcon class="h-5 w-5" />
                </button>
              </div>
              
              <button
                type="button"
                @click="$refs.fileInput.click()"
                class="text-blue-600 hover:text-blue-500 text-sm font-medium"
              >
                + Añadir más archivos
              </button>
            </div>
          </div>
        </div>

        <!-- URL Input -->
        <div v-if="uploadMethod === 'url'" class="space-y-4">
          <div>
            <label for="url" class="block text-sm font-medium text-gray-700 mb-2">
              URL del Documento
            </label>
            <input
              id="url"
              v-model="form.url"
              type="url"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="https://ejemplo.com/documento.pdf"
            />
          </div>
          
          <div class="flex items-center space-x-2">
            <input
              id="autoExtract"
              v-model="form.autoExtract"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="autoExtract" class="text-sm text-gray-700">
              Extraer automáticamente título y descripción
            </label>
          </div>
        </div>

        <!-- Text Input -->
        <div v-if="uploadMethod === 'text'" class="space-y-4">
          <div>
            <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
              Contenido del Documento
            </label>
            <textarea
              id="content"
              v-model="form.content"
              rows="8"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Escribe o pega el contenido del documento aquí..."
            ></textarea>
          </div>
        </div>

        <!-- Document Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Nombre del Documento *
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Nombre descriptivo"
            />
          </div>
          
          <div>
            <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
              Categoría *
            </label>
            <select
              id="category"
              v-model="form.categoryId"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Seleccionar categoría</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            Descripción
          </label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Descripción breve del documento..."
          ></textarea>
        </div>

        <!-- Tags -->
        <div>
          <label for="tags" class="block text-sm font-medium text-gray-700 mb-2">
            Etiquetas
          </label>
          <div class="flex flex-wrap gap-2 mb-2">
            <span
              v-for="(tag, index) in form.tags"
              :key="index"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
            >
              {{ tag }}
              <button
                type="button"
                @click="removeTag(index)"
                class="ml-1 text-blue-600 hover:text-blue-800"
              >
                <XMarkIcon class="h-3 w-3" />
              </button>
            </span>
          </div>
          <div class="flex">
            <input
              v-model="newTag"
              @keydown.enter.prevent="addTag"
              @keydown.comma.prevent="addTag"
              type="text"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Añadir etiqueta..."
            />
            <button
              type="button"
              @click="addTag"
              class="px-3 py-2 bg-gray-100 border border-l-0 border-gray-300 rounded-r-md hover:bg-gray-200"
            >
              <PlusIcon class="h-4 w-4" />
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            Presiona Enter o coma para añadir etiquetas
          </p>
        </div>

        <!-- Access Control -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Control de Acceso</h4>
          
          <div class="space-y-3">
            <label class="flex items-center">
              <input
                v-model="form.visibility"
                value="public"
                type="radio"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span class="ml-3 text-sm text-gray-700">
                <span class="font-medium">Público</span> - Visible para todos los miembros
              </span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="form.visibility"
                value="restricted"
                type="radio"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span class="ml-3 text-sm text-gray-700">
                <span class="font-medium">Restringido</span> - Solo roles específicos
              </span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="form.visibility"
                value="private"
                type="radio"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span class="ml-3 text-sm text-gray-700">
                <span class="font-medium">Privado</span> - Solo el autor
              </span>
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="!isFormValid || isUploading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="isUploading">Subiendo...</span>
            <span v-else>Subir Documento</span>
            <CloudArrowUpIcon v-if="!isUploading" class="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  XMarkIcon,
  DocumentPlusIcon,
  DocumentTextIcon,
  PlusIcon,
  CloudArrowUpIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  categories: {
    type: Array,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'upload'])

// Reactive state
const uploadMethod = ref('file')
const isDragging = ref(false)
const isUploading = ref(false)
const selectedFiles = ref([])
const newTag = ref('')
const fileInput = ref(null)

const form = ref({
  name: '',
  description: '',
  categoryId: '',
  tags: [],
  visibility: 'public',
  url: '',
  content: '',
  autoExtract: true
})

// Computed properties
const isFormValid = computed(() => {
  const hasContent = uploadMethod.value === 'file' ? selectedFiles.value.length > 0 :
                    uploadMethod.value === 'url' ? form.value.url :
                    form.value.content
  
  return form.value.name && form.value.categoryId && hasContent
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  
  const files = Array.from(event.dataTransfer.files)
  addFiles(files)
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
}

const addFiles = (files) => {
  const validFiles = files.filter(file => {
    // Check file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      alert(`El archivo "${file.name}" es demasiado grande. Máximo 10MB.`)
      return false
    }
    
    // Check file type
    const allowedTypes = ['.pdf', '.doc', '.docx', '.txt', '.md']
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    if (!allowedTypes.includes(fileExtension)) {
      alert(`El archivo "${file.name}" no es un tipo válido.`)
      return false
    }
    
    return true
  })
  
  selectedFiles.value.push(...validFiles)
  
  // Auto-fill name if only one file
  if (selectedFiles.value.length === 1 && !form.value.name) {
    form.value.name = selectedFiles.value[0].name.replace(/\.[^/.]+$/, '')
  }
}

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const addTag = () => {
  const tag = newTag.value.trim().replace(',', '')
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (index) => {
  form.value.tags.splice(index, 1)
}

const handleUpload = async () => {
  if (!isFormValid.value) return
  
  isUploading.value = true
  
  try {
    // Simulate upload process
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const documentData = {
      ...form.value,
      type: uploadMethod.value === 'file' ? getFileType(selectedFiles.value[0]) :
            uploadMethod.value === 'url' ? 'url' : 'txt',
      size: uploadMethod.value === 'file' ? selectedFiles.value.reduce((total, file) => total + file.size, 0) :
            uploadMethod.value === 'text' ? new Blob([form.value.content]).size : 0,
      files: uploadMethod.value === 'file' ? selectedFiles.value : null
    }
    
    emit('upload', documentData)
  } catch (error) {
    console.error('Error uploading document:', error)
    alert('Error al subir el documento. Inténtalo de nuevo.')
  } finally {
    isUploading.value = false
  }
}

const getFileType = (file) => {
  const extension = file.name.split('.').pop().toLowerCase()
  const typeMap = {
    'pdf': 'pdf',
    'doc': 'doc',
    'docx': 'doc',
    'txt': 'txt',
    'md': 'md'
  }
  return typeMap[extension] || 'txt'
}

// Drag and drop events
const handleDragEnter = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

// Initialize
onMounted(() => {
  // Set default category if only one exists
  if (props.categories.length === 1) {
    form.value.categoryId = props.categories[0].id
  }
})
</script>