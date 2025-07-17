<template>
  <div class="users-page">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Usuarios</h1>
            <p class="text-gray-600 mt-1">Gestiona usuarios y permisos del sistema</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="showInviteModal = true"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Invitar Usuario
            </button>
            <button
              @click="refreshUsers"
              :disabled="isLoading"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Actualizar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-blue-100">Total Usuarios</p>
                <p class="text-2xl font-bold">{{ stats.totalUsers }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-green-100">Activos</p>
                <p class="text-2xl font-bold">{{ stats.activeUsers }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-yellow-100">Pendientes</p>
                <p class="text-2xl font-bold">{{ stats.pendingUsers }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-4 text-white">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.25-4.5a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 5.25v13.5A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V5.25a2.25 2.25 0 00-2.25-2.25H16.5m-3-3h3v3" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-purple-100">Administradores</p>
                <p class="text-2xl font-bold">{{ stats.adminUsers }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Buscar usuarios..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @input="debouncedSearch"
            >
          </div>

          <!-- Role Filter -->
          <select
            v-model="filters.role"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="editor">Editor</option>
            <option value="viewer">Visualizador</option>
          </select>

          <!-- Status Filter -->
          <select
            v-model="filters.status"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos los estados</option>
            <option value="active">Activo</option>
            <option value="pending">Pendiente</option>
            <option value="inactive">Inactivo</option>
          </select>

          <!-- Sort -->
          <select
            v-model="filters.sort"
            @change="applyFilters"
            class="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="name_asc">Nombre A-Z</option>
            <option value="name_desc">Nombre Z-A</option>
            <option value="created_at_desc">Más recientes</option>
            <option value="created_at_asc">Más antiguos</option>
            <option value="last_login_desc">Último acceso</option>
          </select>
        </div>

        <!-- Clear Filters -->
        <div class="mt-4 flex items-center justify-between">
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            Limpiar filtros
          </button>
          <div class="text-sm text-gray-500">
            {{ filteredUsers.length }} usuarios encontrados
          </div>
        </div>
      </div>
    </div>

    <!-- Users Table -->
    <div class="flex-1 overflow-y-auto bg-white">
      <div v-if="isLoading" class="p-6">
        <div class="animate-pulse space-y-4">
          <div v-for="i in 5" :key="i" class="flex items-center space-x-4">
            <div class="rounded-full bg-gray-200 h-10 w-10"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-200 rounded w-1/4"></div>
              <div class="h-3 bg-gray-200 rounded w-1/6"></div>
            </div>
            <div class="h-4 bg-gray-200 rounded w-20"></div>
            <div class="h-4 bg-gray-200 rounded w-16"></div>
          </div>
        </div>
      </div>

      <div v-else-if="filteredUsers.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No hay usuarios</h3>
        <p class="mt-1 text-sm text-gray-500">Comienza invitando a tu primer usuario.</p>
        <div class="mt-6">
          <button
            @click="showInviteModal = true"
            class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Invitar Usuario
          </button>
        </div>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Usuario
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rol
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Estado
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Último acceso
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fecha de registro
              </th>
              <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Acciones</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                      <span class="text-sm font-medium text-gray-700">{{ getUserInitials(user.name) }}</span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ user.name }}</div>
                    <div class="text-sm text-gray-500">{{ user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getRoleBadgeClass(user.role)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
                  {{ getRoleText(user.role) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusBadgeClass(user.status)" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
                  {{ getStatusText(user.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.last_login ? formatDate(user.last_login) : 'Nunca' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="relative">
                  <button
                    @click="toggleUserMenu(user.id)"
                    class="text-gray-400 hover:text-gray-600 p-1 rounded"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                    </svg>
                  </button>
                  <div
                    v-if="activeUserMenu === user.id"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
                  >
                    <div class="py-1">
                      <button
                        @click="editUser(user)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Editar usuario
                      </button>
                      <button
                        @click="changeUserRole(user)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Cambiar rol
                      </button>
                      <button
                        v-if="user.status === 'active'"
                        @click="deactivateUser(user.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Desactivar
                      </button>
                      <button
                        v-else
                        @click="activateUser(user.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Activar
                      </button>
                      <button
                        v-if="user.status === 'pending'"
                        @click="resendInvitation(user.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Reenviar invitación
                      </button>
                      <button
                        @click="deleteUser(user.id)"
                        class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="filteredUsers.length > 0" class="bg-white px-6 py-3 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="previousPage"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
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
                  @click="previousPage"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                
                <button
                  v-for="page in visiblePages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === currentPage
                      ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                  ]"
                >
                  {{ page }}
                </button>
                
                <button
                  @click="nextPage"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Invite User Modal -->
    <div v-if="showInviteModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-1/2 lg:w-1/3 shadow-lg rounded-lg bg-white">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Invitar Usuario</h3>
          <button
            @click="closeInviteModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="sendInvitation" class="space-y-4">
          <div>
            <label for="invite-email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="invite-email"
              v-model="inviteForm.email"
              type="email"
              required
              placeholder="usuario@ejemplo.com"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label for="invite-name" class="block text-sm font-medium text-gray-700">Nombre completo</label>
            <input
              id="invite-name"
              v-model="inviteForm.name"
              type="text"
              required
              placeholder="Juan Pérez"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label for="invite-role" class="block text-sm font-medium text-gray-700">Rol</label>
            <select
              id="invite-role"
              v-model="inviteForm.role"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="viewer">Visualizador</option>
              <option value="editor">Editor</option>
              <option value="admin">Administrador</option>
            </select>
          </div>
          
          <div>
            <label for="invite-message" class="block text-sm font-medium text-gray-700">Mensaje personalizado (opcional)</label>
            <textarea
              id="invite-message"
              v-model="inviteForm.message"
              rows="3"
              placeholder="Mensaje de bienvenida..."
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>
          
          <div class="flex items-center justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="closeInviteModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isInviting"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isInviting ? 'Enviando...' : 'Enviar Invitación' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { debounce } from 'lodash-es'

export default {
  name: 'Users',
  setup() {
    const toast = useToast()
    
    // State
    const isLoading = ref(false)
    const isInviting = ref(false)
    const users = ref([])
    const showInviteModal = ref(false)
    const activeUserMenu = ref(null)
    const currentPage = ref(1)
    const itemsPerPage = ref(10)
    
    // Filters
    const filters = ref({
      search: '',
      role: '',
      status: '',
      sort: 'name_asc'
    })
    
    // Invite form
    const inviteForm = ref({
      email: '',
      name: '',
      role: 'viewer',
      message: ''
    })
    
    // Stats
    const stats = ref({
      totalUsers: 0,
      activeUsers: 0,
      pendingUsers: 0,
      adminUsers: 0
    })
    
    // Mock data
    const mockUsers = [
      {
        id: 1,
        name: 'Juan Pérez',
        email: 'juan.perez@empresa.com',
        role: 'admin',
        status: 'active',
        created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        last_login: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 2,
        name: 'María García',
        email: 'maria.garcia@empresa.com',
        role: 'editor',
        status: 'active',
        created_at: new Date(Date.now() - 25 * 24 * 60 * 60 * 1000).toISOString(),
        last_login: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 3,
        name: 'Carlos López',
        email: 'carlos.lopez@empresa.com',
        role: 'viewer',
        status: 'active',
        created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
        last_login: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 4,
        name: 'Ana Martínez',
        email: 'ana.martinez@empresa.com',
        role: 'editor',
        status: 'pending',
        created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        last_login: null
      },
      {
        id: 5,
        name: 'Roberto Silva',
        email: 'roberto.silva@empresa.com',
        role: 'viewer',
        status: 'inactive',
        created_at: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(),
        last_login: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString()
      }
    ]
    
    // Computed
    const hasActiveFilters = computed(() => {
      return filters.value.search || filters.value.role || filters.value.status
    })
    
    const filteredUsers = computed(() => {
      let filtered = [...users.value]
      
      if (filters.value.search) {
        const search = filters.value.search.toLowerCase()
        filtered = filtered.filter(user => 
          user.name.toLowerCase().includes(search) ||
          user.email.toLowerCase().includes(search)
        )
      }
      
      if (filters.value.role) {
        filtered = filtered.filter(user => user.role === filters.value.role)
      }
      
      if (filters.value.status) {
        filtered = filtered.filter(user => user.status === filters.value.status)
      }
      
      // Sort
      const [field, direction] = filters.value.sort.split('_')
      filtered.sort((a, b) => {
        let aVal = a[field]
        let bVal = b[field]
        
        if (field === 'created_at' || field === 'last_login') {
          aVal = new Date(aVal || 0)
          bVal = new Date(bVal || 0)
        }
        
        if (direction === 'desc') {
          return bVal > aVal ? 1 : -1
        } else {
          return aVal > bVal ? 1 : -1
        }
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
      
      return pages
    })
    
    // Methods
    const loadUsers = async () => {
      try {
        isLoading.value = true
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        users.value = mockUsers
        
        // Calculate stats
        stats.value = {
          totalUsers: users.value.length,
          activeUsers: users.value.filter(user => user.status === 'active').length,
          pendingUsers: users.value.filter(user => user.status === 'pending').length,
          adminUsers: users.value.filter(user => user.role === 'admin').length
        }
        
      } catch (error) {
        console.error('Error loading users:', error)
        toast.error('Error al cargar los usuarios')
      } finally {
        isLoading.value = false
      }
    }
    
    const refreshUsers = () => {
      loadUsers()
    }
    
    const applyFilters = () => {
      currentPage.value = 1
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        role: '',
        status: '',
        sort: 'name_asc'
      }
      currentPage.value = 1
    }
    
    const debouncedSearch = debounce(() => {
      applyFilters()
    }, 300)
    
    const sendInvitation = async () => {
      try {
        isInviting.value = true
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Add new user to list
        const newUser = {
          id: Date.now(),
          name: inviteForm.value.name,
          email: inviteForm.value.email,
          role: inviteForm.value.role,
          status: 'pending',
          created_at: new Date().toISOString(),
          last_login: null
        }
        
        users.value.unshift(newUser)
        
        toast.success('Invitación enviada exitosamente')
        closeInviteModal()
        
      } catch (error) {
        console.error('Error sending invitation:', error)
        toast.error('Error al enviar la invitación')
      } finally {
        isInviting.value = false
      }
    }
    
    const closeInviteModal = () => {
      showInviteModal.value = false
      inviteForm.value = {
        email: '',
        name: '',
        role: 'viewer',
        message: ''
      }
    }
    
    const toggleUserMenu = (id) => {
      activeUserMenu.value = activeUserMenu.value === id ? null : id
    }
    
    const editUser = (user) => {
      toast.info(`Editando usuario: ${user.name}`)
      activeUserMenu.value = null
    }
    
    const changeUserRole = (user) => {
      toast.info(`Cambiando rol de: ${user.name}`)
      activeUserMenu.value = null
    }
    
    const activateUser = (id) => {
      const user = users.value.find(u => u.id === id)
      if (user) {
        user.status = 'active'
        toast.success('Usuario activado')
      }
      activeUserMenu.value = null
    }
    
    const deactivateUser = (id) => {
      const user = users.value.find(u => u.id === id)
      if (user) {
        user.status = 'inactive'
        toast.success('Usuario desactivado')
      }
      activeUserMenu.value = null
    }
    
    const resendInvitation = (id) => {
      toast.success('Invitación reenviada')
      activeUserMenu.value = null
    }
    
    const deleteUser = (id) => {
      if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
        users.value = users.value.filter(user => user.id !== id)
        toast.success('Usuario eliminado')
      }
      activeUserMenu.value = null
    }
    
    // Pagination
    const goToPage = (page) => {
      if (page !== '...' && page >= 1 && page <= totalPages.value) {
        currentPage.value = page
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
    
    // Utility functions
    const getUserInitials = (name) => {
      return name.split(' ').map(n => n[0]).join('').toUpperCase()
    }
    
    const getRoleBadgeClass = (role) => {
      const classes = {
        admin: 'bg-purple-100 text-purple-800',
        editor: 'bg-blue-100 text-blue-800',
        viewer: 'bg-gray-100 text-gray-800'
      }
      return classes[role] || 'bg-gray-100 text-gray-800'
    }
    
    const getRoleText = (role) => {
      const texts = {
        admin: 'Administrador',
        editor: 'Editor',
        viewer: 'Visualizador'
      }
      return texts[role] || role
    }
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        active: 'bg-green-100 text-green-800',
        pending: 'bg-yellow-100 text-yellow-800',
        inactive: 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    }
    
    const getStatusText = (status) => {
      const texts = {
        active: 'Activo',
        pending: 'Pendiente',
        inactive: 'Inactivo'
      }
      return texts[status] || status
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diffInHours = (now - date) / (1000 * 60 * 60)
      
      if (diffInHours < 1) {
        return 'Hace unos minutos'
      } else if (diffInHours < 24) {
        return `Hace ${Math.floor(diffInHours)} horas`
      } else if (diffInHours < 48) {
        return 'Ayer'
      } else {
        return date.toLocaleDateString('es-ES', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        })
      }
    }
    
    // Lifecycle
    onMounted(() => {
      loadUsers()
    })
    
    // Close menu when clicking outside
    const handleClickOutside = (event) => {
      if (!event.target.closest('.relative')) {
        activeUserMenu.value = null
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })
    
    return {
      // State
      isLoading,
      isInviting,
      users,
      showInviteModal,
      activeUserMenu,
      currentPage,
      itemsPerPage,
      filters,
      inviteForm,
      stats,
      
      // Computed
      hasActiveFilters,
      filteredUsers,
      totalPages,
      paginatedUsers,
      visiblePages,
      
      // Methods
      refreshUsers,
      applyFilters,
      clearFilters,
      debouncedSearch,
      sendInvitation,
      closeInviteModal,
      toggleUserMenu,
      editUser,
      changeUserRole,
      activateUser,
      deactivateUser,
      resendInvitation,
      deleteUser,
      goToPage,
      previousPage,
      nextPage,
      
      // Utilities
      getUserInitials,
      getRoleBadgeClass,
      getRoleText,
      getStatusBadgeClass,
      getStatusText,
      formatDate
    }
  }
}
</script>

<style scoped>
.users-page {
  @apply h-full flex flex-col;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>