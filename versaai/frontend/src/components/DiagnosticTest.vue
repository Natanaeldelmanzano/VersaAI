<template>
  <div style="background: red; color: white; padding: 20px; font-size: 24px; text-align: center;">
    <h1>🚨 DIAGNÓSTICO ACTIVO</h1>
    <p>Si ves este mensaje, Vue.js está funcionando</p>
    <p>Contador: {{ count }}</p>
    <button @click="count++" style="background: blue; color: white; padding: 10px; margin: 10px; border: none; border-radius: 5px;">
      Incrementar
    </button>
    <div style="margin-top: 20px;">
      <p>✅ Vue.js 3 cargado</p>
      <p>✅ Componente reactivo funcionando</p>
      <p>✅ Estilos inline aplicados</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)

console.log('🔥 DiagnosticTest component loaded!')
console.log('🔥 Current count:', count.value)
</script>

<style>
/* Sin estilos externos para evitar problemas */
</style>