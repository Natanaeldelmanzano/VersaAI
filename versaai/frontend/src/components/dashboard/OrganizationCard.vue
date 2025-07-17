<template>
  <div class="organization-card bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200">
    <!-- Header de la Organización -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <!-- Avatar/Logo de la Organización -->
          <div class="relative">
            <div v-if="organization.logo" class="w-16 h-16 rounded-lg overflow-hidden">
              <img :src="organization.logo" :alt="organization.name" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-16 h-16 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
              <span class="text-white text-xl font-bold">{{ organization.name.charAt(0).toUpperCase() }}</span>
            </div>
            
            <!-- Indicador de Estado -->
            <div class="absolute -bottom-1 -right-1">
              <div :class="[
                'w-5 h-5 rounded-full border-2 border-white',
                organization.status === 'active' ? 'bg-green-500' :
                organization.status === 'inactive' ? 'bg-red-500' :
                organization.status === 'pending' ? 'bg-yellow-500' : 'bg-gray-500'
              ]"></div>
            </div>
          </div>
          
          <!-- Información Básica -->
          <div class="flex-1">
            <h3 class="text-xl font-semibold text-gray-900">{{ organization.name }}</h3>
            <p class="text-sm text-gray-600 mt-1">{{ organization.industry || 'Industria no especificada' }}</p>
            <div class="flex items-center mt-2 space-x-4">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="statusClasses">
                {{ statusText }}
              </span>
              <span class="text-xs text-gray-500">ID: {{ organization.id }}</span>
            </div>
          </div>
        </div>
        
        <!-- Menú de Acciones -->
        <div class="relative" ref="menuRef">
          <button
            @click="showMenu = !showMenu"
            class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
          >
            <EllipsisVerticalIcon class="w-5 h-5" />
          </button>
          
          <!-- Dropdown Menu -->
          <div v-if="showMenu" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10">
            <div class="py-1">
              <button
                @click="viewDetails"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
              >
                <EyeIcon class="w-4 h-4 mr-2" />
                Ver Detalles
              </button>
              <button
                @click="editOrganization"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
              >
                <PencilIcon class="w-4 h-4 mr-2" />
                Editar
              </button>
              <button
                @click="manageUsers"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
              >
                <UsersIcon class="w-4 h-4 mr-2" />
                Gestionar Usuarios
              </button>
              <button
                @click="viewBilling"
                class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
              >
                <CreditCardIcon class="w-4 h-4 mr-2" />
                Facturación
              </button>
              <div class="border-t border-gray-100 my-1"></div>
              <button
                @click="toggleStatus"
                class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 flex items-center"
                :class="organization.status === 'active' ? 'text-red-600' : 'text-green-600'"
              >
                <component :is="organization.status === 'active' ? PauseIcon : PlayIcon" class="w-4 h-4 mr-2" />
                {{ organization.status === 'active' ? 'Desactivar' : 'Activar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Métricas Principales -->
    <div class="p-6">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-gray-900">{{ organization.stats?.users || 0 }}</div>
          <div class="text-sm text-gray-600">Usuarios</div>
          <div v-if="organization.stats?.usersGrowth" class="text-xs mt-1" :class="organization.stats.usersGrowth > 0 ? 'text-green-600' : 'text-red-600'">
            {{ organization.stats.usersGrowth > 0 ? '+' : '' }}{{ organization.stats.usersGrowth }}%
          </div>
        </div>
        
        <div class="text-center">
          <div class="text-2xl font-bold text-gray-900">{{ organization.stats?.chatbots || 0 }}</div>
          <div class="text-sm text-gray-600">Chatbots</div>
          <div v-if="organization.stats?.chatbotsActive" class="text-xs text-green-600 mt-1">
            {{ organization.stats.chatbotsActive }} activos
          </div>
        </div>
        
        <div class="text-center">
          <div class="text-2xl font-bold text-gray-900">{{ formatNumber(organization.stats?.conversations || 0) }}</div>
          <div class="text-sm text-gray-600">Conversaciones</div>
          <div v-if="organization.stats?.conversationsGrowth" class="text-xs mt-1" :class="organization.stats.conversationsGrowth > 0 ? 'text-green-600' : 'text-red-600'">
            {{ organization.stats.conversationsGrowth > 0 ? '+' : '' }}{{ organization.stats.conversationsGrowth }}%
          </div>
        </div>
        
        <div class="text-center">
          <div class="text-2xl font-bold text-gray-900">{{ organization.stats?.satisfaction || 'N/A' }}</div>
          <div class="text-sm text-gray-600">Satisfacción</div>
          <div v-if="organization.stats?.satisfactionTrend" class="text-xs mt-1" :class="organization.stats.satisfactionTrend > 0 ? 'text-green-600' : 'text-red-600'">
            {{ organization.stats.satisfactionTrend > 0 ? '+' : '' }}{{ organization.stats.satisfactionTrend }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Plan y Facturación -->
    <div class="px-6 pb-6">
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-medium text-gray-700">Plan:</span>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="planClasses">
              {{ organization.plan?.name || 'Básico' }}
            </span>
          </div>
          <div class="text-sm text-gray-600">
            ${{ organization.plan?.price || 0 }}/mes
          </div>
        </div>
        
        <!-- Uso de Recursos -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600">Usuarios</span>
            <span class="text-gray-900">{{ organization.stats?.users || 0 }} / {{ organization.plan?.limits?.users || '∞' }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5">
            <div 
              class="bg-primary-600 h-1.5 rounded-full transition-all duration-300"
              :style="{ width: `${Math.min(100, ((organization.stats?.users || 0) / (organization.plan?.limits?.users || 100)) * 100)}%` }"
            ></div>
          </div>
          
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-600">Conversaciones/mes</span>
            <span class="text-gray-900">{{ formatNumber(organization.stats?.monthlyConversations || 0) }} / {{ formatNumber(organization.plan?.limits?.conversations || 0) }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5">
            <div 
              class="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
              :style="{ width: `${Math.min(100, ((organization.stats?.monthlyConversations || 0) / (organization.plan?.limits?.conversations || 1000)) * 100)}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer con Información Adicional -->
    <div class="px-6 py-4 bg-gray-50 rounded-b-xl">
      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center space-x-4">
          <span class="text-gray-600">Creado: {{ formatDate(organization.createdAt) }}</span>
          <span class="text-gray-600">Último acceso: {{ formatDate(organization.lastActivity) }}</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Indicadores de Características -->
          <div v-if="organization.features?.sso" class="w-2 h-2 bg-green-500 rounded-full" title="SSO Habilitado"></div>
          <div v-if="organization.features?.api" class="w-2 h-2 bg-blue-500 rounded-full" title="API Habilitada"></div>
          <div v-if="organization.features?.analytics" class="w-2 h-2 bg-purple-500 rounded-full" title="Analytics Avanzado"></div>
          <div v-if="organization.features?.whiteLabel" class="w-2 h-2 bg-orange-500 rounded-full" title="White Label"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  EllipsisVerticalIcon,
  EyeIcon,
  PencilIcon,
  UsersIcon,
  CreditCardIcon,
  PauseIcon,
  PlayIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  organization: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits([
  'view-details',
  'edit',
  'manage-users',
  'view-billing',
  'toggle-status'
])

// State
const showMenu = ref(false)
const menuRef = ref(null)

// Computed
const statusClasses = computed(() => {
  switch (props.organization.status) {
    case 'active':
      return 'bg-green-100 text-green-800'
    case 'inactive':
      return 'bg-red-100 text-red-800'
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'suspended':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

const statusText = computed(() => {
  switch (props.organization.status) {
    case 'active': return 'Activo'
    case 'inactive': return 'Inactivo'
    case 'pending': return 'Pendiente'
    case 'suspended': return 'Suspendido'
    default: return 'Desconocido'
  }
})

const planClasses = computed(() => {
  const planName = props.organization.plan?.name?.toLowerCase() || 'basic'
  
  switch (planName) {
    case 'enterprise':
      return 'bg-purple-100 text-purple-800'
    case 'professional':
    case 'pro':
      return 'bg-blue-100 text-blue-800'
    case 'premium':
      return 'bg-orange-100 text-orange-800'
    case 'basic':
    case 'starter':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

// Methods
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) {
    return 'Ayer'
  } else if (diffDays < 7) {
    return `Hace ${diffDays} días`
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `Hace ${weeks} semana${weeks > 1 ? 's' : ''}`
  } else {
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}

const viewDetails = () => {
  showMenu.value = false
  emit('view-details', props.organization)
}

const editOrganization = () => {
  showMenu.value = false
  emit('edit', props.organization)
}

const manageUsers = () => {
  showMenu.value = false
  emit('manage-users', props.organization)
}

const viewBilling = () => {
  showMenu.value = false
  emit('view-billing', props.organization)
}

const toggleStatus = () => {
  showMenu.value = false
  emit('toggle-status', props.organization)
}

const handleClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.organization-card {
  transition: all 0.2s ease-in-out;
}

.organization-card:hover {
  transform: translateY(-2px);
}

/* Animación para las barras de progreso */
.bg-primary-600,
.bg-blue-600 {
  transition: width 0.3s ease-in-out;
}

/* Efecto hover para el menú */
.relative button:hover + div,
.relative div:hover {
  display: block;
}
</style>