<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Gestión de Roles</h3>
          <p class="text-sm text-gray-600 mt-1">Administra roles y permisos del equipo</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Tabs -->
      <div class="mt-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeTab = 'list'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'list'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Roles Existentes ({{ roles.length }})
            </button>
            <button
              @click="activeTab = 'create'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'create'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ editingRole ? 'Editar Rol' : 'Crear Rol' }}
            </button>
            <button
              @click="activeTab = 'permissions'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'permissions'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              Matriz de Permisos
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="mt-6">
        <!-- Roles List -->
        <div v-if="activeTab === 'list'" class="space-y-4">
          <div class="flex justify-between items-center">
            <p class="text-sm text-gray-600">
              Gestiona los roles disponibles en tu organización
            </p>
            <button
              @click="createNewRole"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <PlusIcon class="h-5 w-5" />
              <span>Nuevo Rol</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              v-for="role in roles"
              :key="role.id"
              class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div :class="[
                    'p-2 rounded-lg',
                    getRoleIconColor(role.name)
                  ]">
                    <component :is="getRoleIcon(role.name)" class="h-6 w-6" />
                  </div>
                  <div>
                    <h4 class="text-lg font-medium text-gray-900">{{ role.displayName }}</h4>
                    <p class="text-sm text-gray-600">{{ role.description }}</p>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2" v-if="!isSystemRole(role.name)">
                  <button
                    @click="editRole(role)"
                    class="text-blue-600 hover:text-blue-800 p-1"
                    title="Editar rol"
                  >
                    <PencilIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="deleteRole(role)"
                    class="text-red-600 hover:text-red-800 p-1"
                    title="Eliminar rol"
                  >
                    <TrashIcon class="h-4 w-4" />
                  </button>
                </div>
              </div>
              
              <div class="space-y-3">
                <div>
                  <span class="text-sm font-medium text-gray-700">Permisos:</span>
                  <div class="mt-2 flex flex-wrap gap-1">
                    <span
                      v-for="permission in getPermissionLabels(role.permissions)"
                      :key="permission"
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ permission }}
                    </span>
                  </div>
                </div>
                
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Miembros con este rol:</span>
                  <span class="font-medium text-gray-900">{{ getRoleMemberCount(role.name) }}</span>
                </div>
                
                <div v-if="isSystemRole(role.name)" class="flex items-center space-x-2">
                  <ShieldCheckIcon class="h-4 w-4 text-gray-400" />
                  <span class="text-xs text-gray-500">Rol del sistema (no editable)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Create/Edit Role -->
        <div v-if="activeTab === 'create'" class="space-y-6">
          <form @submit.prevent="saveRole" class="space-y-6">
            <!-- Basic Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="role-name" class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Rol *
                </label>
                <input
                  id="role-name"
                  v-model="roleForm.displayName"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Nombre del rol"
                />
              </div>
              
              <div>
                <label for="role-key" class="block text-sm font-medium text-gray-700 mb-2">
                  Clave del Rol *
                </label>
                <input
                  id="role-key"
                  v-model="roleForm.name"
                  type="text"
                  required
                  :disabled="!!editingRole"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
                  placeholder="role_key"
                />
                <p class="mt-1 text-xs text-gray-500">
                  Solo letras minúsculas, números y guiones bajos
                </p>
              </div>
            </div>
            
            <div>
              <label for="role-description" class="block text-sm font-medium text-gray-700 mb-2">
                Descripción *
              </label>
              <textarea
                id="role-description"
                v-model="roleForm.description"
                rows="3"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Descripción del rol y sus responsabilidades..."
              ></textarea>
            </div>

            <!-- Permissions -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-3">
                Permisos *
              </label>
              
              <div class="space-y-4">
                <div v-for="category in permissionCategories" :key="category.name" class="border border-gray-200 rounded-lg p-4">
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-900">{{ category.label }}</h4>
                    <button
                      type="button"
                      @click="toggleCategoryPermissions(category.name)"
                      class="text-xs text-blue-600 hover:text-blue-800"
                    >
                      {{ isCategorySelected(category.name) ? 'Deseleccionar todo' : 'Seleccionar todo' }}
                    </button>
                  </div>
                  
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <label
                      v-for="permission in category.permissions"
                      :key="permission.value"
                      class="flex items-start space-x-3 p-2 rounded hover:bg-gray-50 cursor-pointer"
                    >
                      <input
                        v-model="roleForm.permissions"
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
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
              <button
                type="button"
                @click="resetForm"
                class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="!isFormValid"
                class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ editingRole ? 'Actualizar' : 'Crear' }} Rol
              </button>
            </div>
          </form>
        </div>

        <!-- Permissions Matrix -->
        <div v-if="activeTab === 'permissions'" class="space-y-6">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Permiso
                  </th>
                  <th
                    v-for="role in roles"
                    :key="role.id"
                    class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {{ role.displayName }}
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="permission in allPermissions" :key="permission.value" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ permission.label }}</div>
                      <div class="text-sm text-gray-500">{{ permission.description }}</div>
                    </div>
                  </td>
                  <td
                    v-for="role in roles"
                    :key="role.id"
                    class="px-6 py-4 whitespace-nowrap text-center"
                  >
                    <CheckIcon
                      v-if="roleHasPermission(role, permission.value)"
                      class="h-5 w-5 text-green-500 mx-auto"
                    />
                    <XMarkIcon
                      v-else
                      class="h-5 w-5 text-gray-300 mx-auto"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  XMarkIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  ShieldCheckIcon,
  CheckIcon,
  UserGroupIcon,
  CogIcon,
  EyeIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  roles: {
    type: Array,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const activeTab = ref('list')
const editingRole = ref(null)
const roleForm = ref({
  name: '',
  displayName: '',
  description: '',
  permissions: []
})

const permissionCategories = ref([
  {
    name: 'chatbots',
    label: 'Chatbots',
    permissions: [
      { value: 'chatbots.read', label: 'Ver Chatbots', description: 'Ver lista y detalles de chatbots' },
      { value: 'chatbots.create', label: 'Crear Chatbots', description: 'Crear nuevos chatbots' },
      { value: 'chatbots.edit', label: 'Editar Chatbots', description: 'Modificar chatbots existentes' },
      { value: 'chatbots.delete', label: 'Eliminar Chatbots', description: 'Eliminar chatbots' },
      { value: 'chatbots.deploy', label: 'Desplegar Chatbots', description: 'Publicar y despublicar chatbots' }
    ]
  },
  {
    name: 'conversations',
    label: 'Conversaciones',
    permissions: [
      { value: 'conversations.read', label: 'Ver Conversaciones', description: 'Acceder a conversaciones' },
      { value: 'conversations.participate', label: 'Participar', description: 'Responder en conversaciones' },
      { value: 'conversations.assign', label: 'Asignar', description: 'Asignar conversaciones a agentes' },
      { value: 'conversations.close', label: 'Cerrar', description: 'Cerrar conversaciones' },
      { value: 'conversations.export', label: 'Exportar', description: 'Exportar datos de conversaciones' }
    ]
  },
  {
    name: 'analytics',
    label: 'Analytics',
    permissions: [
      { value: 'analytics.read', label: 'Ver Analytics', description: 'Acceder a métricas y reportes' },
      { value: 'analytics.export', label: 'Exportar Reportes', description: 'Exportar datos analíticos' },
      { value: 'analytics.advanced', label: 'Analytics Avanzado', description: 'Acceso a métricas avanzadas' }
    ]
  },
  {
    name: 'team',
    label: 'Gestión de Equipo',
    permissions: [
      { value: 'team.read', label: 'Ver Equipo', description: 'Ver miembros del equipo' },
      { value: 'team.invite', label: 'Invitar Miembros', description: 'Enviar invitaciones' },
      { value: 'team.manage', label: 'Gestionar Equipo', description: 'Editar y eliminar miembros' },
      { value: 'team.roles', label: 'Gestionar Roles', description: 'Crear y modificar roles' }
    ]
  },
  {
    name: 'settings',
    label: 'Configuración',
    permissions: [
      { value: 'settings.read', label: 'Ver Configuración', description: 'Acceder a configuraciones' },
      { value: 'settings.edit', label: 'Editar Configuración', description: 'Modificar configuraciones' },
      { value: 'settings.billing', label: 'Gestionar Facturación', description: 'Acceso a facturación y pagos' },
      { value: 'settings.integrations', label: 'Gestionar Integraciones', description: 'Configurar integraciones' }
    ]
  },
  {
    name: 'admin',
    label: 'Administración',
    permissions: [
      { value: 'admin.full', label: 'Acceso Completo', description: 'Acceso total al sistema' },
      { value: 'admin.audit', label: 'Logs de Auditoría', description: 'Ver logs del sistema' },
      { value: 'admin.backup', label: 'Respaldos', description: 'Gestionar respaldos' }
    ]
  }
])

// Computed properties
const allPermissions = computed(() => {
  return permissionCategories.value.flatMap(category => category.permissions)
})

const isFormValid = computed(() => {
  return roleForm.value.name && 
         roleForm.value.displayName && 
         roleForm.value.description && 
         roleForm.value.permissions.length > 0
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const getRoleIcon = (roleName) => {
  const icons = {
    admin: CogIcon,
    manager: UserGroupIcon,
    agent: ChatBubbleLeftRightIcon,
    viewer: EyeIcon
  }
  return icons[roleName] || UserGroupIcon
}

const getRoleIconColor = (roleName) => {
  const colors = {
    admin: 'bg-red-100 text-red-600',
    manager: 'bg-blue-100 text-blue-600',
    agent: 'bg-green-100 text-green-600',
    viewer: 'bg-gray-100 text-gray-600'
  }
  return colors[roleName] || 'bg-purple-100 text-purple-600'
}

const isSystemRole = (roleName) => {
  return ['admin', 'manager', 'agent', 'viewer'].includes(roleName)
}

const getPermissionLabels = (permissions) => {
  if (permissions.includes('all') || permissions.includes('admin.full')) {
    return ['Todos los permisos']
  }
  
  return permissions.map(permission => {
    const found = allPermissions.value.find(p => p.value === permission)
    return found ? found.label : permission
  }).slice(0, 3).concat(permissions.length > 3 ? [`+${permissions.length - 3} más`] : [])
}

const getRoleMemberCount = (roleName) => {
  // Mock data - in real app, this would come from props or API
  const counts = {
    admin: 1,
    manager: 2,
    agent: 3,
    viewer: 1
  }
  return counts[roleName] || 0
}

const createNewRole = () => {
  editingRole.value = null
  resetForm()
  activeTab.value = 'create'
}

const editRole = (role) => {
  editingRole.value = role
  roleForm.value = {
    name: role.name,
    displayName: role.displayName,
    description: role.description,
    permissions: [...role.permissions]
  }
  activeTab.value = 'create'
}

const deleteRole = (role) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el rol "${role.displayName}"?`)) {
    console.log('Eliminando rol:', role.name)
    // Emit delete event or handle deletion
  }
}

const resetForm = () => {
  editingRole.value = null
  roleForm.value = {
    name: '',
    displayName: '',
    description: '',
    permissions: []
  }
  activeTab.value = 'list'
}

const saveRole = () => {
  if (!isFormValid.value) return
  
  const roleData = {
    ...roleForm.value,
    id: editingRole.value ? editingRole.value.id : Date.now()
  }
  
  emit('save', roleData)
  resetForm()
}

const toggleCategoryPermissions = (categoryName) => {
  const category = permissionCategories.value.find(c => c.name === categoryName)
  if (!category) return
  
  const categoryPermissions = category.permissions.map(p => p.value)
  const hasAll = categoryPermissions.every(p => roleForm.value.permissions.includes(p))
  
  if (hasAll) {
    // Remove all category permissions
    roleForm.value.permissions = roleForm.value.permissions.filter(
      p => !categoryPermissions.includes(p)
    )
  } else {
    // Add all category permissions
    categoryPermissions.forEach(permission => {
      if (!roleForm.value.permissions.includes(permission)) {
        roleForm.value.permissions.push(permission)
      }
    })
  }
}

const isCategorySelected = (categoryName) => {
  const category = permissionCategories.value.find(c => c.name === categoryName)
  if (!category) return false
  
  const categoryPermissions = category.permissions.map(p => p.value)
  return categoryPermissions.every(p => roleForm.value.permissions.includes(p))
}

const roleHasPermission = (role, permission) => {
  return role.permissions.includes('all') || 
         role.permissions.includes('admin.full') || 
         role.permissions.includes(permission)
}
</script>