<template>
  <div class="p-8">
    <h1 class="text-4xl font-bold text-blue-600 mb-4">✅ Test Básico Funcionando</h1>
    <p class="text-lg text-gray-700 mb-4">Si puedes ver esto, Vue.js está funcionando correctamente.</p>
    
    <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
      <strong>Estado:</strong> Frontend operativo
    </div>
    
    <div class="space-y-2">
      <p><strong>Ruta actual:</strong> {{ $route.path }}</p>
      <p><strong>Hora:</strong> {{ currentTime }}</p>
      <p><strong>Contador:</strong> {{ counter }}</p>
    </div>
    
    <button 
      @click="counter++" 
      class="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
    >
      Incrementar Contador
    </button>
    
    <div class="mt-6">
      <h2 class="text-xl font-semibold mb-2">Navegación de Prueba:</h2>
      <div class="space-x-2">
        <router-link to="/" class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded">Dashboard</router-link>
        <router-link to="/diagnostic" class="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1 rounded">Diagnóstico</router-link>
        <router-link to="/test-basic" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded">Test Básico</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const counter = ref(0)
const currentTime = ref('')

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString()
}

onMounted(() => {
  console.log('🧪 Test básico montado')
  updateTime()
  setInterval(updateTime, 1000)
})
</script>