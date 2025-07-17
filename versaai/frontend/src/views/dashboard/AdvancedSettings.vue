<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Configuración Avanzada</h1>
        <p class="text-gray-600 mt-1">Gestiona configuraciones técnicas y avanzadas del sistema</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button
          @click="exportSettings"
          class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2"
        >
          <ArrowDownTrayIcon class="h-4 w-4" />
          <span>Exportar</span>
        </button>
        <button
          @click="showImportModal = true"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
        >
          <ArrowUpTrayIcon class="h-4 w-4" />
          <span>Importar</span>
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="mb-6">
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
            <component :is="tab.icon" class="h-4 w-4 mr-2 inline" />
            {{ tab.name }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="space-y-6">
      <!-- API Configuration -->
      <div v-if="activeTab === 'api'" class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de API</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Rate Limiting</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Habilitar rate limiting</span>
                  <toggle-switch v-model="settings.api.rateLimiting.enabled" />
                </div>
                <div v-if="settings.api.rateLimiting.enabled">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Requests por minuto</label>
                  <input
                    v-model.number="settings.api.rateLimiting.requestsPerMinute"
                    type="number"
                    min="1"
                    max="10000"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">CORS Configuration</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Allowed Origins</label>
                  <textarea
                    v-model="settings.api.cors.allowedOrigins"
                    rows="3"
                    placeholder="https://example.com\nhttps://app.example.com"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  ></textarea>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Allow credentials</span>
                  <toggle-switch v-model="settings.api.cors.allowCredentials" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Cache</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Redis Cache</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Habilitar cache</span>
                  <toggle-switch v-model="settings.api.cache.enabled" />
                </div>
                <div v-if="settings.api.cache.enabled">
                  <label class="block text-xs font-medium text-gray-700 mb-1">TTL por defecto (segundos)</label>
                  <input
                    v-model.number="settings.api.cache.defaultTTL"
                    type="number"
                    min="1"
                    max="86400"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Cache Strategies</label>
              <div class="space-y-2">
                <label class="flex items-center space-x-2">
                  <input
                    v-model="settings.api.cache.strategies"
                    type="checkbox"
                    value="conversations"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">Conversaciones</span>
                </label>
                <label class="flex items-center space-x-2">
                  <input
                    v-model="settings.api.cache.strategies"
                    type="checkbox"
                    value="chatbots"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">Chatbots</span>
                </label>
                <label class="flex items-center space-x-2">
                  <input
                    v-model="settings.api.cache.strategies"
                    type="checkbox"
                    value="analytics"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">Analytics</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Database Configuration -->
      <div v-if="activeTab === 'database'" class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Base de Datos</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Connection Pool</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Pool Size</label>
                  <input
                    v-model.number="settings.database.poolSize"
                    type="number"
                    min="1"
                    max="100"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Max Overflow</label>
                  <input
                    v-model.number="settings.database.maxOverflow"
                    type="number"
                    min="0"
                    max="50"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Query Optimization</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Query logging</span>
                  <toggle-switch v-model="settings.database.queryLogging" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Slow query detection</span>
                  <toggle-switch v-model="settings.database.slowQueryDetection" />
                </div>
                <div v-if="settings.database.slowQueryDetection">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Slow query threshold (ms)</label>
                  <input
                    v-model.number="settings.database.slowQueryThreshold"
                    type="number"
                    min="100"
                    max="10000"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Backup y Mantenimiento</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Backup Automático</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Habilitar backup automático</span>
                  <toggle-switch v-model="settings.database.autoBackup.enabled" />
                </div>
                <div v-if="settings.database.autoBackup.enabled">
                  <label class="block text-xs font-medium text-gray-700 mb-1">Frecuencia</label>
                  <select
                    v-model="settings.database.autoBackup.frequency"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="hourly">Cada hora</option>
                    <option value="daily">Diario</option>
                    <option value="weekly">Semanal</option>
                    <option value="monthly">Mensual</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Acciones de Mantenimiento</label>
              <div class="space-y-2">
                <button
                  @click="runDatabaseMaintenance"
                  class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm font-medium"
                >
                  Ejecutar mantenimiento
                </button>
                <button
                  @click="createBackup"
                  class="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 text-sm font-medium"
                >
                  Crear backup manual
                </button>
                <button
                  @click="showBackupHistory = true"
                  class="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm font-medium"
                >
                  Ver historial de backups
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Security Configuration -->
      <div v-if="activeTab === 'security'" class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Seguridad</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Autenticación</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">JWT Token TTL (horas)</label>
                  <input
                    v-model.number="settings.security.jwt.ttl"
                    type="number"
                    min="1"
                    max="168"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Refresh token rotation</span>
                  <toggle-switch v-model="settings.security.jwt.refreshRotation" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Two-factor authentication</span>
                  <toggle-switch v-model="settings.security.twoFactor.enabled" />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Password Policy</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Longitud mínima</label>
                  <input
                    v-model.number="settings.security.password.minLength"
                    type="number"
                    min="6"
                    max="50"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Requerir mayúsculas</span>
                  <toggle-switch v-model="settings.security.password.requireUppercase" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Requerir números</span>
                  <toggle-switch v-model="settings.security.password.requireNumbers" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Requerir símbolos</span>
                  <toggle-switch v-model="settings.security.password.requireSymbols" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Monitoreo de Seguridad</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Detección de Amenazas</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Detección de fuerza bruta</span>
                  <toggle-switch v-model="settings.security.threatDetection.bruteForce" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Detección de anomalías</span>
                  <toggle-switch v-model="settings.security.threatDetection.anomalies" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Geo-blocking</span>
                  <toggle-switch v-model="settings.security.threatDetection.geoBlocking" />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Logging de Seguridad</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Log de autenticación</span>
                  <toggle-switch v-model="settings.security.logging.authentication" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Log de acceso a API</span>
                  <toggle-switch v-model="settings.security.logging.apiAccess" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Log de cambios de configuración</span>
                  <toggle-switch v-model="settings.security.logging.configChanges" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Configuration -->
      <div v-if="activeTab === 'performance'" class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración de Performance</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Límites de Recursos</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Max workers</label>
                  <input
                    v-model.number="settings.performance.maxWorkers"
                    type="number"
                    min="1"
                    max="32"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Request timeout (segundos)</label>
                  <input
                    v-model.number="settings.performance.requestTimeout"
                    type="number"
                    min="1"
                    max="300"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Max file size (MB)</label>
                  <input
                    v-model.number="settings.performance.maxFileSize"
                    type="number"
                    min="1"
                    max="1000"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Optimizaciones</label>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Compresión gzip</span>
                  <toggle-switch v-model="settings.performance.gzipCompression" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Lazy loading</span>
                  <toggle-switch v-model="settings.performance.lazyLoading" />
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">CDN para assets</span>
                  <toggle-switch v-model="settings.performance.cdnAssets" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Monitoreo de Performance</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ performanceMetrics.responseTime }}ms</div>
              <div class="text-sm text-gray-600">Tiempo de respuesta promedio</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ performanceMetrics.throughput }}</div>
              <div class="text-sm text-gray-600">Requests por segundo</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-yellow-600">{{ performanceMetrics.memoryUsage }}%</div>
              <div class="text-sm text-gray-600">Uso de memoria</div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Configuration -->
      <div v-if="activeTab === 'system'" class="space-y-6">
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración del Sistema</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Configuración General</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Timezone</label>
                  <select
                    v-model="settings.system.timezone"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Chicago">Central Time</option>
                    <option value="America/Denver">Mountain Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                    <option value="Europe/Madrid">Madrid</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Idioma por defecto</label>
                  <select
                    v-model="settings.system.defaultLanguage"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Configuración de Logs</label>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Nivel de log</label>
                  <select
                    v-model="settings.system.logLevel"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="DEBUG">Debug</option>
                    <option value="INFO">Info</option>
                    <option value="WARNING">Warning</option>
                    <option value="ERROR">Error</option>
                    <option value="CRITICAL">Critical</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-700 mb-1">Retención de logs (días)</label>
                  <input
                    v-model.number="settings.system.logRetention"
                    type="number"
                    min="1"
                    max="365"
                    class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Información del Sistema</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">Versiones</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">VersaAI:</span>
                  <span class="text-gray-900">{{ systemInfo.version }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Python:</span>
                  <span class="text-gray-900">{{ systemInfo.pythonVersion }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">FastAPI:</span>
                  <span class="text-gray-900">{{ systemInfo.fastapiVersion }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">PostgreSQL:</span>
                  <span class="text-gray-900">{{ systemInfo.postgresVersion }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">Estado del Sistema</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600">Uptime:</span>
                  <span class="text-gray-900">{{ systemInfo.uptime }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">CPU:</span>
                  <span class="text-gray-900">{{ systemInfo.cpuUsage }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Memoria:</span>
                  <span class="text-gray-900">{{ systemInfo.memoryUsage }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">Disco:</span>
                  <span class="text-gray-900">{{ systemInfo.diskUsage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="flex items-center justify-end space-x-3 mt-8 pt-6 border-t border-gray-200">
      <button
        @click="resetToDefaults"
        class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Restaurar por defecto
      </button>
      <button
        @click="saveSettings"
        :disabled="saving"
        class="px-6 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
      </button>
    </div>

    <!-- Import Modal -->
    <ImportSettingsModal
      v-if="showImportModal"
      @close="showImportModal = false"
      @import="importSettings"
    />
    
    <!-- Backup History Modal -->
    <BackupHistoryModal
      v-if="showBackupHistory"
      @close="showBackupHistory = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  CogIcon,
  CircleStackIcon,
  ShieldCheckIcon,
  ChartBarIcon,
  ComputerDesktopIcon
} from '@heroicons/vue/24/outline'
import ToggleSwitch from '@/components/ui/ToggleSwitch.vue'
import ImportSettingsModal from '@/components/dashboard/ImportSettingsModal.vue'
import BackupHistoryModal from '@/components/dashboard/BackupHistoryModal.vue'

// Reactive state
const activeTab = ref('api')
const saving = ref(false)
const showImportModal = ref(false)
const showBackupHistory = ref(false)

const tabs = [
  { id: 'api', name: 'API', icon: CogIcon },
  { id: 'database', name: 'Base de Datos', icon: CircleStackIcon },
  { id: 'security', name: 'Seguridad', icon: ShieldCheckIcon },
  { id: 'performance', name: 'Performance', icon: ChartBarIcon },
  { id: 'system', name: 'Sistema', icon: ComputerDesktopIcon }
]

const settings = reactive({
  api: {
    rateLimiting: {
      enabled: true,
      requestsPerMinute: 1000
    },
    cors: {
      allowedOrigins: 'https://app.versaai.com\nhttps://dashboard.versaai.com',
      allowCredentials: true
    },
    cache: {
      enabled: true,
      defaultTTL: 3600,
      strategies: ['conversations', 'chatbots']
    }
  },
  database: {
    poolSize: 20,
    maxOverflow: 10,
    queryLogging: false,
    slowQueryDetection: true,
    slowQueryThreshold: 1000,
    autoBackup: {
      enabled: true,
      frequency: 'daily'
    }
  },
  security: {
    jwt: {
      ttl: 24,
      refreshRotation: true
    },
    twoFactor: {
      enabled: false
    },
    password: {
      minLength: 8,
      requireUppercase: true,
      requireNumbers: true,
      requireSymbols: false
    },
    threatDetection: {
      bruteForce: true,
      anomalies: true,
      geoBlocking: false
    },
    logging: {
      authentication: true,
      apiAccess: true,
      configChanges: true
    }
  },
  performance: {
    maxWorkers: 4,
    requestTimeout: 30,
    maxFileSize: 100,
    gzipCompression: true,
    lazyLoading: true,
    cdnAssets: false
  },
  system: {
    timezone: 'UTC',
    defaultLanguage: 'es',
    logLevel: 'INFO',
    logRetention: 30
  }
})

const performanceMetrics = ref({
  responseTime: 145,
  throughput: 250,
  memoryUsage: 68
})

const systemInfo = ref({
  version: '1.0.0',
  pythonVersion: '3.11.5',
  fastapiVersion: '0.104.1',
  postgresVersion: '15.4',
  uptime: '7d 14h 32m',
  cpuUsage: 23,
  memoryUsage: 68,
  diskUsage: 45
})

// Methods
const saveSettings = async () => {
  saving.value = true
  
  try {
    // TODO: Save settings to API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    alert('Configuración guardada exitosamente')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Error al guardar la configuración')
  } finally {
    saving.value = false
  }
}

const resetToDefaults = () => {
  if (confirm('¿Estás seguro de que quieres restaurar la configuración por defecto? Se perderán todos los cambios.')) {
    // TODO: Reset to default settings
    location.reload()
  }
}

const exportSettings = () => {
  const dataStr = JSON.stringify(settings, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `versaai-settings-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const importSettings = (importedSettings) => {
  try {
    Object.assign(settings, importedSettings)
    alert('Configuración importada exitosamente')
  } catch (error) {
    console.error('Error importing settings:', error)
    alert('Error al importar la configuración')
  }
}

const runDatabaseMaintenance = async () => {
  if (confirm('¿Estás seguro de que quieres ejecutar el mantenimiento de la base de datos? Esto puede tomar varios minutos.')) {
    try {
      // TODO: Run database maintenance
      await new Promise(resolve => setTimeout(resolve, 3000))
      alert('Mantenimiento de base de datos completado')
    } catch (error) {
      console.error('Error running maintenance:', error)
      alert('Error al ejecutar el mantenimiento')
    }
  }
}

const createBackup = async () => {
  try {
    // TODO: Create database backup
    await new Promise(resolve => setTimeout(resolve, 2000))
    alert('Backup creado exitosamente')
  } catch (error) {
    console.error('Error creating backup:', error)
    alert('Error al crear el backup')
  }
}

// Initialize
onMounted(() => {
  // TODO: Load settings from API
  console.log('AdvancedSettings mounted')
  
  // Update performance metrics every 30 seconds
  setInterval(() => {
    performanceMetrics.value = {
      responseTime: Math.floor(Math.random() * 100) + 100,
      throughput: Math.floor(Math.random() * 100) + 200,
      memoryUsage: Math.floor(Math.random() * 30) + 50
    }
  }, 30000)
})
</script>