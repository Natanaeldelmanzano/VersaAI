<template>
  <div class="payment-gateway bg-white rounded-lg shadow-sm border border-gray-200">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">Pasarela de Pagos</h3>
          <p class="text-sm text-gray-600 mt-1">Gestiona métodos de pago y transacciones</p>
        </div>
        <div class="flex items-center space-x-3">
          <span :class="[
            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
            gatewayStatus === 'active' ? 'bg-green-100 text-green-800' :
            gatewayStatus === 'maintenance' ? 'bg-yellow-100 text-yellow-800' :
            'bg-red-100 text-red-800'
          ]">
            <span :class="[
              'w-1.5 h-1.5 rounded-full mr-1.5',
              gatewayStatus === 'active' ? 'bg-green-400' :
              gatewayStatus === 'maintenance' ? 'bg-yellow-400' :
              'bg-red-400'
            ]"></span>
            {{ getGatewayStatusLabel(gatewayStatus) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Payment Methods -->
    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Métodos de Pago Guardados -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-lg font-semibold text-gray-900">Métodos de Pago</h4>
            <button
              @click="showAddPaymentModal = true"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              Agregar Método
            </button>
          </div>
          
          <div class="space-y-3">
            <div v-for="method in paymentMethods" :key="method.id" class="border rounded-lg p-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="flex-shrink-0">
                    <CreditCardIcon v-if="method.type === 'card'" class="w-6 h-6 text-gray-400" />
                    <BanknotesIcon v-else-if="method.type === 'bank'" class="w-6 h-6 text-gray-400" />
                    <DevicePhoneMobileIcon v-else class="w-6 h-6 text-gray-400" />
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ method.name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ method.details }}
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2">
                  <span v-if="method.isDefault" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                    Por defecto
                  </span>
                  <div class="relative">
                    <button
                      @click="toggleMethodMenu(method.id)"
                      class="p-1 rounded-full hover:bg-gray-100"
                    >
                      <EllipsisVerticalIcon class="w-4 h-4 text-gray-400" />
                    </button>
                    
                    <!-- Dropdown Menu -->
                    <div v-if="activeMethodMenu === method.id" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-10">
                      <div class="py-1">
                        <button
                          v-if="!method.isDefault"
                          @click="setDefaultMethod(method.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Establecer como predeterminado
                        </button>
                        <button
                          @click="editPaymentMethod(method.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          Editar
                        </button>
                        <button
                          @click="deletePaymentMethod(method.id)"
                          class="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50"
                        >
                          Eliminar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="paymentMethods.length === 0" class="text-center py-8">
              <CreditCardIcon class="mx-auto h-12 w-12 text-gray-400" />
              <h3 class="mt-2 text-sm font-medium text-gray-900">No hay métodos de pago</h3>
              <p class="mt-1 text-sm text-gray-500">Agrega un método de pago para comenzar.</p>
            </div>
          </div>
        </div>

        <!-- Configuración de Pagos -->
        <div>
          <h4 class="text-lg font-semibold text-gray-900 mb-4">Configuración</h4>
          
          <div class="space-y-4">
            <!-- Moneda -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Moneda predeterminada
              </label>
              <select
                v-model="paymentConfig.currency"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="USD">USD - Dólar Estadounidense</option>
                <option value="EUR">EUR - Euro</option>
                <option value="GBP">GBP - Libra Esterlina</option>
                <option value="MXN">MXN - Peso Mexicano</option>
                <option value="COP">COP - Peso Colombiano</option>
              </select>
            </div>
            
            <!-- Facturación automática -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">Facturación automática</label>
                <p class="text-sm text-gray-500">Cobrar automáticamente en la fecha de renovación</p>
              </div>
              <button
                @click="paymentConfig.autoBilling = !paymentConfig.autoBilling"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                  paymentConfig.autoBilling ? 'bg-primary-600' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    paymentConfig.autoBilling ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
            
            <!-- Recordatorios de pago -->
            <div class="flex items-center justify-between">
              <div>
                <label class="text-sm font-medium text-gray-700">Recordatorios de pago</label>
                <p class="text-sm text-gray-500">Enviar recordatorios antes del vencimiento</p>
              </div>
              <button
                @click="paymentConfig.paymentReminders = !paymentConfig.paymentReminders"
                :class="[
                  'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
                  paymentConfig.paymentReminders ? 'bg-primary-600' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    paymentConfig.paymentReminders ? 'translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
            
            <!-- Días de recordatorio -->
            <div v-if="paymentConfig.paymentReminders">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Días antes del vencimiento
              </label>
              <select
                v-model="paymentConfig.reminderDays"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                <option value="1">1 día</option>
                <option value="3">3 días</option>
                <option value="7">7 días</option>
                <option value="14">14 días</option>
              </select>
            </div>
          </div>
          
          <div class="mt-6">
            <button
              @click="savePaymentConfig"
              :disabled="isSavingConfig"
              class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              {{ isSavingConfig ? 'Guardando...' : 'Guardar Configuración' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Transacciones Recientes -->
    <div class="px-6 pb-6">
      <div class="border-t border-gray-200 pt-6">
        <div class="flex items-center justify-between mb-4">
          <h4 class="text-lg font-semibold text-gray-900">Transacciones Recientes</h4>
          <button
            @click="exportTransactions"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
            Exportar
          </button>
        </div>
        
        <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
          <table class="min-w-full divide-y divide-gray-300">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  ID Transacción
                </th>
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
                  Método
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="transaction in recentTransactions" :key="transaction.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
                  {{ transaction.id }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.description }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ transaction.amount }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    transaction.status === 'completed' ? 'bg-green-100 text-green-800' :
                    transaction.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    transaction.status === 'failed' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ getTransactionStatusLabel(transaction.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ transaction.paymentMethod }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Agregar Método de Pago -->
    <div v-if="showAddPaymentModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showAddPaymentModal = false"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Agregar Método de Pago
            </h3>
            
            <form @submit.prevent="addPaymentMethod">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de método
                  </label>
                  <select
                    v-model="newPaymentMethod.type"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="card">Tarjeta de Crédito/Débito</option>
                    <option value="bank">Cuenta Bancaria</option>
                    <option value="paypal">PayPal</option>
                  </select>
                </div>
                
                <div v-if="newPaymentMethod.type === 'card'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Número de tarjeta
                  </label>
                  <input
                    type="text"
                    v-model="newPaymentMethod.cardNumber"
                    placeholder="**** **** **** 1234"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Nombre del método
                  </label>
                  <input
                    type="text"
                    v-model="newPaymentMethod.name"
                    placeholder="Ej: Tarjeta principal"
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                </div>
                
                <div class="flex items-center">
                  <input
                    type="checkbox"
                    v-model="newPaymentMethod.setAsDefault"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  >
                  <label class="ml-2 block text-sm text-gray-900">
                    Establecer como método predeterminado
                  </label>
                </div>
              </div>
            </form>
          </div>
          
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="addPaymentMethod"
              :disabled="isAddingMethod"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              {{ isAddingMethod ? 'Agregando...' : 'Agregar Método' }}
            </button>
            <button
              @click="showAddPaymentModal = false"
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  PlusIcon,
  CreditCardIcon,
  BanknotesIcon,
  DevicePhoneMobileIcon,
  EllipsisVerticalIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

// Estado reactivo
const gatewayStatus = ref('active')
const showAddPaymentModal = ref(false)
const activeMethodMenu = ref(null)
const isSavingConfig = ref(false)
const isAddingMethod = ref(false)

// Métodos de pago
const paymentMethods = ref([
  {
    id: 'pm_001',
    type: 'card',
    name: 'Tarjeta Principal',
    details: '**** **** **** 1234',
    isDefault: true
  },
  {
    id: 'pm_002',
    type: 'bank',
    name: 'Cuenta Bancaria',
    details: 'Banco XYZ - ****5678',
    isDefault: false
  }
])

// Configuración de pagos
const paymentConfig = ref({
  currency: 'USD',
  autoBilling: true,
  paymentReminders: true,
  reminderDays: '7'
})

// Nuevo método de pago
const newPaymentMethod = ref({
  type: 'card',
  name: '',
  cardNumber: '',
  setAsDefault: false
})

// Transacciones recientes
const recentTransactions = ref([
  {
    id: 'txn_001',
    date: '2024-01-15',
    description: 'Plan Professional - Enero 2024',
    amount: 49,
    status: 'completed',
    paymentMethod: '**** 1234'
  },
  {
    id: 'txn_002',
    date: '2024-01-10',
    description: 'Upgrade a Premium',
    amount: 50,
    status: 'completed',
    paymentMethod: '**** 1234'
  },
  {
    id: 'txn_003',
    date: '2024-01-05',
    description: 'Funcionalidad adicional',
    amount: 15,
    status: 'pending',
    paymentMethod: '**** 5678'
  }
])

// Métodos
const toggleMethodMenu = (methodId) => {
  activeMethodMenu.value = activeMethodMenu.value === methodId ? null : methodId
}

const setDefaultMethod = async (methodId) => {
  try {
    // Actualizar método predeterminado
    paymentMethods.value.forEach(method => {
      method.isDefault = method.id === methodId
    })
    activeMethodMenu.value = null
  } catch (error) {
    console.error('Error al establecer método predeterminado:', error)
  }
}

const editPaymentMethod = (methodId) => {
  // Lógica para editar método de pago
  console.log('Editando método:', methodId)
  activeMethodMenu.value = null
}

const deletePaymentMethod = async (methodId) => {
  try {
    const index = paymentMethods.value.findIndex(method => method.id === methodId)
    if (index > -1) {
      paymentMethods.value.splice(index, 1)
    }
    activeMethodMenu.value = null
  } catch (error) {
    console.error('Error al eliminar método de pago:', error)
  }
}

const addPaymentMethod = async () => {
  if (!newPaymentMethod.value.name) return
  
  isAddingMethod.value = true
  try {
    // Simular agregado de método
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const newMethod = {
      id: `pm_${Date.now()}`,
      type: newPaymentMethod.value.type,
      name: newPaymentMethod.value.name,
      details: newPaymentMethod.value.type === 'card' ? newPaymentMethod.value.cardNumber : 'Configurado',
      isDefault: newPaymentMethod.value.setAsDefault
    }
    
    if (newPaymentMethod.value.setAsDefault) {
      paymentMethods.value.forEach(method => {
        method.isDefault = false
      })
    }
    
    paymentMethods.value.push(newMethod)
    
    // Reset form
    newPaymentMethod.value = {
      type: 'card',
      name: '',
      cardNumber: '',
      setAsDefault: false
    }
    
    showAddPaymentModal.value = false
  } catch (error) {
    console.error('Error al agregar método de pago:', error)
  } finally {
    isAddingMethod.value = false
  }
}

const savePaymentConfig = async () => {
  isSavingConfig.value = true
  try {
    // Simular guardado de configuración
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Aquí iría la llamada a la API
  } catch (error) {
    console.error('Error al guardar configuración:', error)
  } finally {
    isSavingConfig.value = false
  }
}

const exportTransactions = () => {
  // Lógica para exportar transacciones
  console.log('Exportando transacciones...')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getGatewayStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    maintenance: 'Mantenimiento',
    inactive: 'Inactivo'
  }
  return labels[status] || status
}

const getTransactionStatusLabel = (status) => {
  const labels = {
    completed: 'Completado',
    pending: 'Pendiente',
    failed: 'Fallido',
    refunded: 'Reembolsado'
  }
  return labels[status] || status
}

// Cerrar menús al hacer clic fuera
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeMethodMenu.value = null
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
/* Estilos adicionales */
.payment-gateway {
  min-height: 600px;
}

/* Animaciones para dropdowns */
.dropdown-enter-active, .dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Estilos para inputs de tarjeta */
input[type="text"]:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .payment-gateway .grid {
    grid-template-columns: 1fr;
  }
}
</style>