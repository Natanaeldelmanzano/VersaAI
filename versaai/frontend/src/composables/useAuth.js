// VersaAI Authentication Composable
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/config/api'
import { useToast } from 'vue-toastification'

// Global state
const user = ref(null)
const isAuthenticated = ref(false)
const isLoading = ref(false)
const token = ref(localStorage.getItem('access_token'))

// Initialize authentication state
if (token.value) {
  isAuthenticated.value = true
}

export function useAuth() {
  const router = useRouter()
  const toast = useToast()

  // Computed properties
  const isLoggedIn = computed(() => isAuthenticated.value && user.value !== null)
  const userRole = computed(() => user.value?.role || 'user')
  const userName = computed(() => user.value?.name || user.value?.email || 'Usuario')
  const userEmail = computed(() => user.value?.email || '')

  // Watch token changes
  watch(token, (newToken) => {
    if (newToken) {
      localStorage.setItem('access_token', newToken)
      isAuthenticated.value = true
    } else {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      isAuthenticated.value = false
      user.value = null
    }
  })

  // Login function
  const login = async (credentials) => {
    try {
      isLoading.value = true
      const response = await api.auth.login(credentials)
      
      if (response.data.access_token) {
        token.value = response.data.access_token
        
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token)
        }
        
        // Get user profile
        await getCurrentUser()
        
        toast.success('¡Bienvenido a VersaAI!')
        return { success: true, user: user.value }
      }
    } catch (error) {
      console.error('Login error:', error)
      const message = error.response?.data?.detail || 'Error al iniciar sesión'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Register function
  const register = async (userData) => {
    try {
      isLoading.value = true
      const response = await api.auth.register(userData)
      
      if (response.data.access_token) {
        token.value = response.data.access_token
        
        if (response.data.refresh_token) {
          localStorage.setItem('refresh_token', response.data.refresh_token)
        }
        
        // Get user profile
        await getCurrentUser()
        
        toast.success('¡Cuenta creada exitosamente!')
        return { success: true, user: user.value }
      }
    } catch (error) {
      console.error('Register error:', error)
      const message = error.response?.data?.detail || 'Error al crear la cuenta'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Logout function
  const logout = async () => {
    try {
      await api.auth.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      isAuthenticated.value = false
      toast.info('Sesión cerrada')
      router.push('/login')
    }
  }

  // Get current user
  const getCurrentUser = async () => {
    try {
      if (!token.value) return null
      
      const response = await api.auth.me()
      user.value = response.data
      return user.value
    } catch (error) {
      console.error('Get user error:', error)
      if (error.response?.status === 401) {
        // Token is invalid, logout
        await logout()
      }
      return null
    }
  }

  // Refresh token
  const refreshToken = async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refresh_token')
      if (!refreshTokenValue) {
        throw new Error('No refresh token available')
      }
      
      const response = await api.auth.refreshToken(refreshTokenValue)
      token.value = response.data.access_token
      
      if (response.data.refresh_token) {
        localStorage.setItem('refresh_token', response.data.refresh_token)
      }
      
      return true
    } catch (error) {
      console.error('Refresh token error:', error)
      await logout()
      return false
    }
  }

  // Update user profile
  const updateProfile = async (profileData) => {
    try {
      isLoading.value = true
      const response = await api.users.updateProfile(profileData)
      user.value = { ...user.value, ...response.data }
      toast.success('Perfil actualizado correctamente')
      return { success: true, user: user.value }
    } catch (error) {
      console.error('Update profile error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar el perfil'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  // Change password
  const changePassword = async (passwordData) => {
    try {
      isLoading.value = true
      await api.users.changePassword(passwordData)
      toast.success('Contraseña cambiada correctamente')
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

  // Check if user has permission
  const hasPermission = (permission) => {
    if (!user.value) return false
    if (user.value.role === 'admin') return true
    return user.value.permissions?.includes(permission) || false
  }

  // Initialize auth state on app start
  const initializeAuth = async () => {
    if (token.value) {
      await getCurrentUser()
    }
  }

  return {
    // State
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    isLoading: computed(() => isLoading.value),
    isLoggedIn,
    userRole,
    userName,
    userEmail,
    
    // Methods
    login,
    register,
    logout,
    getCurrentUser,
    refreshToken,
    updateProfile,
    changePassword,
    hasPermission,
    initializeAuth
  }
}

// Export for global access
export { user, isAuthenticated, isLoading }

// Alias para compatibilidad
export const useSession = useAuth