<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Restablecer contraseña
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Ingresa tu nueva contraseña
        </p>
      </div>
      
      <div v-if="passwordReset" class="rounded-md bg-green-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <CheckCircleIcon class="h-5 w-5 text-green-400" aria-hidden="true" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">
              Contraseña restablecida
            </h3>
            <div class="mt-2 text-sm text-green-700">
              <p>
                Tu contraseña ha sido restablecida exitosamente.
                Ya puedes iniciar sesión con tu nueva contraseña.
              </p>
            </div>
            <div class="mt-4">
              <div class="-mx-2 -my-1.5 flex">
                <router-link
                  to="/login"
                  class="bg-green-50 px-2 py-1.5 rounded-md text-sm font-medium text-green-800 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-green-600"
                >
                  Ir al inicio de sesión
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="invalidToken" class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <XCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Enlace inválido o expirado
            </h3>
            <div class="mt-2 text-sm text-red-700">
              <p>
                El enlace de restablecimiento es inválido o ha expirado.
                Por favor, solicita un nuevo enlace.
              </p>
            </div>
            <div class="mt-4">
              <div class="-mx-2 -my-1.5 flex">
                <router-link
                  to="/forgot-password"
                  class="bg-red-50 px-2 py-1.5 rounded-md text-sm font-medium text-red-800 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-red-50 focus:ring-red-600"
                >
                  Solicitar nuevo enlace
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleResetPassword">
        <div class="space-y-4">
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Nueva contraseña
            </label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Mínimo 8 caracteres"
              :disabled="loading"
            />
          </div>
          
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700">
              Confirmar nueva contraseña
            </label>
            <input
              id="confirm_password"
              v-model="form.confirm_password"
              name="confirm_password"
              type="password"
              autocomplete="new-password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Repite tu nueva contraseña"
              :disabled="loading"
            />
          </div>
        </div>

        <div v-if="form.password && form.confirm_password && form.password !== form.confirm_password" class="text-sm text-red-600">
          Las contraseñas no coinciden
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            :disabled="loading || !isFormValid"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <LockClosedIcon class="h-5 w-5 text-primary-500 group-hover:text-primary-400" aria-hidden="true" />
            </span>
            <span v-if="loading" class="flex items-center">
              <div class="spinner mr-2"></div>
              Restableciendo...
            </span>
            <span v-else>Restablecer contraseña</span>
          </button>
        </div>
        
        <div class="text-center">
          <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
            ← Volver al inicio de sesión
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { LockClosedIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/vue/20/solid'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

const loading = ref(false)
const passwordReset = ref(false)
const invalidToken = ref(false)
const form = reactive({
  password: '',
  confirm_password: ''
})

const isFormValid = computed(() => {
  return (
    form.password.length >= 8 &&
    form.password === form.confirm_password
  )
})

const handleResetPassword = async () => {
  if (loading.value || !isFormValid.value) return
  
  if (form.password !== form.confirm_password) {
    toast.error('Las contraseñas no coinciden')
    return
  }
  
  loading.value = true
  
  try {
    const token = route.query.token
    if (!token) {
      throw new Error('Token no encontrado')
    }
    
    await authStore.resetPassword({
      token: token,
      new_password: form.password
    })
    
    passwordReset.value = true
    toast.success('Contraseña restablecida exitosamente')
  } catch (error) {
    console.error('Reset password error:', error)
    if (error.response?.status === 400 || error.response?.status === 404) {
      invalidToken.value = true
    } else {
      toast.error(error.response?.data?.detail || 'Error al restablecer la contraseña')
    }
  } finally {
    loading.value = false
  }
}

// Validate token on mount
onMounted(() => {
  const token = route.query.token
  if (!token) {
    invalidToken.value = true
  }
})
</script>