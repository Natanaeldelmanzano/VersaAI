import { ref, reactive, computed } from 'vue'
import { settingsAPI } from '@/services/api'

// Global state
const settings = ref({})
const loading = ref(false)
const error = ref(null)
const saving = ref(false)

export function useSettings() {
  // Reactive settings data
  const generalSettings = reactive({
    company_name: '',
    company_logo: '',
    primary_color: '#3B82F6',
    secondary_color: '#10B981',
    language: 'es',
    timezone: 'America/Mexico_City',
    date_format: 'DD/MM/YYYY',
    currency: 'MXN'
  })

  const aiSettings = reactive({
    default_model: 'groq-llama',
    temperature: 0.7,
    max_tokens: 1000,
    response_timeout: 30,
    enable_learning: true,
    auto_training: false,
    confidence_threshold: 0.8
  })

  const notificationSettings = reactive({
    email_notifications: true,
    push_notifications: true,
    daily_reports: true,
    weekly_reports: false,
    error_alerts: true,
    performance_alerts: true
  })

  const securitySettings = reactive({
    two_factor_auth: false,
    session_timeout: 60,
    password_expiry: 90,
    login_attempts: 5,
    ip_whitelist: [],
    api_rate_limit: 1000
  })

  // Computed properties
  const hasUnsavedChanges = computed(() => {
    return saving.value
  })

  const availableLanguages = computed(() => [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'pt', name: 'Português', flag: '🇵🇹' }
  ])

  const availableTimezones = computed(() => [
    { value: 'America/Mexico_City', label: 'Ciudad de México (GMT-6)' },
    { value: 'America/New_York', label: 'Nueva York (GMT-5)' },
    { value: 'America/Los_Angeles', label: 'Los Ángeles (GMT-8)' },
    { value: 'Europe/Madrid', label: 'Madrid (GMT+1)' },
    { value: 'Europe/London', label: 'Londres (GMT+0)' },
    { value: 'Asia/Tokyo', label: 'Tokio (GMT+9)' }
  ])

  const availableModels = computed(() => [
    { value: 'groq-llama', label: 'Groq Llama 3.1 70B', description: 'Modelo rápido y eficiente' },
    { value: 'groq-mixtral', label: 'Groq Mixtral 8x7B', description: 'Modelo multilingüe avanzado' },
    { value: 'groq-gemma', label: 'Groq Gemma 7B', description: 'Modelo optimizado para conversaciones' }
  ])

  // Methods
  const loadSettings = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await settingsAPI.getSettings()
      
      if (response.data) {
        // Update reactive objects with API data
        Object.assign(generalSettings, response.data.general || {})
        Object.assign(aiSettings, response.data.ai || {})
        Object.assign(notificationSettings, response.data.notifications || {})
        Object.assign(securitySettings, response.data.security || {})
        
        settings.value = response.data
      }
    } catch (err) {
      console.warn('Failed to load settings from API, using defaults:', err)
      error.value = 'Error al cargar la configuración'
      
      // Use default values if API fails
      loadDefaultSettings()
    } finally {
      loading.value = false
    }
  }

  const loadDefaultSettings = () => {
    // Default values are already set in reactive objects
    console.log('Using default settings')
  }

  const saveSettings = async (section = 'all') => {
    saving.value = true
    error.value = null

    try {
      const settingsData = {
        general: generalSettings.value,
        ai: aiSettings.value,
        notifications: notificationSettings.value,
        security: securitySettings.value
      }

      let response
      if (section === 'all') {
        response = await settingsAPI.updateSettings(settingsData)
      } else {
        // Use specific API endpoints for each section
        switch (section) {
          case 'ai':
            response = await settingsAPI.updateAISettings(settingsData[section])
            break
          case 'security':
            response = await settingsAPI.updateSecuritySettings(settingsData[section])
            break
          case 'notifications':
            response = await settingsAPI.updateNotificationSettings(settingsData[section])
            break
          default:
            response = await settingsAPI.updateSettings(settingsData)
        }
      }

      if (response.data) {
        settings.value = response.data
        showToast('Configuración guardada exitosamente', 'success')
      }
    } catch (err) {
      console.error('Error saving settings:', err)
      error.value = 'Error al guardar la configuración'
      showToast('Error al guardar la configuración', 'error')
    } finally {
      saving.value = false
    }
  }

  const resetSettings = async (section = 'all') => {
    try {
      const response = await settingsAPI.resetSettings()
      
      if (response.data) {
        await loadSettings()
        showToast('Configuración restablecida', 'success')
      }
    } catch (err) {
      console.error('Error resetting settings:', err)
      error.value = 'Error al restablecer la configuración'
      showToast('Error al restablecer la configuración', 'error')
    }
  }

  const exportSettings = async () => {
    try {
      const response = await settingsAPI.exportSettings()
      
      if (response.data) {
        // Create download link
        const blob = new Blob([JSON.stringify(response.data, null, 2)], {
          type: 'application/json'
        })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `versaai-settings-${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        showToast('Configuración exportada exitosamente', 'success')
      }
    } catch (err) {
      console.error('Error exporting settings:', err)
      error.value = 'Error al exportar la configuración'
      showToast('Error al exportar la configuración', 'error')
    }
  }

  const importSettings = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await settingsAPI.importSettings(formData)
      
      if (response.data) {
        await loadSettings()
        showToast('Configuración importada exitosamente', 'success')
      }
    } catch (err) {
      console.error('Error importing settings:', err)
      error.value = 'Error al importar la configuración'
      showToast('Error al importar la configuración', 'error')
    }
  }

  const validateSettings = (section, data) => {
    const errors = []

    switch (section) {
      case 'general':
        if (!data.company_name?.trim()) {
          errors.push('El nombre de la empresa es requerido')
        }
        if (!data.language) {
          errors.push('El idioma es requerido')
        }
        break

      case 'ai':
        if (data.temperature < 0 || data.temperature > 2) {
          errors.push('La temperatura debe estar entre 0 y 2')
        }
        if (data.max_tokens < 100 || data.max_tokens > 4000) {
          errors.push('Los tokens máximos deben estar entre 100 y 4000')
        }
        break

      case 'security':
        if (data.session_timeout < 5 || data.session_timeout > 480) {
          errors.push('El tiempo de sesión debe estar entre 5 y 480 minutos')
        }
        if (data.login_attempts < 3 || data.login_attempts > 10) {
          errors.push('Los intentos de login deben estar entre 3 y 10')
        }
        break
    }

    return errors
  }

  // Utility functions
  const showToast = (message, type = 'info') => {
    // Simple toast implementation
    console.log(`[${type.toUpperCase()}] ${message}`)
    
    // You can integrate with a toast library here
    if (window.showToast) {
      window.showToast(message, type)
    }
  }

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDuration = (minutes) => {
    if (minutes < 60) {
      return `${minutes} minutos`
    }
    const hours = Math.floor(minutes / 60)
    const remainingMinutes = minutes % 60
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours} horas`
  }

  return {
    // State
    settings,
    loading,
    error,
    saving,
    
    // Settings sections
    generalSettings,
    aiSettings,
    notificationSettings,
    securitySettings,
    
    // Computed
    hasUnsavedChanges,
    availableLanguages,
    availableTimezones,
    availableModels,
    
    // Methods
    loadSettings,
    saveSettings,
    resetSettings,
    exportSettings,
    importSettings,
    validateSettings,
    
    // Utilities
    formatBytes,
    formatDuration
  }
}

// Export singleton instance
export const settingsStore = useSettings()