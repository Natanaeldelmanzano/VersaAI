<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8">
    <!-- Header -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Configuración de Usuario
      </h1>
      <p class="text-gray-600 dark:text-gray-400">
        Ejemplo de validaciones avanzadas y gestión de perfil
      </p>
    </div>

    <!-- Perfil del Usuario -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Información del Perfil
      </h2>
      
      <form @submit.prevent="handleProfileUpdate" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Nombre -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre completo *
            </label>
            <input
              v-model="profileForm.name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Tu nombre completo"
              :disabled="isLoading"
              @blur="validateProfileField('name')"
            />
            <p v-if="profileErrors.name" class="mt-1 text-sm text-red-600">
              {{ profileErrors.name }}
            </p>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Correo electrónico *
            </label>
            <input
              v-model="profileForm.email"
              type="email"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="tu@email.com"
              :disabled="isLoading"
              @blur="validateProfileField('email')"
            />
            <p v-if="profileErrors.email" class="mt-1 text-sm text-red-600">
              {{ profileErrors.email }}
            </p>
          </div>

          <!-- Teléfono -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Teléfono
            </label>
            <input
              v-model="profileForm.phone"
              type="tel"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="+1 (555) 123-4567"
              :disabled="isLoading"
              @blur="validateProfileField('phone')"
            />
            <p v-if="profileErrors.phone" class="mt-1 text-sm text-red-600">
              {{ profileErrors.phone }}
            </p>
          </div>

          <!-- Organización -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Organización
            </label>
            <input
              v-model="profileForm.organization"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Tu empresa u organización"
              :disabled="isLoading"
            />
          </div>
        </div>

        <!-- Bio -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Biografía
          </label>
          <textarea
            v-model="profileForm.bio"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
            placeholder="Cuéntanos sobre ti..."
            :disabled="isLoading"
            maxlength="500"
          ></textarea>
          <p class="mt-1 text-sm text-gray-500">
            {{ profileForm.bio?.length || 0 }}/500 caracteres
          </p>
        </div>

        <!-- Preferencias -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Idioma preferido
            </label>
            <select
              v-model="profileForm.language"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              :disabled="isLoading"
            >
              <option value="es">Español</option>
              <option value="en">English</option>
              <option value="fr">Français</option>
              <option value="de">Deutsch</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Zona horaria
            </label>
            <select
              v-model="profileForm.timezone"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              :disabled="isLoading"
            >
              <option value="America/New_York">Eastern Time (ET)</option>
              <option value="America/Chicago">Central Time (CT)</option>
              <option value="America/Denver">Mountain Time (MT)</option>
              <option value="America/Los_Angeles">Pacific Time (PT)</option>
              <option value="Europe/Madrid">Madrid (CET)</option>
              <option value="Europe/London">London (GMT)</option>
            </select>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="resetProfileForm"
            :disabled="isLoading"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="isLoading || !isProfileFormValid"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
            {{ isLoading ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Cambio de Contraseña -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Cambiar Contraseña
      </h2>
      
      <form @submit.prevent="handlePasswordChange" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Contraseña actual -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Contraseña actual *
            </label>
            <input
              v-model="passwordForm.current_password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Tu contraseña actual"
              :disabled="isLoading"
            />
            <p v-if="passwordErrors.current_password" class="mt-1 text-sm text-red-600">
              {{ passwordErrors.current_password }}
            </p>
          </div>

          <!-- Nueva contraseña -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nueva contraseña *
            </label>
            <input
              v-model="passwordForm.new_password"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Nueva contraseña"
              :disabled="isLoading"
              @input="validatePasswordField('new_password')"
            />
            <p v-if="passwordErrors.new_password" class="mt-1 text-sm text-red-600">
              {{ passwordErrors.new_password }}
            </p>
            
            <!-- Indicador de fortaleza -->
            <div v-if="passwordForm.new_password" class="mt-2">
              <div class="flex items-center space-x-2">
                <div class="flex-1 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="passwordStrengthColor"
                    :style="{ width: passwordStrengthWidth }"
                  ></div>
                </div>
                <span class="text-xs font-medium" :class="passwordStrengthColor.replace('bg-', 'text-')">
                  {{ passwordStrengthText }}
                </span>
              </div>
            </div>
          </div>

          <!-- Confirmar contraseña -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Confirmar nueva contraseña *
            </label>
            <input
              v-model="passwordForm.new_password_confirmation"
              type="password"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder="Confirma tu nueva contraseña"
              :disabled="isLoading"
              @input="validatePasswordField('new_password_confirmation')"
            />
            <p v-if="passwordErrors.new_password_confirmation" class="mt-1 text-sm text-red-600">
              {{ passwordErrors.new_password_confirmation }}
            </p>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="resetPasswordForm"
            :disabled="isLoading"
            class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="isLoading || !isPasswordFormValid"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
            {{ isLoading ? 'Cambiando...' : 'Cambiar Contraseña' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Configuración de Notificaciones -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">
        Preferencias de Notificaciones
      </h2>
      
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">
              Notificaciones por email
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Recibir actualizaciones importantes por correo
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              v-model="notificationSettings.email_notifications"
              type="checkbox"
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">
              Notificaciones push
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Recibir notificaciones en tiempo real
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              v-model="notificationSettings.push_notifications"
              type="checkbox"
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">
              Actualizaciones de producto
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Información sobre nuevas funcionalidades
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              v-model="notificationSettings.product_updates"
              type="checkbox"
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
          </label>
        </div>

        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">
              Recordatorios de seguridad
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Alertas sobre actividad sospechosa
            </p>
          </div>
          <label class="relative inline-flex items-center cursor-pointer">
            <input
              v-model="notificationSettings.security_alerts"
              type="checkbox"
              class="sr-only peer"
            />
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
          </label>
        </div>
      </div>

      <div class="mt-6 flex justify-end">
        <button
          @click="saveNotificationSettings"
          :disabled="isLoading"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          <LoadingSpinner v-if="isLoading" size="sm" color="white" class="mr-2" />
          Guardar Preferencias
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { 
  userProfileSchema, 
  changePasswordSchema, 
  validateData, 
  type UserProfileData, 
  type ChangePasswordData 
} from '@/utils/validation'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { useToast } from 'vue-toastification'

// Composables
const auth = useAuth()
const toast = useToast()

// Estado reactivo
const isLoading = ref(false)

// Formulario de perfil
const profileForm = ref<UserProfileData>({
  name: 'Juan Pérez',
  email: 'juan@versaai.com',
  phone: '+34 123 456 789',
  organization: 'VersaAI',
  bio: 'Desarrollador apasionado por la IA y las nuevas tecnologías.',
  language: 'es',
  timezone: 'Europe/Madrid'
})

const profileErrors = ref<Record<string, string>>({})

// Formulario de contraseña
const passwordForm = ref<ChangePasswordData>({
  current_password: '',
  new_password: '',
  new_password_confirmation: ''
})

const passwordErrors = ref<Record<string, string>>({})

// Configuración de notificaciones
const notificationSettings = ref({
  email_notifications: true,
  push_notifications: true,
  product_updates: false,
  security_alerts: true
})

// Computed properties
const isProfileFormValid = computed(() => {
  const validation = validateData(userProfileSchema, profileForm.value)
  return validation.success && Object.keys(profileErrors.value).length === 0
})

const isPasswordFormValid = computed(() => {
  const validation = validateData(changePasswordSchema, passwordForm.value)
  return validation.success && Object.keys(passwordErrors.value).length === 0
})

// Validación de fortaleza de contraseña
const passwordStrength = computed(() => {
  const password = passwordForm.value.new_password
  if (!password) return { score: 0, text: '', color: 'bg-gray-300', width: '0%' }
  
  let score = 0
  const checks = {
    length: password.length >= 8,
    lowercase: /[a-z]/.test(password),
    uppercase: /[A-Z]/.test(password),
    numbers: /\d/.test(password),
    symbols: /[^\w\s]/.test(password)
  }
  
  score = Object.values(checks).filter(Boolean).length
  
  const levels = [
    { score: 0, text: 'Muy débil', color: 'bg-red-500', width: '20%' },
    { score: 1, text: 'Débil', color: 'bg-red-400', width: '40%' },
    { score: 2, text: 'Regular', color: 'bg-yellow-500', width: '60%' },
    { score: 3, text: 'Buena', color: 'bg-blue-500', width: '80%' },
    { score: 4, text: 'Fuerte', color: 'bg-green-500', width: '100%' },
    { score: 5, text: 'Muy fuerte', color: 'bg-green-600', width: '100%' }
  ]
  
  return levels[Math.min(score, 5)]
})

const passwordStrengthText = computed(() => passwordStrength.value.text)
const passwordStrengthColor = computed(() => passwordStrength.value.color)
const passwordStrengthWidth = computed(() => passwordStrength.value.width)

// Métodos de validación
const validateProfileField = (field: string): void => {
  const fieldValidations = {
    name: () => {
      if (!profileForm.value.name || profileForm.value.name.length < 2) {
        profileErrors.value.name = 'El nombre debe tener al menos 2 caracteres'
      } else {
        delete profileErrors.value.name
      }
    },
    email: () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(profileForm.value.email)) {
        profileErrors.value.email = 'Formato de email inválido'
      } else {
        delete profileErrors.value.email
      }
    },
    phone: () => {
      if (profileForm.value.phone && !/^\+?[1-9]\d{1,14}$/.test(profileForm.value.phone.replace(/\s/g, ''))) {
        profileErrors.value.phone = 'Formato de teléfono inválido'
      } else {
        delete profileErrors.value.phone
      }
    }
  }
  
  if (fieldValidations[field as keyof typeof fieldValidations]) {
    fieldValidations[field as keyof typeof fieldValidations]()
  }
}

const validatePasswordField = (field: string): void => {
  const fieldValidations = {
    new_password: () => {
      const password = passwordForm.value.new_password
      if (password.length < 8) {
        passwordErrors.value.new_password = 'La contraseña debe tener al menos 8 caracteres'
      } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
        passwordErrors.value.new_password = 'Debe contener mayúscula, minúscula y número'
      } else {
        delete passwordErrors.value.new_password
      }
    },
    new_password_confirmation: () => {
      if (passwordForm.value.new_password !== passwordForm.value.new_password_confirmation) {
        passwordErrors.value.new_password_confirmation = 'Las contraseñas no coinciden'
      } else {
        delete passwordErrors.value.new_password_confirmation
      }
    }
  }
  
  if (fieldValidations[field as keyof typeof fieldValidations]) {
    fieldValidations[field as keyof typeof fieldValidations]()
  }
}

// Métodos de manejo de formularios
const handleProfileUpdate = async (): Promise<void> => {
  profileErrors.value = {}
  isLoading.value = true
  
  try {
    // Validar formulario
    const validation = validateData(userProfileSchema, profileForm.value)
    if (!validation.success) {
      validation.errors.forEach(error => {
        const [field, message] = error.split(': ')
        if (field && message) {
          profileErrors.value[field] = message
        }
      })
      toast.error('Por favor corrige los errores en el formulario')
      return
    }
    
    // Simular actualización del perfil
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Actualizar en el store de auth
    const success = await auth.updateProfile(profileForm.value)
    if (success) {
      toast.success('Perfil actualizado exitosamente')
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    toast.error('Error al actualizar el perfil')
  } finally {
    isLoading.value = false
  }
}

const handlePasswordChange = async (): Promise<void> => {
  passwordErrors.value = {}
  isLoading.value = true
  
  try {
    // Validar formulario
    const validation = validateData(changePasswordSchema, passwordForm.value)
    if (!validation.success) {
      validation.errors.forEach(error => {
        const [field, message] = error.split(': ')
        if (field && message) {
          passwordErrors.value[field] = message
        }
      })
      toast.error('Por favor corrige los errores en el formulario')
      return
    }
    
    // Simular cambio de contraseña
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Cambiar contraseña
    const success = await auth.changePassword(passwordForm.value)
    if (success) {
      toast.success('Contraseña cambiada exitosamente')
      resetPasswordForm()
    }
  } catch (error) {
    console.error('Error changing password:', error)
    toast.error('Error al cambiar la contraseña')
  } finally {
    isLoading.value = false
  }
}

const saveNotificationSettings = async (): Promise<void> => {
  isLoading.value = true
  
  try {
    // Simular guardado de configuración
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    toast.success('Preferencias de notificación guardadas')
  } catch (error) {
    console.error('Error saving notification settings:', error)
    toast.error('Error al guardar las preferencias')
  } finally {
    isLoading.value = false
  }
}

// Métodos de reset
const resetProfileForm = (): void => {
  profileForm.value = {
    name: 'Juan Pérez',
    email: 'juan@versaai.com',
    phone: '+34 123 456 789',
    organization: 'VersaAI',
    bio: 'Desarrollador apasionado por la IA y las nuevas tecnologías.',
    language: 'es',
    timezone: 'Europe/Madrid'
  }
  profileErrors.value = {}
}

const resetPasswordForm = (): void => {
  passwordForm.value = {
    current_password: '',
    new_password: '',
    new_password_confirmation: ''
  }
  passwordErrors.value = {}
}

// Lifecycle
onMounted(() => {
  console.log('🔧 UserSettingsExample component mounted')
  
  // Cargar datos del usuario si está autenticado
  if (auth.user.value) {
    profileForm.value.name = auth.user.value.name || profileForm.value.name
    profileForm.value.email = auth.user.value.email || profileForm.value.email
  }
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

/* Mejoras visuales para inputs */
input:focus,
textarea:focus,
select:focus {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

/* Animaciones suaves para botones */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Estilos para el toggle switch */
.peer:checked + div {
  background-color: rgb(37, 99, 235);
}

/* Indicador de fortaleza de contraseña */
.password-strength {
  transition: all 0.3s ease;
}
</style>