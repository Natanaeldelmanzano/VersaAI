<template>
  <div class="monetization-system">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Sistema de Monetización</h2>
        <p class="text-gray-600 mt-2">Gestiona planes, suscripciones y facturación</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="showCreatePlanModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Crear Plan
        </button>
        
        <button
          @click="exportRevenue"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <DocumentArrowDownIcon class="w-4 h-4 mr-2" />
          Exportar
        </button>
      </div>
    </div>

    <!-- Revenue Overview -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Ingresos Mensuales</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">${{ monthlyRevenue.toLocaleString() }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+12.5%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <CurrencyDollarIcon class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Suscriptores Activos</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ activeSubscribers.toLocaleString() }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+8.3%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <UsersIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">ARPU</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">${{ arpu }}</p>
            <div class="flex items-center mt-2">
              <ArrowUpIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">+5.2%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <ChartBarIcon class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Tasa de Churn</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ churnRate }}%</p>
            <div class="flex items-center mt-2">
              <ArrowDownIcon class="w-4 h-4 text-green-600 mr-1" />
              <span class="text-sm font-medium text-green-600">-1.2%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
            <ExclamationTriangleIcon class="w-6 h-6 text-red-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Revenue Chart -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-semibold text-gray-900">Tendencia de Ingresos</h3>
        <div class="flex items-center space-x-4">
          <select 
            v-model="revenueChartPeriod"
            class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="7d">Últimos 7 días</option>
            <option value="30d">Últimos 30 días</option>
            <option value="90d">Últimos 90 días</option>
            <option value="1y">Último año</option>
          </select>
        </div>
      </div>
      <div class="h-80">
        <RevenueChart 
          :data="revenueChartData" 
          :loading="isLoadingChart"
          :period="revenueChartPeriod"
        />
      </div>
    </div>

    <!-- Subscription Plans -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Planes de Suscripción</h3>
          <button
            @click="showCreatePlanModal = true"
            class="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Agregar Plan
          </button>
        </div>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="plan in subscriptionPlans" 
            :key="plan.id"
            class="border border-gray-200 rounded-xl p-6 hover:shadow-md transition-shadow relative"
            :class="{ 'border-primary-500 bg-primary-50': plan.featured }"
          >
            <!-- Featured Badge -->
            <div v-if="plan.featured" class="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <span class="bg-primary-600 text-white px-3 py-1 rounded-full text-xs font-medium">
                Más Popular
              </span>
            </div>
            
            <div class="text-center">
              <h4 class="text-xl font-bold text-gray-900 mb-2">{{ plan.name }}</h4>
              <div class="mb-4">
                <span class="text-4xl font-bold text-gray-900">${{ plan.price }}</span>
                <span class="text-gray-600">{{ plan.interval }}</span>
              </div>
              <p class="text-gray-600 text-sm mb-6">{{ plan.description }}</p>
              
              <!-- Features -->
              <ul class="space-y-3 mb-6">
                <li 
                  v-for="feature in plan.features" 
                  :key="feature"
                  class="flex items-center text-sm text-gray-700"
                >
                  <CheckIcon class="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                  {{ feature }}
                </li>
              </ul>
              
              <!-- Stats -->
              <div class="grid grid-cols-2 gap-4 mb-6">
                <div class="text-center p-3 bg-gray-50 rounded-lg">
                  <p class="text-2xl font-bold text-gray-900">{{ plan.subscribers }}</p>
                  <p class="text-xs text-gray-600">Suscriptores</p>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded-lg">
                  <p class="text-2xl font-bold text-gray-900">${{ (plan.price * plan.subscribers).toLocaleString() }}</p>
                  <p class="text-xs text-gray-600">MRR</p>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex space-x-2">
                <button
                  @click="editPlan(plan)"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Editar
                </button>
                <button
                  @click="viewPlanAnalytics(plan)"
                  class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700"
                >
                  Analytics
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">Transacciones Recientes</h3>
          <div class="flex items-center space-x-4">
            <select 
              v-model="transactionFilter"
              class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option value="all">Todas</option>
              <option value="successful">Exitosas</option>
              <option value="failed">Fallidas</option>
              <option value="pending">Pendientes</option>
            </select>
          </div>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cliente
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Plan
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Monto
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fecha
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="transaction in filteredTransactions" 
              :key="transaction.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <img 
                    :src="transaction.customer.avatar" 
                    :alt="transaction.customer.name"
                    class="w-8 h-8 rounded-full mr-3"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ transaction.customer.name }}</div>
                    <div class="text-sm text-gray-500">{{ transaction.customer.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm text-gray-900">{{ transaction.plan }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm font-medium text-gray-900">${{ transaction.amount }}</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="[
                  'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                  transaction.status === 'successful' ? 'bg-green-100 text-green-800' :
                  transaction.status === 'failed' ? 'bg-red-100 text-red-800' :
                  transaction.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                ]">
                  {{ getStatusLabel(transaction.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(transaction.date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewTransaction(transaction)"
                  class="text-primary-600 hover:text-primary-900 mr-3"
                >
                  Ver
                </button>
                <button
                  v-if="transaction.status === 'failed'"
                  @click="retryTransaction(transaction)"
                  class="text-green-600 hover:text-green-900"
                >
                  Reintentar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Payment Gateway Status -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Estado de Pasarelas de Pago</h3>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div 
            v-for="gateway in paymentGateways" 
            :key="gateway.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <img :src="gateway.logo" :alt="gateway.name" class="w-8 h-8" />
                <h4 class="font-medium text-gray-900">{{ gateway.name }}</h4>
              </div>
              <span :class="[
                'w-3 h-3 rounded-full',
                gateway.status === 'active' ? 'bg-green-500' : 'bg-red-500'
              ]"></span>
            </div>
            
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Transacciones hoy:</span>
                <span class="font-medium">{{ gateway.todayTransactions }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Tasa de éxito:</span>
                <span class="font-medium text-green-600">{{ gateway.successRate }}%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Comisión:</span>
                <span class="font-medium">{{ gateway.fee }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Plan Modal -->
    <PlanModal
      v-if="showCreatePlanModal"
      :show="showCreatePlanModal"
      @close="showCreatePlanModal = false"
      @save="handleCreatePlan"
    />

    <!-- Edit Plan Modal -->
    <PlanModal
      v-if="showEditPlanModal"
      :show="showEditPlanModal"
      :plan="selectedPlan"
      @close="showEditPlanModal = false"
      @save="handleEditPlan"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  PlusIcon,
  DocumentArrowDownIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'
import RevenueChart from './charts/RevenueChart.vue'
import PlanModal from './modals/PlanModal.vue'

// State
const isLoadingChart = ref(false)
const revenueChartPeriod = ref('30d')
const transactionFilter = ref('all')
const showCreatePlanModal = ref(false)
const showEditPlanModal = ref(false)
const selectedPlan = ref(null)

// Mock data
const monthlyRevenue = ref(125000)
const activeSubscribers = ref(1250)
const arpu = ref(100)
const churnRate = ref(2.3)

const subscriptionPlans = ref([
  {
    id: 1,
    name: 'Básico',
    price: 29,
    interval: '/mes',
    description: 'Perfecto para equipos pequeños',
    features: [
      'Hasta 5 chatbots',
      '1,000 conversaciones/mes',
      'Soporte por email',
      'Integraciones básicas'
    ],
    subscribers: 450,
    featured: false
  },
  {
    id: 2,
    name: 'Profesional',
    price: 99,
    interval: '/mes',
    description: 'Para empresas en crecimiento',
    features: [
      'Hasta 20 chatbots',
      '10,000 conversaciones/mes',
      'Soporte prioritario',
      'Todas las integraciones',
      'Analytics avanzados'
    ],
    subscribers: 650,
    featured: true
  },
  {
    id: 3,
    name: 'Enterprise',
    price: 299,
    interval: '/mes',
    description: 'Para grandes organizaciones',
    features: [
      'Chatbots ilimitados',
      'Conversaciones ilimitadas',
      'Soporte 24/7',
      'SSO y seguridad avanzada',
      'API personalizada',
      'Manager dedicado'
    ],
    subscribers: 150,
    featured: false
  }
])

const transactions = ref([
  {
    id: 1,
    customer: {
      name: 'Empresa ABC',
      email: 'admin@empresaabc.com',
      avatar: 'https://ui-avatars.com/api/?name=Empresa+ABC&background=3B82F6&color=fff'
    },
    plan: 'Profesional',
    amount: 99,
    status: 'successful',
    date: new Date('2024-01-15')
  },
  {
    id: 2,
    customer: {
      name: 'TechCorp',
      email: 'billing@techcorp.com',
      avatar: 'https://ui-avatars.com/api/?name=TechCorp&background=10B981&color=fff'
    },
    plan: 'Enterprise',
    amount: 299,
    status: 'successful',
    date: new Date('2024-01-14')
  },
  {
    id: 3,
    customer: {
      name: 'StartupXYZ',
      email: 'founder@startupxyz.com',
      avatar: 'https://ui-avatars.com/api/?name=StartupXYZ&background=F59E0B&color=fff'
    },
    plan: 'Básico',
    amount: 29,
    status: 'failed',
    date: new Date('2024-01-13')
  }
])

const paymentGateways = ref([
  {
    id: 1,
    name: 'Stripe',
    logo: 'https://stripe.com/img/v3/home/social.png',
    status: 'active',
    todayTransactions: 45,
    successRate: 98.5,
    fee: 2.9
  },
  {
    id: 2,
    name: 'PayPal',
    logo: 'https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg',
    status: 'active',
    todayTransactions: 23,
    successRate: 96.2,
    fee: 3.4
  },
  {
    id: 3,
    name: 'Square',
    logo: 'https://squareup.com/us/en/press/assets/square-logo-black.png',
    status: 'inactive',
    todayTransactions: 0,
    successRate: 0,
    fee: 2.6
  }
])

// Computed
const filteredTransactions = computed(() => {
  if (transactionFilter.value === 'all') {
    return transactions.value
  }
  return transactions.value.filter(t => t.status === transactionFilter.value)
})

const revenueChartData = computed(() => ({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Ingresos Recurrentes',
      data: [85000, 92000, 98000, 105000, 118000, 125000],
      borderColor: '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4
    },
    {
      label: 'Ingresos Únicos',
      data: [15000, 18000, 22000, 25000, 28000, 32000],
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    }
  ]
}))

// Methods
const exportRevenue = () => {
  // TODO: Implement revenue export
  console.log('Exporting revenue data...')
}

const editPlan = (plan) => {
  selectedPlan.value = plan
  showEditPlanModal.value = true
}

const viewPlanAnalytics = (plan) => {
  // TODO: Navigate to plan analytics
  console.log('View analytics for plan:', plan.name)
}

const viewTransaction = (transaction) => {
  // TODO: Show transaction details
  console.log('View transaction:', transaction.id)
}

const retryTransaction = (transaction) => {
  // TODO: Retry failed transaction
  console.log('Retry transaction:', transaction.id)
}

const handleCreatePlan = (planData) => {
  const newPlan = {
    id: Date.now(),
    ...planData,
    subscribers: 0,
    featured: false
  }
  subscriptionPlans.value.push(newPlan)
  showCreatePlanModal.value = false
}

const handleEditPlan = (planData) => {
  const index = subscriptionPlans.value.findIndex(p => p.id === selectedPlan.value.id)
  if (index > -1) {
    subscriptionPlans.value[index] = { ...subscriptionPlans.value[index], ...planData }
  }
  showEditPlanModal.value = false
  selectedPlan.value = null
}

const getStatusLabel = (status) => {
  const labels = {
    successful: 'Exitosa',
    failed: 'Fallida',
    pending: 'Pendiente'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

// Lifecycle
onMounted(() => {
  // Load initial data
})
</script>

<style scoped>
.monetization-system {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>