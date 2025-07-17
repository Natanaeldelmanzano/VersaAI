<template>
  <div class="mobile-dashboard min-h-screen bg-gray-50">
    <!-- Mobile Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="px-4 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <button
              @click="toggleSidebar"
              class="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            >
              <Bars3Icon class="h-6 w-6" />
            </button>
            <h1 class="text-lg font-semibold text-gray-900">{{ currentPageTitle }}</h1>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="showNotifications = true"
              class="relative p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            >
              <BellIcon class="h-6 w-6" />
              <span v-if="unreadNotifications > 0" class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
              </span>
            </button>
            <button
              @click="showProfile = true"
              class="p-1 rounded-full"
            >
              <img class="h-8 w-8 rounded-full" :src="user.avatar" :alt="user.name" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 lg:hidden"
      @click="sidebarOpen = false"
    >
      <div class="fixed inset-0 bg-gray-600 bg-opacity-75"></div>
    </div>

    <!-- Mobile Sidebar -->
    <div
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:hidden',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="flex flex-col h-full">
        <!-- Sidebar Header -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">V</span>
            </div>
            <span class="text-lg font-semibold text-gray-900">VersaAI</span>
          </div>
          <button
            @click="sidebarOpen = false"
            class="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            <XMarkIcon class="h-5 w-5" />
          </button>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-4 py-4 space-y-2 overflow-y-auto">
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            @click="sidebarOpen = false"
            :class="[
              $route.path === item.href
                ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                : 'text-gray-700 hover:bg-gray-50',
              'group flex items-center px-3 py-2 text-sm font-medium rounded-md'
            ]"
          >
            <component
              :is="item.icon"
              :class="[
                $route.path === item.href ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500',
                'mr-3 h-5 w-5'
              ]"
            />
            {{ item.name }}
            <span v-if="item.badge" class="ml-auto bg-red-100 text-red-600 text-xs px-2 py-1 rounded-full">
              {{ item.badge }}
            </span>
          </router-link>
        </nav>

        <!-- User Info -->
        <div class="p-4 border-t border-gray-200">
          <div class="flex items-center space-x-3">
            <img class="h-10 w-10 rounded-full" :src="user.avatar" :alt="user.name" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ user.name }}</p>
              <p class="text-xs text-gray-500 truncate">{{ user.email }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="pb-20">
      <!-- Quick Stats Cards -->
      <div class="p-4">
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <ChatBubbleLeftRightIcon class="h-5 w-5 text-blue-600" />
                </div>
              </div>
              <div class="ml-3">
                <p class="text-xs text-gray-600">Conversaciones</p>
                <p class="text-lg font-semibold text-gray-900">{{ stats.conversations }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <UserGroupIcon class="h-5 w-5 text-green-600" />
                </div>
              </div>
              <div class="ml-3">
                <p class="text-xs text-gray-600">Usuarios</p>
                <p class="text-lg font-semibold text-gray-900">{{ stats.users }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <ChartBarIcon class="h-5 w-5 text-purple-600" />
                </div>
              </div>
              <div class="ml-3">
                <p class="text-xs text-gray-600">Satisfacción</p>
                <p class="text-lg font-semibold text-gray-900">{{ stats.satisfaction }}%</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                  <ClockIcon class="h-5 w-5 text-orange-600" />
                </div>
              </div>
              <div class="ml-3">
                <p class="text-xs text-gray-600">Tiempo Resp.</p>
                <p class="text-lg font-semibold text-gray-900">{{ stats.responseTime }}s</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div class="px-4 py-3 border-b border-gray-200">
            <h3 class="text-sm font-medium text-gray-900">Actividad Reciente</h3>
          </div>
          <div class="divide-y divide-gray-200">
            <div
              v-for="activity in recentActivity"
              :key="activity.id"
              class="px-4 py-3 hover:bg-gray-50"
            >
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center',
                    activity.type === 'conversation' ? 'bg-blue-100' : 
                    activity.type === 'user' ? 'bg-green-100' : 'bg-purple-100'
                  ]">
                    <component
                      :is="activity.icon"
                      :class="[
                        'h-4 w-4',
                        activity.type === 'conversation' ? 'text-blue-600' : 
                        activity.type === 'user' ? 'text-green-600' : 'text-purple-600'
                      ]"
                    />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-900">{{ activity.title }}</p>
                  <p class="text-xs text-gray-500">{{ activity.description }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ formatTime(activity.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-4 py-3 border-b border-gray-200">
            <h3 class="text-sm font-medium text-gray-900">Acciones Rápidas</h3>
          </div>
          <div class="p-4">
            <div class="grid grid-cols-2 gap-3">
              <button
                @click="quickAction('new-chatbot')"
                class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <PlusIcon class="h-6 w-6 text-blue-600 mb-2" />
                <span class="text-xs text-gray-700">Nuevo Chatbot</span>
              </button>
              <button
                @click="quickAction('view-analytics')"
                class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <ChartBarIcon class="h-6 w-6 text-green-600 mb-2" />
                <span class="text-xs text-gray-700">Ver Analytics</span>
              </button>
              <button
                @click="quickAction('manage-users')"
                class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <UserGroupIcon class="h-6 w-6 text-purple-600 mb-2" />
                <span class="text-xs text-gray-700">Gestionar Usuarios</span>
              </button>
              <button
                @click="quickAction('settings')"
                class="flex flex-col items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <CogIcon class="h-6 w-6 text-orange-600 mb-2" />
                <span class="text-xs text-gray-700">Configuración</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-40">
      <div class="grid grid-cols-5 h-16">
        <router-link
          v-for="item in bottomNavigation"
          :key="item.name"
          :to="item.href"
          :class="[
            'flex flex-col items-center justify-center space-y-1',
            $route.path === item.href ? 'text-blue-600' : 'text-gray-600'
          ]"
        >
          <component
            :is="item.icon"
            :class="[
              'h-5 w-5',
              $route.path === item.href ? 'text-blue-600' : 'text-gray-400'
            ]"
          />
          <span class="text-xs font-medium">{{ item.name }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Notifications Modal -->
    <MobileNotificationsModal
      v-if="showNotifications"
      @close="showNotifications = false"
    />

    <!-- Profile Modal -->
    <MobileProfileModal
      v-if="showProfile"
      @close="showProfile = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Bars3Icon,
  BellIcon,
  XMarkIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  ChartBarIcon,
  ClockIcon,
  PlusIcon,
  CogIcon,
  HomeIcon,
  DocumentTextIcon,
  UsersIcon,
  Cog6ToothIcon
} from '@heroicons/vue/24/outline'
import MobileNotificationsModal from '../../components/mobile/MobileNotificationsModal.vue'
import MobileProfileModal from '../../components/mobile/MobileProfileModal.vue'

const router = useRouter()
const route = useRoute()

// Reactive data
const sidebarOpen = ref(false)
const showNotifications = ref(false)
const showProfile = ref(false)
const unreadNotifications = ref(3)

const user = reactive({
  name: 'Juan Pérez',
  email: 'juan@empresa.com',
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
})

const stats = reactive({
  conversations: 1247,
  users: 89,
  satisfaction: 94,
  responseTime: 2.3
})

const navigation = [
  { name: 'Dashboard', href: '/mobile', icon: HomeIcon },
  { name: 'Chatbots', href: '/mobile/chatbots', icon: ChatBubbleLeftRightIcon, badge: '3' },
  { name: 'Conversaciones', href: '/mobile/conversations', icon: DocumentTextIcon },
  { name: 'Analytics', href: '/mobile/analytics', icon: ChartBarIcon },
  { name: 'Usuarios', href: '/mobile/users', icon: UsersIcon },
  { name: 'Configuración', href: '/mobile/settings', icon: Cog6ToothIcon }
]

const bottomNavigation = [
  { name: 'Inicio', href: '/mobile', icon: HomeIcon },
  { name: 'Chats', href: '/mobile/conversations', icon: ChatBubbleLeftRightIcon },
  { name: 'Analytics', href: '/mobile/analytics', icon: ChartBarIcon },
  { name: 'Usuarios', href: '/mobile/users', icon: UsersIcon },
  { name: 'Más', href: '/mobile/settings', icon: CogIcon }
]

const recentActivity = reactive([
  {
    id: 1,
    type: 'conversation',
    icon: ChatBubbleLeftRightIcon,
    title: 'Nueva conversación iniciada',
    description: 'Usuario: maria@ejemplo.com',
    timestamp: new Date(Date.now() - 5 * 60 * 1000)
  },
  {
    id: 2,
    type: 'user',
    icon: UserGroupIcon,
    title: 'Nuevo usuario registrado',
    description: 'Carlos Rodríguez se unió al equipo',
    timestamp: new Date(Date.now() - 15 * 60 * 1000)
  },
  {
    id: 3,
    type: 'analytics',
    icon: ChartBarIcon,
    title: 'Reporte semanal generado',
    description: 'Analytics de la semana pasada',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
  }
])

// Computed
const currentPageTitle = computed(() => {
  const currentNav = navigation.find(item => item.href === route.path)
  return currentNav?.name || 'Dashboard'
})

// Methods
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const quickAction = (action) => {
  switch (action) {
    case 'new-chatbot':
      router.push('/mobile/chatbots/new')
      break
    case 'view-analytics':
      router.push('/mobile/analytics')
      break
    case 'manage-users':
      router.push('/mobile/users')
      break
    case 'settings':
      router.push('/mobile/settings')
      break
  }
}

const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  
  if (minutes < 60) {
    return `hace ${minutes} min`
  } else if (hours < 24) {
    return `hace ${hours} h`
  } else {
    return timestamp.toLocaleDateString()
  }
}

// Lifecycle
onMounted(() => {
  // Load mobile-specific data
  console.log('Mobile dashboard mounted')
})
</script>

<style scoped>
.mobile-dashboard {
  /* Mobile-specific styles */
  -webkit-overflow-scrolling: touch;
}

/* Hide scrollbar on mobile */
@media (max-width: 768px) {
  ::-webkit-scrollbar {
    display: none;
  }
}
</style>