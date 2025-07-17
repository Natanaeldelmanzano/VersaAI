<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">🤖 VersaAI Test</h1>
        <div class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Contador Simple</h2>
          <div class="text-4xl font-bold text-blue-600 mb-4">{{ count }}</div>
          <div class="space-y-3">
            <button 
              @click="increment" 
              class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition-colors"
            >
              Incrementar
            </button>
            <button 
              @click="decrement" 
              class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition-colors"
            >
              Decrementar
            </button>
            <button 
              @click="reset" 
              class="w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
            >
              Resetear
            </button>
          </div>
        </div>
        
        <div class="mt-8 bg-white shadow rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Estado de la Aplicación</h3>
          <div class="text-sm text-gray-600 space-y-2">
            <p>✅ Vue.js 3 funcionando</p>
            <p>✅ Tailwind CSS cargado</p>
            <p>✅ Componente reactivo</p>
            <p>✅ Router funcionando</p>
          </div>
        </div>
        
        <div class="mt-6">
          <router-link 
            to="/dashboard" 
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition-colors"
          >
            Ir al Dashboard
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Estado reactivo
const count = ref(0)

// Métodos
const increment = () => {
  count.value++
}

const decrement = () => {
  count.value--
}

const reset = () => {
  count.value = 0
}

// Log para debugging
console.log('✅ SimpleTest component loaded successfully!')
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>