<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-md shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">Invitar Miembro</h3>
          <p class="text-sm text-gray-600 mt-1">Envía una invitación para unirse al equipo</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="sendInvitation" class="mt-6 space-y-6">
        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Correo Electrónico *
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="usuario@empresa.com"
          />
        </div>

        <!-- Name (Optional) -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
            Nombre (Opcional)
          </label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Nombre completo"
          />
        </div>

        <!-- Role -->
        <div>
          <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
            Rol *
          </label>
          <select
            id="role"
            v-model="form.role"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Seleccionar rol</option>
            <option v-for="role in availableRoles" :key="role.id" :value="role.name">
              {{ role.displayName }}
            </option>
          </select>
          <p v-if="selectedRoleDescription" class="mt-1 text-sm text-gray-500">
            {{ selectedRoleDescription }}
          </p>
        </div>

        <!-- Message (Optional) -->
        <div>
          <label for="message" class="block text-sm font-medium text-gray-700 mb-2">
            Mensaje Personal (Opcional)
          </label>
          <textarea
            id="message"
            v-model="form.message"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Mensaje de bienvenida personalizado..."
          ></textarea>
        </div>

        <!-- Send Copy -->
        <div class="flex items-center">
          <input
            id="send-copy"
            v-model="form.sendCopy"
            type="checkbox"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label for="send-copy" class="ml-2 block text-sm text-gray-700">
            Enviarme una copia de la invitación
          </label>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="isLoading">Enviando...</span>
            <span v-else>Enviar Invitación</span>
            <PaperAirplaneIcon v-if="!isLoading" class="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { XMarkIcon, PaperAirplaneIcon } from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  roles: {
    type: Array,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'invite'])

// Reactive state
const isLoading = ref(false)
const form = ref({
  email: '',
  name: '',
  role: '',
  message: '',
  sendCopy: false
})

// Computed properties
const availableRoles = computed(() => {
  // Filter out admin role for security
  return props.roles.filter(role => role.name !== 'admin')
})

const selectedRoleDescription = computed(() => {
  if (!form.value.role) return ''
  const role = props.roles.find(r => r.name === form.value.role)
  return role ? role.description : ''
})

const isFormValid = computed(() => {
  return form.value.email && form.value.role
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const sendInvitation = async () => {
  if (!isFormValid.value) return
  
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    emit('invite', {
      email: form.value.email,
      name: form.value.name,
      role: form.value.role,
      message: form.value.message,
      sendCopy: form.value.sendCopy
    })
    
    emit('close')
  } catch (error) {
    console.error('Error sending invitation:', error)
  } finally {
    isLoading.value = false
  }
}
</script>