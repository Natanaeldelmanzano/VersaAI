import { createApp } from 'vue'
import './style.css'

// Crear una aplicación Vue muy simple para pruebas
const app = createApp({
  template: `
    <div class="min-h-screen bg-gray-100 flex items-center justify-center">
      <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 class="text-3xl font-bold text-green-600 mb-4">✅ VersaAI Funcionando</h1>
        <p class="text-gray-700 mb-4">Esta es una prueba simple de Vue.js</p>
        <p class="text-sm text-gray-500">Hora: {{ currentTime }}</p>
        <button 
          @click="updateTime" 
          class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Actualizar Hora
        </button>
        <div class="mt-4 p-4 bg-yellow-100 border border-yellow-400 rounded">
          <p class="text-yellow-800 text-sm">
            <strong>Diagnóstico:</strong> Si puedes ver esto, Vue.js está funcionando correctamente.
            El problema está en la configuración de la aplicación principal.
          </p>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      currentTime: new Date().toLocaleString()
    }
  },
  methods: {
    updateTime() {
      this.currentTime = new Date().toLocaleString()
    }
  },
  mounted() {
    console.log('✅ Aplicación simple montada correctamente')
    console.log('🔍 Diagnóstico: Vue.js está funcionando')
  }
})

app.mount('#app')

console.log('🚀 main-simple.js ejecutado')
console.log('📍 Si ves este mensaje, el JavaScript se está ejecutando')