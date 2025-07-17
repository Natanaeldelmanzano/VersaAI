<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>
      
      <div class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
        <!-- Header -->
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Mi Perfil</h3>
            <button
              @click="$emit('close')"
              class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>
          
          <!-- User Info -->
          <div class="flex items-center space-x-4 mb-6">
            <div class="relative">
              <img class="h-16 w-16 rounded-full" :src="user.avatar" :alt="user.name" />
              <button
                @click="changeAvatar"
                class="absolute -bottom-1 -right-1 bg-blue-600 text-white rounded-full p-1 hover:bg-blue-700"
              >
                <CameraIcon class="h-4 w-4" />
              </button>
            </div>
            <div class="flex-1">
              <h4 class="text-lg font-semibold text-gray-900">{{ user.name }}</h4>
              <p class="text-sm text-gray-600">{{ user.email }}</p>
              <div class="flex items-center mt-1">
                <span :class="[
                  'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                  user.status === 'online' ? 'bg-green-100 text-green-800' :
                  user.status === 'away' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                ]">
                  <span :class="[
                    'w-1.5 h-1.5 rounded-full mr-1',
                    user.status === 'online' ? 'bg-green-400' :
                    user.status === 'away' ? 'bg-yellow-400' :
                    'bg-gray-400'
                  ]"></span>
                  {{ getStatusText(user.status) }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Profile Options -->
        <div class="divide-y divide-gray-200">
          <!-- Account Section -->
          <div class="px-4 py-4">
            <h5 class="text-sm font-medium text-gray-900 mb-3">Cuenta</h5>
            <div class="space-y-2">
              <button
                @click="navigateTo('/profile/edit')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <UserIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Editar Perfil</span>
                </div>
                <ChevronRightIcon class="h-4 w-4 text-gray-400" />
              </button>
              
              <button
                @click="navigateTo('/profile/security')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <ShieldCheckIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Seguridad</span>
                </div>
                <ChevronRightIcon class="h-4 w-4 text-gray-400" />
              </button>
              
              <button
                @click="navigateTo('/profile/notifications')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <BellIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Notificaciones</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="notificationSettings.enabled" class="w-2 h-2 bg-green-400 rounded-full"></span>
                  <ChevronRightIcon class="h-4 w-4 text-gray-400" />
                </div>
              </button>
            </div>
          </div>
          
          <!-- Preferences Section -->
          <div class="px-4 py-4">
            <h5 class="text-sm font-medium text-gray-900 mb-3">Preferencias</h5>
            <div class="space-y-2">
              <div class="flex items-center justify-between p-3">
                <div class="flex items-center space-x-3">
                  <MoonIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Modo Oscuro</span>
                </div>
                <toggle-switch v-model="preferences.darkMode" />
              </div>
              
              <div class="flex items-center justify-between p-3">
                <div class="flex items-center space-x-3">
                  <SpeakerWaveIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Sonidos</span>
                </div>
                <toggle-switch v-model="preferences.sounds" />
              </div>
              
              <button
                @click="navigateTo('/profile/language')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <LanguageIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Idioma</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-500">{{ preferences.language }}</span>
                  <ChevronRightIcon class="h-4 w-4 text-gray-400" />
                </div>
              </button>
            </div>
          </div>
          
          <!-- Organization Section -->
          <div class="px-4 py-4">
            <h5 class="text-sm font-medium text-gray-900 mb-3">Organización</h5>
            <div class="space-y-2">
              <button
                @click="navigateTo('/organization')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <BuildingOfficeIcon class="h-5 w-5 text-gray-400" />
                  <div>
                    <span class="text-sm text-gray-700 block">{{ user.organization }}</span>
                    <span class="text-xs text-gray-500">{{ user.role }}</span>
                  </div>
                </div>
                <ChevronRightIcon class="h-4 w-4 text-gray-400" />
              </button>
              
              <button
                @click="navigateTo('/team')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <UserGroupIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Mi Equipo</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-500">{{ user.teamMembers }} miembros</span>
                  <ChevronRightIcon class="h-4 w-4 text-gray-400" />
                </div>
              </button>
            </div>
          </div>
          
          <!-- Support Section -->
          <div class="px-4 py-4">
            <h5 class="text-sm font-medium text-gray-900 mb-3">Soporte</h5>
            <div class="space-y-2">
              <button
                @click="navigateTo('/help')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <QuestionMarkCircleIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Centro de Ayuda</span>
                </div>
                <ChevronRightIcon class="h-4 w-4 text-gray-400" />
              </button>
              
              <button
                @click="contactSupport"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <ChatBubbleLeftRightIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Contactar Soporte</span>
                </div>
                <ChevronRightIcon class="h-4 w-4 text-gray-400" />
              </button>
              
              <button
                @click="navigateTo('/about')"
                class="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <InformationCircleIcon class="h-5 w-5 text-gray-400" />
                  <span class="text-sm text-gray-700">Acerca de</span>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-500">v2.1.0</span>
                  <ChevronRightIcon class="h-4 w-4 text-gray-400" />
                </div>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Footer Actions -->
        <div class="bg-gray-50 px-4 py-3">
          <button
            @click="logout"
            class="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <ArrowRightOnRectangleIcon class="h-4 w-4 mr-2" />
            Cerrar Sesión
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import {
  XMarkIcon,
  CameraIcon,
  UserIcon,
  ShieldCheckIcon,
  BellIcon,
  MoonIcon,
  SpeakerWaveIcon,
  LanguageIcon,
  BuildingOfficeIcon,
  UserGroupIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  InformationCircleIcon,
  ArrowRightOnRectangleIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'
import ToggleSwitch from '../ui/ToggleSwitch.vue'

const emit = defineEmits(['close'])
const router = useRouter()

// Reactive data
const user = reactive({
  name: 'Juan Pérez',
  email: 'juan@empresa.com',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
  status: 'online',
  organization: 'Mi Empresa S.A.',
  role: 'Administrador',
  teamMembers: 12
})

const preferences = reactive({
  darkMode: false,
  sounds: true,
  language: 'Español'
})

const notificationSettings = reactive({
  enabled: true
})

// Methods
const getStatusText = (status) => {
  switch (status) {
    case 'online':
      return 'En línea'
    case 'away':
      return 'Ausente'
    case 'busy':
      return 'Ocupado'
    default:
      return 'Desconectado'
  }
}

const changeAvatar = () => {
  // Simulate file picker
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        user.avatar = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
  input.click()
}

const navigateTo = (path) => {
  emit('close')
  router.push(path)
}

const contactSupport = () => {
  // Open support chat or email
  window.open('mailto:support@versaai.com?subject=Soporte Móvil')
}

const logout = async () => {
  try {
    // Simulate logout API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Clear local storage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
    
    // Redirect to login
    router.push('/login')
    emit('close')
  } catch (error) {
    console.error('Error during logout:', error)
  }
}
</script>

<style scoped>
/* Custom scrollbar for mobile */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>