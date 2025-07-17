<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Sistema de Autenticación TypeScript
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Ejemplo de implementación con Zod, Pinia y composables
        </p>
      </div>

      <!-- Estado de autenticación -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
          Estado Actual
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Usuario autenticado -->
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 dark:text-white mb-2">
              Autenticación
            </h3>
            <div class="flex items-center space-x-2">
              <div :class="[
                'w-3 h-3 rounded-full',
                isAuthenticated ? 'bg-green-500' : 'bg-red-500'
              ]"></div>
              <span class="text-sm text-gray-600 dark:text-gray-300">
                {{ isAuthenticated ? 'Autenticado' : 'No autenticado' }}
              </span>
            </div>
            <div v-if="user" class="mt-2">
              <p class="text-sm text-gray-600 dark:text-gray-300">
                <strong>Usuario:</strong> {{ user.name }}
              </p>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                <strong>Email:</strong> {{ user.email }}
              </p>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                <strong>Rol:</strong> {{ userRole }}
              </p>
            </div>
          </div>

          <!-- Estado de carga -->
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 dark:text-white mb-2">
              Estado de Carga
            </h3>
            <div class="flex items-center space-x-2">
              <LoadingSpinner v-if="isLoading" size="sm" />
              <div v-else :class="[
                'w-3 h-3 rounded-full bg-gray-400'
              ]"></div>
              <span class="text-sm text-gray-600 dark:text-gray-300">
                {{ isLoading ? 'Cargando...' : 'Inactivo' }}
              </span>
            </div>
          </div>

          <!-- Permisos -->
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 dark:text-white mb-2">
              Permisos
            </h3>
            <div class="space-y-1">
              <div class="flex items-center space-x-2">
                <div :class="[
                  'w-2 h-2 rounded-full',
                  isAdmin ? 'bg-purple-500' : 'bg-gray-400'
                ]"></div>
                <span class="text-xs text-gray-600 dark:text-gray-300">
                  Admin: {{ isAdmin ? 'Sí' : 'No' }}
                </span>
              </div>
              <div class="flex items-center space-x-2">
                <div :class="[
                  'w-2 h-2 rounded-full',
                  isModerator ? 'bg-blue-500' : 'bg-gray-400'
                ]"></div>
                <span class="text-xs text-gray-600 dark:text-gray-300">
                  Moderador: {{ isModerator ? 'Sí' : 'No' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Formularios de ejemplo -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Login Form -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Formulario de Login
          </h3>
          
          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Email
              </label>
              <input
                v-model="loginForm.email"
                type="email"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="tu@email.com"
                :disabled="isLoading"
              />
              <p v-if="loginErrors.email" class="mt-1 text-sm text-red-600">
                {{ loginErrors.email }}
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Contraseña
              </label>
              <input
                v-model="loginForm.password"
                type="password"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="Tu contraseña"
                :disabled="isLoading"
              />
              <p v-if="loginErrors.password" class="mt-1 text-sm text-red-600">
                {{ loginErrors.password }}
              </p>
            </div>
            
            <div class="flex items-center">
              <input
                v-model="loginForm.remember"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                :disabled="isLoading"
              />
              <label class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Recordarme
              </label>
            </div>
            
            <button
              type="submit"
              :disabled="isLoading || !isLoginFormValid"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
              {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
            </button>
          </form>
        </div>

        <!-- Validation Example -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Ejemplo de Validación con Zod
          </h3>
          
          <form @submit.prevent="handleValidationTest" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Nombre (mín. 2 caracteres)
              </label>
              <input
                v-model="validationForm.name"
                type="text"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="Tu nombre"
                @input="validateField('name')"
              />
              <p v-if="validationErrors.name" class="mt-1 text-sm text-red-600">
                {{ validationErrors.name }}
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Email
              </label>
              <input
                v-model="validationForm.email"
                type="email"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="tu@email.com"
                @input="validateField('email')"
              />
              <p v-if="validationErrors.email" class="mt-1 text-sm text-red-600">
                {{ validationErrors.email }}
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Contraseña (mín. 8 caracteres, mayúscula, minúscula, número)
              </label>
              <input
                v-model="validationForm.password"
                type="password"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                placeholder="Tu contraseña"
                @input="validateField('password')"
              />
              <p v-if="validationErrors.password" class="mt-1 text-sm text-red-600">
                {{ validationErrors.password }}
              </p>
            </div>
            
            <button
              type="submit"
              :disabled="!isValidationFormValid"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Validar Formulario
            </button>
          </form>
          
          <!-- Resultado de validación -->
          <div v-if="validationResult" class="mt-4 p-3 rounded-md" :class="[
            validationResult.success ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200' : 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200'
          ]">
            <h4 class="font-medium mb-2">
              {{ validationResult.success ? '✅ Validación exitosa' : '❌ Errores de validación' }}
            </h4>
            <pre class="text-xs overflow-auto">{{ JSON.stringify(validationResult, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <!-- Acciones de autenticación -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 mt-8">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Acciones de Autenticación
        </h3>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button
            @click="checkAuthStatus"
            :disabled="isLoading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 text-sm"
          >
            Verificar Auth
          </button>
          
          <button
            @click="refreshAuthToken"
            :disabled="isLoading || !isAuthenticated"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 text-sm"
          >
            Refrescar Token
          </button>
          
          <button
            @click="simulateLogout"
            :disabled="isLoading || !isAuthenticated"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 text-sm"
          >
            Cerrar Sesión
          </button>
          
          <button
            @click="clearErrors"
            class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm"
          >
            Limpiar Errores
          </button>
        </div>
      </div>

      <!-- Debug Info -->
      <div v-if="showDebugInfo" class="bg-gray-100 dark:bg-gray-800 rounded-lg p-6 mt-8">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Información de Debug
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Store State</h4>
            <pre class="text-xs bg-white dark:bg-gray-900 p-3 rounded overflow-auto">{{ JSON.stringify({
              user: user,
              isAuthenticated: isAuthenticated,
              isLoading: isLoading,
              userRole: userRole,
              lastActivity: lastActivity
            }, null, 2) }}</pre>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Validation Schemas</h4>
            <pre class="text-xs bg-white dark:bg-gray-900 p-3 rounded overflow-auto">{{ JSON.stringify({
              loginSchema: 'LoginData schema loaded',
              registerSchema: 'RegisterData schema loaded',
              validationUtils: 'validateData function available'
            }, null, 2) }}</pre>
          </div>
        </div>
      </div>
      
      <!-- Toggle Debug -->
      <div class="text-center mt-6">
        <button
          @click="showDebugInfo = !showDebugInfo"
          class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
        >
          {{ showDebugInfo ? 'Ocultar' : 'Mostrar' }} información de debug
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { loginSchema, registerSchema, validateData, type LoginData } from '@/utils/validation'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useToast } from 'vue-toastification'

// Composables
const auth = useAuth()
const toast = useToast()

// Estado reactivo
const showDebugInfo = ref(false)
const validationResult = ref<any>(null)

// Formulario de login
const loginForm = ref<LoginData>({
  email: 'admin@versaai.com',
  password: 'password123',
  remember: false
})

const loginErrors = ref<Record<string, string>>({})

// Formulario de validación
const validationForm = ref({
  name: '',
  email: '',
  password: ''
})

const validationErrors = ref<Record<string, string>>({})

// Computed properties del auth store
const {
  user,
  isAuthenticated,
  isLoading,
  userRole,
  isAdmin,
  isModerator,
  lastActivity
} = auth

// Validación de formularios
const isLoginFormValid = computed(() => {
  const validation = validateData(loginSchema, loginForm.value)
  return validation.success && loginForm.value.email && loginForm.value.password
})

const isValidationFormValid = computed(() => {
  return validationForm.value.name.length >= 2 &&
         validationForm.value.email.includes('@') &&
         validationForm.value.password.length >= 8
})

// Métodos
const handleLogin = async (): Promise<void> => {
  loginErrors.value = {}
  
  // Validar formulario
  const validation = validateData(loginSchema, loginForm.value)
  if (!validation.success) {
    validation.errors.forEach(error => {
      const [field, message] = error.split(': ')
      if (field && message) {
        loginErrors.value[field] = message
      }
    })
    toast.error('Por favor corrige los errores en el formulario')
    return
  }
  
  // Intentar login
  const success = await auth.login(loginForm.value)
  if (success) {
    toast.success('Login exitoso (simulado)')
  }
}

const handleValidationTest = (): void => {
  // Simular validación con registerSchema
  const testData = {
    name: validationForm.value.name,
    email: validationForm.value.email,
    password: validationForm.value.password,
    password_confirmation: validationForm.value.password,
    terms_accepted: true
  }
  
  const validation = validateData(registerSchema, testData)
  validationResult.value = validation
  
  if (validation.success) {
    toast.success('Validación exitosa')
  } else {
    toast.error('Errores de validación encontrados')
  }
}

const validateField = (field: string): void => {
  // Validación en tiempo real
  const fieldValidations = {
    name: () => {
      if (validationForm.value.name.length < 2) {
        validationErrors.value.name = 'El nombre debe tener al menos 2 caracteres'
      } else {
        delete validationErrors.value.name
      }
    },
    email: () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(validationForm.value.email)) {
        validationErrors.value.email = 'Formato de email inválido'
      } else {
        delete validationErrors.value.email
      }
    },
    password: () => {
      const password = validationForm.value.password
      if (password.length < 8) {
        validationErrors.value.password = 'Mínimo 8 caracteres'
      } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
        validationErrors.value.password = 'Debe contener mayúscula, minúscula y número'
      } else {
        delete validationErrors.value.password
      }
    }
  }
  
  if (fieldValidations[field as keyof typeof fieldValidations]) {
    fieldValidations[field as keyof typeof fieldValidations]()
  }
}

const checkAuthStatus = async (): Promise<void> => {
  const isAuth = await auth.checkAuth()
  toast.info(`Estado de autenticación: ${isAuth ? 'Autenticado' : 'No autenticado'}`)
}

const refreshAuthToken = async (): Promise<void> => {
  const success = await auth.refreshToken()
  if (success) {
    toast.success('Token refrescado exitosamente')
  } else {
    toast.error('Error al refrescar token')
  }
}

const simulateLogout = async (): Promise<void> => {
  await auth.logout()
}

const clearErrors = (): void => {
  loginErrors.value = {}
  validationErrors.value = {}
  validationResult.value = null
  auth.clearError()
  toast.success('Errores limpiados')
}

// Lifecycle
onMounted(() => {
  console.log('🔧 AuthExample component mounted')
  console.log('📊 Auth state:', {
    isAuthenticated: isAuthenticated.value,
    user: user.value,
    isLoading: isLoading.value
  })
})
</script>

<style scoped>
/* Estilos específicos del componente */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mejoras visuales */
pre {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 11px;
  line-height: 1.4;
}

/* Animaciones suaves */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

input {
  transition: all 0.2s ease;
}

input:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}
</style>