<template>
  <div style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); min-height: 100vh; padding: 20px; font-family: Arial, sans-serif;">
    <div style="background: white; border-radius: 10px; padding: 30px; max-width: 800px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
      <h1 style="color: #333; font-size: 2.5rem; margin-bottom: 20px; text-align: center;">🔧 DIAGNÓSTICO VERSAAI</h1>
      
      <div style="background: #e8f5e8; border: 2px solid #4caf50; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h2 style="color: #2e7d32; margin: 0 0 10px 0;">✅ ESTADO DEL SISTEMA</h2>
        <p style="margin: 5px 0; color: #333;">🟢 Vue.js: FUNCIONANDO</p>
        <p style="margin: 5px 0; color: #333;">🟢 JavaScript: FUNCIONANDO</p>
        <p style="margin: 5px 0; color: #333;">🟢 CSS: FUNCIONANDO</p>
        <p style="margin: 5px 0; color: #333;">🟢 Tiempo actual: {{ currentTime }}</p>
      </div>

      <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h2 style="color: #856404; margin: 0 0 10px 0;">⚠️ PRUEBAS INTERACTIVAS</h2>
        <button 
          @click="testClick" 
          style="background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;"
        >
          PROBAR CLICK
        </button>
        <button 
          @click="testAlert" 
          style="background: #28a745; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px;"
        >
          PROBAR ALERTA
        </button>
        <p v-if="clicked" style="color: #28a745; font-weight: bold; margin: 10px 0;">✅ EVENTOS FUNCIONANDO CORRECTAMENTE</p>
      </div>

      <div style="background: #f8d7da; border: 2px solid #dc3545; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h2 style="color: #721c24; margin: 0 0 10px 0;">🚨 LOGS DEL SISTEMA</h2>
        <div style="background: #000; color: #00ff00; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; max-height: 200px; overflow-y: auto;">
          <div v-for="(log, index) in logs" :key="index" style="margin: 2px 0; font-size: 14px;">
            {{ log }}
          </div>
        </div>
      </div>

      <div style="background: #d1ecf1; border: 2px solid #17a2b8; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <h2 style="color: #0c5460; margin: 0 0 10px 0;">ℹ️ INFORMACIÓN DEL NAVEGADOR</h2>
        <p style="margin: 5px 0; color: #333;">🌐 User Agent: {{ userAgent }}</p>
        <p style="margin: 5px 0; color: #333;">📱 Pantalla: {{ screenInfo }}</p>
        <p style="margin: 5px 0; color: #333;">🔗 URL: {{ currentUrl }}</p>
      </div>

      <div style="text-align: center; margin-top: 30px;">
        <p style="font-size: 18px; color: #333; font-weight: bold;">Si puedes ver esta página, Vue.js está funcionando correctamente</p>
        <p style="font-size: 14px; color: #666; margin-top: 10px;">Versión de diagnóstico - Sin dependencias externas</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentTime = ref('')
const clicked = ref(false)
const logs = ref([])
const userAgent = ref('')
const screenInfo = ref('')
const currentUrl = ref('')

const addLog = (message) => {
  const timestamp = new Date().toLocaleTimeString()
  logs.value.unshift(`[${timestamp}] ${message}`)
  console.log(`[DIAGNOSTIC] ${message}`)
  
  // Mantener solo los últimos 10 logs
  if (logs.value.length > 10) {
    logs.value = logs.value.slice(0, 10)
  }
}

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}

const testClick = () => {
  clicked.value = true
  addLog('✅ Botón clickeado - Eventos Vue funcionando')
}

const testAlert = () => {
  alert('🎉 ¡JavaScript y Vue.js están funcionando correctamente!')
  addLog('✅ Alerta mostrada - JavaScript funcionando')
}

onMounted(() => {
  addLog('🚀 DiagnosticPage iniciado')
  addLog('⚡ Vue.js Composition API funcionando')
  addLog('🎨 CSS inline aplicado correctamente')
  
  // Información del navegador
  userAgent.value = navigator.userAgent.substring(0, 50) + '...'
  screenInfo.value = `${screen.width}x${screen.height}`
  currentUrl.value = window.location.href
  
  // Actualizar tiempo
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  // Capturar errores globales
  const originalError = window.onerror
  window.onerror = (message, source, lineno, colno, error) => {
    addLog(`❌ ERROR: ${message} en línea ${lineno}`)
    if (originalError) originalError(message, source, lineno, colno, error)
  }
  
  const originalUnhandledRejection = window.onunhandledrejection
  window.onunhandledrejection = (event) => {
    addLog(`❌ PROMISE ERROR: ${event.reason}`)
    if (originalUnhandledRejection) originalUnhandledRejection(event)
  }
  
  addLog('🛡️ Captura de errores configurada')
  addLog('✅ Página completamente cargada')
  
  // Cleanup
  return () => {
    clearInterval(timeInterval)
  }
})
</script>