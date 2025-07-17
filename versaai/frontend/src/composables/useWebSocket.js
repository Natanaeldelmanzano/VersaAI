import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore } from '@/stores/dashboard'

/**
 * Composable para manejo de WebSocket en tiempo real
 * Proporciona conexión persistente, reconexión automática y manejo de eventos
 */
export function useWebSocket(url = null, options = {}) {
  const authStore = useAuthStore()
  const dashboardStore = useDashboardStore()

  // Estado reactivo
  const isConnected = ref(false)
  const isConnecting = ref(false)
  const connectionError = ref(null)
  const lastMessage = ref(null)
  const messageHistory = ref([])
  const reconnectAttempts = ref(0)
  const latency = ref(0)

  // Configuración por defecto
  const defaultOptions = {
    autoConnect: true,
    reconnect: true,
    maxReconnectAttempts: 5,
    reconnectInterval: 3000,
    heartbeatInterval: 30000,
    timeout: 10000,
    protocols: [],
    debug: false
  }

  const config = reactive({ ...defaultOptions, ...options })

  // Referencias internas
  let socket = null
  let reconnectTimer = null
  let heartbeatTimer = null
  let heartbeatResponse = null
  let pingTime = 0

  // Event listeners
  const listeners = reactive({
    open: [],
    message: [],
    close: [],
    error: [],
    reconnect: []
  })

  /**
   * Construir URL del WebSocket
   */
  const buildWebSocketUrl = () => {
    if (url) return url

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const token = authStore.token
    const userId = authStore.user?.id
    
    return `${protocol}//${host}/ws?token=${token}&userId=${userId}`
  }

  /**
   * Log de debug
   */
  const debugLog = (message, data = null) => {
    if (config.debug) {
      console.log(`[WebSocket] ${message}`, data || '')
    }
  }

  /**
   * Conectar WebSocket
   */
  const connect = () => {
    if (socket && (socket.readyState === WebSocket.CONNECTING || socket.readyState === WebSocket.OPEN)) {
      debugLog('Ya existe una conexión activa')
      return
    }

    isConnecting.value = true
    connectionError.value = null
    debugLog('Iniciando conexión...')

    try {
      const wsUrl = buildWebSocketUrl()
      socket = new WebSocket(wsUrl, config.protocols)

      // Timeout para la conexión
      const connectionTimeout = setTimeout(() => {
        if (socket.readyState === WebSocket.CONNECTING) {
          socket.close()
          handleConnectionError(new Error('Timeout de conexión'))
        }
      }, config.timeout)

      socket.onopen = (event) => {
        clearTimeout(connectionTimeout)
        isConnected.value = true
        isConnecting.value = false
        reconnectAttempts.value = 0
        connectionError.value = null
        
        debugLog('Conexión establecida')
        
        // Iniciar heartbeat
        startHeartbeat()
        
        // Notificar listeners
        listeners.open.forEach(callback => callback(event))
        
        // Enviar información de autenticación
        if (authStore.isAuthenticated) {
          send({
            type: 'auth',
            token: authStore.token,
            userId: authStore.user.id,
            timestamp: Date.now()
          })
        }
      }

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          lastMessage.value = data
          messageHistory.value.push({
            ...data,
            receivedAt: Date.now()
          })

          // Mantener solo los últimos 100 mensajes
          if (messageHistory.value.length > 100) {
            messageHistory.value = messageHistory.value.slice(-100)
          }

          debugLog('Mensaje recibido:', data)

          // Manejar mensajes especiales
          handleSpecialMessages(data)

          // Notificar listeners
          listeners.message.forEach(callback => callback(data, event))
        } catch (error) {
          debugLog('Error parseando mensaje:', error)
        }
      }

      socket.onclose = (event) => {
        clearTimeout(connectionTimeout)
        isConnected.value = false
        isConnecting.value = false
        stopHeartbeat()
        
        debugLog('Conexión cerrada:', { code: event.code, reason: event.reason })
        
        // Notificar listeners
        listeners.close.forEach(callback => callback(event))
        
        // Intentar reconectar si no fue cierre manual
        if (event.code !== 1000 && config.reconnect) {
          scheduleReconnect()
        }
      }

      socket.onerror = (event) => {
        debugLog('Error de WebSocket:', event)
        handleConnectionError(new Error('Error de conexión WebSocket'))
      }

    } catch (error) {
      handleConnectionError(error)
    }
  }

  /**
   * Desconectar WebSocket
   */
  const disconnect = () => {
    debugLog('Desconectando...')
    
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    
    stopHeartbeat()
    
    if (socket) {
      socket.close(1000, 'Desconexión manual')
      socket = null
    }
    
    isConnected.value = false
    isConnecting.value = false
  }

  /**
   * Enviar mensaje
   */
  const send = (data) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      debugLog('No se puede enviar: WebSocket no conectado')
      return false
    }

    try {
      const message = typeof data === 'string' ? data : JSON.stringify(data)
      socket.send(message)
      debugLog('Mensaje enviado:', data)
      return true
    } catch (error) {
      debugLog('Error enviando mensaje:', error)
      return false
    }
  }

  /**
   * Manejar errores de conexión
   */
  const handleConnectionError = (error) => {
    isConnecting.value = false
    connectionError.value = error.message
    debugLog('Error de conexión:', error)
    
    listeners.error.forEach(callback => callback(error))
    
    if (config.reconnect) {
      scheduleReconnect()
    }
  }

  /**
   * Programar reconexión
   */
  const scheduleReconnect = () => {
    if (reconnectAttempts.value >= config.maxReconnectAttempts) {
      debugLog('Máximo número de intentos de reconexión alcanzado')
      connectionError.value = 'No se pudo reconectar después de múltiples intentos'
      return
    }

    reconnectAttempts.value++
    const delay = config.reconnectInterval * Math.pow(1.5, reconnectAttempts.value - 1)
    
    debugLog(`Reconectando en ${delay}ms (intento ${reconnectAttempts.value})`)
    
    reconnectTimer = setTimeout(() => {
      listeners.reconnect.forEach(callback => callback(reconnectAttempts.value))
      connect()
    }, delay)
  }

  /**
   * Iniciar heartbeat
   */
  const startHeartbeat = () => {
    if (!config.heartbeatInterval) return
    
    heartbeatTimer = setInterval(() => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        pingTime = Date.now()
        send({ type: 'ping', timestamp: pingTime })
        
        // Timeout para pong
        heartbeatResponse = setTimeout(() => {
          debugLog('Heartbeat timeout - reconectando')
          socket.close()
        }, 5000)
      }
    }, config.heartbeatInterval)
  }

  /**
   * Detener heartbeat
   */
  const stopHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
      heartbeatTimer = null
    }
    
    if (heartbeatResponse) {
      clearTimeout(heartbeatResponse)
      heartbeatResponse = null
    }
  }

  /**
   * Manejar mensajes especiales del sistema
   */
  const handleSpecialMessages = (data) => {
    switch (data.type) {
      case 'pong':
        if (heartbeatResponse) {
          clearTimeout(heartbeatResponse)
          heartbeatResponse = null
        }
        if (pingTime) {
          latency.value = Date.now() - pingTime
        }
        break
        
      case 'metrics_update':
        // Actualizar métricas en tiempo real
        if (data.metrics) {
          dashboardStore.updateRealTimeMetrics(data.metrics)
        }
        break
        
      case 'notification':
        // Manejar notificaciones
        if (data.notification) {
          dashboardStore.addNotification(data.notification)
        }
        break
        
      case 'user_activity':
        // Actualizar actividad de usuarios
        if (data.activity) {
          dashboardStore.updateUserActivity(data.activity)
        }
        break
        
      case 'system_alert':
        // Alertas del sistema
        if (data.alert) {
          dashboardStore.addSystemAlert(data.alert)
        }
        break
        
      case 'chat_message':
        // Nuevos mensajes de chat
        if (data.message) {
          dashboardStore.addChatMessage(data.message)
        }
        break
    }
  }

  /**
   * Agregar listener de eventos
   */
  const on = (event, callback) => {
    if (listeners[event]) {
      listeners[event].push(callback)
    }
  }

  /**
   * Remover listener de eventos
   */
  const off = (event, callback) => {
    if (listeners[event]) {
      const index = listeners[event].indexOf(callback)
      if (index > -1) {
        listeners[event].splice(index, 1)
      }
    }
  }

  /**
   * Limpiar todos los listeners
   */
  const clearListeners = () => {
    Object.keys(listeners).forEach(event => {
      listeners[event] = []
    })
  }

  /**
   * Obtener estado de la conexión
   */
  const getConnectionState = () => {
    if (!socket) return 'CLOSED'
    
    switch (socket.readyState) {
      case WebSocket.CONNECTING: return 'CONNECTING'
      case WebSocket.OPEN: return 'OPEN'
      case WebSocket.CLOSING: return 'CLOSING'
      case WebSocket.CLOSED: return 'CLOSED'
      default: return 'UNKNOWN'
    }
  }

  /**
   * Métodos de conveniencia para eventos específicos
   */
  const onMessage = (callback) => on('message', callback)
  const onOpen = (callback) => on('open', callback)
  const onClose = (callback) => on('close', callback)
  const onError = (callback) => on('error', callback)
  const onReconnect = (callback) => on('reconnect', callback)

  // Watchers
  watch(() => authStore.isAuthenticated, (isAuth) => {
    if (isAuth && config.autoConnect && !isConnected.value) {
      connect()
    } else if (!isAuth && isConnected.value) {
      disconnect()
    }
  })

  // Lifecycle hooks
  onMounted(() => {
    if (config.autoConnect && authStore.isAuthenticated) {
      connect()
    }
  })

  onUnmounted(() => {
    disconnect()
    clearListeners()
  })

  // API pública
  return {
    // Estado
    isConnected,
    isConnecting,
    connectionError,
    lastMessage,
    messageHistory,
    reconnectAttempts,
    latency,
    
    // Métodos
    connect,
    disconnect,
    send,
    
    // Event listeners
    on,
    off,
    onMessage,
    onOpen,
    onClose,
    onError,
    onReconnect,
    clearListeners,
    
    // Utilidades
    getConnectionState,
    config
  }
}

/**
 * Composable específico para métricas en tiempo real
 */
export function useRealTimeMetrics() {
  const { send, onMessage, isConnected } = useWebSocket()
  const metrics = ref({})
  const lastUpdate = ref(null)

  // Suscribirse a actualizaciones de métricas
  const subscribeToMetrics = (metricTypes = []) => {
    if (isConnected.value) {
      send({
        type: 'subscribe_metrics',
        metrics: metricTypes,
        timestamp: Date.now()
      })
    }
  }

  // Desuscribirse de métricas
  const unsubscribeFromMetrics = (metricTypes = []) => {
    if (isConnected.value) {
      send({
        type: 'unsubscribe_metrics',
        metrics: metricTypes,
        timestamp: Date.now()
      })
    }
  }

  // Manejar actualizaciones de métricas
  onMessage((data) => {
    if (data.type === 'metrics_update') {
      metrics.value = { ...metrics.value, ...data.metrics }
      lastUpdate.value = new Date(data.timestamp)
    }
  })

  return {
    metrics,
    lastUpdate,
    subscribeToMetrics,
    unsubscribeFromMetrics,
    isConnected
  }
}

/**
 * Composable para notificaciones en tiempo real
 */
export function useRealTimeNotifications() {
  const { onMessage, isConnected } = useWebSocket()
  const notifications = ref([])
  const unreadCount = ref(0)

  // Manejar nuevas notificaciones
  onMessage((data) => {
    if (data.type === 'notification') {
      notifications.value.unshift(data.notification)
      unreadCount.value++
      
      // Mantener solo las últimas 50 notificaciones
      if (notifications.value.length > 50) {
        notifications.value = notifications.value.slice(0, 50)
      }
    }
  })

  // Marcar como leídas
  const markAsRead = (notificationIds = []) => {
    notifications.value.forEach(notification => {
      if (notificationIds.length === 0 || notificationIds.includes(notification.id)) {
        notification.read = true
      }
    })
    unreadCount.value = notifications.value.filter(n => !n.read).length
  }

  // Limpiar notificaciones
  const clearNotifications = () => {
    notifications.value = []
    unreadCount.value = 0
  }

  return {
    notifications,
    unreadCount,
    markAsRead,
    clearNotifications,
    isConnected
  }
}