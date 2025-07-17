<template>
  <div class="widget-configurator bg-white rounded-lg shadow-sm border border-gray-200">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">Configurador de Widget</h3>
          <p class="text-sm text-gray-600 mt-1">Personaliza la apariencia y comportamiento de tu widget de chat</p>
        </div>
        <div class="flex items-center space-x-3">
          <button
            @click="resetToDefaults"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <ArrowPathIcon class="w-4 h-4 mr-2" />
            Restablecer
          </button>
          <button
            @click="saveConfiguration"
            :disabled="isSaving"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {{ isSaving ? 'Guardando...' : 'Guardar Configuración' }}
          </button>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <!-- Panel de Configuración -->
        <div class="xl:col-span-2 space-y-6">
          <!-- Configuración Básica -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Configuración Básica</h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Chatbot
                </label>
                <input
                  v-model="config.botName"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Mi Asistente Virtual"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Mensaje de Bienvenida
                </label>
                <input
                  v-model="config.welcomeMessage"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="¡Hola! ¿En qué puedo ayudarte?"
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Placeholder del Input
                </label>
                <input
                  v-model="config.inputPlaceholder"
                  type="text"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Escribe tu mensaje..."
                >
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Idioma
                </label>
                <select
                  v-model="config.language"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="es">Español</option>
                  <option value="en">English</option>
                  <option value="fr">Français</option>
                  <option value="de">Deutsch</option>
                  <option value="pt">Português</option>
                </select>
              </div>
            </div>
          </div>
          
          <!-- Apariencia y Estilo -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Apariencia y Estilo</h4>
            
            <div class="space-y-4">
              <!-- Colores -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Color Primario
                  </label>
                  <div class="flex items-center space-x-2">
                    <input
                      v-model="config.primaryColor"
                      type="color"
                      class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                    >
                    <input
                      v-model="config.primaryColor"
                      type="text"
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    >
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Color de Fondo
                  </label>
                  <div class="flex items-center space-x-2">
                    <input
                      v-model="config.backgroundColor"
                      type="color"
                      class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                    >
                    <input
                      v-model="config.backgroundColor"
                      type="text"
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    >
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Color del Texto
                  </label>
                  <div class="flex items-center space-x-2">
                    <input
                      v-model="config.textColor"
                      type="color"
                      class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                    >
                    <input
                      v-model="config.textColor"
                      type="text"
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    >
                  </div>
                </div>
              </div>
              
              <!-- Posición y Tamaño -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Posición
                  </label>
                  <select
                    v-model="config.position"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="bottom-right">Abajo Derecha</option>
                    <option value="bottom-left">Abajo Izquierda</option>
                    <option value="top-right">Arriba Derecha</option>
                    <option value="top-left">Arriba Izquierda</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Tamaño del Widget
                  </label>
                  <select
                    v-model="config.size"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="small">Pequeño</option>
                    <option value="medium">Mediano</option>
                    <option value="large">Grande</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Forma del Botón
                  </label>
                  <select
                    v-model="config.buttonShape"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="circle">Circular</option>
                    <option value="square">Cuadrado</option>
                    <option value="rounded">Redondeado</option>
                  </select>
                </div>
              </div>
              
              <!-- Avatar -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  URL del Avatar
                </label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="config.avatarUrl"
                    type="url"
                    class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    placeholder="https://ejemplo.com/avatar.jpg"
                  >
                  <button
                    @click="uploadAvatar"
                    class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <PhotoIcon class="w-4 h-4 mr-2" />
                    Subir
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Comportamiento -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h4 class="text-lg font-medium text-gray-900 mb-4">Comportamiento</h4>
            
            <div class="space-y-4">
              <!-- Opciones de comportamiento -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="flex items-center justify-between">
                  <div>
                    <label class="text-sm font-medium text-gray-700">Auto-abrir widget</label>
                    <p class="text-xs text-gray-500">Abrir automáticamente después de unos segundos</p>
                  </div>
                  <button
                    @click="config.autoOpen = !config.autoOpen"
                    :class="[
                      'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                      config.autoOpen ? 'bg-primary-600' : 'bg-gray-200'
                    ]"
                  >
                    <span
                      :class="[
                        'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                        config.autoOpen ? 'translate-x-5' : 'translate-x-0'
                      ]"
                    />
                  </button>
                </div>
                
                <div class="flex items-center justify-between">
                  <div>
                    <label class="text-sm font-medium text-gray-700">Mostrar notificaciones</label>
                    <p class="text-xs text-gray-500">Mostrar badge con mensajes no leídos</p>
                  </div>
                  <button
                    @click="config.showNotifications = !config.showNotifications"
                    :class="[
                      'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                      config.showNotifications ? 'bg-primary-600' : 'bg-gray-200'
                    ]"
                  >
                    <span
                      :class="[
                        'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                        config.showNotifications ? 'translate-x-5' : 'translate-x-0'
                      ]"
                    />
                  </button>
                </div>
                
                <div class="flex items-center justify-between">
                  <div>
                    <label class="text-sm font-medium text-gray-700">Sonidos</label>
                    <p class="text-xs text-gray-500">Reproducir sonidos para nuevos mensajes</p>
                  </div>
                  <button
                    @click="config.enableSounds = !config.enableSounds"
                    :class="[
                      'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                      config.enableSounds ? 'bg-primary-600' : 'bg-gray-200'
                    ]"
                  >
                    <span
                      :class="[
                        'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                        config.enableSounds ? 'translate-x-5' : 'translate-x-0'
                      ]"
                    />
                  </button>
                </div>
                
                <div class="flex items-center justify-between">
                  <div>
                    <label class="text-sm font-medium text-gray-700">Mostrar "Powered by"</label>
                    <p class="text-xs text-gray-500">Mostrar marca VersaAI en el widget</p>
                  </div>
                  <button
                    @click="config.showPoweredBy = !config.showPoweredBy"
                    :class="[
                      'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                      config.showPoweredBy ? 'bg-primary-600' : 'bg-gray-200'
                    ]"
                  >
                    <span
                      :class="[
                        'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                        config.showPoweredBy ? 'translate-x-5' : 'translate-x-0'
                      ]"
                    />
                  </button>
                </div>
              </div>
              
              <!-- Configuraciones numéricas -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-if="config.autoOpen">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Retraso de auto-apertura (segundos)
                  </label>
                  <input
                    v-model.number="config.autoOpenDelay"
                    type="number"
                    min="1"
                    max="60"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Altura máxima del chat (px)
                  </label>
                  <input
                    v-model.number="config.maxHeight"
                    type="number"
                    min="300"
                    max="800"
                    step="50"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                </div>
              </div>
            </div>
          </div>
          
          <!-- Mensajes Predefinidos -->
          <div class="bg-gray-50 rounded-lg p-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-medium text-gray-900">Mensajes Predefinidos</h4>
              <button
                @click="addPredefinedMessage"
                class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200"
              >
                <PlusIcon class="w-4 h-4 mr-2" />
                Agregar Mensaje
              </button>
            </div>
            
            <div class="space-y-3">
              <div v-for="(message, index) in config.predefinedMessages" :key="index" class="flex items-center space-x-3">
                <input
                  v-model="message.text"
                  type="text"
                  placeholder="Texto del mensaje predefinido"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                <button
                  @click="removePredefinedMessage(index)"
                  class="p-2 text-red-600 hover:text-red-800"
                >
                  <XMarkIcon class="w-4 h-4" />
                </button>
              </div>
              
              <div v-if="config.predefinedMessages.length === 0" class="text-center py-4 text-gray-500">
                No hay mensajes predefinidos. Agrega algunos para mejorar la experiencia del usuario.
              </div>
            </div>
          </div>
        </div>
        
        <!-- Vista Previa -->
        <div class="xl:col-span-1">
          <div class="sticky top-6">
            <div class="bg-gray-50 rounded-lg p-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Vista Previa</h4>
              
              <!-- Simulador del widget -->
              <div class="widget-preview-container relative bg-white rounded-lg border-2 border-dashed border-gray-300 p-8 min-h-[400px]">
                <div 
                  :class="[
                    'widget-preview absolute',
                    getPositionClass(config.position),
                    getSizeClass(config.size)
                  ]"
                >
                  <!-- Botón del widget -->
                  <div 
                    v-if="!isPreviewOpen"
                    @click="togglePreview"
                    :class="[
                      'widget-button cursor-pointer flex items-center justify-center text-white shadow-lg transition-all duration-200 hover:scale-105',
                      getButtonShapeClass(config.buttonShape)
                    ]"
                    :style="{ backgroundColor: config.primaryColor }"
                  >
                    <ChatBubbleLeftRightIcon class="w-6 h-6" />
                    <span v-if="config.showNotifications" class="notification-badge">3</span>
                  </div>
                  
                  <!-- Chat abierto -->
                  <div v-if="isPreviewOpen" class="widget-chat bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden">
                    <!-- Header -->
                    <div class="widget-chat-header p-4 text-white" :style="{ backgroundColor: config.primaryColor }">
                      <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                          <img v-if="config.avatarUrl" :src="config.avatarUrl" class="w-8 h-8 rounded-full" />
                          <div v-else class="w-8 h-8 rounded-full bg-white bg-opacity-20 flex items-center justify-center">
                            <ChatBubbleLeftRightIcon class="w-4 h-4" />
                          </div>
                          <div>
                            <div class="font-medium text-sm">{{ config.botName }}</div>
                            <div class="text-xs opacity-80">En línea</div>
                          </div>
                        </div>
                        <button @click="togglePreview" class="text-white hover:text-opacity-80">
                          <XMarkIcon class="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                    
                    <!-- Mensajes -->
                    <div class="widget-chat-messages p-4 space-y-3" :style="{ maxHeight: config.maxHeight + 'px' }">
                      <div class="flex items-start space-x-2">
                        <img v-if="config.avatarUrl" :src="config.avatarUrl" class="w-6 h-6 rounded-full" />
                        <div v-else class="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center">
                          <ChatBubbleLeftRightIcon class="w-3 h-3 text-gray-600" />
                        </div>
                        <div class="bg-gray-100 rounded-lg p-3 max-w-xs">
                          <p class="text-sm" :style="{ color: config.textColor }">{{ config.welcomeMessage }}</p>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Input -->
                    <div class="widget-chat-input p-4 border-t border-gray-200">
                      <div class="flex items-center space-x-2">
                        <input
                          type="text"
                          :placeholder="config.inputPlaceholder"
                          class="flex-1 px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                          readonly
                        >
                        <button 
                          class="p-2 rounded-full text-white"
                          :style="{ backgroundColor: config.primaryColor }"
                        >
                          <PaperAirplaneIcon class="w-4 h-4" />
                        </button>
                      </div>
                      
                      <!-- Mensajes predefinidos -->
                      <div v-if="config.predefinedMessages.length > 0" class="mt-3 flex flex-wrap gap-2">
                        <button
                          v-for="message in config.predefinedMessages.slice(0, 3)"
                          :key="message.text"
                          class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs hover:bg-gray-200"
                        >
                          {{ message.text }}
                        </button>
                      </div>
                    </div>
                    
                    <!-- Footer -->
                    <div v-if="config.showPoweredBy" class="widget-chat-footer p-2 bg-gray-50 border-t border-gray-200">
                      <div class="text-center text-xs text-gray-500">
                        Powered by <span class="font-medium text-primary-600">VersaAI</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Información de la vista previa -->
              <div class="mt-4 text-sm text-gray-600">
                <p><strong>Posición:</strong> {{ getPositionLabel(config.position) }}</p>
                <p><strong>Tamaño:</strong> {{ getSizeLabel(config.size) }}</p>
                <p><strong>Idioma:</strong> {{ getLanguageLabel(config.language) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer con acciones -->
    <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-600">
          Última actualización: {{ lastUpdated }}
        </div>
        <div class="flex items-center space-x-3">
          <button
            @click="exportConfiguration"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
            Exportar
          </button>
          <button
            @click="generateEmbedCode"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            <CodeBracketIcon class="w-4 h-4 mr-2" />
            Generar Código
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  ArrowPathIcon,
  PlusIcon,
  XMarkIcon,
  PhotoIcon,
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  ArrowDownTrayIcon,
  CodeBracketIcon
} from '@heroicons/vue/24/outline'

// Estado reactivo
const isSaving = ref(false)
const isPreviewOpen = ref(false)
const lastUpdated = ref(new Date().toLocaleString())

// Configuración del widget
const config = ref({
  // Básico
  botName: 'VersaAI Assistant',
  welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
  inputPlaceholder: 'Escribe tu mensaje...',
  language: 'es',
  
  // Apariencia
  primaryColor: '#3B82F6',
  backgroundColor: '#FFFFFF',
  textColor: '#1F2937',
  position: 'bottom-right',
  size: 'medium',
  buttonShape: 'circle',
  avatarUrl: '',
  
  // Comportamiento
  autoOpen: false,
  autoOpenDelay: 5,
  showNotifications: true,
  enableSounds: true,
  showPoweredBy: true,
  maxHeight: 500,
  
  // Mensajes predefinidos
  predefinedMessages: [
    { text: '¿Cómo funciona?' },
    { text: 'Ver precios' },
    { text: 'Contactar soporte' }
  ]
})

// Configuración por defecto
const defaultConfig = {
  botName: 'VersaAI Assistant',
  welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
  inputPlaceholder: 'Escribe tu mensaje...',
  language: 'es',
  primaryColor: '#3B82F6',
  backgroundColor: '#FFFFFF',
  textColor: '#1F2937',
  position: 'bottom-right',
  size: 'medium',
  buttonShape: 'circle',
  avatarUrl: '',
  autoOpen: false,
  autoOpenDelay: 5,
  showNotifications: true,
  enableSounds: true,
  showPoweredBy: true,
  maxHeight: 500,
  predefinedMessages: [
    { text: '¿Cómo funciona?' },
    { text: 'Ver precios' },
    { text: 'Contactar soporte' }
  ]
}

// Métodos
const togglePreview = () => {
  isPreviewOpen.value = !isPreviewOpen.value
}

const resetToDefaults = () => {
  config.value = { ...defaultConfig }
  lastUpdated.value = new Date().toLocaleString()
}

const saveConfiguration = async () => {
  isSaving.value = true
  try {
    // Simular guardado
    await new Promise(resolve => setTimeout(resolve, 1000))
    lastUpdated.value = new Date().toLocaleString()
    // Aquí iría la llamada a la API
  } catch (error) {
    console.error('Error al guardar configuración:', error)
  } finally {
    isSaving.value = false
  }
}

const addPredefinedMessage = () => {
  config.value.predefinedMessages.push({ text: '' })
}

const removePredefinedMessage = (index) => {
  config.value.predefinedMessages.splice(index, 1)
}

const uploadAvatar = () => {
  // Simular subida de archivo
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Aquí iría la lógica de subida real
      const reader = new FileReader()
      reader.onload = (e) => {
        config.value.avatarUrl = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
  input.click()
}

const exportConfiguration = () => {
  const configJson = JSON.stringify(config.value, null, 2)
  const blob = new Blob([configJson], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'widget-config.json'
  a.click()
  URL.revokeObjectURL(url)
}

const generateEmbedCode = () => {
  const embedCode = `
<!-- VersaAI Chat Widget -->
<script>
  window.VersaAIConfig = ${JSON.stringify(config.value, null, 2)};
<\/script>
<script src="https://cdn.versaai.com/widget/versaai-widget.js"><\/script>
<!-- End VersaAI Chat Widget -->`
  
  navigator.clipboard.writeText(embedCode).then(() => {
    alert('Código de integración copiado al portapapeles')
  })
}

// Helpers para clases CSS
const getPositionClass = (position) => {
  const positions = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4'
  }
  return positions[position] || positions['bottom-right']
}

const getSizeClass = (size) => {
  const sizes = {
    'small': 'w-12 h-12',
    'medium': 'w-16 h-16',
    'large': 'w-20 h-20'
  }
  return sizes[size] || sizes['medium']
}

const getButtonShapeClass = (shape) => {
  const shapes = {
    'circle': 'rounded-full',
    'square': 'rounded-none',
    'rounded': 'rounded-lg'
  }
  return shapes[shape] || shapes['circle']
}

// Helpers para labels
const getPositionLabel = (position) => {
  const labels = {
    'bottom-right': 'Abajo Derecha',
    'bottom-left': 'Abajo Izquierda',
    'top-right': 'Arriba Derecha',
    'top-left': 'Arriba Izquierda'
  }
  return labels[position] || position
}

const getSizeLabel = (size) => {
  const labels = {
    'small': 'Pequeño',
    'medium': 'Mediano',
    'large': 'Grande'
  }
  return labels[size] || size
}

const getLanguageLabel = (language) => {
  const labels = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français',
    'de': 'Deutsch',
    'pt': 'Português'
  }
  return labels[language] || language
}

// Watchers
watch(config, () => {
  lastUpdated.value = new Date().toLocaleString()
}, { deep: true })

// Lifecycle
onMounted(() => {
  // Cargar configuración guardada si existe
})
</script>

<style scoped>
.widget-preview-container {
  position: relative;
  min-height: 400px;
  background-image: 
    radial-gradient(circle at 25px 25px, lightgray 2px, transparent 0),
    radial-gradient(circle at 75px 75px, lightgray 2px, transparent 0);
  background-size: 100px 100px;
  background-position: 0 0, 50px 50px;
}

.widget-preview {
  z-index: 10;
}

.widget-button {
  transition: all 0.3s ease;
  position: relative;
}

.widget-button:hover {
  transform: scale(1.05);
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #EF4444;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
}

.widget-chat {
  width: 320px;
  height: 450px;
  display: flex;
  flex-direction: column;
}

.widget-chat-messages {
  flex: 1;
  overflow-y: auto;
  background: #F9FAFB;
}

.widget-chat-input {
  background: white;
}

.widget-chat-footer {
  background: #F9FAFB;
}

/* Responsive */
@media (max-width: 1280px) {
  .widget-preview-container {
    min-height: 300px;
  }
  
  .widget-chat {
    width: 280px;
    height: 400px;
  }
}

@media (max-width: 768px) {
  .widget-preview-container {
    min-height: 250px;
  }
  
  .widget-chat {
    width: 250px;
    height: 350px;
  }
}

/* Animaciones */
.widget-preview {
  transition: all 0.3s ease;
}

.widget-chat {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>