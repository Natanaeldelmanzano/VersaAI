<template>
  <div class="min-h-screen bg-green-100 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-green-800 mb-6">Página Simple - Sin Layout</h1>
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Estado del Sistema</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-green-50 p-4 rounded">
            <h3 class="font-semibold text-green-700">✅ Vue.js</h3>
            <p class="text-sm text-green-600">Framework funcionando</p>
          </div>
          <div class="bg-blue-50 p-4 rounded">
            <h3 class="font-semibold text-blue-700">✅ Vite</h3>
            <p class="text-sm text-blue-600">Build tool activo</p>
          </div>
          <div class="bg-purple-50 p-4 rounded">
            <h3 class="font-semibold text-purple-700">✅ Tailwind CSS</h3>
            <p class="text-sm text-purple-600">Estilos aplicados</p>
          </div>
          <div class="bg-yellow-50 p-4 rounded">
            <h3 class="font-semibold text-yellow-700">✅ Router</h3>
            <p class="text-sm text-yellow-600">Navegación activa</p>
          </div>
        </div>
        <div class="mt-6">
          <button 
            @click="showAlert" 
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-4"
          >
            Mostrar Alerta
          </button>
          <p class="mt-4 text-gray-600">Tiempo actual: {{ currentTime }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentTime = ref('')

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}

const showAlert = () => {
  alert('¡La aplicación está funcionando correctamente!')
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
})
</script>