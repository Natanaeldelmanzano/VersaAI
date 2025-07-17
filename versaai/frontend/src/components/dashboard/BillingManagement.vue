<template>
  <div class="billing-management">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Gestión de Facturación</h2>
        <p class="text-gray-600 mt-1">Administra suscripciones, pagos y facturación</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="exportBilling"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <DocumentArrowDownIcon class="w-4 h-4 mr-2" />
          Exportar
        </button>
        
        <button
          @click="openSubscriptionModal"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Nueva Suscripción
        </button>
      </div>
    </div>

    <!-- Revenue Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <CurrencyDollarIcon class="w-5 h-5 text-green-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Ingresos Mensuales</p>
            <p class="text-2xl font-bold text-gray-900">${{ formatCurrency(monthlyRevenue) }}</p>
            <p class="text-sm text-green-600 mt-1">+12.5% vs mes anterior</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <UsersIcon class="w-5 h-5 text-blue-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Suscriptores Activos</p>
            <p class="text-2xl font-bold text-gray-900">{{ activeSubscriptions }}</p>
            <p class="text-sm text-blue-600 mt-1">+8 nuevos este mes</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <ChartBarIcon class="w-5 h-5 text-purple-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">ARPU</p>
            <p class="text-2xl font-bold text-gray-900">${{ formatCurrency(arpu) }}</p>
            <p class="text-sm text-purple-600 mt-1">Ingreso promedio por usuario</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
              <ExclamationTriangleIcon class="w-5 h-5 text-orange-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Churn Rate</p>
            <p class="text-2xl font-bold text-gray-900">{{ churnRate }}%</p>
            <p class="text-sm text-orange-600 mt-1">-0.5% vs mes anterior</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Subscription Plans -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Planes de Suscripción</h3>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div 
            v-for="plan in subscriptionPlans" 
            :key="plan.id"
            class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
          >
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-gray-900">{{ plan.name }}</h4>
              <span 
                :class="[
                  'px-2 py-1 text-xs font-semibold rounded-full',
                  plan.status === 'active' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-gray-100 text-gray-800'
                ]"
              >
                {{ plan.status === 'active' ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
            
            <div class="mb-4">
              <span class="text-3xl font-bold text-gray-900">${{ plan.price }}</span>
              <span class="text-gray-600">/{{ plan.interval }}</span>
            </div>
            
            <ul class="space-y-2 mb-6">
              <li 
                v-for="feature in plan.features" 
                :key="feature"
                class="flex items-center text-sm text-gray-600"
              >
                <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
                {{ feature }}
              </li>
            </ul>
            
            <div class="flex items-center justify-between text-sm text-gray-600">
              <span>{{ plan.subscribers }} suscriptores</span>
              <button 
                @click="editPlan(plan)"
                class="text-primary-600 hover:text-primary-700"
              >
                Editar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-8">
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">Transacciones Recientes</h3>
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
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
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
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <UserIcon class="h-6 w-6 text-gray-600" />
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ transaction.customer_name }}</div>
                    <div class="text-sm text-gray-500">{{ transaction.customer_email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ transaction.plan_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ formatCurrency(transaction.amount) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    getTransactionStatusColor(transaction.status)
                  ]"
                >
                  {{ getTransactionStatusLabel(transaction.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(transaction.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button 
                    @click="viewTransaction(transaction)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <EyeIcon class="w-4 h-4" />
                  </button>
                  <button 
                    v-if="transaction.status === 'failed'"
                    @click="retryTransaction(transaction)"
                    class="text-green-600 hover:text-green-900"
                  >
                    <ArrowPathIcon class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Invoices Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">Facturas</h3>
        <button
          @click="generateInvoice"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <DocumentPlusIcon class="w-4 h-4 mr-2" />
          Generar Factura
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Número
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cliente
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
              v-for="invoice in invoices" 
              :key="invoice.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                #{{ invoice.number }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ invoice.customer_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ formatCurrency(invoice.amount) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    getInvoiceStatusColor(invoice.status)
                  ]"
                >
                  {{ getInvoiceStatusLabel(invoice.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(invoice.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button 
                    @click="downloadInvoice(invoice)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <DocumentArrowDownIcon class="w-4 h-4" />
                  </button>
                  <button 
                    @click="sendInvoice(invoice)"
                    class="text-green-600 hover:text-green-900"
                  >
                    <PaperAirplaneIcon class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  DocumentArrowDownIcon,
  PlusIcon,
  CurrencyDollarIcon,
  UsersIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckIcon,
  UserIcon,
  EyeIcon,
  ArrowPathIcon,
  DocumentPlusIcon,
  PaperAirplaneIcon
} from '@heroicons/vue/24/outline'

// State
const transactionFilter = ref('all')
const showSubscriptionModal = ref(false)

// Mock data
const monthlyRevenue = ref(45000)
const activeSubscriptions = ref(156)
const arpu = ref(288.46)
const churnRate = ref(2.3)

const subscriptionPlans = ref([
  {
    id: 1,
    name: 'Básico',
    price: 29,
    interval: 'mes',
    status: 'active',
    subscribers: 45,
    features: [
      '5 chatbots',
      '1,000 conversaciones/mes',
      'Soporte por email',
      'Integraciones básicas'
    ]
  },
  {
    id: 2,
    name: 'Profesional',
    price: 99,
    interval: 'mes',
    status: 'active',
    subscribers: 78,
    features: [
      '25 chatbots',
      '10,000 conversaciones/mes',
      'Soporte prioritario',
      'Todas las integraciones',
      'Analytics avanzados'
    ]
  },
  {
    id: 3,
    name: 'Empresarial',
    price: 299,
    interval: 'mes',
    status: 'active',
    subscribers: 33,
    features: [
      'Chatbots ilimitados',
      'Conversaciones ilimitadas',
      'Soporte 24/7',
      'API personalizada',
      'Implementación dedicada'
    ]
  }
])

const transactions = ref([
  {
    id: 1,
    customer_name: 'Acme Corp',
    customer_email: 'billing@acme.com',
    plan_name: 'Profesional',
    amount: 99.00,
    status: 'successful',
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: 2,
    customer_name: 'TechStart Inc',
    customer_email: 'finance@techstart.com',
    plan_name: 'Empresarial',
    amount: 299.00,
    status: 'successful',
    created_at: '2024-01-14T15:45:00Z'
  },
  {
    id: 3,
    customer_name: 'Global Solutions',
    customer_email: 'payments@global.com',
    plan_name: 'Básico',
    amount: 29.00,
    status: 'failed',
    created_at: '2024-01-13T09:15:00Z'
  },
  {
    id: 4,
    customer_name: 'Innovation Labs',
    customer_email: 'billing@innovation.com',
    plan_name: 'Profesional',
    amount: 99.00,
    status: 'pending',
    created_at: '2024-01-12T14:20:00Z'
  }
])

const invoices = ref([
  {
    id: 1,
    number: 'INV-2024-001',
    customer_name: 'Acme Corp',
    amount: 99.00,
    status: 'paid',
    created_at: '2024-01-15T10:30:00Z'
  },
  {
    id: 2,
    number: 'INV-2024-002',
    customer_name: 'TechStart Inc',
    amount: 299.00,
    status: 'paid',
    created_at: '2024-01-14T15:45:00Z'
  },
  {
    id: 3,
    number: 'INV-2024-003',
    customer_name: 'Global Solutions',
    amount: 29.00,
    status: 'overdue',
    created_at: '2024-01-13T09:15:00Z'
  },
  {
    id: 4,
    number: 'INV-2024-004',
    customer_name: 'Innovation Labs',
    amount: 99.00,
    status: 'sent',
    created_at: '2024-01-12T14:20:00Z'
  }
])

// Computed
const filteredTransactions = computed(() => {
  if (transactionFilter.value === 'all') {
    return transactions.value
  }
  return transactions.value.filter(t => t.status === transactionFilter.value)
})

// Methods
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getTransactionStatusColor = (status) => {
  const colors = {
    successful: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    pending: 'bg-yellow-100 text-yellow-800'
  }
  return colors[status] || colors.pending
}

const getTransactionStatusLabel = (status) => {
  const labels = {
    successful: 'Exitosa',
    failed: 'Fallida',
    pending: 'Pendiente'
  }
  return labels[status] || status
}

const getInvoiceStatusColor = (status) => {
  const colors = {
    paid: 'bg-green-100 text-green-800',
    sent: 'bg-blue-100 text-blue-800',
    overdue: 'bg-red-100 text-red-800',
    draft: 'bg-gray-100 text-gray-800'
  }
  return colors[status] || colors.draft
}

const getInvoiceStatusLabel = (status) => {
  const labels = {
    paid: 'Pagada',
    sent: 'Enviada',
    overdue: 'Vencida',
    draft: 'Borrador'
  }
  return labels[status] || status
}

const exportBilling = () => {
  // Implement billing export
  console.log('Exporting billing data...')
}

const openSubscriptionModal = () => {
  showSubscriptionModal.value = true
}

const editPlan = (plan) => {
  console.log('Editing plan:', plan)
}

const viewTransaction = (transaction) => {
  console.log('Viewing transaction:', transaction)
}

const retryTransaction = (transaction) => {
  console.log('Retrying transaction:', transaction)
}

const generateInvoice = () => {
  console.log('Generating new invoice...')
}

const downloadInvoice = (invoice) => {
  console.log('Downloading invoice:', invoice)
}

const sendInvoice = (invoice) => {
  console.log('Sending invoice:', invoice)
}

// Lifecycle
onMounted(() => {
  // Load billing data
})
</script>

<style scoped>
.billing-management {
  @apply p-6;
}
</style>