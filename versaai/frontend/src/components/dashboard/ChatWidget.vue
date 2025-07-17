<template>
  <div class="chat-widget-container">
    <!-- Widget Preview -->
    <div class="widget-preview bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-medium text-gray-900">Vista Previa del Widget</h3>
        <div class="flex items-center space-x-2">
          <button
            @click="toggleWidgetSize"
            class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
          >
            {{ widgetSize === 'compact' ? 'Expandir' : 'Compactar' }}
          </button>
          <button
            @click="resetWidget"
            class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
          >
            <ArrowPathIcon class="w-3 h-3 mr-1" />
            Reset
          </button>
        </div>
      </div>
      
      <!-- Widget Simulator -->
      <div class="widget-simulator relative">
        <div 
          :class="[
            'chat-widget transition-all duration-300',
            widgetSize === 'compact' ? 'widget-compact' : 'widget-expanded',
            isWidgetOpen ? 'widget-open' : 'widget-closed'
          ]"
          :style="{
            '--primary-color': widgetConfig.primaryColor,
            '--secondary-color': widgetConfig.secondaryColor,
            '--text-color': widgetConfig.textColor
          }"
        >
          <!-- Widget Button -->
          <div 
            v-if="!isWidgetOpen"
            @click="toggleWidget"
            class="widget-button"
            :style="{ backgroundColor: widgetConfig.primaryColor }"
          >
            <ChatBubbleLeftRightIcon class="w-6 h-6 text-white" />
            <span v-if="widgetConfig.showUnreadCount && unreadCount > 0" class="unread-badge">
              {{ unreadCount }}
            </span>
          </div>
          
          <!-- Widget Chat Interface -->
          <div v-if="isWidgetOpen" class="widget-chat">
            <!-- Header -->
            <div class="widget-header" :style="{ backgroundColor: widgetConfig.primaryColor }">
              <div class="flex items-center space-x-3">
                <div class="widget-avatar">
                  <img 
                    v-if="widgetConfig.avatarUrl" 
                    :src="widgetConfig.avatarUrl" 
                    :alt="widgetConfig.botName"
                    class="w-8 h-8 rounded-full"
                  >
                  <div v-else class="w-8 h-8 rounded-full bg-white bg-opacity-20 flex items-center justify-center">
                    <ChatBubbleLeftRightIcon class="w-4 h-4 text-white" />
                  </div>
                </div>
                <div class="flex-1">
                  <div class="text-white font-medium text-sm">{{ widgetConfig.botName }}</div>
                  <div class="text-white text-opacity-80 text-xs">{{ widgetConfig.subtitle }}</div>
                </div>
                <button @click="toggleWidget" class="text-white hover:text-opacity-80">
                  <XMarkIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <!-- Messages -->
            <div class="widget-messages">
              <div v-for="message in chatMessages" :key="message.id" class="message-item">
                <div :class="['message', message.type === 'user' ? 'message-user' : 'message-bot']">
                  <div v-if="message.type === 'bot'" class="message-avatar">
                    <img 
                      v-if="widgetConfig.avatarUrl" 
                      :src="widgetConfig.avatarUrl" 
                      :alt="widgetConfig.botName"
                      class="w-6 h-6 rounded-full"
                    >
                    <div v-else class="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center">
                      <ChatBubbleLeftRightIcon class="w-3 h-3 text-gray-600" />
                    </div>
                  </div>
                  <div class="message-content">
                    <div 
                      :class="[
                        'message-bubble',
                        message.type === 'user' ? 'message-bubble-user' : 'message-bubble-bot'
                      ]"
                      :style="message.type === 'user' ? { backgroundColor: widgetConfig.primaryColor } : {}"
                    >
                      {{ message.content }}
                    </div>
                    <div class="message-time">
                      {{ formatTime(message.timestamp) }}
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Typing Indicator -->
              <div v-if="isTyping" class="message-item">
                <div class="message message-bot">
                  <div class="message-avatar">
                    <div class="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center">
                      <ChatBubbleLeftRightIcon class="w-3 h-3 text-gray-600" />
                    </div>
                  </div>
                  <div class="message-content">
                    <div class="message-bubble message-bubble-bot">
                      <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Input -->
            <div class="widget-input">
              <div class="input-container">
                <input
                  v-model="currentMessage"
                  @keypress.enter="sendMessage"
                  type="text"
                  :placeholder="widgetConfig.placeholder"
                  class="message-input"
                >
                <button 
                  @click="sendMessage"
                  :disabled="!currentMessage.trim()"
                  class="send-button"
                  :style="{ backgroundColor: widgetConfig.primaryColor }"
                >
                  <PaperAirplaneIcon class="w-4 h-4 text-white" />
                </button>
              </div>
              
              <!-- Quick Actions -->
              <div v-if="widgetConfig.quickActions.length > 0" class="quick-actions">
                <button
                  v-for="action in widgetConfig.quickActions"
                  :key="action.id"
                  @click="sendQuickAction(action.text)"
                  class="quick-action-btn"
                >
                  {{ action.text }}
                </button>
              </div>
            </div>
            
            <!-- Footer -->
            <div v-if="widgetConfig.showPoweredBy" class="widget-footer">
              <div class="text-xs text-gray-500 text-center">
                Powered by <span class="font-medium text-primary-600">VersaAI</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Widget Configuration -->
    <div class="widget-config bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración del Widget</h3>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Apariencia -->
        <div>
          <h4 class="text-md font-medium text-gray-900 mb-3">Apariencia</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nombre del Bot
              </label>
              <input
                v-model="widgetConfig.botName"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Subtítulo
              </label>
              <input
                v-model="widgetConfig.subtitle"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Placeholder del input
              </label>
              <input
                v-model="widgetConfig.placeholder"
                type="text"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                URL del Avatar
              </label>
              <input
                v-model="widgetConfig.avatarUrl"
                type="url"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
            </div>
          </div>
        </div>
        
        <!-- Colores -->
        <div>
          <h4 class="text-md font-medium text-gray-900 mb-3">Colores</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Color Primario
              </label>
              <div class="flex items-center space-x-3">
                <input
                  v-model="widgetConfig.primaryColor"
                  type="color"
                  class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                >
                <input
                  v-model="widgetConfig.primaryColor"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Color Secundario
              </label>
              <div class="flex items-center space-x-3">
                <input
                  v-model="widgetConfig.secondaryColor"
                  type="color"
                  class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                >
                <input
                  v-model="widgetConfig.secondaryColor"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Color del Texto
              </label>
              <div class="flex items-center space-x-3">
                <input
                  v-model="widgetConfig.textColor"
                  type="color"
                  class="h-10 w-16 border border-gray-300 rounded cursor-pointer"
                >
                <input
                  v-model="widgetConfig.textColor"
                  type="text"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Opciones adicionales -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <h4 class="text-md font-medium text-gray-900 mb-3">Opciones</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-gray-700">Mostrar contador de no leídos</label>
            <button
              @click="widgetConfig.showUnreadCount = !widgetConfig.showUnreadCount"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                widgetConfig.showUnreadCount ? 'bg-primary-600' : 'bg-gray-200'
              ]"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  widgetConfig.showUnreadCount ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
          
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-gray-700">Mostrar "Powered by"</label>
            <button
              @click="widgetConfig.showPoweredBy = !widgetConfig.showPoweredBy"
              :class="[
                'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                widgetConfig.showPoweredBy ? 'bg-primary-600' : 'bg-gray-200'
              ]"
            >
              <span
                :class="[
                  'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                  widgetConfig.showPoweredBy ? 'translate-x-5' : 'translate-x-0'
                ]"
              />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Acciones rápidas -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-md font-medium text-gray-900">Acciones Rápidas</h4>
          <button
            @click="addQuickAction"
            class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-primary-700 bg-primary-100 hover:bg-primary-200"
          >
            <PlusIcon class="w-3 h-3 mr-1" />
            Agregar
          </button>
        </div>
        
        <div class="space-y-2">
          <div v-for="(action, index) in widgetConfig.quickActions" :key="action.id" class="flex items-center space-x-2">
            <input
              v-model="action.text"
              type="text"
              placeholder="Texto de la acción"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
            <button
              @click="removeQuickAction(index)"
              class="p-2 text-red-600 hover:text-red-800"
            >
              <XMarkIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Botones de acción -->
      <div class="mt-6 pt-6 border-t border-gray-200 flex justify-end space-x-3">
        <button
          @click="saveConfiguration"
          :disabled="isSaving"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          {{ isSaving ? 'Guardando...' : 'Guardar Configuración' }}
        </button>
        
        <button
          @click="generateEmbedCode"
          class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <CodeBracketIcon class="w-4 h-4 mr-2" />
          Generar Código
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  ChatBubbleLeftRightIcon,
  XMarkIcon,
  PaperAirplaneIcon,
  PlusIcon,
  ArrowPathIcon,
  CodeBracketIcon
} from '@heroicons/vue/24/outline'

// Estado reactivo
const isWidgetOpen = ref(false)
const widgetSize = ref('expanded')
const currentMessage = ref('')
const isTyping = ref(false)
const unreadCount = ref(3)
const isSaving = ref(false)

// Configuración del widget
const widgetConfig = ref({
  botName: 'VersaAI Assistant',
  subtitle: 'Estoy aquí para ayudarte',
  placeholder: 'Escribe tu mensaje...',
  avatarUrl: '',
  primaryColor: '#3B82F6',
  secondaryColor: '#EFF6FF',
  textColor: '#1F2937',
  showUnreadCount: true,
  showPoweredBy: true,
  quickActions: [
    { id: 1, text: '¿Cómo funciona?' },
    { id: 2, text: 'Precios' },
    { id: 3, text: 'Contactar soporte' }
  ]
})

// Mensajes del chat
const chatMessages = ref([
  {
    id: 1,
    type: 'bot',
    content: '¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?',
    timestamp: new Date(Date.now() - 300000)
  },
  {
    id: 2,
    type: 'user',
    content: 'Hola, me gustaría saber más sobre sus servicios',
    timestamp: new Date(Date.now() - 240000)
  },
  {
    id: 3,
    type: 'bot',
    content: 'Por supuesto, estaré encantado de ayudarte. Ofrecemos soluciones de IA conversacional para empresas. ¿Hay algo específico que te interese?',
    timestamp: new Date(Date.now() - 180000)
  }
])

// Métodos
const toggleWidget = () => {
  isWidgetOpen.value = !isWidgetOpen.value
  if (isWidgetOpen.value) {
    unreadCount.value = 0
  }
}

const toggleWidgetSize = () => {
  widgetSize.value = widgetSize.value === 'compact' ? 'expanded' : 'compact'
}

const resetWidget = () => {
  isWidgetOpen.value = false
  currentMessage.value = ''
  unreadCount.value = 3
}

const sendMessage = () => {
  if (!currentMessage.value.trim()) return
  
  // Agregar mensaje del usuario
  chatMessages.value.push({
    id: Date.now(),
    type: 'user',
    content: currentMessage.value,
    timestamp: new Date()
  })
  
  const userMessage = currentMessage.value
  currentMessage.value = ''
  
  // Simular respuesta del bot
  isTyping.value = true
  setTimeout(() => {
    isTyping.value = false
    chatMessages.value.push({
      id: Date.now() + 1,
      type: 'bot',
      content: generateBotResponse(userMessage),
      timestamp: new Date()
    })
  }, 1500)
}

const sendQuickAction = (actionText) => {
  currentMessage.value = actionText
  sendMessage()
}

const generateBotResponse = (userMessage) => {
  const responses = [
    'Gracias por tu mensaje. Te ayudo con eso enseguida.',
    'Entiendo tu consulta. Déjame buscar la información para ti.',
    'Excelente pregunta. Te proporciono los detalles que necesitas.',
    'Por supuesto, puedo ayudarte con eso. Aquí tienes la información.',
    'Me alegra poder asistirte. Esta es la respuesta a tu consulta.'
  ]
  
  return responses[Math.floor(Math.random() * responses.length)]
}

const addQuickAction = () => {
  widgetConfig.value.quickActions.push({
    id: Date.now(),
    text: ''
  })
}

const removeQuickAction = (index) => {
  widgetConfig.value.quickActions.splice(index, 1)
}

const saveConfiguration = async () => {
  isSaving.value = true
  try {
    // Simular guardado
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Aquí iría la llamada a la API para guardar la configuración
    console.log('Configuración guardada:', widgetConfig.value)
  } catch (error) {
    console.error('Error al guardar configuración:', error)
  } finally {
    isSaving.value = false
  }
}

const generateEmbedCode = () => {
  const embedCode = `
<!-- VersaAI Chat Widget -->
<script>
  window.VersaAIConfig = {
    botName: "${widgetConfig.value.botName}",
    subtitle: "${widgetConfig.value.subtitle}",
    primaryColor: "${widgetConfig.value.primaryColor}",
    secondaryColor: "${widgetConfig.value.secondaryColor}",
    textColor: "${widgetConfig.value.textColor}",
    placeholder: "${widgetConfig.value.placeholder}",
    avatarUrl: "${widgetConfig.value.avatarUrl}",
    showUnreadCount: ${widgetConfig.value.showUnreadCount},
    showPoweredBy: ${widgetConfig.value.showPoweredBy},
    quickActions: ${JSON.stringify(widgetConfig.value.quickActions)}
  };
</script>
<script src="https://cdn.versaai.com/widget/versaai-widget.js"></script>
<!-- End VersaAI Chat Widget -->`
  
  // Copiar al portapapeles
  navigator.clipboard.writeText(embedCode).then(() => {
    alert('Código copiado al portapapeles')
  })
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  // Inicializar widget
})
</script>

<style scoped>
/* Widget Styles */
.chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.widget-compact {
  max-width: 300px;
}

.widget-expanded {
  max-width: 380px;
}

.widget-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  position: relative;
}

.widget-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.unread-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #EF4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
}

.widget-chat {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.widget-header {
  padding: 16px;
  color: white;
}

.widget-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #F9FAFB;
}

.message-item {
  margin-bottom: 16px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  max-width: 80%;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.4;
}

.message-bubble-bot {
  background: white;
  color: #374151;
  border-bottom-left-radius: 4px;
}

.message-bubble-user {
  color: white;
  border-bottom-right-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #9CA3AF;
  margin-top: 4px;
  text-align: right;
}

.message-user .message-time {
  text-align: left;
}

.typing-indicator {
  display: flex;
  gap: 4px;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #9CA3AF;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.widget-input {
  padding: 16px;
  background: white;
  border-top: 1px solid #E5E7EB;
}

.input-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #D1D5DB;
  border-radius: 24px;
  outline: none;
  font-size: 14px;
}

.message-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.send-button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
}

.quick-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.quick-action-btn {
  padding: 8px 12px;
  background: #F3F4F6;
  border: 1px solid #D1D5DB;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-action-btn:hover {
  background: #E5E7EB;
}

.widget-footer {
  padding: 8px 16px;
  background: #F9FAFB;
  border-top: 1px solid #E5E7EB;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-widget {
    bottom: 10px;
    right: 10px;
    left: 10px;
    max-width: none !important;
  }
  
  .widget-chat {
    height: 400px;
  }
}

/* Animations */
.widget-open {
  animation: slideUp 0.3s ease-out;
}

.widget-closed {
  animation: slideDown 0.3s ease-out;
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

@keyframes slideDown {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}
</style>