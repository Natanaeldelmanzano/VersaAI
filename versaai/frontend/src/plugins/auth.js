import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'

export function createAuthPlugin(options = {}) {
  const defaultOptions = {
    autoCheck: true,
    sessionMonitoring: true,
    tokenRefreshInterval: 15, // minutes
    sessionTimeout: 60, // minutes
    showNotifications: true
  }

  const config = { ...defaultOptions, ...options }

  return {
    install(app) {
      const authStore = useAuthStore()
      const toast = useToast()

      // Auto-check authentication on app start
      if (config.autoCheck) {
        authStore.checkAuth().catch(error => {
          console.warn('Auth check failed:', error)
        })
      }

      // Session monitoring
      if (config.sessionMonitoring) {
        let sessionTimer
        let refreshTimer

        const startSessionTimer = () => {
          if (sessionTimer) clearTimeout(sessionTimer)
          
          sessionTimer = setTimeout(() => {
            if (config.showNotifications) {
              toast.warning('Sesión expirada. Por favor, inicia sesión nuevamente.')
            }
            authStore.logout()
          }, config.sessionTimeout * 60 * 1000)
        }

        const startRefreshTimer = () => {
          if (refreshTimer) clearInterval(refreshTimer)
          
          refreshTimer = setInterval(() => {
            if (authStore.isAuthenticated) {
              authStore.checkAuth().catch(() => {
                console.warn('Token refresh failed')
              })
            }
          }, config.tokenRefreshInterval * 60 * 1000)
        }

        // Start timers when user is authenticated
        if (authStore.isAuthenticated) {
          startSessionTimer()
          startRefreshTimer()
        }

        // Watch for authentication changes
        authStore.$subscribe((mutation, state) => {
          if (state.isAuthenticated) {
            startSessionTimer()
            startRefreshTimer()
          } else {
            if (sessionTimer) clearTimeout(sessionTimer)
            if (refreshTimer) clearInterval(refreshTimer)
          }
        })
      }

      // Make auth store globally available
      app.config.globalProperties.$auth = authStore
      app.provide('auth', authStore)
    }
  }
}

export default createAuthPlugin