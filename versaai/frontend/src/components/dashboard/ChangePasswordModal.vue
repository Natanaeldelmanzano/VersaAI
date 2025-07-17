<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div>
          <h2 class="text-xl font-semibold text-gray-900">Cambiar Contraseña</h2>
          <p class="text-sm text-gray-600 mt-1">Actualiza tu contraseña para mayor seguridad</p>
        </div>
        
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
        >
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="changePassword" class="p-6">
        <div class="space-y-4">
          <!-- Current Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña Actual *</label>
            <div class="relative">
              <input
                v-model="form.currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="{ 'border-red-300': errors.currentPassword }"
                placeholder="Ingresa tu contraseña actual"
              />
              <button
                type="button"
                @click="showCurrentPassword = !showCurrentPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showCurrentPassword" class="h-4 w-4 text-gray-400" />
                <EyeSlashIcon v-else class="h-4 w-4 text-gray-400" />
              </button>
            </div>
            <p v-if="errors.currentPassword" class="text-red-600 text-xs mt-1">{{ errors.currentPassword }}</p>
          </div>

          <!-- New Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña *</label>
            <div class="relative">
              <input
                v-model="form.newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="{ 'border-red-300': errors.newPassword }"
                placeholder="Ingresa tu nueva contraseña"
                @input="validatePassword"
              />
              <button
                type="button"
                @click="showNewPassword = !showNewPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showNewPassword" class="h-4 w-4 text-gray-400" />
                <EyeSlashIcon v-else class="h-4 w-4 text-gray-400" />
              </button>
            </div>
            <p v-if="errors.newPassword" class="text-red-600 text-xs mt-1">{{ errors.newPassword }}</p>
            
            <!-- Password Strength Indicator -->
            <div v-if="form.newPassword" class="mt-2">
              <div class="flex items-center space-x-2">
                <div class="flex-1 bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="passwordStrengthClass"
                    :style="{ width: passwordStrengthWidth }"
                  ></div>
                </div>
                <span class="text-xs font-medium" :class="passwordStrengthTextClass">
                  {{ passwordStrengthText }}
                </span>
              </div>
              
              <!-- Password Requirements -->
              <div class="mt-2 space-y-1">
                <div class="flex items-center space-x-2">
                  <CheckCircleIcon v-if="passwordChecks.length" class="h-3 w-3 text-green-500" />
                  <XCircleIcon v-else class="h-3 w-3 text-gray-300" />
                  <span class="text-xs" :class="passwordChecks.length ? 'text-green-600' : 'text-gray-500'">
                    Al menos 8 caracteres
                  </span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <CheckCircleIcon v-if="passwordChecks.uppercase" class="h-3 w-3 text-green-500" />
                  <XCircleIcon v-else class="h-3 w-3 text-gray-300" />
                  <span class="text-xs" :class="passwordChecks.uppercase ? 'text-green-600' : 'text-gray-500'">
                    Una letra mayúscula
                  </span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <CheckCircleIcon v-if="passwordChecks.lowercase" class="h-3 w-3 text-green-500" />
                  <XCircleIcon v-else class="h-3 w-3 text-gray-300" />
                  <span class="text-xs" :class="passwordChecks.lowercase ? 'text-green-600' : 'text-gray-500'">
                    Una letra minúscula
                  </span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <CheckCircleIcon v-if="passwordChecks.number" class="h-3 w-3 text-green-500" />
                  <XCircleIcon v-else class="h-3 w-3 text-gray-300" />
                  <span class="text-xs" :class="passwordChecks.number ? 'text-green-600' : 'text-gray-500'">
                    Un número
                  </span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <CheckCircleIcon v-if="passwordChecks.special" class="h-3 w-3 text-green-500" />
                  <XCircleIcon v-else class="h-3 w-3 text-gray-300" />
                  <span class="text-xs" :class="passwordChecks.special ? 'text-green-600' : 'text-gray-500'">
                    Un carácter especial
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nueva Contraseña *</label>
            <div class="relative">
              <input
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="{ 'border-red-300': errors.confirmPassword }"
                placeholder="Confirma tu nueva contraseña"
                @input="validateConfirmPassword"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <EyeIcon v-if="!showConfirmPassword" class="h-4 w-4 text-gray-400" />
                <EyeSlashIcon v-else class="h-4 w-4 text-gray-400" />
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="text-red-600 text-xs mt-1">{{ errors.confirmPassword }}</p>
          </div>
        </div>

        <!-- Security Tips -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 class="text-sm font-medium text-blue-900 mb-2">Consejos de Seguridad</h4>
          <ul class="text-xs text-blue-800 space-y-1">
            <li>• Usa una combinación única de letras, números y símbolos</li>
            <li>• Evita usar información personal como fechas de nacimiento</li>
            <li>• No reutilices contraseñas de otras cuentas</li>
            <li>• Considera usar un gestor de contraseñas</li>
          </ul>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-3 mt-6 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          
          <button
            type="submit"
            :disabled="!isFormValid || loading"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <ArrowPathIcon v-if="loading" class="h-4 w-4 animate-spin" />
            <CheckIcon v-else class="h-4 w-4" />
            <span>{{ loading ? 'Cambiando...' : 'Cambiar Contraseña' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {
  XMarkIcon,
  EyeIcon,
  EyeSlashIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'

// Emits
const emit = defineEmits(['close', 'success'])

// Reactive state
const loading = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const form = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const errors = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// Computed
const passwordChecks = computed(() => {
  const password = form.value.newPassword
  return {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
  }
})

const passwordStrength = computed(() => {
  const checks = passwordChecks.value
  const score = Object.values(checks).filter(Boolean).length
  
  if (score === 0) return 0
  if (score <= 2) return 1
  if (score <= 3) return 2
  if (score <= 4) return 3
  return 4
})

const passwordStrengthClass = computed(() => {
  const classes = {
    0: 'bg-gray-300',
    1: 'bg-red-500',
    2: 'bg-yellow-500',
    3: 'bg-blue-500',
    4: 'bg-green-500'
  }
  return classes[passwordStrength.value]
})

const passwordStrengthTextClass = computed(() => {
  const classes = {
    0: 'text-gray-500',
    1: 'text-red-600',
    2: 'text-yellow-600',
    3: 'text-blue-600',
    4: 'text-green-600'
  }
  return classes[passwordStrength.value]
})

const passwordStrengthText = computed(() => {
  const texts = {
    0: 'Sin contraseña',
    1: 'Muy débil',
    2: 'Débil',
    3: 'Buena',
    4: 'Muy fuerte'
  }
  return texts[passwordStrength.value]
})

const passwordStrengthWidth = computed(() => {
  return `${(passwordStrength.value / 4) * 100}%`
})

const isFormValid = computed(() => {
  return (
    form.value.currentPassword &&
    form.value.newPassword &&
    form.value.confirmPassword &&
    passwordStrength.value >= 3 &&
    form.value.newPassword === form.value.confirmPassword &&
    !errors.value.currentPassword &&
    !errors.value.newPassword &&
    !errors.value.confirmPassword
  )
})

// Watchers
watch(() => form.value.newPassword, () => {
  validatePassword()
  if (form.value.confirmPassword) {
    validateConfirmPassword()
  }
})

watch(() => form.value.confirmPassword, validateConfirmPassword)

// Methods
const validatePassword = () => {
  errors.value.newPassword = ''
  
  if (!form.value.newPassword) {
    return
  }
  
  if (form.value.newPassword.length < 8) {
    errors.value.newPassword = 'La contraseña debe tener al menos 8 caracteres'
    return
  }
  
  if (passwordStrength.value < 3) {
    errors.value.newPassword = 'La contraseña debe ser más fuerte'
    return
  }
  
  if (form.value.currentPassword && form.value.newPassword === form.value.currentPassword) {
    errors.value.newPassword = 'La nueva contraseña debe ser diferente a la actual'
    return
  }
}

const validateConfirmPassword = () => {
  errors.value.confirmPassword = ''
  
  if (!form.value.confirmPassword) {
    return
  }
  
  if (form.value.newPassword !== form.value.confirmPassword) {
    errors.value.confirmPassword = 'Las contraseñas no coinciden'
    return
  }
}

const changePassword = async () => {
  // Clear previous errors
  errors.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  
  // Validate form
  validatePassword()
  validateConfirmPassword()
  
  if (!isFormValid.value) {
    return
  }
  
  loading.value = true
  
  try {
    // TODO: Call API to change password
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Simulate API response
    const success = Math.random() > 0.2 // 80% success rate for demo
    
    if (success) {
      emit('success')
    } else {
      errors.value.currentPassword = 'Contraseña actual incorrecta'
    }
  } catch (error) {
    console.error('Error changing password:', error)
    errors.value.currentPassword = 'Error al cambiar la contraseña. Inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>