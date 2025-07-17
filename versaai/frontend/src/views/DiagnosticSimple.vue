<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Diagnostico Simple</h1>
      
      <div class="bg-white p-6 rounded-lg shadow mb-6">
        <h2 class="text-xl font-semibold mb-4">Test Basico de Vue</h2>
        <p class="mb-2">Contador: <span class="font-bold text-blue-600">{{ counter }}</span></p>
        <button 
          @click="counter++" 
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
        >
          Incrementar
        </button>
        <button 
          @click="counter = 0" 
          class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
        >
          Reset
        </button>
      </div>

      <div class="bg-white p-6 rounded-lg shadow mb-6">
        <h2 class="text-xl font-semibold mb-4">Test de Reactividad</h2>
        <p class="mb-2">Hora actual: <span class="font-mono text-green-600">{{ currentTime }}</span></p>
        <p class="mb-2">Mensaje: <span class="text-purple-600">{{ message }}</span></p>
        <input 
          v-model="message" 
          class="border border-gray-300 rounded px-3 py-2 w-full"
          placeholder="Escribe algo..."
        >
      </div>

      <div class="bg-white p-6 rounded-lg shadow mb-6">
        <h2 class="text-xl font-semibold mb-4">Test de Navegacion</h2>
        <p class="mb-4">Ruta actual: <span class="font-mono text-indigo-600">{{ $route.path }}</span></p>
        <div class="space-x-2">
          <router-link 
            to="/dashboard" 
            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded inline-block"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/test-minimal" 
            class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded inline-block"
          >
            Test Minimal
          </router-link>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">Informacion del Entorno</h2>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <strong>Modo:</strong> {{ isDev ? 'Desarrollo' : 'Produccion' }}
          </div>
          <div>
            <strong>Vue Version:</strong> {{ vueVersion }}
          </div>
          <div>
            <strong>Navegador:</strong> {{ userAgent }}
          </div>
          <div>
            <strong>Timestamp:</strong> {{ timestamp }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { version } from 'vue'

const counter = ref(0)
const message = ref('Vue.js esta funcionando!')
const currentTime = ref('')
const timestamp = ref(Date.now())

const isDev = computed(() => import.meta.env.DEV)
const vueVersion = version
const userAgent = navigator.userAgent.split(' ')[0]

const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString('es-ES')
}

let timeInterval

onMounted(() => {
  console.log('DiagnosticSimple montado')
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  console.log('DiagnosticSimple desmontado')
})
</script>