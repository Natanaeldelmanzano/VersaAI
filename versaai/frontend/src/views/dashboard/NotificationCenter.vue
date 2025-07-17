<template>
  <div class="p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Centro de Notificaciones</h1>
        <p class="text-gray-600 mt-1">Gestiona todas tus notificaciones y alertas</p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button
          @click="markAllAsRead"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
        >
          <CheckIcon class="h-4 w-4" />
          <span>Marcar todo como leído</span>
        </button>
        <button
          @click="showSettings = true"
          class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center space-x-2"
        >
          <Cog6ToothIcon class="h-4 w-4" />
          <span>Configuración</span>
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-blue-100 rounded-lg">
            <BellIcon class="h-6 w-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-red-100 rounded-lg">
            <ExclamationCircleIcon class="h-6 w-6 text-red-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Sin leer</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.unread }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-yellow-100 rounded-lg">
            <ClockIcon class="h-6 w-6 text-yellow-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Hoy</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.today }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="p-2 bg-green-100 rounded-lg">
            <CheckCircleIcon class="h-6 w-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Leídas</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats.read }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex items-center space-x-2">
          <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar notificaciones..."
            class="border-0 focus:ring-0 focus:outline-none text-sm"
          />
        </div>
        
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Tipo:</label>
          <select
            v-model="selectedType"
            class="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todos</option>
            <option value="system">Sistema</option>
            <option value="chat">Chat</option>
            <option value="billing">Facturación</option>
            <option value="security">Seguridad</option>
            <option value="update">Actualizaciones</option>
          </select>
        </div>
        
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Estado:</label>
          <select
            v-model="selectedStatus"
            class="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todos</option>
            <option value="unread">Sin leer</option>
            <option value="read">Leídas</option>
          </select>
        </div>
        
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Prioridad:</label>
          <select
            v-model="selectedPriority"
            class="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todas</option>
            <option value="high">Alta</option>
            <option value="medium">Media</option>
            <option value="low">Baja</option>
          </select>
        </div>
        
        <button
          @click="clearFilters"
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          Limpiar filtros
        </button>
      </div>
    </div>

    <!-- Notifications List -->
    <div class="bg-white rounded-lg shadow">
      <div class="divide-y divide-gray-200">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          :class="[
            'p-4 hover:bg-gray-50 transition-colors cursor-pointer',
            !notification.read ? 'bg-blue-50' : ''
          ]"
          @click="markAsRead(notification)"
        >
          <div class="flex items-start space-x-4">
            <!-- Icon -->
            <div :class="[
              'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center',
              getNotificationColor(notification.type, notification.priority)
            ]">
              <component :is="getNotificationIcon(notification.type)" class="h-5 w-5" />
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <h3 :class="[
                    'text-sm font-medium',
                    !notification.read ? 'text-gray-900' : 'text-gray-700'
                  ]">
                    {{ notification.title }}
                  </h3>
                  <span v-if="!notification.read" class="w-2 h-2 bg-blue-600 rounded-full"></span>
                </div>
                
                <div class="flex items-center space-x-2">
                  <span :class="[
                    'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                    getPriorityColor(notification.priority)
                  ]">
                    {{ getPriorityLabel(notification.priority) }}
                  </span>
                  <span class="text-xs text-gray-500">
                    {{ formatDate(notification.createdAt) }}
                  </span>
                </div>
              </div>
              
              <p class="text-sm text-gray-600 mt-1">{{ notification.message }}</p>
              
              <div v-if="notification.actions && notification.actions.length" class="flex items-center space-x-2 mt-3">
                <button
                  v-for="action in notification.actions"
                  :key="action.id"
                  @click.stop="handleAction(notification, action)"
                  :class="[
                    'px-3 py-1 rounded text-xs font-medium',
                    action.type === 'primary' ? 'bg-blue-600 text-white hover:bg-blue-700' :
                    action.type === 'danger' ? 'bg-red-600 text-white hover:bg-red-700' :
                    'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  ]"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center space-x-2">
              <button
                @click.stop="toggleRead(notification)"
                class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                :title="notification.read ? 'Marcar como no leída' : 'Marcar como leída'"
              >
                <component :is="notification.read ? EyeSlashIcon : EyeIcon" class="h-4 w-4" />
              </button>
              <button
                @click.stop="deleteNotification(notification)"
                class="p-1 text-gray-400 hover:text-red-600 transition-colors"
                title="Eliminar"
              >
                <TrashIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="filteredNotifications.length === 0" class="p-8 text-center">
          <BellSlashIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">No hay notificaciones</h3>
          <p class="text-gray-600">No se encontraron notificaciones que coincidan con los filtros.</p>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between mt-6">
      <div class="text-sm text-gray-700">
        Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredNotifications.length) }} de {{ filteredNotifications.length }} notificaciones
      </div>
      
      <div class="flex items-center space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Anterior
        </button>
        
        <span class="px-3 py-2 text-sm font-medium text-gray-700">
          {{ currentPage }} de {{ totalPages }}
        </span>
        
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Siguiente
        </button>
      </div>
    </div>

    <!-- Settings Modal -->
    <NotificationSettings
      v-if="showSettings"
      @close="showSettings = false"
      @save="updateSettings"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  BellIcon,
  BellSlashIcon,
  CheckIcon,
  Cog6ToothIcon,
  ExclamationCircleIcon,
  ClockIcon,
  CheckCircleIcon,
  MagnifyingGlassIcon,
  EyeIcon,
  EyeSlashIcon,
  TrashIcon,
  ChatBubbleLeftRightIcon,
  CreditCardIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  ComputerDesktopIcon
} from '@heroicons/vue/24/outline'
import NotificationSettings from '@/components/dashboard/NotificationSettings.vue'

// Reactive state
const searchQuery = ref('')
const selectedType = ref('')
const selectedStatus = ref('')
const selectedPriority = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(20)
const showSettings = ref(false)

const stats = ref({
  total: 156,
  unread: 23,
  today: 12,
  read: 133
})

const notifications = ref([
  {
    id: 1,
    type: 'system',
    priority: 'high',
    title: 'Actualización del sistema disponible',
    message: 'Una nueva versión del sistema está disponible. Se recomienda actualizar para obtener las últimas funcionalidades.',
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 30),
    actions: [
      { id: 1, label: 'Actualizar ahora', type: 'primary' },
      { id: 2, label: 'Recordar más tarde', type: 'secondary' }
    ]
  },
  {
    id: 2,
    type: 'chat',
    priority: 'medium',
    title: 'Nueva conversación iniciada',
    message: 'Un usuario ha iniciado una nueva conversación en el chatbot "Soporte Técnico".',
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 45),
    actions: [
      { id: 1, label: 'Ver conversación', type: 'primary' }
    ]
  },
  {
    id: 3,
    type: 'billing',
    priority: 'high',
    title: 'Pago pendiente',
    message: 'Tu suscripción vence en 3 días. Actualiza tu método de pago para evitar interrupciones.',
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2),
    actions: [
      { id: 1, label: 'Actualizar pago', type: 'primary' },
      { id: 2, label: 'Ver factura', type: 'secondary' }
    ]
  },
  {
    id: 4,
    type: 'security',
    priority: 'medium',
    title: 'Nuevo inicio de sesión detectado',
    message: 'Se detectó un inicio de sesión desde una nueva ubicación: Madrid, España.',
    read: true,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4),
    actions: [
      { id: 1, label: 'Revisar actividad', type: 'primary' }
    ]
  },
  {
    id: 5,
    type: 'update',
    priority: 'low',
    title: 'Nuevas funcionalidades disponibles',
    message: 'Hemos añadido nuevas funcionalidades de análisis avanzado a tu dashboard.',
    read: true,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 6)
  }
])

// Computed
const filteredNotifications = computed(() => {
  let filtered = notifications.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(n => 
      n.title.toLowerCase().includes(query) ||
      n.message.toLowerCase().includes(query)
    )
  }
  
  if (selectedType.value) {
    filtered = filtered.filter(n => n.type === selectedType.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(n => 
      selectedStatus.value === 'read' ? n.read : !n.read
    )
  }
  
  if (selectedPriority.value) {
    filtered = filtered.filter(n => n.priority === selectedPriority.value)
  }
  
  return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const totalPages = computed(() => {
  return Math.ceil(filteredNotifications.value.length / itemsPerPage.value)
})

// Methods
const getNotificationIcon = (type) => {
  const icons = {
    system: ComputerDesktopIcon,
    chat: ChatBubbleLeftRightIcon,
    billing: CreditCardIcon,
    security: ShieldCheckIcon,
    update: ArrowPathIcon
  }
  return icons[type] || BellIcon
}

const getNotificationColor = (type, priority) => {
  const baseColors = {
    system: 'bg-blue-100 text-blue-600',
    chat: 'bg-green-100 text-green-600',
    billing: 'bg-yellow-100 text-yellow-600',
    security: 'bg-red-100 text-red-600',
    update: 'bg-purple-100 text-purple-600'
  }
  
  if (priority === 'high') {
    return 'bg-red-100 text-red-600'
  }
  
  return baseColors[type] || 'bg-gray-100 text-gray-600'
}

const getPriorityColor = (priority) => {
  const colors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return colors[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityLabel = (priority) => {
  const labels = {
    high: 'Alta',
    medium: 'Media',
    low: 'Baja'
  }
  return labels[priority] || 'Normal'
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 60) {
    return `hace ${minutes} min`
  } else if (hours < 24) {
    return `hace ${hours}h`
  } else if (days < 7) {
    return `hace ${days}d`
  } else {
    return new Intl.DateTimeFormat('es-ES', {
      month: 'short',
      day: 'numeric'
    }).format(date)
  }
}

const markAsRead = (notification) => {
  if (!notification.read) {
    notification.read = true
    stats.value.unread--
    stats.value.read++
  }
}

const toggleRead = (notification) => {
  notification.read = !notification.read
  if (notification.read) {
    stats.value.unread--
    stats.value.read++
  } else {
    stats.value.unread++
    stats.value.read--
  }
}

const deleteNotification = (notification) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta notificación?')) {
    const index = notifications.value.findIndex(n => n.id === notification.id)
    if (index > -1) {
      notifications.value.splice(index, 1)
      stats.value.total--
      if (!notification.read) {
        stats.value.unread--
      } else {
        stats.value.read--
      }
    }
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    if (!notification.read) {
      notification.read = true
    }
  })
  stats.value.read = stats.value.total
  stats.value.unread = 0
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedType.value = ''
  selectedStatus.value = ''
  selectedPriority.value = ''
  currentPage.value = 1
}

const handleAction = (notification, action) => {
  console.log('Handle action:', action.label, 'for notification:', notification.title)
  // TODO: Implement specific actions based on action type
  
  switch (action.label) {
    case 'Actualizar ahora':
      // Handle system update
      break
    case 'Ver conversación':
      // Navigate to conversation
      break
    case 'Actualizar pago':
      // Navigate to billing
      break
    case 'Revisar actividad':
      // Navigate to security logs
      break
  }
}

const updateSettings = (settings) => {
  console.log('Update notification settings:', settings)
  // TODO: Save settings to API
  showSettings.value = false
}

// Initialize
onMounted(() => {
  // TODO: Load notifications from API
  console.log('NotificationCenter mounted')
})
</script>