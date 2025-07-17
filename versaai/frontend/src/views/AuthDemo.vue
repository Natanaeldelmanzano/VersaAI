<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Nuevas Páginas de Autenticación VersaAI
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Diseños modernos con glassmorphism y gradientes
        </p>
      </div>

      <!-- Navigation Cards -->
      <div class="grid md:grid-cols-2 gap-8 mb-12">
        <!-- Login Card -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <div class="text-center mb-6">
            <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg mb-4">
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Nueva Página de Login
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Diseño moderno con efectos glassmorphism, gradientes azul-púrpura y mejor UX
            </p>
          </div>
          
          <div class="space-y-4">
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Mostrar/ocultar contraseña
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Efectos de hover y animaciones
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Fondo con patrones y blur
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Soporte para modo oscuro
            </div>
          </div>
          
          <div class="mt-8">
            <router-link
              to="/auth/new-login"
              class="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
            >
              Ver Nueva Página de Login
            </router-link>
          </div>
        </div>

        <!-- Register Card -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <div class="text-center mb-6">
            <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-lg mb-4">
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Nueva Página de Registro
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Formulario completo con validaciones en tiempo real y indicadores visuales
            </p>
          </div>
          
          <div class="space-y-4">
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Indicador de fuerza de contraseña
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Validación de coincidencia de contraseñas
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Gradientes emerald-teal
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-400">
              <svg class="h-4 w-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Iconos para cada campo
            </div>
          </div>
          
          <div class="mt-8">
            <router-link
              to="/auth/new-register"
              class="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98]"
            >
              Ver Nueva Página de Registro
            </router-link>
          </div>
        </div>
      </div>

      <!-- Comparison Section -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
          Comparación: Páginas Originales vs Nuevas
        </h3>
        
        <div class="grid md:grid-cols-2 gap-8">
          <!-- Original Pages -->
          <div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Páginas Originales
            </h4>
            <div class="space-y-3">
              <router-link
                to="/auth/login"
                class="block w-full py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                Login Original
              </router-link>
              <router-link
                to="/auth/register"
                class="block w-full py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
              >
                Registro Original
              </router-link>
            </div>
          </div>
          
          <!-- New Pages -->
          <div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Páginas Nuevas
            </h4>
            <div class="space-y-3">
              <router-link
                to="/auth/new-login"
                class="block w-full py-2 px-4 border border-transparent rounded-lg text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-[1.02]"
              >
                Nuevo Login
              </router-link>
              <router-link
                to="/auth/new-register"
                class="block w-full py-2 px-4 border border-transparent rounded-lg text-sm font-medium text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 transition-all transform hover:scale-[1.02]"
              >
                Nuevo Registro
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div class="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
          Características de las Nuevas Páginas
        </h3>
        
        <div class="grid md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900 mb-4">
              <svg class="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Diseño Moderno
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Glassmorphism, gradientes y efectos visuales avanzados
            </p>
          </div>
          
          <div class="text-center">
            <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900 mb-4">
              <svg class="h-6 w-6 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              UX Mejorada
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Validaciones en tiempo real y feedback visual inmediato
            </p>
          </div>
          
          <div class="text-center">
            <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900 mb-4">
              <svg class="h-6 w-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Rendimiento
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Optimizado para carga rápida y animaciones fluidas
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No necesitamos lógica adicional para esta página de demostración
</script>

<style scoped>
/* Transiciones suaves */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>