<template>
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo y marca -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-3 group">
            <div class="text-2xl group-hover:scale-110 transition-transform duration-200">🤖</div>
            <div class="flex flex-col">
              <span class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                VersaAI
              </span>
              <span class="text-xs text-gray-500 -mt-1">AI Platform</span>
            </div>
          </router-link>
        </div>

        <!-- Navegación principal -->
        <div class="hidden md:flex items-center space-x-1">
          <router-link 
            v-for="item in navigationItems" 
            :key="item.name"
            :to="item.path" 
            class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            :class="{ 
              'text-blue-600 bg-blue-50 border border-blue-200': isActiveRoute(item.path),
              'hover:bg-gray-50': !isActiveRoute(item.path)
            }"
          >
            <span class="text-lg">{{ item.icon }}</span>
            <span>{{ item.name }}</span>
            <span v-if="item.badge" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
              {{ item.badge }}
            </span>
          </router-link>
        </div>

        <!-- Acciones del usuario -->
        <div class="flex items-center space-x-4">
          <!-- Notificaciones -->
          <button 
            @click="toggleNotifications"
            class="relative p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-full"
          >
            <span class="sr-only">Ver notificaciones</span>
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM10.5 3.75a6 6 0 0 1 6 6v2.25l2.25 2.25v.75H2.25v-.75L4.5 12V9.75a6 6 0 0 1 6-6z" />
            </svg>
            <span v-if="notificationCount > 0" class="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              {{ notificationCount > 9 ? '9+' : notificationCount }}
            </span>
          </button>

          <!-- Toggle tema -->
          <button 
            @click="toggleTheme"
            class="p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-full transition-colors"
          >
            <span class="sr-only">Cambiar tema</span>
            <svg v-if="!isDarkMode" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>

          <!-- Menú de usuario -->
          <div class="relative">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 p-1"
            >
              <div class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                <span class="text-white text-sm font-medium">{{ userInitials }}</span>
              </div>
              <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <!-- Dropdown del usuario -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="isUserMenuOpen" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                <div class="py-1">
                  <div class="px-4 py-2 text-sm text-gray-700 border-b border-gray-100">
                    <p class="font-medium">{{ userName }}</p>
                    <p class="text-gray-500">{{ userEmail }}</p>
                  </div>
                  <router-link to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors" @click="isUserMenuOpen = false">
                    👤 Mi Perfil
                  </router-link>
                  <router-link to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors" @click="isUserMenuOpen = false">
                    ⚙️ Configuración
                  </router-link>
                  <router-link to="/analytics" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors" @click="isUserMenuOpen = false">
                    📊 Analíticas
                  </router-link>
                  <div class="border-t border-gray-100">
                    <button 
                      @click="handleLogout"
                      class="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50 transition-colors"
                    >
                      🚪 Cerrar Sesión
                    </button>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Menú móvil -->
          <button 
            @click="toggleMobileMenu"
            class="md:hidden p-2 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-md"
          >
            <span class="sr-only">Abrir menú principal</span>
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Menú móvil -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="isMobileMenuOpen" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t border-gray-200">
          <router-link 
            v-for="item in navigationItems" 
            :key="item.name"
            :to="item.path" 
            @click="closeMobileMenu"
            class="flex items-center space-x-3 text-gray-700 hover:text-blue-600 hover:bg-gray-50 block px-3 py-2 rounded-md text-base font-medium transition-colors"
            :class="{ 'text-blue-600 bg-blue-50': isActiveRoute(item.path) }"
          >
            <span class="text-xl">{{ item.icon }}</span>
            <span>{{ item.name }}</span>
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const appStore = useAppStore()

// Estado local
const isUserMenuOpen = ref(false)
const isMobileMenuOpen = ref(false)
const notificationCount = ref(3)

// Datos del usuario (simulados)
const userName = ref('Usuario Demo')
const userEmail = ref('demo@versaai.com')

// Navegación
const navigationItems = ref([
  {
    name: 'Dashboard',
    path: '/',
    icon: '📊'
  },
  {
    name: 'Chat',
    path: '/chat',
    icon: '💬'
  },
  {
    name: 'Chatbots',
    path: '/chatbots',
    icon: '🤖'
  },
  {
    name: 'Analíticas',
    path: '/analytics',
    icon: '📈'
  },
  {
    name: 'Configuración',
    path: '/settings',
    icon: '⚙️'
  }
])

// Computed
const isDarkMode = computed(() => appStore.isDarkMode)

const userInitials = computed(() => {
  return userName.value
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

// Métodos
const isActiveRoute = (path) => {
  return route.path === path
}

const toggleTheme = () => {
  appStore.toggleTheme()
}

const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
  if (isUserMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  if (isMobileMenuOpen.value) {
    isUserMenuOpen.value = false
  }
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

const toggleNotifications = () => {
  console.log('🔔 Mostrar notificaciones')
  // Aquí iría la lógica para mostrar notificaciones
}

const handleLogout = () => {
  console.log('🚪 Cerrando sesión...')
  // Aquí iría la lógica de logout
  alert('Función de logout próximamente')
}

// Cerrar menús al hacer clic fuera
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    isUserMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>