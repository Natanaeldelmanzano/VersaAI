<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
        @click="closeModal"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-4xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-lg">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-lg font-medium text-gray-900">
              Gestionar Miembros - {{ team?.name }}
            </h3>
            <p class="text-sm text-gray-500 mt-1">
              {{ team?.department }} • {{ members.length }} miembros
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="showAddMember = true"
              class="px-3 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon class="w-4 h-4 mr-1" />
              Agregar Miembro
            </button>
            <button
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>
        </div>

        <!-- Search and Filters -->
        <div class="flex flex-col sm:flex-row gap-4 mb-6">
          <div class="flex-1">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar miembros..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
          <div class="flex gap-2">
            <select
              v-model="roleFilter"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Todos los roles</option>
              <option value="admin">Administrador</option>
              <option value="manager">Gerente</option>
              <option value="developer">Desarrollador</option>
              <option value="analyst">Analista</option>
            </select>
            <select
              v-model="statusFilter"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Todos los estados</option>
              <option value="active">Activo</option>
              <option value="inactive">Inactivo</option>
              <option value="pending">Pendiente</option>
            </select>
          </div>
        </div>

        <!-- Members List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            <li v-for="member in filteredMembers" :key="member.id" class="px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <img 
                      :src="member.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(member.name)}&background=3B82F6&color=fff`" 
                      :alt="member.name"
                      class="h-10 w-10 rounded-full"
                    />
                  </div>
                  <div class="ml-4">
                    <div class="flex items-center">
                      <p class="text-sm font-medium text-gray-900">{{ member.name }}</p>
                      <span v-if="member.isLead" class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        <StarIcon class="w-3 h-3 mr-1" />
                        Líder
                      </span>
                    </div>
                    <p class="text-sm text-gray-500">{{ member.email }}</p>
                    <div class="flex items-center mt-1">
                      <span class="text-xs text-gray-500">{{ member.role }}</span>
                      <span class="mx-2 text-gray-300">•</span>
                      <span :class="getStatusClass(member.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
                        {{ getStatusText(member.status) }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2">
                  <!-- Role Change -->
                  <select
                    :value="member.role"
                    @change="updateMemberRole(member.id, $event.target.value)"
                    class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  >
                    <option value="admin">Administrador</option>
                    <option value="manager">Gerente</option>
                    <option value="developer">Desarrollador</option>
                    <option value="analyst">Analista</option>
                    <option value="viewer">Visualizador</option>
                  </select>
                  
                  <!-- Actions -->
                  <div class="flex items-center space-x-1">
                    <button
                      @click="toggleMemberStatus(member.id)"
                      :class="member.status === 'active' ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'"
                      class="p-1 rounded hover:bg-gray-100"
                      :title="member.status === 'active' ? 'Desactivar' : 'Activar'"
                    >
                      <component :is="member.status === 'active' ? PauseIcon : PlayIcon" class="w-4 h-4" />
                    </button>
                    
                    <button
                      @click="editMemberPermissions(member)"
                      class="p-1 rounded text-blue-600 hover:text-blue-800 hover:bg-gray-100"
                      title="Editar permisos"
                    >
                      <KeyIcon class="w-4 h-4" />
                    </button>
                    
                    <button
                      @click="removeMember(member.id)"
                      class="p-1 rounded text-red-600 hover:text-red-800 hover:bg-gray-100"
                      title="Remover del equipo"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Member Details -->
              <div v-if="member.showDetails" class="mt-4 pl-14">
                <div class="bg-gray-50 rounded-lg p-4">
                  <h4 class="text-sm font-medium text-gray-900 mb-2">Información Adicional</h4>
                  <div class="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span class="text-gray-500">Fecha de ingreso:</span>
                      <span class="ml-2 text-gray-900">{{ formatDate(member.joinedAt) }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">Último acceso:</span>
                      <span class="ml-2 text-gray-900">{{ formatDate(member.lastAccess) }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">Proyectos asignados:</span>
                      <span class="ml-2 text-gray-900">{{ member.projects?.length || 0 }}</span>
                    </div>
                    <div>
                      <span class="text-gray-500">Permisos especiales:</span>
                      <span class="ml-2 text-gray-900">{{ member.permissions?.length || 0 }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Add Member Form -->
        <div v-if="showAddMember" class="mt-6 border-t pt-6">
          <h4 class="text-md font-medium text-gray-900 mb-4">Agregar Nuevo Miembro</h4>
          <form @submit.prevent="addMember" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Usuario</label>
              <select
                v-model="newMember.userId"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Seleccionar usuario</option>
                <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                  {{ user.name }} - {{ user.email }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
              <select
                v-model="newMember.role"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="">Seleccionar rol</option>
                <option value="admin">Administrador</option>
                <option value="manager">Gerente</option>
                <option value="developer">Desarrollador</option>
                <option value="analyst">Analista</option>
                <option value="viewer">Visualizador</option>
              </select>
            </div>
            <div class="flex items-end">
              <button
                type="submit"
                class="w-full px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Agregar
              </button>
            </div>
          </form>
          <div class="flex justify-end mt-4">
            <button
              @click="showAddMember = false"
              class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancelar
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200 mt-6">
          <button
            @click="exportMembers"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <DocumentArrowDownIcon class="w-4 h-4 mr-2" />
            Exportar
          </button>
          <button
            @click="closeModal"
            class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {
  XMarkIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  StarIcon,
  PauseIcon,
  PlayIcon,
  KeyIcon,
  TrashIcon,
  DocumentArrowDownIcon
} from '@heroicons/vue/24/outline'

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
const emit = defineEmits(['close', 'update'])

// State
const searchQuery = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const showAddMember = ref(false)

// Form for new member
const newMember = ref({
  userId: '',
  role: ''
})

// Mock data
const members = ref([
  {
    id: 1,
    name: 'Juan Pérez',
    email: 'juan@empresa.com',
    role: 'manager',
    status: 'active',
    isLead: true,
    avatar: null,
    joinedAt: '2024-01-15',
    lastAccess: '2024-01-20',
    projects: [1, 2],
    permissions: ['read_analytics', 'manage_users']
  },
  {
    id: 2,
    name: 'María García',
    email: 'maria@empresa.com',
    role: 'developer',
    status: 'active',
    isLead: false,
    avatar: null,
    joinedAt: '2024-01-10',
    lastAccess: '2024-01-19',
    projects: [1],
    permissions: ['read_analytics']
  },
  {
    id: 3,
    name: 'Carlos López',
    email: 'carlos@empresa.com',
    role: 'developer',
    status: 'inactive',
    isLead: false,
    avatar: null,
    joinedAt: '2024-01-05',
    lastAccess: '2024-01-18',
    projects: [2],
    permissions: []
  },
  {
    id: 4,
    name: 'Ana Martínez',
    email: 'ana@empresa.com',
    role: 'analyst',
    status: 'pending',
    isLead: false,
    avatar: null,
    joinedAt: '2024-01-20',
    lastAccess: null,
    projects: [],
    permissions: ['read_analytics']
  }
])

const availableUsers = ref([
  { id: 5, name: 'Pedro Rodríguez', email: 'pedro@empresa.com' },
  { id: 6, name: 'Laura Sánchez', email: 'laura@empresa.com' },
  { id: 7, name: 'Miguel Torres', email: 'miguel@empresa.com' }
])

// Computed
const filteredMembers = computed(() => {
  let filtered = members.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(member => 
      member.name.toLowerCase().includes(query) ||
      member.email.toLowerCase().includes(query)
    )
  }
  
  if (roleFilter.value) {
    filtered = filtered.filter(member => member.role === roleFilter.value)
  }
  
  if (statusFilter.value) {
    filtered = filtered.filter(member => member.status === statusFilter.value)
  }
  
  return filtered
})

// Methods
const closeModal = () => {
  emit('close')
  resetForm()
}

const resetForm = () => {
  searchQuery.value = ''
  roleFilter.value = ''
  statusFilter.value = ''
  showAddMember.value = false
  newMember.value = {
    userId: '',
    role: ''
  }
}

const getStatusClass = (status) => {
  const classes = {
    active: 'bg-green-100 text-green-800',
    inactive: 'bg-red-100 text-red-800',
    pending: 'bg-yellow-100 text-yellow-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    active: 'Activo',
    inactive: 'Inactivo',
    pending: 'Pendiente'
  }
  return texts[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return 'Nunca'
  return new Date(dateString).toLocaleDateString('es-ES')
}

const updateMemberRole = (memberId, newRole) => {
  const member = members.value.find(m => m.id === memberId)
  if (member) {
    member.role = newRole
    emit('update', { type: 'role_change', memberId, newRole })
  }
}

const toggleMemberStatus = (memberId) => {
  const member = members.value.find(m => m.id === memberId)
  if (member) {
    member.status = member.status === 'active' ? 'inactive' : 'active'
    emit('update', { type: 'status_change', memberId, newStatus: member.status })
  }
}

const editMemberPermissions = (member) => {
  // This would open a permissions modal
  console.log('Edit permissions for:', member.name)
}

const removeMember = (memberId) => {
  if (confirm('¿Estás seguro de que quieres remover este miembro del equipo?')) {
    const index = members.value.findIndex(m => m.id === memberId)
    if (index > -1) {
      members.value.splice(index, 1)
      emit('update', { type: 'member_removed', memberId })
    }
  }
}

const addMember = () => {
  const user = availableUsers.value.find(u => u.id === parseInt(newMember.value.userId))
  if (user) {
    const newMemberData = {
      id: Date.now(),
      name: user.name,
      email: user.email,
      role: newMember.value.role,
      status: 'active',
      isLead: false,
      avatar: null,
      joinedAt: new Date().toISOString().split('T')[0],
      lastAccess: null,
      projects: [],
      permissions: []
    }
    
    members.value.push(newMemberData)
    emit('update', { type: 'member_added', member: newMemberData })
    
    // Reset form
    newMember.value = { userId: '', role: '' }
    showAddMember.value = false
  }
}

const exportMembers = () => {
  // This would export the members list
  console.log('Exporting members...')
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
/* Custom styles for better UX */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>