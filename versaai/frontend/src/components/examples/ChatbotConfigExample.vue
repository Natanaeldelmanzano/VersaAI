<template>
  <div class="max-w-6xl mx-auto p-6 space-y-8">
    <!-- Header -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Configuración de Chatbot
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        Ejemplo de validaciones complejas y configuraciones avanzadas
      </p>
    </div>

    <!-- Configuración Básica -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Configuración Básica del Chatbot
      </h2>
      
      <form @submit.prevent="handleBasicConfigSave" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Nombre del chatbot -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre del Chatbot *
            </label>
            <input
              v-model="basicConfig.name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Mi Asistente IA"
              :disabled="isLoading"
              @blur="validateBasicField('name')"
            />
            <p v-if="basicErrors.name" class="mt-1 text-sm text-red-600">
              {{ basicErrors.name }}
            </p>
          </div>

          <!-- Modelo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Modelo de IA *
            </label>
            <select
              v-model="basicConfig.model"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              :disabled="isLoading"
            >
              <option value="">Selecciona un modelo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="claude-3-opus">Claude 3 Opus</option>
              <option value="claude-3-sonnet">Claude 3 Sonnet</option>
              <option value="gemini-pro">Gemini Pro</option>
            </select>
            <p v-if="basicErrors.model" class="mt-1 text-sm text-red-600">
              {{ basicErrors.model }}
            </p>
          </div>

          <!-- Temperatura -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Temperatura ({{ basicConfig.temperature }})
            </label>
            <input
              v-model.number="basicConfig.temperature"
              type="range"
              min="0"
              max="2"
              step="0.1"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              :disabled="isLoading"
            />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Conservador (0)</span>
              <span>Creativo (2)</span>
            </div>
          </div>

          <!-- Máximo de tokens -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Máximo de Tokens
            </label>
            <input
              v-model.number="basicConfig.max_tokens"
              type="number"
              min="1"
              max="4096"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="2048"
              :disabled="isLoading"
            />
            <p class="mt-1 text-xs text-gray-500">
              Límite de tokens por respuesta (1-4096)
            </p>
          </div>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Descripción
          </label>
          <textarea
            v-model="basicConfig.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
            placeholder="Describe el propósito y funcionalidades de tu chatbot..."
            :disabled="isLoading"
            maxlength="500"
          ></textarea>
          <p class="mt-1 text-sm text-gray-500">
            {{ basicConfig.description?.length || 0 }}/500 caracteres
          </p>
        </div>

        <!-- Prompt del sistema -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Prompt del Sistema *
          </label>
          <textarea
            v-model="basicConfig.system_prompt"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white font-mono text-sm"
            placeholder="Eres un asistente útil y amigable. Responde de manera clara y concisa..."
            :disabled="isLoading"
            @blur="validateBasicField('system_prompt')"
          ></textarea>
          <p v-if="basicErrors.system_prompt" class="mt-1 text-sm text-red-600">
            {{ basicErrors.system_prompt }}
          </p>
          <p class="mt-1 text-xs text-gray-500">
            Define el comportamiento y personalidad del chatbot
          </p>
        </div>

        <!-- Configuraciones adicionales -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="flex items-center">
            <input
              v-model="basicConfig.is_public"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              :disabled="isLoading"
            />
            <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Chatbot público
            </label>
          </div>

          <div class="flex items-center">
            <input
              v-model="basicConfig.enable_memory"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              :disabled="isLoading"
            />
            <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Habilitar memoria
            </label>
          </div>

          <div class="flex items-center">
            <input
              v-model="basicConfig.enable_web_search"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              :disabled="isLoading"
            />
            <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Búsqueda web
            </label>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="resetBasicConfig"
            :disabled="isLoading"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            Restablecer
          </button>
          <button
            type="submit"
            :disabled="isLoading || !isBasicConfigValid"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
            {{ isLoading ? 'Guardando...' : 'Guardar Configuración' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Configuración Avanzada -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Configuración Avanzada
      </h2>
      
      <form @submit.prevent="handleAdvancedConfigSave" class="space-y-6">
        <!-- Configuración de respuestas -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Top P ({{ advancedConfig.top_p }})
            </label>
            <input
              v-model.number="advancedConfig.top_p"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              :disabled="isLoading"
            />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Determinista (0)</span>
              <span>Diverso (1)</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Penalización de Frecuencia ({{ advancedConfig.frequency_penalty }})
            </label>
            <input
              v-model.number="advancedConfig.frequency_penalty"
              type="range"
              min="-2"
              max="2"
              step="0.1"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              :disabled="isLoading"
            />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Repetitivo (-2)</span>
              <span>Variado (2)</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Penalización de Presencia ({{ advancedConfig.presence_penalty }})
            </label>
            <input
              v-model.number="advancedConfig.presence_penalty"
              type="range"
              min="-2"
              max="2"
              step="0.1"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
              :disabled="isLoading"
            />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Enfocado (-2)</span>
              <span>Exploratorio (2)</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Timeout (segundos)
            </label>
            <input
              v-model.number="advancedConfig.timeout"
              type="number"
              min="5"
              max="300"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="30"
              :disabled="isLoading"
            />
          </div>
        </div>

        <!-- Palabras prohibidas -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Palabras Prohibidas
          </label>
          <div class="space-y-2">
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="(word, index) in advancedConfig.forbidden_words"
                :key="index"
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
              >
                {{ word }}
                <button
                  @click="removeForbiddenWord(index)"
                  type="button"
                  class="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full hover:bg-red-200 dark:hover:bg-red-800"
                >
                  ×
                </button>
              </span>
            </div>
            <div class="flex space-x-2">
              <input
                v-model="newForbiddenWord"
                type="text"
                class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="Agregar palabra prohibida"
                @keyup.enter="addForbiddenWord"
              />
              <button
                @click="addForbiddenWord"
                type="button"
                class="px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Agregar
              </button>
            </div>
          </div>
        </div>

        <!-- Configuración de contexto -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Ventana de Contexto
            </label>
            <select
              v-model="advancedConfig.context_window"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              :disabled="isLoading"
            >
              <option value="4096">4K tokens</option>
              <option value="8192">8K tokens</option>
              <option value="16384">16K tokens</option>
              <option value="32768">32K tokens</option>
              <option value="65536">64K tokens</option>
              <option value="131072">128K tokens</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Máximo de Conversaciones
            </label>
            <input
              v-model.number="advancedConfig.max_conversations"
              type="number"
              min="1"
              max="1000"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="100"
              :disabled="isLoading"
            />
          </div>
        </div>

        <!-- Configuraciones de seguridad -->
        <div class="space-y-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">
            Configuraciones de Seguridad
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-center">
              <input
                v-model="advancedConfig.enable_content_filter"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                :disabled="isLoading"
              />
              <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Filtro de contenido
              </label>
            </div>

            <div class="flex items-center">
              <input
                v-model="advancedConfig.enable_pii_detection"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                :disabled="isLoading"
              />
              <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Detección de PII
              </label>
            </div>

            <div class="flex items-center">
              <input
                v-model="advancedConfig.enable_rate_limiting"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                :disabled="isLoading"
              />
              <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Limitación de velocidad
              </label>
            </div>

            <div class="flex items-center">
              <input
                v-model="advancedConfig.enable_logging"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                :disabled="isLoading"
              />
              <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Registro de conversaciones
              </label>
            </div>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="resetAdvancedConfig"
            :disabled="isLoading"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            Restablecer
          </button>
          <button
            type="submit"
            :disabled="isLoading"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
            {{ isLoading ? 'Guardando...' : 'Guardar Configuración Avanzada' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Vista previa de configuración -->
    <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Vista Previa de Configuración
      </h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 class="font-medium text-gray-900 dark:text-white mb-3">Configuración Básica</h3>
          <pre class="text-xs bg-white dark:bg-gray-800 p-4 rounded-lg overflow-auto border">{{ JSON.stringify(basicConfig, null, 2) }}</pre>
        </div>
        
        <div>
          <h3 class="font-medium text-gray-900 dark:text-white mb-3">Configuración Avanzada</h3>
          <pre class="text-xs bg-white dark:bg-gray-800 p-4 rounded-lg overflow-auto border">{{ JSON.stringify(advancedConfig, null, 2) }}</pre>
        </div>
      </div>
      
      <!-- Validación en tiempo real -->
      <div class="mt-6">
        <h3 class="font-medium text-gray-900 dark:text-white mb-3">Estado de Validación</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center space-x-2">
            <div :class="[
              'w-3 h-3 rounded-full',
              isBasicConfigValid ? 'bg-green-500' : 'bg-red-500'
            ]"></div>
            <span class="text-sm text-gray-600 dark:text-gray-300">
              Configuración Básica: {{ isBasicConfigValid ? 'Válida' : 'Inválida' }}
            </span>
          </div>
          
          <div class="flex items-center space-x-2">
            <div :class="[
              'w-3 h-3 rounded-full',
              isAdvancedConfigValid ? 'bg-green-500' : 'bg-red-500'
            ]"></div>
            <span class="text-sm text-gray-600 dark:text-gray-300">
              Configuración Avanzada: {{ isAdvancedConfigValid ? 'Válida' : 'Inválida' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  chatbotConfigSchema, 
  validateData, 
  type ChatbotConfigData 
} from '@/utils/validation'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useToast } from 'vue-toastification'

// Composables
const toast = useToast()

// Estado reactivo
const isLoading = ref(false)
const newForbiddenWord = ref('')

// Configuración básica
const basicConfig = ref<Partial<ChatbotConfigData>>({
  name: 'Mi Asistente IA',
  model: 'gpt-4',
  temperature: 0.7,
  max_tokens: 2048,
  description: 'Un asistente inteligente para ayudar con diversas tareas.',
  system_prompt: 'Eres un asistente útil y amigable. Responde de manera clara y concisa, proporcionando información precisa y útil.',
  is_public: false,
  enable_memory: true,
  enable_web_search: false
})

const basicErrors = ref<Record<string, string>>({})

// Configuración avanzada
const advancedConfig = ref({
  top_p: 0.9,
  frequency_penalty: 0.0,
  presence_penalty: 0.0,
  timeout: 30,
  forbidden_words: ['spam', 'hack', 'virus'] as string[],
  context_window: 8192,
  max_conversations: 100,
  enable_content_filter: true,
  enable_pii_detection: true,
  enable_rate_limiting: true,
  enable_logging: true
})

// Computed properties
const isBasicConfigValid = computed(() => {
  const validation = validateData(chatbotConfigSchema, basicConfig.value)
  return validation.success && Object.keys(basicErrors.value).length === 0
})

const isAdvancedConfigValid = computed(() => {
  // Validaciones personalizadas para configuración avanzada
  return advancedConfig.value.top_p >= 0 && advancedConfig.value.top_p <= 1 &&
         advancedConfig.value.frequency_penalty >= -2 && advancedConfig.value.frequency_penalty <= 2 &&
         advancedConfig.value.presence_penalty >= -2 && advancedConfig.value.presence_penalty <= 2 &&
         advancedConfig.value.timeout >= 5 && advancedConfig.value.timeout <= 300 &&
         advancedConfig.value.max_conversations >= 1 && advancedConfig.value.max_conversations <= 1000
})

// Métodos de validación
const validateBasicField = (field: string): void => {
  const fieldValidations = {
    name: () => {
      if (!basicConfig.value.name || basicConfig.value.name.length < 2) {
        basicErrors.value.name = 'El nombre debe tener al menos 2 caracteres'
      } else if (basicConfig.value.name.length > 100) {
        basicErrors.value.name = 'El nombre no puede exceder 100 caracteres'
      } else {
        delete basicErrors.value.name
      }
    },
    model: () => {
      if (!basicConfig.value.model) {
        basicErrors.value.model = 'Debes seleccionar un modelo'
      } else {
        delete basicErrors.value.model
      }
    },
    system_prompt: () => {
      if (!basicConfig.value.system_prompt || basicConfig.value.system_prompt.length < 10) {
        basicErrors.value.system_prompt = 'El prompt del sistema debe tener al menos 10 caracteres'
      } else if (basicConfig.value.system_prompt.length > 2000) {
        basicErrors.value.system_prompt = 'El prompt del sistema no puede exceder 2000 caracteres'
      } else {
        delete basicErrors.value.system_prompt
      }
    }
  }
  
  if (fieldValidations[field as keyof typeof fieldValidations]) {
    fieldValidations[field as keyof typeof fieldValidations]()
  }
}

// Métodos para palabras prohibidas
const addForbiddenWord = (): void => {
  const word = newForbiddenWord.value.trim().toLowerCase()
  if (word && !advancedConfig.value.forbidden_words.includes(word)) {
    advancedConfig.value.forbidden_words.push(word)
    newForbiddenWord.value = ''
    toast.success(`Palabra "${word}" agregada a la lista prohibida`)
  } else if (word && advancedConfig.value.forbidden_words.includes(word)) {
    toast.warning('Esta palabra ya está en la lista')
  }
}

const removeForbiddenWord = (index: number): void => {
  const word = advancedConfig.value.forbidden_words[index]
  advancedConfig.value.forbidden_words.splice(index, 1)
  toast.info(`Palabra "${word}" eliminada de la lista prohibida`)
}

// Métodos de manejo de formularios
const handleBasicConfigSave = async (): Promise<void> => {
  basicErrors.value = {}
  isLoading.value = true
  
  try {
    // Validar configuración básica
    const validation = validateData(chatbotConfigSchema, basicConfig.value)
    if (!validation.success) {
      validation.errors.forEach(error => {
        const [field, message] = error.split(': ')
        if (field && message) {
          basicErrors.value[field] = message
        }
      })
      toast.error('Por favor corrige los errores en la configuración básica')
      return
    }
    
    // Simular guardado
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    toast.success('Configuración básica guardada exitosamente')
    console.log('Basic config saved:', basicConfig.value)
  } catch (error) {
    console.error('Error saving basic config:', error)
    toast.error('Error al guardar la configuración básica')
  } finally {
    isLoading.value = false
  }
}

const handleAdvancedConfigSave = async (): Promise<void> => {
  isLoading.value = true
  
  try {
    // Validaciones personalizadas
    if (!isAdvancedConfigValid.value) {
      toast.error('Por favor verifica los valores de la configuración avanzada')
      return
    }
    
    // Simular guardado
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    toast.success('Configuración avanzada guardada exitosamente')
    console.log('Advanced config saved:', advancedConfig.value)
  } catch (error) {
    console.error('Error saving advanced config:', error)
    toast.error('Error al guardar la configuración avanzada')
  } finally {
    isLoading.value = false
  }
}

// Métodos de reset
const resetBasicConfig = (): void => {
  basicConfig.value = {
    name: 'Mi Asistente IA',
    model: 'gpt-4',
    temperature: 0.7,
    max_tokens: 2048,
    description: 'Un asistente inteligente para ayudar con diversas tareas.',
    system_prompt: 'Eres un asistente útil y amigable. Responde de manera clara y concisa, proporcionando información precisa y útil.',
    is_public: false,
    enable_memory: true,
    enable_web_search: false
  }
  basicErrors.value = {}
  toast.info('Configuración básica restablecida')
}

const resetAdvancedConfig = (): void => {
  advancedConfig.value = {
    top_p: 0.9,
    frequency_penalty: 0.0,
    presence_penalty: 0.0,
    timeout: 30,
    forbidden_words: ['spam', 'hack', 'virus'],
    context_window: 8192,
    max_conversations: 100,
    enable_content_filter: true,
    enable_pii_detection: true,
    enable_rate_limiting: true,
    enable_logging: true
  }
  toast.info('Configuración avanzada restablecida')
}

// Lifecycle
onMounted(() => {
  console.log('🔧 ChatbotConfigExample component mounted')
  console.log('📊 Initial config state:', {
    basicValid: isBasicConfigValid.value,
    advancedValid: isAdvancedConfigValid.value
  })
})
</script>

<style scoped>
/* Estilos específicos del componente */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mejoras visuales para inputs */
input:focus,
textarea:focus,
select:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* Animaciones suaves para botones */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Estilos para sliders */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  cursor: pointer;
}

input[type="range"]::-webkit-slider-track {
  background: #d1d5db;
  height: 8px;
  border-radius: 4px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  background: #3b82f6;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type="range"]::-moz-range-track {
  background: #d1d5db;
  height: 8px;
  border-radius: 4px;
  border: none;
}

input[type="range"]::-moz-range-thumb {
  background: #3b82f6;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Estilos para código */
pre {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 11px;
  line-height: 1.4;
}

/* Tags de palabras prohibidas */
.forbidden-word-tag {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>