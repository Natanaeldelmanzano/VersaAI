<template>
  <div class="pricing-page p-6 space-y-8">
    <!-- Header -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Planes y Precios</h1>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">
        Elige el plan perfecto para tu organización. Todos los planes incluyen soporte 24/7 y actualizaciones gratuitas.
      </p>
    </div>
    
    <!-- Toggle de Facturación -->
    <div class="flex items-center justify-center space-x-4">
      <span class="text-sm font-medium text-gray-900">Mensual</span>
      <button
        @click="isAnnual = !isAnnual"
        :class="[
          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
          isAnnual ? 'bg-primary-600' : 'bg-gray-200'
        ]"
      >
        <span
          :class="[
            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
            isAnnual ? 'translate-x-5' : 'translate-x-0'
          ]"
        ></span>
      </button>
      <span class="text-sm font-medium text-gray-900">
        Anual
        <span class="ml-1 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Ahorra 20%
        </span>
      </span>
    </div>
    
    <!-- Planes de Precios -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
      <!-- Plan Básico -->
      <PricingCard
        :plan="{
          id: 'basic',
          name: 'Básico',
          description: 'Perfecto para equipos pequeños que están comenzando',
          price: isAnnual ? 39 : 49,
          originalPrice: isAnnual ? 49 : null,
          period: isAnnual ? 'año' : 'mes',
          popular: false,
          features: [
            'Hasta 5 usuarios',
            '3 chatbots',
            '1,000 conversaciones/mes',
            'Soporte por email',
            'Analytics básicos',
            'Integraciones básicas',
            'Plantillas predefinidas'
          ],
          limitations: [
            'Sin API access',
            'Sin SSO',
            'Sin white label',
            'Sin soporte prioritario'
          ],
          cta: 'Comenzar Gratis',
          highlight: false
        }"
        @select="selectPlan"
      />
      
      <!-- Plan Profesional -->
      <PricingCard
        :plan="{
          id: 'professional',
          name: 'Profesional',
          description: 'Ideal para equipos en crecimiento con necesidades avanzadas',
          price: isAnnual ? 119 : 149,
          originalPrice: isAnnual ? 149 : null,
          period: isAnnual ? 'año' : 'mes',
          popular: true,
          features: [
            'Hasta 25 usuarios',
            '10 chatbots',
            '10,000 conversaciones/mes',
            'Soporte prioritario',
            'Analytics avanzados',
            'API access',
            'Integraciones avanzadas',
            'Personalización de marca',
            'Reportes personalizados',
            'Webhooks'
          ],
          limitations: [
            'Sin SSO empresarial',
            'Sin white label completo'
          ],
          cta: 'Prueba Gratuita',
          highlight: true
        }"
        @select="selectPlan"
      />
      
      <!-- Plan Premium -->
      <PricingCard
        :plan="{
          id: 'premium',
          name: 'Premium',
          description: 'Para organizaciones que necesitan funcionalidades premium',
          price: isAnnual ? 199 : 249,
          originalPrice: isAnnual ? 249 : null,
          period: isAnnual ? 'año' : 'mes',
          popular: false,
          features: [
            'Hasta 100 usuarios',
            '25 chatbots',
            '50,000 conversaciones/mes',
            'Soporte 24/7',
            'Analytics premium',
            'API completa',
            'Todas las integraciones',
            'White label parcial',
            'SSO básico',
            'Entrenamiento personalizado',
            'Manager dedicado',
            'SLA garantizado'
          ],
          limitations: [
            'Límites en personalización',
            'Sin infraestructura dedicada'
          ],
          cta: 'Contactar Ventas',
          highlight: false
        }"
        @select="selectPlan"
      />
      
      <!-- Plan Enterprise -->
      <PricingCard
        :plan="{
          id: 'enterprise',
          name: 'Enterprise',
          description: 'Solución completa para grandes organizaciones',
          price: isAnnual ? 399 : 499,
          originalPrice: isAnnual ? 499 : null,
          period: isAnnual ? 'año' : 'mes',
          popular: false,
          features: [
            'Usuarios ilimitados',
            'Chatbots ilimitados',
            'Conversaciones ilimitadas',
            'Soporte dedicado 24/7',
            'Analytics empresarial',
            'API empresarial',
            'Integraciones personalizadas',
            'White label completo',
            'SSO empresarial',
            'Infraestructura dedicada',
            'Cumplimiento GDPR/HIPAA',
            'Auditorías de seguridad',
            'Implementación asistida',
            'Entrenamiento on-site'
          ],
          limitations: [],
          cta: 'Contactar Ventas',
          highlight: false
        }"
        @select="selectPlan"
      />
    </div>
    
    <!-- Comparación de Características -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">Comparación Detallada de Planes</h3>
        <p class="text-sm text-gray-600 mt-1">Compara todas las características disponibles en cada plan</p>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-1/4">
                Características
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Básico
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Profesional
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Premium
              </th>
              <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Enterprise
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="feature in comparisonFeatures" :key="feature.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ feature.name }}
                <div v-if="feature.description" class="text-xs text-gray-500 mt-1">
                  {{ feature.description }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <component :is="getFeatureIcon(feature.basic)" :class="getFeatureClass(feature.basic)" />
                <div v-if="typeof feature.basic === 'string'" class="text-xs text-gray-600 mt-1">
                  {{ feature.basic }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <component :is="getFeatureIcon(feature.professional)" :class="getFeatureClass(feature.professional)" />
                <div v-if="typeof feature.professional === 'string'" class="text-xs text-gray-600 mt-1">
                  {{ feature.professional }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <component :is="getFeatureIcon(feature.premium)" :class="getFeatureClass(feature.premium)" />
                <div v-if="typeof feature.premium === 'string'" class="text-xs text-gray-600 mt-1">
                  {{ feature.premium }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <component :is="getFeatureIcon(feature.enterprise)" :class="getFeatureClass(feature.enterprise)" />
                <div v-if="typeof feature.enterprise === 'string'" class="text-xs text-gray-600 mt-1">
                  {{ feature.enterprise }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- FAQ Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-6">Preguntas Frecuentes</h3>
      
      <div class="space-y-4">
        <div v-for="faq in faqs" :key="faq.question" class="border-b border-gray-200 pb-4 last:border-b-0">
          <button
            @click="faq.open = !faq.open"
            class="flex items-center justify-between w-full text-left"
          >
            <span class="text-sm font-medium text-gray-900">{{ faq.question }}</span>
            <ChevronDownIcon 
              :class="[
                'w-5 h-5 text-gray-500 transition-transform duration-200',
                faq.open ? 'transform rotate-180' : ''
              ]" 
            />
          </button>
          <div v-if="faq.open" class="mt-3 text-sm text-gray-600">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- CTA Section -->
    <div class="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-8 text-center">
      <h3 class="text-2xl font-bold text-white mb-4">
        ¿Necesitas un plan personalizado?
      </h3>
      <p class="text-primary-100 mb-6 max-w-2xl mx-auto">
        Nuestro equipo de ventas puede ayudarte a encontrar la solución perfecta para tu organización, 
        incluyendo descuentos por volumen y características personalizadas.
      </p>
      <div class="flex items-center justify-center space-x-4">
        <button
          @click="contactSales"
          class="bg-white text-primary-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors"
        >
          Contactar Ventas
        </button>
        <button
          @click="scheduleDemo"
          class="border border-white text-white px-6 py-3 rounded-lg font-medium hover:bg-white hover:text-primary-600 transition-colors"
        >
          Agendar Demo
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import {
  CheckIcon,
  XMarkIcon,
  MinusIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline'

import PricingCard from '@/components/dashboard/PricingCard.vue'

// Router
const router = useRouter()

// State
const isAnnual = ref(false)

// Características de comparación
const comparisonFeatures = ref([
  {
    name: 'Usuarios',
    description: 'Número máximo de usuarios en la organización',
    basic: '5',
    professional: '25',
    premium: '100',
    enterprise: 'Ilimitados'
  },
  {
    name: 'Chatbots',
    description: 'Número de chatbots que puedes crear',
    basic: '3',
    professional: '10',
    premium: '25',
    enterprise: 'Ilimitados'
  },
  {
    name: 'Conversaciones/mes',
    description: 'Límite mensual de conversaciones',
    basic: '1,000',
    professional: '10,000',
    premium: '50,000',
    enterprise: 'Ilimitadas'
  },
  {
    name: 'Soporte',
    basic: 'Email',
    professional: 'Prioritario',
    premium: '24/7',
    enterprise: 'Dedicado 24/7'
  },
  {
    name: 'Analytics',
    basic: true,
    professional: true,
    premium: true,
    enterprise: true
  },
  {
    name: 'API Access',
    basic: false,
    professional: true,
    premium: true,
    enterprise: true
  },
  {
    name: 'SSO',
    basic: false,
    professional: false,
    premium: 'Básico',
    enterprise: 'Empresarial'
  },
  {
    name: 'White Label',
    basic: false,
    professional: 'Parcial',
    premium: 'Parcial',
    enterprise: 'Completo'
  },
  {
    name: 'Integraciones',
    basic: 'Básicas',
    professional: 'Avanzadas',
    premium: 'Todas',
    enterprise: 'Personalizadas'
  },
  {
    name: 'Webhooks',
    basic: false,
    professional: true,
    premium: true,
    enterprise: true
  },
  {
    name: 'Reportes Personalizados',
    basic: false,
    professional: true,
    premium: true,
    enterprise: true
  },
  {
    name: 'SLA',
    basic: false,
    professional: false,
    premium: '99.5%',
    enterprise: '99.9%'
  },
  {
    name: 'Cumplimiento',
    basic: false,
    professional: false,
    premium: false,
    enterprise: 'GDPR/HIPAA'
  },
  {
    name: 'Infraestructura',
    basic: 'Compartida',
    professional: 'Compartida',
    premium: 'Compartida',
    enterprise: 'Dedicada'
  }
])

// FAQs
const faqs = reactive([
  {
    question: '¿Puedo cambiar de plan en cualquier momento?',
    answer: 'Sí, puedes actualizar o degradar tu plan en cualquier momento. Los cambios se reflejarán en tu próxima facturación.',
    open: false
  },
  {
    question: '¿Hay período de prueba gratuito?',
    answer: 'Ofrecemos una prueba gratuita de 14 días para todos los planes de pago. No se requiere tarjeta de crédito.',
    open: false
  },
  {
    question: '¿Qué métodos de pago aceptan?',
    answer: 'Aceptamos todas las tarjetas de crédito principales, PayPal y transferencias bancarias para planes Enterprise.',
    open: false
  },
  {
    question: '¿Hay descuentos para organizaciones sin fines de lucro?',
    answer: 'Sí, ofrecemos descuentos especiales del 30% para organizaciones sin fines de lucro verificadas.',
    open: false
  },
  {
    question: '¿Qué incluye el soporte técnico?',
    answer: 'El soporte incluye asistencia técnica, resolución de problemas, guías de implementación y mejores prácticas.',
    open: false
  },
  {
    question: '¿Puedo cancelar mi suscripción en cualquier momento?',
    answer: 'Sí, puedes cancelar tu suscripción en cualquier momento. No hay penalizaciones por cancelación anticipada.',
    open: false
  }
])

// Methods
const getFeatureIcon = (value) => {
  if (typeof value === 'boolean') {
    return value ? CheckIcon : XMarkIcon
  } else if (typeof value === 'string') {
    return MinusIcon
  }
  return MinusIcon
}

const getFeatureClass = (value) => {
  if (typeof value === 'boolean') {
    return value 
      ? 'w-5 h-5 text-green-500' 
      : 'w-5 h-5 text-red-500'
  }
  return 'w-5 h-5 text-blue-500'
}

const selectPlan = (plan) => {
  console.log('Selected plan:', plan)
  
  if (plan.id === 'basic') {
    // Redirigir a registro gratuito
    router.push('/register?plan=basic')
  } else if (plan.id === 'professional') {
    // Iniciar prueba gratuita
    router.push('/register?plan=professional&trial=true')
  } else {
    // Contactar ventas para planes premium y enterprise
    contactSales()
  }
}

const contactSales = () => {
  // Implementar contacto con ventas
  console.log('Contacting sales...')
  // Podría abrir un modal, redirigir a un formulario, etc.
}

const scheduleDemo = () => {
  // Implementar agendamiento de demo
  console.log('Scheduling demo...')
  // Podría abrir Calendly, un modal de agendamiento, etc.
}
</script>

<style scoped>
.pricing-page {
  min-height: calc(100vh - 200px);
}

/* Animaciones para las transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Estilos para el toggle */
.toggle-enter-active,
.toggle-leave-active {
  transition: all 0.2s ease;
}

.toggle-enter-from,
.toggle-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>