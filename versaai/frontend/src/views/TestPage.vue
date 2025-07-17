<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-6">🎉 ¡VersaAI Funciona!</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-green-50 border border-green-200 rounded-lg p-6">
            <h2 class="text-2xl font-semibold text-green-800 mb-4">✅ Estado del Sistema</h2>
            <ul class="space-y-2 text-green-700">
              <li>• Vue.js 3 - Funcionando</li>
              <li>• Vite - Funcionando</li>
              <li>• Tailwind CSS - Funcionando</li>
              <li>• Vue Router - Funcionando</li>
              <li>• Pinia Store - Funcionando</li>
            </ul>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 class="text-2xl font-semibold text-blue-800 mb-4">📊 Información</h2>
            <div class="space-y-2 text-blue-700">
              <p><strong>Proyecto:</strong> VersaAI</p>
              <p><strong>Versión:</strong> 1.0.0</p>
              <p><strong>Entorno:</strong> Desarrollo</p>
              <p><strong>Puerto:</strong> 3000</p>
              <p><strong>Hora:</strong> {{ currentTime }}</p>
            </div>
          </div>
        </div>
        
        <div class="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 class="text-2xl font-semibold text-yellow-800 mb-4">🚀 Próximos Pasos</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-yellow-700">
            <div>
              <h3 class="font-semibold mb-2">Backend:</h3>
              <ul class="space-y-1 text-sm">
                <li>• Configurar base de datos</li>
                <li>• Implementar autenticación</li>
                <li>• Crear endpoints de API</li>
                <li>• Integrar servicios de IA</li>
              </ul>
            </div>
            <div>
              <h3 class="font-semibold mb-2">Frontend:</h3>
              <ul class="space-y-1 text-sm">
                <li>• Crear componentes de UI</li>
                <li>• Implementar dashboard</li>
                <li>• Configurar formularios</li>
                <li>• Añadir funcionalidades</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="mt-8 flex flex-wrap gap-4">
          <button 
            @click="updateTime" 
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            🔄 Actualizar Hora
          </button>
          
          <button 
            @click="showAlert" 
            class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            ✨ Probar Interactividad
          </button>
          
          <button 
            @click="toggleTheme" 
            class="bg-purple-500 hover:bg-purple-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            🌙 Cambiar Tema
          </button>
        </div>
        
        <div class="mt-8 text-center text-gray-600">
          <p class="text-lg">🎯 <strong>VersaAI</strong> - Plataforma de Chatbots con IA</p>
          <p class="text-sm mt-2">Desarrollado con Vue.js 3, FastAPI y mucho ❤️</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const currentTime = ref(new Date().toLocaleString())

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}

const showAlert = () => {
  alert('🎉 ¡La interactividad funciona perfectamente!')
}

const toggleTheme = () => {
  appStore.toggleTheme()
}

onMounted(() => {
  console.log('🎯 TestPage mounted successfully!')
  
  // Update time every second
  setInterval(() => {
    updateTime()
  }, 1000)
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>