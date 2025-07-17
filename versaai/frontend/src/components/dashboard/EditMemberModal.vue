<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-lg shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Editar Miembro</h3>
          <p class="text-sm text-gray-600 mt-1">Modifica la información del miembro del equipo</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="saveMember" class="mt-6 space-y-6">
        <!-- Avatar -->
        <div class="flex items-center space-x-6">
          <div class="relative">
            <img
              :src="form.avatar || '/api/placeholder/80/80'"
              :alt="form.name"
              class="h-20 w-20 rounded-full object-cover border-4 border-gray-200"
              @error="handleImageError"
            />
            <div :class="[
              'absolute -bottom-1 -right-1 h-6 w-6 rounded-full border-2 border-white',
              form.status === 'active' ? 'bg-green-400' :
              form.status === 'inactive' ? 'bg-gray-400' :
              'bg-yellow-400'
            ]"></div>
          </div>
          <div class="flex-1">
            <button
              type="button"
              @click="triggerFileUpload"
              class="bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cambiar foto
            </button>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileUpload"
              class="hidden"
            />
            <p class="mt-2 text-xs text-gray-500">
              JPG, GIF o PNG. Máximo 1MB.
            </p>
          </div>
        </div>

        <!-- Basic Information -->
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Nombre Completo *
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Nombre completo"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico *
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              :disabled="member.status === 'active'"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              placeholder="usuario@empresa.com"
            />
            <p v-if="member.status === 'active'" class="mt-1 text-xs text-gray-500">
              No se puede cambiar el email de usuarios activos
            </p>
          </div>
        </div>

        <!-- Role and Status -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
              Rol *
            </label>
            <select
              id="role"
              v-model="form.role"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option v-for="role in availableRoles" :key="role.id" :value="role.name">
                {{ role.displayName }}
              </option>
            </select>
            <p v-if="selectedRoleDescription" class="mt-1 text-xs text-gray-500">
              {{ selectedRoleDescription }}
            </p>
          </div>

          <div>
            <label for="status" class="block text-sm font-medium text-gray-700 mb-2">
              Estado
            </label>
            <select
              id="status"
              v-model="form.status"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="active">Activo</option>
              <option value="inactive">Inactivo</option>
              <option value="pending" v-if="member.status === 'pending'">Pendiente</option>
            </select>
          </div>
        </div>

        <!-- Additional Information -->
        <div class="space-y-4">
          <div>
            <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
              Departamento
            </label>
            <input
              id="department"
              v-model="form.department"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Departamento o área"
            />
          </div>

          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
              Teléfono
            </label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="+1 (555) 123-4567"
            />
          </div>

          <div>
            <label for="notes" class="block text-sm font-medium text-gray-700 mb-2">
              Notas Internas
            </label>
            <textarea
              id="notes"
              v-model="form.notes"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Notas adicionales sobre el miembro..."
            ></textarea>
          </div>
        </div>

        <!-- Permissions Override -->
        <div v-if="form.role !== 'admin'" class="space-y-4">
          <div class="flex items-center justify-between">
            <label class="block text-sm font-medium text-gray-700">
              Permisos Especiales
            </label>
            <button
              type="button"
              @click="showPermissions = !showPermissions"
              class="text-sm text-blue-600 hover:text-blue-800"
            >
              {{ showPermissions ? 'Ocultar' : 'Mostrar' }} permisos
            </button>
          </div>
          
          <div v-if="showPermissions" class="border border-gray-200 rounded-lg p-4 space-y-3">
            <p class="text-sm text-gray-600">
              Otorga permisos adicionales específicos para este usuario
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <label
                v-for="permission in specialPermissions"
                :key="permission.value"
                class="flex items-start space-x-3 p-2 rounded hover:bg-gray-50 cursor-pointer"
              >
                <input
                  v-model="form.specialPermissions"
                  :value="permission.value"
                  type="checkbox"
                  class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900">{{ permission.label }}</div>
                  <div class="text-xs text-gray-500">{{ permission.description }}</div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Member Statistics -->
        <div class="bg-gray-50 rounded-lg p-4 space-y-3">
          <h4 class="text-sm font-medium text-gray-900">Información del Miembro</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-600">Miembro desde:</span>
              <div class="font-medium">{{ formatDate(member.joinedAt) }}</div>
            </div>
            <div>
              <span class="text-gray-600">Último acceso:</span>
              <div class="font-medium">{{ formatDate(member.lastLogin) }}</div>
            </div>
            <div v-if="member.conversationsHandled">
              <span class="text-gray-600">Conversaciones:</span>
              <div class="font-medium">{{ member.conversationsHandled }}</div>
            </div>
            <div v-if="member.avgResponseTime">
              <span class="text-gray-600">Tiempo respuesta:</span>
              <div class="font-medium">{{ member.avgResponseTime }}</div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="isLoading">Guardando...</span>
            <span v-else>Guardar Cambios</span>
            <CheckIcon v-if="!isLoading" class="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { XMarkIcon, CheckIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  member: {
    type: Object,
    required: true
  },
  roles: {
    type: Array,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const isLoading = ref(false)
const showPermissions = ref(false)
const fileInput = ref(null)

const form = ref({
  name: '',
  email: '',
  role: '',
  status: '',
  avatar: '',
  department: '',
  phone: '',
  notes: '',
  specialPermissions: []
})

const specialPermissions = ref([
  {
    value: 'analytics.advanced',
    label: 'Analytics Avanzado',
    description: 'Acceso a métricas detalladas'
  },
  {
    value: 'conversations.export',
    label: 'Exportar Conversaciones',
    description: 'Descargar datos de conversaciones'
  },
  {
    value: 'chatbots.deploy',
    label: 'Desplegar Chatbots',
    description: 'Publicar chatbots en producción'
  },
  {
    value: 'team.invite',
    label: 'Invitar Miembros',
    description: 'Enviar invitaciones al equipo'
  },
  {
    value: 'settings.integrations',
    label: 'Gestionar Integraciones',
    description: 'Configurar integraciones externas'
  },
  {
    value: 'billing.view',
    label: 'Ver Facturación',
    description: 'Acceso a información de facturación'
  }
])

// Computed properties
const availableRoles = computed(() => {
  // Filter roles based on current user permissions
  return props.roles.filter(role => {
    // Don't allow assigning admin role unless current user is admin
    return role.name !== 'admin' || true // TODO: Check current user permissions
  })
})

const selectedRoleDescription = computed(() => {
  if (!form.value.role) return ''
  const role = props.roles.find(r => r.name === form.value.role)
  return role ? role.description : ''
})

const isFormValid = computed(() => {
  return form.value.name && form.value.email && form.value.role
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const handleImageError = (event) => {
  event.target.src = '/api/placeholder/80/80'
}

const formatDate = (date) => {
  if (!date) return 'Nunca'
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file size (1MB max)
  if (file.size > 1024 * 1024) {
    alert('El archivo debe ser menor a 1MB')
    return
  }
  
  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('Solo se permiten archivos de imagen')
    return
  }
  
  // Create preview URL
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.avatar = e.target.result
  }
  reader.readAsDataURL(file)
}

const saveMember = async () => {
  if (!isFormValid.value) return
  
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const memberData = {
      id: props.member.id,
      ...form.value
    }
    
    emit('save', memberData)
    emit('close')
  } catch (error) {
    console.error('Error saving member:', error)
  } finally {
    isLoading.value = false
  }
}

// Initialize form with member data
onMounted(() => {
  form.value = {
    name: props.member.name || '',
    email: props.member.email || '',
    role: props.member.role || '',
    status: props.member.status || 'active',
    avatar: props.member.avatar || '',
    department: props.member.department || '',
    phone: props.member.phone || '',
    notes: props.member.notes || '',
    specialPermissions: props.member.specialPermissions || []
  }
})
</script>