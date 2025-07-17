<template>
  <div class="min-h-screen bg-gray-50 relative">
    <!-- Mobile sidebar overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 z-40 lg:hidden">
      <div class="fixed inset-0 bg-gray-600 bg-opacity-75" @click="sidebarOpen = false"></div>
    </div>

    <!-- Mobile sidebar -->
    <div
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:hidden',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <router-link to="/dashboard" class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-lg">V</span>
          </div>
          <span class="text-xl font-bold text-gradient">VersaAI</span>
        </router-link>
        <button @click="sidebarOpen = false" class="text-gray-400 hover:text-gray-600">
          <XMarkIcon class="w-6 h-6" />
        </button>
      </div>
      <nav class="mt-5 px-2">
        <SidebarNavigation @navigate="sidebarOpen = false" />
      </nav>
    </div>

    <!-- Desktop sidebar -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
      <div class="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
        <div class="flex items-center flex-shrink-0 px-4">
          <router-link to="/dashboard" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">V</span>
            </div>
            <span class="text-xl font-bold text-gradient">VersaAI</span>
          </router-link>
        </div>
        <nav class="mt-5 flex-1 px-2 space-y-1">
          <SidebarNavigation />
        </nav>
      </div>
    </div>

    <!-- Main content -->
    <div class="lg:pl-64 flex flex-col min-h-screen">
      <!-- Top navigation -->
      <div class="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow border-b border-gray-200">
        <!-- Mobile menu button -->
        <button
          @click="sidebarOpen = true"
          class="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
        >
          <Bars3Icon class="h-6 w-6" />
        </button>

        <!-- Top navigation content -->
        <div class="flex-1 px-4 flex justify-between">
          <!-- Breadcrumbs -->
          <div class="flex-1 flex items-center">
            <Breadcrumbs />
          </div>

          <!-- Right side -->
          <div class="ml-4 flex items-center md:ml-6 space-x-4">
            <!-- Notifications -->
            <NotificationDropdown />
            
            <!-- User menu -->
            <UserDropdown />
          </div>
        </div>
      </div>

      <!-- Page content -->
      <main class="flex-1 bg-gray-50 relative z-0">
        <div class="content-wrapper">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8 py-6">
            <!-- Page header -->
            <div v-if="$route.meta.title" class="mb-6">
              <h1 class="text-2xl font-semibold text-gray-900">{{ pageTitle }}</h1>
              <p v-if="pageDescription" class="mt-1 text-sm text-gray-600">{{ pageDescription }}</p>
            </div>
            
            <!-- Router view -->
            <div class="relative z-1">
              <router-view />
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner h-8 w-8"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

// Components
import SidebarNavigation from '@/components/layout/SidebarNavigation.vue'
import Breadcrumbs from '@/components/layout/Breadcrumbs.vue'
import NotificationDropdown from '@/components/layout/NotificationDropdown.vue'
import UserDropdown from '@/components/layout/UserDropdown.vue'

const route = useRoute()
const authStore = useAuthStore()

// State
const sidebarOpen = ref(false)

// Computed
const isLoading = computed(() => authStore.isLoading)
const pageTitle = computed(() => {
  const title = route.meta.title || route.name
  return title?.replace(' - VersaAI', '') || 'Dashboard'
})
const pageDescription = computed(() => route.meta.description || null)

// Handle window resize
const handleResize = () => {
  if (window.innerWidth >= 1024) {
    sidebarOpen.value = false
  }
}

// Lifecycle
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>