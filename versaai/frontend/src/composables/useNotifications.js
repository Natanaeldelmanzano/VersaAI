import { ref, reactive } from 'vue'

// Estado global de notificaciones
const notificationsState = reactive({
  notifications: [],
  settings: {
    position: 'top-right',
    duration: 4000,
    maxNotifications: 5,
    showProgress: true,
    pauseOnHover: true
  }
})

let notificationId = 0

export function useNotifications() {
  // Métodos para gestionar notificaciones
  const showNotification = (message, type = 'info', options = {}) => {
    const notification = {
      id: ++notificationId,
      message,
      type, // 'success', 'error', 'warning', 'info'
      timestamp: new Date(),
      duration: options.duration || notificationsState.settings.duration,
      persistent: options.persistent || false,
      actions: options.actions || [],
      progress: options.showProgress !== false ? 100 : null,
      paused: false
    }
    
    // Añadir notificación al inicio del array
    notificationsState.notifications.unshift(notification)
    
    // Limitar número de notificaciones
    if (notificationsState.notifications.length > notificationsState.settings.maxNotifications) {
      notificationsState.notifications = notificationsState.notifications.slice(0, notificationsState.settings.maxNotifications)
    }
    
    // Auto-remover si no es persistente
    if (!notification.persistent && notification.duration > 0) {
      startNotificationTimer(notification)
    }
    
    return notification.id
  }
  
  const removeNotification = (id) => {
    const index = notificationsState.notifications.findIndex(n => n.id === id)
    if (index > -1) {
      notificationsState.notifications.splice(index, 1)
    }
  }
  
  const clearAllNotifications = () => {
    notificationsState.notifications.splice(0)
  }
  
  const pauseNotification = (id) => {
    const notification = notificationsState.notifications.find(n => n.id === id)
    if (notification) {
      notification.paused = true
    }
  }
  
  const resumeNotification = (id) => {
    const notification = notificationsState.notifications.find(n => n.id === id)
    if (notification) {
      notification.paused = false
      if (notification.progress > 0) {
        startNotificationTimer(notification)
      }
    }
  }
  
  const updateSettings = (newSettings) => {
    Object.assign(notificationsState.settings, newSettings)
  }
  
  // Métodos de conveniencia
  const showSuccess = (message, options = {}) => {
    return showNotification(message, 'success', options)
  }
  
  const showError = (message, options = {}) => {
    return showNotification(message, 'error', { ...options, duration: 6000 })
  }
  
  const showWarning = (message, options = {}) => {
    return showNotification(message, 'warning', options)
  }
  
  const showInfo = (message, options = {}) => {
    return showNotification(message, 'info', options)
  }
  
  const showLoading = (message, options = {}) => {
    return showNotification(message, 'info', { 
      ...options, 
      persistent: true,
      showProgress: false
    })
  }
  
  // Timer para auto-remover notificaciones
  const startNotificationTimer = (notification) => {
    if (notification.progress === null) return
    
    const interval = 50 // Actualizar cada 50ms
    const decrement = (100 / notification.duration) * interval
    
    const timer = setInterval(() => {
      if (notification.paused) return
      
      notification.progress -= decrement
      
      if (notification.progress <= 0) {
        clearInterval(timer)
        removeNotification(notification.id)
      }
    }, interval)
  }
  
  return {
    // Estado
    notifications: notificationsState.notifications,
    settings: notificationsState.settings,
    
    // Métodos principales
    showNotification,
    removeNotification,
    clearAllNotifications,
    pauseNotification,
    resumeNotification,
    updateSettings,
    
    // Métodos de conveniencia
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showLoading
  }
}

// Composable para notificaciones del sistema
export function useSystemNotifications() {
  const { showNotification, showError, showSuccess, showWarning } = useNotifications()
  
  const notifyConnectionStatus = (connected) => {
    if (connected) {
      showSuccess('Conexión restablecida', {
        duration: 3000
      })
    } else {
      showError('Conexión perdida', {
        persistent: true,
        actions: [{
          label: 'Reintentar',
          action: () => window.location.reload()
        }]
      })
    }
  }
  
  const notifyDataSaved = (entity = 'datos') => {
    showSuccess(`${entity} guardados correctamente`)
  }
  
  const notifyDataError = (entity = 'datos', error = null) => {
    const message = error ? `Error al guardar ${entity}: ${error}` : `Error al guardar ${entity}`
    showError(message)
  }
  
  const notifyValidationError = (errors) => {
    if (Array.isArray(errors)) {
      errors.forEach(error => showWarning(error))
    } else {
      showWarning(errors)
    }
  }
  
  const notifyPermissionDenied = (action = 'realizar esta acción') => {
    showWarning(`No tienes permisos para ${action}`)
  }
  
  const notifyMaintenanceMode = () => {
    showWarning('El sistema está en modo mantenimiento. Algunas funciones pueden no estar disponibles.', {
      persistent: true
    })
  }
  
  const notifyNewVersion = (version) => {
    showInfo(`Nueva versión disponible: ${version}`, {
      persistent: true,
      actions: [{
        label: 'Actualizar',
        action: () => window.location.reload()
      }, {
        label: 'Más tarde',
        action: () => {}
      }]
    })
  }
  
  return {
    notifyConnectionStatus,
    notifyDataSaved,
    notifyDataError,
    notifyValidationError,
    notifyPermissionDenied,
    notifyMaintenanceMode,
    notifyNewVersion
  }
}

// Composable para notificaciones de chat
export function useChatNotifications() {
  const { showNotification, showInfo, showWarning } = useNotifications()
  
  const notifyNewMessage = (senderName, preview) => {
    if (document.hidden) { // Solo mostrar si la página no está visible
      showNotification(`Nuevo mensaje de ${senderName}`, 'info', {
        duration: 5000,
        actions: [{
          label: 'Ver',
          action: () => {
            window.focus()
            // Aquí se podría navegar al chat específico
          }
        }]
      })
    }
  }
  
  const notifyTyping = (senderName) => {
    showInfo(`${senderName} está escribiendo...`, {
      duration: 2000,
      showProgress: false
    })
  }
  
  const notifyMessageFailed = (messageId) => {
    showWarning('No se pudo enviar el mensaje', {
      actions: [{
        label: 'Reintentar',
        action: () => {
          // Aquí se podría reintentar el envío
          console.log('Reintentando mensaje:', messageId)
        }
      }]
    })
  }
  
  const notifyUserJoined = (userName) => {
    showInfo(`${userName} se ha unido al chat`)
  }
  
  const notifyUserLeft = (userName) => {
    showInfo(`${userName} ha abandonado el chat`)
  }
  
  const notifyFileUploadProgress = (filename, progress) => {
    return showNotification(`Subiendo ${filename}...`, 'info', {
      persistent: true,
      showProgress: false // Usaremos nuestro propio indicador
    })
  }
  
  const notifyFileUploadComplete = (filename) => {
    showNotification(`${filename} subido correctamente`, 'success')
  }
  
  const notifyFileUploadError = (filename, error) => {
    showNotification(`Error al subir ${filename}: ${error}`, 'error')
  }
  
  return {
    notifyNewMessage,
    notifyTyping,
    notifyMessageFailed,
    notifyUserJoined,
    notifyUserLeft,
    notifyFileUploadProgress,
    notifyFileUploadComplete,
    notifyFileUploadError
  }
}

// Plugin para Vue (opcional)
export default {
  install(app) {
    const notifications = useNotifications()
    
    app.config.globalProperties.$notify = notifications.showNotification
    app.config.globalProperties.$notifySuccess = notifications.showSuccess
    app.config.globalProperties.$notifyError = notifications.showError
    app.config.globalProperties.$notifyWarning = notifications.showWarning
    app.config.globalProperties.$notifyInfo = notifications.showInfo
    
    app.provide('notifications', notifications)
  }
}