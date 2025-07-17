<template>
  <div class="organization-management p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Gestión de Organizaciones</h1>
        <p class="text-gray-600 mt-1">Administra todas las organizaciones de la plataforma</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button
          @click="exportData"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
          Exportar
        </button>
        
        <button
          @click="showCreateModal = true"
          class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Nueva Organización
        </button>
      </div>
    </div>
    
    <!-- Estadísticas Generales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-blue-100">
            <BuildingOfficeIcon class="w-6 h-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Organizaciones</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
            <p class="text-xs text-green-600 mt-1">+{{ stats.newThisMonth }} este mes</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-green-100">
            <CheckCircleIcon class="w-6 h-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Organizaciones Activas</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.active }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ ((stats.active / stats.total) * 100).toFixed(1) }}% del total</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-purple-100">
            <CurrencyDollarIcon class="w-6 h-6 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Ingresos Mensuales</p>
            <p class="text-2xl font-bold text-gray-900">${{ formatNumber(stats.monthlyRevenue) }}</p>
            <p class="text-xs text-green-600 mt-1">+{{ stats.revenueGrowth }}% vs mes anterior</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div class="flex items-center">
          <div class="p-3 rounded-lg bg-orange-100">
            <UsersIcon class="w-6 h-6 text-orange-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Usuarios</p>
            <p class="text-2xl font-bold text-gray-900">{{ formatNumber(stats.totalUsers) }}</p>
            <p class="text-xs text-blue-600 mt-1">{{ (stats.totalUsers / stats.total).toFixed(0) }} promedio/org</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Filtros y Búsqueda -->
    <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Búsqueda -->
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            v-model="filters.search"
            type="text"
            placeholder="Buscar organizaciones..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        
        <!-- Filtro por Estado -->
        <select
          v-model="filters.status"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">Todos los estados</option>
          <option value="active">Activo</option>
          <option value="inactive">Inactivo</option>
          <option value="pending">Pendiente</option>
          <option value="suspended">Suspendido</option>
        </select>
        
        <!-- Filtro por Plan -->
        <select
          v-model="filters.plan"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">Todos los planes</option>
          <option value="basic">Básico</option>
          <option value="professional">Profesional</option>
          <option value="premium">Premium</option>
          <option value="enterprise">Enterprise</option>
        </select>
        
        <!-- Filtro por Industria -->
        <select
          v-model="filters.industry"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">Todas las industrias</option>
          <option value="technology">Tecnología</option>
          <option value="healthcare">Salud</option>
          <option value="finance">Finanzas</option>
          <option value="education">Educación</option>
          <option value="retail">Retail</option>
          <option value="manufacturing">Manufactura</option>
          <option value="other">Otros</option>
        </select>
      </div>
      
      <!-- Opciones de Vista -->
      <div class="flex items-center justify-between mt-4">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">Vista:</span>
          <button
            @click="viewMode = 'grid'"
            :class="[
              'p-2 rounded-lg',
              viewMode === 'grid' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'
            ]"
          >
            <Squares2X2Icon class="w-4 h-4" />
          </button>
          <button
            @click="viewMode = 'list'"
            :class="[
              'p-2 rounded-lg',
              viewMode === 'list' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'
            ]"
          >
            <ListBulletIcon class="w-4 h-4" />
          </button>
        </div>
        
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">Ordenar por:</span>
          <select
            v-model="sortBy"
            class="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="name">Nombre</option>
            <option value="createdAt">Fecha de creación</option>
            <option value="lastActivity">Última actividad</option>
            <option value="users">Número de usuarios</option>
            <option value="revenue">Ingresos</option>
          </select>
          
          <button
            @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
            class="p-1 text-gray-400 hover:text-gray-600"
          >
            <component :is="sortOrder === 'asc' ? ChevronUpIcon : ChevronDownIcon" class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Lista/Grid de Organizaciones -->
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else-if="filteredOrganizations.length === 0" class="text-center py-12">
      <BuildingOfficeIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">No se encontraron organizaciones</h3>
      <p class="text-gray-600">Intenta ajustar los filtros o crear una nueva organización.</p>
    </div>
    
    <!-- Vista Grid -->
    <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <OrganizationCard
        v-for="organization in paginatedOrganizations"
        :key="organization.id"
        :organization="organization"
        @view-details="viewOrganizationDetails"
        @edit="editOrganization"
        @manage-users="manageOrganizationUsers"
        @view-billing="viewOrganizationBilling"
        @toggle-status="toggleOrganizationStatus"
      />
    </div>
    
    <!-- Vista Lista -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Organización</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Plan</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuarios</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ingresos</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Última Actividad</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="organization in paginatedOrganizations" :key="organization.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div v-if="organization.logo" class="h-10 w-10 rounded-lg overflow-hidden">
                      <img :src="organization.logo" :alt="organization.name" class="h-full w-full object-cover" />
                    </div>
                    <div v-else class="h-10 w-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center">
                      <span class="text-white text-sm font-bold">{{ organization.name.charAt(0).toUpperCase() }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ organization.name }}</div>
                    <div class="text-sm text-gray-500">{{ organization.industry || 'N/A' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="getStatusClasses(organization.status)">
                  {{ getStatusText(organization.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="getPlanClasses(organization.plan?.name)">
                  {{ organization.plan?.name || 'Básico' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ organization.stats?.users || 0 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ organization.plan?.price || 0 }}/mes
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(organization.lastActivity) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end space-x-2">
                  <button
                    @click="viewOrganizationDetails(organization)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <EyeIcon class="w-4 h-4" />
                  </button>
                  <button
                    @click="editOrganization(organization)"
                    class="text-gray-600 hover:text-gray-900"
                  >
                    <PencilIcon class="w-4 h-4" />
                  </button>
                  <button
                    @click="toggleOrganizationStatus(organization)"
                    :class="organization.status === 'active' ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'"
                  >
                    <component :is="organization.status === 'active' ? PauseIcon : PlayIcon" class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Paginación -->
    <div v-if="totalPages > 1" class="flex items-center justify-between">
      <div class="text-sm text-gray-700">
        Mostrando {{ ((currentPage - 1) * itemsPerPage) + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredOrganizations.length) }} de {{ filteredOrganizations.length }} organizaciones
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="currentPage = Math.max(1, currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Anterior
        </button>
        
        <div class="flex items-center space-x-1">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-lg',
              page === currentPage
                ? 'bg-primary-600 text-white'
                : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
            ]"
          >
            {{ page }}
          </button>
        </div>
        
        <button
          @click="currentPage = Math.min(totalPages, currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Siguiente
        </button>
      </div>
    </div>
    
    <!-- Modal de Crear/Editar Organización -->
    <OrganizationModal
      v-if="showCreateModal || showEditModal"
      :organization="selectedOrganization"
      :is-edit="showEditModal"
      @close="closeModals"
      @save="handleSaveOrganization"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  BuildingOfficeIcon,
  CheckCircleIcon,
  CurrencyDollarIcon,
  UsersIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  EyeIcon,
  PencilIcon,
  PauseIcon,
  PlayIcon
} from '@heroicons/vue/24/outline'

import OrganizationCard from '@/components/dashboard/OrganizationCard.vue'
import OrganizationModal from '@/components/dashboard/modals/OrganizationModal.vue'

// Router
const router = useRouter()

// State
const isLoading = ref(true)
const organizations = ref([])
const stats = ref({
  total: 0,
  active: 0,
  newThisMonth: 0,
  monthlyRevenue: 0,
  revenueGrowth: 0,
  totalUsers: 0
})

// Filtros
const filters = ref({
  search: '',
  status: '',
  plan: '',
  industry: ''
})

// Vista y ordenamiento
const viewMode = ref('grid')
const sortBy = ref('name')
const sortOrder = ref('asc')

// Paginación
const currentPage = ref(1)
const itemsPerPage = ref(12)

// Modales
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedOrganization = ref(null)

// Computed
const filteredOrganizations = computed(() => {
  let filtered = organizations.value.filter(org => {
    const matchesSearch = !filters.value.search || 
      org.name.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      org.industry?.toLowerCase().includes(filters.value.search.toLowerCase())
    
    const matchesStatus = !filters.value.status || org.status === filters.value.status
    const matchesPlan = !filters.value.plan || org.plan?.name?.toLowerCase() === filters.value.plan
    const matchesIndustry = !filters.value.industry || org.industry === filters.value.industry
    
    return matchesSearch && matchesStatus && matchesPlan && matchesIndustry
  })
  
  // Ordenamiento
  filtered.sort((a, b) => {
    let aValue, bValue
    
    switch (sortBy.value) {
      case 'name':
        aValue = a.name.toLowerCase()
        bValue = b.name.toLowerCase()
        break
      case 'createdAt':
        aValue = new Date(a.createdAt)
        bValue = new Date(b.createdAt)
        break
      case 'lastActivity':
        aValue = new Date(a.lastActivity)
        bValue = new Date(b.lastActivity)
        break
      case 'users':
        aValue = a.stats?.users || 0
        bValue = b.stats?.users || 0
        break
      case 'revenue':
        aValue = a.plan?.price || 0
        bValue = b.plan?.price || 0
        break
      default:
        aValue = a.name.toLowerCase()
        bValue = b.name.toLowerCase()
    }
    
    if (sortOrder.value === 'asc') {
      return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
    } else {
      return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
    }
  })
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredOrganizations.value.length / itemsPerPage.value)
})

const paginatedOrganizations = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredOrganizations.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    } else if (current >= total - 3) {
      pages.push(1, '...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1, '...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    }
  }
  
  return pages.filter(page => page !== '...' || pages.indexOf(page) === pages.lastIndexOf(page))
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
  } else {
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }
}

const getStatusClasses = (status) => {
  switch (status) {
    case 'active': return 'bg-green-100 text-green-800'
    case 'inactive': return 'bg-red-100 text-red-800'
    case 'pending': return 'bg-yellow-100 text-yellow-800'
    case 'suspended': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'active': return 'Activo'
    case 'inactive': return 'Inactivo'
    case 'pending': return 'Pendiente'
    case 'suspended': return 'Suspendido'
    default: return 'Desconocido'
  }
}

const getPlanClasses = (planName) => {
  const plan = planName?.toLowerCase() || 'basic'
  
  switch (plan) {
    case 'enterprise': return 'bg-purple-100 text-purple-800'
    case 'professional':
    case 'pro': return 'bg-blue-100 text-blue-800'
    case 'premium': return 'bg-orange-100 text-orange-800'
    case 'basic':
    case 'starter': return 'bg-gray-100 text-gray-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const loadOrganizations = async () => {
  try {
    isLoading.value = true
    
    // Simular datos de organizaciones
    const mockOrganizations = [
      {
        id: '1',
        name: 'TechCorp Solutions',
        industry: 'technology',
        status: 'active',
        logo: null,
        plan: { name: 'Enterprise', price: 299 },
        stats: {
          users: 150,
          usersGrowth: 12,
          chatbots: 25,
          chatbotsActive: 23,
          conversations: 45000,
          conversationsGrowth: 8,
          satisfaction: '4.8',
          satisfactionTrend: 0.2,
          monthlyConversations: 15000
        },
        features: {
          sso: true,
          api: true,
          analytics: true,
          whiteLabel: true
        },
        createdAt: '2023-01-15T10:00:00Z',
        lastActivity: '2024-01-15T14:30:00Z'
      },
      {
        id: '2',
        name: 'HealthCare Plus',
        industry: 'healthcare',
        status: 'active',
        logo: null,
        plan: { name: 'Professional', price: 149 },
        stats: {
          users: 75,
          usersGrowth: 5,
          chatbots: 12,
          chatbotsActive: 11,
          conversations: 28000,
          conversationsGrowth: 15,
          satisfaction: '4.6',
          satisfactionTrend: 0.1,
          monthlyConversations: 9500
        },
        features: {
          sso: false,
          api: true,
          analytics: true,
          whiteLabel: false
        },
        createdAt: '2023-03-20T09:00:00Z',
        lastActivity: '2024-01-14T16:45:00Z'
      },
      {
        id: '3',
        name: 'EduLearn Academy',
        industry: 'education',
        status: 'pending',
        logo: null,
        plan: { name: 'Basic', price: 49 },
        stats: {
          users: 25,
          usersGrowth: 0,
          chatbots: 5,
          chatbotsActive: 3,
          conversations: 8500,
          conversationsGrowth: -2,
          satisfaction: '4.2',
          satisfactionTrend: -0.1,
          monthlyConversations: 2800
        },
        features: {
          sso: false,
          api: false,
          analytics: false,
          whiteLabel: false
        },
        createdAt: '2023-11-10T11:30:00Z',
        lastActivity: '2024-01-10T12:00:00Z'
      }
    ]
    
    organizations.value = mockOrganizations
    
    // Calcular estadísticas
    stats.value = {
      total: mockOrganizations.length,
      active: mockOrganizations.filter(org => org.status === 'active').length,
      newThisMonth: 2,
      monthlyRevenue: mockOrganizations.reduce((sum, org) => sum + (org.plan?.price || 0), 0),
      revenueGrowth: 15.5,
      totalUsers: mockOrganizations.reduce((sum, org) => sum + (org.stats?.users || 0), 0)
    }
    
  } catch (error) {
    console.error('Error loading organizations:', error)
  } finally {
    isLoading.value = false
  }
}

const viewOrganizationDetails = (organization) => {
  router.push(`/dashboard/organizations/${organization.id}`)
}

const editOrganization = (organization) => {
  selectedOrganization.value = organization
  showEditModal.value = true
}

const manageOrganizationUsers = (organization) => {
  router.push(`/dashboard/organizations/${organization.id}/users`)
}

const viewOrganizationBilling = (organization) => {
  router.push(`/dashboard/organizations/${organization.id}/billing`)
}

const toggleOrganizationStatus = async (organization) => {
  try {
    const newStatus = organization.status === 'active' ? 'inactive' : 'active'
    
    // Aquí iría la llamada a la API
    console.log(`Toggling organization ${organization.id} status to ${newStatus}`)
    
    // Actualizar localmente
    organization.status = newStatus
    
  } catch (error) {
    console.error('Error toggling organization status:', error)
  }
}

const exportData = () => {
  // Implementar exportación de datos
  console.log('Exporting organization data...')
}

const closeModals = () => {
  showCreateModal.value = false
  showEditModal.value = false
  selectedOrganization.value = null
}

const handleSaveOrganization = async (organizationData) => {
  try {
    if (showEditModal.value) {
      // Actualizar organización existente
      const index = organizations.value.findIndex(org => org.id === selectedOrganization.value.id)
      if (index !== -1) {
        organizations.value[index] = { ...organizations.value[index], ...organizationData }
      }
    } else {
      // Crear nueva organización
      const newOrganization = {
        id: Date.now().toString(),
        ...organizationData,
        createdAt: new Date().toISOString(),
        lastActivity: new Date().toISOString()
      }
      organizations.value.unshift(newOrganization)
    }
    
    closeModals()
    
  } catch (error) {
    console.error('Error saving organization:', error)
  }
}

// Watchers
watch([filters], () => {
  currentPage.value = 1
}, { deep: true })

// Lifecycle
onMounted(() => {
  loadOrganizations()
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
.organization-management {
  min-height: calc(100vh - 200px);
}

/* Animaciones para las transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>