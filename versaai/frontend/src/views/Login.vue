<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
    <div class="max-w-md w-full bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          🔐 Iniciar Sesión
        </h1>
        <p class="text-gray-600 dark:text-gray-300">
          Accede a tu cuenta VersaAI
        </p>
      </div>
      
      <div class="text-center">
        <p class="text-gray-500 dark:text-gray-400 mb-4">
          Vista de login - Próximamente
        </p>
        
        <button 
          @click="$router.push('/')"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
        >
          ← Volver al Inicio
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
console.log('✅ Vista Login cargada')
</script>