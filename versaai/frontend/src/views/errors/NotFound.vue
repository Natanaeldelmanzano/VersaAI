<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <!-- 404 Illustration -->
        <div class="mx-auto h-32 w-32 text-primary-600 mb-8">
          <svg viewBox="0 0 200 200" class="w-full h-full">
            <!-- Robot Head -->
            <rect x="60" y="40" width="80" height="60" rx="10" fill="currentColor" opacity="0.1" />
            <rect x="65" y="45" width="70" height="50" rx="5" fill="currentColor" opacity="0.2" />
            
            <!-- Eyes -->
            <circle cx="80" cy="65" r="8" fill="currentColor" opacity="0.6" />
            <circle cx="120" cy="65" r="8" fill="currentColor" opacity="0.6" />
            <circle cx="80" cy="65" r="3" fill="white" />
            <circle cx="120" cy="65" r="3" fill="white" />
            
            <!-- Mouth (sad) -->
            <path d="M 85 85 Q 100 75 115 85" stroke="currentColor" stroke-width="3" fill="none" opacity="0.6" />
            
            <!-- Antennas -->
            <line x1="85" y1="40" x2="85" y2="25" stroke="currentColor" stroke-width="2" opacity="0.4" />
            <line x1="115" y1="40" x2="115" y2="25" stroke="currentColor" stroke-width="2" opacity="0.4" />
            <circle cx="85" cy="25" r="3" fill="currentColor" opacity="0.4" />
            <circle cx="115" cy="25" r="3" fill="currentColor" opacity="0.4" />
            
            <!-- Body -->
            <rect x="70" y="100" width="60" height="80" rx="8" fill="currentColor" opacity="0.1" />
            
            <!-- Arms -->
            <rect x="40" y="110" width="30" height="15" rx="7" fill="currentColor" opacity="0.2" />
            <rect x="130" y="110" width="30" height="15" rx="7" fill="currentColor" opacity="0.2" />
            
            <!-- Legs -->
            <rect x="80" y="180" width="15" height="20" rx="7" fill="currentColor" opacity="0.2" />
            <rect x="105" y="180" width="15" height="20" rx="7" fill="currentColor" opacity="0.2" />
          </svg>
        </div>
        
        <!-- Error Message -->
        <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Página No Encontrada</h2>
        <p class="text-gray-600 mb-8 max-w-md mx-auto">
          Lo sentimos, la página que estás buscando no existe o ha sido movida. 
          Nuestro robot está tan confundido como tú.
        </p>
        
        <!-- Action Buttons -->
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <button
            @click="goBack"
            class="w-full sm:w-auto bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
          >
            Volver Atrás
          </button>
          <router-link
            to="/"
            class="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 inline-block text-center"
          >
            Ir al Inicio
          </router-link>
        </div>
        
        <!-- Help Links -->
        <div class="mt-12 pt-8 border-t border-gray-200">
          <p class="text-sm text-gray-500 mb-4">¿Necesitas ayuda?</p>
          <div class="flex justify-center space-x-6 text-sm">
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Centro de Ayuda
            </router-link>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Contactar Soporte
            </router-link>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Estado del Sistema
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>