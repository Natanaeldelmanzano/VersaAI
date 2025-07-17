<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-indigo-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-32 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-purple-600/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-32 w-80 h-80 bg-gradient-to-tr from-indigo-400/20 to-pink-600/20 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-md w-full space-y-8">
      <!-- Logo y Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
          <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h2 class="mt-6 text-3xl font-bold text-gray-900 dark:text-white">
          Bienvenido de vuelta
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Inicia sesión en tu cuenta de VersaAI
        </p>
      </div>

      <!-- Formulario -->
      <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20 dark:border-gray-700/20 p-8">
        <form class="space-y-6" @submit.prevent="handleLogin">
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
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                placeholder="tu@email.com"
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
                autocomplete="current-password"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white/50 dark:bg-gray-700/50 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                placeholder="••••••••"
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
          </div>

          <!-- Remember me y Forgot password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="form.rememberMe"
                name="remember-me"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                :disabled="loading"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Recordarme
              </label>
            </div>

            <div class="text-sm">
              <router-link 
                to="/auth/forgot-password" 
                class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
              >
                ¿Olvidaste tu contraseña?
              </router-link>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
              :disabled="loading || !isFormValid"
            >
              <span v-if="loading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Iniciando sesión...
              </span>
              <span v-else class="flex items-center">
                <ArrowRightOnRectangleIcon class="h-5 w-5 mr-2" />
                Iniciar sesión
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
                ¿No tienes una cuenta?
              </span>
            </div>
          </div>
        </div>

        <!-- Quick Login Buttons (Development) -->
        <div class="mt-6 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400">Login rápido (testing):</span>
            <button
              @click="showDebug = !showDebug"
              class="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 flex items-center"
            >
              <BugAntIcon class="h-4 w-4 mr-1" />
              Debug
            </button>
          </div>
          
          <div class="grid grid-cols-2 gap-2">
            <button
              @click="quickLogin({ email: 'admin@versaai.com', password: 'admin123' })"
              class="flex items-center justify-center py-2 px-3 text-xs font-medium text-blue-600 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
              :disabled="loading"
            >
              <UserIcon class="h-4 w-4 mr-1" />
              Admin
            </button>
            
            <button
              @click="quickLogin({ email: 'user@versaai.com', password: 'user123' })"
              class="flex items-center justify-center py-2 px-3 text-xs font-medium text-green-600 bg-green-50 dark:bg-green-900/20 dark:text-green-400 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors"
              :disabled="loading"
            >
              <UserIcon class="h-4 w-4 mr-1" />
              Usuario
            </button>
          </div>
        </div>

        <!-- Debug Information -->
        <div v-if="showDebug" class="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Debug Info:</h4>
          <div class="text-xs text-gray-600 dark:text-gray-400 space-y-1">
            <div><strong>Loading:</strong> {{ isLoading }}</div>
            <div><strong>Form Valid:</strong> {{ isFormValid }}</div>
            <div><strong>Has Error:</strong> {{ hasError }}</div>
            <div><strong>Authenticated:</strong> {{ isAuthenticated }}</div>
            <div v-if="authStore.error"><strong>Error:</strong> {{ authStore.error }}</div>
            <div v-if="debugInfo.timestamp"><strong>Last Action:</strong> {{ debugInfo.timestamp }}</div>
            <div v-if="debugInfo.result"><strong>Result:</strong> {{ debugInfo.result }}</div>
          </div>
        </div>

        <!-- Register Link -->
        <div class="mt-6">
          <router-link
            to="/auth/new-register"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 dark:border-gray-600 rounded-xl text-sm font-medium text-gray-700 dark:text-gray-300 bg-white/50 dark:bg-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            <UserPlusIcon class="h-5 w-5 mr-2" />
            Crear cuenta nueva
          </router-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Al iniciar sesión, aceptas nuestros
          <a href="#" class="text-blue-600 hover:text-blue-500 dark:text-blue-400">
            Términos de Servicio
          </a>
          y
          <a href="#" class="text-blue-600 hover:text-blue-500 dark:text-blue-400">
            Política de Privacidad
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  LockClosedIcon, 
  EnvelopeIcon, 
  EyeIcon, 
  EyeSlashIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  BugAntIcon,
  UserIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

// Estados reactivos
const loading = ref(false)
const showPassword = ref(false)
const showDebug = ref(false)
const debugInfo = ref({})

// Formulario
const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

// Computed properties
const isFormValid = computed(() => {
  return form.email.trim() && form.password.trim()
})

const isLoading = computed(() => loading.value)
const hasError = computed(() => authStore.error)
const isAuthenticated = computed(() => authStore.isAuthenticated)

// Función principal de login
const handleLogin = async () => {
  console.log('🔐 [NewLogin] Iniciando proceso de login...')
  
  if (loading.value) {
    console.warn('🔐 [NewLogin] Login ya en progreso, ignorando...')
    return
  }
  
  if (!isFormValid.value) {
    console.error('🔐 [NewLogin] Formulario inválido:', {
      email: form.email,
      password: form.password ? '***' : 'vacío',
      emailValid: !!form.email.trim(),
      passwordValid: !!form.password.trim()
    })
    toast.error('Por favor completa todos los campos')
    return
  }
  
  // Validaciones básicas
  if (!form.email.includes('@')) {
    console.error('🔐 [NewLogin] Email inválido:', form.email)
    toast.error('Por favor ingresa un email válido')
    return
  }
  
  if (form.password.length < 3) {
    console.error('🔐 [NewLogin] Contraseña muy corta')
    toast.error('La contraseña debe tener al menos 3 caracteres')
    return
  }
  
  loading.value = true
  
  try {
    console.log('🔐 [NewLogin] Enviando credenciales:', {
      email: form.email,
      password: '***',
      rememberMe: form.rememberMe
    })
    
    // Actualizar debug info
    debugInfo.value = {
      timestamp: new Date().toISOString(),
      action: 'login_attempt',
      email: form.email,
      rememberMe: form.rememberMe
    }
    
    const result = await authStore.login({
      email: form.email,
      password: form.password,
      remember_me: form.rememberMe
    })
    
    console.log('🔐 [NewLogin] Resultado del login:', result)
    
    if (result && result.success) {
      console.log('✅ [NewLogin] Login exitoso, redirigiendo...')
      
      toast.success('¡Bienvenido de vuelta! 🎉', {
        timeout: 3000,
        position: 'top-right'
      })
      
      // Actualizar debug info
      debugInfo.value = {
        ...debugInfo.value,
        result: 'success',
        user: authStore.user
      }
      
      // Redireccionar
      const redirectTo = router.currentRoute.value.query.redirect || '/dashboard'
      console.log('🔐 [NewLogin] Redirigiendo a:', redirectTo)
      await router.push(redirectTo)
    } else {
      throw new Error(result?.error || 'Error de autenticación desconocido')
    }
  } catch (error) {
    console.error('❌ [NewLogin] Error en login:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      stack: error.stack
    })
    
    // Actualizar debug info
    debugInfo.value = {
      ...debugInfo.value,
      result: 'error',
      error: {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data
      }
    }
    
    // Determinar mensaje de error
    let errorMessage = 'Error al iniciar sesión. Por favor, verifica tus credenciales.'
    
    if (error.response?.status === 401) {
      errorMessage = 'Credenciales incorrectas. Verifica tu email y contraseña.'
    } else if (error.response?.status === 422) {
      errorMessage = 'Datos inválidos. Verifica el formato de tu email.'
    } else if (error.response?.status >= 500) {
      errorMessage = 'Error del servidor. Intenta nuevamente en unos momentos.'
    } else if (error.message.includes('Network Error')) {
      errorMessage = 'Error de conexión. Verifica tu conexión a internet.'
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    }
    
    toast.error(errorMessage, {
      timeout: 5000,
      position: 'top-right'
    })
  } finally {
    loading.value = false
    console.log('🔐 [NewLogin] Proceso de login finalizado')
  }
}

// Función para login rápido (testing)
const quickLogin = (credentials) => {
  console.log('🚀 [NewLogin] Login rápido:', credentials.email)
  form.email = credentials.email
  form.password = credentials.password
  form.rememberMe = credentials.rememberMe || false
  handleLogin()
}

// Lifecycle
onMounted(() => {
  console.log('🔐 [NewLogin] Componente montado')
  console.log('🔐 [NewLogin] Estado inicial del auth store:', {
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user,
    token: authStore.token ? '***' : null
  })
  
  // Si ya está autenticado, redirigir
  if (authStore.isAuthenticated) {
    console.log('🔐 [NewLogin] Usuario ya autenticado, redirigiendo...')
    router.push('/dashboard')
  }
})
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