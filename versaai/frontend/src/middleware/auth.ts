import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

/**
 * Middleware de autenticación para Vue Router
 * Maneja la protección de rutas y redirecciones
 */

// Tipos para los guards
type RouteGuard = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => Promise<void> | void

/**
 * Guard principal de autenticación
 * Verifica si el usuario está autenticado antes de acceder a rutas protegidas
 */
export const authGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()
  const toast = useToast()

  try {
    // Verificar autenticación actual
    await authStore.checkAuth()

    if (!authStore.isAuthenticated) {
      // Usuario no autenticado, redirigir al login
      const redirectPath = to.fullPath !== '/auth/login' ? to.fullPath : undefined
      
      toast.warning('Debes iniciar sesión para acceder a esta página')
      
      next({
        path: '/auth/login',
        query: redirectPath ? { redirect: redirectPath } : undefined
      })
      return
    }

    // Usuario autenticado, continuar
    next()
  } catch (error) {
    console.error('Error en authGuard:', error)
    
    // En caso de error, redirigir al login
    toast.error('Error al verificar autenticación')
    next('/auth/login')
  }
}

/**
 * Guard para usuarios invitados (no autenticados)
 * Redirige a dashboard si ya está autenticado
 */
export const guestGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()

  try {
    await authStore.checkAuth()

    if (authStore.isAuthenticated) {
      // Usuario ya autenticado, redirigir al dashboard
      next('/dashboard')
      return
    }

    // Usuario no autenticado, continuar
    next()
  } catch (error) {
    console.error('Error en guestGuard:', error)
    // En caso de error, permitir acceso (asumir no autenticado)
    next()
  }
}

/**
 * Factory para crear guards de roles
 * @param requiredRole - Rol requerido para acceder
 * @param redirectTo - Ruta de redirección si no tiene el rol (por defecto: /unauthorized)
 */
export const createRoleGuard = (requiredRole: string, redirectTo = '/unauthorized'): RouteGuard => {
  return async (to, from, next) => {
    const authStore = useAuthStore()
    const toast = useToast()

    try {
      await authStore.checkAuth()

      if (!authStore.isAuthenticated) {
        toast.warning('Debes iniciar sesión para acceder a esta página')
        next('/auth/login')
        return
      }

      if (!authStore.hasRole(requiredRole)) {
        toast.error(`Acceso denegado. Se requiere rol: ${requiredRole}`)
        next(redirectTo)
        return
      }

      next()
    } catch (error) {
      console.error('Error en roleGuard:', error)
      toast.error('Error al verificar permisos')
      next('/auth/login')
    }
  }
}

/**
 * Factory para crear guards de permisos
 * @param requiredPermission - Permiso requerido para acceder
 * @param redirectTo - Ruta de redirección si no tiene el permiso (por defecto: /unauthorized)
 */
export const createPermissionGuard = (requiredPermission: string, redirectTo = '/unauthorized'): RouteGuard => {
  return async (to, from, next) => {
    const authStore = useAuthStore()
    const toast = useToast()

    try {
      await authStore.checkAuth()

      if (!authStore.isAuthenticated) {
        toast.warning('Debes iniciar sesión para acceder a esta página')
        next('/auth/login')
        return
      }

      if (!authStore.hasPermission(requiredPermission)) {
        toast.error(`Acceso denegado. Se requiere permiso: ${requiredPermission}`)
        next(redirectTo)
        return
      }

      next()
    } catch (error) {
      console.error('Error en permissionGuard:', error)
      toast.error('Error al verificar permisos')
      next('/auth/login')
    }
  }
}

/**
 * Guards específicos para roles comunes
 */
export const adminGuard = createRoleGuard('admin')
export const moderatorGuard = createRoleGuard('moderator')
export const userGuard = createRoleGuard('user')

/**
 * Guard combinado para admin o moderador
 */
export const adminOrModeratorGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()
  const toast = useToast()

  try {
    await authStore.checkAuth()

    if (!authStore.isAuthenticated) {
      toast.warning('Debes iniciar sesión para acceder a esta página')
      next('/auth/login')
      return
    }

    if (!authStore.isAdmin && !authStore.isModerator) {
      toast.error('Acceso denegado. Se requieren permisos de administrador o moderador')
      next('/unauthorized')
      return
    }

    next()
  } catch (error) {
    console.error('Error en adminOrModeratorGuard:', error)
    toast.error('Error al verificar permisos')
    next('/auth/login')
  }
}

/**
 * Guard para verificar si el usuario puede acceder a su propio perfil
 * o si es admin/moderador
 */
export const profileGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()
  const toast = useToast()

  try {
    await authStore.checkAuth()

    if (!authStore.isAuthenticated) {
      toast.warning('Debes iniciar sesión para acceder a esta página')
      next('/auth/login')
      return
    }

    const userId = to.params.id as string
    const currentUserId = authStore.user?.id?.toString()

    // Permitir acceso si es su propio perfil o es admin/moderador
    if (userId === currentUserId || authStore.isAdmin || authStore.isModerator) {
      next()
      return
    }

    toast.error('No tienes permisos para acceder a este perfil')
    next('/dashboard')
  } catch (error) {
    console.error('Error en profileGuard:', error)
    toast.error('Error al verificar permisos')
    next('/auth/login')
  }
}

/**
 * Guard para verificar si el token está próximo a expirar
 * y refrescarlo automáticamente
 */
export const tokenRefreshGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()

  try {
    if (authStore.isAuthenticated && authStore.token) {
      // Verificar si el token expira en los próximos 5 minutos
      const tokenPayload = JSON.parse(atob(authStore.token.split('.')[1]))
      const expirationTime = tokenPayload.exp * 1000
      const currentTime = Date.now()
      const timeUntilExpiration = expirationTime - currentTime

      // Si expira en menos de 5 minutos, intentar refrescar
      if (timeUntilExpiration < 5 * 60 * 1000) {
        try {
          await authStore.refreshToken()
        } catch (error) {
          console.error('Error al refrescar token:', error)
          // Si falla el refresh, hacer logout
          await authStore.logout()
          next('/auth/login')
          return
        }
      }
    }

    next()
  } catch (error) {
    console.error('Error en tokenRefreshGuard:', error)
    next()
  }
}

/**
 * Guard para verificar el estado de la cuenta del usuario
 */
export const accountStatusGuard: RouteGuard = async (to, from, next) => {
  const authStore = useAuthStore()
  const toast = useToast()

  try {
    await authStore.checkAuth()

    if (!authStore.isAuthenticated) {
      next('/auth/login')
      return
    }

    const user = authStore.user
    if (!user) {
      next('/auth/login')
      return
    }

    // Verificar si la cuenta está activa
    if (user.status === 'inactive') {
      toast.error('Tu cuenta está inactiva. Contacta al administrador')
      await authStore.logout()
      next('/auth/login')
      return
    }

    // Verificar si la cuenta está suspendida
    if (user.status === 'suspended') {
      toast.error('Tu cuenta está suspendida. Contacta al administrador')
      await authStore.logout()
      next('/auth/login')
      return
    }

    // Verificar si el email está verificado (solo para ciertas rutas)
    const requiresEmailVerification = [
      '/dashboard',
      '/chatbots',
      '/settings',
      '/profile'
    ]

    if (requiresEmailVerification.some(route => to.path.startsWith(route))) {
      if (!user.email_verified_at) {
        toast.warning('Debes verificar tu email para acceder a esta función')
        next('/auth/verify-email')
        return
      }
    }

    next()
  } catch (error) {
    console.error('Error en accountStatusGuard:', error)
    next('/auth/login')
  }
}

/**
 * Middleware combinado que aplica múltiples guards
 * @param guards - Array de guards a aplicar en orden
 */
export const combineGuards = (...guards: RouteGuard[]): RouteGuard => {
  return async (to, from, next) => {
    let index = 0

    const runNextGuard = async () => {
      if (index >= guards.length) {
        next()
        return
      }

      const guard = guards[index++]
      
      await guard(to, from, (result?: any) => {
        if (result === undefined || result === true) {
          // Continuar con el siguiente guard
          runNextGuard()
        } else {
          // Redirigir o detener
          next(result)
        }
      })
    }

    await runNextGuard()
  }
}

/**
 * Configuración de guards por defecto para diferentes tipos de rutas
 */
export const routeGuards = {
  // Rutas públicas (sin autenticación)
  public: [],
  
  // Rutas de invitados (solo no autenticados)
  guest: [guestGuard],
  
  // Rutas protegidas básicas
  protected: [authGuard, tokenRefreshGuard, accountStatusGuard],
  
  // Rutas de administrador
  admin: [authGuard, tokenRefreshGuard, accountStatusGuard, adminGuard],
  
  // Rutas de moderador
  moderator: [authGuard, tokenRefreshGuard, accountStatusGuard, moderatorGuard],
  
  // Rutas de admin o moderador
  adminOrModerator: [authGuard, tokenRefreshGuard, accountStatusGuard, adminOrModeratorGuard],
  
  // Rutas de perfil
  profile: [authGuard, tokenRefreshGuard, accountStatusGuard, profileGuard]
}

/**
 * Helper para aplicar guards a una ruta
 * @param guardType - Tipo de guard a aplicar
 */
export const applyGuards = (guardType: keyof typeof routeGuards) => {
  const guards = routeGuards[guardType]
  return guards.length === 1 ? guards[0] : combineGuards(...guards)
}

export default {
  authGuard,
  guestGuard,
  createRoleGuard,
  createPermissionGuard,
  adminGuard,
  moderatorGuard,
  userGuard,
  adminOrModeratorGuard,
  profileGuard,
  tokenRefreshGuard,
  accountStatusGuard,
  combineGuards,
  routeGuards,
  applyGuards
}