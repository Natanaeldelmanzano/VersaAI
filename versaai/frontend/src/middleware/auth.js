// frontend/src/middleware/auth.js
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

/**
 * Middleware de autenticación simplificado para resolver problemas de autorización
 */

export const requireAuth = () => {
  const authStore = useAuthStore()
  const router = useRouter()

  if (!authStore.isAuthenticated) {
    console.warn('🔒 Usuario no autenticado, redirigiendo a login')
    router.push('/login')
    return false
  }

  return true
}

export const requireRole = (requiredRole) => {
  const authStore = useAuthStore()
  const router = useRouter()

  if (!authStore.isAuthenticated) {
    console.warn('🔒 Usuario no autenticado, redirigiendo a login')
    router.push('/login')
    return false
  }

  const userRole = authStore.userRole || authStore.user?.role || 'user'
  const roleHierarchy = {
    'user': 1,
    'moderator': 2,
    'admin': 3,
    'super_admin': 4
  }

  const userLevel = roleHierarchy[userRole] || 0
  const requiredLevel = roleHierarchy[requiredRole] || 0

  if (userLevel < requiredLevel) {
    console.warn(`🚫 Acceso denegado. Requerido: ${requiredRole}, Usuario: ${userRole}`)
    router.push('/unauthorized')
    return false
  }

  return true
}

// Middleware para rutas de Vue Router
// Nuevo authGuard mejorado para resolver errores 401
export const authGuard = (to, from, next) => {
  const authStore = useAuthStore()
  const token = authStore.token || localStorage.getItem('auth_token')

  if (!token) {
    // Redirigir a login si no hay token
    next('/login')
    return
  }

  // Verificar si el token es válido
  if (authStore.isTokenExpired && authStore.isTokenExpired(token)) {
    authStore.logout()
    next('/login')
    return
  }

  // Verificar permisos específicos por ruta
  const requiredRole = to.meta.requiresRole
  if (requiredRole && !authStore.hasRole(requiredRole)) {
    // En lugar de mostrar 401, redirigir al dashboard
    next('/dashboard')
    return
  }

  next()
}

// Función para manejar rutas protegidas
export const roleGuard = (requiredRole) => {
  return (to, from, next) => {
    const authStore = useAuthStore()

    if (!authStore.isAuthenticated) {
      next('/login')
      return
    }

    if (!authStore.hasRole(requiredRole)) {
      // Mostrar mensaje amigable en lugar de 401
      if (authStore.setError) {
        authStore.setError(`Necesitas permisos de ${requiredRole} para acceder a esta página`)
      }
      next('/dashboard')
      return
    }

    next()
  }
}

export const authMiddleware = {
  beforeEnter: async (to, from, next) => {
    const authStore = useAuthStore()

    try {
      // Inicializar el store si no está inicializado
      if (typeof authStore.initialize === 'function') {
        await authStore.initialize()
      }

      // Usar el nuevo authGuard
      if (to.meta.requiresAuth) {
        authGuard(to, from, next)
        return
      }

      // Verificar roles específicos usando roleGuard
      if (to.meta.requiredRole) {
        const guard = roleGuard(to.meta.requiredRole)
        guard(to, from, next)
        return
      }

      // Verificar si es una ruta de invitado (login, register) y el usuario ya está autenticado
      if (to.meta.guestOnly && authStore.isAuthenticated) {
        console.log('👤 Usuario ya autenticado, redirigiendo a dashboard')
        next('/dashboard')
        return
      }

      next()
    } catch (error) {
      console.error('❌ Error en middleware de autenticación:', error)
      // En caso de error, redirigir al dashboard en lugar de mostrar 401
      next('/dashboard')
    }
  }
}

// Guards específicos para roles comunes
export const adminGuard = {
  beforeEnter: (to, from, next) => {
    if (requireRole('admin')) {
      next()
    }
  }
}

export const moderatorGuard = {
  beforeEnter: (to, from, next) => {
    if (requireRole('moderator')) {
      next()
    }
  }
}

export const userGuard = {
  beforeEnter: (to, from, next) => {
    if (requireAuth()) {
      next()
    }
  }
}

// Composable para usar en componentes
export const useAuthGuard = () => {
  const authStore = useAuthStore()
  const router = useRouter()

  const checkAuth = () => {
    if (!authStore.isAuthenticated) {
      console.warn('🔒 Usuario no autenticado')
      router.push('/login')
      throw new Error('Usuario no autenticado')
    }
    return true
  }

  const checkRole = (role) => {
    checkAuth()
    if (!requireRole(role)) {
      throw new Error(`Rol insuficiente: se requiere ${role}`)
    }
    return true
  }

  const hasPermission = (permission) => {
    if (!authStore.isAuthenticated) return false
    
    const userPermissions = authStore.user?.permissions || []
    return userPermissions.includes(permission)
  }

  const canAccess = (requiredRole = null, requiredPermission = null) => {
    if (!authStore.isAuthenticated) return false
    
    if (requiredRole && !requireRole(requiredRole)) return false
    if (requiredPermission && !hasPermission(requiredPermission)) return false
    
    return true
  }

  return {
    checkAuth,
    checkRole,
    hasPermission,
    canAccess,
    isAuthenticated: authStore.isAuthenticated,
    userRole: authStore.userRole || authStore.user?.role || 'user',
    user: authStore.user
  }
}

// Función helper para verificar autenticación en cualquier lugar
export const isAuthenticated = () => {
  const authStore = useAuthStore()
  return authStore.isAuthenticated
}

// Función helper para obtener el rol del usuario
export const getUserRole = () => {
  const authStore = useAuthStore()
  return authStore.userRole || authStore.user?.role || 'user'
}

// Función helper para verificar si el usuario es admin
export const isAdmin = () => {
  const role = getUserRole()
  return role === 'admin' || role === 'super_admin'
}

// Función helper para verificar si el usuario es moderador o superior
export const isModerator = () => {
  const role = getUserRole()
  return role === 'moderator' || role === 'admin' || role === 'super_admin'
}

console.log('✅ Middleware de autenticación cargado correctamente')