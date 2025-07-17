<template>
  <div class="mobile-layout min-h-screen bg-gray-50">
    <!-- Mobile Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="px-4 py-3">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">V</span>
            </div>
            <span class="font-semibold text-gray-900">VersaAI</span>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            @click="toggleMobileMenu"
            class="p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <Bars3Icon v-if="!showMobileMenu" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Sidebar Overlay -->
    <div 
      v-if="showMobileMenu"
      class="fixed inset-0 z-40 bg-black bg-opacity-50"
      @click="closeMobileMenu"
    ></div>

    <!-- Mobile Sidebar -->
    <div 
      :class="[
        'fixed top-0 right-0 h-full w-80 bg-white shadow-xl transform transition-transform duration-300 z-50',
        showMobileMenu ? 'translate-x-0' : 'translate-x-full'
      ]"
    >
      <div class="p-4">
        <!-- Close Button -->
        <div class="flex justify-end mb-4">
          <button 
            @click="closeMobileMenu"
            class="p-2 rounded-lg text-gray-600 hover:bg-gray-100"
          >
            <XMarkIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Navigation Menu -->
        <nav class="space-y-2">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.to"
            @click="closeMobileMenu"
            class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
            :class="{ 'bg-blue-50 text-blue-700': $route.name === item.name }"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span>{{ item.label }}</span>
          </router-link>
        </nav>

        <!-- User Section -->
        <div class="mt-8 pt-4 border-t border-gray-200">
          <div class="flex items-center space-x-3 px-3 py-2">
            <div class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
              <UserIcon class="w-5 h-5 text-gray-600" />
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">{{ user?.name || 'Usuario' }}</p>
              <p class="text-xs text-gray-500">{{ user?.email || 'usuario@ejemplo.com' }}</p>
            </div>
          </div>
          
          <div class="mt-4 space-y-1">
            <router-link
              to="/dashboard/profile"
              @click="closeMobileMenu"
              class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <UserCircleIcon class="w-5 h-5" />
              <span>Perfil</span>
            </router-link>
            
            <router-link
              to="/dashboard/settings"
              @click="closeMobileMenu"
              class="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <CogIcon class="w-5 h-5" />
              <span>Configuración</span>
            </router-link>
            
            <button
              @click="logout"
              class="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-red-700 hover:bg-red-50 transition-colors"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />
              <span>Cerrar Sesión</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="pb-16">
      <router-view />
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
      <div class="flex justify-around">
        <router-link
          v-for="item in bottomNavItems"
          :key="item.name"
          :to="item.to"
          class="flex flex-col items-center space-y-1 py-2 px-3 rounded-lg transition-colors"
          :class="{
            'text-blue-600': $route.name === item.name,
            'text-gray-600': $route.name !== item.name
          }"
        >
          <component :is="item.icon" class="w-5 h-5" />
          <span class="text-xs font-medium">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  Bars3Icon,
  XMarkIcon,
  HomeIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  UserIcon,
  UserCircleIcon,
  CogIcon,
  ArrowRightOnRectangleIcon,
  DocumentTextIcon,
  UsersIcon,
  CubeIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const showMobileMenu = ref(false)

const user = computed(() => authStore.user)

const navigationItems = [
  {
    name: 'MobileDashboard',
    to: '/mobile',
    label: 'Dashboard',
    icon: HomeIcon
  },
  {
    name: 'Chatbots',
    to: '/dashboard/chatbots',
    label: 'Chatbots',
    icon: CubeIcon
  },
  {
    name: 'Conversations',
    to: '/dashboard/conversations',
    label: 'Conversaciones',
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: 'Analytics',
    to: '/dashboard/analytics',
    label: 'Analíticas',
    icon: ChartBarIcon
  },
  {
    name: 'KnowledgeBases',
    to: '/dashboard/knowledge-bases',
    label: 'Bases de Conocimiento',
    icon: DocumentTextIcon
  },
  {
    name: 'Users',
    to: '/dashboard/users',
    label: 'Usuarios',
    icon: UsersIcon
  }
]

const bottomNavItems = [
  {
    name: 'MobileDashboard',
    to: '/mobile',
    label: 'Inicio',
    icon: HomeIcon
  },
  {
    name: 'Chatbots',
    to: '/dashboard/chatbots',
    label: 'Bots',
    icon: CubeIcon
  },
  {
    name: 'Conversations',
    to: '/dashboard/conversations',
    label: 'Chat',
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: 'Analytics',
    to: '/dashboard/analytics',
    label: 'Stats',
    icon: ChartBarIcon
  }
]

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const logout = async () => {
  try {
    await authStore.logout()
    router.push('/auth/login')
  } catch (error) {
    console.error('Error al cerrar sesión:', error)
  }
}
</script>

<style scoped>
.mobile-layout {
  /* Ensure proper mobile viewport */
  min-height: 100vh;
  min-height: -webkit-fill-available;
}

/* Smooth transitions for mobile menu */
.transform {
  transition: transform 0.3s ease-in-out;
}

/* Bottom navigation safe area */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  nav {
    padding-bottom: calc(0.5rem + env(safe-area-inset-bottom));
  }
}
</style>