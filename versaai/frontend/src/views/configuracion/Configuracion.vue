<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Configuración</h1>
            <p class="mt-2 text-gray-600">Gestiona la configuración de tu plataforma VersaAI</p>
          </div>
          <div class="flex space-x-4">
            <EnhancedButton
              @click="resetToDefaults"
              variant="secondary"
              size="lg"
            >
              <ArrowUturnLeftIcon class="w-5 h-5 mr-2" />
              Restaurar
            </EnhancedButton>
            <EnhancedButton
              @click="saveConfiguration"
              variant="primary"
              size="lg"
              :loading="isSaving"
              :disabled="!hasChanges"
            >
              <CheckIcon class="w-5 h-5 mr-2" />
              Guardar Cambios
            </EnhancedButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white/60 backdrop-blur-sm rounded-2xl p-2 shadow-soft border border-white/20">
        <nav class="flex space-x-2">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300',
              activeTab === tab.id
                ? 'bg-primary-500 text-white shadow-lg'
                : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5 mr-2" />
            {{ tab.name }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Content Area -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <!-- General Settings -->
      <div v-if="activeTab === 'general'" class="space-y-6">
        <EnhancedCard variant="glass" shadow="soft" class="p-6">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Configuración General</h3>
          </template>
          <template #body>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre de la Organización
                </label>
                <input
                  v-model="config.general.organizationName"
                  type="text"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  placeholder="Mi Empresa S.A."
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Zona Horaria
                </label>
                <select
                  v-model="config.general.timezone"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="America/Mexico_City">Ciudad de México (GMT-6)</option>
                  <option value="America/New_York">Nueva York (GMT-5)</option>
                  <option value="Europe/Madrid">Madrid (GMT+1)</option>
                  <option value="Asia/Tokyo">Tokio (GMT+9)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Idioma Principal
                </label>
                <select
                  v-model="config.general.defaultLanguage"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="es">Español</option>
                  <option value="en">English</option>
                  <option value="pt">Português</option>
                  <option value="fr">Français</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Formato de Fecha
                </label>
                <select
                  v-model="config.general.dateFormat"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>
            <div class="mt-6">
              <div class="flex items-center">
                <input
                  id="maintenance-mode"
                  v-model="config.general.maintenanceMode"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label for="maintenance-mode" class="ml-2 block text-sm text-gray-900">
                  Modo de mantenimiento
                </label>
              </div>
              <p class="mt-1 text-sm text-gray-500">Activar para realizar mantenimiento del sistema</p>
            </div>
          </template>
        </EnhancedCard>
      </div>

      <!-- AI Settings -->
      <div v-if="activeTab === 'ai'" class="space-y-6">
        <EnhancedCard variant="glass" shadow="soft" class="p-6">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Configuración de IA</h3>
          </template>
          <template #body>
            <div class="space-y-6 mt-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Proveedor de IA Principal
                </label>
                <select
                  v-model="config.ai.provider"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                >
                  <option value="groq">Groq (Recomendado)</option>
                  <option value="openai">OpenAI</option>
                  <option value="anthropic">Anthropic</option>
                  <option value="local">Modelo Local</option>
                </select>
              </div>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Modelo por Defecto
                  </label>
                  <select
                    v-model="config.ai.defaultModel"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  >
                    <option value="llama-3.1-70b">Llama 3.1 70B</option>
                    <option value="llama-3.1-8b">Llama 3.1 8B</option>
                    <option value="mixtral-8x7b">Mixtral 8x7B</option>
                    <option value="gemma-7b">Gemma 7B</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Temperatura por Defecto: {{ config.ai.defaultTemperature }}
                  </label>
                  <input
                    v-model.number="config.ai.defaultTemperature"
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
              </div>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Máximo de Tokens
                  </label>
                  <input
                    v-model.number="config.ai.maxTokens"
                    type="number"
                    min="50"
                    max="2000"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Timeout (segundos)
                  </label>
                  <input
                    v-model.number="config.ai.timeout"
                    type="number"
                    min="5"
                    max="120"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  />
                </div>
              </div>
              <div class="space-y-4">
                <div class="flex items-center">
                  <input
                    id="enable-rag"
                    v-model="config.ai.enableRAG"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="enable-rag" class="ml-2 block text-sm text-gray-900">
                    Habilitar RAG por defecto
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="enable-memory"
                    v-model="config.ai.enableMemory"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="enable-memory" class="ml-2 block text-sm text-gray-900">
                    Memoria de conversación
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="enable-analytics"
                    v-model="config.ai.enableAnalytics"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="enable-analytics" class="ml-2 block text-sm text-gray-900">
                    Análisis automático de conversaciones
                  </label>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>

      <!-- Security Settings -->
      <div v-if="activeTab === 'security'" class="space-y-6">
        <EnhancedCard variant="glass" shadow="soft" class="p-6">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Configuración de Seguridad</h3>
          </template>
          <template #body>
            <div class="space-y-6 mt-6">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Duración de Sesión (minutos)
                  </label>
                  <input
                    v-model.number="config.security.sessionDuration"
                    type="number"
                    min="15"
                    max="1440"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Intentos de Login Máximos
                  </label>
                  <input
                    v-model.number="config.security.maxLoginAttempts"
                    type="number"
                    min="3"
                    max="10"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  />
                </div>
              </div>
              <div class="space-y-4">
                <div class="flex items-center">
                  <input
                    id="require-2fa"
                    v-model="config.security.require2FA"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="require-2fa" class="ml-2 block text-sm text-gray-900">
                    Requerir autenticación de dos factores
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="password-complexity"
                    v-model="config.security.passwordComplexity"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="password-complexity" class="ml-2 block text-sm text-gray-900">
                    Requerir contraseñas complejas
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="audit-logs"
                    v-model="config.security.auditLogs"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="audit-logs" class="ml-2 block text-sm text-gray-900">
                    Registrar logs de auditoría
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="ip-whitelist"
                    v-model="config.security.ipWhitelist"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="ip-whitelist" class="ml-2 block text-sm text-gray-900">
                    Habilitar lista blanca de IPs
                  </label>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>

      <!-- Notifications Settings -->
      <div v-if="activeTab === 'notifications'" class="space-y-6">
        <EnhancedCard variant="glass" shadow="soft" class="p-6">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Configuración de Notificaciones</h3>
          </template>
          <template #body>
            <div class="space-y-6 mt-6">
              <div class="space-y-4">
                <h4 class="text-md font-medium text-gray-900">Notificaciones por Email</h4>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-900">Nuevas conversaciones</label>
                      <p class="text-sm text-gray-500">Recibir notificación cuando inicie una nueva conversación</p>
                    </div>
                    <input
                      v-model="config.notifications.email.newConversations"
                      type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-900">Errores del sistema</label>
                      <p class="text-sm text-gray-500">Notificar sobre errores críticos del sistema</p>
                    </div>
                    <input
                      v-model="config.notifications.email.systemErrors"
                      type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-900">Reportes semanales</label>
                      <p class="text-sm text-gray-500">Resumen semanal de actividad y métricas</p>
                    </div>
                    <input
                      v-model="config.notifications.email.weeklyReports"
                      type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                </div>
              </div>
              <div class="space-y-4 border-t border-gray-200 pt-6">
                <h4 class="text-md font-medium text-gray-900">Notificaciones Push</h4>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-900">Mensajes urgentes</label>
                      <p class="text-sm text-gray-500">Notificaciones push para mensajes marcados como urgentes</p>
                    </div>
                    <input
                      v-model="config.notifications.push.urgentMessages"
                      type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm font-medium text-gray-900">Actualizaciones del sistema</label>
                      <p class="text-sm text-gray-500">Notificar sobre actualizaciones y nuevas funcionalidades</p>
                    </div>
                    <input
                      v-model="config.notifications.push.systemUpdates"
                      type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                  </div>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>

      <!-- API Settings -->
      <div v-if="activeTab === 'api'" class="space-y-6">
        <EnhancedCard variant="glass" shadow="soft" class="p-6">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900">Configuración de API</h3>
          </template>
          <template #body>
            <div class="space-y-6 mt-6">
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Rate Limit (requests/minuto)
                  </label>
                  <input
                    v-model.number="config.api.rateLimit"
                    type="number"
                    min="10"
                    max="1000"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Versión de API
                  </label>
                  <select
                    v-model="config.api.version"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
                  >
                    <option value="v1">v1 (Actual)</option>
                    <option value="v2">v2 (Beta)</option>
                  </select>
                </div>
              </div>
              <div class="space-y-4">
                <div class="flex items-center">
                  <input
                    id="enable-cors"
                    v-model="config.api.enableCORS"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="enable-cors" class="ml-2 block text-sm text-gray-900">
                    Habilitar CORS
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="require-api-key"
                    v-model="config.api.requireApiKey"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="require-api-key" class="ml-2 block text-sm text-gray-900">
                    Requerir API Key
                  </label>
                </div>
                <div class="flex items-center">
                  <input
                    id="log-requests"
                    v-model="config.api.logRequests"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="log-requests" class="ml-2 block text-sm text-gray-900">
                    Registrar todas las peticiones
                  </label>
                </div>
              </div>
            </div>
          </template>
        </EnhancedCard>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="showMessage" class="fixed bottom-4 right-4 z-50">
      <div :class="[
        'px-6 py-4 rounded-xl shadow-lg transition-all duration-300',
        messageType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <div class="flex items-center">
          <CheckIcon v-if="messageType === 'success'" class="w-5 h-5 mr-2" />
          <ExclamationTriangleIcon v-else class="w-5 h-5 mr-2" />
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import {
  CogIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  BellIcon,
  CodeBracketIcon,
  CheckIcon,
  ArrowUturnLeftIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import EnhancedCard from '@/components/ui/EnhancedCard.vue'
import EnhancedButton from '@/components/ui/EnhancedButton.vue'

// Estado reactivo
const activeTab = ref('general')
const isSaving = ref(false)
const showMessage = ref(false)
const message = ref('')
const messageType = ref('success')
const originalConfig = ref({})

// Tabs de navegación
const tabs = [
  { id: 'general', name: 'General', icon: CogIcon },
  { id: 'ai', name: 'Inteligencia Artificial', icon: CpuChipIcon },
  { id: 'security', name: 'Seguridad', icon: ShieldCheckIcon },
  { id: 'notifications', name: 'Notificaciones', icon: BellIcon },
  { id: 'api', name: 'API', icon: CodeBracketIcon }
]

// Configuración reactiva
const config = reactive({
  general: {
    organizationName: 'VersaAI Enterprise',
    timezone: 'America/Mexico_City',
    defaultLanguage: 'es',
    dateFormat: 'DD/MM/YYYY',
    maintenanceMode: false
  },
  ai: {
    provider: 'groq',
    defaultModel: 'llama-3.1-70b',
    defaultTemperature: 0.7,
    maxTokens: 500,
    timeout: 30,
    enableRAG: true,
    enableMemory: true,
    enableAnalytics: true
  },
  security: {
    sessionDuration: 480,
    maxLoginAttempts: 5,
    require2FA: false,
    passwordComplexity: true,
    auditLogs: true,
    ipWhitelist: false
  },
  notifications: {
    email: {
      newConversations: true,
      systemErrors: true,
      weeklyReports: false
    },
    push: {
      urgentMessages: true,
      systemUpdates: false
    }
  },
  api: {
    rateLimit: 100,
    version: 'v1',
    enableCORS: true,
    requireApiKey: true,
    logRequests: false
  }
})

// Computed properties
const hasChanges = computed(() => {
  return JSON.stringify(config) !== JSON.stringify(originalConfig.value)
})

// Métodos
const saveConfiguration = async () => {
  isSaving.value = true
  try {
    // Simular guardado
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Actualizar configuración original
    originalConfig.value = JSON.parse(JSON.stringify(config))
    
    showSuccessMessage('Configuración guardada exitosamente')
  } catch (error) {
    console.error('Error al guardar configuración:', error)
    showErrorMessage('Error al guardar la configuración')
  } finally {
    isSaving.value = false
  }
}

const resetToDefaults = () => {
  if (confirm('¿Estás seguro de que quieres restaurar la configuración por defecto?')) {
    // Restaurar valores por defecto
    Object.assign(config, {
      general: {
        organizationName: 'VersaAI Enterprise',
        timezone: 'America/Mexico_City',
        defaultLanguage: 'es',
        dateFormat: 'DD/MM/YYYY',
        maintenanceMode: false
      },
      ai: {
        provider: 'groq',
        defaultModel: 'llama-3.1-70b',
        defaultTemperature: 0.7,
        maxTokens: 500,
        timeout: 30,
        enableRAG: true,
        enableMemory: true,
        enableAnalytics: true
      },
      security: {
        sessionDuration: 480,
        maxLoginAttempts: 5,
        require2FA: false,
        passwordComplexity: true,
        auditLogs: true,
        ipWhitelist: false
      },
      notifications: {
        email: {
          newConversations: true,
          systemErrors: true,
          weeklyReports: false
        },
        push: {
          urgentMessages: true,
          systemUpdates: false
        }
      },
      api: {
        rateLimit: 100,
        version: 'v1',
        enableCORS: true,
        requireApiKey: true,
        logRequests: false
      }
    })
    
    showSuccessMessage('Configuración restaurada a valores por defecto')
  }
}

const showSuccessMessage = (msg) => {
  message.value = msg
  messageType.value = 'success'
  showMessage.value = true
  setTimeout(() => {
    showMessage.value = false
  }, 3000)
}

const showErrorMessage = (msg) => {
  message.value = msg
  messageType.value = 'error'
  showMessage.value = true
  setTimeout(() => {
    showMessage.value = false
  }, 3000)
}

// Inicializar configuración original
originalConfig.value = JSON.parse(JSON.stringify(config))
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