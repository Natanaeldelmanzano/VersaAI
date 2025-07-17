<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo and brand -->
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center">
                <span class="text-white font-bold text-xl">V</span>
              </div>
              <div>
                <span class="text-2xl font-bold text-gradient">VersaAI</span>
                <div class="text-xs text-gray-500 -mt-1">Chatbots Empresariales</div>
              </div>
            </router-link>
          </div>

          <!-- Desktop navigation -->
          <div class="hidden md:flex items-center space-x-8">
            <router-link
              to="/"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
              :class="{ 'text-primary-600': $route.name === 'Home' }"
            >
              Inicio
            </router-link>
            <a
              href="#features"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Características
            </a>
            <a
              href="#pricing"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Precios
            </a>
            <router-link
              to="/widget-demo"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
              :class="{ 'text-primary-600': $route.name === 'WidgetDemo' }"
            >
              Demo
            </router-link>
            <a
              href="/docs"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Docs
            </a>
          </div>

          <!-- Auth buttons -->
          <div class="hidden md:flex items-center space-x-4">
            <template v-if="!authStore.isAuthenticated">
              <router-link
                to="/auth/login"
                class="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
              >
                Iniciar Sesión
              </router-link>
              <router-link
                to="/auth/register"
                class="btn-primary text-sm"
              >
                Registrarse
              </router-link>
            </template>
            <template v-else>
              <router-link
                to="/dashboard"
                class="btn-primary text-sm"
              >
                Dashboard
              </router-link>
            </template>
          </div>

          <!-- Mobile menu button -->
          <div class="md:hidden flex items-center">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="text-gray-700 hover:text-primary-600 focus:outline-none focus:text-primary-600"
            >
              <Bars3Icon v-if="!mobileMenuOpen" class="h-6 w-6" />
              <XMarkIcon v-else class="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-50">
          <router-link
            to="/"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
            :class="{ 'text-primary-600 bg-primary-50': $route.name === 'Home' }"
          >
            Inicio
          </router-link>
          <a
            href="#features"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
          >
            Características
          </a>
          <a
            href="#pricing"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
          >
            Precios
          </a>
          <router-link
            to="/widget-demo"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
            :class="{ 'text-primary-600 bg-primary-50': $route.name === 'WidgetDemo' }"
          >
            Demo
          </router-link>
          <a
            href="/docs"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
          >
            Documentación
          </a>
          
          <!-- Mobile auth buttons -->
          <div class="pt-4 border-t border-gray-200">
            <template v-if="!authStore.isAuthenticated">
              <router-link
                to="/auth/login"
                @click="mobileMenuOpen = false"
                class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
              >
                Iniciar Sesión
              </router-link>
              <router-link
                to="/auth/register"
                @click="mobileMenuOpen = false"
                class="block mt-2 mx-3 btn-primary text-center"
              >
                Registrarse
              </router-link>
            </template>
            <template v-else>
              <router-link
                to="/dashboard"
                @click="mobileMenuOpen = false"
                class="block mx-3 btn-primary text-center"
              >
                Dashboard
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main>
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <!-- Brand -->
          <div class="col-span-1 md:col-span-2">
            <div class="flex items-center space-x-3 mb-4">
              <div class="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center">
                <span class="text-white font-bold text-xl">V</span>
              </div>
              <div>
                <span class="text-2xl font-bold text-white">VersaAI</span>
                <div class="text-sm text-gray-400 -mt-1">Chatbots Empresariales</div>
              </div>
            </div>
            <p class="text-gray-400 text-sm max-w-md">
              Plataforma de IA empresarial optimizada para recursos limitados con capacidades RAG avanzadas.
              Crea chatbots inteligentes para tu negocio en minutos.
            </p>
            <div class="mt-4 flex space-x-4">
              <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <span class="sr-only">Twitter</span>
                <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                </svg>
              </a>
              <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <span class="sr-only">GitHub</span>
                <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                </svg>
              </a>
              <a href="#" class="text-gray-400 hover:text-white transition-colors duration-200">
                <span class="sr-only">LinkedIn</span>
                <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M19 0H5a5 5 0 00-5 5v14a5 5 0 005 5h14a5 5 0 005-5V5a5 5 0 00-5-5zM8 19H5V8h3v11zM6.5 6.732c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zM20 19h-3v-5.604c0-3.368-4-3.113-4 0V19h-3V8h3v1.765c1.396-2.586 7-2.777 7 2.476V19z" clip-rule="evenodd" />
                </svg>
              </a>
            </div>
          </div>

          <!-- Links -->
          <div>
            <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Producto</h3>
            <ul class="space-y-2">
              <li><a href="#features" class="text-gray-400 hover:text-white transition-colors duration-200">Características</a></li>
              <li><a href="#pricing" class="text-gray-400 hover:text-white transition-colors duration-200">Precios</a></li>
              <li><router-link to="/widget-demo" class="text-gray-400 hover:text-white transition-colors duration-200">Demo</router-link></li>
              <li><a href="/docs" class="text-gray-400 hover:text-white transition-colors duration-200">API</a></li>
            </ul>
          </div>

          <!-- Support -->
          <div>
            <h3 class="text-sm font-semibold text-white tracking-wider uppercase mb-4">Soporte</h3>
            <ul class="space-y-2">
              <li><a href="/docs" class="text-gray-400 hover:text-white transition-colors duration-200">Documentación</a></li>
              <li><a href="mailto:support@versaai.com" class="text-gray-400 hover:text-white transition-colors duration-200">Contacto</a></li>
              <li><a href="/status" class="text-gray-400 hover:text-white transition-colors duration-200">Estado del Sistema</a></li>
              <li><a href="/privacy" class="text-gray-400 hover:text-white transition-colors duration-200">Privacidad</a></li>
            </ul>
          </div>
        </div>

        <div class="mt-8 pt-8 border-t border-gray-800">
          <div class="flex flex-col md:flex-row justify-between items-center">
            <p class="text-gray-400 text-sm">
              © {{ currentYear }} VersaAI. Todos los derechos reservados.
            </p>
            <div class="mt-4 md:mt-0 flex space-x-6 text-sm text-gray-400">
              <a href="/terms" class="hover:text-white transition-colors duration-200">Términos</a>
              <a href="/privacy" class="hover:text-white transition-colors duration-200">Privacidad</a>
              <a href="/cookies" class="hover:text-white transition-colors duration-200">Cookies</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

const currentYear = computed(() => new Date().getFullYear())
</script>