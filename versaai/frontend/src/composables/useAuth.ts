import { computed, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import type { LoginData, RegisterData, ForgotPasswordData, ResetPasswordData, ChangePasswordData, UpdateProfileData } from '@/utils/validation'

/**
 * Composable para manejar la autenticación de manera reactiva
 * Proporciona métodos y estado para login, registro, logout, etc.
 */
export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()
  const toast = useToast()

  // Estado local
  const isProcessing = ref(false)
  const lastError = ref<string | null>(null)

  // Computed properties
  const user = computed(() => authStore.user)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isLoading = computed(() => authStore.isLoading || isProcessing.value)
  const userRole = computed(() => authStore.userRole)
  const userPermissions = computed(() => authStore.userPermissions)
  const isAdmin = computed(() => authStore.isAdmin)
  const isModerator = computed(() => authStore.isModerator)
  const userInitials = computed(() => authStore.userInitials)
  const lastActivity = computed(() => authStore.lastActivity)

  // Métodos de autenticación
  const login = async (credentials: LoginData, redirectTo?: string): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.login(credentials)
      
      toast.success(`¡Bienvenido de vuelta, ${authStore.user?.name}!`)
      
      // Redirigir después del login exitoso
      const targetRoute = redirectTo || '/dashboard'
      await router.push(targetRoute)
      
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al iniciar sesión'
      
      // Manejar diferentes tipos de errores
      if (error.response?.status === 401) {
        toast.error('Credenciales incorrectas')
      } else if (error.response?.status === 423) {
        toast.error('Cuenta bloqueada. Contacta al administrador')
      } else if (error.response?.status === 429) {
        toast.error('Demasiados intentos. Intenta más tarde')
      } else {
        toast.error('Error al iniciar sesión. Intenta nuevamente')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const register = async (userData: RegisterData, redirectTo?: string): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.register(userData)
      
      toast.success(`¡Cuenta creada exitosamente! Bienvenido, ${authStore.user?.name}!`)
      
      // Redirigir después del registro exitoso
      const targetRoute = redirectTo || '/dashboard'
      await router.push(targetRoute)
      
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al crear la cuenta'
      
      // Manejar errores específicos
      if (error.response?.status === 422) {
        const errors = error.response.data.errors
        if (errors?.email) {
          toast.error('Este email ya está registrado')
        } else {
          toast.error('Datos inválidos. Verifica la información')
        }
      } else if (error.response?.status === 409) {
        toast.error('Este email ya está registrado')
      } else {
        toast.error('Error al crear la cuenta. Intenta nuevamente')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const logout = async (showMessage = true): Promise<void> => {
    try {
      isProcessing.value = true
      
      await authStore.logout()
      
      if (showMessage) {
        toast.info('Sesión cerrada correctamente')
      }
      
      // Redirigir al login
      await router.push('/auth/login')
    } catch (error: any) {
      console.error('Error al cerrar sesión:', error)
      // Forzar logout local aunque falle el servidor
      authStore.$reset()
      await router.push('/auth/login')
    } finally {
      isProcessing.value = false
    }
  }

  const forgotPassword = async (data: ForgotPasswordData): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.forgotPassword(data)
      
      toast.success('Se ha enviado un enlace de recuperación a tu email')
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al enviar email de recuperación'
      
      if (error.response?.status === 404) {
        toast.error('No se encontró una cuenta con este email')
      } else if (error.response?.status === 429) {
        toast.error('Demasiados intentos. Intenta más tarde')
      } else {
        toast.error('Error al enviar email de recuperación')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const resetPassword = async (data: ResetPasswordData): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.resetPassword(data)
      
      toast.success('Contraseña restablecida exitosamente')
      
      // Redirigir al login
      await router.push('/auth/login')
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al restablecer contraseña'
      
      if (error.response?.status === 400) {
        toast.error('Token inválido o expirado')
      } else if (error.response?.status === 422) {
        toast.error('Datos inválidos')
      } else {
        toast.error('Error al restablecer contraseña')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const changePassword = async (data: ChangePasswordData): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.changePassword(data)
      
      toast.success('Contraseña cambiada exitosamente')
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al cambiar contraseña'
      
      if (error.response?.status === 400) {
        toast.error('Contraseña actual incorrecta')
      } else if (error.response?.status === 422) {
        toast.error('Nueva contraseña inválida')
      } else {
        toast.error('Error al cambiar contraseña')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const updateProfile = async (data: UpdateProfileData): Promise<boolean> => {
    try {
      isProcessing.value = true
      lastError.value = null

      await authStore.updateProfile(data)
      
      toast.success('Perfil actualizado exitosamente')
      return true
    } catch (error: any) {
      lastError.value = error.message || 'Error al actualizar perfil'
      
      if (error.response?.status === 422) {
        const errors = error.response.data.errors
        if (errors?.email) {
          toast.error('Este email ya está en uso')
        } else {
          toast.error('Datos inválidos')
        }
      } else {
        toast.error('Error al actualizar perfil')
      }
      
      return false
    } finally {
      isProcessing.value = false
    }
  }

  const checkAuth = async (): Promise<boolean> => {
    try {
      await authStore.checkAuth()
      return authStore.isAuthenticated
    } catch (error) {
      console.error('Error al verificar autenticación:', error)
      return false
    }
  }

  const refreshToken = async (): Promise<boolean> => {
    try {
      await authStore.refreshToken()
      return true
    } catch (error) {
      console.error('Error al refrescar token:', error)
      // Si falla el refresh, hacer logout
      await logout(false)
      return false
    }
  }

  // Utilidades
  const hasPermission = (permission: string): boolean => {
    return authStore.hasPermission(permission)
  }

  const hasRole = (role: string): boolean => {
    return authStore.hasRole(role)
  }

  const requireAuth = async (redirectTo = '/auth/login'): Promise<boolean> => {
    if (!isAuthenticated.value) {
      await router.push(redirectTo)
      return false
    }
    return true
  }

  const requireRole = async (role: string, redirectTo = '/unauthorized'): Promise<boolean> => {
    if (!hasRole(role)) {
      await router.push(redirectTo)
      return false
    }
    return true
  }

  const requirePermission = async (permission: string, redirectTo = '/unauthorized'): Promise<boolean> => {
    if (!hasPermission(permission)) {
      await router.push(redirectTo)
      return false
    }
    return true
  }

  // Watchers para monitoreo de sesión
  watch(
    () => authStore.lastActivity,
    (newActivity) => {
      if (newActivity && isAuthenticated.value) {
        const now = Date.now()
        const lastActivity = new Date(newActivity).getTime()
        const timeDiff = now - lastActivity
        
        // Si han pasado más de 30 minutos sin actividad, mostrar advertencia
        if (timeDiff > 30 * 60 * 1000) {
          toast.warning('Tu sesión expirará pronto por inactividad')
        }
        
        // Si han pasado más de 60 minutos, hacer logout automático
        if (timeDiff > 60 * 60 * 1000) {
          logout(true)
          toast.error('Sesión expirada por inactividad')
        }
      }
    },
    { immediate: true }
  )

  // Limpiar errores cuando cambie el estado de autenticación
  watch(isAuthenticated, () => {
    lastError.value = null
  })

  return {
    // Estado
    user,
    isAuthenticated,
    isLoading,
    isProcessing: computed(() => isProcessing.value),
    lastError: computed(() => lastError.value),
    userRole,
    userPermissions,
    isAdmin,
    isModerator,
    userInitials,
    lastActivity,

    // Métodos de autenticación
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    changePassword,
    updateProfile,
    checkAuth,
    refreshToken,

    // Utilidades
    hasPermission,
    hasRole,
    requireAuth,
    requireRole,
    requirePermission,

    // Métodos para limpiar estado
    clearError: () => { lastError.value = null },
    clearProcessing: () => { isProcessing.value = false }
  }
}

/**
 * Composable específico para guards de rutas
 */
export function useAuthGuards() {
  const { isAuthenticated, hasRole, hasPermission, checkAuth } = useAuth()
  const router = useRouter()

  const authGuard = async (to: any, from: any, next: any) => {
    // Verificar autenticación
    const isAuth = await checkAuth()
    
    if (!isAuth) {
      // Guardar la ruta a la que quería acceder
      const redirectTo = to.fullPath !== '/auth/login' ? to.fullPath : undefined
      next({
        path: '/auth/login',
        query: redirectTo ? { redirect: redirectTo } : undefined
      })
      return
    }
    
    next()
  }

  const roleGuard = (requiredRole: string) => {
    return async (to: any, from: any, next: any) => {
      if (!hasRole(requiredRole)) {
        next('/unauthorized')
        return
      }
      next()
    }
  }

  const permissionGuard = (requiredPermission: string) => {
    return async (to: any, from: any, next: any) => {
      if (!hasPermission(requiredPermission)) {
        next('/unauthorized')
        return
      }
      next()
    }
  }

  const guestGuard = async (to: any, from: any, next: any) => {
    const isAuth = await checkAuth()
    
    if (isAuth) {
      // Si ya está autenticado, redirigir al dashboard
      next('/dashboard')
      return
    }
    
    next()
  }

  return {
    authGuard,
    roleGuard,
    permissionGuard,
    guestGuard
  }
}

/**
 * Composable para manejo de sesiones
 */
export function useSession() {
  const { refreshToken, logout, isAuthenticated } = useAuth()
  
  let refreshInterval: NodeJS.Timeout | null = null
  let activityTimeout: NodeJS.Timeout | null = null

  const startSessionMonitoring = () => {
    // Refrescar token cada 15 minutos
    refreshInterval = setInterval(async () => {
      if (isAuthenticated.value) {
        await refreshToken()
      }
    }, 15 * 60 * 1000)

    // Monitorear actividad del usuario
    const resetActivityTimer = () => {
      if (activityTimeout) {
        clearTimeout(activityTimeout)
      }
      
      // Logout automático después de 60 minutos de inactividad
      activityTimeout = setTimeout(() => {
        logout(true)
      }, 60 * 60 * 1000)
    }

    // Eventos que indican actividad del usuario
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart']
    
    activityEvents.forEach(event => {
      document.addEventListener(event, resetActivityTimer, true)
    })

    // Inicializar timer
    resetActivityTimer()
  }

  const stopSessionMonitoring = () => {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
    
    if (activityTimeout) {
      clearTimeout(activityTimeout)
      activityTimeout = null
    }

    // Remover event listeners
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart']
    activityEvents.forEach(event => {
      document.removeEventListener(event, () => {}, true)
    })
  }

  return {
    startSessionMonitoring,
    stopSessionMonitoring
  }
}

export default useAuth