<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <!-- 401 Illustration -->
        <div class="mx-auto h-32 w-32 text-red-600 mb-8">
          <svg viewBox="0 0 200 200" class="w-full h-full">
            <!-- Shield -->
            <path d="M100 20 L160 50 L160 120 Q160 160 100 180 Q40 160 40 120 L40 50 Z" fill="currentColor" opacity="0.1" />
            <path d="M100 30 L150 55 L150 115 Q150 150 100 170 Q50 150 50 115 L50 55 Z" fill="currentColor" opacity="0.2" />
            
            <!-- Lock -->
            <rect x="80" y="90" width="40" height="30" rx="3" fill="currentColor" opacity="0.6" />
            <rect x="85" y="95" width="30" height="20" rx="2" fill="white" />
            <path d="M90 90 L90 80 Q90 70 100 70 Q110 70 110 80 L110 90" stroke="currentColor" stroke-width="3" fill="none" opacity="0.6" />
            
            <!-- Keyhole -->
            <circle cx="100" cy="105" r="3" fill="currentColor" opacity="0.8" />
            <rect x="98" y="105" width="4" height="6" fill="currentColor" opacity="0.8" />
            
            <!-- X Mark -->
            <line x1="70" y1="60" x2="90" y2="80" stroke="currentColor" stroke-width="4" opacity="0.8" />
            <line x1="90" y1="60" x2="70" y2="80" stroke="currentColor" stroke-width="4" opacity="0.8" />
            
            <line x1="110" y1="60" x2="130" y2="80" stroke="currentColor" stroke-width="4" opacity="0.8" />
            <line x1="130" y1="60" x2="110" y2="80" stroke="currentColor" stroke-width="4" opacity="0.8" />
          </svg>
        </div>
        
        <!-- Error Message -->
        <h1 class="text-6xl font-bold text-gray-900 mb-4">401</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Acceso No Autorizado</h2>
        <p class="text-gray-600 mb-8 max-w-md mx-auto">
          No tienes permisos para acceder a esta página. 
          Por favor, inicia sesión con una cuenta que tenga los permisos necesarios.
        </p>
        
        <!-- Action Buttons -->
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <router-link
            to="/auth/login"
            class="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 inline-block text-center"
          >
            Iniciar Sesión
          </router-link>
          <button
            @click="goBack"
            class="w-full sm:w-auto bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
          >
            Volver Atrás
          </button>
        </div>
        
        <!-- Additional Info -->
        <div class="mt-12 pt-8 border-t border-gray-200">
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">
                  ¿Por qué veo este error?
                </h3>
                <div class="mt-2 text-sm text-yellow-700">
                  <ul class="list-disc list-inside space-y-1">
                    <li>Tu sesión puede haber expirado</li>
                    <li>No tienes el rol necesario para esta página</li>
                    <li>Tu cuenta puede estar desactivada</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <p class="text-sm text-gray-500 mb-4">¿Necesitas ayuda?</p>
          <div class="flex justify-center space-x-6 text-sm">
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Contactar Administrador
            </router-link>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Centro de Ayuda
            </router-link>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Solicitar Acceso
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>