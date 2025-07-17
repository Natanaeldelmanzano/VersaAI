<template>
  <div class="enterprise-dashboard min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <ChartBarIcon class="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h1 class="text-xl font-semibold text-gray-900">Dashboard Empresarial</h1>
              <p class="text-sm text-gray-500">Analytics y métricas en tiempo real</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- View Selector -->
            <select 
              v-model="currentView"
              @change="onViewChange"
              class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 text-sm"
            >
              <option value="overview">Vista General</option>
              <option value="users">Gestión de Usuarios</option>
              <option value="billing">Facturación</option>
              <option value="analytics">Analytics Avanzados</option>
            </select>
            
            <!-- Organization selector -->
            <select 
              v-model="selectedOrganization"
              @change="handleOrganizationChange"
              class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 text-sm"
            >
              <option value="all">Todas las organizaciones</option>
              <option 
                v-for="org in organizations" 
                :key="org.id" 
                :value="org.id"
              >
                {{ org.name }}
              </option>
            </select>
            
            <!-- Export button -->
            <button
              @click="exportData"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              Exportar
            </button>
            
            <!-- Settings button -->
            <button
              @click="openSettings"
              class="inline-flex items-center p-2 border border-gray-300 rounded-lg shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <Cog6ToothIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Quick stats overview -->
      <div class="mb-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <UsersIcon class="w-5 h-5 text-blue-600" />
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Usuarios Activos</p>
                <p class="text-2xl font-bold text-gray-900">{{ formatNumber(activeUsers) }}</p>
                <p class="text-sm text-green-600">+12% vs ayer</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <CurrencyDollarIcon class="w-5 h-5 text-green-600" />
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Ingresos del Mes</p>
                <p class="text-2xl font-bold text-gray-900">${{ formatNumber(monthlyRevenue) }}</p>
                <p class="text-sm text-green-600">+8% vs mes anterior</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <ChatBubbleLeftRightIcon class="w-5 h-5 text-purple-600" />
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Conversaciones Hoy</p>
                <p class="text-2xl font-bold text-gray-900">{{ formatNumber(todayConversations) }}</p>
                <p class="text-sm text-green-600">+15% vs ayer</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                  <ClockIcon class="w-5 h-5 text-orange-600" />
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Tiempo Respuesta</p>
                <p class="text-2xl font-bold text-gray-900">{{ averageResponseTime }}ms</p>
                <p class="text-sm text-red-600">+5% vs ayer</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Overview View -->
      <div v-if="currentView === 'overview'">
        <!-- Enterprise Metrics Component -->
        <EnterpriseMetrics />
        
        <!-- Additional enterprise features -->
        <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- User Management Summary -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-900">Gestión de Usuarios</h3>
              <button 
                @click="currentView = 'users'"
                class="text-primary-600 hover:text-primary-700 text-sm font-medium"
              >
                Ver todos
              </button>
            </div>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p class="font-medium text-gray-900">Usuarios Totales</p>
                  <p class="text-sm text-gray-500">Registrados en la plataforma</p>
                </div>
                <div class="text-2xl font-bold text-blue-600">{{ formatNumber(totalUsers) }}</div>
              </div>
              
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p class="font-medium text-gray-900">Usuarios Premium</p>
                  <p class="text-sm text-gray-500">Con suscripción activa</p>
                </div>
                <div class="text-2xl font-bold text-green-600">{{ formatNumber(premiumUsers) }}</div>
              </div>
              
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p class="font-medium text-gray-900">Nuevos Usuarios</p>
                  <p class="text-sm text-gray-500">Últimos 30 días</p>
                </div>
                <div class="text-2xl font-bold text-purple-600">{{ formatNumber(newUsers) }}</div>
              </div>
            </div>
          </div>
          
          <!-- System Health -->
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-900">Estado del Sistema</h3>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <span class="text-sm text-green-600 font-medium">Operativo</span>
              </div>
            </div>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">CPU</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" style="width: 45%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">45%</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Memoria</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 68%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">68%</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Almacenamiento</span>
                <div class="flex items-center space-x-2">
                  <div class="w-24 bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" style="width: 32%"></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900">32%</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Conexiones Activas</span>
                <span class="text-sm font-medium text-gray-900">{{ formatNumber(activeConnections) }}</span>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Uptime</span>
                <span class="text-sm font-medium text-green-600">99.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- User Management View -->
      <div v-else-if="currentView === 'users'">
        <UserManagement />
      </div>
      
      <!-- Billing Management View -->
      <div v-else-if="currentView === 'billing'">
        <BillingManagement />
      </div>
      
      <!-- Analytics View -->
      <div v-else-if="currentView === 'analytics'">
        <EnterpriseMetrics :detailed="true" />
      </div>
    </div>
    
    <!-- Settings Modal -->
    <div 
      v-if="showSettings"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeSettings"
    >
      <div 
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Configuración del Dashboard</h3>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Actualización automática
              </label>
              <select 
                v-model="autoRefreshInterval"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="0">Desactivado</option>
                <option value="30">30 segundos</option>
                <option value="60">1 minuto</option>
                <option value="300">5 minutos</option>
              </select>
            </div>
            
            <div>
              <label class="flex items-center">
                <input 
                  v-model="showNotifications"
                  type="checkbox" 
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                <span class="ml-2 text-sm text-gray-700">Mostrar notificaciones</span>
              </label>
            </div>
            
            <div>
              <label class="flex items-center">
                <input 
                  v-model="enableSounds"
                  type="checkbox" 
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                <span class="ml-2 text-sm text-gray-700">Sonidos de alerta</span>
              </label>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button
              @click="closeSettings"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancelar
            </button>
            <button
              @click="saveSettings"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
            >
              Guardar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import { useDashboardStore } from '@/stores/dashboard'
import { useUserManagementStore } from '@/stores/userManagement'
import { useBillingStore } from '@/stores/billing'
import {
  ChartBarIcon,
  UsersIcon,
  CurrencyDollarIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  ArrowDownTrayIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'
import EnterpriseMetrics from '@/components/dashboard/EnterpriseMetrics.vue'
import UserManagement from '@/components/dashboard/UserManagement.vue'
import BillingManagement from '@/components/dashboard/BillingManagement.vue'

// Stores
const analyticsStore = useAnalyticsStore()
const dashboardStore = useDashboardStore()
const userManagementStore = useUserManagementStore()
const billingStore = useBillingStore()

// State
const currentView = ref('overview')
const selectedOrganization = ref('all')
const showSettings = ref(false)
const autoRefreshInterval = ref(30)
const showNotifications = ref(true)
const enableSounds = ref(false)
const refreshTimer = ref(null)

// Mock data for enterprise features
const organizations = ref([
  { id: 1, name: 'Acme Corp' },
  { id: 2, name: 'TechStart Inc' },
  { id: 3, name: 'Global Solutions' }
])

// Computed
const activeUsers = computed(() => 1247)
const monthlyRevenue = computed(() => 45680)
const todayConversations = computed(() => analyticsStore.overview.total_conversations || 892)
const averageResponseTime = computed(() => Math.round(analyticsStore.overview.average_response_time || 450))
const totalUsers = computed(() => 5420)
const premiumUsers = computed(() => 1680)
const newUsers = computed(() => 234)
const activeConnections = computed(() => 156)

// Methods
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toLocaleString()
}

const onViewChange = () => {
  // Load data for the selected view
  if (currentView.value === 'users') {
    userManagementStore.fetchUsers()
    userManagementStore.fetchOrganizations()
  } else if (currentView.value === 'billing') {
    billingStore.initializeBilling()
  }
}

const handleOrganizationChange = () => {
  // Refresh data for selected organization
  refreshData()
}

const exportData = () => {
  // Export dashboard data
  const data = {
    timestamp: new Date().toISOString(),
    organization: selectedOrganization.value,
    metrics: {
      activeUsers: activeUsers.value,
      monthlyRevenue: monthlyRevenue.value,
      todayConversations: todayConversations.value,
      averageResponseTime: averageResponseTime.value
    },
    analytics: analyticsStore.overview
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `dashboard-export-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const openSettings = () => {
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const saveSettings = () => {
  // Save settings to localStorage
  const settings = {
    autoRefreshInterval: autoRefreshInterval.value,
    showNotifications: showNotifications.value,
    enableSounds: enableSounds.value
  }
  localStorage.setItem('enterpriseDashboardSettings', JSON.stringify(settings))
  
  // Update refresh timer
  setupAutoRefresh()
  
  closeSettings()
}

const loadSettings = () => {
  const saved = localStorage.getItem('enterpriseDashboardSettings')
  if (saved) {
    const settings = JSON.parse(saved)
    autoRefreshInterval.value = settings.autoRefreshInterval || 30
    showNotifications.value = settings.showNotifications !== false
    enableSounds.value = settings.enableSounds || false
  }
}

const refreshData = async () => {
  try {
    const promises = [
      analyticsStore.fetchOverview(),
      analyticsStore.fetchConversationMetrics(),
      analyticsStore.fetchChatbotPerformance(),
      dashboardStore.fetchStats()
    ]
    
    // Load additional data based on current view
    if (currentView.value === 'users') {
      promises.push(
        userManagementStore.fetchUsers(),
        userManagementStore.fetchOrganizations()
      )
    } else if (currentView.value === 'billing') {
      promises.push(billingStore.initializeBilling())
    }
    
    await Promise.all(promises)
  } catch (error) {
    console.error('Error refreshing dashboard data:', error)
  }
}

const setupAutoRefresh = () => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
  
  if (autoRefreshInterval.value > 0) {
    refreshTimer.value = setInterval(() => {
      refreshData()
    }, autoRefreshInterval.value * 1000)
  }
}

// Lifecycle
onMounted(() => {
  loadSettings()
  refreshData()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
  }
})
</script>

<style scoped>
.enterprise-dashboard {
  min-height: 100vh;
}
</style>