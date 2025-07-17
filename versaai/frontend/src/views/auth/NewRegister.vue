<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-emerald-900 dark:to-teal-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-32 w-80 h-80 bg-gradient-to-br from-emerald-400/20 to-teal-600/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-32 w-80 h-80 bg-gradient-to-tr from-cyan-400/20 to-blue-600/20 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-md w-full space-y-8">
      <!-- Logo y Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
        <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
          Únete a VersaAI
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Crea tu cuenta y comienza a construir chatbots inteligentes
        </p>
      </div>

      <!-- Formulario -->
      <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20 dark:border-gray-700/20 p-8">
        <form class="space-y-6" @submit.prevent="handleRegister">
          <!-- Nombre completo -->
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre completo
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="full_name"
                v-model="form.full_name"
                name="full_name"
                type="text"
                autocomplete="name"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200"
                placeholder="Tu nombre completo"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Correo electrónico
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <EnvelopeIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200"
                placeholder="tu@email.com"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Organización -->
          <div>
            <label for="organization_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre de la organización
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <BuildingOfficeIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="organization_name"
                v-model="form.organization_name"
                name="organization_name"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200"
                placeholder="Mi Empresa S.A."
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockClosedIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                v-model="form.password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200"
                placeholder="Mínimo 8 caracteres"
                :disabled="loading"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showPassword = !showPassword"
              >
                <EyeIcon v-if="!showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
              </button>
            </div>
            <!-- Password strength indicator -->
            <div class="mt-2">
              <div class="flex space-x-1">
                <div 
                  v-for="i in 4" 
                  :key="i"
                  class="h-1 flex-1 rounded-full transition-colors duration-200"
                  :class="getPasswordStrengthColor(i)"
                ></div>
              </div>
              <p class="text-xs mt-1" :class="passwordStrengthTextColor">
                {{ passwordStrengthText }}
              </p>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Confirmar contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockClosedIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="confirm_password"
                v-model="form.confirm_password"
                name="confirm_password"
                :type="showConfirmPassword ? 'text' : 'password'"
                autocomplete="new-password"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-200"
                placeholder="Repite tu contraseña"
                :disabled="loading"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <EyeIcon v-if="!showConfirmPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
                <EyeSlashIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
              </button>
            </div>
            <!-- Password match indicator -->
            <div v-if="form.confirm_password" class="mt-2">
              <p class="text-xs" :class="passwordsMatch ? 'text-emerald-600' : 'text-red-600'">
                <CheckIcon v-if="passwordsMatch" class="inline h-3 w-3 mr-1" />
                <XMarkIcon v-else class="inline h-3 w-3 mr-1" />
                {{ passwordsMatch ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden' }}
              </p>
            </div>
          </div>

          <!-- Terms and conditions -->
          <div class="flex items-start">
            <div class="flex items-center h-5">
              <input
                id="accept-terms"
                v-model="form.acceptTerms"
                name="accept-terms"
                type="checkbox"
                required
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                :disabled="loading"
              />
            </div>
            <div class="ml-3 text-sm">
              <label for="accept-terms" class="text-gray-700 dark:text-gray-300">
                Acepto los
                <a href="#" class="text-emerald-600 hover:text-emerald-500 dark:text-emerald-400 font-medium">
                  términos y condiciones
                </a>
                y la
                <a href="#" class="text-emerald-600 hover:text-emerald-500 dark:text-emerald-400 font-medium">
                  política de privacidad
                </a>
              </label>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
              :disabled="loading || !isFormValid"
            >
              <span v-if="loading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creando cuenta...
              </span>
              <span v-else class="flex items-center">
                <UserPlusIcon class="h-5 w-5 mr-2" />
                Crear cuenta
              </span>
            </button>
          </div>
        </form>

        <!-- Divider -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300 dark:border-gray-600" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white/80 dark:bg-gray-800/80 text-gray-500 dark:text-gray-400">
                ¿Ya tienes una cuenta?
              </span>
            </div>
          </div>
        </div>

        <!-- Login Link -->
        <div class="mt-6">
          <router-link
            to="/auth/new-login"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 dark:border-gray-600 rounded-xl text-sm font-medium text-gray-700 dark:text-gray-300 bg-white/50 dark:bg-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5 mr-2" />
            Iniciar sesión
          </router-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Al crear una cuenta, aceptas nuestros
          <a href="#" class="text-emerald-600 hover:text-emerald-500 dark:text-emerald-400">
            Términos de Servicio
          </a>
          y
          <a href="#" class="text-emerald-600 hover:text-emerald-500 dark:text-emerald-400">
            Política de Privacidad
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  LockClosedIcon, 
  EnvelopeIcon, 
  EyeIcon, 
  EyeSlashIcon,
  UserIcon,
  UserPlusIcon,
  BuildingOfficeIcon,
  ArrowRightOnRectangleIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  confirm_password: '',
  organization_name: '',
  acceptTerms: false
})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.password
  let strength = 0
  
  if (password.length >= 8) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  return Math.min(strength, 4)
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (form.password.length === 0) return ''
  if (strength <= 1) return 'Muy débil'
  if (strength === 2) return 'Débil'
  if (strength === 3) return 'Buena'
  return 'Muy fuerte'
})

const passwordStrengthTextColor = computed(() => {
  const strength = passwordStrength.value
  if (form.password.length === 0) return 'text-gray-500'
  if (strength <= 1) return 'text-red-600'
  if (strength === 2) return 'text-orange-600'
  if (strength === 3) return 'text-yellow-600'
  return 'text-emerald-600'
})

const getPasswordStrengthColor = (index) => {
  const strength = passwordStrength.value
  if (form.password.length === 0) return 'bg-gray-200'
  if (index <= strength) {
    if (strength <= 1) return 'bg-red-500'
    if (strength === 2) return 'bg-orange-500'
    if (strength === 3) return 'bg-yellow-500'
    return 'bg-emerald-500'
  }
  return 'bg-gray-200'
}

const passwordsMatch = computed(() => {
  return form.password && form.confirm_password && form.password === form.confirm_password
})

const isFormValid = computed(() => {
  return (
    form.full_name.trim() &&
    form.email.trim() &&
    form.password.length >= 8 &&
    passwordsMatch.value &&
    form.organization_name.trim() &&
    form.acceptTerms
  )
})

const handleRegister = async () => {
  if (loading.value || !isFormValid.value) return
  
  if (!passwordsMatch.value) {
    toast.error('Las contraseñas no coinciden', {
      timeout: 5000,
      position: 'top-right'
    })
    return
  }
  
  loading.value = true
  
  try {
    await authStore.register({
      full_name: form.full_name,
      email: form.email,
      password: form.password,
      organization_name: form.organization_name
    })
    
    toast.success('¡Cuenta creada exitosamente! Bienvenido a VersaAI 🎉', {
      timeout: 4000,
      position: 'top-right'
    })
    
    await router.push('/dashboard')
  } catch (error) {
    console.error('Registration error:', error)
    const errorMessage = error.response?.data?.detail || 'Error al crear la cuenta. Por favor, inténtalo de nuevo.'
    toast.error(errorMessage, {
      timeout: 5000,
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Animaciones personalizadas */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Efectos de glassmorphism */
.backdrop-blur-xl {
  backdrop-filter: blur(16px);
}

/* Transiciones suaves */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>