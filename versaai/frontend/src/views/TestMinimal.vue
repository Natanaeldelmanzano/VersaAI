<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">✅ Test Minimal</h1>
      <p class="text-gray-600 mb-4">Si puedes ver esto, Vue.js está funcionando correctamente.</p>
      
      <div class="space-y-2">
        <p><strong>Hora actual:</strong> {{ currentTime }}</p>
        <p><strong>Contador:</strong> {{ counter }}</p>
        <p><strong>Ruta actual:</strong> {{ $route.path }}</p>
      </div>
      
      <div class="mt-6 space-y-2">
        <button 
          @click="counter++" 
          class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
        >
          Incrementar Contador
        </button>
        
        <router-link 
          to="/dashboard-simple" 
          class="block w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded text-center"
        >
          Ir a Dashboard Simple
        </router-link>
        
        <router-link 
          to="/test-basic" 
          class="block w-full bg-purple-500 hover:bg-purple-600 text-white py-2 px-4 rounded text-center"
        >
          Ir a Test Básico
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const counter = ref(0)
const currentTime = ref('')

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString('es-ES')
}

let timeInterval

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  console.log('✅ TestMinimal montado correctamente')
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>