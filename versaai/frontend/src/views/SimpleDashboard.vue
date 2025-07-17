<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header Simple -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">🚀 Dashboard VersaAI</h1>
        <p class="text-gray-600">Bienvenido a la plataforma de chatbots con IA</p>
      </div>

      <!-- Stats Cards Simples -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <!-- Card 1 -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="text-3xl mr-4">💬</div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Conversaciones</h3>
              <p class="text-2xl font-bold text-blue-600">1,234</p>
            </div>
          </div>
        </div>

        <!-- Card 2 -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="text-3xl mr-4">🤖</div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Chatbots</h3>
              <p class="text-2xl font-bold text-green-600">12</p>
            </div>
          </div>
        </div>

        <!-- Card 3 -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="text-3xl mr-4">👥</div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Usuarios</h3>
              <p class="text-2xl font-bold text-purple-600">567</p>
            </div>
          </div>
        </div>

        <!-- Card 4 -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="text-3xl mr-4">📊</div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">Satisfacción</h3>
              <p class="text-2xl font-bold text-orange-600">98%</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones Rápidas -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">🚀 Acciones Rápidas</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <router-link 
            to="/chatbots" 
            class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg text-center transition-colors duration-200"
          >
            <div class="text-2xl mb-2">🤖</div>
            <div class="font-medium">Crear Chatbot</div>
          </router-link>
          
          <router-link 
            to="/chat" 
            class="bg-green-500 hover:bg-green-600 text-white p-4 rounded-lg text-center transition-colors duration-200"
          >
            <div class="text-2xl mb-2">💬</div>
            <div class="font-medium">Nuevo Chat</div>
          </router-link>
          
          <router-link 
            to="/analytics" 
            class="bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-lg text-center transition-colors duration-200"
          >
            <div class="text-2xl mb-2">📈</div>
            <div class="font-medium">Ver Analíticas</div>
          </router-link>
        </div>
      </div>

      <!-- Actividad Reciente -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">📋 Actividad Reciente</h2>
        <div class="space-y-4">
          <div class="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl">💬</div>
            <div class="flex-1">
              <p class="font-medium text-gray-900">Nueva conversación iniciada</p>
              <p class="text-sm text-gray-500">Hace 5 minutos</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl">🤖</div>
            <div class="flex-1">
              <p class="font-medium text-gray-900">Chatbot "Soporte" actualizado</p>
              <p class="text-sm text-gray-500">Hace 1 hora</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl">👤</div>
            <div class="flex-1">
              <p class="font-medium text-gray-900">Nuevo usuario registrado</p>
              <p class="text-sm text-gray-500">Hace 2 horas</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado del Sistema -->
      <div class="mt-6 bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">🔧 Estado del Sistema</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-gray-700">API Backend: Operativo</span>
          </div>
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-gray-700">Base de Datos: Conectada</span>
          </div>
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-gray-700">IA Service: Activo</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

onMounted(() => {
  console.log('📊 Dashboard Simple cargado')
  appStore.setPageInfo('Dashboard', 'Panel de control principal')
})
</script>

<style scoped>
/* Estilos específicos del componente */
</style>