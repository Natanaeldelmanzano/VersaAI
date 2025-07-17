<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-medium text-gray-900">Importar Configuración</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Import Methods -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              v-for="method in importMethods"
              :key="method.id"
              @click="activeMethod = method.id"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeMethod === method.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              <component :is="method.icon" class="h-4 w-4 mr-2 inline" />
              {{ method.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- File Upload -->
      <div v-if="activeMethod === 'file'" class="space-y-4">
        <div
          @drop="handleFileDrop"
          @dragover.prevent
          @dragenter.prevent
          :class="[
            'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
            dragOver ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
          ]"
        >
          <ArrowUpTrayIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p class="text-lg font-medium text-gray-900 mb-2">Arrastra tu archivo aquí</p>
          <p class="text-sm text-gray-600 mb-4">o haz clic para seleccionar</p>
          <input
            ref="fileInput"
            type="file"
            accept=".json"
            @change="handleFileSelect"
            class="hidden"
          />
          <button
            @click="$refs.fileInput.click()"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Seleccionar archivo
          </button>
        </div>
        
        <div v-if="selectedFile" class="bg-gray-50 rounded-lg p-4">
          <div class="flex items-center space-x-3">
            <DocumentIcon class="h-8 w-8 text-blue-600" />
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</p>
              <p class="text-xs text-gray-600">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <button
              @click="selectedFile = null"
              class="text-gray-400 hover:text-gray-600"
            >
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- URL Import -->
      <div v-if="activeMethod === 'url'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">URL del archivo de configuración</label>
          <input
            v-model="importUrl"
            type="url"
            placeholder="https://example.com/settings.json"
            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div class="flex">
            <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400 mr-2" />
            <div class="text-sm text-yellow-700">
              <p class="font-medium">Advertencia de seguridad</p>
              <p>Solo importa configuraciones de fuentes confiables. Los archivos maliciosos pueden comprometer tu sistema.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- JSON Text -->
      <div v-if="activeMethod === 'text'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Configuración JSON</label>
          <textarea
            v-model="jsonText"
            rows="12"
            placeholder="Pega aquí tu configuración en formato JSON..."
            class="w-full border border-gray-300 rounded-md px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        
        <div v-if="jsonError" class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <ExclamationCircleIcon class="h-5 w-5 text-red-400 mr-2" />
            <div class="text-sm text-red-700">
              <p class="font-medium">Error en JSON</p>
              <p>{{ jsonError }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div v-if="previewData" class="mt-6">
        <h4 class="text-sm font-medium text-gray-900 mb-3">Vista previa de la configuración</h4>
        <div class="bg-gray-50 rounded-lg p-4 max-h-64 overflow-y-auto">
          <pre class="text-xs text-gray-700 whitespace-pre-wrap">{{ JSON.stringify(previewData, null, 2) }}</pre>
        </div>
      </div>

      <!-- Import Options -->
      <div v-if="previewData" class="mt-6 space-y-4">
        <h4 class="text-sm font-medium text-gray-900">Opciones de importación</h4>
        
        <div class="space-y-3">
          <label class="flex items-center space-x-2">
            <input
              v-model="importOptions.mergeWithExisting"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Combinar con configuración existente</span>
          </label>
          
          <label class="flex items-center space-x-2">
            <input
              v-model="importOptions.createBackup"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Crear backup antes de importar</span>
          </label>
          
          <label class="flex items-center space-x-2">
            <input
              v-model="importOptions.validateSettings"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Validar configuración antes de aplicar</span>
          </label>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-end space-x-3 mt-8 pt-6 border-t border-gray-200">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          @click="validateAndPreview"
          :disabled="!canPreview"
          class="px-4 py-2 bg-gray-600 text-white rounded-md text-sm font-medium hover:bg-gray-700 disabled:opacity-50"
        >
          Vista previa
        </button>
        <button
          @click="importConfiguration"
          :disabled="!previewData || importing"
          class="px-6 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {{ importing ? 'Importando...' : 'Importar' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {
  XMarkIcon,
  ArrowUpTrayIcon,
  DocumentIcon,
  LinkIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/24/outline'

// Emits
const emit = defineEmits(['close', 'import'])

// Reactive state
const activeMethod = ref('file')
const dragOver = ref(false)
const selectedFile = ref(null)
const importUrl = ref('')
const jsonText = ref('')
const jsonError = ref('')
const previewData = ref(null)
const importing = ref(false)

const importMethods = [
  { id: 'file', name: 'Archivo', icon: DocumentIcon },
  { id: 'url', name: 'URL', icon: LinkIcon },
  { id: 'text', name: 'Texto JSON', icon: DocumentTextIcon }
]

const importOptions = ref({
  mergeWithExisting: false,
  createBackup: true,
  validateSettings: true
})

// Computed
const canPreview = computed(() => {
  switch (activeMethod.value) {
    case 'file':
      return selectedFile.value !== null
    case 'url':
      return importUrl.value.trim() !== ''
    case 'text':
      return jsonText.value.trim() !== ''
    default:
      return false
  }
})

// Watchers
watch(jsonText, (newValue) => {
  jsonError.value = ''
  if (newValue.trim()) {
    try {
      JSON.parse(newValue)
    } catch (error) {
      jsonError.value = error.message
    }
  }
})

watch(activeMethod, () => {
  previewData.value = null
  jsonError.value = ''
})

// Methods
const handleFileDrop = (event) => {
  event.preventDefault()
  dragOver.value = false
  
  const files = event.dataTransfer.files
  if (files.length > 0) {
    const file = files[0]
    if (file.type === 'application/json' || file.name.endsWith('.json')) {
      selectedFile.value = file
    } else {
      alert('Por favor selecciona un archivo JSON válido')
    }
  }
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const validateAndPreview = async () => {
  try {
    let configData = null
    
    switch (activeMethod.value) {
      case 'file':
        if (selectedFile.value) {
          const text = await readFileAsText(selectedFile.value)
          configData = JSON.parse(text)
        }
        break
        
      case 'url':
        if (importUrl.value.trim()) {
          const response = await fetch(importUrl.value)
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`)
          }
          configData = await response.json()
        }
        break
        
      case 'text':
        if (jsonText.value.trim()) {
          configData = JSON.parse(jsonText.value)
        }
        break
    }
    
    if (configData) {
      // Validate configuration structure
      if (importOptions.value.validateSettings) {
        validateConfigurationStructure(configData)
      }
      
      previewData.value = configData
    }
  } catch (error) {
    console.error('Error validating configuration:', error)
    alert(`Error al validar la configuración: ${error.message}`)
  }
}

const validateConfigurationStructure = (config) => {
  const requiredSections = ['api', 'database', 'security', 'performance', 'system']
  const missingSections = requiredSections.filter(section => !config[section])
  
  if (missingSections.length > 0) {
    throw new Error(`Faltan las siguientes secciones: ${missingSections.join(', ')}`)
  }
  
  // Additional validation can be added here
}

const readFileAsText = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = (e) => reject(e)
    reader.readAsText(file)
  })
}

const importConfiguration = async () => {
  if (!previewData.value) return
  
  importing.value = true
  
  try {
    // Create backup if requested
    if (importOptions.value.createBackup) {
      // TODO: Create backup
      console.log('Creating backup before import...')
    }
    
    // Emit import event with configuration and options
    emit('import', {
      configuration: previewData.value,
      options: importOptions.value
    })
    
    emit('close')
  } catch (error) {
    console.error('Error importing configuration:', error)
    alert(`Error al importar la configuración: ${error.message}`)
  } finally {
    importing.value = false
  }
}
</script>