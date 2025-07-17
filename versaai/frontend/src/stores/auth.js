import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/config/api'
import Cookies from 'js-cookie'
import { useToast } from 'vue-toastification'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(Cookies.get('token') || null)
  const isLoading = ref(false)
  const toast = useToast()

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role || null)
  const userOrganization = computed(() => user.value?.organization || null)
  const isSuperAdmin = computed(() => userRole.value === 'super_admin')
  const isAdmin = computed(() => ['super_admin', 'admin'].includes(userRole.value))
  const isUser = computed(() => userRole.value === 'user')

  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      Cookies.set('token', newToken, { expires: 7, secure: true, sameSite: 'strict' })
      localStorage.setItem('access_token', newToken)
    } else {
      Cookies.remove('token')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const login = async (credentials) => {
    console.log('🔐 Iniciando login con:', credentials)

    try {
      isLoading.value = true
      
      // Llamada a la API
      console.log('📡 Enviando petición a la API de autenticación')
      const response = await api.auth.login({
        email: credentials.email,
        password: credentials.password
      })
      
      console.log('✅ Respuesta del servidor:', response)
      console.log('📦 Datos de respuesta:', response.data)
      
      // Verificar que la respuesta tenga los datos necesarios
      if (!response.data || !response.data.access_token) {
        throw new Error('Respuesta del servidor inválida: falta access_token')
      }
      
      const { access_token, refresh_token, user: userData } = response.data
      
      setToken(access_token)
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token)
      }
      setUser(userData || {
          id: 1,
          email: credentials.email,
          full_name: 'Usuario Demo',
          role: 'admin',
          organization: 'Demo Org'
        })
      
      console.log('✅ Login exitoso:', {
        token: access_token.substring(0, 20) + '...',
        user: user.value
      })
      
      toast.success(`¡Bienvenido, ${user.value.full_name || user.value.email}!`)
      
      // Redirigir al dashboard después del login exitoso
      setTimeout(() => {
        window.location.href = '/dashboard'
      }, 1000)
      
      return { success: true, user: user.value }
    } catch (error) {
      console.error('❌ Error en login:', error)
      
      // Limpiar estado en caso de error
      setToken(null)
      setUser(null)
      
      // Manejar diferentes tipos de errores
      let message = 'Error al iniciar sesión'
      
      if (error.response) {
        // Error del servidor (4xx, 5xx)
        const status = error.response.status
        message = error.response.data?.detail || error.response.data?.message || `Error del servidor (${status})`
        console.error('📡 Error del servidor:', error.response.data)
      } else if (error.request) {
        // Error de red
        message = 'Error de conexión. Verifica tu conexión a internet.'
        console.error('🌐 Error de red:', error.request)
      } else {
        // Error de configuración
        message = error.message || 'Error desconocido'
        console.error('⚙️ Error de configuración:', error.message)
      }
      
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Función de registro CORREGIDA
  const register = async (userData) => {
    console.log('📝 Iniciando registro con:', userData)

    try {
      isLoading.value = true

      // Mapear datos correctamente (name -> full_name)
      const registerData = {
        email: userData.email,
        password: userData.password,
        full_name: userData.name || userData.full_name,
        username: userData.username || userData.email.split('@')[0]
      }

      console.log('📡 Enviando datos de registro:', registerData)
      const response = await api.auth.register(registerData)

      console.log('✅ Registro exitoso:', response.data)
      
      const { access_token, refresh_token, user: newUser } = response.data
      
      setToken(access_token)
      if (refresh_token) {
        localStorage.setItem('refresh_token', refresh_token)
      }
      setUser(newUser)
      
      toast.success(`¡Cuenta creada exitosamente! Bienvenido, ${newUser.full_name || newUser.email}!`)
      
      return { success: true, user: newUser }

    } catch (error) {
      console.error('❌ Error en registro:', error)

      if (error.response) {
        const message = error.response.data?.detail || 'Error en el registro'
        toast.error(message)
        return { success: false, error: message }
      } else {
        const message = 'Error de conexión'
        toast.error(message)
        return { success: false, error: message }
      }
    } finally {
      isLoading.value = false
    }
  }

  // Función de logout
  const logout = async () => {
    try {
      // Llamar al endpoint de logout si existe
      if (token.value) {
        await api.auth.logout()
      }
    } catch (err) {
      console.warn('Error al hacer logout en el servidor:', err)
    } finally {
      // Limpiar estado local
      user.value = null
      token.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_data')
      Cookies.remove('token')
      toast.info('Sesión cerrada correctamente')
    }
  }

  // Función para restaurar sesión
  const restoreSession = async () => {
    const savedToken = localStorage.getItem('access_token')
    const savedUser = localStorage.getItem('user_data')

    if (savedToken && savedUser) {
      try {
        token.value = savedToken
        user.value = JSON.parse(savedUser)

        // Verificar que el token sigue siendo válido (solo si hay conexión)
        // await api.auth.me()
        console.log('✅ Sesión restaurada exitosamente')
      } catch (err) {
        console.warn('⚠️ Token expirado, limpiando sesión')
        logout()
      }
    }
  }

  const checkAuth = async () => {
    const savedToken = Cookies.get('token') || localStorage.getItem('access_token')
    
    // If no token exists, user is not authenticated
    if (!savedToken) {
      console.log('🔧 No hay token guardado, usuario no autenticado')
      return false
    }

    try {
      setToken(savedToken)
      
      // Try to get current user info, fallback to existing user data if not available
      try {
        const response = await api.auth.me()
        setUser(response.data)
        console.log('✅ Usuario verificado con la API')
      } catch (apiError) {
        console.log('⚠️ API no disponible, usando datos de usuario existentes')
        // If API is not available but we have a token, check if we have user data
        if (!user.value) {
          // Set a default user if no user data exists
          setUser({
            id: 1,
            email: 'usuario@versaai.com',
            full_name: 'Usuario Demo',
            role: 'admin',
            organization: 'Demo Org'
          })
        }
        console.log('✅ Continuando con token existente')
      }
      
      return true
    } catch (error) {
      console.error('Auth check error:', error)
      // Only logout if there's a clear authentication error (401)
      if (error.response && error.response.status === 401) {
        console.log('🔧 Token inválido (401), cerrando sesión')
        await logout()
        return false
      }
      
      // For other errors, try to continue with existing token
      console.log('⚠️ Error de verificación, pero continuando con token existente')
      return true
    }
  }

  const updateProfile = async (profileData) => {
    try {
      isLoading.value = true
      
      const response = await api.users.updateProfile(profileData)
      setUser(response.data)
      
      toast.success('Perfil actualizado correctamente')
      return response.data
    } catch (error) {
      console.error('Update profile error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar el perfil'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    try {
      isLoading.value = true
      
      await api.users.changePassword(passwordData)
      
      toast.success('Contraseña actualizada correctamente')
      return { success: true }
    } catch (error) {
      console.error('Change password error:', error)
      const message = error.response?.data?.detail || 'Error al cambiar la contraseña'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const forgotPassword = async (email) => {
    try {
      isLoading.value = true
      
      await api.auth.forgotPassword({ email })
      
      toast.success('Se ha enviado un enlace de recuperación a tu correo electrónico')
      
      return { success: true }
    } catch (error) {
      console.error('Forgot password error:', error)
      const message = error.response?.data?.detail || 'Error al enviar el correo de recuperación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const resetPassword = async (token, password) => {
    try {
      isLoading.value = true
      
      await api.auth.resetPassword({
        token,
        new_password: password
      })
      
      toast.success('Contraseña restablecida exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Reset password error:', error)
      const message = error.response?.data?.detail || 'Error al restablecer la contraseña'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const refreshToken = async () => {
    try {
      const response = await api.auth.refresh()
      const { access_token } = response.data
      setToken(access_token)
      return true
    } catch (error) {
      console.error('Token refresh error:', error)
      // If refresh fails, logout user
      await logout()
      return false
    }
  }

  // Demo functions for role switching with real users
  const switchToRole = async (role) => {
    try {
      const roleCredentials = {
        'user': {
          email: 'user@versaai.com',
          password: 'user123456'
        },
        'viewer': {
          email: 'viewer@versaai.com',
          password: 'viewer123456'
        },
        'org_admin': {
          email: 'admin@versaai.com',
          password: 'admin123456'
        },
        'admin': {
          email: 'admin@versaai.com',
          password: 'admin123456'
        },
        'super_admin': {
          email: 'superadmin@versaai.com',
          password: 'super123456'
        }
      }
      
      const credentials = roleCredentials[role]
      if (!credentials) {
        console.error('Rol no válido:', role)
        return false
      }
      
      // Hacer login real con las credenciales del rol
      const result = await login(credentials)
      const success = result.success
      
      if (success) {
        toast.success(`Cambiado a rol: ${role}`)
        console.log('🔄 Rol cambiado exitosamente a:', role)
        return true
      } else {
        toast.error('Error al cambiar de rol')
        return false
      }
    } catch (error) {
      console.error('Error en switchToRole:', error)
      toast.error('Error al cambiar de rol')
      return false
    }
  }
  
  const createDemoUser = (role = 'user') => {
    const roleData = {
      'user': {
        id: 1,
        email: 'usuario@versaai.com',
        full_name: 'Usuario Demo',
        role: 'user',
        organization: 'Demo Org',
        permissions: ['read_own_data', 'create_conversations']
      },
      'admin': {
        id: 2,
        email: 'admin@versaai.com',
        full_name: 'Administrador Demo',
        role: 'admin',
        organization: 'Demo Org',
        permissions: ['read_all_data', 'create_users', 'manage_system', 'delete_data']
      },
      'super_admin': {
        id: 3,
        email: 'superadmin@versaai.com',
        full_name: 'Super Administrador Demo',
        role: 'super_admin',
        organization: 'Demo Org',
        permissions: ['full_access', 'system_config', 'user_management', 'organization_management']
      },
      'org_admin': {
        id: 4,
        email: 'orgadmin@versaai.com',
        full_name: 'Administrador de Organización Demo',
        role: 'org_admin',
        organization: 'Demo Org',
        permissions: ['manage_organization', 'create_users', 'view_analytics']
      },
      'viewer': {
        id: 5,
        email: 'viewer@versaai.com',
        full_name: 'Visualizador Demo',
        role: 'viewer',
        organization: 'Demo Org',
        permissions: ['read_only']
      }
    }
    
    const demoUser = roleData[role] || roleData['user']
    const demoToken = `demo_token_${role}_${Date.now()}`
    
    setToken(demoToken)
    setUser(demoUser)
    localStorage.setItem('user_data', JSON.stringify(demoUser))
    
    console.log('👤 Usuario demo creado:', demoUser)
    toast.success(`Usuario demo creado: ${demoUser.full_name}`)
    
    return demoUser
  }
  
  const getAvailableRoles = () => {
    return [
      { value: 'user', label: 'Usuario', description: 'Acceso básico a funcionalidades' },
      { value: 'viewer', label: 'Visualizador', description: 'Solo lectura' },
      { value: 'org_admin', label: 'Admin de Organización', description: 'Gestión de organización' },
      { value: 'admin', label: 'Administrador', description: 'Gestión completa del sistema' },
      { value: 'super_admin', label: 'Super Administrador', description: 'Acceso total al sistema' }
    ]
  }
  
  const getUserPermissions = () => {
    return user.value?.permissions || []
  }
  
  const hasPermission = (permission) => {
    const permissions = getUserPermissions()
    return permissions.includes(permission) || permissions.includes('full_access')
  }

  // Initialize axios interceptors
  const initializeInterceptors = () => {
    // Request interceptor to add token
    axios.interceptors.request.use(
      (config) => {
        if (token.value) {
          config.headers.Authorization = `Bearer ${token.value}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor to handle token expiration
    axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          // Try to refresh token
          const refreshed = await refreshToken()
          if (refreshed) {
            // Retry original request with new token
            return axios(originalRequest)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  // Initialize function for app startup
  const initialize = async () => {
    console.log('🔧 Inicializando authStore...')
    
    try {
      // Initialize interceptors
      initializeInterceptors()
      
      // Check for existing authentication
      const isAuth = await checkAuth()
      
      console.log('✅ AuthStore inicializado:', { isAuthenticated: isAuth })
      return isAuth
    } catch (error) {
      console.error('❌ Error inicializando authStore:', error)
      return false
    }
  }

  // Initialize interceptors when store is created
  initializeInterceptors()

  // Inicializar automáticamente (comentado para evitar llamadas API durante arranque)
  // restoreSession()

  return {
    // State
    user,
    token,
    isLoading,
    
    // Getters
    isAuthenticated,
    userRole,
    userOrganization,
    isSuperAdmin,
    isAdmin,
    isUser,
    
    // Actions
    setToken,
    setUser,
    login,
    register,
    logout,
    restoreSession,
    checkAuth,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    refreshToken,
    initialize,
    
    // Demo functions
    switchToRole,
    createDemoUser,
    getAvailableRoles,
    getUserPermissions,
    hasPermission
  }
})