<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Crea tu cuenta
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          ¿Ya tienes una cuenta?
          <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500">
            Inicia sesión aquí
          </router-link>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700">Nombre completo</label>
            <input
              id="full_name"
              v-model="form.full_name"
              name="full_name"
              type="text"
              autocomplete="name"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Tu nombre completo"
              :disabled="loading"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="tu@email.com"
              :disabled="loading"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Mínimo 8 caracteres"
              :disabled="loading"
            />
          </div>
          
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700">Confirmar contraseña</label>
            <input
              id="confirm_password"
              v-model="form.confirm_password"
              name="confirm_password"
              type="password"
              autocomplete="new-password"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Repite tu contraseña"
              :disabled="loading"
            />
          </div>
          
          <div>
            <label for="organization_name" class="block text-sm font-medium text-gray-700">Nombre de la organización</label>
            <input
              id="organization_name"
              v-model="form.organization_name"
              name="organization_name"
              type="text"
              required
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Mi Empresa S.A."
              :disabled="loading"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            id="accept-terms"
            v-model="form.acceptTerms"
            name="accept-terms"
            type="checkbox"
            required
            class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            :disabled="loading"
          />
          <label for="accept-terms" class="ml-2 block text-sm text-gray-900">
            Acepto los
            <a href="#" class="text-primary-600 hover:text-primary-500">términos y condiciones</a>
            y la
            <a href="#" class="text-primary-600 hover:text-primary-500">política de privacidad</a>
          </label>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            :disabled="loading || !isFormValid"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <UserPlusIcon class="h-5 w-5 text-primary-500 group-hover:text-primary-400" aria-hidden="true" />
            </span>
            <span v-if="loading" class="flex items-center">
              <div class="spinner mr-2"></div>
              Creando cuenta...
            </span>
            <span v-else>Crear cuenta</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlusIcon } from '@heroicons/vue/20/solid'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const loading = ref(false)
const form = reactive({
  full_name: '',
  email: '',
  password: '',
  confirm_password: '',
  organization_name: '',
  acceptTerms: false
})

const isFormValid = computed(() => {
  return (
    form.full_name.trim() &&
    form.email.trim() &&
    form.password.length >= 8 &&
    form.password === form.confirm_password &&
    form.organization_name.trim() &&
    form.acceptTerms
  )
})

const handleRegister = async () => {
  if (loading.value || !isFormValid.value) return
  
  if (form.password !== form.confirm_password) {
    toast.error('Las contraseñas no coinciden')
    return
  }
  
  loading.value = true
  
  try {
    await authStore.register({
      full_name: form.full_name,
      email: form.email,
      password: form.password,
      organization_name: form.organization_name
    })
    
    toast.success('¡Cuenta creada exitosamente! Bienvenido a VersaAI')
    router.push('/dashboard')
  } catch (error) {
    console.error('Registration error:', error)
    toast.error(error.response?.data?.detail || 'Error al crear la cuenta')
  } finally {
    loading.value = false
  }
}
</script>