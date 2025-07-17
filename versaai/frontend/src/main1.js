import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

console.log('🚀 Iniciando VersaAI...')

const app = createApp(App)

// Intentar cargar dependencias opcionales
try {
  const { createPinia } = await import('pinia')
  app.use(createPinia())
  console.log('✅ Pinia cargado')
} catch (e) {
  console.log('⚠️ Pinia no disponible, continuando sin él')
}

try {
  const { createRouter, createWebHistory } = await import('vue-router')
  
  const routes = [
    {
      path: '/',
      name: 'Home',
      component: { 
        template: `
          <div class="text-center py-20">
            <h1 class="text-4xl font-bold mb-4">🏠 Inicio</h1>
            <p class="text-gray-600 dark:text-gray-300">Página principal de VersaAI</p>
          </div>
        `
      }
    },
    {
      path: '/test',
      name: 'Test',
      component: { 
        template: `
          <div class="text-center py-20">
            <h1 class="text-4xl font-bold mb-4">🧪 Prueba</h1>
            <p class="text-gray-600 dark:text-gray-300">Página de prueba</p>
            <button @click="$router.push('/')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
              ← Volver
            </button>
          </div>
        `
      }
    }
  ]

  const router = createRouter({
    history: createWebHistory(),
    routes
  })

  app.use(router)
  console.log('✅ Router cargado')
} catch (e) {
  console.log('⚠️ Router no disponible, continuando sin él')
}

try {
  const Toast = await import('vue-toastification')
  app.use(Toast.default)
  console.log('✅ Toast cargado')
} catch (e) {
  console.log('⚠️ Toast no disponible, continuando sin él')
}

app.mount('#app')
console.log('✅ VersaAI montado correctamente')