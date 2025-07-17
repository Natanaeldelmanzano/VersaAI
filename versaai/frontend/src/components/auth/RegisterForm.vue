<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900">
          <svg class="h-6 w-6 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
          Crear Cuenta
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Únete a VersaAI y comienza a crear chatbots inteligentes
        </p>
      </div>

      <!-- Formulario -->
      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div class="space-y-4">
          <!-- Nombre -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Nombre completo
            </label>
            <div class="mt-1 relative">
              <input
                id="name"
                v-model="form.name"
                type="text"
                autocomplete="name"
                :class="[
                  'appearance-none relative block w-full px-3 py-2 border rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm transition-colors',
                  errors.name ? 'border-red-300 dark:border-red-600' : 'border-gray-300 dark:border-gray-600'
                ]"
                placeholder="Tu nombre completo"
                :disabled="isLoading"
                @input="clearError('name')"
              />
              <div v-if="errors.name" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
            <p v-if="errors.name" class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ errors.name }}
            </p>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email
            </label>
            <div class="mt-1 relative">
              <input
                id="email"
                v-model="form.email"
                type="email"
                autocomplete="email"
                :class="[
                  'appearance-none relative block w-full px-3 py-2 border rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm transition-colors',
                  errors.email ? 'border-red-300 dark:border-red-600' : 'border-gray-300 dark:border-gray-600'
                ]"
                placeholder="tu@email.com"
                :disabled="isLoading"
                @input="clearError('email')"
              />
              <div v-if="errors.email" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
            <p v-if="errors.email" class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ errors.email }}
            </p>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Contraseña
            </label>
            <div class="mt-1 relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                :class="[
                  'appearance-none relative block w-full px-3 py-2 pr-10 border rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm transition-colors',
                  errors.password ? 'border-red-300 dark:border-red-600' : 'border-gray-300 dark:border-gray-600'
                ]"
                placeholder="Mínimo 8 caracteres"
                :disabled="isLoading"
                @input="clearError('password')"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showPassword = !showPassword"
                :disabled="isLoading"
              >
                <svg v-if="showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ errors.password }}
            </p>
            <!-- Indicador de fortaleza de contraseña -->
            <div v-if="form.password" class="mt-2">
              <div class="flex items-center space-x-2">
                <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    :class="[
                      'h-2 rounded-full transition-all duration-300',
                      passwordStrength.color
                    ]"
                    :style="{ width: passwordStrength.width }"
                  ></div>
                </div>
                <span :class="['text-xs font-medium', passwordStrength.textColor]">
                  {{ passwordStrength.text }}
                </span>
              </div>
            </div>
          </div>

          <!-- Confirmar Password -->
          <div>
            <label for="password_confirmation" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Confirmar contraseña
            </label>
            <div class="mt-1 relative">
              <input
                id="password_confirmation"
                v-model="form.password_confirmation"
                :type="showPasswordConfirmation ? 'text' : 'password'"
                autocomplete="new-password"
                :class="[
                  'appearance-none relative block w-full px-3 py-2 pr-10 border rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-800 focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm transition-colors',
                  errors.password_confirmation ? 'border-red-300 dark:border-red-600' : 'border-gray-300 dark:border-gray-600'
                ]"
                placeholder="Repite tu contraseña"
                :disabled="isLoading"
                @input="clearError('password_confirmation')"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                @click="showPasswordConfirmation = !showPasswordConfirmation"
                :disabled="isLoading"
              >
                <svg v-if="showPasswordConfirmation" class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                </svg>
                <svg v-else class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="errors.password_confirmation" class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ errors.password_confirmation }}
            </p>
          </div>
        </div>

        <!-- Términos y condiciones -->
        <div class="flex items-start">
          <div class="flex items-center h-5">
            <input
              id="terms_accepted"
              v-model="form.terms_accepted"
              type="checkbox"
              :class="[
                'h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 dark:border-gray-600 rounded dark:bg-gray-800',
                errors.terms_accepted ? 'border-red-300 dark:border-red-600' : ''
              ]"
              :disabled="isLoading"
              @change="clearError('terms_accepted')"
            />
          </div>
          <div class="ml-3 text-sm">
            <label for="terms_accepted" class="text-gray-700 dark:text-gray-300">
              Acepto los 
              <router-link to="/terms" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300">
                términos y condiciones
              </router-link>
              y la 
              <router-link to="/privacy" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300">
                política de privacidad
              </router-link>
            </label>
            <p v-if="errors.terms_accepted" class="mt-1 text-sm text-red-600 dark:text-red-400">
              {{ errors.terms_accepted }}
            </p>
          </div>
        </div>

        <!-- Submit button -->
        <div>
          <button
            type="submit"
            :disabled="isLoading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <LoadingSpinner
                v-if="isLoading"
                size="sm"
                color="white"
              />
              <svg v-else class="h-5 w-5 text-primary-500 group-hover:text-primary-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z" />
              </svg>
            </span>
            {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
          </button>
        </div>

        <!-- Login link -->
        <div class="text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            ¿Ya tienes una cuenta?
            <router-link
              to="/auth/login"
              class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 transition-colors"
            >
              Inicia sesión aquí
            </router-link>
          </p>
        </div>
      </form>

      <!-- Social register (opcional) -->
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-600" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              O regístrate con
            </span>
          </div>
        </div>

        <div class="mt-6 grid grid-cols-2 gap-3">
          <button
            type="button"
            class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            :disabled="isLoading"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span class="ml-2">Google</span>
          </button>

          <button
            type="button"
            class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            :disabled="isLoading"
          >
            <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.097.118.112.222.083.343-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/>
            </svg>
            <span class="ml-2">GitHub</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { registerSchema, validateData, type RegisterData } from '@/utils/validation'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useToast } from 'vue-toastification'

// Composables
const authStore = useAuthStore()
const toast = useToast()

// Estado reactivo
const form = ref<RegisterData>({
  name: '',
  email: '',
  password: '',
  password_confirmation: '',
  terms_accepted: false
})

const errors = ref<Record<string, string>>({})
const showPassword = ref(false)
const showPasswordConfirmation = ref(false)

// Computed
const isLoading = computed(() => authStore.isLoading)

const isFormValid = computed(() => {
  const validation = validateData(registerSchema, form.value)
  return validation.success && 
         form.value.name && 
         form.value.email && 
         form.value.password && 
         form.value.password_confirmation &&
         form.value.terms_accepted
})

// Indicador de fortaleza de contraseña
const passwordStrength = computed(() => {
  const password = form.value.password
  if (!password) return { width: '0%', color: 'bg-gray-300', textColor: 'text-gray-500', text: '' }
  
  let score = 0
  let feedback = []
  
  // Longitud
  if (password.length >= 8) score += 1
  else feedback.push('mínimo 8 caracteres')
  
  // Minúsculas
  if (/[a-z]/.test(password)) score += 1
  else feedback.push('una minúscula')
  
  // Mayúsculas
  if (/[A-Z]/.test(password)) score += 1
  else feedback.push('una mayúscula')
  
  // Números
  if (/\d/.test(password)) score += 1
  else feedback.push('un número')
  
  // Caracteres especiales
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 1
  
  const strengthLevels = [
    { width: '20%', color: 'bg-red-500', textColor: 'text-red-600', text: 'Muy débil' },
    { width: '40%', color: 'bg-orange-500', textColor: 'text-orange-600', text: 'Débil' },
    { width: '60%', color: 'bg-yellow-500', textColor: 'text-yellow-600', text: 'Regular' },
    { width: '80%', color: 'bg-blue-500', textColor: 'text-blue-600', text: 'Buena' },
    { width: '100%', color: 'bg-green-500', textColor: 'text-green-600', text: 'Excelente' }
  ]
  
  return strengthLevels[Math.min(score, 4)]
})

// Métodos
const validateForm = (): boolean => {
  const validation = validateData(registerSchema, form.value)
  
  if (!validation.success) {
    // Convertir errores de array a objeto
    errors.value = {}
    validation.errors.forEach(error => {
      const [field, message] = error.split(': ')
      if (field && message) {
        errors.value[field] = message
      }
    })
    return false
  }
  
  errors.value = {}
  return true
}

const handleSubmit = async (): Promise<void> => {
  // Limpiar errores previos
  errors.value = {}
  
  // Validar formulario
  if (!validateForm()) {
    toast.error('Por favor corrige los errores en el formulario')
    return
  }
  
  try {
    await authStore.register(form.value)
    // El store maneja la redirección y notificaciones
  } catch (error: any) {
    // Manejar errores específicos del servidor
    if (error.response?.status === 422) {
      const serverErrors = error.response.data.errors
      if (serverErrors) {
        Object.keys(serverErrors).forEach(field => {
          errors.value[field] = serverErrors[field][0]
        })
      }
    } else if (error.response?.status === 409) {
      // Email ya existe
      errors.value.email = 'Este email ya está registrado'
      toast.error('Este email ya está registrado')
    }
  }
}

const clearError = (field: string): void => {
  if (errors.value[field]) {
    delete errors.value[field]
  }
}

// Validación en tiempo real
const validateField = (field: string): void => {
  const fieldValidation = {
    name: () => {
      if (!form.value.name) return
      if (form.value.name.length < 2) {
        errors.value.name = 'El nombre debe tener al menos 2 caracteres'
      } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(form.value.name)) {
        errors.value.name = 'El nombre solo puede contener letras y espacios'
      } else {
        delete errors.value.name
      }
    },
    email: () => {
      if (!form.value.email) return
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(form.value.email)) {
        errors.value.email = 'Formato de email inválido'
      } else {
        delete errors.value.email
      }
    },
    password: () => {
      if (!form.value.password) return
      if (form.value.password.length < 8) {
        errors.value.password = 'La contraseña debe tener al menos 8 caracteres'
      } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(form.value.password)) {
        errors.value.password = 'Debe contener al menos una minúscula, una mayúscula y un número'
      } else {
        delete errors.value.password
      }
    },
    password_confirmation: () => {
      if (!form.value.password_confirmation) return
      if (form.value.password !== form.value.password_confirmation) {
        errors.value.password_confirmation = 'Las contraseñas no coinciden'
      } else {
        delete errors.value.password_confirmation
      }
    }
  }
  
  if (fieldValidation[field as keyof typeof fieldValidation]) {
    fieldValidation[field as keyof typeof fieldValidation]()
  }
}

// Lifecycle
onMounted(() => {
  // Verificar si ya está autenticado
  if (authStore.isAuthenticated) {
    // Redirigir al dashboard si ya está logueado
    window.location.href = '/dashboard'
  }
  
  // Focus en el primer campo
  const nameInput = document.getElementById('name')
  nameInput?.focus()
  
  // Configurar validación en tiempo real
  const inputs = ['name', 'email', 'password', 'password_confirmation']
  inputs.forEach(field => {
    const input = document.getElementById(field)
    input?.addEventListener('blur', () => validateField(field))
  })
})
</script>

<style scoped>
/* Animaciones personalizadas */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Efectos de hover mejorados */
button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Transiciones suaves para inputs */
input {
  transition: all 0.2s ease;
}

input:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* Estilo para el estado de carga */
.loading {
  pointer-events: none;
  opacity: 0.7;
}

/* Indicador de fortaleza de contraseña */
.password-strength {
  transition: all 0.3s ease;
}

/* Mejoras de accesibilidad */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Estilos para checkbox personalizado */
input[type="checkbox"]:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}
</style>