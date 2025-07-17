<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
        <p class="text-gray-600">Administra usuarios, roles y permisos del sistema</p>
      </div>
      <div class="flex space-x-3">
        <button
          @click="exportUsers"
          class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          Exportar
        </button>
        <button
          @click="showInviteModal = true"
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors duration-200"
        >
          Invitar Usuario
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <UsersIcon class="h-8 w-8 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Total Usuarios</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <CheckCircleIcon class="h-8 w-8 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Usuarios Activos</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.activeUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <ClockIcon class="h-8 w-8 text-yellow-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Pendientes</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingUsers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <ShieldCheckIcon class="h-8 w-8 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Administradores</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.adminUsers }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
          <input
            id="search-users"
            name="search-users"
            v-model="filters.search"
            type="text"
            placeholder="Buscar por nombre o email..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Rol</label>
          <select
            id="filter-role"
            name="filter-role"
            v-model="filters.role"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="manager">Manager</option>
            <option value="user">Usuario</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Estado</label>
          <select
            id="filter-status"
            name="filter-status"
            v-model="filters.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
            <option value="pending">Pendiente</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Ordenar por</label>
          <select
            id="sort-by"
            name="sort-by"
            v-model="filters.sortBy"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="name">Nombre</option>
            <option value="email">Email</option>
            <option value="role">Rol</option>
            <option value="createdAt">Fecha de registro</option>
            <option value="lastLogin">Último acceso</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Lista de Usuarios</h3>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        <p class="mt-2 text-gray-600">Cargando usuarios...</p>
      </div>
      
      <div v-else-if="filteredUsers.length === 0" class="p-8 text-center">
        <UsersIcon class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">No hay usuarios</h3>
        <p class="mt-1 text-sm text-gray-500">No se encontraron usuarios con los filtros aplicados.</p>
      </div>
      
      <div v-else class="overflow-x-auto">
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
                Registro
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img
                      v-if="user.avatar"
                      :src="user.avatar"
                      :alt="user.name"
                      class="h-10 w-10 rounded-full"
                    >
                    <div
                      v-else
                      class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center"
                    >
                      <span class="text-sm font-medium text-primary-600">
                        {{ user.name.charAt(0).toUpperCase() }}
                      </span>
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
                    user.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                    user.role === 'manager' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    user.status === 'active' ? 'bg-green-100 text-green-800' :
                    user.status === 'inactive' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  ]"
                >
                  {{ getStatusLabel(user.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.lastLogin ? formatDate(user.lastLogin) : 'Nunca' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.createdAt) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <button
                    @click="editUser(user)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="toggleUserStatus(user)"
                    :class="[
                      user.status === 'active' ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'
                    ]"
                  >
                    <component :is="user.status === 'active' ? XCircleIcon : CheckCircleIcon" class="h-4 w-4" />
                  </button>
                  <button
                    @click="deleteUser(user)"
                    class="text-red-600 hover:text-red-900"
                  >
                    <TrashIcon class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
            >
              Anterior
            </button>
            <button
              @click="currentPage++"
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
                <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                a
                <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, filteredUsers.length) }}</span>
                de
                <span class="font-medium">{{ filteredUsers.length }}</span>
                resultados
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="currentPage--"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Anterior
                </button>
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="currentPage = page"
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
                  @click="currentPage++"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                >
                  Siguiente
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Invite User Modal -->
    <div v-if="showInviteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Invitar Usuario</h3>
          <form @submit.prevent="inviteUser">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  id="invite-email"
                  name="invite-email"
                  v-model="inviteForm.email"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="usuario@ejemplo.com"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
                <select
                  id="invite-role"
                  name="invite-role"
                  v-model="inviteForm.role"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="user">Usuario</option>
                  <option value="manager">Manager</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Mensaje (opcional)</label>
                <textarea
                  id="invite-message"
                  name="invite-message"
                  v-model="inviteForm.message"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Mensaje personalizado para la invitación..."
                ></textarea>
              </div>
            </div>
            <div class="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                @click="showInviteModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="inviteLoading"
                class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {{ inviteLoading ? 'Enviando...' : 'Enviar Invitación' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Editar Usuario</h3>
          <form @submit.prevent="updateUser">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                <input
                  id="edit-name"
                  name="edit-name"
                  v-model="editForm.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  id="edit-email"
                  name="edit-email"
                  v-model="editForm.email"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
                <select
                  id="edit-role"
                  name="edit-role"
                  v-model="editForm.role"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="user">Usuario</option>
                  <option value="manager">Manager</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end space-x-3 mt-6">
              <button
                type="button"
                @click="showEditModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="editLoading"
                class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {{ editLoading ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  UsersIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  ShieldCheckIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/api'

const toast = useToast()

const loading = ref(false)
const inviteLoading = ref(false)
const editLoading = ref(false)
const showInviteModal = ref(false)
const showEditModal = ref(false)

const currentPage = ref(1)
const itemsPerPage = ref(10)

const users = ref([])
const stats = ref({
  totalUsers: 0,
  activeUsers: 0,
  pendingUsers: 0,
  adminUsers: 0
})

const filters = ref({
  search: '',
  role: '',
  status: '',
  sortBy: 'name'
})

const inviteForm = ref({
  email: '',
  role: 'user',
  message: ''
})

const editForm = ref({
  id: null,
  name: '',
  email: '',
  role: ''
})

const formatDate = (date) => {
  return format(new Date(date), 'dd MMM yyyy', { locale: es })
}

const getRoleLabel = (role) => {
  const labels = {
    admin: 'Administrador',
    manager: 'Manager',
    user: 'Usuario'
  }
  return labels[role] || role
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    pending: 'Pendiente'
  }
  return labels[status] || status
}

const filteredUsers = computed(() => {
  let filtered = [...users.value]
  
  // Search filter
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(user => 
      user.name.toLowerCase().includes(search) ||
      user.email.toLowerCase().includes(search)
    )
  }
  
  // Role filter
  if (filters.value.role) {
    filtered = filtered.filter(user => user.role === filters.value.role)
  }
  
  // Status filter
  if (filters.value.status) {
    filtered = filtered.filter(user => user.status === filters.value.status)
  }
  
  // Sort
  filtered.sort((a, b) => {
    const field = filters.value.sortBy
    if (field === 'name' || field === 'email') {
      return a[field].localeCompare(b[field])
    }
    if (field === 'createdAt' || field === 'lastLogin') {
      return new Date(b[field]) - new Date(a[field])
    }
    return a[field] > b[field] ? 1 : -1
  })
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredUsers.value.length / itemsPerPage.value)
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredUsers.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    } else if (current >= total - 3) {
      pages.push(1, '...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1, '...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    }
  }
  
  return pages.filter(page => page !== '...')
})

const fetchUsers = async () => {
  loading.value = true
  try {
    const [usersRes, statsRes] = await Promise.all([
      api.get('/users'),
      api.get('/users/stats')
    ])
    
    users.value = usersRes.data
    stats.value = statsRes.data
  } catch (error) {
    console.error('Error fetching users:', error)
    toast.error('Error al cargar los usuarios')
  } finally {
    loading.value = false
  }
}

const inviteUser = async () => {
  inviteLoading.value = true
  try {
    await api.post('/users/invite', inviteForm.value)
    toast.success('Invitación enviada correctamente')
    showInviteModal.value = false
    inviteForm.value = { email: '', role: 'user', message: '' }
    await fetchUsers()
  } catch (error) {
    console.error('Error inviting user:', error)
    toast.error('Error al enviar la invitación')
  } finally {
    inviteLoading.value = false
  }
}

const editUser = (user) => {
  editForm.value = {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role
  }
  showEditModal.value = true
}

const updateUser = async () => {
  editLoading.value = true
  try {
    await api.put(`/users/${editForm.value.id}`, {
      name: editForm.value.name,
      email: editForm.value.email,
      role: editForm.value.role
    })
    toast.success('Usuario actualizado correctamente')
    showEditModal.value = false
    await fetchUsers()
  } catch (error) {
    console.error('Error updating user:', error)
    toast.error('Error al actualizar el usuario')
  } finally {
    editLoading.value = false
  }
}

const toggleUserStatus = async (user) => {
  try {
    const newStatus = user.status === 'active' ? 'inactive' : 'active'
    await api.patch(`/users/${user.id}/status`, { status: newStatus })
    toast.success(`Usuario ${newStatus === 'active' ? 'activado' : 'desactivado'} correctamente`)
    await fetchUsers()
  } catch (error) {
    console.error('Error toggling user status:', error)
    toast.error('Error al cambiar el estado del usuario')
  }
}

const deleteUser = async (user) => {
  if (!confirm(`¿Estás seguro de que quieres eliminar al usuario ${user.name}?`)) {
    return
  }
  
  try {
    await api.delete(`/users/${user.id}`)
    toast.success('Usuario eliminado correctamente')
    await fetchUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    toast.error('Error al eliminar el usuario')
  }
}

const exportUsers = async () => {
  try {
    const response = await api.get('/users/export', {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `usuarios_${format(new Date(), 'yyyy-MM-dd')}.csv`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    toast.success('Lista de usuarios exportada correctamente')
  } catch (error) {
    console.error('Error exporting users:', error)
    toast.error('Error al exportar la lista de usuarios')
  }
}

// Reset pagination when filters change
watch([filters], () => {
  currentPage.value = 1
}, { deep: true })

onMounted(() => {
  fetchUsers()
})
</script>