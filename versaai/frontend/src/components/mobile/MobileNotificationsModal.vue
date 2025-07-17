<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>
      
      <div class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
        <!-- Header -->
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Notificaciones</h3>
            <button
              @click="$emit('close')"
              class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <XMarkIcon class="h-6 w-6" />
            </button>
          </div>
          
          <!-- Notification Tabs -->
          <div class="flex space-x-1 bg-gray-100 rounded-lg p-1">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex-1 py-2 px-3 text-sm font-medium rounded-md transition-colors',
                activeTab === tab.id
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              {{ tab.name }}
              <span v-if="tab.count > 0" class="ml-2 bg-red-100 text-red-600 text-xs px-2 py-1 rounded-full">
                {{ tab.count }}
              </span>
            </button>
          </div>
        </div>
        
        <!-- Notifications List -->
        <div class="max-h-96 overflow-y-auto">
          <div class="divide-y divide-gray-200">
            <div
              v-for="notification in filteredNotifications"
              :key="notification.id"
              :class="[
                'px-4 py-4 hover:bg-gray-50 cursor-pointer',
                !notification.read ? 'bg-blue-50' : ''
              ]"
              @click="markAsRead(notification.id)"
            >
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center',
                    getNotificationColor(notification.type)
                  ]">
                    <component :is="getNotificationIcon(notification.type)" class="h-4 w-4" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p :class="[
                      'text-sm',
                      !notification.read ? 'font-medium text-gray-900' : 'text-gray-700'
                    ]">
                      {{ notification.title }}
                    </p>
                    <div class="flex items-center space-x-2">
                      <span class="text-xs text-gray-500">{{ formatTime(notification.timestamp) }}</span>
                      <div v-if="!notification.read" class="w-2 h-2 bg-blue-600 rounded-full"></div>
                    </div>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ notification.message }}</p>
                  <div v-if="notification.actions" class="flex space-x-2 mt-2">
                    <button
                      v-for="action in notification.actions"
                      :key="action.label"
                      @click.stop="handleAction(action, notification)"
                      :class="[
                        'text-xs px-3 py-1 rounded-md font-medium',
                        action.primary
                          ? 'bg-blue-600 text-white hover:bg-blue-700'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      ]"
                    >
                      {{ action.label }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredNotifications.length === 0" class="px-4 py-8 text-center">
            <BellIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">No hay notificaciones</h3>
            <p class="mt-1 text-sm text-gray-500">No tienes notificaciones {{ activeTab === 'unread' ? 'sin leer' : 'en esta categoría' }}.</p>
          </div>
        </div>
        
        <!-- Footer Actions -->
        <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
          <button
            @click="markAllAsRead"
            :disabled="unreadCount === 0"
            class="inline-flex w-full justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Marcar todas como leídas
          </button>
          <button
            @click="$emit('close')"
            class="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sm:mt-0 sm:w-auto sm:text-sm"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import {
  XMarkIcon,
  BellIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

const emit = defineEmits(['close'])

// Reactive data
const activeTab = ref('all')

const tabs = [
  { id: 'all', name: 'Todas', count: 0 },
  { id: 'unread', name: 'Sin leer', count: 3 },
  { id: 'important', name: 'Importantes', count: 1 }
]

const notifications = reactive([
  {
    id: 1,
    type: 'conversation',
    title: 'Nueva conversación',
    message: 'Un usuario ha iniciado una nueva conversación en el chatbot "Soporte"',
    timestamp: new Date(Date.now() - 5 * 60 * 1000),
    read: false,
    important: false,
    actions: [
      { label: 'Ver conversación', primary: true, action: 'view-conversation' },
      { label: 'Ignorar', primary: false, action: 'dismiss' }
    ]
  },
  {
    id: 2,
    type: 'user',
    title: 'Nuevo miembro del equipo',
    message: 'Carlos Rodríguez se ha unido a tu organización',
    timestamp: new Date(Date.now() - 15 * 60 * 1000),
    read: false,
    important: false,
    actions: [
      { label: 'Ver perfil', primary: true, action: 'view-profile' }
    ]
  },
  {
    id: 3,
    type: 'warning',
    title: 'Límite de uso alcanzado',
    message: 'Has alcanzado el 90% de tu límite mensual de conversaciones',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    read: false,
    important: true,
    actions: [
      { label: 'Actualizar plan', primary: true, action: 'upgrade-plan' },
      { label: 'Ver detalles', primary: false, action: 'view-usage' }
    ]
  },
  {
    id: 4,
    type: 'info',
    title: 'Actualización disponible',
    message: 'Nueva versión de VersaAI disponible con mejoras de rendimiento',
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    read: true,
    important: false,
    actions: [
      { label: 'Ver cambios', primary: true, action: 'view-changelog' }
    ]
  },
  {
    id: 5,
    type: 'success',
    title: 'Backup completado',
    message: 'El backup automático de tus datos se ha completado exitosamente',
    timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    read: true,
    important: false
  }
])

// Computed
const filteredNotifications = computed(() => {
  switch (activeTab.value) {
    case 'unread':
      return notifications.filter(n => !n.read)
    case 'important':
      return notifications.filter(n => n.important)
    default:
      return notifications
  }
})

const unreadCount = computed(() => {
  return notifications.filter(n => !n.read).length
})

// Methods
const getNotificationIcon = (type) => {
  switch (type) {
    case 'conversation':
      return ChatBubbleLeftRightIcon
    case 'user':
      return UserGroupIcon
    case 'warning':
      return ExclamationTriangleIcon
    case 'success':
      return CheckCircleIcon
    default:
      return InformationCircleIcon
  }
}

const getNotificationColor = (type) => {
  switch (type) {
    case 'conversation':
      return 'bg-blue-100 text-blue-600'
    case 'user':
      return 'bg-green-100 text-green-600'
    case 'warning':
      return 'bg-yellow-100 text-yellow-600'
    case 'success':
      return 'bg-green-100 text-green-600'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 60) {
    return `${minutes}m`
  } else if (hours < 24) {
    return `${hours}h`
  } else {
    return `${days}d`
  }
}

const markAsRead = (notificationId) => {
  const notification = notifications.find(n => n.id === notificationId)
  if (notification) {
    notification.read = true
  }
  updateTabCounts()
}

const markAllAsRead = () => {
  notifications.forEach(n => {
    n.read = true
  })
  updateTabCounts()
}

const handleAction = (action, notification) => {
  console.log('Action:', action.action, 'Notification:', notification.id)
  
  switch (action.action) {
    case 'view-conversation':
      // Navigate to conversation
      break
    case 'view-profile':
      // Navigate to user profile
      break
    case 'upgrade-plan':
      // Navigate to billing
      break
    case 'view-usage':
      // Navigate to usage stats
      break
    case 'view-changelog':
      // Open changelog
      break
    case 'dismiss':
      markAsRead(notification.id)
      break
  }
}

const updateTabCounts = () => {
  tabs[1].count = notifications.filter(n => !n.read).length
  tabs[2].count = notifications.filter(n => n.important && !n.read).length
}

// Initialize tab counts
updateTabCounts()
</script>

<style scoped>
/* Custom scrollbar for mobile */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>