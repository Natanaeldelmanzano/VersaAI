<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Configuración</h1>
        <p class="text-gray-600">Gestiona las preferencias y configuraciones del sistema</p>
      </div>
      <button
        @click="saveAllSettings"
        :disabled="saving"
        class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 disabled:opacity-50"
      >
        {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
      </button>
    </div>

    <!-- Settings Tabs -->
    <div class="bg-white rounded-lg shadow">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8 px-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === tab.id
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <component :is="tab.icon" class="h-5 w-5 inline mr-2" />
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- General Settings -->
      <div v-if="activeTab === 'general'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración General</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de la Aplicación</label>
              <input
                id="app-name"
                name="app-name"
                v-model="settings.general.appName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">URL Base</label>
              <input
                id="base-url"
                name="base-url"
                v-model="settings.general.baseUrl"
                type="url"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Idioma por Defecto</label>
              <select
                id="default-language"
                name="default-language"
                v-model="settings.general.defaultLanguage"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="es">Español</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Zona Horaria</label>
              <select
                id="timezone"
                name="timezone"
                v-model="settings.general.timezone"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="America/Mexico_City">Ciudad de México (GMT-6)</option>
                <option value="America/New_York">Nueva York (GMT-5)</option>
                <option value="Europe/Madrid">Madrid (GMT+1)</option>
                <option value="UTC">UTC (GMT+0)</option>
              </select>
            </div>
          </div>
          
          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Descripción de la Aplicación</label>
            <textarea
              id="app-description"
              name="app-description"
              v-model="settings.general.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Descripción breve de la aplicación..."
            ></textarea>
          </div>
          
          <div class="flex items-center space-x-4 mt-6">
            <label class="flex items-center">
              <input
                v-model="settings.general.maintenanceMode"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Modo de Mantenimiento</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="settings.general.allowRegistration"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Permitir Registro de Usuarios</span>
            </label>
          </div>
        </div>
      </div>

      <!-- AI Settings -->
      <div v-if="activeTab === 'ai'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de IA</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Proveedor de IA</label>
              <select
                id="ai-provider"
                name="ai-provider"
                v-model="settings.ai.provider"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="google">Google AI</option>
                <option value="local">Modelo Local</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Modelo por Defecto</label>
              <select
                id="ai-default-model"
                name="ai-default-model"
                v-model="settings.ai.defaultModel"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="claude-3">Claude 3</option>
                <option value="gemini-pro">Gemini Pro</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Temperatura</label>
              <input
                id="ai-temperature"
                name="ai-temperature"
                v-model.number="settings.ai.temperature"
                type="range"
                min="0"
                max="2"
                step="0.1"
                class="w-full"
              >
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>Conservador (0)</span>
                <span>{{ settings.ai.temperature }}</span>
                <span>Creativo (2)</span>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Máximo de Tokens</label>
              <input
                id="ai-max-tokens"
                name="ai-max-tokens"
                v-model.number="settings.ai.maxTokens"
                type="number"
                min="100"
                max="4000"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
          </div>
          
          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Prompt del Sistema</label>
            <textarea
              id="ai-system-prompt"
              name="ai-system-prompt"
              v-model="settings.ai.systemPrompt"
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="Instrucciones base para el comportamiento de la IA..."
            ></textarea>
          </div>
          
          <div class="flex items-center space-x-4 mt-6">
            <label class="flex items-center">
              <input
                v-model="settings.ai.enableRAG"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Habilitar RAG</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="settings.ai.enableMemory"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Memoria de Conversación</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Security Settings -->
      <div v-if="activeTab === 'security'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Seguridad</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Duración de Sesión (minutos)</label>
              <input
                id="session-duration"
                name="session-duration"
                v-model.number="settings.security.sessionDuration"
                type="number"
                min="15"
                max="1440"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Intentos de Login Máximos</label>
              <input
                id="max-login-attempts"
                name="max-login-attempts"
                v-model.number="settings.security.maxLoginAttempts"
                type="number"
                min="3"
                max="10"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Longitud Mínima de Contraseña</label>
              <input
                id="min-password-length"
                name="min-password-length"
                v-model.number="settings.security.minPasswordLength"
                type="number"
                min="6"
                max="20"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tiempo de Bloqueo (minutos)</label>
              <input
                id="lockout-duration"
                name="lockout-duration"
                v-model.number="settings.security.lockoutDuration"
                type="number"
                min="5"
                max="60"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
          </div>
          
          <div class="flex items-center space-x-4 mt-6">
            <label class="flex items-center">
              <input
                v-model="settings.security.requireTwoFactor"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Requerir Autenticación de Dos Factores</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="settings.security.enableAuditLog"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Habilitar Log de Auditoría</span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="settings.security.requirePasswordChange"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Forzar Cambio de Contraseña Periódico</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Email Settings -->
      <div v-if="activeTab === 'email'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Email</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Servidor SMTP</label>
              <input
                id="smtp-host"
                name="smtp-host"
                v-model="settings.email.smtpHost"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="smtp.gmail.com"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Puerto SMTP</label>
              <input
                id="smtp-port"
                name="smtp-port"
                v-model.number="settings.email.smtpPort"
                type="number"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="587"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Usuario SMTP</label>
              <input
                id="smtp-user"
                name="smtp-user"
                v-model="settings.email.smtpUser"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="usuario@ejemplo.com"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña SMTP</label>
              <input
                id="smtp-password"
                name="smtp-password"
                v-model="settings.email.smtpPassword"
                type="password"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="••••••••"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email Remitente</label>
              <input
                id="from-email"
                name="from-email"
                v-model="settings.email.fromEmail"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="noreply@ejemplo.com"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre Remitente</label>
              <input
                id="from-name"
                name="from-name"
                v-model="settings.email.fromName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="VersaAI"
              >
            </div>
          </div>
          
          <div class="flex items-center space-x-4 mt-6">
            <label class="flex items-center">
              <input
                v-model="settings.email.enableSSL"
                type="checkbox"
                class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
              >
              <span class="ml-2 text-sm text-gray-700">Habilitar SSL/TLS</span>
            </label>
            
            <button
              @click="testEmailConnection"
              :disabled="testingEmail"
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 disabled:opacity-50"
            >
              {{ testingEmail ? 'Probando...' : 'Probar Conexión' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Storage Settings -->
      <div v-if="activeTab === 'storage'" class="p-6 space-y-6">
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Almacenamiento</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Proveedor de Almacenamiento</label>
              <select
                id="storage-provider"
                name="storage-provider"
                v-model="settings.storage.provider"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="local">Almacenamiento Local</option>
                <option value="s3">Amazon S3</option>
                <option value="gcs">Google Cloud Storage</option>
                <option value="azure">Azure Blob Storage</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tamaño Máximo de Archivo (MB)</label>
              <input
                id="max-file-size"
                name="max-file-size"
                v-model.number="settings.storage.maxFileSize"
                type="number"
                min="1"
                max="100"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
            </div>
            
            <div v-if="settings.storage.provider !== 'local'">
              <label class="block text-sm font-medium text-gray-700 mb-2">Bucket/Contenedor</label>
              <input
                id="storage-bucket"
                name="storage-bucket"
                v-model="settings.storage.bucket"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="mi-bucket"
              >
            </div>
            
            <div v-if="settings.storage.provider !== 'local'">
              <label class="block text-sm font-medium text-gray-700 mb-2">Región</label>
              <input
                id="storage-region"
                name="storage-region"
                v-model="settings.storage.region"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="us-east-1"
              >
            </div>
          </div>
          
          <div class="mt-6">
            <h4 class="text-md font-medium text-gray-900 mb-3">Tipos de Archivo Permitidos</h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <label v-for="fileType in fileTypes" :key="fileType.value" class="flex items-center">
                <input
                  v-model="settings.storage.allowedFileTypes"
                  :value="fileType.value"
                  type="checkbox"
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50"
                >
                <span class="ml-2 text-sm text-gray-700">{{ fileType.label }}</span>
              </label>
            </div>
          </div>
          
          <div class="mt-6">
            <h4 class="text-md font-medium text-gray-900 mb-3">Uso de Almacenamiento</h4>
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm text-gray-600">Espacio Utilizado</span>
                <span class="text-sm font-medium text-gray-900">{{ storageUsage.used }} / {{ storageUsage.total }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-primary-600 h-2 rounded-full"
                  :style="{ width: `${storageUsage.percentage}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  CogIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  EnvelopeIcon,
  CloudIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'
import api from '@/api'

const toast = useToast()

const saving = ref(false)
const testingEmail = ref(false)
const activeTab = ref('general')

const tabs = [
  { id: 'general', name: 'General', icon: CogIcon },
  { id: 'ai', name: 'IA', icon: CpuChipIcon },
  { id: 'security', name: 'Seguridad', icon: ShieldCheckIcon },
  { id: 'email', name: 'Email', icon: EnvelopeIcon },
  { id: 'storage', name: 'Almacenamiento', icon: CloudIcon }
]

const fileTypes = [
  { value: 'pdf', label: 'PDF' },
  { value: 'doc', label: 'Word' },
  { value: 'txt', label: 'Texto' },
  { value: 'md', label: 'Markdown' },
  { value: 'csv', label: 'CSV' },
  { value: 'json', label: 'JSON' },
  { value: 'xml', label: 'XML' },
  { value: 'html', label: 'HTML' }
]

const settings = ref({
  general: {
    appName: 'VersaAI',
    baseUrl: 'https://versaai.com',
    defaultLanguage: 'es',
    timezone: 'America/Mexico_City',
    description: '',
    maintenanceMode: false,
    allowRegistration: true
  },
  ai: {
    provider: 'openai',
    defaultModel: 'gpt-4',
    temperature: 0.7,
    maxTokens: 2000,
    systemPrompt: '',
    enableRAG: true,
    enableMemory: true
  },
  security: {
    sessionDuration: 480,
    maxLoginAttempts: 5,
    minPasswordLength: 8,
    lockoutDuration: 15,
    requireTwoFactor: false,
    enableAuditLog: true,
    requirePasswordChange: false
  },
  email: {
    smtpHost: '',
    smtpPort: 587,
    smtpUser: '',
    smtpPassword: '',
    fromEmail: '',
    fromName: 'VersaAI',
    enableSSL: true
  },
  storage: {
    provider: 'local',
    maxFileSize: 10,
    bucket: '',
    region: '',
    allowedFileTypes: ['pdf', 'doc', 'txt', 'md']
  }
})

const storageUsage = ref({
  used: '2.3 GB',
  total: '10 GB',
  percentage: 23
})

const fetchSettings = async () => {
  try {
    const response = await api.get('/settings')
    settings.value = { ...settings.value, ...response.data }
  } catch (error) {
    console.error('Error fetching settings:', error)
    toast.error('Error al cargar la configuración')
  }
}

const fetchStorageUsage = async () => {
  try {
    const response = await api.get('/settings/storage-usage')
    storageUsage.value = response.data
  } catch (error) {
    console.error('Error fetching storage usage:', error)
  }
}

const saveAllSettings = async () => {
  saving.value = true
  try {
    await api.put('/settings', settings.value)
    toast.success('Configuración guardada correctamente')
  } catch (error) {
    console.error('Error saving settings:', error)
    toast.error('Error al guardar la configuración')
  } finally {
    saving.value = false
  }
}

const testEmailConnection = async () => {
  testingEmail.value = true
  try {
    await api.post('/settings/test-email', settings.value.email)
    toast.success('Conexión de email exitosa')
  } catch (error) {
    console.error('Error testing email:', error)
    toast.error('Error en la conexión de email')
  } finally {
    testingEmail.value = false
  }
}

onMounted(() => {
  fetchSettings()
  fetchStorageUsage()
})
</script>