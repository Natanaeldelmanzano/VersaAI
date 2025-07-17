<template>
  <div id="app">
    <!-- Loading Screen -->
    <div v-if="isLoading" class="loading-screen">
      <div class="loading-content">
        <div class="loading-logo">
          <font-awesome-icon icon="robot" class="loading-icon" />
        </div>
        <h2>VersaAI</h2>
        <div class="loading-spinner">
          <font-awesome-icon icon="spinner" spin />
        </div>
        <p>Cargando aplicación...</p>
      </div>
    </div>

    <!-- Main Application -->
    <div v-else class="app-container">
      <!-- Global Notifications -->
      <div id="notifications-container"></div>
      
      <!-- Router View -->
      <router-view v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </div>

    <!-- Global Modals -->
    <teleport to="body">
      <!-- Error Modal -->
      <div v-if="globalError" class="modal-overlay" @click="clearGlobalError">
        <div class="error-modal" @click.stop>
          <div class="error-header">
            <font-awesome-icon icon="exclamation-triangle" class="error-icon" />
            <h3>Error de Aplicación</h3>
            <button @click="clearGlobalError" class="close-btn">
              <font-awesome-icon icon="times" />
            </button>
          </div>
          <div class="error-content">
            <p>{{ globalError.message }}</p>
            <details v-if="globalError.details">
              <summary>Detalles técnicos</summary>
              <pre>{{ globalError.details }}</pre>
            </details>
          </div>
          <div class="error-actions">
            <button @click="reloadApp" class="btn btn-primary">
              Recargar Aplicación
            </button>
            <button @click="clearGlobalError" class="btn btn-secondary">
              Cerrar
            </button>
          </div>
        </div>
      </div>

      <!-- Maintenance Modal -->
      <div v-if="maintenanceMode" class="modal-overlay">
        <div class="maintenance-modal">
          <div class="maintenance-content">
            <font-awesome-icon icon="cog" class="maintenance-icon" spin />
            <h2>Mantenimiento Programado</h2>
            <p>La aplicación está temporalmente en mantenimiento.</p>
            <p>Por favor, inténtalo de nuevo en unos minutos.</p>
            <button @click="checkMaintenance" class="btn btn-primary">
              Verificar Estado
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'
import { useToast } from 'vue-toastification'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const appStore = useAppStore()
    const toast = useToast()
    
    const isLoading = ref(true)
    const globalError = ref(null)
    const maintenanceMode = ref(false)
    
    // Computed properties
    const isDarkMode = computed(() => appStore.isDarkMode)
    
    // Methods
    const initializeApp = async () => {
      try {
        console.log('🚀 Inicializando aplicación VersaAI...')
        
        // Check maintenance mode
        await checkMaintenance()
        
        if (maintenanceMode.value) {
          isLoading.value = false
          return
        }
        
        // Initialize auth store
        await authStore.initialize()
        
        // Initialize app store
        await appStore.initialize()
        
        // Set theme
        updateTheme()
        
        console.log('✅ Aplicación inicializada correctamente')
        
      } catch (error) {
        console.error('❌ Error inicializando aplicación:', error)
        handleGlobalError(error)
      } finally {
        // Minimum loading time for better UX
        setTimeout(() => {
          isLoading.value = false
        }, 1000)
      }
    }
    
    const checkMaintenance = async () => {
      try {
        // This would typically check a maintenance endpoint
        // For now, we'll just check if there's a maintenance flag
        const maintenanceFlag = localStorage.getItem('maintenance_mode')
        maintenanceMode.value = maintenanceFlag === 'true'
      } catch (error) {
        console.warn('Could not check maintenance status:', error)
      }
    }
    
    const handleGlobalError = (error) => {
      globalError.value = {
        message: error.message || 'Ha ocurrido un error inesperado',
        details: error.stack || error.toString()
      }
      
      // Log to external service in production
      if (import.meta.env.PROD) {
        // logErrorToService(error)
      }
    }
    
    const clearGlobalError = () => {
      globalError.value = null
    }
    
    const reloadApp = () => {
      window.location.reload()
    }
    
    const updateTheme = () => {
      const root = document.documentElement
      if (isDarkMode.value) {
        root.classList.add('dark-theme')
      } else {
        root.classList.remove('dark-theme')
      }
    }
    
    // Handle online/offline status
    const handleOnline = () => {
      toast.success('Conexión restaurada')
      appStore.setOnlineStatus(true)
    }
    
    const handleOffline = () => {
      toast.warning('Sin conexión a internet')
      appStore.setOnlineStatus(false)
    }
    
    // Handle visibility change
    const handleVisibilityChange = () => {
      if (document.hidden) {
        appStore.setAppVisibility(false)
      } else {
        appStore.setAppVisibility(true)
        // Refresh auth token if needed
        if (authStore.isAuthenticated) {
          authStore.refreshTokenIfNeeded()
        }
      }
    }
    
    // Lifecycle
    onMounted(() => {
      initializeApp()
      
      // Add event listeners
      window.addEventListener('online', handleOnline)
      window.addEventListener('offline', handleOffline)
      document.addEventListener('visibilitychange', handleVisibilityChange)
      
      // Global error handler
      window.addEventListener('error', (event) => {
        handleGlobalError(new Error(event.message))
      })
      
      window.addEventListener('unhandledrejection', (event) => {
        handleGlobalError(new Error(event.reason))
      })
    })
    
    onUnmounted(() => {
      // Remove event listeners
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    })
    
    // Watch for theme changes
    const unwatchTheme = appStore.$subscribe((mutation, state) => {
      if (mutation.events?.some(event => event.key === 'isDarkMode')) {
        updateTheme()
      }
    })
    
    onUnmounted(() => {
      unwatchTheme()
    })
    
    return {
      isLoading,
      globalError,
      maintenanceMode,
      isDarkMode,
      clearGlobalError,
      reloadApp,
      checkMaintenance
    }
  }
}
</script>

<style>
/* Global Styles */
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100vh;
  overflow: hidden;
}

.app-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Loading Screen */
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-logo {
  margin-bottom: 1rem;
}

.loading-icon {
  font-size: 4rem;
  color: white;
  animation: pulse 2s infinite;
}

.loading-spinner {
  margin: 1rem 0;
  font-size: 1.5rem;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Page Transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(4px);
}

.error-modal,
.maintenance-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
}

.error-header {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: #fee;
  border-bottom: 1px solid #fcc;
}

.error-icon {
  color: #e53e3e;
  font-size: 1.5rem;
  margin-right: 0.75rem;
}

.error-header h3 {
  margin: 0;
  flex: 1;
  color: #e53e3e;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #666;
  cursor: pointer;
  padding: 0.25rem;
}

.error-content {
  padding: 1.5rem;
}

.error-content details {
  margin-top: 1rem;
}

.error-content pre {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow: auto;
  font-size: 0.875rem;
}

.error-actions {
  padding: 1rem 1.5rem;
  background: #f9f9f9;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.maintenance-content {
  padding: 3rem 2rem;
  text-align: center;
}

.maintenance-icon {
  font-size: 3rem;
  color: #3182ce;
  margin-bottom: 1rem;
}

.maintenance-content h2 {
  margin: 0 0 1rem 0;
  color: #2d3748;
}

.maintenance-content p {
  color: #4a5568;
  margin: 0.5rem 0;
}

/* Button Styles */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #3182ce;
  color: white;
}

.btn-primary:hover {
  background: #2c5aa0;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

/* Dark Theme */
.dark-theme {
  --bg-primary: #1a202c;
  --bg-secondary: #2d3748;
  --text-primary: #f7fafc;
  --text-secondary: #e2e8f0;
  --border-color: #4a5568;
}

.dark-theme .error-modal,
.dark-theme .maintenance-modal {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.dark-theme .error-header {
  background: #742a2a;
  border-color: #c53030;
}

.dark-theme .error-actions {
  background: var(--bg-primary);
}

/* Responsive */
@media (max-width: 768px) {
  .error-modal,
  .maintenance-modal {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}

/* Notifications Container */
#notifications-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 9998;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .page-enter-active,
  .page-leave-active {
    transition: none;
  }
  
  .loading-icon {
    animation: none;
  }
}

/* Focus styles */
.btn:focus,
.close-btn:focus {
  outline: 2px solid #3182ce;
  outline-offset: 2px;
}
</style>