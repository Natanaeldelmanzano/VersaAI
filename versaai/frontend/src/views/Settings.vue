<template>
  <div class="settings-page">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Configuración</h1>
            <p class="text-gray-600 mt-1">Gestiona la configuración del sistema y preferencias</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="exportSettings"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Exportar
            </button>
            <label class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 cursor-pointer">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Importar
              <input
                type="file"
                accept=".json"
                @change="handleImportFile"
                class="hidden"
              />
            </label>
            <button
              @click="saveAllSettings"
              :disabled="isSaving || !hasUnsavedChanges || hasValidationErrors"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isSaving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ isSaving ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
            <button
              @click="resetSettings"
              :disabled="isSaving"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Restablecer
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Settings Navigation -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6">
        <nav class="flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-4 px-1 border-b-2 font-medium text-sm',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            <div class="flex items-center">
              <component :is="tab.icon" class="w-5 h-5 mr-2" />
              {{ tab.name }}
            </div>
          </button>
        </nav>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex items-center justify-center bg-gray-50">
      <div class="text-center">
        <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-600">Cargando configuración...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 flex items-center justify-center bg-gray-50">
      <div class="text-center">
        <svg class="h-12 w-12 text-red-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <p class="text-red-600 mb-4">Error al cargar la configuración</p>
        <button
          @click="loadSettings"
          class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Reintentar
        </button>
      </div>
    </div>

    <!-- Settings Content -->
    <div v-else class="flex-1 overflow-y-auto bg-gray-50">
      <div class="max-w-4xl mx-auto py-6 px-6">
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Configuración General</h3>
              <p class="text-sm text-gray-600 mt-1">Configuración básica del sistema</p>
            </div>
            <div class="px-6 py-4 space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="company-name" class="block text-sm font-medium text-gray-700">Nombre de la empresa</label>
                  <input
                    id="company-name"
                    v-model="settings.general.companyName"
                    type="text"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
                <div>
                  <label for="company-website" class="block text-sm font-medium text-gray-700">Sitio web</label>
                  <input
                    id="company-website"
                    v-model="settings.general.companyWebsite"
                    type="url"
                    placeholder="https://ejemplo.com"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
              </div>
              
              <div>
                <label for="company-description" class="block text-sm font-medium text-gray-700">Descripción</label>
                <textarea
                  id="company-description"
                  v-model="settings.general.companyDescription"
                  rows="3"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  @input="markAsChanged"
                ></textarea>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="timezone" class="block text-sm font-medium text-gray-700">Zona horaria</label>
                  <select
                    id="timezone"
                    v-model="settings.general.timezone"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @change="markAsChanged"
                  >
                    <option value="America/Mexico_City">Ciudad de México (GMT-6)</option>
                    <option value="America/New_York">Nueva York (GMT-5)</option>
                    <option value="Europe/Madrid">Madrid (GMT+1)</option>
                    <option value="Europe/London">Londres (GMT+0)</option>
                    <option value="Asia/Tokyo">Tokio (GMT+9)</option>
                  </select>
                </div>
                <div>
                  <label for="language" class="block text-sm font-medium text-gray-700">Idioma</label>
                  <select
                    id="language"
                    v-model="settings.general.language"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @change="markAsChanged"
                  >
                    <option value="es">Español</option>
                    <option value="en">English</option>
                    <option value="fr">Français</option>
                    <option value="de">Deutsch</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Settings -->
        <div v-if="activeTab === 'ai'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Configuración de IA</h3>
              <p class="text-sm text-gray-600 mt-1">Configuración de modelos y parámetros de IA</p>
            </div>
            <div class="px-6 py-4 space-y-6">
              <div>
                <label for="default-model" class="block text-sm font-medium text-gray-700">Modelo por defecto</label>
                <select
                  id="default-model"
                  v-model="settings.ai.defaultModel"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  @change="markAsChanged"
                >
                  <option value="llama3-8b-8192">Llama 3 8B</option>
                  <option value="llama3-70b-8192">Llama 3 70B</option>
                  <option value="mixtral-8x7b-32768">Mixtral 8x7B</option>
                  <option value="gemma-7b-it">Gemma 7B</option>
                </select>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="temperature" class="block text-sm font-medium text-gray-700">
                    Temperatura: {{ settings.ai.temperature }}
                  </label>
                  <input
                    id="temperature"
                    v-model.number="settings.ai.temperature"
                    type="range"
                    min="0"
                    max="2"
                    step="0.1"
                    class="mt-1 block w-full"
                    @input="markAsChanged"
                  >
                  <div class="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Conservador</span>
                    <span>Creativo</span>
                  </div>
                </div>
                <div>
                  <label for="max-tokens" class="block text-sm font-medium text-gray-700">Tokens máximos</label>
                  <input
                    id="max-tokens"
                    v-model.number="settings.ai.maxTokens"
                    type="number"
                    min="100"
                    max="8192"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
              </div>
              
              <div>
                <label for="system-prompt" class="block text-sm font-medium text-gray-700">Prompt del sistema</label>
                <textarea
                  id="system-prompt"
                  v-model="settings.ai.systemPrompt"
                  rows="4"
                  placeholder="Eres un asistente útil y amigable..."
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  @input="markAsChanged"
                ></textarea>
              </div>
              
              <div class="flex items-center">
                <input
                  id="enable-rag"
                  v-model="settings.ai.enableRAG"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  @change="markAsChanged"
                >
                <label for="enable-rag" class="ml-2 block text-sm text-gray-900">
                  Habilitar RAG (Retrieval-Augmented Generation)
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Security Settings -->
        <div v-if="activeTab === 'security'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Configuración de Seguridad</h3>
              <p class="text-sm text-gray-600 mt-1">Configuración de autenticación y seguridad</p>
            </div>
            <div class="px-6 py-4 space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="session-timeout" class="block text-sm font-medium text-gray-700">Tiempo de sesión (minutos)</label>
                  <input
                    id="session-timeout"
                    v-model.number="settings.security.sessionTimeout"
                    type="number"
                    min="15"
                    max="1440"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
                <div>
                  <label for="max-login-attempts" class="block text-sm font-medium text-gray-700">Intentos máximos de login</label>
                  <input
                    id="max-login-attempts"
                    v-model.number="settings.security.maxLoginAttempts"
                    type="number"
                    min="3"
                    max="10"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
              </div>
              
              <div class="space-y-4">
                <div class="flex items-center">
                  <input
                    id="require-2fa"
                    v-model="settings.security.require2FA"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    @change="markAsChanged"
                  >
                  <label for="require-2fa" class="ml-2 block text-sm text-gray-900">
                    Requerir autenticación de dos factores (2FA)
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="force-password-change"
                    v-model="settings.security.forcePasswordChange"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    @change="markAsChanged"
                  >
                  <label for="force-password-change" class="ml-2 block text-sm text-gray-900">
                    Forzar cambio de contraseña cada 90 días
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="enable-audit-log"
                    v-model="settings.security.enableAuditLog"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    @change="markAsChanged"
                  >
                  <label for="enable-audit-log" class="ml-2 block text-sm text-gray-900">
                    Habilitar registro de auditoría
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications Settings -->
        <div v-if="activeTab === 'notifications'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Configuración de Notificaciones</h3>
              <p class="text-sm text-gray-600 mt-1">Configuración de alertas y notificaciones</p>
            </div>
            <div class="px-6 py-4 space-y-6">
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-4">Notificaciones por Email</h4>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm text-gray-900">Nuevos usuarios registrados</label>
                      <p class="text-xs text-gray-500">Recibir notificación cuando se registre un nuevo usuario</p>
                    </div>
                    <input
                      v-model="settings.notifications.email.newUsers"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      @change="markAsChanged"
                    >
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm text-gray-900">Errores del sistema</label>
                      <p class="text-xs text-gray-500">Recibir notificación cuando ocurran errores críticos</p>
                    </div>
                    <input
                      v-model="settings.notifications.email.systemErrors"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      @change="markAsChanged"
                    >
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm text-gray-900">Reportes semanales</label>
                      <p class="text-xs text-gray-500">Recibir resumen semanal de actividad</p>
                    </div>
                    <input
                      v-model="settings.notifications.email.weeklyReports"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      @change="markAsChanged"
                    >
                  </div>
                </div>
              </div>
              
              <div>
                <h4 class="text-sm font-medium text-gray-900 mb-4">Notificaciones Push</h4>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm text-gray-900">Conversaciones nuevas</label>
                      <p class="text-xs text-gray-500">Notificar cuando lleguen nuevas conversaciones</p>
                    </div>
                    <input
                      v-model="settings.notifications.push.newConversations"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      @change="markAsChanged"
                    >
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <div>
                      <label class="text-sm text-gray-900">Actualizaciones del sistema</label>
                      <p class="text-xs text-gray-500">Notificar sobre actualizaciones disponibles</p>
                    </div>
                    <input
                      v-model="settings.notifications.push.systemUpdates"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      @change="markAsChanged"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- API Settings -->
        <div v-if="activeTab === 'api'" class="space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Configuración de API</h3>
              <p class="text-sm text-gray-600 mt-1">Configuración de claves y límites de API</p>
            </div>
            <div class="px-6 py-4 space-y-6">
              <div>
                <label for="groq-api-key" class="block text-sm font-medium text-gray-700">Clave API de Groq</label>
                <div class="mt-1 relative">
                  <input
                    id="groq-api-key"
                    v-model="settings.api.groqApiKey"
                    :type="showApiKey ? 'text' : 'password'"
                    placeholder="gsk_..."
                    class="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                  <button
                    type="button"
                    @click="showApiKey = !showApiKey"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center"
                  >
                    <svg v-if="showApiKey" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                    </svg>
                    <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="rate-limit" class="block text-sm font-medium text-gray-700">Límite de requests por minuto</label>
                  <input
                    id="rate-limit"
                    v-model.number="settings.api.rateLimit"
                    type="number"
                    min="10"
                    max="1000"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
                <div>
                  <label for="timeout" class="block text-sm font-medium text-gray-700">Timeout (segundos)</label>
                  <input
                    id="timeout"
                    v-model.number="settings.api.timeout"
                    type="number"
                    min="5"
                    max="300"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    @input="markAsChanged"
                  >
                </div>
              </div>
              
              <div class="flex items-center">
                <input
                  id="enable-api-logging"
                  v-model="settings.api.enableLogging"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  @change="markAsChanged"
                >
                <label for="enable-api-logging" class="ml-2 block text-sm text-gray-900">
                  Habilitar logging de API
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Import Confirmation Modal -->
    <div v-if="showImportModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100">
            <svg class="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 mt-4">Confirmar Importación</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              ¿Estás seguro de que quieres importar esta configuración? Esto sobrescribirá la configuración actual.
            </p>
          </div>
          <div class="items-center px-4 py-3">
            <button
              @click="confirmImport"
              class="px-4 py-2 bg-blue-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300 mb-2"
            >
              Confirmar
            </button>
            <button
              @click="cancelImport"
              class="px-4 py-2 bg-gray-300 text-gray-800 text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useSettings } from '@/composables/useSettings'

// Icons
const CogIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  `
}

const CpuChipIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
    </svg>
  `
}

const ShieldCheckIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
    </svg>
  `
}

const BellIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
    </svg>
  `
}

const CodeBracketIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
    </svg>
  `
}

export default {
  name: 'Settings',
  components: {
    CogIcon,
    CpuChipIcon,
    ShieldCheckIcon,
    BellIcon,
    CodeBracketIcon
  },
  setup() {
    const toast = useToast()
    
    // Use settings composable
    const {
      loading,
      error,
      saving,
      generalSettings,
      aiSettings,
      notificationSettings,
      securitySettings,
      apiSettings,
      availableLanguages,
      availableTimezones,
      availableModels,
      loadSettings: loadSettingsAPI,
      saveSettings: saveSettingsAPI,
      resetSettings: resetSettingsAPI,
      exportSettings: exportSettingsAPI,
      importSettings,
      validateSettings
    } = useSettings()
    
    // Local state
    const activeTab = ref('general')
    const showApiKey = ref(false)
    const showImportModal = ref(false)
    const importFile = ref(null)
    
    // Tabs
    const tabs = [
      { id: 'general', name: 'General', icon: 'CogIcon' },
      { id: 'ai', name: 'IA', icon: 'CpuChipIcon' },
      { id: 'security', name: 'Seguridad', icon: 'ShieldCheckIcon' },
      { id: 'notifications', name: 'Notificaciones', icon: 'BellIcon' },
      { id: 'api', name: 'API', icon: 'CodeBracketIcon' }
    ]
    
    // Computed properties
    const settings = computed(() => ({
      general: generalSettings.value,
      ai: aiSettings.value,
      security: securitySettings.value,
      notifications: notificationSettings.value,
      api: apiSettings.value
    }))
    
    const isSaving = computed(() => saving.value)
    const hasUnsavedChanges = computed(() => {
      // Check if any settings have been modified
      return Object.keys(settings.value).some(key => {
        const current = settings.value[key]
        const original = settings.value[key] // This would need to track original values
        return JSON.stringify(current) !== JSON.stringify(original)
      })
    })
    
    const currentSettings = computed(() => {
      switch (activeTab.value) {
        case 'general': return generalSettings.value
        case 'ai': return aiSettings.value
        case 'notifications': return notificationSettings.value
        case 'security': return securitySettings.value
        case 'api': return apiSettings.value
        default: return {}
      }
    })
    
    const hasValidationErrors = computed(() => {
      const errors = validateSettings(activeTab.value, currentSettings.value)
      return errors.length > 0
    })
    
    // Methods
    const loadSettings = async () => {
      try {
        await loadSettingsAPI()
        toast.success('Configuración cargada')
      } catch (error) {
        console.error('Error loading settings:', error)
        toast.error('Error al cargar la configuración')
      }
    }
    
    const saveAllSettings = async () => {
      try {
        await saveSettingsAPI('all')
        toast.success('Configuración guardada exitosamente')
      } catch (error) {
        console.error('Error saving settings:', error)
        toast.error('Error al guardar la configuración')
      }
    }
    
    const resetSettings = async () => {
      if (confirm('¿Estás seguro de que quieres restablecer todos los cambios?')) {
        try {
          await resetSettingsAPI(activeTab.value)
          toast.info('Configuración restablecida')
        } catch (error) {
          console.error('Error resetting settings:', error)
          toast.error('Error al restablecer la configuración')
        }
      }
    }
    
    const exportSettings = async () => {
      try {
        await exportSettingsAPI()
        toast.success('Configuración exportada')
      } catch (error) {
        console.error('Error exporting settings:', error)
        toast.error('Error al exportar la configuración')
      }
    }
    
    const handleImportFile = (event) => {
      const file = event.target.files[0]
      if (file && file.type === 'application/json') {
        importFile.value = file
        showImportModal.value = true
      } else {
        toast.error('Por favor selecciona un archivo JSON válido')
      }
    }
    
    const confirmImport = async () => {
      if (importFile.value) {
        try {
          await importSettings(importFile.value)
          showImportModal.value = false
          importFile.value = null
          toast.success('Configuración importada exitosamente')
        } catch (error) {
          console.error('Error importing settings:', error)
          toast.error('Error al importar la configuración')
        }
      }
    }
    
    const cancelImport = () => {
      showImportModal.value = false
      importFile.value = null
    }
    
    const markAsChanged = () => {
      // This would be handled by the composable
      // when settings are modified
    }
    
    // Lifecycle
    onMounted(async () => {
      await loadSettings()
    })
    
    return {
      // State
      activeTab,
      isSaving,
      hasUnsavedChanges,
      showApiKey,
      showImportModal,
      settings,
      tabs,
      loading,
      error,
      availableLanguages,
      availableTimezones,
      availableModels,
      hasValidationErrors,
      
      // Methods
      saveAllSettings,
      resetSettings,
      exportSettings,
      handleImportFile,
      confirmImport,
      cancelImport,
      markAsChanged
    }
  }
}
</script>

<style scoped>
.settings-page {
  @apply h-full flex flex-col;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Range input styling */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}
</style>