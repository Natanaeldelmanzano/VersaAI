<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Gestión de Equipos</h1>
            <p class="mt-1 text-sm text-gray-600">
              Administra miembros del equipo, roles y permisos
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="showInviteModal = true"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <UserPlusIcon class="h-5 w-5" />
              <span>Invitar Miembro</span>
            </button>
            <button
              @click="showRoleModal = true"
              class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2"
            >
              <ShieldCheckIcon class="h-5 w-5" />
              <span>Gestionar Roles</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 rounded-lg">
              <UsersIcon class="h-6 w-6 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Miembros</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalMembers }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-green-100 rounded-lg">
              <CheckCircleIcon class="h-6 w-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Miembros Activos</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.activeMembers }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <ClockIcon class="h-6 w-6 text-yellow-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Invitaciones Pendientes</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.pendingInvitations }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-2 bg-purple-100 rounded-lg">
              <ShieldCheckIcon class="h-6 w-6 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Roles Personalizados</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.customRoles }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div class="bg-white rounded-lg shadow mb-6">
        <div class="p-6">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div class="flex items-center space-x-4">
              <div class="relative">
                <MagnifyingGlassIcon class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar miembros..."
                  class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select
                v-model="filterRole"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los roles</option>
                <option v-for="role in roles" :key="role.id" :value="role.name">
                  {{ role.displayName }}
                </option>
              </select>
              
              <select
                v-model="filterStatus"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Todos los estados</option>
                <option value="active">Activo</option>
                <option value="inactive">Inactivo</option>
                <option value="pending">Pendiente</option>
              </select>
            </div>
            
            <div class="flex items-center space-x-2">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <Squares2X2Icon class="h-5 w-5" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'p-2 rounded-lg transition-colors',
                  viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <ListBulletIcon class="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Team Members -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">Miembros del Equipo</h2>
          
          <!-- Grid View -->
          <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="member in filteredMembers"
              :key="member.id"
              class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center space-x-4 mb-4">
                <div class="relative">
                  <img
                    :src="member.avatar || '/api/placeholder/40/40'"
                    :alt="member.name"
                    class="h-12 w-12 rounded-full object-cover"
                    @error="handleImageError"
                  />
                  <div :class="[
                    'absolute -bottom-1 -right-1 h-4 w-4 rounded-full border-2 border-white',
                    member.status === 'active' ? 'bg-green-400' :
                    member.status === 'inactive' ? 'bg-gray-400' :
                    'bg-yellow-400'
                  ]"></div>
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ member.name }}</h3>
                  <p class="text-sm text-gray-500">{{ member.email }}</p>
                </div>
              </div>
              
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Rol:</span>
                  <span :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    getRoleColor(member.role)
                  ]">
                    {{ getRoleDisplayName(member.role) }}
                  </span>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Último acceso:</span>
                  <span class="text-sm text-gray-900">{{ formatDate(member.lastLogin) }}</span>
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Unido:</span>
                  <span class="text-sm text-gray-900">{{ formatDate(member.joinedAt) }}</span>
                </div>
              </div>
              
              <div class="mt-4 flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <button
                    @click="editMember(member)"
                    class="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Editar
                  </button>
                  <button
                    v-if="member.status !== 'pending'"
                    @click="toggleMemberStatus(member)"
                    :class="[
                      'text-sm',
                      member.status === 'active' 
                        ? 'text-red-600 hover:text-red-800' 
                        : 'text-green-600 hover:text-green-800'
                    ]"
                  >
                    {{ member.status === 'active' ? 'Desactivar' : 'Activar' }}
                  </button>
                </div>
                
                <div class="relative" v-if="member.id !== currentUser.id">
                  <button
                    @click="toggleMemberMenu(member.id)"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <EllipsisVerticalIcon class="h-5 w-5" />
                  </button>
                  
                  <div
                    v-if="showMemberMenu === member.id"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
                  >
                    <div class="py-1">
                      <button
                        @click="resendInvitation(member)"
                        v-if="member.status === 'pending'"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Reenviar invitación
                      </button>
                      <button
                        @click="resetPassword(member)"
                        v-if="member.status === 'active'"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Restablecer contraseña
                      </button>
                      <button
                        @click="removeMember(member)"
                        class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                      >
                        Eliminar miembro
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- List View -->
          <div v-else class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Miembro
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rol
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Último acceso
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Unido
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Acciones</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="member in filteredMembers" :key="member.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="relative">
                        <img
                          :src="member.avatar || '/api/placeholder/40/40'"
                          :alt="member.name"
                          class="h-10 w-10 rounded-full object-cover"
                          @error="handleImageError"
                        />
                        <div :class="[
                          'absolute -bottom-1 -right-1 h-3 w-3 rounded-full border-2 border-white',
                          member.status === 'active' ? 'bg-green-400' :
                          member.status === 'inactive' ? 'bg-gray-400' :
                          'bg-yellow-400'
                        ]"></div>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">{{ member.name }}</div>
                        <div class="text-sm text-gray-500">{{ member.email }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      getRoleColor(member.role)
                    ]">
                      {{ getRoleDisplayName(member.role) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      member.status === 'active' ? 'bg-green-100 text-green-800' :
                      member.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                      'bg-yellow-100 text-yellow-800'
                    ]">
                      {{ getStatusLabel(member.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(member.lastLogin) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(member.joinedAt) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex items-center justify-end space-x-2">
                      <button
                        @click="editMember(member)"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        Editar
                      </button>
                      <div class="relative" v-if="member.id !== currentUser.id">
                        <button
                          @click="toggleMemberMenu(member.id)"
                          class="text-gray-400 hover:text-gray-600"
                        >
                          <EllipsisVerticalIcon class="h-5 w-5" />
                        </button>
                        
                        <div
                          v-if="showMemberMenu === member.id"
                          class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
                        >
                          <div class="py-1">
                            <button
                              @click="toggleMemberStatus(member)"
                              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                            >
                              {{ member.status === 'active' ? 'Desactivar' : 'Activar' }}
                            </button>
                            <button
                              @click="resendInvitation(member)"
                              v-if="member.status === 'pending'"
                              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                            >
                              Reenviar invitación
                            </button>
                            <button
                              @click="resetPassword(member)"
                              v-if="member.status === 'active'"
                              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                            >
                              Restablecer contraseña
                            </button>
                            <button
                              @click="removeMember(member)"
                              class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                            >
                              Eliminar miembro
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Invite Member Modal -->
    <InviteMemberModal
      v-if="showInviteModal"
      :roles="roles"
      @close="showInviteModal = false"
      @invite="handleInviteMember"
    />

    <!-- Role Management Modal -->
    <RoleManagementModal
      v-if="showRoleModal"
      :roles="roles"
      @close="showRoleModal = false"
      @save="handleSaveRole"
    />

    <!-- Edit Member Modal -->
    <EditMemberModal
      v-if="showEditModal"
      :member="editingMember"
      :roles="roles"
      @close="showEditModal = false"
      @save="handleSaveMember"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  UsersIcon,
  UserPlusIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
  ClockIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  EllipsisVerticalIcon
} from '@heroicons/vue/24/outline'
import InviteMemberModal from '@/components/dashboard/InviteMemberModal.vue'
import RoleManagementModal from '@/components/dashboard/RoleManagementModal.vue'
import EditMemberModal from '@/components/dashboard/EditMemberModal.vue'

// Reactive state
const searchQuery = ref('')
const filterRole = ref('')
const filterStatus = ref('')
const viewMode = ref('grid')
const showInviteModal = ref(false)
const showRoleModal = ref(false)
const showEditModal = ref(false)
const showMemberMenu = ref(null)
const editingMember = ref(null)

const currentUser = ref({
  id: 1,
  name: 'Usuario Actual',
  email: 'usuario@empresa.com'
})

const stats = ref({
  totalMembers: 12,
  activeMembers: 10,
  pendingInvitations: 2,
  customRoles: 3
})

const roles = ref([
  {
    id: 1,
    name: 'admin',
    displayName: 'Administrador',
    description: 'Acceso completo al sistema',
    permissions: ['all'],
    color: 'bg-red-100 text-red-800'
  },
  {
    id: 2,
    name: 'manager',
    displayName: 'Gerente',
    description: 'Gestión de equipos y proyectos',
    permissions: ['team.manage', 'projects.manage', 'analytics.read'],
    color: 'bg-blue-100 text-blue-800'
  },
  {
    id: 3,
    name: 'agent',
    displayName: 'Agente',
    description: 'Gestión de conversaciones',
    permissions: ['conversations.manage', 'chatbots.read'],
    color: 'bg-green-100 text-green-800'
  },
  {
    id: 4,
    name: 'viewer',
    displayName: 'Visualizador',
    description: 'Solo lectura',
    permissions: ['read'],
    color: 'bg-gray-100 text-gray-800'
  }
])

const members = ref([
  {
    id: 1,
    name: 'Ana García',
    email: 'ana.garcia@empresa.com',
    avatar: null,
    role: 'admin',
    status: 'active',
    lastLogin: new Date('2024-01-15T10:30:00'),
    joinedAt: new Date('2024-01-01T00:00:00')
  },
  {
    id: 2,
    name: 'Carlos Rodríguez',
    email: 'carlos.rodriguez@empresa.com',
    avatar: null,
    role: 'manager',
    status: 'active',
    lastLogin: new Date('2024-01-15T09:15:00'),
    joinedAt: new Date('2024-01-05T00:00:00')
  },
  {
    id: 3,
    name: 'María López',
    email: 'maria.lopez@empresa.com',
    avatar: null,
    role: 'agent',
    status: 'active',
    lastLogin: new Date('2024-01-14T16:45:00'),
    joinedAt: new Date('2024-01-10T00:00:00')
  },
  {
    id: 4,
    name: 'Juan Martínez',
    email: 'juan.martinez@empresa.com',
    avatar: null,
    role: 'agent',
    status: 'inactive',
    lastLogin: new Date('2024-01-10T14:20:00'),
    joinedAt: new Date('2024-01-08T00:00:00')
  },
  {
    id: 5,
    name: 'Laura Sánchez',
    email: 'laura.sanchez@empresa.com',
    avatar: null,
    role: 'viewer',
    status: 'pending',
    lastLogin: null,
    joinedAt: new Date('2024-01-14T00:00:00')
  }
])

// Computed properties
const filteredMembers = computed(() => {
  return members.value.filter(member => {
    const matchesSearch = member.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         member.email.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesRole = !filterRole.value || member.role === filterRole.value
    const matchesStatus = !filterStatus.value || member.status === filterStatus.value
    
    return matchesSearch && matchesRole && matchesStatus
  })
})

// Methods
const handleImageError = (event) => {
  event.target.src = '/api/placeholder/40/40'
}

const getRoleColor = (roleName) => {
  const role = roles.value.find(r => r.name === roleName)
  return role ? role.color : 'bg-gray-100 text-gray-800'
}

const getRoleDisplayName = (roleName) => {
  const role = roles.value.find(r => r.name === roleName)
  return role ? role.displayName : roleName
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    pending: 'Pendiente'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  if (!date) return 'Nunca'
  return new Intl.DateTimeFormat('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(date)
}

const toggleMemberMenu = (memberId) => {
  showMemberMenu.value = showMemberMenu.value === memberId ? null : memberId
}

const editMember = (member) => {
  editingMember.value = member
  showEditModal.value = true
  showMemberMenu.value = null
}

const toggleMemberStatus = (member) => {
  member.status = member.status === 'active' ? 'inactive' : 'active'
  showMemberMenu.value = null
}

const resendInvitation = (member) => {
  console.log('Reenviando invitación a:', member.email)
  showMemberMenu.value = null
}

const resetPassword = (member) => {
  if (confirm(`¿Enviar email de restablecimiento de contraseña a ${member.name}?`)) {
    console.log('Restableciendo contraseña para:', member.email)
  }
  showMemberMenu.value = null
}

const removeMember = (member) => {
  if (confirm(`¿Estás seguro de que quieres eliminar a ${member.name} del equipo?`)) {
    const index = members.value.findIndex(m => m.id === member.id)
    if (index > -1) {
      members.value.splice(index, 1)
      stats.value.totalMembers--
      if (member.status === 'active') {
        stats.value.activeMembers--
      } else if (member.status === 'pending') {
        stats.value.pendingInvitations--
      }
    }
  }
  showMemberMenu.value = null
}

const handleInviteMember = (inviteData) => {
  const newMember = {
    id: Date.now(),
    name: inviteData.name || inviteData.email.split('@')[0],
    email: inviteData.email,
    avatar: null,
    role: inviteData.role,
    status: 'pending',
    lastLogin: null,
    joinedAt: new Date()
  }
  
  members.value.push(newMember)
  stats.value.totalMembers++
  stats.value.pendingInvitations++
  
  console.log('Invitación enviada a:', inviteData.email)
}

const handleSaveRole = (roleData) => {
  if (roleData.id) {
    // Update existing role
    const index = roles.value.findIndex(r => r.id === roleData.id)
    if (index > -1) {
      roles.value[index] = roleData
    }
  } else {
    // Create new role
    const newRole = {
      ...roleData,
      id: Date.now(),
      color: 'bg-purple-100 text-purple-800'
    }
    roles.value.push(newRole)
    stats.value.customRoles++
  }
}

const handleSaveMember = (memberData) => {
  const index = members.value.findIndex(m => m.id === memberData.id)
  if (index > -1) {
    members.value[index] = { ...members.value[index], ...memberData }
  }
}

// Close menus when clicking outside
onMounted(() => {
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.relative')) {
      showMemberMenu.value = null
    }
  })
})
</script>