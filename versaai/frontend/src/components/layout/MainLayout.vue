<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation Bar -->
    <nav class="bg-white border-b border-gray-200 fixed w-full z-30 top-0">
      <div class="px-3 py-3 lg:px-5 lg:pl-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center justify-start">
            <!-- Sidebar Toggle -->
            <button
              @click="toggleSidebar"
              class="p-2 text-gray-600 rounded cursor-pointer lg:hidden hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 focus:ring-2 focus:ring-gray-100"
            >
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
              </svg>
            </button>
            
            <!-- Logo -->
            <router-link to="/" class="flex ml-2 md:mr-24">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap text-gray-900">VersaAI</span>
              </div>
            </router-link>
          </div>
          
          <!-- Right side items -->
          <div class="flex items-center">
            <!-- Search -->
            <div class="hidden lg:block lg:pl-2">
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Buscar..."
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"
                >
              </div>
            </div>
            
            <!-- Notifications -->
            <button class="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100 ml-3">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
              </svg>
              <span class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            
            <!-- User Menu -->
            <div class="relative ml-3">
              <button
                @click="toggleUserMenu"
                class="flex items-center text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300"
              >
                <img class="w-8 h-8 rounded-full" src="https://ui-avatars.com/api/?name=Admin&background=3b82f6&color=fff" alt="user photo">
              </button>
              
              <!-- User Dropdown -->
              <div v-show="showUserMenu" class="absolute right-0 z-50 my-4 text-base list-none bg-white divide-y divide-gray-100 rounded shadow">
                <div class="px-4 py-3">
                  <p class="text-sm text-gray-900">Administrador</p>
                  <p class="text-sm font-medium text-gray-900 truncate">admin@versaai.com</p>
                </div>
                <ul class="py-1">
                  <li>
                    <router-link to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Configuración</router-link>
                  </li>
                  <li>
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Cerrar sesión</a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform bg-white border-r border-gray-200',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <div class="h-full px-3 pb-4 overflow-y-auto bg-white">
        <ul class="space-y-2 font-medium">
          <!-- Dashboard -->
          <li>
            <router-link
              to="/"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/>
                <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/>
              </svg>
              <span class="ml-3">Dashboard</span>
            </router-link>
          </li>
          
          <!-- Chat -->
          <li>
            <router-link
              to="/chat"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/chat' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
              </svg>
              <span class="ml-3">Chat IA</span>
            </router-link>
          </li>
          
          <!-- Analytics -->
          <li>
            <router-link
              to="/analytics"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/analytics' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
              </svg>
              <span class="ml-3">Analíticas</span>
            </router-link>
          </li>
          
          <!-- Chatbots -->
          <li>
            <router-link
              to="/chatbots"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/chatbots' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm12 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>
                <path d="M11 14H9v4h2v-4z"/>
                <path d="M8 14H6a1 1 0 00-1 1v3h4v-4z"/>
              </svg>
              <span class="ml-3">Chatbots</span>
            </router-link>
          </li>
          
          <!-- Configuration -->
          <li>
            <router-link
              to="/configuracion"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/configuracion' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
              </svg>
              <span class="ml-3">Configuración</span>
            </router-link>
          </li>
          
          <!-- Divider -->
          <li class="pt-4 mt-4 space-y-2 border-t border-gray-200">
            <p class="text-xs font-medium text-gray-500 uppercase">Herramientas</p>
          </li>
          
          <!-- Test -->
          <li>
            <router-link
              to="/test"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/test' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <span class="ml-3">Pruebas</span>
            </router-link>
          </li>
          
          <!-- Diagnostic -->
          <li>
            <router-link
              to="/diagnostic"
              class="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 group"
              :class="{ 'bg-blue-50 text-blue-700': $route.path === '/diagnostic' }"
            >
              <svg class="w-5 h-5 text-gray-500 transition duration-75 group-hover:text-gray-900" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 3a1 1 0 00-1.447-.894L8.763 6H5a3 3 0 000 6h.28l1.771 5.316A1 1 0 008 18h1a1 1 0 001-1v-4.382l6.553 3.894A1 1 0 0018 16V3z" clip-rule="evenodd"/>
              </svg>
              <span class="ml-3">Diagnóstico</span>
            </router-link>
          </li>
        </ul>
        
        <!-- Footer -->
        <div class="absolute bottom-0 left-0 justify-center p-4 space-x-4 w-full bg-white border-r border-gray-200">
          <div class="text-center">
            <p class="text-xs text-gray-500">VersaAI v1.0</p>
            <p class="text-xs text-gray-400">© 2024</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="p-4 lg:ml-64">
      <div class="p-4 mt-14">
        <slot />
      </div>
    </div>
    
    <!-- Sidebar Overlay for mobile -->
    <div
      v-show="sidebarOpen"
      @click="closeSidebar"
      class="fixed inset-0 z-30 bg-gray-900 opacity-50 lg:hidden"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const sidebarOpen = ref(false)
const showUserMenu = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// Close user menu when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>