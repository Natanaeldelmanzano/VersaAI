<template>
  <div class="test-component bg-red-500 text-white p-4 m-4 rounded">
    <h1 class="text-2xl font-bold">COMPONENTE DE PRUEBA</h1>
    <p>Si puedes ver esto, Vue está funcionando correctamente.</p>
    <p>Hora actual: {{ currentTime }}</p>
    <button @click="updateTime" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2">
      Actualizar Hora
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentTime = ref(new Date().toLocaleString())

const updateTime = () => {
  currentTime.value = new Date().toLocaleString()
}

onMounted(() => {
  console.log('TestComponent montado correctamente')
})
</script>

<style scoped>
.test-component {
  border: 3px solid #000;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
</style>