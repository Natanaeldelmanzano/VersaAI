<template>
  <div class="customization-system">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold text-gray-900">Sistema de Personalización</h2>
            <p class="text-sm text-gray-600 mt-1">Configura la apariencia y comportamiento de tu plataforma</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="resetToDefaults"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <ArrowPathIcon class="h-4 w-4 mr-2" />
              Restaurar
            </button>
            <button
              @click="previewChanges"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <EyeIcon class="h-4 w-4 mr-2" />
              Vista Previa
            </button>
            <button
              @click="saveCustomization"
              :disabled="saving"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <CheckIcon v-if="!saving" class="h-4 w-4 mr-2" />
              <ArrowPathIcon v-else class="h-4 w-4 mr-2 animate-spin" />
              {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="px-6">
        <nav class="flex space-x-8" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            <component :is="tab.icon" class="h-5 w-5 mr-2 inline" />
            {{ tab.name }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Settings Panel -->
      <div class="lg:col-span-2">
        <!-- Theme & Branding -->
        <div v-if="activeTab === 'theme'" class="space-y-6">
          <!-- Brand Colors -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Colores de Marca</h3>
            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Color Primario</label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="customization.theme.primaryColor"
                    type="color"
                    class="h-10 w-20 rounded border border-gray-300 cursor-pointer"
                  />
                  <input
                    v-model="customization.theme.primaryColor"
                    type="text"
                    class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="#3B82F6"
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Color Secundario</label>
                <div class="flex items-center space-x-3">
                  <input
                    v-model="customization.theme.secondaryColor"
                    type="color"
                    class="h-10 w-20 rounded border border-gray-300 cursor-pointer"
                  />
                  <input
                    v-model="customization.theme.secondaryColor"
                    type="text"
                    class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    placeholder="#6B7280"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Logo & Branding -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Logo y Marca</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Logo URL</label>
                <input
                  v-model="customization.branding.logoUrl"
                  type="url"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="https://ejemplo.com/logo.png"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de la Empresa</label>
                <input
                  v-model="customization.branding.companyName"
                  type="text"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="Mi Empresa"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Favicon URL</label>
                <input
                  v-model="customization.branding.faviconUrl"
                  type="url"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="https://ejemplo.com/favicon.ico"
                />
              </div>
            </div>
          </div>

          <!-- Typography -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Tipografía</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Fuente Principal</label>
                <select
                  v-model="customization.theme.fontFamily"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="Inter">Inter</option>
                  <option value="Roboto">Roboto</option>
                  <option value="Open Sans">Open Sans</option>
                  <option value="Lato">Lato</option>
                  <option value="Poppins">Poppins</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tamaño Base</label>
                <select
                  v-model="customization.theme.fontSize"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="14px">Pequeño (14px)</option>
                  <option value="16px">Mediano (16px)</option>
                  <option value="18px">Grande (18px)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Layout Settings -->
        <div v-if="activeTab === 'layout'" class="space-y-6">
          <!-- Sidebar Configuration -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Sidebar</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Sidebar Colapsible</label>
                  <p class="text-sm text-gray-500">Permitir colapsar el menú lateral</p>
                </div>
                <toggle-switch v-model="customization.layout.sidebarCollapsible" />
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Sidebar Fijo</label>
                  <p class="text-sm text-gray-500">Mantener el sidebar fijo al hacer scroll</p>
                </div>
                <toggle-switch v-model="customization.layout.sidebarFixed" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ancho del Sidebar</label>
                <select
                  v-model="customization.layout.sidebarWidth"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="240px">Estrecho (240px)</option>
                  <option value="280px">Mediano (280px)</option>
                  <option value="320px">Ancho (320px)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Header Configuration -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Header</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Header Fijo</label>
                  <p class="text-sm text-gray-500">Mantener el header fijo al hacer scroll</p>
                </div>
                <toggle-switch v-model="customization.layout.headerFixed" />
              </div>
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Mostrar Breadcrumbs</label>
                  <p class="text-sm text-gray-500">Mostrar navegación de migas de pan</p>
                </div>
                <toggle-switch v-model="customization.layout.showBreadcrumbs" />
              </div>
            </div>
          </div>

          <!-- Content Layout -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Diseño de Contenido</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Ancho Máximo</label>
                <select
                  v-model="customization.layout.maxWidth"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="1200px">Estándar (1200px)</option>
                  <option value="1400px">Amplio (1400px)</option>
                  <option value="100%">Completo (100%)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Espaciado</label>
                <select
                  v-model="customization.layout.spacing"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="compact">Compacto</option>
                  <option value="normal">Normal</option>
                  <option value="spacious">Espacioso</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Widget Settings -->
        <div v-if="activeTab === 'widgets'" class="space-y-6">
          <!-- Available Widgets -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Widgets Disponibles</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="widget in availableWidgets"
                :key="widget.id"
                class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <component :is="widget.icon" class="h-6 w-6 text-gray-600" />
                    <div>
                      <h4 class="text-sm font-medium text-gray-900">{{ widget.name }}</h4>
                      <p class="text-xs text-gray-500">{{ widget.description }}</p>
                    </div>
                  </div>
                  <toggle-switch v-model="widget.enabled" />
                </div>
              </div>
            </div>
          </div>

          <!-- Widget Configuration -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Widgets</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Auto-refresh</label>
                  <p class="text-sm text-gray-500">Actualizar widgets automáticamente</p>
                </div>
                <toggle-switch v-model="customization.widgets.autoRefresh" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Intervalo de Actualización</label>
                <select
                  v-model="customization.widgets.refreshInterval"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  :disabled="!customization.widgets.autoRefresh"
                >
                  <option value="30">30 segundos</option>
                  <option value="60">1 minuto</option>
                  <option value="300">5 minutos</option>
                  <option value="900">15 minutos</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced Settings -->
        <div v-if="activeTab === 'advanced'" class="space-y-6">
          <!-- Custom CSS -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">CSS Personalizado</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Habilitar CSS Personalizado</label>
                  <p class="text-sm text-gray-500">Permite agregar estilos CSS personalizados</p>
                </div>
                <toggle-switch v-model="customization.advanced.enableCustomCSS" />
              </div>
              <div v-if="customization.advanced.enableCustomCSS">
                <label class="block text-sm font-medium text-gray-700 mb-2">CSS Code</label>
                <textarea
                  v-model="customization.advanced.customCSS"
                  rows="10"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 font-mono text-sm"
                  placeholder="/* Agrega tu CSS personalizado aquí */
.custom-class {
  color: #3B82F6;
}"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- JavaScript Hooks -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Hooks de JavaScript</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Habilitar Hooks</label>
                  <p class="text-sm text-gray-500">Permite ejecutar JavaScript personalizado</p>
                </div>
                <toggle-switch v-model="customization.advanced.enableJSHooks" />
              </div>
              <div v-if="customization.advanced.enableJSHooks">
                <label class="block text-sm font-medium text-gray-700 mb-2">JavaScript Code</label>
                <textarea
                  v-model="customization.advanced.jsHooks"
                  rows="8"
                  class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 font-mono text-sm"
                  placeholder="// Agrega tu JavaScript personalizado aquí
window.customFunction = function() {
  console.log('Hook ejecutado');
};"
                ></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Preview Panel -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Vista Previa</h3>
          <div class="border border-gray-200 rounded-lg overflow-hidden">
            <div 
              class="h-64 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center"
              :style="previewStyles"
            >
              <div class="text-center">
                <div class="w-16 h-16 bg-white rounded-lg shadow-lg flex items-center justify-center mx-auto mb-3">
                  <component :is="customization.branding.logoUrl ? 'img' : 'BuildingOfficeIcon'" 
                    :src="customization.branding.logoUrl"
                    class="h-8 w-8 text-gray-600" 
                  />
                </div>
                <h4 class="text-lg font-semibold text-gray-900">{{ customization.branding.companyName || 'Mi Empresa' }}</h4>
                <p class="text-sm text-gray-600">Vista previa del tema</p>
              </div>
            </div>
          </div>
          
          <!-- Quick Actions -->
          <div class="mt-4 space-y-2">
            <button
              @click="applyPreset('modern')"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
            >
              🎨 Tema Moderno
            </button>
            <button
              @click="applyPreset('classic')"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
            >
              📚 Tema Clásico
            </button>
            <button
              @click="applyPreset('dark')"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
            >
              🌙 Tema Oscuro
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import {
  ArrowPathIcon,
  EyeIcon,
  CheckIcon,
  PaintBrushIcon,
  Squares2X2Icon,
  PuzzlePieceIcon,
  CogIcon,
  ChartBarIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  BellIcon,
  BuildingOfficeIcon
} from '@heroicons/vue/24/outline'
import ToggleSwitch from '../ui/ToggleSwitch.vue'

// Reactive data
const activeTab = ref('theme')
const saving = ref(false)

const tabs = [
  { id: 'theme', name: 'Tema y Marca', icon: PaintBrushIcon },
  { id: 'layout', name: 'Diseño', icon: Squares2X2Icon },
  { id: 'widgets', name: 'Widgets', icon: PuzzlePieceIcon },
  { id: 'advanced', name: 'Avanzado', icon: CogIcon }
]

const customization = reactive({
  theme: {
    primaryColor: '#3B82F6',
    secondaryColor: '#6B7280',
    fontFamily: 'Inter',
    fontSize: '16px'
  },
  branding: {
    logoUrl: '',
    companyName: 'VersaAI',
    faviconUrl: ''
  },
  layout: {
    sidebarCollapsible: true,
    sidebarFixed: true,
    sidebarWidth: '280px',
    headerFixed: true,
    showBreadcrumbs: true,
    maxWidth: '1200px',
    spacing: 'normal'
  },
  widgets: {
    autoRefresh: true,
    refreshInterval: 300
  },
  advanced: {
    enableCustomCSS: false,
    customCSS: '',
    enableJSHooks: false,
    jsHooks: ''
  }
})

const availableWidgets = reactive([
  {
    id: 'analytics',
    name: 'Analytics',
    description: 'Métricas y estadísticas',
    icon: ChartBarIcon,
    enabled: true
  },
  {
    id: 'conversations',
    name: 'Conversaciones',
    description: 'Chat en tiempo real',
    icon: ChatBubbleLeftRightIcon,
    enabled: true
  },
  {
    id: 'users',
    name: 'Usuarios',
    description: 'Gestión de usuarios',
    icon: UserGroupIcon,
    enabled: true
  },
  {
    id: 'notifications',
    name: 'Notificaciones',
    description: 'Centro de notificaciones',
    icon: BellIcon,
    enabled: false
  }
])

// Computed
const previewStyles = computed(() => {
  return {
    backgroundColor: customization.theme.primaryColor + '20',
    fontFamily: customization.theme.fontFamily,
    fontSize: customization.theme.fontSize
  }
})

// Methods
const saveCustomization = async () => {
  saving.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Apply customization to document
    applyCustomization()
    
    console.log('Customization saved:', customization)
  } catch (error) {
    console.error('Error saving customization:', error)
  } finally {
    saving.value = false
  }
}

const resetToDefaults = () => {
  Object.assign(customization.theme, {
    primaryColor: '#3B82F6',
    secondaryColor: '#6B7280',
    fontFamily: 'Inter',
    fontSize: '16px'
  })
  
  Object.assign(customization.branding, {
    logoUrl: '',
    companyName: 'VersaAI',
    faviconUrl: ''
  })
  
  Object.assign(customization.layout, {
    sidebarCollapsible: true,
    sidebarFixed: true,
    sidebarWidth: '280px',
    headerFixed: true,
    showBreadcrumbs: true,
    maxWidth: '1200px',
    spacing: 'normal'
  })
}

const previewChanges = () => {
  applyCustomization()
}

const applyCustomization = () => {
  // Apply CSS variables
  const root = document.documentElement
  root.style.setProperty('--primary-color', customization.theme.primaryColor)
  root.style.setProperty('--secondary-color', customization.theme.secondaryColor)
  root.style.setProperty('--font-family', customization.theme.fontFamily)
  root.style.setProperty('--font-size', customization.theme.fontSize)
  
  // Apply custom CSS if enabled
  if (customization.advanced.enableCustomCSS && customization.advanced.customCSS) {
    let styleElement = document.getElementById('custom-styles')
    if (!styleElement) {
      styleElement = document.createElement('style')
      styleElement.id = 'custom-styles'
      document.head.appendChild(styleElement)
    }
    styleElement.textContent = customization.advanced.customCSS
  }
  
  // Execute JS hooks if enabled
  if (customization.advanced.enableJSHooks && customization.advanced.jsHooks) {
    try {
      eval(customization.advanced.jsHooks)
    } catch (error) {
      console.error('Error executing JS hooks:', error)
    }
  }
}

const applyPreset = (preset) => {
  switch (preset) {
    case 'modern':
      Object.assign(customization.theme, {
        primaryColor: '#6366F1',
        secondaryColor: '#8B5CF6',
        fontFamily: 'Poppins',
        fontSize: '16px'
      })
      break
    case 'classic':
      Object.assign(customization.theme, {
        primaryColor: '#1F2937',
        secondaryColor: '#6B7280',
        fontFamily: 'Roboto',
        fontSize: '14px'
      })
      break
    case 'dark':
      Object.assign(customization.theme, {
        primaryColor: '#10B981',
        secondaryColor: '#374151',
        fontFamily: 'Inter',
        fontSize: '16px'
      })
      break
  }
}
</script>

<style scoped>
.customization-system {
  @apply space-y-6;
}
</style>