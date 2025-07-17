<template>
  <div class="p-6">
    <!-- Header with refresh button -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
        <p class="text-gray-600">Bienvenido al panel de control de VersaAI</p>
      </div>
      <button 
        @click="refreshData" 
        :disabled="isLoading"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="!isLoading" class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <svg v-else class="-ml-1 mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ isLoading ? 'Actualizando...' : 'Actualizar' }}
      </button>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading && !hasData" class="mt-8 flex justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    
    <!-- Stats cards -->
    <div v-else class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div 
         v-for="(stat, key) in formattedStats" 
         :key="key"
         class="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow duration-200"
       >
         <div class="flex items-center justify-between">
           <div>
             <h3 class="text-lg font-semibold text-gray-900">{{ stat.label }}</h3>
             <p :class="getStatColorClass(stat.color)">{{ stat.value || 0 }}</p>
           </div>
           <div :class="getIconBgClass(stat.color)">
             <component 
               :is="getIconComponent(stat.icon)" 
               :class="getIconColorClass(stat.color)"
             />
           </div>
         </div>
       </div>
    </div>
    
    <div class="mt-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">Acciones Rápidas</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <router-link to="/dashboard/chatbots" class="bg-blue-500 text-white p-4 rounded-lg hover:bg-blue-600 transition-colors">
          Ver Chatbots
        </router-link>
        <router-link to="/dashboard/users" class="bg-green-500 text-white p-4 rounded-lg hover:bg-green-600 transition-colors">
          Gestionar Usuarios
        </router-link>
        <router-link to="/dashboard/analytics" class="bg-purple-500 text-white p-4 rounded-lg hover:bg-purple-600 transition-colors">
          Ver Analíticas
        </router-link>
        <router-link to="/dashboard/settings" class="bg-orange-500 text-white p-4 rounded-lg hover:bg-orange-600 transition-colors">
          Configuración
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { useDashboardStore } from '@/stores/dashboard'
import {
  ChatBubbleLeftRightIcon,
  UsersIcon,
  ChatBubbleOvalLeftEllipsisIcon,
  BookOpenIcon
} from '@heroicons/vue/24/outline'

// Stores
const authStore = useAuthStore()
const appStore = useAppStore()
const dashboardStore = useDashboardStore()

// Computed properties from store
const isLoading = computed(() => dashboardStore.isLoading)
const stats = computed(() => dashboardStore.stats)
const formattedStats = computed(() => dashboardStore.formattedStats)
const hasData = computed(() => dashboardStore.hasData)

// Icon mapping
const iconComponents = {
  ChatBubbleLeftRightIcon,
  UsersIcon,
  ChatBubbleOvalLeftEllipsisIcon,
  BookOpenIcon
}

// Get icon component
const getIconComponent = (iconName) => {
  return iconComponents[iconName] || ChatBubbleLeftRightIcon
}

// Color class helpers
const getStatColorClass = (color) => {
  const colorClasses = {
    blue: 'text-3xl font-bold text-blue-600 mt-2',
    green: 'text-3xl font-bold text-green-600 mt-2',
    purple: 'text-3xl font-bold text-purple-600 mt-2',
    orange: 'text-3xl font-bold text-orange-600 mt-2'
  }
  return colorClasses[color] || colorClasses.blue
}

const getIconBgClass = (color) => {
  const bgClasses = {
    blue: 'p-3 rounded-full bg-blue-100',
    green: 'p-3 rounded-full bg-green-100',
    purple: 'p-3 rounded-full bg-purple-100',
    orange: 'p-3 rounded-full bg-orange-100'
  }
  return bgClasses[color] || bgClasses.blue
}

const getIconColorClass = (color) => {
  const iconClasses = {
    blue: 'h-6 w-6 text-blue-600',
    green: 'h-6 w-6 text-green-600',
    purple: 'h-6 w-6 text-purple-600',
    orange: 'h-6 w-6 text-orange-600'
  }
  return iconClasses[color] || iconClasses.blue
}

// Load dashboard stats
const loadStats = async () => {
  try {
    const result = await dashboardStore.fetchDashboardStats()
    
    if (result.success && result.mock) {
      console.warn('Using mock data - API not available')
    }
    
    // Set page info
    appStore.setPageInfo('Dashboard Overview', 'Resumen general de tu plataforma VersaAI')
    
  } catch (error) {
    console.error('Error loading dashboard stats:', error)
  }
}

// Refresh data
const refreshData = async () => {
  await dashboardStore.refreshAllData()
}

// Initialize on mount
onMounted(() => {
  loadStats()
})
</script>