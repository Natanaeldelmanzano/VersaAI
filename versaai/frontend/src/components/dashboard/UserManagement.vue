<template>
  <div class="user-management">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Gestión de Usuarios</h2>
        <p class="text-gray-600 mt-1">Administra usuarios, roles y permisos</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Search -->
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar usuarios..."
            class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
        
        <!-- Filter -->
        <select 
          v-model="selectedRole"
          class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        >
          <option value="">Todos los roles</option>
          <option value="admin">Administrador</option>
          <option value="manager">Manager</option>
          <option value="user">Usuario</option>
          <option value="viewer">Visualizador</option>
        </select>
        
        <!-- Add user button -->
        <button
          @click="openAddUserModal"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Agregar Usuario
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <UsersIcon class="w-5 h-5 text-blue-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Usuarios</p>
            <p class="text-2xl font-bold text-gray-900">{{ totalUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircleIcon class="w-5 h-5 text-green-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Usuarios Activos</p>
            <p class="text-2xl font-bold text-gray-900">{{ activeUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <CrownIcon class="w-5 h-5 text-purple-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Administradores</p>
            <p class="text-2xl font-bold text-gray-900">{{ adminUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
              <ClockIcon class="w-5 h-5 text-orange-600" />
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Nuevos (30d)</p>
            <p class="text-2xl font-bold text-gray-900">{{ newUsers }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Lista de Usuarios</h3>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usuario
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rol
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Último Acceso
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Organización
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="user in filteredUsers" 
              :key="user.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img 
                      v-if="user.avatar"
                      class="h-10 w-10 rounded-full" 
                      :src="user.avatar" 
                      :alt="user.name"
                    >
                    <div 
                      v-else
                      class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                    >
                      <UserIcon class="h-6 w-6 text-gray-600" />
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ user.name }}</div>
                    <div class="text-sm text-gray-500">{{ user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    getRoleColor(user.role)
                  ]"
                >
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    user.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ user.status === 'active' ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.last_login) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.organization || 'Sin organización' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button 
                    @click="editUser(user)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <PencilIcon class="w-4 h-4" />
                  </button>
                  <button 
                    @click="toggleUserStatus(user)"
                    :class="[
                      user.status === 'active' 
                        ? 'text-red-600 hover:text-red-900' 
                        : 'text-green-600 hover:text-green-900'
                    ]"
                  >
                    <component 
                      :is="user.status === 'active' ? XMarkIcon : CheckIcon"
                      class="w-4 h-4"
                    />
                  </button>
                  <button 
                    @click="deleteUser(user)"
                    class="text-red-600 hover:text-red-900"
                  >
                    <TrashIcon class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="previousPage"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Anterior
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Siguiente
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Mostrando
              <span class="font-medium">{{ startIndex }}</span>
              a
              <span class="font-medium">{{ endIndex }}</span>
              de
              <span class="font-medium">{{ totalUsers }}</span>
              resultados
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                <ChevronLeftIcon class="h-5 w-5" />
              </button>
              
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                  page === currentPage
                    ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                    : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                ]"
              >
                {{ page }}
              </button>
              
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                <ChevronRightIcon class="h-5 w-5" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit User Modal -->
    <div 
      v-if="showUserModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeUserModal"
    >
      <div 
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingUser ? 'Editar Usuario' : 'Agregar Usuario' }}
          </h3>
          
          <form @submit.prevent="saveUser" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nombre completo
              </label>
              <input
                v-model="userForm.name"
                type="text"
                required
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                v-model="userForm.email"
                type="email"
                required
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Rol
              </label>
              <select 
                v-model="userForm.role"
                required
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="user">Usuario</option>
                <option value="manager">Manager</option>
                <option value="admin">Administrador</option>
                <option value="viewer">Visualizador</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Organización
              </label>
              <input
                v-model="userForm.organization"
                type="text"
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            
            <div v-if="!editingUser">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Contraseña temporal
              </label>
              <input
                v-model="userForm.password"
                type="password"
                required
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            
            <div class="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                @click="closeUserModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700"
              >
                {{ editingUser ? 'Actualizar' : 'Crear' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  MagnifyingGlassIcon,
  PlusIcon,
  UsersIcon,
  CheckCircleIcon,
  ClockIcon,
  UserIcon,
  PencilIcon,
  XMarkIcon,
  CheckIcon,
  TrashIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'

// Custom crown icon component
const CrownIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
      <path d="M5 16L3 6l5.5 4L12 4l3.5 6L21 6l-2 10H5zm2.7-2h8.6l.9-4.4L14 12l-2-4-2 4-3.2-2.4L7.7 14z"/>
    </svg>
  `
}

// State
const searchQuery = ref('')
const selectedRole = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const showUserModal = ref(false)
const editingUser = ref(null)
const userForm = ref({
  name: '',
  email: '',
  role: 'user',
  organization: '',
  password: ''
})

// Mock data
const users = ref([
  {
    id: 1,
    name: 'Juan Pérez',
    email: 'juan@example.com',
    role: 'admin',
    status: 'active',
    last_login: '2024-01-15T10:30:00Z',
    organization: 'Acme Corp',
    avatar: null
  },
  {
    id: 2,
    name: 'María García',
    email: 'maria@example.com',
    role: 'manager',
    status: 'active',
    last_login: '2024-01-14T15:45:00Z',
    organization: 'TechStart Inc',
    avatar: null
  },
  {
    id: 3,
    name: 'Carlos López',
    email: 'carlos@example.com',
    role: 'user',
    status: 'active',
    last_login: '2024-01-13T09:15:00Z',
    organization: 'Global Solutions',
    avatar: null
  },
  {
    id: 4,
    name: 'Ana Martínez',
    email: 'ana@example.com',
    role: 'viewer',
    status: 'inactive',
    last_login: '2024-01-10T14:20:00Z',
    organization: 'Acme Corp',
    avatar: null
  },
  {
    id: 5,
    name: 'Luis Rodríguez',
    email: 'luis@example.com',
    role: 'user',
    status: 'active',
    last_login: '2024-01-15T11:00:00Z',
    organization: 'TechStart Inc',
    avatar: null
  }
])

// Computed
const filteredUsers = computed(() => {
  let filtered = users.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      user.organization?.toLowerCase().includes(query)
    )
  }
  
  if (selectedRole.value) {
    filtered = filtered.filter(user => user.role === selectedRole.value)
  }
  
  // Pagination
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filtered.slice(start, end)
})

const totalUsers = computed(() => users.value.length)
const activeUsers = computed(() => users.value.filter(u => u.status === 'active').length)
const adminUsers = computed(() => users.value.filter(u => u.role === 'admin').length)
const newUsers = computed(() => {
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
  return users.value.filter(u => new Date(u.last_login) > thirtyDaysAgo).length
})

const totalPages = computed(() => Math.ceil(totalUsers.value / itemsPerPage.value))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value + 1)
const endIndex = computed(() => Math.min(currentPage.value * itemsPerPage.value, totalUsers.value))

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const getRoleColor = (role) => {
  const colors = {
    admin: 'bg-red-100 text-red-800',
    manager: 'bg-blue-100 text-blue-800',
    user: 'bg-green-100 text-green-800',
    viewer: 'bg-gray-100 text-gray-800'
  }
  return colors[role] || colors.user
}

const getRoleLabel = (role) => {
  const labels = {
    admin: 'Administrador',
    manager: 'Manager',
    user: 'Usuario',
    viewer: 'Visualizador'
  }
  return labels[role] || role
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openAddUserModal = () => {
  editingUser.value = null
  userForm.value = {
    name: '',
    email: '',
    role: 'user',
    organization: '',
    password: ''
  }
  showUserModal.value = true
}

const editUser = (user) => {
  editingUser.value = user
  userForm.value = {
    name: user.name,
    email: user.email,
    role: user.role,
    organization: user.organization || '',
    password: ''
  }
  showUserModal.value = true
}

const closeUserModal = () => {
  showUserModal.value = false
  editingUser.value = null
}

const saveUser = () => {
  if (editingUser.value) {
    // Update existing user
    const index = users.value.findIndex(u => u.id === editingUser.value.id)
    if (index !== -1) {
      users.value[index] = {
        ...users.value[index],
        name: userForm.value.name,
        email: userForm.value.email,
        role: userForm.value.role,
        organization: userForm.value.organization
      }
    }
  } else {
    // Add new user
    const newUser = {
      id: Math.max(...users.value.map(u => u.id)) + 1,
      name: userForm.value.name,
      email: userForm.value.email,
      role: userForm.value.role,
      status: 'active',
      last_login: new Date().toISOString(),
      organization: userForm.value.organization,
      avatar: null
    }
    users.value.push(newUser)
  }
  
  closeUserModal()
}

const toggleUserStatus = (user) => {
  const index = users.value.findIndex(u => u.id === user.id)
  if (index !== -1) {
    users.value[index].status = user.status === 'active' ? 'inactive' : 'active'
  }
}

const deleteUser = (user) => {
  if (confirm(`¿Estás seguro de que quieres eliminar a ${user.name}?`)) {
    const index = users.value.findIndex(u => u.id === user.id)
    if (index !== -1) {
      users.value.splice(index, 1)
    }
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const goToPage = (page) => {
  currentPage.value = page
}

// Lifecycle
onMounted(() => {
  // Load users data
})
</script>

<style scoped>
.user-management {
  @apply p-6;
}
</style>