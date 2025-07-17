<template>
  <div class="role-switcher bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-semibold text-gray-800">
        <i class="fas fa-user-cog mr-2 text-blue-500"></i>
        Demo - Cambiar Rol
      </h3>
      <span class="px-3 py-1 text-xs font-medium rounded-full" :class="getRoleBadgeClass(currentRole)">
        {{ getRoleLabel(currentRole) }}
      </span>
    </div>
    
    <div class="mb-4">
      <p class="text-sm text-gray-600 mb-2">
        Usuario actual: <strong>{{ user?.full_name }}</strong>
      </p>
      <p class="text-xs text-gray-500">
        Email: {{ user?.email }}
      </p>
    </div>
    
    <div class="space-y-3">
      <h4 class="text-sm font-medium text-gray-700">Cambiar a:</h4>
      
      <div class="grid grid-cols-1 gap-2">
        <button
          v-for="role in availableRoles"
          :key="role.value"
          @click="switchRole(role.value)"
          :disabled="role.value === currentRole"
          class="flex items-center justify-between p-3 border rounded-lg transition-all duration-200 hover:shadow-md"
          :class="{
            'border-blue-500 bg-blue-50': role.value === currentRole,
            'border-gray-200 hover:border-blue-300': role.value !== currentRole,
            'opacity-50 cursor-not-allowed': role.value === currentRole
          }"
        >
          <div class="flex items-center space-x-3">
            <i :class="getRoleIcon(role.value)" class="text-lg"></i>
            <div class="text-left">
              <div class="font-medium text-sm">{{ role.label }}</div>
              <div class="text-xs text-gray-500">{{ role.description }}</div>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <span v-if="role.value === currentRole" class="text-xs text-blue-600 font-medium">
              Actual
            </span>
            <i v-else class="fas fa-arrow-right text-gray-400"></i>
          </div>
        </button>
      </div>
    </div>
    
    <div class="mt-6 p-4 bg-gray-50 rounded-lg">
      <h5 class="text-sm font-medium text-gray-700 mb-2">
        <i class="fas fa-shield-alt mr-1"></i>
        Permisos actuales:
      </h5>
      <div class="flex flex-wrap gap-1">
        <span
          v-for="permission in userPermissions"
          :key="permission"
          class="px-2 py-1 text-xs bg-green-100 text-green-700 rounded-full"
        >
          {{ formatPermission(permission) }}
        </span>
      </div>
    </div>
    
    <div class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
      <div class="flex items-start space-x-2">
        <i class="fas fa-info-circle text-yellow-600 mt-0.5"></i>
        <div class="text-xs text-yellow-700">
          <strong>Modo Demo:</strong> Los cambios de rol son temporales y solo afectan la interfaz. 
          En producción, los roles son gestionados por administradores.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const toast = useToast()

// Computed properties
const user = computed(() => authStore.user)
const currentRole = computed(() => authStore.userRole)
const availableRoles = computed(() => authStore.getAvailableRoles())
const userPermissions = computed(() => authStore.getUserPermissions())

// Methods
const switchRole = async (role) => {
  try {
    const success = await authStore.switchToRole(role)
    if (success) {
      console.log('✅ Rol cambiado exitosamente a:', role)
      // Reload page to reflect role changes in UI
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } else {
      console.error('❌ Error al cambiar rol a:', role)
    }
  } catch (error) {
    console.error('❌ Error en switchRole:', error)
    toast.error('Error al cambiar el rol')
  }
}

const getRoleLabel = (role) => {
  const roleMap = {
    'user': 'Usuario',
    'viewer': 'Visualizador',
    'org_admin': 'Admin Org',
    'admin': 'Administrador',
    'super_admin': 'Super Admin'
  }
  return roleMap[role] || role
}

const getRoleBadgeClass = (role) => {
  const classMap = {
    'user': 'bg-blue-100 text-blue-800',
    'viewer': 'bg-gray-100 text-gray-800',
    'org_admin': 'bg-purple-100 text-purple-800',
    'admin': 'bg-red-100 text-red-800',
    'super_admin': 'bg-yellow-100 text-yellow-800'
  }
  return classMap[role] || 'bg-gray-100 text-gray-800'
}

const getRoleIcon = (role) => {
  const iconMap = {
    'user': 'fas fa-user text-blue-500',
    'viewer': 'fas fa-eye text-gray-500',
    'org_admin': 'fas fa-users-cog text-purple-500',
    'admin': 'fas fa-user-shield text-red-500',
    'super_admin': 'fas fa-crown text-yellow-500'
  }
  return iconMap[role] || 'fas fa-user text-gray-500'
}

const formatPermission = (permission) => {
  const permissionMap = {
    'read_own_data': 'Leer datos propios',
    'create_conversations': 'Crear conversaciones',
    'read_all_data': 'Leer todos los datos',
    'create_users': 'Crear usuarios',
    'manage_system': 'Gestionar sistema',
    'delete_data': 'Eliminar datos',
    'full_access': 'Acceso completo',
    'system_config': 'Configurar sistema',
    'user_management': 'Gestión de usuarios',
    'organization_management': 'Gestión de organizaciones',
    'manage_organization': 'Gestionar organización',
    'view_analytics': 'Ver analíticas',
    'read_only': 'Solo lectura'
  }
  return permissionMap[permission] || permission
}
</script>

<style scoped>
.role-switcher {
  max-width: 400px;
}

.role-switcher button:hover:not(:disabled) {
  transform: translateY(-1px);
}

.role-switcher button:active:not(:disabled) {
  transform: translateY(0);
}
</style>