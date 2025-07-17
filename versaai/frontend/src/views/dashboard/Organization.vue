<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Organización</h1>
        <p class="text-gray-600">Gestiona la información y configuración de tu organización</p>
      </div>
      <button
        @click="editMode = !editMode"
        class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
      >
        {{ editMode ? 'Cancelar' : 'Editar' }}
      </button>
    </div>

    <!-- Organization Info -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-6">Información de la Organización</h2>
      
      <form @submit.prevent="updateOrganization" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nombre de la Organización
            </label>
            <input
              id="organization-name"
              name="organization-name"
              v-model="organizationData.name"
              type="text"
              :disabled="!editMode"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
              required
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Sitio Web
            </label>
            <input
              id="organization-website"
              name="organization-website"
              v-model="organizationData.website"
              type="url"
              :disabled="!editMode"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Industria
            </label>
            <select
              id="organization-industry"
              name="organization-industry"
              v-model="organizationData.industry"
              :disabled="!editMode"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
            >
              <option value="">Seleccionar industria</option>
              <option value="technology">Tecnología</option>
              <option value="healthcare">Salud</option>
              <option value="finance">Finanzas</option>
              <option value="education">Educación</option>
              <option value="retail">Retail</option>
              <option value="manufacturing">Manufactura</option>
              <option value="consulting">Consultoría</option>
              <option value="other">Otro</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Tamaño de la Empresa
            </label>
            <select
              id="organization-size"
              name="organization-size"
              v-model="organizationData.size"
              :disabled="!editMode"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
            >
              <option value="">Seleccionar tamaño</option>
              <option value="1-10">1-10 empleados</option>
              <option value="11-50">11-50 empleados</option>
              <option value="51-200">51-200 empleados</option>
              <option value="201-1000">201-1000 empleados</option>
              <option value="1000+">1000+ empleados</option>
            </select>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Descripción
          </label>
          <textarea
            id="organization-description"
            name="organization-description"
            v-model="organizationData.description"
            :disabled="!editMode"
            rows="4"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
            placeholder="Describe tu organización..."
          ></textarea>
        </div>
        
        <div v-if="editMode" class="flex justify-end space-x-3">
          <button
            type="button"
            @click="editMode = false"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 disabled:opacity-50"
          >
            {{ loading ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Team Members -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-lg font-semibold text-gray-900">Miembros del Equipo</h2>
        <button
          @click="showInviteModal = true"
          class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
        >
          Invitar Miembro
        </button>
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
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="member in teamMembers" :key="member.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img
                      class="h-10 w-10 rounded-full"
                      :src="member.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(member.name)}&background=6366f1&color=fff`"
                      :alt="member.name"
                    />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ member.name }}</div>
                    <div class="text-sm text-gray-500">{{ member.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    member.role === 'admin' ? 'bg-red-100 text-red-800' :
                    member.role === 'manager' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  ]"
                >
                  {{ getRoleLabel(member.role) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                    member.status === 'active' ? 'bg-green-100 text-green-800' :
                    member.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]"
                >
                  {{ getStatusLabel(member.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(member.lastAccess) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <button
                    @click="editMember(member)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    Editar
                  </button>
                  <button
                    v-if="member.id !== currentUser.id"
                    @click="removeMember(member)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Usage Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <UsersIcon class="h-8 w-8 text-primary-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Miembros Activos</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.activeMembers }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <ChatBubbleLeftRightIcon class="h-8 w-8 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Chatbots Totales</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalChatbots }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <DocumentTextIcon class="h-8 w-8 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Documentos</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalDocuments }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Invite Member Modal -->
    <div
      v-if="showInviteModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showInviteModal = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Invitar Miembro</h3>
          
          <form @submit.prevent="inviteMember" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                id="invite-email"
                name="invite-email"
                v-model="inviteForm.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Rol
              </label>
              <select
                id="invite-role"
                name="invite-role"
                v-model="inviteForm.role"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                required
              >
                <option value="member">Miembro</option>
                <option value="manager">Manager</option>
                <option value="admin">Administrador</option>
              </select>
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showInviteModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="inviteLoading"
                class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 disabled:opacity-50"
              >
                {{ inviteLoading ? 'Enviando...' : 'Enviar Invitación' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UsersIcon, ChatBubbleLeftRightIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/api'

const authStore = useAuthStore()
const toast = useToast()

const editMode = ref(false)
const loading = ref(false)
const showInviteModal = ref(false)
const inviteLoading = ref(false)

const organizationData = ref({
  name: '',
  website: '',
  industry: '',
  size: '',
  description: ''
})

const teamMembers = ref([])
const stats = ref({
  activeMembers: 0,
  totalChatbots: 0,
  totalDocuments: 0
})

const inviteForm = ref({
  email: '',
  role: 'member'
})

const currentUser = authStore.user

const getRoleLabel = (role) => {
  const labels = {
    admin: 'Administrador',
    manager: 'Manager',
    member: 'Miembro'
  }
  return labels[role] || role
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    pending: 'Pendiente',
    inactive: 'Inactivo'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  if (!date) return 'Nunca'
  return format(new Date(date), 'dd MMM yyyy', { locale: es })
}

const fetchOrganizationData = async () => {
  try {
    const response = await api.get('/organization')
    organizationData.value = response.data
  } catch (error) {
    console.error('Error fetching organization data:', error)
    toast.error('Error al cargar los datos de la organización')
  }
}

const fetchTeamMembers = async () => {
  try {
    const response = await api.get('/organization/members')
    teamMembers.value = response.data
  } catch (error) {
    console.error('Error fetching team members:', error)
    toast.error('Error al cargar los miembros del equipo')
  }
}

const fetchStats = async () => {
  try {
    const response = await api.get('/organization/stats')
    stats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  }
}

const updateOrganization = async () => {
  loading.value = true
  try {
    await api.put('/organization', organizationData.value)
    toast.success('Organización actualizada correctamente')
    editMode.value = false
  } catch (error) {
    console.error('Error updating organization:', error)
    toast.error('Error al actualizar la organización')
  } finally {
    loading.value = false
  }
}

const inviteMember = async () => {
  inviteLoading.value = true
  try {
    await api.post('/organization/invite', inviteForm.value)
    toast.success('Invitación enviada correctamente')
    showInviteModal.value = false
    inviteForm.value = { email: '', role: 'member' }
    await fetchTeamMembers()
  } catch (error) {
    console.error('Error inviting member:', error)
    toast.error('Error al enviar la invitación')
  } finally {
    inviteLoading.value = false
  }
}

const editMember = (member) => {
  // TODO: Implement edit member functionality
  toast.info('Funcionalidad de edición próximamente')
}

const removeMember = async (member) => {
  if (!confirm(`¿Estás seguro de que quieres eliminar a ${member.name}?`)) {
    return
  }
  
  try {
    await api.delete(`/organization/members/${member.id}`)
    toast.success('Miembro eliminado correctamente')
    await fetchTeamMembers()
  } catch (error) {
    console.error('Error removing member:', error)
    toast.error('Error al eliminar el miembro')
  }
}

onMounted(async () => {
  await Promise.all([
    fetchOrganizationData(),
    fetchTeamMembers(),
    fetchStats()
  ])
})
</script>