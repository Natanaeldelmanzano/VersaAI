<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
        aria-hidden="true"
        @click="$emit('close')"
      ></div>
      
      <!-- Modal -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <!-- Header -->
        <div class="bg-white px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900" id="modal-title">
              {{ isEdit ? 'Editar Organización' : 'Nueva Organización' }}
            </h3>
            <button
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 focus:outline-none"
            >
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
        </div>
        
        <!-- Content -->
        <form @submit.prevent="handleSubmit" class="bg-white">
          <div class="px-6 py-6 space-y-6">
            <!-- Información Básica -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Nombre de la Organización -->
              <div class="md:col-span-2">
                <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre de la Organización *
                </label>
                <input
                  id="name"
                  v-model="form.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Ej: TechCorp Solutions"
                />
                <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
              </div>
              
              <!-- Industria -->
              <div>
                <label for="industry" class="block text-sm font-medium text-gray-700 mb-2">
                  Industria
                </label>
                <select
                  id="industry"
                  v-model="form.industry"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="">Seleccionar industria</option>
                  <option value="technology">Tecnología</option>
                  <option value="healthcare">Salud</option>
                  <option value="finance">Finanzas</option>
                  <option value="education">Educación</option>
                  <option value="retail">Retail</option>
                  <option value="manufacturing">Manufactura</option>
                  <option value="consulting">Consultoría</option>
                  <option value="media">Medios</option>
                  <option value="government">Gobierno</option>
                  <option value="nonprofit">Sin fines de lucro</option>
                  <option value="other">Otros</option>
                </select>
              </div>
              
              <!-- Estado -->
              <div>
                <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
                  Estado
                </label>
                <select
                  id="status"
                  v-model="form.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="active">Activo</option>
                  <option value="inactive">Inactivo</option>
                  <option value="pending">Pendiente</option>
                  <option value="suspended">Suspendido</option>
                </select>
              </div>
            </div>
            
            <!-- Información de Contacto -->
            <div class="border-t border-gray-200 pt-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Información de Contacto</h4>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Email de Contacto -->
                <div>
                  <label for="contactEmail" class="block text-sm font-medium text-gray-700 mb-2">
                    Email de Contacto
                  </label>
                  <input
                    id="contactEmail"
                    v-model="form.contactEmail"
                    type="email"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="contacto@empresa.com"
                  />
                </div>
                
                <!-- Teléfono -->
                <div>
                  <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                    Teléfono
                  </label>
                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                
                <!-- Sitio Web -->
                <div>
                  <label for="website" class="block text-sm font-medium text-gray-700 mb-2">
                    Sitio Web
                  </label>
                  <input
                    id="website"
                    v-model="form.website"
                    type="url"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="https://www.empresa.com"
                  />
                </div>
                
                <!-- País -->
                <div>
                  <label for="country" class="block text-sm font-medium text-gray-700 mb-2">
                    País
                  </label>
                  <select
                    id="country"
                    v-model="form.country"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Seleccionar país</option>
                    <option value="US">Estados Unidos</option>
                    <option value="CA">Canadá</option>
                    <option value="MX">México</option>
                    <option value="ES">España</option>
                    <option value="AR">Argentina</option>
                    <option value="CL">Chile</option>
                    <option value="CO">Colombia</option>
                    <option value="PE">Perú</option>
                    <option value="BR">Brasil</option>
                    <option value="UK">Reino Unido</option>
                    <option value="DE">Alemania</option>
                    <option value="FR">Francia</option>
                    <option value="IT">Italia</option>
                    <option value="OTHER">Otro</option>
                  </select>
                </div>
              </div>
              
              <!-- Dirección -->
              <div class="mt-6">
                <label for="address" class="block text-sm font-medium text-gray-700 mb-2">
                  Dirección
                </label>
                <textarea
                  id="address"
                  v-model="form.address"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Dirección completa de la organización"
                ></textarea>
              </div>
            </div>
            
            <!-- Plan y Configuración -->
            <div class="border-t border-gray-200 pt-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Plan y Configuración</h4>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Plan -->
                <div>
                  <label for="plan" class="block text-sm font-medium text-gray-700 mb-2">
                    Plan de Suscripción
                  </label>
                  <select
                    id="plan"
                    v-model="form.planId"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Seleccionar plan</option>
                    <option value="basic">Básico - $49/mes</option>
                    <option value="professional">Profesional - $149/mes</option>
                    <option value="premium">Premium - $249/mes</option>
                    <option value="enterprise">Enterprise - $499/mes</option>
                  </select>
                </div>
                
                <!-- Límite de Usuarios -->
                <div>
                  <label for="userLimit" class="block text-sm font-medium text-gray-700 mb-2">
                    Límite de Usuarios
                  </label>
                  <input
                    id="userLimit"
                    v-model.number="form.userLimit"
                    type="number"
                    min="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Ej: 100"
                  />
                </div>
                
                <!-- Límite de Chatbots -->
                <div>
                  <label for="chatbotLimit" class="block text-sm font-medium text-gray-700 mb-2">
                    Límite de Chatbots
                  </label>
                  <input
                    id="chatbotLimit"
                    v-model.number="form.chatbotLimit"
                    type="number"
                    min="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Ej: 10"
                  />
                </div>
                
                <!-- Límite de Conversaciones Mensuales -->
                <div>
                  <label for="conversationLimit" class="block text-sm font-medium text-gray-700 mb-2">
                    Límite de Conversaciones/Mes
                  </label>
                  <input
                    id="conversationLimit"
                    v-model.number="form.conversationLimit"
                    type="number"
                    min="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Ej: 10000"
                  />
                </div>
              </div>
            </div>
            
            <!-- Características y Permisos -->
            <div class="border-t border-gray-200 pt-6">
              <h4 class="text-lg font-medium text-gray-900 mb-4">Características y Permisos</h4>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- SSO -->
                <div class="flex items-center">
                  <input
                    id="sso"
                    v-model="form.features.sso"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="sso" class="ml-2 block text-sm text-gray-900">
                    Single Sign-On (SSO)
                  </label>
                </div>
                
                <!-- API Access -->
                <div class="flex items-center">
                  <input
                    id="api"
                    v-model="form.features.api"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="api" class="ml-2 block text-sm text-gray-900">
                    Acceso a API
                  </label>
                </div>
                
                <!-- Advanced Analytics -->
                <div class="flex items-center">
                  <input
                    id="analytics"
                    v-model="form.features.analytics"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="analytics" class="ml-2 block text-sm text-gray-900">
                    Analytics Avanzado
                  </label>
                </div>
                
                <!-- White Label -->
                <div class="flex items-center">
                  <input
                    id="whiteLabel"
                    v-model="form.features.whiteLabel"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="whiteLabel" class="ml-2 block text-sm text-gray-900">
                    White Label
                  </label>
                </div>
                
                <!-- Custom Integrations -->
                <div class="flex items-center">
                  <input
                    id="integrations"
                    v-model="form.features.integrations"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="integrations" class="ml-2 block text-sm text-gray-900">
                    Integraciones Personalizadas
                  </label>
                </div>
                
                <!-- Priority Support -->
                <div class="flex items-center">
                  <input
                    id="prioritySupport"
                    v-model="form.features.prioritySupport"
                    type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="prioritySupport" class="ml-2 block text-sm text-gray-900">
                    Soporte Prioritario
                  </label>
                </div>
              </div>
            </div>
            
            <!-- Notas Adicionales -->
            <div class="border-t border-gray-200 pt-6">
              <label for="notes" class="block text-sm font-medium text-gray-700 mb-2">
                Notas Adicionales
              </label>
              <textarea
                id="notes"
                v-model="form.notes"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Información adicional sobre la organización..."
              ></textarea>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="bg-gray-50 px-6 py-4 flex items-center justify-end space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isSubmitting" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Guardando...
              </span>
              <span v-else>
                {{ isEdit ? 'Actualizar' : 'Crear' }} Organización
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  organization: {
    type: Object,
    default: null
  },
  isEdit: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// State
const isSubmitting = ref(false)
const errors = ref({})

// Form data
const form = reactive({
  name: '',
  industry: '',
  status: 'active',
  contactEmail: '',
  phone: '',
  website: '',
  country: '',
  address: '',
  planId: '',
  userLimit: null,
  chatbotLimit: null,
  conversationLimit: null,
  features: {
    sso: false,
    api: false,
    analytics: false,
    whiteLabel: false,
    integrations: false,
    prioritySupport: false
  },
  notes: ''
})

// Methods
const validateForm = () => {
  errors.value = {}
  
  if (!form.name.trim()) {
    errors.value.name = 'El nombre de la organización es requerido'
  }
  
  if (form.contactEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.contactEmail)) {
    errors.value.contactEmail = 'El email no tiene un formato válido'
  }
  
  if (form.website && !/^https?:\/\/.+/.test(form.website)) {
    errors.value.website = 'El sitio web debe incluir http:// o https://'
  }
  
  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  try {
    isSubmitting.value = true
    
    // Preparar datos para enviar
    const organizationData = {
      ...form,
      plan: form.planId ? {
        id: form.planId,
        name: getPlanName(form.planId),
        price: getPlanPrice(form.planId),
        limits: {
          users: form.userLimit,
          chatbots: form.chatbotLimit,
          conversations: form.conversationLimit
        }
      } : null
    }
    
    // Simular delay de API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    emit('save', organizationData)
    
  } catch (error) {
    console.error('Error saving organization:', error)
  } finally {
    isSubmitting.value = false
  }
}

const getPlanName = (planId) => {
  const plans = {
    basic: 'Básico',
    professional: 'Profesional',
    premium: 'Premium',
    enterprise: 'Enterprise'
  }
  return plans[planId] || planId
}

const getPlanPrice = (planId) => {
  const prices = {
    basic: 49,
    professional: 149,
    premium: 249,
    enterprise: 499
  }
  return prices[planId] || 0
}

const loadFormData = () => {
  if (props.organization && props.isEdit) {
    // Cargar datos existentes
    Object.assign(form, {
      name: props.organization.name || '',
      industry: props.organization.industry || '',
      status: props.organization.status || 'active',
      contactEmail: props.organization.contactEmail || '',
      phone: props.organization.phone || '',
      website: props.organization.website || '',
      country: props.organization.country || '',
      address: props.organization.address || '',
      planId: props.organization.plan?.id || '',
      userLimit: props.organization.plan?.limits?.users || null,
      chatbotLimit: props.organization.plan?.limits?.chatbots || null,
      conversationLimit: props.organization.plan?.limits?.conversations || null,
      features: {
        sso: props.organization.features?.sso || false,
        api: props.organization.features?.api || false,
        analytics: props.organization.features?.analytics || false,
        whiteLabel: props.organization.features?.whiteLabel || false,
        integrations: props.organization.features?.integrations || false,
        prioritySupport: props.organization.features?.prioritySupport || false
      },
      notes: props.organization.notes || ''
    })
  }
}

// Watchers
watch(() => props.organization, loadFormData, { immediate: true })

// Lifecycle
onMounted(() => {
  loadFormData()
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>