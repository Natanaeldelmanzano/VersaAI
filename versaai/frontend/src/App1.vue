<template>
  <div id="app" class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header simple -->
    <header class="bg-white dark:bg-gray-800 shadow-sm p-4">
      <div class="flex justify-between items-center max-w-6xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          🚀 VersaAI
        </h1>
        <button 
          @click="toggleTheme" 
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {{ isDark ? '☀️' : '🌙' }}
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="max-w-6xl mx-auto p-4">
      <router-view v-if="hasRouter" />
      <div v-else class="text-center py-20">
        <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          ¡Hola! 👋
        </h2>
        <p class="text-gray-600 dark:text-gray-300 mb-8">
          VersaAI está funcionando correctamente
        </p>
        
        <!-- Información de debug -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow max-w-md mx-auto">
          <h3 class="font-semibold mb-4">🔧 Estado del Sistema</h3>
          <div class="space-y-2 text-sm text-left">
            <div>✅ Vue.js: Funcionando</div>
            <div>{{ hasRouter ? '✅' : '❌' }} Router: {{ hasRouter ? 'Configurado' : 'No encontrado' }}</div>
            <div>{{ hasPinia ? '✅' : '❌' }} Pinia: {{ hasPinia ? 'Configurado' : 'No encontrado' }}</div>
            <div>{{ hasToast ? '✅' : '❌' }} Toast: {{ hasToast ? 'Configurado' : 'No encontrado' }}</div>
            <div>🎨 Tema: {{ isDark ? 'Oscuro' : 'Claro' }}</div>
            <div>🌐 Entorno: {{ isDev ? 'Desarrollo' : 'Producción' }}</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// Estados reactivos
const isDark = ref(false)
const hasRouter = ref(false)
const hasPinia = ref(false)
const hasToast = ref(false)

// Computed
const isDev = computed(() => import.meta.env.DEV)

// Verificar dependencias
onMounted(() => {
  console.log('🚀 VersaAI iniciando...')
  
  // Verificar router
  try {
    const router = useRouter()
    hasRouter.value = !!router
    console.log('✅ Router disponible')
  } catch (e) {
    console.log('❌ Router no disponible:', e.message)
  }

  // Verificar Pinia
  try {
    const { createPinia } = require('pinia')
    hasPinia.value = true
    console.log('✅ Pinia disponible')
  } catch (e) {
    console.log('❌ Pinia no disponible')
  }

  // Verificar Toast
  try {
    const { useToast } = require('vue-toastification')
    hasToast.value = true
    console.log('✅ Toast disponible')
  } catch (e) {
    console.log('❌ Toast no disponible')
  }

  // Cargar tema guardado
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }

  console.log('✅ VersaAI iniciado correctamente')
})

// Funciones
const toggleTheme = () => {
  isDark.value = !isDark.value
  
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
  
  console.log('🎨 Tema cambiado a:', isDark.value ? 'oscuro' : 'claro')
}
</script>