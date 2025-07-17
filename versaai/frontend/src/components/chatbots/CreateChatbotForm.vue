<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Información Básica -->
    <div class="space-y-4">
      <h3 class="text-lg font-medium text-gray-900">Información Básica</h3>
      
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
          Nombre del Chatbot *
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          placeholder="Ej: Asistente de Ventas"
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
          :class="{ 'border-red-500': errors.name }"
        />
        <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
          Descripción
        </label>
        <textarea
          id="description"
          v-model="form.description"
          rows="3"
          placeholder="Describe el propósito y funcionalidades del chatbot..."
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 resize-none"
          :class="{ 'border-red-500': errors.description }"
        ></textarea>
        <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
            Categoría *
          </label>
          <select
            id="category"
            v-model="form.category"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            :class="{ 'border-red-500': errors.category }"
          >
            <option value="">Seleccionar categoría</option>
            <option value="customer-service">Atención al Cliente</option>
            <option value="sales">Ventas</option>
            <option value="support">Soporte Técnico</option>
            <option value="general">General</option>
            <option value="hr">Recursos Humanos</option>
            <option value="marketing">Marketing</option>
          </select>
          <p v-if="errors.category" class="mt-1 text-sm text-red-600">{{ errors.category }}</p>
        </div>

        <div>
          <label for="language" class="block text-sm font-medium text-gray-700 mb-2">
            Idioma Principal *
          </label>
          <select
            id="language"
            v-model="form.language"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
            :class="{ 'border-red-500': errors.language }"
          >
            <option value="">Seleccionar idioma</option>
            <option value="es">Español</option>
            <option value="en">Inglés</option>
            <option value="pt">Portugués</option>
            <option value="fr">Francés</option>
          </select>
          <p v-if="errors.language" class="mt-1 text-sm text-red-600">{{ errors.language }}</p>
        </div>
      </div>
    </div>

    <!-- Configuración de IA -->
    <div class="space-y-4 border-t border-gray-200 pt-6">
      <h3 class="text-lg font-medium text-gray-900">Configuración de IA</h3>
      
      <div>
        <label for="model" class="block text-sm font-medium text-gray-700 mb-2">
          Modelo de IA *
        </label>
        <select
          id="model"
          v-model="form.model"
          required
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
          :class="{ 'border-red-500': errors.model }"
        >
          <option value="">Seleccionar modelo</option>
          <option value="llama-3.1-70b">Llama 3.1 70B (Recomendado)</option>
          <option value="llama-3.1-8b">Llama 3.1 8B (Rápido)</option>
          <option value="mixtral-8x7b">Mixtral 8x7B (Balanceado)</option>
          <option value="gemma-7b">Gemma 7B (Eficiente)</option>
        </select>
        <p v-if="errors.model" class="mt-1 text-sm text-red-600">{{ errors.model }}</p>
      </div>

      <div>
        <label for="personality" class="block text-sm font-medium text-gray-700 mb-2">
          Personalidad del Chatbot
        </label>
        <textarea
          id="personality"
          v-model="form.personality"
          rows="3"
          placeholder="Ej: Eres un asistente amigable y profesional que ayuda a los clientes con sus consultas sobre productos..."
          class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300 resize-none"
        ></textarea>
        <p class="mt-1 text-sm text-gray-500">Define cómo debe comportarse y responder el chatbot</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="temperature" class="block text-sm font-medium text-gray-700 mb-2">
            Creatividad (Temperature): {{ form.temperature }}
          </label>
          <input
            id="temperature"
            v-model.number="form.temperature"
            type="range"
            min="0"
            max="1"
            step="0.1"
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>Conservador</span>
            <span>Creativo</span>
          </div>
        </div>

        <div>
          <label for="max_tokens" class="block text-sm font-medium text-gray-700 mb-2">
            Longitud de Respuesta
          </label>
          <select
            id="max_tokens"
            v-model.number="form.max_tokens"
            class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
          >
            <option :value="150">Corta (150 tokens)</option>
            <option :value="300">Media (300 tokens)</option>
            <option :value="500">Larga (500 tokens)</option>
            <option :value="1000">Muy Larga (1000 tokens)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Configuración Avanzada -->
    <div class="space-y-4 border-t border-gray-200 pt-6">
      <h3 class="text-lg font-medium text-gray-900">Configuración Avanzada</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center">
          <input
            id="enable_rag"
            v-model="form.enable_rag"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label for="enable_rag" class="ml-2 block text-sm text-gray-900">
            Habilitar RAG (Retrieval-Augmented Generation)
          </label>
        </div>

        <div class="flex items-center">
          <input
            id="enable_memory"
            v-model="form.enable_memory"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label for="enable_memory" class="ml-2 block text-sm text-gray-900">
            Memoria de conversación
          </label>
        </div>

        <div class="flex items-center">
          <input
            id="enable_analytics"
            v-model="form.enable_analytics"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label for="enable_analytics" class="ml-2 block text-sm text-gray-900">
            Análisis de conversaciones
          </label>
        </div>

        <div class="flex items-center">
          <input
            id="auto_start"
            v-model="form.auto_start"
            type="checkbox"
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label for="auto_start" class="ml-2 block text-sm text-gray-900">
            Iniciar automáticamente
          </label>
        </div>
      </div>
    </div>

    <!-- Botones de Acción -->
    <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200">
      <EnhancedButton
        type="button"
        variant="secondary"
        @click="$emit('cancel')"
        :disabled="isSubmitting"
      >
        Cancelar
      </EnhancedButton>
      <EnhancedButton
        type="submit"
        variant="primary"
        :loading="isSubmitting"
        :disabled="!isFormValid"
      >
        <PlusIcon class="w-5 h-5 mr-2" />
        Crear Chatbot
      </EnhancedButton>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import EnhancedButton from '@/components/ui/EnhancedButton.vue'

// Emits
const emit = defineEmits(['created', 'cancel'])

// Estado reactivo
const isSubmitting = ref(false)
const errors = ref({})

// Formulario
const form = reactive({
  name: '',
  description: '',
  category: '',
  language: 'es',
  model: 'llama-3.1-70b',
  personality: '',
  temperature: 0.7,
  max_tokens: 300,
  enable_rag: true,
  enable_memory: true,
  enable_analytics: true,
  auto_start: false
})

// Computed properties
const isFormValid = computed(() => {
  return form.name.trim() && 
         form.category && 
         form.language && 
         form.model &&
         Object.keys(errors.value).length === 0
})

// Métodos
const validateForm = () => {
  errors.value = {}

  if (!form.name.trim()) {
    errors.value.name = 'El nombre es requerido'
  } else if (form.name.length < 3) {
    errors.value.name = 'El nombre debe tener al menos 3 caracteres'
  } else if (form.name.length > 50) {
    errors.value.name = 'El nombre no puede exceder 50 caracteres'
  }

  if (form.description && form.description.length > 500) {
    errors.value.description = 'La descripción no puede exceder 500 caracteres'
  }

  if (!form.category) {
    errors.value.category = 'La categoría es requerida'
  }

  if (!form.language) {
    errors.value.language = 'El idioma es requerido'
  }

  if (!form.model) {
    errors.value.model = 'El modelo de IA es requerido'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Simular creación del chatbot
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const newChatbot = {
      id: Date.now(),
      name: form.name,
      description: form.description || 'Sin descripción',
      status: form.auto_start ? 'active' : 'inactive',
      category: form.category,
      conversations: 0,
      accuracy: 0,
      training_progress: 0,
      updated_at: new Date(),
      ...form
    }

    emit('created', newChatbot)
  } catch (error) {
    console.error('Error al crear chatbot:', error)
    errors.value.submit = 'Error al crear el chatbot. Inténtalo de nuevo.'
  } finally {
    isSubmitting.value = false
  }
}

// Limpiar errores cuando el usuario empiece a escribir
const clearError = (field) => {
  if (errors.value[field]) {
    delete errors.value[field]
  }
}
</script>

<style scoped>
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>