<template>
  <div>
    <h1>ULTRA SIMPLE TEST</h1>
    <p>Si ves esto, Vue funciona</p>
    <p>Contador: {{ count }}</p>
    <button @click="count++">+</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const count = ref(0)
console.log('UltraSimpleTest cargado')
</script>

<style>
h1 {
  color: red;
  font-size: 32px;
  background: yellow;
  padding: 20px;
}
p {
  color: blue;
  font-size: 18px;
}
button {
  background: green;
  color: white;
  padding: 10px;
  font-size: 16px;
}
</style>