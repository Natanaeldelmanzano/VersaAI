<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="md:flex md:items-center md:justify-between">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Mi Perfil
        </h2>
        <p class="mt-1 text-sm text-gray-500">
          Gestiona tu información personal y configuración de cuenta
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile Information -->
      <div class="lg:col-span-2">
        <div class="bg-white shadow rounded-lg">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Información Personal</h3>
          </div>
          
          <form @submit.prevent="updateProfile" class="p-6 space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label for="full_name" class="block text-sm font-medium text-gray-700">
                  Nombre completo
                </label>
                <input
                  id="full_name"
                  v-model="profileForm.full_name"
                  type="text"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  :disabled="profileLoading"
                />
              </div>
              
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  id="email"
                  v-model="profileForm.email"
                  type="email"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  :disabled="profileLoading"
                />
              </div>
            </div>
            
            <div>
              <label for="bio" class="block text-sm font-medium text-gray-700">
                Biografía
              </label>
              <textarea
                id="bio"
                v-model="profileForm.bio"
                rows="3"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Cuéntanos un poco sobre ti..."
                :disabled="profileLoading"
              ></textarea>
            </div>
            
            <div class="flex justify-end">
              <button
                type="submit"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="profileLoading"
              >
                <span v-if="profileLoading" class="flex items-center">
                  <div class="spinner mr-2"></div>
                  Guardando...
                </span>
                <span v-else>Guardar Cambios</span>
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Profile Picture & Stats -->
      <div class="space-y-6">
        <!-- Profile Picture -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Foto de Perfil</h3>
          
          <div class="flex flex-col items-center">
            <div class="h-24 w-24 rounded-full bg-primary-100 flex items-center justify-center mb-4">
              <UserIcon class="h-12 w-12 text-primary-600" />
            </div>
            
            <button
              type="button"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <CameraIcon class="-ml-0.5 mr-2 h-4 w-4" />
              Cambiar Foto
            </button>
          </div>
        </div>
        
        <!-- Account Stats -->
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Estadísticas de Cuenta</h3>
          
          <div class="space-y-4">
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Miembro desde</span>
              <span class="text-sm font-medium text-gray-900">
                {{ formatDate(authStore.user?.created_at) }}
              </span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Chatbots creados</span>
              <span class="text-sm font-medium text-gray-900">{{ userStats.chatbots_count }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Mensajes procesados</span>
              <span class="text-sm font-medium text-gray-900">{{ userStats.messages_count }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="text-sm text-gray-500">Plan actual</span>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                {{ authStore.user?.subscription_plan || 'Free' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Security Section -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Seguridad</h3>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Change Password -->
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Cambiar Contraseña</h4>
            
            <form @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label for="current_password" class="block text-sm font-medium text-gray-700">
                  Contraseña actual
                </label>
                <input
                  id="current_password"
                  v-model="passwordForm.current_password"
                  type="password"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  :disabled="passwordLoading"
                />
              </div>
              
              <div>
                <label for="new_password" class="block text-sm font-medium text-gray-700">
                  Nueva contraseña
                </label>
                <input
                  id="new_password"
                  v-model="passwordForm.new_password"
                  type="password"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  :disabled="passwordLoading"
                />
              </div>
              
              <div>
                <label for="confirm_password" class="block text-sm font-medium text-gray-700">
                  Confirmar nueva contraseña
                </label>
                <input
                  id="confirm_password"
                  v-model="passwordForm.confirm_password"
                  type="password"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  :disabled="passwordLoading"
                />
              </div>
              
              <button
                type="submit"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="passwordLoading || !isPasswordFormValid"
              >
                <span v-if="passwordLoading" class="flex items-center">
                  <div class="spinner mr-2"></div>
                  Cambiando...
                </span>
                <span v-else>Cambiar Contraseña</span>
              </button>
            </form>
          </div>
          
          <!-- Two-Factor Authentication -->
          <div>
            <h4 class="text-base font-medium text-gray-900 mb-4">Autenticación de Dos Factores</h4>
            
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <p class="text-sm font-medium text-gray-900">Autenticación SMS</p>
                  <p class="text-sm text-gray-500">Recibe códigos por mensaje de texto</p>
                </div>
                <button
                  type="button"
                  class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 bg-gray-200"
                  role="switch"
                  aria-checked="false"
                >
                  <span class="translate-x-0 pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"></span>
                </button>
              </div>
              
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <p class="text-sm font-medium text-gray-900">App Autenticadora</p>
                  <p class="text-sm text-gray-500">Usa Google Authenticator o similar</p>
                </div>
                <button
                  type="button"
                  class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 bg-gray-200"
                  role="switch"
                  aria-checked="false"
                >
                  <span class="translate-x-0 pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200"></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { UserIcon, CameraIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/api'

const authStore = useAuthStore()
const toast = useToast()

const profileLoading = ref(false)
const passwordLoading = ref(false)
const userStats = ref({
  chatbots_count: 0,
  messages_count: 0
})

const profileForm = reactive({
  full_name: '',
  email: '',
  bio: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const isPasswordFormValid = computed(() => {
  return (
    passwordForm.current_password &&
    passwordForm.new_password.length >= 8 &&
    passwordForm.new_password === passwordForm.confirm_password
  )
})

const formatDate = (date) => {
  if (!date) return 'N/A'
  return format(new Date(date), 'dd MMMM yyyy', { locale: es })
}

const updateProfile = async () => {
  profileLoading.value = true
  
  try {
    await authStore.updateProfile({
      full_name: profileForm.full_name,
      email: profileForm.email,
      bio: profileForm.bio
    })
    
    toast.success('Perfil actualizado exitosamente')
  } catch (error) {
    console.error('Error updating profile:', error)
    toast.error(error.response?.data?.detail || 'Error al actualizar el perfil')
  } finally {
    profileLoading.value = false
  }
}

const changePassword = async () => {
  if (!isPasswordFormValid.value) return
  
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.error('Las contraseñas no coinciden')
    return
  }
  
  passwordLoading.value = true
  
  try {
    await authStore.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })
    
    // Reset form
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    
    toast.success('Contraseña cambiada exitosamente')
  } catch (error) {
    console.error('Error changing password:', error)
    toast.error(error.response?.data?.detail || 'Error al cambiar la contraseña')
  } finally {
    passwordLoading.value = false
  }
}

const loadUserStats = async () => {
  try {
    const response = await api.get('/users/me/stats')
    userStats.value = response.data
  } catch (error) {
    console.error('Error loading user stats:', error)
  }
}

onMounted(() => {
  // Initialize form with user data
  if (authStore.user) {
    profileForm.full_name = authStore.user.full_name || ''
    profileForm.email = authStore.user.email || ''
    profileForm.bio = authStore.user.bio || ''
  }
  
  loadUserStats()
})
</script>