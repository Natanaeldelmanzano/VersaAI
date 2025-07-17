<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Configuración de Notificaciones</h3>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Tabs -->
      <div class="mt-4">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="space-y-6">
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Configuración General</h4>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Habilitar notificaciones</label>
                  <p class="text-sm text-gray-500">Recibir todas las notificaciones del sistema</p>
                </div>
                <toggle-switch v-model="settings.general.enabled" />
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Notificaciones de escritorio</label>
                  <p class="text-sm text-gray-500">Mostrar notificaciones en el navegador</p>
                </div>
                <toggle-switch v-model="settings.general.desktop" />
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Sonidos</label>
                  <p class="text-sm text-gray-500">Reproducir sonido al recibir notificaciones</p>
                </div>
                <toggle-switch v-model="settings.general.sound" />
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Modo no molestar</label>
                  <p class="text-sm text-gray-500">Pausar notificaciones temporalmente</p>
                </div>
                <toggle-switch v-model="settings.general.doNotDisturb" />
              </div>
            </div>
          </div>
          
          <div v-if="settings.general.doNotDisturb">
            <h5 class="text-sm font-medium text-gray-700 mb-3">Horario de no molestar</h5>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Desde</label>
                <input
                  v-model="settings.general.quietHours.start"
                  type="time"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Hasta</label>
                <input
                  v-model="settings.general.quietHours.end"
                  type="time"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Email Settings -->
        <div v-if="activeTab === 'email'" class="space-y-6">
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Notificaciones por Email</h4>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Habilitar emails</label>
                  <p class="text-sm text-gray-500">Recibir notificaciones por correo electrónico</p>
                </div>
                <toggle-switch v-model="settings.email.enabled" />
              </div>
              
              <div v-if="settings.email.enabled">
                <label class="block text-sm font-medium text-gray-700 mb-2">Frecuencia de resumen</label>
                <select
                  v-model="settings.email.frequency"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="instant">Instantáneo</option>
                  <option value="hourly">Cada hora</option>
                  <option value="daily">Diario</option>
                  <option value="weekly">Semanal</option>
                </select>
              </div>
              
              <div v-if="settings.email.enabled && settings.email.frequency === 'daily'">
                <label class="block text-sm font-medium text-gray-700 mb-2">Hora de envío diario</label>
                <input
                  v-model="settings.email.dailyTime"
                  type="time"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Categories Settings -->
        <div v-if="activeTab === 'categories'" class="space-y-6">
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Tipos de Notificaciones</h4>
            
            <div class="space-y-4">
              <div
                v-for="category in notificationCategories"
                :key="category.id"
                class="border border-gray-200 rounded-lg p-4"
              >
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-3">
                    <div :class="[
                      'w-8 h-8 rounded-lg flex items-center justify-center',
                      category.color
                    ]">
                      <component :is="category.icon" class="h-4 w-4" />
                    </div>
                    <div>
                      <h5 class="text-sm font-medium text-gray-900">{{ category.name }}</h5>
                      <p class="text-xs text-gray-500">{{ category.description }}</p>
                    </div>
                  </div>
                  <toggle-switch v-model="settings.categories[category.id].enabled" />
                </div>
                
                <div v-if="settings.categories[category.id].enabled" class="ml-11 space-y-3">
                  <div class="flex items-center space-x-6">
                    <label class="flex items-center space-x-2">
                      <input
                        v-model="settings.categories[category.id].inApp"
                        type="checkbox"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span class="text-xs text-gray-700">En la app</span>
                    </label>
                    
                    <label class="flex items-center space-x-2">
                      <input
                        v-model="settings.categories[category.id].email"
                        type="checkbox"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span class="text-xs text-gray-700">Email</span>
                    </label>
                    
                    <label class="flex items-center space-x-2">
                      <input
                        v-model="settings.categories[category.id].desktop"
                        type="checkbox"
                        class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span class="text-xs text-gray-700">Escritorio</span>
                    </label>
                  </div>
                  
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Prioridad mínima</label>
                    <select
                      v-model="settings.categories[category.id].minPriority"
                      class="w-32 border border-gray-300 rounded-md px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="low">Baja</option>
                      <option value="medium">Media</option>
                      <option value="high">Alta</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced Settings -->
        <div v-if="activeTab === 'advanced'" class="space-y-6">
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Configuración Avanzada</h4>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Retención de notificaciones</label>
                <select
                  v-model="settings.advanced.retention"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="7">7 días</option>
                  <option value="30">30 días</option>
                  <option value="90">90 días</option>
                  <option value="365">1 año</option>
                  <option value="-1">Indefinido</option>
                </select>
                <p class="text-xs text-gray-500 mt-1">Tiempo que se mantienen las notificaciones antes de ser eliminadas automáticamente</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Límite de notificaciones</label>
                <input
                  v-model.number="settings.advanced.maxNotifications"
                  type="number"
                  min="10"
                  max="1000"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p class="text-xs text-gray-500 mt-1">Número máximo de notificaciones a mantener</p>
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Agrupar notificaciones similares</label>
                  <p class="text-sm text-gray-500">Combinar notificaciones del mismo tipo</p>
                </div>
                <toggle-switch v-model="settings.advanced.groupSimilar" />
              </div>
              
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-sm font-medium text-gray-700">Marcar como leídas automáticamente</label>
                  <p class="text-sm text-gray-500">Marcar notificaciones como leídas después de un tiempo</p>
                </div>
                <toggle-switch v-model="settings.advanced.autoMarkRead" />
              </div>
              
              <div v-if="settings.advanced.autoMarkRead">
                <label class="block text-sm font-medium text-gray-700 mb-2">Tiempo para marcar como leída (minutos)</label>
                <input
                  v-model.number="settings.advanced.autoMarkReadTime"
                  type="number"
                  min="1"
                  max="1440"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
          
          <div class="border-t border-gray-200 pt-6">
            <h5 class="text-sm font-medium text-gray-900 mb-4">Acciones de Limpieza</h5>
            <div class="space-y-3">
              <button
                @click="clearAllNotifications"
                class="w-full bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm font-medium"
              >
                Eliminar todas las notificaciones
              </button>
              <button
                @click="clearReadNotifications"
                class="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm font-medium"
              >
                Eliminar notificaciones leídas
              </button>
              <button
                @click="resetSettings"
                class="w-full bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 text-sm font-medium"
              >
                Restaurar configuración por defecto
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-end space-x-3 mt-8 pt-4 border-t border-gray-200">
        <button
          @click="$emit('close')"
          class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          @click="saveSettings"
          :disabled="saving"
          class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  XMarkIcon,
  ComputerDesktopIcon,
  ChatBubbleLeftRightIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
import ToggleSwitch from '@/components/ui/ToggleSwitch.vue'

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const activeTab = ref('general')
const saving = ref(false)

const tabs = [
  { id: 'general', name: 'General' },
  { id: 'email', name: 'Email' },
  { id: 'categories', name: 'Categorías' },
  { id: 'advanced', name: 'Avanzado' }
]

const notificationCategories = [
  {
    id: 'system',
    name: 'Sistema',
    description: 'Actualizaciones y mantenimiento del sistema',
    icon: ComputerDesktopIcon,
    color: 'bg-blue-100 text-blue-600'
  },
  {
    id: 'chat',
    name: 'Conversaciones',
    description: 'Nuevas conversaciones y mensajes',
    icon: ChatBubbleLeftRightIcon,
    color: 'bg-green-100 text-green-600'
  },
  {
    id: 'billing',
    name: 'Facturación',
    description: 'Pagos, facturas y suscripciones',
    icon: CreditCardIcon,
    color: 'bg-yellow-100 text-yellow-600'
  },
  {
    id: 'security',
    name: 'Seguridad',
    description: 'Alertas de seguridad y acceso',
    icon: ShieldCheckIcon,
    color: 'bg-red-100 text-red-600'
  },
  {
    id: 'update',
    name: 'Actualizaciones',
    description: 'Nuevas funcionalidades y mejoras',
    icon: ArrowPathIcon,
    color: 'bg-purple-100 text-purple-600'
  },
  {
    id: 'team',
    name: 'Equipo',
    description: 'Actividad del equipo y colaboradores',
    icon: UserGroupIcon,
    color: 'bg-indigo-100 text-indigo-600'
  }
]

const settings = reactive({
  general: {
    enabled: true,
    desktop: true,
    sound: true,
    doNotDisturb: false,
    quietHours: {
      start: '22:00',
      end: '08:00'
    }
  },
  email: {
    enabled: true,
    frequency: 'daily',
    dailyTime: '09:00'
  },
  categories: {
    system: {
      enabled: true,
      inApp: true,
      email: true,
      desktop: true,
      minPriority: 'medium'
    },
    chat: {
      enabled: true,
      inApp: true,
      email: false,
      desktop: true,
      minPriority: 'low'
    },
    billing: {
      enabled: true,
      inApp: true,
      email: true,
      desktop: true,
      minPriority: 'high'
    },
    security: {
      enabled: true,
      inApp: true,
      email: true,
      desktop: true,
      minPriority: 'medium'
    },
    update: {
      enabled: true,
      inApp: true,
      email: false,
      desktop: false,
      minPriority: 'low'
    },
    team: {
      enabled: true,
      inApp: true,
      email: false,
      desktop: false,
      minPriority: 'medium'
    }
  },
  advanced: {
    retention: 30,
    maxNotifications: 500,
    groupSimilar: true,
    autoMarkRead: false,
    autoMarkReadTime: 60
  }
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const saveSettings = async () => {
  saving.value = true
  
  try {
    // TODO: Save settings to API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    emit('save', settings)
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Error al guardar la configuración')
  } finally {
    saving.value = false
  }
}

const clearAllNotifications = () => {
  if (confirm('¿Estás seguro de que quieres eliminar todas las notificaciones? Esta acción no se puede deshacer.')) {
    // TODO: Implement clear all notifications
    console.log('Clear all notifications')
  }
}

const clearReadNotifications = () => {
  if (confirm('¿Estás seguro de que quieres eliminar todas las notificaciones leídas?')) {
    // TODO: Implement clear read notifications
    console.log('Clear read notifications')
  }
}

const resetSettings = () => {
  if (confirm('¿Estás seguro de que quieres restaurar la configuración por defecto? Se perderán todos los cambios.')) {
    // TODO: Reset to default settings
    console.log('Reset settings')
    location.reload()
  }
}

// Initialize
onMounted(() => {
  // TODO: Load settings from API
  console.log('NotificationSettings mounted')
})
</script>