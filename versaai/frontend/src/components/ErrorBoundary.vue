<template>
  <div v-if="hasError" class="error-boundary">
    <!-- Error UI personalizable -->
    <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <div class="max-w-md w-full">
        <!-- Icono de error -->
        <div class="text-center mb-6">
          <div class="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {{ errorTitle }}
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            {{ errorMessage }}
          </p>
        </div>

        <!-- Detalles del error (solo en desarrollo) -->
        <div v-if="showDetails && isDevelopment" class="mb-6">
          <details class="bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <summary class="cursor-pointer text-sm font-medium text-red-800 dark:text-red-200 mb-2">
              Detalles técnicos
            </summary>
            <div class="mt-2 text-xs text-red-700 dark:text-red-300 font-mono">
              <div class="mb-2">
                <strong>Error:</strong> {{ error?.message || 'Error desconocido' }}
              </div>
              <div class="mb-2">
                <strong>Componente:</strong> {{ errorInfo?.componentName || 'Desconocido' }}
              </div>
              <div v-if="error?.stack" class="mb-2">
                <strong>Stack trace:</strong>
                <pre class="mt-1 whitespace-pre-wrap text-xs">{{ error.stack }}</pre>
              </div>
              <div v-if="errorInfo?.componentStack" class="mb-2">
                <strong>Component stack:</strong>
                <pre class="mt-1 whitespace-pre-wrap text-xs">{{ errorInfo.componentStack }}</pre>
              </div>
            </div>
          </details>
        </div>

        <!-- Acciones -->
        <div class="flex flex-col sm:flex-row gap-3">
          <button
            @click="retry"
            class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Reintentar
          </button>
          
          <button
            @click="goHome"
            class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
            Ir al inicio
          </button>
        </div>

        <!-- Información adicional -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Si el problema persiste, contacta al soporte técnico.
          </p>
          <button
            @click="reportError"
            class="mt-2 text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            Reportar este error
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Contenido normal cuando no hay error -->
  <slot v-else></slot>
</template>

<script>
import { ref, computed, onErrorCaptured, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ErrorBoundary',
  props: {
    // Título personalizado del error
    fallbackTitle: {
      type: String,
      default: 'Algo salió mal'
    },
    // Mensaje personalizado del error
    fallbackMessage: {
      type: String,
      default: 'Ha ocurrido un error inesperado. Por favor, inténtalo de nuevo.'
    },
    // Mostrar detalles técnicos
    showDetails: {
      type: Boolean,
      default: true
    },
    // Callback personalizado para manejo de errores
    onError: {
      type: Function,
      default: null
    },
    // Habilitar reporte automático de errores
    enableReporting: {
      type: Boolean,
      default: true
    }
  },
  emits: ['error', 'retry', 'report'],
  setup(props, { emit }) {
    const router = useRouter()
    
    // Estado del error
    const hasError = ref(false)
    const error = ref(null)
    const errorInfo = ref(null)
    const errorId = ref(null)
    
    // Computed properties
    const isDevelopment = computed(() => {
      return import.meta.env.DEV
    })
    
    const errorTitle = computed(() => {
      if (error.value?.name === 'ChunkLoadError') {
        return 'Error de carga'
      }
      if (error.value?.name === 'NetworkError') {
        return 'Error de conexión'
      }
      return props.fallbackTitle
    })
    
    const errorMessage = computed(() => {
      if (error.value?.name === 'ChunkLoadError') {
        return 'No se pudo cargar parte de la aplicación. Por favor, recarga la página.'
      }
      if (error.value?.name === 'NetworkError') {
        return 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
      }
      return props.fallbackMessage
    })
    
    // Capturar errores de componentes hijos
    onErrorCaptured((err, instance, info) => {
      console.error('Error capturado por ErrorBoundary:', err)
      
      // Generar ID único para el error
      errorId.value = `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      
      // Guardar información del error
      error.value = err
      errorInfo.value = {
        componentName: instance?.$options.name || instance?.$options.__name || 'Unknown',
        componentStack: info,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        url: window.location.href
      }
      
      hasError.value = true
      
      // Llamar callback personalizado si existe
      if (props.onError) {
        props.onError(err, errorInfo.value)
      }
      
      // Emitir evento
      emit('error', {
        error: err,
        errorInfo: errorInfo.value,
        errorId: errorId.value
      })
      
      // Reportar error automáticamente si está habilitado
      if (props.enableReporting) {
        reportErrorToService(err, errorInfo.value)
      }
      
      // Prevenir que el error se propague
      return false
    })
    
    // Capturar errores globales de JavaScript
    onMounted(() => {
      const handleGlobalError = (event) => {
        console.error('Error global capturado:', event.error)
        
        error.value = event.error
        errorInfo.value = {
          componentName: 'Global',
          componentStack: 'Global error',
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno
        }
        
        hasError.value = true
      }
      
      const handleUnhandledRejection = (event) => {
        console.error('Promise rejection no manejada:', event.reason)
        
        error.value = new Error(event.reason)
        errorInfo.value = {
          componentName: 'Promise',
          componentStack: 'Unhandled promise rejection',
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href
        }
        
        hasError.value = true
      }
      
      window.addEventListener('error', handleGlobalError)
      window.addEventListener('unhandledrejection', handleUnhandledRejection)
      
      // Cleanup
      return () => {
        window.removeEventListener('error', handleGlobalError)
        window.removeEventListener('unhandledrejection', handleUnhandledRejection)
      }
    })
    
    // Funciones de acción
    const retry = () => {
      hasError.value = false
      error.value = null
      errorInfo.value = null
      errorId.value = null
      
      emit('retry')
      
      // Recargar la página si es un error de chunk
      if (error.value?.name === 'ChunkLoadError') {
        window.location.reload()
      }
    }
    
    const goHome = () => {
      hasError.value = false
      error.value = null
      errorInfo.value = null
      errorId.value = null
      
      router.push('/')
    }
    
    const reportError = () => {
      const errorData = {
        error: error.value,
        errorInfo: errorInfo.value,
        errorId: errorId.value
      }
      
      emit('report', errorData)
      reportErrorToService(error.value, errorInfo.value)
      
      // Mostrar confirmación
      console.log('Error reportado:', errorId.value)
    }
    
    // Función para reportar errores a un servicio externo
    const reportErrorToService = async (err, info) => {
      try {
        // Aquí puedes integrar con servicios como Sentry, LogRocket, etc.
        const errorReport = {
          message: err?.message || 'Unknown error',
          stack: err?.stack,
          componentInfo: info,
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href,
          userId: null, // Agregar ID de usuario si está disponible
          sessionId: sessionStorage.getItem('sessionId') || 'unknown'
        }
        
        // Ejemplo de envío a API de errores
        // await fetch('/api/errors', {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify(errorReport)
        // })
        
        console.log('Error report prepared:', errorReport)
      } catch (reportError) {
        console.error('Failed to report error:', reportError)
      }
    }
    
    return {
      hasError,
      error,
      errorInfo,
      errorId,
      isDevelopment,
      errorTitle,
      errorMessage,
      retry,
      goHome,
      reportError
    }
  }
}
</script>

<style scoped>
.error-boundary {
  isolation: isolate;
}

/* Animaciones suaves */
.error-boundary > div {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estilos para el código */
pre {
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.05);
  padding: 8px;
  border-radius: 4px;
  font-size: 11px;
}

/* Dark mode para el código */
.dark pre {
  background: rgba(255, 255, 255, 0.05);
}
</style>