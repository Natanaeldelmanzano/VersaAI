<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
        @click="closeModal"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-lg p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900">
            Invitar Usuario
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
          <!-- Email Input -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico *
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="usuario@empresa.com"
            />
          </div>

          <!-- Name Input -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
              Nombre Completo *
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="Nombre del usuario"
            />
          </div>

          <!-- Role Selection -->
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
              Rol *
            </label>
            <select
              id="role"
              v-model="form.role"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Seleccionar rol</option>
              <option v-for="role in availableRoles" :key="role.id" :value="role.id">
                {{ role.name }} - {{ role.description }}
              </option>
            </select>
          </div>

          <!-- Team Selection -->
          <div>
            <label for="team" class="block text-sm font-medium text-gray-700 mb-2">
              Equipo
            </label>
            <select
              id="team"
              v-model="form.team"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Sin equipo asignado</option>
              <option v-for="team in availableTeams" :key="team.id" :value="team.id">
                {{ team.name }} - {{ team.department }}
              </option>
            </select>
          </div>

          <!-- Department Selection -->
          <div>
            <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
              Departamento
            </label>
            <select
              id="department"
              v-model="form.department"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Seleccionar departamento</option>
              <option value="Desarrollo">Desarrollo</option>
              <option value="Marketing">Marketing</option>
              <option value="Ventas">Ventas</option>
              <option value="Soporte">Soporte</option>
              <option value="Recursos Humanos">Recursos Humanos</option>
              <option value="Finanzas">Finanzas</option>
              <option value="Operaciones">Operaciones</option>
            </select>
          </div>

          <!-- Permissions -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Permisos Adicionales
            </label>
            <div class="space-y-2 max-h-32 overflow-y-auto border border-gray-200 rounded-md p-3">
              <div v-for="permission in availablePermissions" :key="permission.id" class="flex items-center">
                <input
                  :id="`permission-${permission.id}`"
                  v-model="form.permissions"
                  :value="permission.id"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label :for="`permission-${permission.id}`" class="ml-2 text-sm text-gray-700">
                  {{ permission.name }}
                </label>
              </div>
            </div>
          </div>

          <!-- Welcome Message -->
          <div>
            <label for="message" class="block text-sm font-medium text-gray-700 mb-2">
              Mensaje de Bienvenida (Opcional)
            </label>
            <textarea
              id="message"
              v-model="form.message"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              placeholder="Mensaje personalizado para el nuevo usuario..."
            ></textarea>
          </div>

          <!-- Send Options -->
          <div class="space-y-3">
            <div class="flex items-center">
              <input
                id="sendEmail"
                v-model="form.sendEmail"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="sendEmail" class="ml-2 text-sm text-gray-700">
                Enviar invitación por correo electrónico
              </label>
            </div>
            
            <div class="flex items-center">
              <input
                id="requirePasswordChange"
                v-model="form.requirePasswordChange"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label for="requirePasswordChange" class="ml-2 text-sm text-gray-700">
                Requerir cambio de contraseña en el primer acceso
              </label>
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
                Enviando invitación...
              </span>
              <span v-else>
                Enviar Invitación
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['close', 'invite'])

// State
const isSubmitting = ref(false)

// Form data
const form = ref({
  email: '',
  name: '',
  role: '',
  team: '',
  department: '',
  permissions: [],
  message: '',
  sendEmail: true,
  requirePasswordChange: true
})

// Mock data
const availableRoles = ref([
  { id: 'admin', name: 'Administrador', description: 'Acceso completo al sistema' },
  { id: 'manager', name: 'Gerente', description: 'Gestión de equipos y proyectos' },
  { id: 'developer', name: 'Desarrollador', description: 'Acceso a herramientas de desarrollo' },
  { id: 'analyst', name: 'Analista', description: 'Acceso a analytics y reportes' },
  { id: 'support', name: 'Soporte', description: 'Gestión de tickets y usuarios' },
  { id: 'viewer', name: 'Visualizador', description: 'Solo lectura' }
])

const availableTeams = ref([
  { id: 1, name: 'Equipo Frontend', department: 'Desarrollo' },
  { id: 2, name: 'Equipo Backend', department: 'Desarrollo' },
  { id: 3, name: 'Equipo Marketing', department: 'Marketing' },
  { id: 4, name: 'Equipo Ventas', department: 'Ventas' },
  { id: 5, name: 'Equipo Soporte', department: 'Soporte' }
])

const availablePermissions = ref([
  { id: 'read_analytics', name: 'Ver Analytics' },
  { id: 'export_data', name: 'Exportar Datos' },
  { id: 'manage_integrations', name: 'Gestionar Integraciones' },
  { id: 'view_reports', name: 'Ver Reportes' },
  { id: 'manage_billing', name: 'Gestionar Facturación' },
  { id: 'system_settings', name: 'Configuración del Sistema' }
])

// Methods
const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  form.value = {
    email: '',
    name: '',
    role: '',
    team: '',
    department: '',
    permissions: [],
    message: '',
    sendEmail: true,
    requirePasswordChange: true
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const invitationData = {
      ...form.value,
      id: Date.now(),
      invitedAt: new Date().toISOString(),
      status: 'pending'
    }
    
    emit('invite', invitationData)
    closeModal()
  } catch (error) {
    console.error('Error sending invitation:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Watchers
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
/* Custom scrollbar for permissions list */
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