import type { App } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useSession } from '@/composables/useAuth'
import { useToast } from 'vue-toastification'

/**
 * Plugin de autenticación para Vue
 * Inicializa automáticamente la autenticación y el monitoreo de sesión
 */

interface AuthPluginOptions {
  // Configuración del plugin
  autoCheck?: boolean // Verificar autenticación automáticamente al iniciar
  sessionMonitoring?: boolean // Habilitar monitoreo de sesión
  tokenRefreshInterval?: number // Intervalo de refresco de token en minutos
  sessionTimeout?: number // Timeout de sesión en minutos
  showNotifications?: boolean // Mostrar notificaciones de autenticación
}

const defaultOptions: AuthPluginOptions = {
  autoCheck: true,
  sessionMonitoring: true,
  tokenRefreshInterval: 15, // 15 minutos
  sessionTimeout: 60, // 60 minutos
  showNotifications: true
}

/**
 * Instala el plugin de autenticación
 */
export function createAuthPlugin(options: AuthPluginOptions = {}) {
  const config = { ...defaultOptions, ...options }

  return {
    install(app: App) {
      // Configurar propiedades globales
      app.config.globalProperties.$auth = {
        config,
        store: null as any,
        session: null as any
      }

      // Inicializar cuando la app esté montada
      app.mixin({
        async created() {
          // Solo inicializar una vez en el componente raíz
          if (this.$root === this) {
            await initializeAuth(config)
          }
        }
      })
    }
  }
}

/**
 * Inicializa la autenticación
 */
async function initializeAuth(config: AuthPluginOptions) {
  const authStore = useAuthStore()
  const { startSessionMonitoring, stopSessionMonitoring } = useSession()
  const toast = useToast()

  try {
    // Verificar autenticación automáticamente si está habilitado
    if (config.autoCheck) {
      await authStore.checkAuth()
      
      if (authStore.isAuthenticated && config.showNotifications) {
        console.log('✅ Usuario autenticado:', authStore.user?.name)
      }
    }

    // Iniciar monitoreo de sesión si está habilitado
    if (config.sessionMonitoring && authStore.isAuthenticated) {
      startSessionMonitoring()
      console.log('🔄 Monitoreo de sesión iniciado')
    }

    // Configurar interceptores de respuesta para manejar errores de autenticación
    setupAuthInterceptors(authStore, toast, config)

    // Configurar listeners para eventos de autenticación
    setupAuthListeners(authStore, { startSessionMonitoring, stopSessionMonitoring }, config)

  } catch (error) {
    console.error('❌ Error al inicializar autenticación:', error)
    
    if (config.showNotifications) {
      toast.error('Error al inicializar la autenticación')
    }
  }
}

/**
 * Configura interceptores para manejar errores de autenticación
 */
function setupAuthInterceptors(authStore: any, toast: any, config: AuthPluginOptions) {
  // Interceptor para respuestas HTTP (si usas axios)
  if (typeof window !== 'undefined' && (window as any).axios) {
    const axios = (window as any).axios

    // Interceptor de request para agregar token
    axios.interceptors.request.use(
      (requestConfig: any) => {
        if (authStore.token) {
          requestConfig.headers.Authorization = `Bearer ${authStore.token}`
        }
        return requestConfig
      },
      (error: any) => Promise.reject(error)
    )

    // Interceptor de response para manejar errores de autenticación
    axios.interceptors.response.use(
      (response: any) => response,
      async (error: any) => {
        const originalRequest = error.config

        // Token expirado o inválido
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            // Intentar refrescar token
            await authStore.refreshToken()
            
            // Reintentar request original con nuevo token
            originalRequest.headers.Authorization = `Bearer ${authStore.token}`
            return axios(originalRequest)
          } catch (refreshError) {
            // Si falla el refresh, hacer logout
            await authStore.logout()
            
            if (config.showNotifications) {
              toast.error('Sesión expirada. Por favor, inicia sesión nuevamente')
            }
            
            // Redirigir al login
            if (typeof window !== 'undefined') {
              window.location.href = '/auth/login'
            }
          }
        }

        // Cuenta suspendida o bloqueada
        if (error.response?.status === 403) {
          await authStore.logout()
          
          if (config.showNotifications) {
            toast.error('Tu cuenta ha sido suspendida. Contacta al administrador')
          }
          
          if (typeof window !== 'undefined') {
            window.location.href = '/auth/login'
          }
        }

        return Promise.reject(error)
      }
    )
  }
}

/**
 * Configura listeners para eventos de autenticación
 */
function setupAuthListeners(
  authStore: any, 
  sessionManager: { startSessionMonitoring: () => void, stopSessionMonitoring: () => void },
  config: AuthPluginOptions
) {
  // Listener para cambios en el estado de autenticación
  authStore.$subscribe((mutation: any, state: any) => {
    if (mutation.type === 'direct' && mutation.payload) {
      const { user, token } = mutation.payload
      
      // Usuario se autenticó
      if (user && token && config.sessionMonitoring) {
        sessionManager.startSessionMonitoring()
        console.log('🔄 Monitoreo de sesión iniciado para:', user.name)
      }
      
      // Usuario cerró sesión
      if (!user && !token) {
        sessionManager.stopSessionMonitoring()
        console.log('⏹️ Monitoreo de sesión detenido')
      }
    }
  })

  // Listener para eventos de visibilidad de la página
  if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', async () => {
      if (!document.hidden && authStore.isAuthenticated) {
        // Página visible nuevamente, verificar autenticación
        try {
          await authStore.checkAuth()
        } catch (error) {
          console.error('Error al verificar autenticación:', error)
        }
      }
    })
  }

  // Listener para eventos de almacenamiento (múltiples pestañas)
  if (typeof window !== 'undefined') {
    window.addEventListener('storage', (event) => {
      if (event.key === 'auth_token') {
        if (!event.newValue) {
          // Token eliminado en otra pestaña, hacer logout local
          authStore.$reset()
          sessionManager.stopSessionMonitoring()
          
          if (config.showNotifications) {
            const toast = useToast()
            toast.info('Sesión cerrada en otra pestaña')
          }
        }
      }
    })
  }

  // Listener para eventos de conexión de red
  if (typeof window !== 'undefined') {
    window.addEventListener('online', async () => {
      if (authStore.isAuthenticated) {
        // Reconectado, verificar autenticación
        try {
          await authStore.checkAuth()
          console.log('🌐 Conexión restaurada, autenticación verificada')
        } catch (error) {
          console.error('Error al verificar autenticación tras reconexión:', error)
        }
      }
    })

    window.addEventListener('offline', () => {
      console.log('📴 Conexión perdida')
    })
  }
}

/**
 * Utilidades para el plugin de autenticación
 */
export const authUtils = {
  /**
   * Verifica si el token está próximo a expirar
   */
  isTokenExpiringSoon(token: string, minutesThreshold = 5): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const expirationTime = payload.exp * 1000
      const currentTime = Date.now()
      const timeUntilExpiration = expirationTime - currentTime
      
      return timeUntilExpiration < minutesThreshold * 60 * 1000
    } catch (error) {
      console.error('Error al verificar expiración del token:', error)
      return true // Asumir que expira si hay error
    }
  },

  /**
   * Obtiene información del token JWT
   */
  getTokenInfo(token: string) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return {
        userId: payload.sub,
        email: payload.email,
        roles: payload.roles || [],
        permissions: payload.permissions || [],
        issuedAt: new Date(payload.iat * 1000),
        expiresAt: new Date(payload.exp * 1000)
      }
    } catch (error) {
      console.error('Error al decodificar token:', error)
      return null
    }
  },

  /**
   * Formatea el tiempo restante hasta la expiración
   */
  formatTimeUntilExpiration(token: string): string {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const expirationTime = payload.exp * 1000
      const currentTime = Date.now()
      const timeUntilExpiration = expirationTime - currentTime
      
      if (timeUntilExpiration <= 0) {
        return 'Expirado'
      }
      
      const minutes = Math.floor(timeUntilExpiration / (1000 * 60))
      const hours = Math.floor(minutes / 60)
      const days = Math.floor(hours / 24)
      
      if (days > 0) {
        return `${days}d ${hours % 24}h`
      } else if (hours > 0) {
        return `${hours}h ${minutes % 60}m`
      } else {
        return `${minutes}m`
      }
    } catch (error) {
      return 'Error'
    }
  },

  /**
   * Genera un ID de sesión único
   */
  generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  },

  /**
   * Verifica si el navegador soporta almacenamiento local
   */
  supportsLocalStorage(): boolean {
    try {
      const test = 'test'
      localStorage.setItem(test, test)
      localStorage.removeItem(test)
      return true
    } catch (error) {
      return false
    }
  }
}

/**
 * Composable para acceder a la configuración del plugin
 */
export function useAuthPlugin() {
  const authStore = useAuthStore()
  const { startSessionMonitoring, stopSessionMonitoring } = useSession()
  
  return {
    authStore,
    sessionManager: { startSessionMonitoring, stopSessionMonitoring },
    utils: authUtils
  }
}

export default createAuthPlugin