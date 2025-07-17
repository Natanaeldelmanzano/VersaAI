<template>
  <div class="team-management">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
      <div>
        <h2 class="text-3xl font-bold text-gray-900">Gestión de Equipos</h2>
        <p class="text-gray-600 mt-2">Administra equipos, roles y permisos empresariales</p>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="showCreateTeamModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Crear Equipo
        </button>
        
        <button
          @click="showInviteModal = true"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          <UserPlusIcon class="w-4 h-4 mr-2" />
          Invitar Usuario
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Total Equipos</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ totalTeams }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <UsersIcon class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Miembros Activos</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ activeMembers }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <UserIcon class="w-6 h-6 text-green-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Invitaciones Pendientes</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ pendingInvitations }}</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
            <ClockIcon class="w-6 h-6 text-yellow-600" />
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600">Roles Personalizados</p>
            <p class="text-3xl font-bold text-gray-900 mt-2">{{ customRoles }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <ShieldCheckIcon class="w-6 h-6 text-purple-600" />
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div class="flex-1 max-w-md">
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar equipos o miembros..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <select 
            v-model="selectedDepartment"
            class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="">Todos los departamentos</option>
            <option value="engineering">Ingeniería</option>
            <option value="sales">Ventas</option>
            <option value="marketing">Marketing</option>
            <option value="support">Soporte</option>
            <option value="hr">Recursos Humanos</option>
          </select>
          
          <select 
            v-model="selectedRole"
            class="rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="">Todos los roles</option>
            <option value="admin">Administrador</option>
            <option value="manager">Manager</option>
            <option value="member">Miembro</option>
            <option value="viewer">Visualizador</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Teams Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
      <div 
        v-for="team in filteredTeams" 
        :key="team.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
      >
        <div class="p-6">
          <!-- Team Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div :class="['w-12 h-12 rounded-lg flex items-center justify-center', team.color]">
                <component :is="team.icon" class="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ team.name }}</h3>
                <p class="text-sm text-gray-600">{{ team.department }}</p>
              </div>
            </div>
            
            <div class="relative">
              <button
                @click="toggleTeamMenu(team.id)"
                class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <EllipsisVerticalIcon class="w-5 h-5" />
              </button>
              
              <!-- Dropdown Menu -->
              <div 
                v-if="activeTeamMenu === team.id"
                class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-10"
              >
                <div class="py-1">
                  <button
                    @click="editTeam(team)"
                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <PencilIcon class="w-4 h-4 inline mr-2" />
                    Editar equipo
                  </button>
                  <button
                    @click="manageMembers(team)"
                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <UsersIcon class="w-4 h-4 inline mr-2" />
                    Gestionar miembros
                  </button>
                  <button
                    @click="viewPermissions(team)"
                    class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <ShieldCheckIcon class="w-4 h-4 inline mr-2" />
                    Permisos
                  </button>
                  <hr class="my-1" />
                  <button
                    @click="deleteTeam(team)"
                    class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    <TrashIcon class="w-4 h-4 inline mr-2" />
                    Eliminar equipo
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Team Description -->
          <p class="text-gray-600 text-sm mb-4">{{ team.description }}</p>
          
          <!-- Team Stats -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <p class="text-2xl font-bold text-gray-900">{{ team.memberCount }}</p>
              <p class="text-xs text-gray-600">Miembros</p>
            </div>
            <div class="text-center p-3 bg-gray-50 rounded-lg">
              <p class="text-2xl font-bold text-gray-900">{{ team.projectCount }}</p>
              <p class="text-xs text-gray-600">Proyectos</p>
            </div>
          </div>
          
          <!-- Team Members Preview -->
          <div class="flex items-center justify-between">
            <div class="flex -space-x-2">
              <img
                v-for="member in team.members.slice(0, 4)"
                :key="member.id"
                :src="member.avatar"
                :alt="member.name"
                class="w-8 h-8 rounded-full border-2 border-white"
              />
              <div 
                v-if="team.members.length > 4"
                class="w-8 h-8 rounded-full border-2 border-white bg-gray-200 flex items-center justify-center text-xs font-medium text-gray-600"
              >
                +{{ team.members.length - 4 }}
              </div>
            </div>
            
            <span :class="['px-2 py-1 text-xs font-medium rounded-full', team.statusColor]">
              {{ team.status }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Actividad Reciente</h3>
      </div>
      <div class="p-6">
        <div class="space-y-4">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id"
            class="flex items-start space-x-4"
          >
            <div :class="['w-8 h-8 rounded-full flex items-center justify-center', activity.bgColor]">
              <component :is="activity.icon" :class="['w-4 h-4', activity.iconColor]" />
            </div>
            <div class="flex-1">
              <p class="text-sm text-gray-900">
                <span class="font-medium">{{ activity.user }}</span>
                {{ activity.action }}
                <span class="font-medium">{{ activity.target }}</span>
              </p>
              <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Team Modal -->
    <TeamModal
      v-if="showCreateTeamModal"
      :show="showCreateTeamModal"
      @close="showCreateTeamModal = false"
      @save="handleCreateTeam"
    />

    <!-- Invite User Modal -->
    <InviteModal
      v-if="showInviteModal"
      :show="showInviteModal"
      :teams="teams"
      @close="showInviteModal = false"
      @invite="handleInviteUser"
    />

    <!-- Edit Team Modal -->
    <TeamModal
      v-if="showEditTeamModal"
      :show="showEditTeamModal"
      :team="selectedTeam"
      @close="showEditTeamModal = false"
      @save="handleEditTeam"
    />

    <!-- Members Management Modal -->
    <MembersModal
      v-if="showMembersModal"
      :show="showMembersModal"
      :team="selectedTeam"
      @close="showMembersModal = false"
      @update="handleUpdateMembers"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  PlusIcon,
  UserPlusIcon,
  UsersIcon,
  UserIcon,
  ClockIcon,
  ShieldCheckIcon,
  MagnifyingGlassIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon,
  CodeBracketIcon,
  ChartBarIcon,
  MegaphoneIcon,
  LifebuoyIcon,
  UserGroupIcon
} from '@heroicons/vue/24/outline'
import TeamModal from './modals/TeamModal.vue'
import InviteModal from './modals/InviteModal.vue'
import MembersModal from './modals/MembersModal.vue'

// State
const searchQuery = ref('')
const selectedDepartment = ref('')
const selectedRole = ref('')
const activeTeamMenu = ref(null)
const showCreateTeamModal = ref(false)
const showEditTeamModal = ref(false)
const showInviteModal = ref(false)
const showMembersModal = ref(false)
const selectedTeam = ref(null)

// Mock data
const teams = ref([
  {
    id: 1,
    name: 'Equipo de Desarrollo',
    department: 'Ingeniería',
    description: 'Desarrollo de productos y características principales',
    memberCount: 8,
    projectCount: 12,
    status: 'Activo',
    statusColor: 'bg-green-100 text-green-800',
    color: 'bg-blue-500',
    icon: CodeBracketIcon,
    members: [
      { id: 1, name: 'Juan Pérez', avatar: 'https://ui-avatars.com/api/?name=Juan+Perez&background=3B82F6&color=fff' },
      { id: 2, name: 'María García', avatar: 'https://ui-avatars.com/api/?name=Maria+Garcia&background=10B981&color=fff' },
      { id: 3, name: 'Carlos López', avatar: 'https://ui-avatars.com/api/?name=Carlos+Lopez&background=F59E0B&color=fff' },
      { id: 4, name: 'Ana Martín', avatar: 'https://ui-avatars.com/api/?name=Ana+Martin&background=EF4444&color=fff' },
      { id: 5, name: 'Luis Rodríguez', avatar: 'https://ui-avatars.com/api/?name=Luis+Rodriguez&background=8B5CF6&color=fff' }
    ]
  },
  {
    id: 2,
    name: 'Equipo de Marketing',
    department: 'Marketing',
    description: 'Estrategias de marketing y crecimiento',
    memberCount: 5,
    projectCount: 8,
    status: 'Activo',
    statusColor: 'bg-green-100 text-green-800',
    color: 'bg-purple-500',
    icon: MegaphoneIcon,
    members: [
      { id: 6, name: 'Elena Ruiz', avatar: 'https://ui-avatars.com/api/?name=Elena+Ruiz&background=3B82F6&color=fff' },
      { id: 7, name: 'David Sánchez', avatar: 'https://ui-avatars.com/api/?name=David+Sanchez&background=10B981&color=fff' }
    ]
  },
  {
    id: 3,
    name: 'Equipo de Soporte',
    department: 'Soporte',
    description: 'Atención al cliente y soporte técnico',
    memberCount: 6,
    projectCount: 4,
    status: 'Activo',
    statusColor: 'bg-green-100 text-green-800',
    color: 'bg-green-500',
    icon: LifebuoyIcon,
    members: [
      { id: 8, name: 'Carmen Torres', avatar: 'https://ui-avatars.com/api/?name=Carmen+Torres&background=3B82F6&color=fff' }
    ]
  }
])

const recentActivities = ref([
  {
    id: 1,
    user: 'Juan Pérez',
    action: 'se unió al equipo',
    target: 'Desarrollo',
    time: 'Hace 2 horas',
    icon: UserPlusIcon,
    bgColor: 'bg-green-100',
    iconColor: 'text-green-600'
  },
  {
    id: 2,
    user: 'María García',
    action: 'creó el equipo',
    target: 'Analytics',
    time: 'Hace 4 horas',
    icon: PlusIcon,
    bgColor: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    id: 3,
    user: 'Carlos López',
    action: 'actualizó los permisos del equipo',
    target: 'Marketing',
    time: 'Hace 1 día',
    icon: ShieldCheckIcon,
    bgColor: 'bg-purple-100',
    iconColor: 'text-purple-600'
  }
])

// Computed
const totalTeams = computed(() => teams.value.length)
const activeMembers = computed(() => teams.value.reduce((sum, team) => sum + team.memberCount, 0))
const pendingInvitations = computed(() => 3) // Mock data
const customRoles = computed(() => 5) // Mock data

const filteredTeams = computed(() => {
  return teams.value.filter(team => {
    const matchesSearch = !searchQuery.value || 
      team.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      team.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesDepartment = !selectedDepartment.value || 
      team.department.toLowerCase() === selectedDepartment.value
    
    return matchesSearch && matchesDepartment
  })
})

// Methods
const toggleTeamMenu = (teamId) => {
  activeTeamMenu.value = activeTeamMenu.value === teamId ? null : teamId
}

const editTeam = (team) => {
  selectedTeam.value = team
  showEditTeamModal.value = true
  activeTeamMenu.value = null
}

const manageMembers = (team) => {
  selectedTeam.value = team
  showMembersModal.value = true
  activeTeamMenu.value = null
}

const viewPermissions = (team) => {
  // TODO: Implement permissions view
  console.log('View permissions for team:', team.name)
  activeTeamMenu.value = null
}

const deleteTeam = (team) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el equipo "${team.name}"?`)) {
    const index = teams.value.findIndex(t => t.id === team.id)
    if (index > -1) {
      teams.value.splice(index, 1)
    }
  }
  activeTeamMenu.value = null
}

const handleCreateTeam = (teamData) => {
  const newTeam = {
    id: Date.now(),
    ...teamData,
    memberCount: 1,
    projectCount: 0,
    status: 'Activo',
    statusColor: 'bg-green-100 text-green-800',
    members: []
  }
  teams.value.push(newTeam)
  showCreateTeamModal.value = false
}

const handleEditTeam = (teamData) => {
  const index = teams.value.findIndex(t => t.id === selectedTeam.value.id)
  if (index > -1) {
    teams.value[index] = { ...teams.value[index], ...teamData }
  }
  showEditTeamModal.value = false
  selectedTeam.value = null
}

const handleInviteUser = (inviteData) => {
  // TODO: Implement user invitation
  console.log('Invite user:', inviteData)
  showInviteModal.value = false
}

const handleUpdateMembers = (membersData) => {
  // TODO: Implement members update
  console.log('Update members:', membersData)
  showMembersModal.value = false
  selectedTeam.value = null
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeTeamMenu.value = null
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.team-management {
  @apply p-6;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>