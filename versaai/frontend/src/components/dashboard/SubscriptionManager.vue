<template>
  <div class="subscription-manager bg-white rounded-lg shadow-sm border border-gray-200">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">Gestión de Suscripciones</h3>
          <p class="text-sm text-gray-600 mt-1">Administra planes, facturación y renovaciones</p>
        </div>
        <div class="flex items-center space-x-3">
          <button
            @click="refreshSubscriptions"
            :disabled="isLoading"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            <ArrowPathIcon :class="['w-4 h-4 mr-2', isLoading ? 'animate-spin' : '']" />
            Actualizar
          </button>
          <button
            @click="showUpgradeModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <PlusIcon class="w-4 h-4 mr-2" />
            Cambiar Plan
          </button>
        </div>
      </div>
    </div>

    <!-- Current Subscription -->
    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Plan Actual -->
        <div class="bg-gradient-to-br from-primary-50 to-primary-100 rounded-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-semibold text-gray-900">Plan Actual</h4>
            <span :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              currentSubscription.status === 'active' ? 'bg-green-100 text-green-800' :
              currentSubscription.status === 'trial' ? 'bg-blue-100 text-blue-800' :
              currentSubscription.status === 'expired' ? 'bg-red-100 text-red-800' :
              'bg-yellow-100 text-yellow-800'
            ]">
              {{ getStatusLabel(currentSubscription.status) }}
            </span>
          </div>
          
          <div class="space-y-3">
            <div>
              <div class="text-2xl font-bold text-gray-900">{{ currentSubscription.planName }}</div>
              <div class="text-sm text-gray-600">{{ currentSubscription.planDescription }}</div>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Precio:</span>
              <span class="text-lg font-semibold text-gray-900">
                ${{ currentSubscription.price }}/{{ currentSubscription.period }}
              </span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Próxima facturación:</span>
              <span class="text-sm font-medium text-gray-900">
                {{ formatDate(currentSubscription.nextBilling) }}
              </span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Renovación automática:</span>
              <button
                @click="toggleAutoRenewal"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                  currentSubscription.autoRenewal ? 'bg-primary-600' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    currentSubscription.autoRenewal ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
          </div>
        </div>

        <!-- Uso de Recursos -->
        <div class="bg-gray-50 rounded-lg p-6">
          <h4 class="text-lg font-semibold text-gray-900 mb-4">Uso de Recursos</h4>
          
          <div class="space-y-4">
            <div v-for="resource in resourceUsage" :key="resource.name">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">{{ resource.name }}</span>
                <span class="text-sm text-gray-600">
                  {{ resource.used }} / {{ resource.limit === -1 ? 'Ilimitado' : resource.limit }}
                </span>
              </div>
              
              <div v-if="resource.limit !== -1" class="w-full bg-gray-200 rounded-full h-2">
                <div
                  :class="[
                    'h-2 rounded-full transition-all duration-300',
                    resource.percentage >= 90 ? 'bg-red-500' :
                    resource.percentage >= 75 ? 'bg-yellow-500' :
                    'bg-green-500'
                  ]"
                  :style="{ width: `${Math.min(resource.percentage, 100)}%` }"
                ></div>
              </div>
              
              <div v-if="resource.limit !== -1 && resource.percentage >= 80" class="mt-1">
                <span class="text-xs text-orange-600">
                  ⚠️ Cerca del límite - considera actualizar tu plan
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Historial de Facturación -->
    <div class="px-6 pb-6">
      <div class="border-t border-gray-200 pt-6">
        <div class="flex items-center justify-between mb-4">
          <h4 class="text-lg font-semibold text-gray-900">Historial de Facturación</h4>
          <button
            @click="downloadInvoices"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
            Descargar Facturas
          </button>
        </div>
        
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
          <table class="min-w-full divide-y divide-gray-300">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fecha
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descripción
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Monto
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="invoice in billingHistory" :key="invoice.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(invoice.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ invoice.description }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ invoice.amount }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    invoice.status === 'paid' ? 'bg-green-100 text-green-800' :
                    invoice.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]">
                    {{ getInvoiceStatusLabel(invoice.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    @click="downloadInvoice(invoice.id)"
                    class="text-primary-600 hover:text-primary-900 mr-3"
                  >
                    Descargar
                  </button>
                  <button
                    v-if="invoice.status === 'failed'"
                    @click="retryPayment(invoice.id)"
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
    </div>

    <!-- Modal de Cambio de Plan -->
    <div v-if="showUpgradeModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showUpgradeModal = false"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Cambiar Plan de Suscripción
            </h3>
            
            <div class="space-y-3">
              <div v-for="plan in availablePlans" :key="plan.id" class="border rounded-lg p-4 cursor-pointer hover:bg-gray-50" @click="selectedPlan = plan">
                <div class="flex items-center">
                  <input
                    type="radio"
                    :value="plan.id"
                    v-model="selectedPlan.id"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                  >
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">{{ plan.name }}</div>
                    <div class="text-sm text-gray-500">${{ plan.price }}/{{ plan.period }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="changePlan"
              :disabled="!selectedPlan || isChangingPlan"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              {{ isChangingPlan ? 'Cambiando...' : 'Cambiar Plan' }}
            </button>
            <button
              @click="showUpgradeModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  ArrowPathIcon,
  PlusIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

// Estado reactivo
const isLoading = ref(false)
const showUpgradeModal = ref(false)
const selectedPlan = ref(null)
const isChangingPlan = ref(false)

// Datos de suscripción actual
const currentSubscription = ref({
  id: 'sub_123',
  planName: 'Plan Professional',
  planDescription: 'Perfecto para equipos en crecimiento',
  price: 49,
  period: 'mes',
  status: 'active',
  nextBilling: '2024-02-15',
  autoRenewal: true
})

// Uso de recursos
const resourceUsage = ref([
  {
    name: 'Usuarios',
    used: 8,
    limit: 10,
    percentage: 80
  },
  {
    name: 'Chatbots',
    used: 3,
    limit: 5,
    percentage: 60
  },
  {
    name: 'Conversaciones/mes',
    used: 1250,
    limit: 2000,
    percentage: 62.5
  },
  {
    name: 'Almacenamiento',
    used: 2.1,
    limit: 5,
    percentage: 42,
    unit: 'GB'
  }
])

// Historial de facturación
const billingHistory = ref([
  {
    id: 'inv_001',
    date: '2024-01-15',
    description: 'Plan Professional - Enero 2024',
    amount: 49,
    status: 'paid'
  },
  {
    id: 'inv_002',
    date: '2023-12-15',
    description: 'Plan Professional - Diciembre 2023',
    amount: 49,
    status: 'paid'
  },
  {
    id: 'inv_003',
    date: '2023-11-15',
    description: 'Plan Professional - Noviembre 2023',
    amount: 49,
    status: 'paid'
  }
])

// Planes disponibles
const availablePlans = ref([
  {
    id: 'basic',
    name: 'Plan Básico',
    price: 19,
    period: 'mes'
  },
  {
    id: 'professional',
    name: 'Plan Professional',
    price: 49,
    period: 'mes'
  },
  {
    id: 'premium',
    name: 'Plan Premium',
    price: 99,
    period: 'mes'
  },
  {
    id: 'enterprise',
    name: 'Plan Enterprise',
    price: 199,
    period: 'mes'
  }
])

// Métodos
const refreshSubscriptions = async () => {
  isLoading.value = true
  try {
    // Simular llamada a API
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Aquí iría la lógica para actualizar los datos
  } catch (error) {
    console.error('Error al actualizar suscripciones:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleAutoRenewal = async () => {
  try {
    currentSubscription.value.autoRenewal = !currentSubscription.value.autoRenewal
    // Aquí iría la llamada a la API para actualizar la configuración
  } catch (error) {
    console.error('Error al cambiar renovación automática:', error)
    // Revertir el cambio en caso de error
    currentSubscription.value.autoRenewal = !currentSubscription.value.autoRenewal
  }
}

const changePlan = async () => {
  if (!selectedPlan.value) return
  
  isChangingPlan.value = true
  try {
    // Simular cambio de plan
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Actualizar suscripción actual
    currentSubscription.value.planName = selectedPlan.value.name
    currentSubscription.value.price = selectedPlan.value.price
    currentSubscription.value.period = selectedPlan.value.period
    
    showUpgradeModal.value = false
    selectedPlan.value = null
  } catch (error) {
    console.error('Error al cambiar plan:', error)
  } finally {
    isChangingPlan.value = false
  }
}

const downloadInvoices = () => {
  // Lógica para descargar todas las facturas
  console.log('Descargando todas las facturas...')
}

const downloadInvoice = (invoiceId) => {
  // Lógica para descargar una factura específica
  console.log('Descargando factura:', invoiceId)
}

const retryPayment = async (invoiceId) => {
  try {
    // Lógica para reintentar el pago
    console.log('Reintentando pago para factura:', invoiceId)
  } catch (error) {
    console.error('Error al reintentar pago:', error)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    trial: 'Prueba',
    expired: 'Expirado',
    cancelled: 'Cancelado'
  }
  return labels[status] || status
}

const getInvoiceStatusLabel = (status) => {
  const labels = {
    paid: 'Pagado',
    pending: 'Pendiente',
    failed: 'Fallido'
  }
  return labels[status] || status
}

// Lifecycle
onMounted(() => {
  refreshSubscriptions()
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
.subscription-manager {
  min-height: 600px;
}

/* Animaciones para las barras de progreso */
.progress-bar {
  transition: width 0.3s ease-in-out;
}

/* Estilos para el modal */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>