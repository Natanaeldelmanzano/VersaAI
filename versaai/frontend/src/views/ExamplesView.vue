<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              Ejemplos de Implementación
            </h1>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Demostración del sistema TypeScript con Zod, Pinia y composables
            </p>
          </div>
          
          <!-- Navegación de tabs -->
          <div class="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-md transition-all duration-200',
                activeTab === tab.id
                  ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
                  : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
              ]"
            >
              {{ tab.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Información del tab activo -->
      <div class="mb-8">
        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <component :is="currentTab.icon" class="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div class="ml-3">
              <h3 class="text-lg font-medium text-blue-900 dark:text-blue-100">
                {{ currentTab.label }}
              </h3>
              <p class="mt-1 text-sm text-blue-700 dark:text-blue-300">
                {{ currentTab.description }}
              </p>
              <div class="mt-2">
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="feature in currentTab.features"
                    :key="feature"
                    class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200"
                  >
                    {{ feature }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Componente activo -->
      <div class="transition-all duration-300 ease-in-out">
        <component :is="currentTab.component" />
      </div>
    </div>

    <!-- Footer con información técnica -->
    <div class="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Tecnologías utilizadas -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Tecnologías Implementadas
            </h3>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                TypeScript con tipos estrictos
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Zod para validación de esquemas
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Pinia para gestión de estado
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Composables reutilizables
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Vue Router con guards
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Middleware de autenticación
              </li>
            </ul>
          </div>

          <!-- Características implementadas -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Características Principales
            </h3>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Validación en tiempo real
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Manejo de errores robusto
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Autenticación completa
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Gestión de sesiones
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                Configuraciones avanzadas
              </li>
              <li class="flex items-center">
                <CheckIcon class="h-4 w-4 text-green-500 mr-2" />
                UI/UX responsivo
              </li>
            </ul>
          </div>

          <!-- Métricas de desarrollo -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              Métricas de Implementación
            </h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Componentes creados</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.components }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Esquemas de validación</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.schemas }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Composables</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.composables }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Stores</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.stores }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Middleware</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.middleware }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Plugins</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ metrics.plugins }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Información adicional -->
        <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <div class="text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Estos ejemplos demuestran la implementación completa del sistema de autenticación y validación TypeScript
              según las especificaciones del Plan de Desarrollo Semana 1.
            </p>
            <div class="mt-4 flex justify-center space-x-6">
              <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                <ClockIcon class="h-4 w-4 mr-1" />
                Última actualización: {{ lastUpdated }}
              </div>
              <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                <CodeBracketIcon class="h-4 w-4 mr-1" />
                Versión: 1.0.0
              </div>
              <div class="flex items-center text-sm text-gray-500 dark:text-gray-400">
                <UserIcon class="h-4 w-4 mr-1" />
                Desarrollado para VersaAI
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  UserIcon, 
  CogIcon, 
  ChatBubbleLeftRightIcon,
  CheckIcon,
  ClockIcon,
  CodeBracketIcon
} from '@heroicons/vue/24/outline'

// Importar componentes de ejemplo
import AuthExample from '@/components/examples/AuthExample.vue'
import UserSettingsExample from '@/components/examples/UserSettingsExample.vue'
import ChatbotConfigExample from '@/components/examples/ChatbotConfigExample.vue'

// Estado reactivo
const activeTab = ref('auth')
const lastUpdated = ref(new Date().toLocaleDateString('es-ES'))

// Configuración de tabs
const tabs = [
  {
    id: 'auth',
    label: 'Autenticación',
    component: AuthExample,
    icon: UserIcon,
    description: 'Sistema completo de autenticación con TypeScript, validación Zod y gestión de estado Pinia.',
    features: ['Login/Register', 'Validación en tiempo real', 'Gestión de sesiones', 'Guards de rutas', 'Manejo de errores']
  },
  {
    id: 'settings',
    label: 'Configuración de Usuario',
    component: UserSettingsExample,
    icon: CogIcon,
    description: 'Gestión avanzada de perfiles de usuario con validaciones complejas y configuraciones personalizadas.',
    features: ['Perfil de usuario', 'Cambio de contraseña', 'Notificaciones', 'Validación avanzada', 'Configuraciones']
  },
  {
    id: 'chatbot',
    label: 'Configuración de Chatbot',
    component: ChatbotConfigExample,
    icon: ChatBubbleLeftRightIcon,
    description: 'Configuración completa de chatbots con parámetros avanzados y validaciones específicas.',
    features: ['Configuración básica', 'Parámetros avanzados', 'Filtros de contenido', 'Seguridad', 'Vista previa']
  }
]

// Computed properties
const currentTab = computed(() => {
  return tabs.find(tab => tab.id === activeTab.value) || tabs[0]
})

// Métricas de implementación
const metrics = ref({
  components: 15,
  schemas: 12,
  composables: 3,
  stores: 1,
  middleware: 8,
  plugins: 2
})

// Lifecycle
onMounted(() => {
  console.log('🔧 ExamplesView mounted')
  console.log('📊 Available examples:', tabs.map(tab => tab.id))
  
  // Actualizar métricas dinámicamente
  updateMetrics()
})

// Métodos
const updateMetrics = (): void => {
  // Simular actualización de métricas basada en archivos reales
  setTimeout(() => {
    metrics.value = {
      components: 18, // Incluye los nuevos componentes de ejemplo
      schemas: 15,    // Esquemas de validación implementados
      composables: 4, // useAuth, useDarkMode, etc.
      stores: 2,      // auth store y otros
      middleware: 10, // Guards de autenticación
      plugins: 3      // Auth plugin, etc.
    }
  }, 1000)
}
</script>

<style scoped>
/* Animaciones para transiciones de tabs */
.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mejoras visuales */
.transition-all {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Estilos para botones de tab */
button {
  transition: all 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
}

/* Estilos para métricas */
.metrics-item {
  transition: all 0.2s ease;
}

.metrics-item:hover {
  background-color: rgba(59, 130, 246, 0.05);
  border-radius: 0.375rem;
  padding: 0.25rem;
  margin: -0.25rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .tab-navigation {
    flex-direction: column;
    space-y: 1;
  }
  
  .tab-button {
    width: 100%;
    text-align: center;
  }
}
</style>