<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Mi Perfil</h1>
        <p class="text-gray-600 mt-1">Gestiona tu información personal y configuraciones</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button
          @click="resetChanges"
          :disabled="!hasChanges"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Descartar Cambios
        </button>
        <button
          @click="saveProfile"
          :disabled="!hasChanges || saving"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
        >
          <CheckIcon v-if="!saving" class="h-4 w-4" />
          <ArrowPathIcon v-else class="h-4 w-4 animate-spin" />
          <span>{{ saving ? 'Guardando...' : 'Guardar Cambios' }}</span>
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main Content -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Personal Information -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Información Personal</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre *</label>
              <input
                v-model="profile.firstName"
                type="text"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tu nombre"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Apellido *</label>
              <input
                v-model="profile.lastName"
                type="text"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tu apellido"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
              <input
                v-model="profile.email"
                type="email"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="tu@email.com"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
              <input
                v-model="profile.phone"
                type="tel"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="+1 (555) 123-4567"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Departamento</label>
              <select
                v-model="profile.department"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccionar departamento</option>
                <option value="sales">Ventas</option>
                <option value="marketing">Marketing</option>
                <option value="support">Soporte</option>
                <option value="development">Desarrollo</option>
                <option value="hr">Recursos Humanos</option>
                <option value="finance">Finanzas</option>
                <option value="operations">Operaciones</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Cargo</label>
              <input
                v-model="profile.jobTitle"
                type="text"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tu cargo"
              />
            </div>
          </div>
          
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Biografía</label>
            <textarea
              v-model="profile.bio"
              rows="3"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Cuéntanos un poco sobre ti..."
            ></textarea>
          </div>
        </div>

        <!-- Security Settings -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Configuración de Seguridad</h2>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Cambiar Contraseña</h3>
                <p class="text-sm text-gray-600">Actualiza tu contraseña regularmente para mayor seguridad</p>
              </div>
              <button
                @click="showChangePassword = true"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm"
              >
                Cambiar
              </button>
            </div>
            
            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Autenticación de Dos Factores</h3>
                <p class="text-sm text-gray-600">Añade una capa extra de seguridad a tu cuenta</p>
              </div>
              <ToggleSwitch
                v-model="profile.twoFactorEnabled"
                @update:modelValue="updateTwoFactor"
              />
            </div>
            
            <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h3 class="text-sm font-medium text-gray-900">Sesiones Activas</h3>
                <p class="text-sm text-gray-600">Gestiona tus sesiones activas en diferentes dispositivos</p>
              </div>
              <button
                @click="showActiveSessions = true"
                class="text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                Ver Sesiones
              </button>
            </div>
          </div>
        </div>

        <!-- Preferences -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Preferencias</h2>
          
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Idioma</label>
                <select
                  v-model="profile.language"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="es">Español</option>
                  <option value="en">English</option>
                  <option value="fr">Français</option>
                  <option value="de">Deutsch</option>
                  <option value="pt">Português</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Zona Horaria</label>
                <select
                  v-model="profile.timezone"
                  class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="America/New_York">Eastern Time (ET)</option>
                  <option value="America/Chicago">Central Time (CT)</option>
                  <option value="America/Denver">Mountain Time (MT)</option>
                  <option value="America/Los_Angeles">Pacific Time (PT)</option>
                  <option value="Europe/Madrid">Madrid (CET)</option>
                  <option value="Europe/London">London (GMT)</option>
                  <option value="Asia/Tokyo">Tokyo (JST)</option>
                </select>
              </div>
            </div>
            
            <div class="space-y-3">
              <label class="flex items-center space-x-3">
                <input
                  v-model="profile.emailNotifications"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700">Recibir notificaciones por email</span>
              </label>
              
              <label class="flex items-center space-x-3">
                <input
                  v-model="profile.desktopNotifications"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700">Notificaciones de escritorio</span>
              </label>
              
              <label class="flex items-center space-x-3">
                <input
                  v-model="profile.marketingEmails"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-700">Recibir emails de marketing</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Danger Zone -->
        <div class="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
          <h2 class="text-lg font-semibold text-red-900 mb-4">Zona de Peligro</h2>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg">
              <div>
                <h3 class="text-sm font-medium text-red-900">Desactivar Cuenta</h3>
                <p class="text-sm text-red-700">Desactiva temporalmente tu cuenta. Podrás reactivarla más tarde.</p>
              </div>
              <button
                @click="deactivateAccount"
                class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 text-sm"
              >
                Desactivar
              </button>
            </div>
            
            <div class="flex items-center justify-between p-4 bg-red-50 rounded-lg">
              <div>
                <h3 class="text-sm font-medium text-red-900">Eliminar Cuenta</h3>
                <p class="text-sm text-red-700">Elimina permanentemente tu cuenta y todos tus datos. Esta acción no se puede deshacer.</p>
              </div>
              <button
                @click="deleteAccount"
                class="bg-red-700 text-white px-4 py-2 rounded-lg hover:bg-red-800 text-sm"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Profile Picture -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Foto de Perfil</h3>
          
          <div class="text-center">
            <div class="relative inline-block">
              <img
                v-if="profile.avatar"
                :src="profile.avatar"
                :alt="profile.firstName + ' ' + profile.lastName"
                class="h-24 w-24 rounded-full object-cover"
              />
              <div
                v-else
                class="h-24 w-24 rounded-full bg-blue-500 flex items-center justify-center text-white text-2xl font-bold"
              >
                {{ getInitials(profile.firstName, profile.lastName) }}
              </div>
              
              <button
                @click="$refs.avatarInput.click()"
                class="absolute bottom-0 right-0 bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700"
              >
                <CameraIcon class="h-4 w-4" />
              </button>
            </div>
            
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              @change="handleAvatarUpload"
              class="hidden"
            />
            
            <p class="text-sm text-gray-600 mt-3">JPG, PNG o GIF. Máximo 5MB.</p>
            
            <div v-if="profile.avatar" class="mt-3">
              <button
                @click="removeAvatar"
                class="text-red-600 hover:text-red-700 text-sm"
              >
                Eliminar foto
              </button>
            </div>
          </div>
        </div>

        <!-- Account Stats -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Estadísticas de Cuenta</h3>
          
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Miembro desde</span>
              <span class="text-sm font-medium text-gray-900">{{ formatDate(profile.createdAt) }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Último acceso</span>
              <span class="text-sm font-medium text-gray-900">{{ formatDate(profile.lastLogin) }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Conversaciones</span>
              <span class="text-sm font-medium text-gray-900">{{ profile.stats.conversations }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Mensajes enviados</span>
              <span class="text-sm font-medium text-gray-900">{{ profile.stats.messagesSent }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Tiempo promedio respuesta</span>
              <span class="text-sm font-medium text-gray-900">{{ profile.stats.avgResponseTime }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
          
          <div class="space-y-2">
            <button
              @click="downloadData"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
            >
              <ArrowDownTrayIcon class="h-4 w-4" />
              <span>Descargar mis datos</span>
            </button>
            
            <button
              @click="exportProfile"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
            >
              <DocumentArrowUpIcon class="h-4 w-4" />
              <span>Exportar perfil</span>
            </button>
            
            <button
              @click="viewActivityLog"
              class="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2"
            >
              <ClockIcon class="h-4 w-4" />
              <span>Ver actividad</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Change Password Modal -->
    <ChangePasswordModal
      v-if="showChangePassword"
      @close="showChangePassword = false"
      @success="handlePasswordChanged"
    />

    <!-- Active Sessions Modal -->
    <ActiveSessionsModal
      v-if="showActiveSessions"
      @close="showActiveSessions = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  CheckIcon,
  ArrowPathIcon,
  CameraIcon,
  ArrowDownTrayIcon,
  DocumentArrowUpIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import ToggleSwitch from '@/components/ui/ToggleSwitch.vue'
import ChangePasswordModal from '@/components/dashboard/ChangePasswordModal.vue'
import ActiveSessionsModal from '@/components/dashboard/ActiveSessionsModal.vue'

// Reactive state
const saving = ref(false)
const showChangePassword = ref(false)
const showActiveSessions = ref(false)

const profile = ref({
  firstName: 'Juan',
  lastName: 'Pérez',
  email: 'juan@example.com',
  phone: '+1 (555) 123-4567',
  department: 'sales',
  jobTitle: 'Gerente de Ventas',
  bio: 'Especialista en ventas con más de 5 años de experiencia en el sector tecnológico.',
  avatar: null,
  language: 'es',
  timezone: 'Europe/Madrid',
  emailNotifications: true,
  desktopNotifications: true,
  marketingEmails: false,
  twoFactorEnabled: false,
  createdAt: '2023-06-15T10:30:00Z',
  lastLogin: '2024-01-15T14:25:00Z',
  stats: {
    conversations: 1247,
    messagesSent: 8934,
    avgResponseTime: '2.3 min'
  }
})

const originalProfile = ref({})

// Computed
const hasChanges = computed(() => {
  return JSON.stringify(profile.value) !== JSON.stringify(originalProfile.value)
})

// Watchers
watch(profile, () => {
  // Auto-save draft changes to localStorage
  localStorage.setItem('profileDraft', JSON.stringify(profile.value))
}, { deep: true })

// Methods
const getInitials = (firstName, lastName) => {
  return (firstName?.charAt(0) || '') + (lastName?.charAt(0) || '')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const handleAvatarUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    alert('El archivo es demasiado grande. Máximo 5MB.')
    return
  }
  
  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('Por favor selecciona un archivo de imagen válido.')
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    profile.value.avatar = e.target.result
  }
  reader.readAsDataURL(file)
}

const removeAvatar = () => {
  profile.value.avatar = null
}

const saveProfile = async () => {
  saving.value = true
  
  try {
    // TODO: Save profile to API
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Update original profile
    originalProfile.value = JSON.parse(JSON.stringify(profile.value))
    
    // Clear draft from localStorage
    localStorage.removeItem('profileDraft')
    
    alert('Perfil actualizado exitosamente')
  } catch (error) {
    console.error('Error saving profile:', error)
    alert('Error al guardar el perfil')
  } finally {
    saving.value = false
  }
}

const resetChanges = () => {
  if (confirm('¿Estás seguro de que quieres descartar todos los cambios?')) {
    profile.value = JSON.parse(JSON.stringify(originalProfile.value))
    localStorage.removeItem('profileDraft')
  }
}

const updateTwoFactor = (enabled) => {
  if (enabled) {
    // TODO: Show 2FA setup modal
    alert('Configuración de autenticación de dos factores')
  } else {
    if (confirm('¿Estás seguro de que quieres desactivar la autenticación de dos factores?')) {
      profile.value.twoFactorEnabled = false
    } else {
      profile.value.twoFactorEnabled = true
    }
  }
}

const handlePasswordChanged = () => {
  showChangePassword.value = false
  alert('Contraseña cambiada exitosamente')
}

const deactivateAccount = () => {
  if (confirm('¿Estás seguro de que quieres desactivar tu cuenta? Podrás reactivarla más tarde.')) {
    // TODO: Deactivate account via API
    alert('Cuenta desactivada. Te enviaremos un email con instrucciones para reactivarla.')
  }
}

const deleteAccount = () => {
  const confirmation = prompt('Para confirmar la eliminación de tu cuenta, escribe "ELIMINAR" en mayúsculas:')
  if (confirmation === 'ELIMINAR') {
    // TODO: Delete account via API
    alert('Tu cuenta será eliminada en 30 días. Te enviaremos un email de confirmación.')
  } else if (confirmation !== null) {
    alert('Confirmación incorrecta. La cuenta no ha sido eliminada.')
  }
}

const downloadData = () => {
  // TODO: Generate and download user data
  alert('Preparando descarga de datos. Te enviaremos un email cuando esté listo.')
}

const exportProfile = () => {
  const profileData = {
    ...profile.value,
    exportedAt: new Date().toISOString()
  }
  
  const dataStr = JSON.stringify(profileData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `perfil-${profile.value.firstName}-${profile.value.lastName}-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const viewActivityLog = () => {
  // TODO: Navigate to activity log or show modal
  alert('Función de registro de actividad próximamente')
}

// Initialize
onMounted(() => {
  // Store original profile
  originalProfile.value = JSON.parse(JSON.stringify(profile.value))
  
  // Load draft from localStorage if exists
  const draft = localStorage.getItem('profileDraft')
  if (draft) {
    try {
      const draftData = JSON.parse(draft)
      if (confirm('Se encontraron cambios no guardados. ¿Quieres restaurarlos?')) {
        profile.value = draftData
      } else {
        localStorage.removeItem('profileDraft')
      }
    } catch (error) {
      console.error('Error loading draft:', error)
      localStorage.removeItem('profileDraft')
    }
  }
  
  console.log('UserProfile mounted')
})
</script>