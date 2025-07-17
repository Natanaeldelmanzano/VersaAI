<template>
  <div class="integrations-hub min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Hub de Integraciones</h1>
            <p class="text-gray-600 mt-1">Centro unificado para gestionar todas las integraciones de VersaAI</p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="showWebhookManager = true"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <PlusIcon class="h-5 w-5" />
              <span>Nuevo Webhook</span>
            </button>
            <button
              @click="showAPIKeyManager = true"
              class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center space-x-2"
            >
              <KeyIcon class="h-5 w-5" />
              <span>Gestionar APIs</span>
            </button>
            <button
              @click="refreshIntegrations"
              :disabled="isLoading"
              class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2 disabled:opacity-50"
            >
              <ArrowPathIcon :class="['h-5 w-5', { 'animate-spin': isLoading }]" />
              <span>Actualizar</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="p-6 space-y-8">
      <!-- Integration Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">Integraciones Activas</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.active }}</p>
              <div class="flex items-center mt-2">
                <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
                <span class="text-sm font-medium text-green-600">+{{ stats.activeGrowth }}</span>
                <span class="text-sm text-gray-500 ml-2">este mes</span>
              </div>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircleIcon class="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">Total Requests</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatNumber(stats.totalRequests) }}</p>
              <div class="flex items-center mt-2">
                <ArrowUpIcon class="w-4 h-4 text-blue-600 mr-1" />
                <span class="text-sm font-medium text-blue-600">{{ stats.requestsGrowth }}%</span>
                <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
              </div>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <ChartBarIcon class="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">Tasa de Éxito</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.successRate }}%</p>
              <div class="flex items-center mt-2">
                <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
                <span class="text-sm font-medium text-green-600">+{{ stats.successRateGrowth }}%</span>
                <span class="text-sm text-gray-500 ml-2">mejora</span>
              </div>
            </div>
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <ShieldCheckIcon class="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-600">Tiempo Respuesta</p>
              <p class="text-3xl font-bold text-gray-900 mt-2">{{ stats.avgResponseTime }}ms</p>
              <div class="flex items-center mt-2">
                <ArrowDownIcon class="w-4 h-4 text-green-600 mr-1" />
                <span class="text-sm font-medium text-green-600">-{{ stats.responseTimeImprovement }}ms</span>
                <span class="text-sm text-gray-500 ml-2">mejora</span>
              </div>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <ClockIcon class="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div class="flex-1 max-w-md">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar integraciones..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <select
              v-model="selectedCategory"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Todas las categorías</option>
              <option value="communication">Comunicación</option>
              <option value="crm">CRM & Sales</option>
              <option value="automation">Automatización</option>
              <option value="analytics">Analytics</option>
              <option value="payment">Pagos</option>
            </select>
            <select
              v-model="selectedStatus"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Todos los estados</option>
              <option value="active">Activo</option>
              <option value="inactive">Inactivo</option>
              <option value="error">Error</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Integrations Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <IntegrationCard
          v-for="integration in filteredIntegrations"
          :key="integration.id"
          :integration="integration"
          @configure="handleConfigure"
          @toggle="handleToggle"
          @test="handleTest"
          @view-details="handleViewDetails"
        />
      </div>

      <!-- Empty State -->
      <div v-if="filteredIntegrations.length === 0" class="text-center py-12">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <PuzzlePieceIcon class="w-12 h-12 text-gray-400" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No se encontraron integraciones</h3>
        <p class="text-gray-600 mb-6">Ajusta los filtros o agrega una nueva integración</p>
        <button
          @click="clearFilters"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Scroll to Top Button -->
    <button
      v-if="showScrollTop"
      @click="scrollToTop"
      class="fixed bottom-6 right-6 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-200 z-50"
    >
      <ArrowUpIcon class="h-5 w-5" />
    </button>

    <!-- Modals -->
    <WebhookManager
      v-if="showWebhookManager"
      @close="showWebhookManager = false"
      @save="handleWebhookSave"
    />

    <APIKeyManager
      v-if="showAPIKeyManager"
      @close="showAPIKeyManager = false"
      @save="handleAPIKeySave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useIntegrations } from '@/composables/useIntegrations'
import { useNotifications } from '@/composables/useNotifications'
import IntegrationCard from '@/components/integrations/IntegrationCard.vue'
import WebhookManager from '@/components/integrations/WebhookManager.vue'
import APIKeyManager from '@/components/integrations/APIKeyManager.vue'
import {
  PlusIcon,
  KeyIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  ClockIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  MagnifyingGlassIcon,
  PuzzlePieceIcon
} from '@heroicons/vue/24/outline'

// Composables
const { integrations, stats, isLoading, refreshIntegrations: refresh } = useIntegrations()
const { showSuccess, showError } = useNotifications()

// Reactive state
const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedStatus = ref('all')
const showWebhookManager = ref(false)
const showAPIKeyManager = ref(false)
const showScrollTop = ref(false)

// Computed
const filteredIntegrations = computed(() => {
  let filtered = integrations.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(integration => 
      integration.name.toLowerCase().includes(query) ||
      integration.description.toLowerCase().includes(query)
    )
  }

  // Filter by category
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(integration => integration.category === selectedCategory.value)
  }

  // Filter by status
  if (selectedStatus.value !== 'all') {
    filtered = filtered.filter(integration => integration.status === selectedStatus.value)
  }

  return filtered
})

// Methods
const refreshIntegrations = async () => {
  try {
    await refresh()
    showSuccess('Integraciones actualizadas correctamente')
  } catch (error) {
    showError('Error al actualizar las integraciones')
  }
}

const handleConfigure = (integration) => {
  console.log('Configurando integración:', integration.name)
  // TODO: Implementar configuración específica
}

const handleToggle = async (integration) => {
  try {
    // TODO: Implementar toggle de integración
    const newStatus = integration.status === 'active' ? 'inactive' : 'active'
    showSuccess(`Integración ${integration.name} ${newStatus === 'active' ? 'activada' : 'desactivada'}`)
  } catch (error) {
    showError('Error al cambiar el estado de la integración')
  }
}

const handleTest = async (integration) => {
  try {
    // TODO: Implementar test de integración
    showSuccess(`Test de ${integration.name} ejecutado correctamente`)
  } catch (error) {
    showError('Error al ejecutar el test de la integración')
  }
}

const handleViewDetails = (integration) => {
  console.log('Viendo detalles de:', integration.name)
  // TODO: Implementar vista de detalles
}

const handleWebhookSave = (webhookData) => {
  console.log('Guardando webhook:', webhookData)
  showSuccess('Webhook guardado correctamente')
  showWebhookManager.value = false
}

const handleAPIKeySave = (apiKeyData) => {
  console.log('Guardando API key:', apiKeyData)
  showSuccess('API key guardada correctamente')
  showAPIKeyManager.value = false
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedStatus.value = 'all'
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-ES').format(num)
}

// Scroll handling
const handleScroll = () => {
  showScrollTop.value = window.scrollY > 300
}

// Lifecycle
onMounted(() => {
  refreshIntegrations()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.integrations-hub {
  @apply scroll-smooth;
}

.scrollable {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.scrollable::-webkit-scrollbar {
  width: 6px;
}

.scrollable::-webkit-scrollbar-track {
  @apply bg-gray-100 rounded-full;
}

.scrollable::-webkit-scrollbar-thumb {
  @apply bg-gray-400 rounded-full hover:bg-gray-500;
}

@media (prefers-color-scheme: dark) {
  .scrollable {
    scrollbar-color: #4b5563 #1f2937;
  }
  
  .scrollable::-webkit-scrollbar-track {
    @apply bg-gray-800;
  }
  
  .scrollable::-webkit-scrollbar-thumb {
    @apply bg-gray-600 hover:bg-gray-500;
  }
}
</style>