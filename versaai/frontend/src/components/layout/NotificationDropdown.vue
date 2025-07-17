<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton class="relative p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-full">
        <span class="sr-only">Ver notificaciones</span>
        <BellIcon class="h-6 w-6" aria-hidden="true" />
        <span
          v-if="unreadCount > 0"
          class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
        >
          {{ unreadCount > 9 ? '9+' : unreadCount }}
        </span>
      </MenuButton>
    </div>

    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <MenuItems class="absolute right-0 z-10 mt-2 w-80 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
        <div class="py-1">
          <div class="px-4 py-3 border-b border-gray-200">
            <h3 class="text-sm font-medium text-gray-900">Notificaciones</h3>
            <p class="text-xs text-gray-500">{{ unreadCount }} sin leer</p>
          </div>
          
          <div class="max-h-96 overflow-y-auto">
            <div v-if="notifications.length === 0" class="px-4 py-6 text-center">
              <BellIcon class="mx-auto h-12 w-12 text-gray-400" />
              <h3 class="mt-2 text-sm font-medium text-gray-900">No hay notificaciones</h3>
              <p class="mt-1 text-sm text-gray-500">Cuando tengas notificaciones, aparecerán aquí.</p>
            </div>
            
            <MenuItem
              v-for="notification in notifications"
              :key="notification.id"
              v-slot="{ active }"
            >
              <div
                :class="[
                  active ? 'bg-gray-50' : '',
                  'block px-4 py-3 text-sm cursor-pointer border-b border-gray-100 last:border-b-0'
                ]"
                @click="markAsRead(notification.id)"
              >
                <div class="flex items-start space-x-3">
                  <div class="flex-shrink-0">
                    <div
                      :class="[
                        getNotificationColor(notification.type),
                        'h-8 w-8 rounded-full flex items-center justify-center'
                      ]"
                    >
                      <component
                        :is="getNotificationIcon(notification.type)"
                        class="h-4 w-4 text-white"
                      />
                    </div>
                  </div>
                  <div class="min-w-0 flex-1">
                    <p
                      :class="[
                        notification.read ? 'text-gray-600' : 'text-gray-900 font-medium',
                        'text-sm'
                      ]"
                    >
                      {{ notification.title }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">{{ notification.message }}</p>
                    <p class="text-xs text-gray-400 mt-1">{{ formatTime(notification.createdAt) }}</p>
                  </div>
                  <div v-if="!notification.read" class="flex-shrink-0">
                    <div class="h-2 w-2 bg-primary-500 rounded-full"></div>
                  </div>
                </div>
              </div>
            </MenuItem>
          </div>
          
          <div v-if="notifications.length > 0" class="px-4 py-3 border-t border-gray-200">
            <button
              @click="markAllAsRead"
              class="text-sm text-primary-600 hover:text-primary-500 font-medium"
            >
              Marcar todas como leídas
            </button>
          </div>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  BellIcon,
  ChatBubbleLeftRightIcon,
  UserIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'
import { formatDistanceToNow } from 'date-fns'
import { es } from 'date-fns/locale'

const notifications = ref([
  {
    id: 1,
    type: 'success',
    title: 'Chatbot creado exitosamente',
    message: 'Tu nuevo chatbot "Asistente de Ventas" está listo para usar.',
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 30) // 30 minutos atrás
  },
  {
    id: 2,
    type: 'info',
    title: 'Nuevo usuario registrado',
    message: 'juan.perez@email.com se ha registrado en tu organización.',
    read: false,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 horas atrás
  },
  {
    id: 3,
    type: 'warning',
    title: 'Límite de uso alcanzado',
    message: 'Has alcanzado el 80% de tu límite mensual de conversaciones.',
    read: true,
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24) // 1 día atrás
  }
])

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
}

const getNotificationIcon = (type) => {
  const icons = {
    success: CheckCircleIcon,
    info: InformationCircleIcon,
    warning: ExclamationTriangleIcon,
    error: ExclamationTriangleIcon,
    user: UserIcon,
    chat: ChatBubbleLeftRightIcon
  }
  return icons[type] || InformationCircleIcon
}

const getNotificationColor = (type) => {
  const colors = {
    success: 'bg-green-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
    user: 'bg-purple-500',
    chat: 'bg-primary-500'
  }
  return colors[type] || 'bg-gray-500'
}

const formatTime = (date) => {
  return formatDistanceToNow(date, { addSuffix: true, locale: es })
}

onMounted(() => {
  // Aquí podrías cargar las notificaciones desde la API
})
</script>