<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
    <div class="text-center">
      <div class="text-9xl mb-4">🤖</div>
      <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
        404 - Página no encontrada
      </h1>
      <p class="text-gray-600 dark:text-gray-300 mb-8">
        La página que buscas no existe o ha sido movida.
      </p>
      
      <button 
        @click="$router.push('/')"
        class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
      >
        🏠 Volver al Inicio
      </button>
    </div>
  </div>
</template>

<script setup>
console.log('✅ Vista NotFound cargada')
</script>