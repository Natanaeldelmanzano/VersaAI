<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
        @click="closeModal"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-medium text-gray-900">
            {{ isEditing ? 'Editar Equipo' : 'Crear Nuevo Equipo' }}
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
                Nombre del Equipo *
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Ej: Equipo de Desarrollo"
              />
            </div>

            <div>
              <label for="department" class="block text-sm font-medium text-gray-700 mb-2">
                Departamento *
              </label>
              <select
                id="department"
                v-model="form.department"
                required
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
              placeholder="Describe el propósito y objetivos del equipo..."
            ></textarea>
          </div>

          <!-- Team Lead -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="teamLead" class="block text-sm font-medium text-gray-700 mb-2">
                Líder del Equipo
              </label>
              <select
                id="teamLead"
                v-model="form.teamLead"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Seleccionar líder</option>
                <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                  {{ user.name }} - {{ user.email }}
                </option>
              </select>
            </div>

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
                <option value="archived">Archivado</option>
              </select>
            </div>
          </div>

          <!-- Project Assignment -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Proyectos Asignados
            </label>
            <div class="space-y-2 max-h-32 overflow-y-auto border border-gray-200 rounded-md p-3">
              <div v-for="project in availableProjects" :key="project.id" class="flex items-center">
                <input
                  :id="`project-${project.id}`"
                  v-model="form.projects"
                  :value="project.id"
                  type="checkbox"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label :for="`project-${project.id}`" class="ml-2 text-sm text-gray-700">
                  {{ project.name }}
                </label>
              </div>
            </div>
          </div>

          <!-- Permissions -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Permisos del Equipo
            </label>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
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
                {{ isEditing ? 'Actualizar Equipo' : 'Crear Equipo' }}
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
import { XMarkIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  team: {
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
  department: '',
  description: '',
  teamLead: '',
  status: 'active',
  projects: [],
  permissions: []
})

// Mock data
const availableUsers = ref([
  { id: 1, name: 'Juan Pérez', email: 'juan@empresa.com' },
  { id: 2, name: 'María García', email: 'maria@empresa.com' },
  { id: 3, name: 'Carlos López', email: 'carlos@empresa.com' },
  { id: 4, name: 'Ana Martínez', email: 'ana@empresa.com' }
])

const availableProjects = ref([
  { id: 1, name: 'Proyecto Alpha' },
  { id: 2, name: 'Proyecto Beta' },
  { id: 3, name: 'Proyecto Gamma' },
  { id: 4, name: 'Proyecto Delta' }
])

const availablePermissions = ref([
  { id: 'read_analytics', name: 'Ver Analytics' },
  { id: 'manage_users', name: 'Gestionar Usuarios' },
  { id: 'export_data', name: 'Exportar Datos' },
  { id: 'manage_integrations', name: 'Gestionar Integraciones' },
  { id: 'view_reports', name: 'Ver Reportes' },
  { id: 'manage_settings', name: 'Gestionar Configuración' }
])

// Computed
const isEditing = computed(() => !!props.team)

// Methods
const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  form.value = {
    name: '',
    department: '',
    description: '',
    teamLead: '',
    status: 'active',
    projects: [],
    permissions: []
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const teamData = {
      ...form.value,
      id: isEditing.value ? props.team.id : Date.now()
    }
    
    emit('save', teamData)
    closeModal()
  } catch (error) {
    console.error('Error saving team:', error)
  } finally {
    isSubmitting.value = false
  }
}

// Watchers
watch(
  () => props.team,
  (newTeam) => {
    if (newTeam) {
      form.value = {
        name: newTeam.name || '',
        department: newTeam.department || '',
        description: newTeam.description || '',
        teamLead: newTeam.teamLead || '',
        status: newTeam.status || 'active',
        projects: newTeam.projects || [],
        permissions: newTeam.permissions || []
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
/* Custom scrollbar for project list */
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