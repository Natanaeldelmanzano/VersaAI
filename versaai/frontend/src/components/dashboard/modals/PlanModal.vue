<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
        @click="closeModal"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isEditing ? 'Editar Plan' : 'Crear Nuevo Plan' }}
          </h3>
          <button
            @click="closeModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                Nombre del Plan *
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Ej: Plan Profesional"
              />
            </div>

            <div>
              <label for="type" class="block text-sm font-medium text-gray-700 mb-2">
                Tipo de Plan *
              </label>
              <select
                id="type"
                v-model="form.type"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Seleccionar tipo</option>
                <option value="free">Gratuito</option>
                <option value="basic">Básico</option>
                <option value="professional">Profesional</option>
                <option value="enterprise">Empresarial</option>
                <option value="custom">Personalizado</option>
              </select>
            </div>
          </div>

          <!-- Pricing -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label for="price" class="block text-sm font-medium text-gray-700 mb-2">
                Precio *
              </label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
                <input
                  id="price"
                  v-model.number="form.price"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  class="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="0.00"
                />
              </div>
            </div>

            <div>
              <label for="billingCycle" class="block text-sm font-medium text-gray-700 mb-2">
                Ciclo de Facturación *
              </label>
              <select
                id="billingCycle"
                v-model="form.billingCycle"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="monthly">Mensual</option>
                <option value="quarterly">Trimestral</option>
                <option value="yearly">Anual</option>
                <option value="lifetime">De por vida</option>
              </select>
            </div>

            <div>
              <label for="currency" class="block text-sm font-medium text-gray-700 mb-2">
                Moneda
              </label>
              <select
                id="currency"
                v-model="form.currency"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="USD">USD - Dólar</option>
                <option value="EUR">EUR - Euro</option>
                <option value="MXN">MXN - Peso Mexicano</option>
                <option value="COP">COP - Peso Colombiano</option>
                <option value="ARS">ARS - Peso Argentino</option>
              </select>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
              Descripción
            </label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="Describe las características y beneficios del plan..."
            ></textarea>
          </div>

          <!-- Features -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Características del Plan
            </label>
            <div class="space-y-3">
              <div v-for="(feature, index) in form.features" :key="index" class="flex items-center space-x-3">
                <input
                  v-model="feature.name"
                  type="text"
                  placeholder="Nombre de la característica"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
                <input
                  v-model="feature.limit"
                  type="text"
                  placeholder="Límite (ej: 1000, Ilimitado)"
                  class="w-32 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                />
                <button
                  type="button"
                  @click="removeFeature(index)"
                  class="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
                >
                  <TrashIcon class="w-4 h-4" />
                </button>
              </div>
              <button
                type="button"
                @click="addFeature"
                class="flex items-center text-sm text-primary-600 hover:text-primary-800"
              >
                <PlusIcon class="w-4 h-4 mr-1" />
                Agregar característica
              </button>
            </div>
          </div>

          <!-- Limits and Quotas -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-4">Límites y Cuotas</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label for="maxUsers" class="block text-sm font-medium text-gray-700 mb-1">
                  Máximo de Usuarios
                </label>
                <input
                  id="maxUsers"
                  v-model.number="form.limits.maxUsers"
                  type="number"
                  min="1"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Ilimitado"
                />
              </div>
              
              <div>
                <label for="maxConversations" class="block text-sm font-medium text-gray-700 mb-1">
                  Conversaciones/Mes
                </label>
                <input
                  id="maxConversations"
                  v-model.number="form.limits.maxConversations"
                  type="number"
                  min="1"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Ilimitado"
                />
              </div>
              
              <div>
                <label for="maxStorage" class="block text-sm font-medium text-gray-700 mb-1">
                  Almacenamiento (GB)
                </label>
                <input
                  id="maxStorage"
                  v-model.number="form.limits.maxStorage"
                  type="number"
                  min="1"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Ilimitado"
                />
              </div>
              
              <div>
                <label for="maxIntegrations" class="block text-sm font-medium text-gray-700 mb-1">
                  Integraciones
                </label>
                <input
                  id="maxIntegrations"
                  v-model.number="form.limits.maxIntegrations"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Ilimitado"
                />
              </div>
              
              <div>
                <label for="maxApiCalls" class="block text-sm font-medium text-gray-700 mb-1">
                  Llamadas API/Mes
                </label>
                <input
                  id="maxApiCalls"
                  v-model.number="form.limits.maxApiCalls"
                  type="number"
                  min="1"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Ilimitado"
                />
              </div>
              
              <div>
                <label for="supportLevel" class="block text-sm font-medium text-gray-700 mb-1">
                  Nivel de Soporte
                </label>
                <select
                  id="supportLevel"
                  v-model="form.limits.supportLevel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="community">Comunidad</option>
                  <option value="email">Email</option>
                  <option value="priority">Prioritario</option>
                  <option value="dedicated">Dedicado</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Advanced Features -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-4">Características Avanzadas</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-3">
                <div class="flex items-center">
                  <input
                    id="hasAnalytics"
                    v-model="form.advancedFeatures.hasAnalytics"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasAnalytics" class="ml-2 text-sm text-gray-700">
                    Analytics Avanzados
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasCustomBranding"
                    v-model="form.advancedFeatures.hasCustomBranding"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasCustomBranding" class="ml-2 text-sm text-gray-700">
                    Marca Personalizada
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasApiAccess"
                    v-model="form.advancedFeatures.hasApiAccess"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasApiAccess" class="ml-2 text-sm text-gray-700">
                    Acceso a API
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasSSO"
                    v-model="form.advancedFeatures.hasSSO"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasSSO" class="ml-2 text-sm text-gray-700">
                    Single Sign-On (SSO)
                  </label>
                </div>
              </div>
              
              <div class="space-y-3">
                <div class="flex items-center">
                  <input
                    id="hasWebhooks"
                    v-model="form.advancedFeatures.hasWebhooks"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasWebhooks" class="ml-2 text-sm text-gray-700">
                    Webhooks
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasAdvancedSecurity"
                    v-model="form.advancedFeatures.hasAdvancedSecurity"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasAdvancedSecurity" class="ml-2 text-sm text-gray-700">
                    Seguridad Avanzada
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasDataExport"
                    v-model="form.advancedFeatures.hasDataExport"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasDataExport" class="ml-2 text-sm text-gray-700">
                    Exportación de Datos
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="hasPrioritySupport"
                    v-model="form.advancedFeatures.hasPrioritySupport"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="hasPrioritySupport" class="ml-2 text-sm text-gray-700">
                    Soporte Prioritario
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Status and Visibility -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
                Estado
              </label>
              <select
                id="status"
                v-model="form.status"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="draft">Borrador</option>
                <option value="archived">Archivado</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Opciones
              </label>
              <div class="space-y-2">
                <div class="flex items-center">
                  <input
                    id="isPopular"
                    v-model="form.isPopular"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="isPopular" class="ml-2 text-sm text-gray-700">
                    Marcar como popular
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input
                    id="isVisible"
                    v-model="form.isVisible"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="isVisible" class="ml-2 text-sm text-gray-700">
                    Visible en la página de precios
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
            <button
              type="button"
              @click="closeModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isSubmitting" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Guardando...
              </span>
              <span v-else>
                {{ isEditing ? 'Actualizar Plan' : 'Crear Plan' }}
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { XMarkIcon, PlusIcon, TrashIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  plan: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// State
const isSubmitting = ref(false)

// Form data
const form = ref({
  name: '',
  type: '',
  price: 0,
  billingCycle: 'monthly',
  currency: 'USD',
  description: '',
  features: [
    { name: '', limit: '' }
  ],
  limits: {
    maxUsers: null,
    maxConversations: null,
    maxStorage: null,
    maxIntegrations: null,
    maxApiCalls: null,
    supportLevel: 'email'
  },
  advancedFeatures: {
    hasAnalytics: false,
    hasCustomBranding: false,
    hasApiAccess: false,
    hasSSO: false,
    hasWebhooks: false,
    hasAdvancedSecurity: false,
    hasDataExport: false,
    hasPrioritySupport: false
  },
  status: 'active',
  isPopular: false,
  isVisible: true
})

// Computed
const isEditing = computed(() => !!props.plan)

// Methods
const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  form.value = {
    name: '',
    type: '',
    price: 0,
    billingCycle: 'monthly',
    currency: 'USD',
    description: '',
    features: [
      { name: '', limit: '' }
    ],
    limits: {
      maxUsers: null,
      maxConversations: null,
      maxStorage: null,
      maxIntegrations: null,
      maxApiCalls: null,
      supportLevel: 'email'
    },
    advancedFeatures: {
      hasAnalytics: false,
      hasCustomBranding: false,
      hasApiAccess: false,
      hasSSO: false,
      hasWebhooks: false,
      hasAdvancedSecurity: false,
      hasDataExport: false,
      hasPrioritySupport: false
    },
    status: 'active',
    isPopular: false,
    isVisible: true
  }
}

const addFeature = () => {
  form.value.features.push({ name: '', limit: '' })
}

const removeFeature = (index) => {
  if (form.value.features.length > 1) {
    form.value.features.splice(index, 1)
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const planData = {
      ...form.value,
      id: isEditing.value ? props.plan.id : Date.now(),
      features: form.value.features.filter(f => f.name.trim() !== '')
    }
    
    emit('save', planData)
    closeModal()
  } catch (error) {
    console.error('Error saving plan:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Watchers
watch(
  () => props.plan,
  (newPlan) => {
    if (newPlan) {
      form.value = {
        name: newPlan.name || '',
        type: newPlan.type || '',
        price: newPlan.price || 0,
        billingCycle: newPlan.billingCycle || 'monthly',
        currency: newPlan.currency || 'USD',
        description: newPlan.description || '',
        features: newPlan.features?.length ? [...newPlan.features] : [{ name: '', limit: '' }],
        limits: {
          maxUsers: newPlan.limits?.maxUsers || null,
          maxConversations: newPlan.limits?.maxConversations || null,
          maxStorage: newPlan.limits?.maxStorage || null,
          maxIntegrations: newPlan.limits?.maxIntegrations || null,
          maxApiCalls: newPlan.limits?.maxApiCalls || null,
          supportLevel: newPlan.limits?.supportLevel || 'email'
        },
        advancedFeatures: {
          hasAnalytics: newPlan.advancedFeatures?.hasAnalytics || false,
          hasCustomBranding: newPlan.advancedFeatures?.hasCustomBranding || false,
          hasApiAccess: newPlan.advancedFeatures?.hasApiAccess || false,
          hasSSO: newPlan.advancedFeatures?.hasSSO || false,
          hasWebhooks: newPlan.advancedFeatures?.hasWebhooks || false,
          hasAdvancedSecurity: newPlan.advancedFeatures?.hasAdvancedSecurity || false,
          hasDataExport: newPlan.advancedFeatures?.hasDataExport || false,
          hasPrioritySupport: newPlan.advancedFeatures?.hasPrioritySupport || false
        },
        status: newPlan.status || 'active',
        isPopular: newPlan.isPopular || false,
        isVisible: newPlan.isVisible !== undefined ? newPlan.isVisible : true
      }
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

watch(
  () => props.isOpen,
  (isOpen) => {
    if (!isOpen) {
      resetForm()
    }
  }
)
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>