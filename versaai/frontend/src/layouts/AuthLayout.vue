<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-32 w-80 h-80 bg-primary-100 rounded-full opacity-20 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-32 w-80 h-80 bg-secondary-100 rounded-full opacity-20 blur-3xl"></div>
    </div>

    <!-- Header -->
    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <router-link to="/" class="flex justify-center">
        <div class="flex items-center space-x-3">
          <div class="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-lg">
            <span class="text-white font-bold text-2xl">V</span>
          </div>
          <div>
            <h1 class="text-3xl font-bold text-gradient">VersaAI</h1>
            <p class="text-sm text-gray-600">Plataforma de Chatbots</p>
          </div>
        </div>
      </router-link>
      
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        {{ pageTitle }}
      </h2>
      <p v-if="pageDescription" class="mt-2 text-center text-sm text-gray-600">
        {{ pageDescription }}
      </p>
    </div>

    <!-- Main content -->
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <div class="bg-white py-8 px-4 shadow-xl sm:rounded-lg sm:px-10 border border-gray-200">
        <router-view />
      </div>
      
      <!-- Footer links -->
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">¿Necesitas ayuda?</span>
          </div>
        </div>

        <div class="mt-6 flex justify-center space-x-4 text-sm">
          <router-link
            to="/"
            class="text-primary-600 hover:text-primary-500 transition-colors duration-200"
          >
            Inicio
          </router-link>
          <span class="text-gray-300">|</span>
          <a
            href="mailto:support@versaai.com"
            class="text-primary-600 hover:text-primary-500 transition-colors duration-200"
          >
            Soporte
          </a>
          <span class="text-gray-300">|</span>
          <a
            href="/docs"
            class="text-primary-600 hover:text-primary-500 transition-colors duration-200"
          >
            Documentación
          </a>
        </div>
      </div>
    </div>

    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner h-8 w-8"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

// Computed
const isLoading = computed(() => authStore.isLoading)

const pageTitle = computed(() => {
  switch (route.name) {
    case 'Login':
      return 'Iniciar Sesión'
    case 'Register':
      return 'Crear Cuenta'
    case 'ForgotPassword':
      return 'Recuperar Contraseña'
    case 'ResetPassword':
      return 'Restablecer Contraseña'
    default:
      return 'Autenticación'
  }
})

const pageDescription = computed(() => {
  switch (route.name) {
    case 'Login':
      return 'Accede a tu cuenta para gestionar tus chatbots'
    case 'Register':
      return 'Crea tu cuenta y comienza a usar VersaAI'
    case 'ForgotPassword':
      return 'Te enviaremos un enlace para restablecer tu contraseña'
    case 'ResetPassword':
      return 'Ingresa tu nueva contraseña'
    default:
      return null
  }
})
</script>

<style scoped>
/* Additional auth-specific styles */
.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>