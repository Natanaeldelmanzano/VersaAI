<template>
  <div style="padding: 20px; background: white; margin: 20px; border: 5px solid red;">
    <h1 style="color: red; font-size: 32px; background: yellow; padding: 10px;">🔥 SIMPLE TEST FUNCIONANDO</h1>
    <p style="color: blue; font-size: 18px;">Si ves esto, Vue.js está funcionando correctamente</p>
    <p style="color: green; font-size: 16px;">Contador: {{ count }}</p>
    <button 
      @click="count++" 
      style="background: green; color: white; padding: 10px; margin: 5px; border: none; font-size: 16px;"
    >
      Incrementar: {{ count }}
    </button>
    <button 
      @click="count = 0" 
      style="background: red; color: white; padding: 10px; margin: 5px; border: none; font-size: 16px;"
    >
      Reset
    </button>
    <div style="margin-top: 20px; padding: 10px; background: #f0f0f0; border: 2px solid #333;">
      <h3>Estado de Vue:</h3>
      <p>✅ Componente montado</p>
      <p>✅ Reactividad funcionando</p>
      <p>✅ Eventos funcionando</p>
      <p>Timestamp: {{ timestamp }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const count = ref(0)
const timestamp = ref('')

onMounted(() => {
  timestamp.value = new Date().toISOString()
  console.log('🔥 SimpleTest.vue montado exitosamente!')
  console.log('📊 Estado inicial:', { count: count.value, timestamp: timestamp.value })
})

console.log('📄 SimpleTest.vue script ejecutado')
</script>

<style>
/* Sin estilos adicionales para evitar conflictos */
</style>