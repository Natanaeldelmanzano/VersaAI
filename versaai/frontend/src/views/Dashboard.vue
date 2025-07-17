<template>
  <div class="dashboard-content scroll-smooth">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 sticky top-0 z-10">
      <div class="px-6 py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-2xl font-semibold text-gray-900">Panel de Control</h1>
            <p class="mt-1 text-sm text-gray-500">Bienvenido al centro de administración de VersaAI</p>
          </div>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-500 rounded-full"></div>
              <span class="text-sm text-gray-600">Sistema operativo</span>
            </div>
            <div class="text-sm text-gray-500">{{ currentTime }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0 space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Conversaciones</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.conversations }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-50 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                </svg>
              </div>
            </div>
            <div class="mt-4 flex items-center">
              <span class="text-sm text-green-600 font-medium">+12%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Tokens Procesados</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.tokensUsed.toLocaleString() }}</p>
              </div>
              <div class="w-12 h-12 bg-green-50 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
            </div>
            <div class="mt-4 flex items-center">
              <span class="text-sm text-green-600 font-medium">+8%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Disponibilidad</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.uptime }}</p>
              </div>
              <div class="w-12 h-12 bg-yellow-50 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
            </div>
            <div class="mt-4 flex items-center">
              <span class="text-sm text-green-600 font-medium">+0.1%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600">Usuarios Activos</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.users }}</p>
              </div>
              <div class="w-12 h-12 bg-purple-50 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"/>
                </svg>
              </div>
            </div>
            <div class="mt-4 flex items-center">
              <span class="text-sm text-green-600 font-medium">+15%</span>
              <span class="text-sm text-gray-500 ml-2">vs mes anterior</span>
            </div>
          </div>
        </div>

        <!-- Integrations Section -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-lg font-semibold text-gray-900">Integraciones Empresariales</h2>
                <p class="text-sm text-gray-500">Conecta VersaAI con tus herramientas favoritas</p>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-sm text-gray-600">{{ stats.integrations.active }}/{{ stats.integrations.total }} activas</span>
                <button
                  @click="router.push('/dashboard/integrations')"
                  class="text-sm text-blue-600 hover:text-blue-800 flex items-center space-x-1"
                >
                  <span>Ver todas</span>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <!-- Slack Integration -->
              <div class="integration-card bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-all duration-200 cursor-pointer" @click="openIntegration('slack')">
                <div class="flex items-center justify-between mb-3">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-purple-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52-2.523A2.528 2.528 0 0 1 5.042 10.12h2.52v2.522a2.528 2.528 0 0 1-2.52 2.523Zm0 0a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165v-6.734a2.528 2.528 0 0 1 2.522-2.523 2.528 2.528 0 0 1 2.52 2.523v6.734Z"/>
                      <path d="M8.83 15.165a2.528 2.528 0 0 1 2.523-2.523 2.528 2.528 0 0 1 2.52 2.523v2.522a2.528 2.528 0 0 1-2.52 2.523 2.528 2.528 0 0 1-2.523-2.523v-2.522Z"/>
                    </svg>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-xs text-green-600 font-medium">Conectado</span>
                  </div>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">Slack</h3>
                <p class="text-xs text-gray-500 mb-3">Notificaciones y chat</p>
                <button class="w-full bg-white border border-gray-200 text-gray-700 text-xs py-2 px-3 rounded-md hover:bg-gray-50 transition-colors">
                  Configurar
                </button>
              </div>

              <!-- Webhooks Integration -->
              <div class="integration-card bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-all duration-200 cursor-pointer" @click="openIntegration('webhooks')">
                <div class="flex items-center justify-between mb-3">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                    </svg>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-xs text-green-600 font-medium">{{ stats.integrations.webhooks }} activos</span>
                  </div>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">Webhooks</h3>
                <p class="text-xs text-gray-500 mb-3">Eventos en tiempo real</p>
                <button class="w-full bg-white border border-gray-200 text-gray-700 text-xs py-2 px-3 rounded-md hover:bg-gray-50 transition-colors">
                  Gestionar
                </button>
              </div>

              <!-- API Keys Integration -->
              <div class="integration-card bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition-all duration-200 cursor-pointer" @click="openIntegration('apikeys')">
                <div class="flex items-center justify-between mb-3">
                  <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                    </svg>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="text-xs text-green-600 font-medium">{{ stats.integrations.apiKeys }} claves</span>
                  </div>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">API Keys</h3>
                <p class="text-xs text-gray-500 mb-3">Autenticación segura</p>
                <button class="w-full bg-white border border-gray-200 text-gray-700 text-xs py-2 px-3 rounded-md hover:bg-gray-50 transition-colors">
                  Administrar
                </button>
              </div>

              <!-- Stripe Integration -->
              <div class="integration-card bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-orange-300 transition-all duration-200 cursor-pointer" @click="openIntegration('stripe')">
                <div class="flex items-center justify-between mb-3">
                  <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                    <svg class="w-6 h-6 text-indigo-600" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M13.976 9.15c-2.172-.806-3.356-1.426-3.356-2.409 0-.831.683-1.305 1.901-1.305 2.227 0 4.515.858 6.09 1.631l.89-5.494C18.252.975 15.697 0 12.165 0 9.667 0 7.589.654 6.104 1.872 4.56 3.147 3.757 4.992 3.757 7.218c0 4.039 2.467 5.76 6.476 7.219 2.585.92 3.445 1.574 3.445 2.583 0 .98-.84 1.545-2.354 1.545-1.875 0-4.965-.921-6.99-2.109l-.9 5.555C5.175 22.99 8.385 24 11.714 24c2.641 0 4.843-.624 6.328-1.813 1.664-1.305 2.525-3.236 2.525-5.732 0-4.128-2.524-5.851-6.591-7.305z"/>
                    </svg>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                    <span class="text-xs text-orange-600 font-medium">Pendiente</span>
                  </div>
                </div>
                <h3 class="text-sm font-semibold text-gray-900 mb-1">Stripe</h3>
                <p class="text-xs text-gray-500 mb-3">Pagos y facturación</p>
                <button class="w-full bg-white border border-gray-200 text-gray-700 text-xs py-2 px-3 rounded-md hover:bg-gray-50 transition-colors">
                  Conectar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Acciones Rápidas</h2>
            <p class="text-sm text-gray-500">Accede a las funciones principales del sistema</p>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <button
                @click="router.push('/chat')"
                class="flex flex-col items-center p-6 bg-gray-50 rounded-lg hover:bg-blue-50 hover:border-blue-200 border border-gray-200 transition-all duration-200 group"
              >
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-blue-200">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-medium text-gray-900 mb-1">Chat IA</h3>
                <p class="text-xs text-gray-500 text-center">Iniciar conversación</p>
              </button>
              
              <button
                @click="router.push('/analytics')"
                class="flex flex-col items-center p-6 bg-gray-50 rounded-lg hover:bg-green-50 hover:border-green-200 border border-gray-200 transition-all duration-200 group"
              >
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-green-200">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-medium text-gray-900 mb-1">Analíticas</h3>
                <p class="text-xs text-gray-500 text-center">Ver estadísticas</p>
              </button>
              
              <button
                @click="router.push('/chatbots')"
                class="flex flex-col items-center p-6 bg-gray-50 rounded-lg hover:bg-purple-50 hover:border-purple-200 border border-gray-200 transition-all duration-200 group"
              >
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-purple-200">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-medium text-gray-900 mb-1">Chatbots</h3>
                <p class="text-xs text-gray-500 text-center">Gestionar bots</p>
              </button>
              
              <button
                @click="router.push('/dashboard/integrations')"
                class="flex flex-col items-center p-6 bg-gray-50 rounded-lg hover:bg-indigo-50 hover:border-indigo-200 border border-gray-200 transition-all duration-200 group"
              >
                <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-indigo-200">
                  <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                  </svg>
                </div>
                <h3 class="text-sm font-medium text-gray-900 mb-1">Integraciones</h3>
                <p class="text-xs text-gray-500 text-center">Conectar servicios</p>
              </button>
              
              <button
                @click="router.push('/configuracion')"
                class="flex flex-col items-center p-6 bg-gray-50 rounded-lg hover:bg-orange-50 hover:border-orange-200 border border-gray-200 transition-all duration-200 group"
              >
                <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-3 group-hover:bg-orange-200">
                  <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                </div>
                <h3 class="text-sm font-medium text-gray-900 mb-1">Configuración</h3>
                <p class="text-xs text-gray-500 text-center">Ajustar sistema</p>
              </button>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-lg font-semibold text-gray-900">Actividad Reciente</h2>
                <p class="text-sm text-gray-500">Últimas acciones realizadas en el sistema</p>
              </div>
              <button 
                @click="scrollToTop"
                class="text-sm text-blue-600 hover:text-blue-800 flex items-center space-x-1"
                title="Ir al inicio"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
                </svg>
                <span>Inicio</span>
              </button>
            </div>
          </div>
          <div class="p-6">
            <div class="max-h-96 overflow-y-auto scrollable space-y-4">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg v-if="activity.type === 'chat'" class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                  </svg>
                  <svg v-else-if="activity.type === 'bot'" class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  <svg v-else-if="activity.type === 'report'" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                  <svg v-else class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                    <span class="text-xs text-gray-500">{{ activity.time }}</span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ activity.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>


      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Reactive data
const currentTime = ref('')

// Stats data
const stats = ref({
  conversations: 24,
  tokensUsed: 15420,
  uptime: '99.9%',
  users: 156,
  integrations: {
    active: 3,
    total: 4,
    webhooks: 5,
    apiKeys: 8
  }
})

// Recent activity data
const recentActivity = ref([
  {
    id: 1,
    type: 'chat',
    title: 'Nueva conversación iniciada',
    description: 'Sesión de chat sobre desarrollo web con IA',
    time: 'hace 5 min'
  },
  {
    id: 2,
    type: 'bot',
    title: 'Chatbot actualizado',
    description: 'Mejoras implementadas en el modelo de IA',
    time: 'hace 1 hora'
  },
  {
    id: 3,
    type: 'report',
    title: 'Reporte de analíticas generado',
    description: 'Análisis de uso y rendimiento semanal',
    time: 'hace 2 horas'
  },
  {
    id: 4,
    type: 'user',
    title: 'Nuevo usuario registrado',
    description: 'Usuario corporativo se unió al sistema',
    time: 'hace 3 horas'
  }
])

// Update time every second
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

let timeInterval

// Simulate stats updates
const updateStats = () => {
  // Simulate real-time updates
  if (Math.random() > 0.7) {
    stats.value.conversations += Math.floor(Math.random() * 3)
    stats.value.tokensUsed += Math.floor(Math.random() * 100)
    stats.value.users += Math.floor(Math.random() * 2)
  }
}

// Scroll to top function
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// Integration management
const openIntegration = (type) => {
  switch (type) {
    case 'slack':
      router.push('/dashboard/integrations?tab=slack')
      break
    case 'webhooks':
      router.push('/dashboard/integrations?tab=webhooks')
      break
    case 'apikeys':
      router.push('/dashboard/integrations?tab=apikeys')
      break
    case 'stripe':
      router.push('/dashboard/integrations?tab=stripe')
      break
    default:
      router.push('/dashboard/integrations')
  }
}

// Lifecycle
onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 60000) // Update every minute
  
  // Update stats periodically
  setInterval(updateStats, 30000) // Every 30 seconds
  
  console.log('✅ Dashboard corporativo cargado correctamente')
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>