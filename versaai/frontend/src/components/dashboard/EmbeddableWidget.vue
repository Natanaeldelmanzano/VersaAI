<template>
  <div class="embeddable-widget">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Widget Embebible</h2>
        <p class="text-gray-600 mt-2">Configura y personaliza el widget de chat para tu sitio web</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="previewWidget"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <EyeIcon class="w-4 h-4 mr-2" />
          Vista Previa
        </button>
        
        <button
          @click="generateCode"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <CodeBracketIcon class="w-4 h-4 mr-2" />
          Generar Código
        </button>
      </div>
    </div>

    <!-- Widget Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Widgets Activos</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ widgetStats.active }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+12%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <ChatBubbleLeftRightIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Conversaciones/día</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ widgetStats.conversations }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+8%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <ChartBarIcon class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Tasa de Conversión</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ widgetStats.conversionRate }}%</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+2.1%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <ArrowTrendingUpIcon class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Satisfacción</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ widgetStats.satisfaction }}/5</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+0.3</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
            <StarIcon class="w-6 h-6 text-orange-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Widget Configuration -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Configuration Panel -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Configuración del Widget</h3>
        </div>
        <div class="p-6 space-y-6">
          <!-- Basic Settings -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-4">Configuración Básica</h4>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Widget</label>
                <input
                  v-model="widgetConfig.name"
                  type="text"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="Mi Widget de Chat"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Mensaje de Bienvenida</label>
                <textarea
                  v-model="widgetConfig.welcomeMessage"
                  rows="3"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  placeholder="¡Hola! ¿En qué puedo ayudarte hoy?"
                ></textarea>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Posición</label>
                <select
                  v-model="widgetConfig.position"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="bottom-right">Abajo Derecha</option>
                  <option value="bottom-left">Abajo Izquierda</option>
                  <option value="top-right">Arriba Derecha</option>
                  <option value="top-left">Arriba Izquierda</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Appearance Settings -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-4">Apariencia</h4>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Color Principal</label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="widgetConfig.primaryColor"
                    type="color"
                    class="w-12 h-10 rounded-lg border border-gray-300 cursor-pointer"
                  />
                  <input
                    v-model="widgetConfig.primaryColor"
                    type="text"
                    class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="#3B82F6"
                  />
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Color Secundario</label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="widgetConfig.secondaryColor"
                    type="color"
                    class="w-12 h-10 rounded-lg border border-gray-300 cursor-pointer"
                  />
                  <input
                    v-model="widgetConfig.secondaryColor"
                    type="text"
                    class="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    placeholder="#F3F4F6"
                  />
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tamaño</label>
                <select
                  v-model="widgetConfig.size"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="small">Pequeño</option>
                  <option value="medium">Mediano</option>
                  <option value="large">Grande</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Estilo de Burbuja</label>
                <select
                  v-model="widgetConfig.bubbleStyle"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="rounded">Redondeado</option>
                  <option value="square">Cuadrado</option>
                  <option value="pill">Píldora</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Behavior Settings -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-4">Comportamiento</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Auto-abrir después de</label>
                <div class="flex items-center space-x-2">
                  <input
                    v-model="widgetConfig.autoOpenDelay"
                    type="number"
                    min="0"
                    max="60"
                    class="w-20 rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  />
                  <span class="text-sm text-gray-500">segundos</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Mostrar en móviles</label>
                <button
                  @click="widgetConfig.showOnMobile = !widgetConfig.showOnMobile"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    widgetConfig.showOnMobile ? 'bg-primary-600' : 'bg-gray-200'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      widgetConfig.showOnMobile ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Sonido de notificación</label>
                <button
                  @click="widgetConfig.soundEnabled = !widgetConfig.soundEnabled"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    widgetConfig.soundEnabled ? 'bg-primary-600' : 'bg-gray-200'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      widgetConfig.soundEnabled ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>
              
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-700">Recopilar email</label>
                <button
                  @click="widgetConfig.collectEmail = !widgetConfig.collectEmail"
                  :class="[
                    'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                    widgetConfig.collectEmail ? 'bg-primary-600' : 'bg-gray-200'
                  ]"
                >
                  <span
                    :class="[
                      'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                      widgetConfig.collectEmail ? 'translate-x-6' : 'translate-x-1'
                    ]"
                  ></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Widget Preview -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">Vista Previa</h3>
        </div>
        <div class="p-6">
          <div class="bg-gray-100 rounded-lg p-8 min-h-96 relative overflow-hidden">
            <!-- Simulated Website -->
            <div class="bg-white rounded-lg shadow-sm p-6 mb-4">
              <div class="h-4 bg-gray-300 rounded mb-2"></div>
              <div class="h-4 bg-gray-200 rounded mb-2 w-3/4"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
            
            <!-- Widget Preview -->
            <div 
              :class="[
                'absolute transition-all duration-300',
                getWidgetPositionClass(),
                getWidgetSizeClass()
              ]"
            >
              <!-- Chat Bubble -->
              <div 
                v-if="!isWidgetOpen"
                @click="isWidgetOpen = true"
                :class="[
                  'cursor-pointer shadow-lg flex items-center justify-center text-white font-medium transition-transform hover:scale-105',
                  getBubbleStyleClass()
                ]"
                :style="{ backgroundColor: widgetConfig.primaryColor }"
              >
                <ChatBubbleLeftRightIcon class="w-6 h-6" />
              </div>
              
              <!-- Chat Window -->
              <div 
                v-if="isWidgetOpen"
                class="bg-white rounded-lg shadow-xl border border-gray-200 w-80 h-96 flex flex-col"
              >
                <!-- Header -->
                <div 
                  class="px-4 py-3 rounded-t-lg flex items-center justify-between text-white"
                  :style="{ backgroundColor: widgetConfig.primaryColor }"
                >
                  <div class="flex items-center space-x-2">
                    <div class="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                      <ChatBubbleLeftRightIcon class="w-4 h-4" />
                    </div>
                    <span class="font-medium">{{ widgetConfig.name }}</span>
                  </div>
                  <button
                    @click="isWidgetOpen = false"
                    class="text-white hover:text-gray-200"
                  >
                    <XMarkIcon class="w-5 h-5" />
                  </button>
                </div>
                
                <!-- Messages -->
                <div class="flex-1 p-4 space-y-3 overflow-y-auto">
                  <div class="flex items-start space-x-2">
                    <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                      <ChatBubbleLeftRightIcon class="w-4 h-4 text-gray-600" />
                    </div>
                    <div 
                      class="max-w-xs px-3 py-2 rounded-lg text-sm"
                      :style="{ backgroundColor: widgetConfig.secondaryColor }"
                    >
                      {{ widgetConfig.welcomeMessage }}
                    </div>
                  </div>
                  
                  <div class="flex justify-end">
                    <div 
                      class="max-w-xs px-3 py-2 rounded-lg text-sm text-white"
                      :style="{ backgroundColor: widgetConfig.primaryColor }"
                    >
                      ¡Hola! Me gustaría saber más sobre sus servicios.
                    </div>
                  </div>
                </div>
                
                <!-- Input -->
                <div class="p-4 border-t border-gray-200">
                  <div class="flex items-center space-x-2">
                    <input
                      type="text"
                      placeholder="Escribe tu mensaje..."
                      class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                    <button 
                      class="p-2 rounded-lg text-white"
                      :style="{ backgroundColor: widgetConfig.primaryColor }"
                    >
                      <PaperAirplaneIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Generated Code -->
    <div v-if="generatedCode" class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Código de Integración</h3>
          <button
            @click="copyCode"
            class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <ClipboardIcon class="w-4 h-4 mr-2" />
            Copiar
          </button>
        </div>
      </div>
      <div class="p-6">
        <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
          <pre class="text-sm text-gray-300"><code>{{ generatedCode }}</code></pre>
        </div>
        
        <div class="mt-4 p-4 bg-blue-50 rounded-lg">
          <h4 class="text-sm font-medium text-blue-900 mb-2">Instrucciones de Instalación:</h4>
          <ol class="text-sm text-blue-800 space-y-1">
            <li>1. Copia el código JavaScript generado</li>
            <li>2. Pégalo antes del cierre de la etiqueta &lt;/body&gt; en tu sitio web</li>
            <li>3. El widget aparecerá automáticamente en tu sitio</li>
            <li>4. Personaliza la configuración desde este panel cuando lo necesites</li>
          </ol>
        </div>
      </div>
    </div>

    <!-- Widget Analytics -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Analíticas del Widget</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Usage Chart -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-4">Uso del Widget (Últimos 7 días)</h4>
            <div class="h-64">
              <WidgetChart 
                :data="widgetUsageData" 
                :loading="isLoading"
                type="line"
                :options="widgetChartOptions"
              />
            </div>
          </div>
          
          <!-- Conversion Funnel -->
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-4">Embudo de Conversión</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span class="text-sm font-medium text-gray-700">Visitantes únicos</span>
                <span class="text-sm font-bold text-gray-900">12,450</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <span class="text-sm font-medium text-gray-700">Interacciones con widget</span>
                <span class="text-sm font-bold text-blue-900">3,120 (25.1%)</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <span class="text-sm font-medium text-gray-700">Conversaciones iniciadas</span>
                <span class="text-sm font-bold text-green-900">1,890 (60.6%)</span>
              </div>
              <div class="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                <span class="text-sm font-medium text-gray-700">Conversiones</span>
                <span class="text-sm font-bold text-purple-900">456 (24.1%)</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import {
  EyeIcon,
  CodeBracketIcon,
  ArrowUpIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon,
  StarIcon,
  XMarkIcon,
  PaperAirplaneIcon,
  ClipboardIcon
} from '@heroicons/vue/24/outline'
import WidgetChart from './charts/WidgetChart.vue'

// Store
const dashboardStore = useDashboardStore()

// State
const isLoading = ref(false)
const isWidgetOpen = ref(false)
const generatedCode = ref('')

// Widget Configuration
const widgetConfig = ref({
  name: 'Asistente VersaAI',
  welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
  position: 'bottom-right',
  primaryColor: '#3B82F6',
  secondaryColor: '#F3F4F6',
  size: 'medium',
  bubbleStyle: 'rounded',
  autoOpenDelay: 0,
  showOnMobile: true,
  soundEnabled: true,
  collectEmail: false
})

// Mock data
const widgetStats = ref({
  active: 24,
  conversations: 1247,
  conversionRate: 24.3,
  satisfaction: 4.7
})

const widgetUsageData = computed(() => ({
  labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  datasets: [
    {
      label: 'Interacciones',
      data: [120, 190, 300, 500, 200, 300, 450],
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    },
    {
      label: 'Conversaciones',
      data: [80, 120, 180, 300, 150, 200, 280],
      borderColor: '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4
    }
  ]
}))

const widgetChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

// Computed
const getWidgetPositionClass = () => {
  const positions = {
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4'
  }
  return positions[widgetConfig.value.position] || 'bottom-4 right-4'
}

const getWidgetSizeClass = () => {
  const sizes = {
    small: 'w-12 h-12',
    medium: 'w-14 h-14',
    large: 'w-16 h-16'
  }
  return sizes[widgetConfig.value.size] || 'w-14 h-14'
}

const getBubbleStyleClass = () => {
  const styles = {
    rounded: 'rounded-full',
    square: 'rounded-lg',
    pill: 'rounded-full'
  }
  return styles[widgetConfig.value.bubbleStyle] || 'rounded-full'
}

// Methods
const previewWidget = () => {
  isWidgetOpen.value = !isWidgetOpen.value
}

const generateCode = () => {
  const config = JSON.stringify(widgetConfig.value, null, 2)
  
  generatedCode.value = `<!-- VersaAI Widget -->
<script>
  (function() {
    var config = ${config};
    
    var script = document.createElement('script');
    script.src = 'https://cdn.versaai.com/widget/v1/widget.js';
    script.async = true;
    script.onload = function() {
      VersaAI.init({
        apiKey: 'YOUR_API_KEY',
        config: config
      });
    };
    
    document.head.appendChild(script);
  })();
</script>
<!-- End VersaAI Widget -->`
}

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(generatedCode.value)
    // Show success message
    console.log('Código copiado al portapapeles')
  } catch (error) {
    console.error('Error al copiar código:', error)
  }
}

// Lifecycle
onMounted(() => {
  generateCode()
})
</script>

<style scoped>
.embeddable-widget {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>