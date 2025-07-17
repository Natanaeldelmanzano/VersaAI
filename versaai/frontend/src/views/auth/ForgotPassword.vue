<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          ¿Olvidaste tu contraseña?
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          No te preocupes, te enviaremos un enlace para restablecerla.
        </p>
      </div>
      
      <div v-if="emailSent" class="rounded-md bg-green-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <CheckCircleIcon class="h-5 w-5 text-green-400" aria-hidden="true" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">
              Email enviado
            </h3>
            <div class="mt-2 text-sm text-green-700">
              <p>
                Hemos enviado un enlace de recuperación a <strong>{{ form.email }}</strong>.
                Revisa tu bandeja de entrada y sigue las instrucciones.
              </p>
            </div>
            <div class="mt-4">
              <div class="-mx-2 -my-1.5 flex">
                <button
                  type="button"
                  @click="resetForm"
                  class="bg-green-50 px-2 py-1.5 rounded-md text-sm font-medium text-green-800 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-green-600"
                >
                  Enviar a otro email
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleForgotPassword">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Dirección de email
          </label>
          <div class="mt-1">
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="tu@email.com"
              :disabled="loading"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            :disabled="loading"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <EnvelopeIcon class="h-5 w-5 text-primary-500 group-hover:text-primary-400" aria-hidden="true" />
            </span>
            <span v-if="loading" class="flex items-center">
              <div class="spinner mr-2"></div>
              Enviando...
            </span>
            <span v-else>Enviar enlace de recuperación</span>
          </button>
        </div>
        
        <div class="text-center">
          <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
            ← Volver al inicio de sesión
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { EnvelopeIcon, CheckCircleIcon } from '@heroicons/vue/20/solid'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const toast = useToast()

const loading = ref(false)
const emailSent = ref(false)
const form = reactive({
  email: ''
})

const handleForgotPassword = async () => {
  if (loading.value) return
  
  loading.value = true
  
  try {
    await authStore.forgotPassword(form.email)
    emailSent.value = true
    toast.success('Enlace de recuperación enviado')
  } catch (error) {
    console.error('Forgot password error:', error)
    toast.error(error.response?.data?.detail || 'Error al enviar el enlace de recuperación')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  emailSent.value = false
  form.email = ''
}
</script>