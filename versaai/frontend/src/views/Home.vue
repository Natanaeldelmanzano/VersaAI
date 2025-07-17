<template>
  <div>
    <!-- Hero Section -->
    <section class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto">
        <div class="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
          <svg
            class="hidden lg:block absolute right-0 inset-y-0 h-full w-48 text-white transform translate-x-1/2"
            fill="currentColor"
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
            aria-hidden="true"
          >
            <polygon points="50,0 100,0 50,100 0,100" />
          </svg>

          <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span class="block xl:inline">Chatbots</span>
                <span class="block text-gradient xl:inline">Empresariales</span>
                <span class="block xl:inline">Inteligentes</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Plataforma de IA empresarial optimizada para recursos limitados con capacidades RAG avanzadas. 
                Crea chatbots inteligentes que entienden tu negocio en minutos.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <router-link
                    to="/auth/register"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-gradient-primary hover:opacity-90 md:py-4 md:text-lg md:px-10 transition-opacity duration-200"
                  >
                    Comenzar Gratis
                  </router-link>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-3">
                  <router-link
                    to="/widget-demo"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 md:py-4 md:text-lg md:px-10 transition-colors duration-200"
                  >
                    Ver Demo
                  </router-link>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
      <div class="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
        <img
          class="h-56 w-full object-cover sm:h-72 md:h-96 lg:w-full lg:h-full"
          src="https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80"
          alt="AI Chatbot Dashboard"
        />
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">Características</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Todo lo que necesitas para crear chatbots inteligentes
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            VersaAI combina la potencia de la IA moderna con una arquitectura optimizada para recursos limitados.
          </p>
        </div>

        <div class="mt-10">
          <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div v-for="feature in features" :key="feature.name" class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <component :is="feature.icon" class="h-6 w-6" aria-hidden="true" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ feature.name }}</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">{{ feature.description }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="bg-primary-800">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:py-16 sm:px-6 lg:px-8 lg:py-20">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
            Confiado por empresas de todo el mundo
          </h2>
          <p class="mt-3 text-xl text-primary-200 sm:mt-4">
            Optimizado para equipos con recursos limitados pero grandes ambiciones
          </p>
        </div>
        <dl class="mt-10 text-center sm:max-w-3xl sm:mx-auto sm:grid sm:grid-cols-3 sm:gap-8">
          <div v-for="stat in stats" :key="stat.label" class="flex flex-col">
            <dt class="order-2 mt-2 text-lg leading-6 font-medium text-primary-200">{{ stat.label }}</dt>
            <dd class="order-1 text-5xl font-extrabold text-white">{{ stat.value }}</dd>
          </div>
        </dl>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="bg-gray-50">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:py-16 sm:px-6 lg:px-8">
        <div class="sm:flex sm:flex-col sm:align-center">
          <h1 class="text-5xl font-extrabold text-gray-900 sm:text-center">Precios</h1>
          <p class="mt-5 text-xl text-gray-500 sm:text-center">
            Comienza gratis y escala según tus necesidades
          </p>
        </div>
        <div class="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-2 sm:gap-6 lg:max-w-4xl lg:mx-auto xl:max-w-none xl:mx-0 xl:grid-cols-3">
          <div v-for="plan in pricingPlans" :key="plan.name" class="border border-gray-200 rounded-lg shadow-sm divide-y divide-gray-200">
            <div class="p-6">
              <h2 class="text-lg leading-6 font-medium text-gray-900">{{ plan.name }}</h2>
              <p class="mt-4 text-sm text-gray-500">{{ plan.description }}</p>
              <p class="mt-8">
                <span class="text-4xl font-extrabold text-gray-900">${{ plan.price }}</span>
                <span class="text-base font-medium text-gray-500">/mes</span>
              </p>
              <router-link
                to="/auth/register"
                :class="[
                  'mt-8 block w-full border border-transparent rounded-md py-2 text-sm font-semibold text-center transition-colors duration-200',
                  plan.featured
                    ? 'bg-primary-600 text-white hover:bg-primary-700'
                    : 'bg-primary-50 text-primary-700 hover:bg-primary-100'
                ]"
              >
                {{ plan.cta }}
              </router-link>
            </div>
            <div class="pt-6 pb-8 px-6">
              <h3 class="text-xs font-medium text-gray-900 tracking-wide uppercase">Incluye</h3>
              <ul class="mt-6 space-y-4">
                <li v-for="feature in plan.features" :key="feature" class="flex space-x-3">
                  <CheckIcon class="flex-shrink-0 h-5 w-5 text-green-500" aria-hidden="true" />
                  <span class="text-sm text-gray-500">{{ feature }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-white">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          <span class="block">¿Listo para comenzar?</span>
          <span class="block text-primary-600">Crea tu primer chatbot hoy.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <router-link
              to="/auth/register"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors duration-200"
            >
              Comenzar Gratis
            </router-link>
          </div>
          <div class="ml-3 inline-flex rounded-md shadow">
            <router-link
              to="/widget-demo"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50 transition-colors duration-200"
            >
              Ver Demo
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import {
  ChatBubbleLeftRightIcon,
  CpuChipIcon,
  DocumentTextIcon,
  ChartBarIcon,
  CodeBracketIcon,
  ShieldCheckIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'

const features = [
  {
    name: 'Sistema RAG Avanzado',
    description: 'Integración con bases de conocimiento para respuestas precisas y contextuales basadas en tus documentos.',
    icon: DocumentTextIcon,
  },
  {
    name: 'Multi-tenancy Nativo',
    description: 'Arquitectura multi-tenant que permite gestionar múltiples organizaciones y usuarios de forma segura.',
    icon: ShieldCheckIcon,
  },
  {
    name: 'Widget Embebible',
    description: 'Integra fácilmente el chatbot en cualquier sitio web con nuestro widget personalizable.',
    icon: CodeBracketIcon,
  },
  {
    name: 'Analytics en Tiempo Real',
    description: 'Dashboard completo con métricas detalladas sobre el rendimiento y uso de tus chatbots.',
    icon: ChartBarIcon,
  },
  {
    name: 'IA Conversacional',
    description: 'Powered by Groq-Claude API para conversaciones naturales y respuestas inteligentes.',
    icon: ChatBubbleLeftRightIcon,
  },
  {
    name: 'Optimizado para 8GB RAM',
    description: 'Arquitectura eficiente diseñada para funcionar perfectamente en recursos limitados.',
    icon: CpuChipIcon,
  },
]

const stats = [
  { label: 'Tiempo de Setup', value: '< 5min' },
  { label: 'Uso de RAM', value: '< 8GB' },
  { label: 'Uptime', value: '99.9%' },
]

const pricingPlans = [
  {
    name: 'Starter',
    description: 'Perfecto para proyectos pequeños y pruebas.',
    price: '0',
    cta: 'Comenzar Gratis',
    featured: false,
    features: [
      '1 Chatbot',
      '1,000 mensajes/mes',
      '1 Base de conocimiento',
      'Widget básico',
      'Soporte por email',
    ],
  },
  {
    name: 'Professional',
    description: 'Ideal para empresas en crecimiento.',
    price: '29',
    cta: 'Comenzar Prueba',
    featured: true,
    features: [
      '5 Chatbots',
      '10,000 mensajes/mes',
      '5 Bases de conocimiento',
      'Widget personalizable',
      'Analytics avanzados',
      'Soporte prioritario',
    ],
  },
  {
    name: 'Enterprise',
    description: 'Para organizaciones grandes con necesidades específicas.',
    price: '99',
    cta: 'Contactar Ventas',
    featured: false,
    features: [
      'Chatbots ilimitados',
      'Mensajes ilimitados',
      'Bases de conocimiento ilimitadas',
      'Widget white-label',
      'Analytics personalizados',
      'Soporte dedicado',
      'SLA garantizado',
    ],
  },
]
</script>