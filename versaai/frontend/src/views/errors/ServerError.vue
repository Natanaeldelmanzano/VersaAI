<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <!-- 500 Illustration -->
        <div class="mx-auto h-32 w-32 text-red-600 mb-8">
          <svg viewBox="0 0 200 200" class="w-full h-full">
            <!-- Server Rack -->
            <rect x="50" y="40" width="100" height="120" rx="8" fill="currentColor" opacity="0.1" />
            <rect x="55" y="45" width="90" height="110" rx="4" fill="currentColor" opacity="0.2" />
            
            <!-- Server Units -->
            <rect x="60" y="55" width="80" height="15" rx="2" fill="currentColor" opacity="0.3" />
            <rect x="60" y="75" width="80" height="15" rx="2" fill="currentColor" opacity="0.3" />
            <rect x="60" y="95" width="80" height="15" rx="2" fill="currentColor" opacity="0.3" />
            <rect x="60" y="115" width="80" height="15" rx="2" fill="currentColor" opacity="0.3" />
            <rect x="60" y="135" width="80" height="15" rx="2" fill="currentColor" opacity="0.3" />
            
            <!-- Status Lights (Red) -->
            <circle cx="130" cy="62" r="3" fill="currentColor" opacity="0.8" />
            <circle cx="130" cy="82" r="3" fill="currentColor" opacity="0.8" />
            <circle cx="130" cy="102" r="3" fill="currentColor" opacity="0.8" />
            <circle cx="130" cy="122" r="3" fill="currentColor" opacity="0.8" />
            <circle cx="130" cy="142" r="3" fill="currentColor" opacity="0.8" />
            
            <!-- Ventilation Grilles -->
            <line x1="65" y1="60" x2="75" y2="60" stroke="currentColor" stroke-width="1" opacity="0.4" />
            <line x1="65" y1="65" x2="75" y2="65" stroke="currentColor" stroke-width="1" opacity="0.4" />
            <line x1="65" y1="80" x2="75" y2="80" stroke="currentColor" stroke-width="1" opacity="0.4" />
            <line x1="65" y1="85" x2="75" y2="85" stroke="currentColor" stroke-width="1" opacity="0.4" />
            
            <!-- Error Sparks -->
            <g opacity="0.6">
              <path d="M40 30 L45 25 L42 35 L48 32" stroke="currentColor" stroke-width="2" fill="none" />
              <path d="M160 35 L165 30 L162 40 L168 37" stroke="currentColor" stroke-width="2" fill="none" />
              <path d="M45 170 L50 165 L47 175 L53 172" stroke="currentColor" stroke-width="2" fill="none" />
              <path d="M155 175 L160 170 L157 180 L163 177" stroke="currentColor" stroke-width="2" fill="none" />
            </g>
            
            <!-- Smoke/Steam -->
            <g opacity="0.3">
              <circle cx="85" cy="25" r="3" fill="currentColor" />
              <circle cx="95" cy="20" r="4" fill="currentColor" />
              <circle cx="105" cy="15" r="3" fill="currentColor" />
              <circle cx="115" cy="25" r="3" fill="currentColor" />
            </g>
          </svg>
        </div>
        
        <!-- Error Message -->
        <h1 class="text-6xl font-bold text-gray-900 mb-4">500</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Error Interno del Servidor</h2>
        <p class="text-gray-600 mb-8 max-w-md mx-auto">
          Algo salió mal en nuestros servidores. Nuestro equipo técnico ha sido notificado 
          y está trabajando para resolver el problema.
        </p>
        
        <!-- Action Buttons -->
        <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
          <button
            @click="refreshPage"
            :disabled="refreshing"
            class="w-full sm:w-auto bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 disabled:opacity-50"
          >
            {{ refreshing ? 'Recargando...' : 'Intentar de Nuevo' }}
          </button>
          <button
            @click="goBack"
            class="w-full sm:w-auto bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200"
          >
            Volver Atrás
          </button>
        </div>
        
        <!-- Error Details -->
        <div class="mt-12 pt-8 border-t border-gray-200">
          <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationCircleIcon class="h-5 w-5 text-red-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Detalles del Error
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <p class="mb-2">Código de Error: <span class="font-mono">{{ errorCode }}</span></p>
                  <p class="mb-2">Tiempo: <span class="font-mono">{{ errorTime }}</span></p>
                  <p v-if="errorId">ID de Seguimiento: <span class="font-mono">{{ errorId }}</span></p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div class="flex">
              <div class="flex-shrink-0">
                <InformationCircleIcon class="h-5 w-5 text-blue-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-800">
                  ¿Qué puedes hacer?
                </h3>
                <div class="mt-2 text-sm text-blue-700">
                  <ul class="list-disc list-inside space-y-1">
                    <li>Espera unos minutos e intenta de nuevo</li>
                    <li>Verifica tu conexión a internet</li>
                    <li>Contacta a soporte si el problema persiste</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <p class="text-sm text-gray-500 mb-4">¿Necesitas ayuda inmediata?</p>
          <div class="flex justify-center space-x-6 text-sm">
            <a href="mailto:soporte@versaai.com" class="text-primary-600 hover:text-primary-500">
              Contactar Soporte
            </a>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Estado del Sistema
            </router-link>
            <router-link to="/" class="text-primary-600 hover:text-primary-500">
              Centro de Ayuda
            </router-link>
          </div>
        </div>
        
        <!-- Auto Refresh Timer -->
        <div v-if="autoRefresh" class="mt-8 p-4 bg-gray-100 rounded-lg">
          <div class="flex items-center justify-center">
            <ClockIcon class="h-5 w-5 text-gray-500 mr-2" />
            <span class="text-sm text-gray-600">
              Reintentando automáticamente en {{ countdown }} segundos
            </span>
            <button
              @click="cancelAutoRefresh"
              class="ml-4 text-sm text-primary-600 hover:text-primary-500"
            >
              Cancelar
            </button>
          </div>
          <div class="mt-2 w-full bg-gray-200 rounded-full h-1">
            <div
              class="bg-primary-600 h-1 rounded-full transition-all duration-1000"
              :style="{ width: `${(30 - countdown) / 30 * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ExclamationCircleIcon,
  InformationCircleIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'

const router = useRouter()

const refreshing = ref(false)
const autoRefresh = ref(true)
const countdown = ref(30)
let countdownInterval = null

const errorCode = ref('ERR_INTERNAL_SERVER_ERROR')
const errorTime = ref(format(new Date(), 'dd/MM/yyyy HH:mm:ss', { locale: es }))
const errorId = ref(`ERR-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`)

const refreshPage = async () => {
  refreshing.value = true
  try {
    // Simulate a delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    window.location.reload()
  } catch (error) {
    console.error('Error refreshing page:', error)
  } finally {
    refreshing.value = false
  }
}

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}

const startCountdown = () => {
  countdownInterval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      refreshPage()
    }
  }, 1000)
}

const cancelAutoRefresh = () => {
  autoRefresh.value = false
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

onMounted(() => {
  if (autoRefresh.value) {
    startCountdown()
  }
})

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
})
</script>