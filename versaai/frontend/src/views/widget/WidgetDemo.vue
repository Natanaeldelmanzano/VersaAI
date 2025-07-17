<template>
  <div class="widget-demo">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Demo del Widget de Chat</h1>
            <p class="mt-2 text-gray-600">Prueba nuestro widget de chat en acción</p>
          </div>
          <router-link 
            to="/"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Volver al Inicio
          </router-link>
        </div>
      </div>
    </div>

    <!-- Demo Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Configuration Panel -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Configuración del Widget</h2>
          
          <div class="space-y-4">
            <!-- Widget Theme -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tema</label>
              <select 
                v-model="widgetConfig.theme" 
                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="light">Claro</option>
                <option value="dark">Oscuro</option>
                <option value="blue">Azul</option>
              </select>
            </div>

            <!-- Widget Position -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Posición</label>
              <select 
                v-model="widgetConfig.position" 
                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="bottom-right">Abajo Derecha</option>
                <option value="bottom-left">Abajo Izquierda</option>
                <option value="top-right">Arriba Derecha</option>
                <option value="top-left">Arriba Izquierda</option>
              </select>
            </div>

            <!-- Welcome Message -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Mensaje de Bienvenida</label>
              <textarea 
                v-model="widgetConfig.welcomeMessage" 
                rows="3"
                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="¡Hola! ¿En qué puedo ayudarte hoy?"
              ></textarea>
            </div>

            <!-- Bot Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Bot</label>
              <input 
                v-model="widgetConfig.botName" 
                type="text"
                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Asistente Virtual"
              >
            </div>

            <!-- Primary Color -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Color Principal</label>
              <input 
                v-model="widgetConfig.primaryColor" 
                type="color"
                class="w-full h-10 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>

            <!-- Show Avatar -->
            <div class="flex items-center">
              <input 
                v-model="widgetConfig.showAvatar" 
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <label class="ml-2 text-sm text-gray-700">Mostrar Avatar del Bot</label>
            </div>

            <!-- Enable Sound -->
            <div class="flex items-center">
              <input 
                v-model="widgetConfig.enableSound" 
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <label class="ml-2 text-sm text-gray-700">Habilitar Sonidos</label>
            </div>
          </div>

          <!-- Reset Button -->
          <button 
            @click="resetConfig"
            class="mt-6 w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 transition-colors"
          >
            Restablecer Configuración
          </button>
        </div>

        <!-- Preview Panel -->
        <div class="bg-gray-100 rounded-lg p-6 relative" style="min-height: 600px;">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Vista Previa</h2>
          <p class="text-gray-600 mb-4">Así se verá el widget en tu sitio web:</p>
          
          <!-- Simulated Website -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 h-96 relative overflow-hidden">
            <!-- Fake Website Content -->
            <div class="p-6">
              <div class="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
              <div class="h-4 bg-gray-200 rounded w-2/3 mb-6"></div>
              <div class="h-20 bg-gray-100 rounded mb-4"></div>
              <div class="h-4 bg-gray-200 rounded w-full mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-5/6 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-4/5"></div>
            </div>

            <!-- Chat Widget -->
            <div 
              class="absolute transition-all duration-300"
              :class="getWidgetPositionClasses()"
              :style="{ zIndex: 1000 }"
            >
              <!-- Chat Button -->
              <div 
                v-if="!chatOpen"
                @click="chatOpen = true"
                class="w-14 h-14 rounded-full shadow-lg cursor-pointer flex items-center justify-center transition-transform hover:scale-110"
                :style="{ backgroundColor: widgetConfig.primaryColor }"
              >
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.955 8.955 0 01-4.906-1.471L3 21l2.471-5.094A8.955 8.955 0 013 12c0-4.418 3.582-8 8-8s8 3.582 8 8z" />
                </svg>
              </div>

              <!-- Chat Window -->
              <div 
                v-if="chatOpen"
                class="w-80 h-96 bg-white rounded-lg shadow-xl border border-gray-200 flex flex-col"
                :class="getThemeClasses()"
              >
                <!-- Header -->
                <div 
                  class="flex items-center justify-between p-4 border-b border-gray-200 rounded-t-lg"
                  :style="{ backgroundColor: widgetConfig.primaryColor }"
                >
                  <div class="flex items-center space-x-3">
                    <div 
                      v-if="widgetConfig.showAvatar"
                      class="w-8 h-8 bg-white rounded-full flex items-center justify-center"
                    >
                      <svg class="w-5 h-5" :style="{ color: widgetConfig.primaryColor }" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1L9 7V9C9 10.1 9.9 11 11 11V14L13 16L15 14V11C16.1 11 17 10.1 17 9H21Z" />
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-white font-medium">{{ widgetConfig.botName }}</h3>
                      <p class="text-white text-xs opacity-90">En línea</p>
                    </div>
                  </div>
                  <button 
                    @click="chatOpen = false"
                    class="text-white hover:text-gray-200 transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <!-- Messages -->
                <div class="flex-1 p-4 overflow-y-auto">
                  <div class="space-y-3">
                    <!-- Welcome Message -->
                    <div class="flex items-start space-x-2">
                      <div 
                        v-if="widgetConfig.showAvatar"
                        class="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0"
                        :style="{ backgroundColor: widgetConfig.primaryColor }"
                      >
                        <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1L9 7V9C9 10.1 9.9 11 11 11V14L13 16L15 14V11C16.1 11 17 10.1 17 9H21Z" />
                        </svg>
                      </div>
                      <div class="bg-gray-100 rounded-lg px-3 py-2 max-w-xs">
                        <p class="text-sm text-gray-800">{{ widgetConfig.welcomeMessage }}</p>
                      </div>
                    </div>

                    <!-- Sample User Message -->
                    <div class="flex justify-end">
                      <div 
                        class="rounded-lg px-3 py-2 max-w-xs text-white"
                        :style="{ backgroundColor: widgetConfig.primaryColor }"
                      >
                        <p class="text-sm">Hola, necesito ayuda con mi pedido</p>
                      </div>
                    </div>

                    <!-- Sample Bot Response -->
                    <div class="flex items-start space-x-2">
                      <div 
                        v-if="widgetConfig.showAvatar"
                        class="w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0"
                        :style="{ backgroundColor: widgetConfig.primaryColor }"
                      >
                        <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1L9 7V9C9 10.1 9.9 11 11 11V14L13 16L15 14V11C16.1 11 17 10.1 17 9H21Z" />
                        </svg>
                      </div>
                      <div class="bg-gray-100 rounded-lg px-3 py-2 max-w-xs">
                        <p class="text-sm text-gray-800">¡Por supuesto! Estaré encantado de ayudarte con tu pedido. ¿Podrías proporcionarme tu número de pedido?</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Input -->
                <div class="p-4 border-t border-gray-200">
                  <div class="flex space-x-2">
                    <input 
                      type="text" 
                      placeholder="Escribe tu mensaje..."
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                    <button 
                      class="px-3 py-2 rounded-lg text-white transition-colors"
                      :style="{ backgroundColor: widgetConfig.primaryColor }"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Integration Code -->
      <div class="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Código de Integración</h2>
        <p class="text-gray-600 mb-4">Copia y pega este código en tu sitio web para integrar el widget:</p>
        
        <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
          <pre class="text-green-400 text-sm"><code v-html="integrationCode"></code></pre>
        </div>
        
        <button 
          @click="copyCode"
          class="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Copiar Código
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()

const chatOpen = ref(false)

const widgetConfig = ref({
  theme: 'light',
  position: 'bottom-right',
  welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
  botName: 'Asistente Virtual',
  primaryColor: '#2563eb',
  showAvatar: true,
  enableSound: true
})

const integrationCode = computed(() => {
  return `&lt;script&gt;
  (function() {
    var script = document.createElement('script');
    script.src = 'https://widget.versaai.com/widget.js';
    script.setAttribute('data-widget-id', 'your-widget-id');
    script.setAttribute('data-theme', '${widgetConfig.value.theme}');
    script.setAttribute('data-position', '${widgetConfig.value.position}');
    script.setAttribute('data-primary-color', '${widgetConfig.value.primaryColor}');
    script.setAttribute('data-bot-name', '${widgetConfig.value.botName}');
    script.setAttribute('data-welcome-message', '${widgetConfig.value.welcomeMessage}');
    script.setAttribute('data-show-avatar', '${widgetConfig.value.showAvatar}');
    script.setAttribute('data-enable-sound', '${widgetConfig.value.enableSound}');
    document.head.appendChild(script);
  })();
&lt;\/script&gt;`
})

const getWidgetPositionClasses = () => {
  const positions = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4'
  }
  return positions[widgetConfig.value.position] || 'bottom-4 right-4'
}

const getThemeClasses = () => {
  const themes = {
    'light': 'bg-white text-gray-900',
    'dark': 'bg-gray-800 text-white',
    'blue': 'bg-blue-50 text-blue-900'
  }
  return themes[widgetConfig.value.theme] || 'bg-white text-gray-900'
}

const resetConfig = () => {
  widgetConfig.value = {
    theme: 'light',
    position: 'bottom-right',
    welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
    botName: 'Asistente Virtual',
    primaryColor: '#2563eb',
    showAvatar: true,
    enableSound: true
  }
  toast.success('Configuración restablecida')
}

const copyCode = async () => {
  const code = `<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'https://widget.versaai.com/widget.js';
    script.setAttribute('data-widget-id', 'your-widget-id');
    script.setAttribute('data-theme', '${widgetConfig.value.theme}');
    script.setAttribute('data-position', '${widgetConfig.value.position}');
    script.setAttribute('data-primary-color', '${widgetConfig.value.primaryColor}');
    script.setAttribute('data-bot-name', '${widgetConfig.value.botName}');
    script.setAttribute('data-welcome-message', '${widgetConfig.value.welcomeMessage}');
    script.setAttribute('data-show-avatar', '${widgetConfig.value.showAvatar}');
    script.setAttribute('data-enable-sound', '${widgetConfig.value.enableSound}');
    document.head.appendChild(script);
  })();
<\/script>`

  try {
    await navigator.clipboard.writeText(code)
    toast.success('Código copiado al portapapeles')
  } catch (err) {
    toast.error('Error al copiar el código')
  }
}
</script>

<style scoped>
.widget-demo {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style>