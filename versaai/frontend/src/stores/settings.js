import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useSettingsStore = defineStore('settings', () => {
  // State
  const generalSettings = ref({
    site_name: '',
    site_description: '',
    site_url: '',
    admin_email: '',
    support_email: '',
    default_language: 'es',
    timezone: 'UTC',
    date_format: 'DD/MM/YYYY',
    time_format: '24h',
    maintenance_mode: false,
    registration_enabled: true,
    email_verification_required: true
  })
  
  const aiSettings = ref({
    default_model: 'groq-llama',
    groq_api_key: '',
    claude_api_key: '',
    openai_api_key: '',
    max_tokens: 2048,
    temperature: 0.7,
    top_p: 0.9,
    frequency_penalty: 0.0,
    presence_penalty: 0.0,
    response_timeout: 30,
    max_context_length: 4096,
    enable_streaming: true,
    enable_function_calling: false,
    default_system_prompt: '',
    fallback_model: 'groq-llama'
  })
  
  const securitySettings = ref({
    password_min_length: 8,
    password_require_uppercase: true,
    password_require_lowercase: true,
    password_require_numbers: true,
    password_require_symbols: false,
    password_expiry_days: 90,
    max_login_attempts: 5,
    lockout_duration: 15,
    session_timeout: 24,
    two_factor_enabled: false,
    jwt_expiry_hours: 24,
    refresh_token_expiry_days: 7,
    cors_origins: [],
    rate_limit_enabled: true,
    rate_limit_requests: 100,
    rate_limit_window: 60
  })
  
  const emailSettings = ref({
    smtp_host: '',
    smtp_port: 587,
    smtp_username: '',
    smtp_password: '',
    smtp_use_tls: true,
    smtp_use_ssl: false,
    from_email: '',
    from_name: '',
    reply_to_email: '',
    email_templates: {
      welcome: '',
      password_reset: '',
      email_verification: '',
      invitation: ''
    }
  })
  
  const storageSettings = ref({
    storage_provider: 'local',
    max_file_size: 10,
    allowed_file_types: ['pdf', 'txt', 'docx', 'md'],
    storage_path: '/uploads',
    aws_access_key: '',
    aws_secret_key: '',
    aws_bucket: '',
    aws_region: 'us-east-1',
    gcs_credentials: '',
    gcs_bucket: '',
    azure_connection_string: '',
    azure_container: '',
    cleanup_temp_files: true,
    temp_file_expiry: 24
  })
  
  const storageUsage = ref({
    total_size: 0,
    used_size: 0,
    available_size: 0,
    file_count: 0,
    usage_percentage: 0,
    breakdown: {
      documents: 0,
      images: 0,
      temp_files: 0,
      backups: 0
    }
  })
  
  const isLoading = ref(false)
  const isSaving = ref(false)
  const isTesting = ref(false)
  
  const toast = useToast()

  // Getters
  const isMaintenanceMode = computed(() => generalSettings.value.maintenance_mode)
  
  const isRegistrationEnabled = computed(() => generalSettings.value.registration_enabled)
  
  const storageUsagePercentage = computed(() => {
    if (storageUsage.value.total_size === 0) return 0
    return Math.round((storageUsage.value.used_size / storageUsage.value.total_size) * 100)
  })
  
  const isStorageNearLimit = computed(() => storageUsagePercentage.value > 80)
  
  const formattedStorageSize = computed(() => {
    const formatBytes = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    return {
      used: formatBytes(storageUsage.value.used_size),
      total: formatBytes(storageUsage.value.total_size),
      available: formatBytes(storageUsage.value.available_size)
    }
  })
  
  const hasValidEmailConfig = computed(() => {
    return emailSettings.value.smtp_host && 
           emailSettings.value.smtp_username && 
           emailSettings.value.from_email
  })
  
  const hasValidAIConfig = computed(() => {
    return aiSettings.value.groq_api_key || 
           aiSettings.value.claude_api_key || 
           aiSettings.value.openai_api_key
  })

  // Actions
  const fetchAllSettings = async () => {
    try {
      isLoading.value = true
      
      const [generalRes, aiRes, securityRes, emailRes, storageRes] = await Promise.all([
        axios.get('/api/v1/settings/general'),
        axios.get('/api/v1/settings/ai'),
        axios.get('/api/v1/settings/security'),
        axios.get('/api/v1/settings/email'),
        axios.get('/api/v1/settings/storage')
      ])
      
      generalSettings.value = { ...generalSettings.value, ...generalRes.data }
      aiSettings.value = { ...aiSettings.value, ...aiRes.data }
      securitySettings.value = { ...securitySettings.value, ...securityRes.data }
      emailSettings.value = { ...emailSettings.value, ...emailRes.data }
      storageSettings.value = { ...storageSettings.value, ...storageRes.data }
      
      return { success: true }
    } catch (error) {
      console.error('Fetch settings error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las configuraciones'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const saveGeneralSettings = async (settings) => {
    try {
      isSaving.value = true
      
      const response = await axios.put('/api/v1/settings/general', settings)
      
      generalSettings.value = { ...generalSettings.value, ...response.data }
      
      toast.success('Configuración general guardada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Save general settings error:', error)
      const message = error.response?.data?.detail || 'Error al guardar la configuración general'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSaving.value = false
    }
  }
  
  const saveAISettings = async (settings) => {
    try {
      isSaving.value = true
      
      const response = await axios.put('/api/v1/settings/ai', settings)
      
      aiSettings.value = { ...aiSettings.value, ...response.data }
      
      toast.success('Configuración de IA guardada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Save AI settings error:', error)
      const message = error.response?.data?.detail || 'Error al guardar la configuración de IA'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSaving.value = false
    }
  }
  
  const saveSecuritySettings = async (settings) => {
    try {
      isSaving.value = true
      
      const response = await axios.put('/api/v1/settings/security', settings)
      
      securitySettings.value = { ...securitySettings.value, ...response.data }
      
      toast.success('Configuración de seguridad guardada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Save security settings error:', error)
      const message = error.response?.data?.detail || 'Error al guardar la configuración de seguridad'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSaving.value = false
    }
  }
  
  const saveEmailSettings = async (settings) => {
    try {
      isSaving.value = true
      
      const response = await axios.put('/api/v1/settings/email', settings)
      
      emailSettings.value = { ...emailSettings.value, ...response.data }
      
      toast.success('Configuración de email guardada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Save email settings error:', error)
      const message = error.response?.data?.detail || 'Error al guardar la configuración de email'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSaving.value = false
    }
  }
  
  const saveStorageSettings = async (settings) => {
    try {
      isSaving.value = true
      
      const response = await axios.put('/api/v1/settings/storage', settings)
      
      storageSettings.value = { ...storageSettings.value, ...response.data }
      
      toast.success('Configuración de almacenamiento guardada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Save storage settings error:', error)
      const message = error.response?.data?.detail || 'Error al guardar la configuración de almacenamiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSaving.value = false
    }
  }
  
  const testEmailConnection = async () => {
    try {
      isTesting.value = true
      
      const response = await axios.post('/api/v1/settings/email/test', {
        ...emailSettings.value
      })
      
      if (response.data.success) {
        toast.success('Conexión de email probada exitosamente')
      } else {
        toast.error('Error en la conexión de email')
      }
      
      return { success: response.data.success, data: response.data }
    } catch (error) {
      console.error('Test email connection error:', error)
      const message = error.response?.data?.detail || 'Error al probar la conexión de email'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isTesting.value = false
    }
  }
  
  const testAIConnection = async (provider = null) => {
    try {
      isTesting.value = true
      
      const testProvider = provider || aiSettings.value.default_model
      
      const response = await axios.post('/api/v1/settings/ai/test', {
        provider: testProvider,
        ...aiSettings.value
      })
      
      if (response.data.success) {
        toast.success(`Conexión con ${testProvider} probada exitosamente`)
      } else {
        toast.error(`Error en la conexión con ${testProvider}`)
      }
      
      return { success: response.data.success, data: response.data }
    } catch (error) {
      console.error('Test AI connection error:', error)
      const message = error.response?.data?.detail || 'Error al probar la conexión de IA'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isTesting.value = false
    }
  }
  
  const testStorageConnection = async () => {
    try {
      isTesting.value = true
      
      const response = await axios.post('/api/v1/settings/storage/test', {
        ...storageSettings.value
      })
      
      if (response.data.success) {
        toast.success('Conexión de almacenamiento probada exitosamente')
      } else {
        toast.error('Error en la conexión de almacenamiento')
      }
      
      return { success: response.data.success, data: response.data }
    } catch (error) {
      console.error('Test storage connection error:', error)
      const message = error.response?.data?.detail || 'Error al probar la conexión de almacenamiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isTesting.value = false
    }
  }
  
  const fetchStorageUsage = async () => {
    try {
      const response = await axios.get('/api/v1/settings/storage/usage')
      
      storageUsage.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch storage usage error:', error)
      const message = error.response?.data?.detail || 'Error al cargar el uso de almacenamiento'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const cleanupStorage = async (options = {}) => {
    try {
      const response = await axios.post('/api/v1/settings/storage/cleanup', options)
      
      // Refresh storage usage after cleanup
      await fetchStorageUsage()
      
      toast.success('Limpieza de almacenamiento completada')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Cleanup storage error:', error)
      const message = error.response?.data?.detail || 'Error al limpiar el almacenamiento'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const exportSettings = async (sections = []) => {
    try {
      const params = sections.length > 0 ? { sections: sections.join(',') } : {}
      
      const response = await axios.get('/api/v1/settings/export', {
        params,
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'settings_backup.json')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Configuraciones exportadas exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Export settings error:', error)
      const message = error.response?.data?.detail || 'Error al exportar las configuraciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const importSettings = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post('/api/v1/settings/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Refresh all settings after import
      await fetchAllSettings()
      
      toast.success('Configuraciones importadas exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Import settings error:', error)
      const message = error.response?.data?.detail || 'Error al importar las configuraciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const resetSettings = async (section) => {
    try {
      const response = await axios.post(`/api/v1/settings/${section}/reset`)
      
      // Update local state with reset values
      switch (section) {
        case 'general':
          generalSettings.value = { ...generalSettings.value, ...response.data }
          break
        case 'ai':
          aiSettings.value = { ...aiSettings.value, ...response.data }
          break
        case 'security':
          securitySettings.value = { ...securitySettings.value, ...response.data }
          break
        case 'email':
          emailSettings.value = { ...emailSettings.value, ...response.data }
          break
        case 'storage':
          storageSettings.value = { ...storageSettings.value, ...response.data }
          break
      }
      
      toast.success(`Configuración de ${section} restablecida a valores por defecto`)
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Reset settings error:', error)
      const message = error.response?.data?.detail || 'Error al restablecer las configuraciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  // Utility functions
  const updateGeneralSettings = (updates) => {
    generalSettings.value = { ...generalSettings.value, ...updates }
  }
  
  const updateAISettings = (updates) => {
    aiSettings.value = { ...aiSettings.value, ...updates }
  }
  
  const updateSecuritySettings = (updates) => {
    securitySettings.value = { ...securitySettings.value, ...updates }
  }
  
  const updateEmailSettings = (updates) => {
    emailSettings.value = { ...emailSettings.value, ...updates }
  }
  
  const updateStorageSettings = (updates) => {
    storageSettings.value = { ...storageSettings.value, ...updates }
  }
  
  const refreshAllSettings = async () => {
    return await fetchAllSettings()
  }

  return {
    // State
    generalSettings,
    aiSettings,
    securitySettings,
    emailSettings,
    storageSettings,
    storageUsage,
    isLoading,
    isSaving,
    isTesting,
    
    // Getters
    isMaintenanceMode,
    isRegistrationEnabled,
    storageUsagePercentage,
    isStorageNearLimit,
    formattedStorageSize,
    hasValidEmailConfig,
    hasValidAIConfig,
    
    // Actions
    fetchAllSettings,
    saveGeneralSettings,
    saveAISettings,
    saveSecuritySettings,
    saveEmailSettings,
    saveStorageSettings,
    testEmailConnection,
    testAIConnection,
    testStorageConnection,
    fetchStorageUsage,
    cleanupStorage,
    exportSettings,
    importSettings,
    resetSettings,
    
    // Utilities
    updateGeneralSettings,
    updateAISettings,
    updateSecuritySettings,
    updateEmailSettings,
    updateStorageSettings,
    refreshAllSettings
  }
})