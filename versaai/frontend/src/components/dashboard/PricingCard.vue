<template>
  <div 
    :class="[
      'pricing-card relative bg-white rounded-xl shadow-sm border transition-all duration-200 hover:shadow-lg',
      plan.highlight ? 'border-primary-500 ring-2 ring-primary-500 ring-opacity-50' : 'border-gray-200',
      plan.popular ? 'transform scale-105' : ''
    ]"
  >
    <!-- Badge Popular -->
    <div v-if="plan.popular" class="absolute -top-3 left-1/2 transform -translate-x-1/2">
      <span class="inline-flex items-center px-4 py-1 rounded-full text-xs font-medium bg-primary-600 text-white">
        Más Popular
      </span>
    </div>
    
    <!-- Header -->
    <div class="p-6 text-center">
      <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ plan.name }}</h3>
      <p class="text-sm text-gray-600 mb-6">{{ plan.description }}</p>
      
      <!-- Precio -->
      <div class="mb-6">
        <div class="flex items-center justify-center space-x-2">
          <span v-if="plan.originalPrice" class="text-lg text-gray-400 line-through">
            ${{ plan.originalPrice }}
          </span>
          <span class="text-4xl font-bold text-gray-900">
            ${{ plan.price }}
          </span>
        </div>
        <div class="text-sm text-gray-600 mt-1">
          por {{ plan.period }}
        </div>
        
        <!-- Ahorro anual -->
        <div v-if="plan.originalPrice" class="mt-2">
          <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Ahorra ${{ (plan.originalPrice - plan.price) * 12 }}/año
          </span>
        </div>
      </div>
      
      <!-- CTA Button -->
      <button
        @click="$emit('select', plan)"
        :class="[
          'w-full py-3 px-4 rounded-lg font-medium transition-colors duration-200',
          plan.highlight 
            ? 'bg-primary-600 text-white hover:bg-primary-700' 
            : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
        ]"
      >
        {{ plan.cta }}
      </button>
    </div>
    
    <!-- Features -->
    <div class="px-6 pb-6">
      <div class="border-t border-gray-200 pt-6">
        <h4 class="text-sm font-medium text-gray-900 mb-4">Incluye:</h4>
        
        <ul class="space-y-3">
          <li v-for="feature in plan.features" :key="feature" class="flex items-start">
            <CheckIcon class="w-4 h-4 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
            <span class="text-sm text-gray-600">{{ feature }}</span>
          </li>
        </ul>
        
        <!-- Limitaciones -->
        <div v-if="plan.limitations && plan.limitations.length > 0" class="mt-6">
          <h4 class="text-sm font-medium text-gray-900 mb-4">Limitaciones:</h4>
          <ul class="space-y-3">
            <li v-for="limitation in plan.limitations" :key="limitation" class="flex items-start">
              <XMarkIcon class="w-4 h-4 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
              <span class="text-sm text-gray-500">{{ limitation }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- Footer con información adicional -->
    <div v-if="showDetails" class="px-6 pb-6">
      <div class="border-t border-gray-200 pt-4">
        <div class="space-y-2 text-xs text-gray-500">
          <div class="flex items-center justify-between">
            <span>Configuración incluida</span>
            <CheckIcon class="w-3 h-3 text-green-500" />
          </div>
          <div class="flex items-center justify-between">
            <span>Migración de datos</span>
            <CheckIcon v-if="plan.id !== 'basic'" class="w-3 h-3 text-green-500" />
            <XMarkIcon v-else class="w-3 h-3 text-red-500" />
          </div>
          <div class="flex items-center justify-between">
            <span>Entrenamiento del equipo</span>
            <CheckIcon v-if="['premium', 'enterprise'].includes(plan.id)" class="w-3 h-3 text-green-500" />
            <XMarkIcon v-else class="w-3 h-3 text-red-500" />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Overlay de carga -->
    <div v-if="isLoading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  CheckIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  plan: {
    type: Object,
    required: true
  },
  showDetails: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['select'])

// Computed
const planBenefits = computed(() => {
  const benefits = {
    basic: [
      'Ideal para equipos pequeños',
      'Funcionalidades esenciales',
      'Soporte por email'
    ],
    professional: [
      'Perfecto para equipos en crecimiento',
      'Funcionalidades avanzadas',
      'Soporte prioritario'
    ],
    premium: [
      'Para organizaciones establecidas',
      'Funcionalidades premium',
      'Soporte 24/7'
    ],
    enterprise: [
      'Solución empresarial completa',
      'Funcionalidades ilimitadas',
      'Soporte dedicado'
    ]
  }
  
  return benefits[props.plan.id] || []
})

const planColor = computed(() => {
  const colors = {
    basic: 'gray',
    professional: 'blue',
    premium: 'purple',
    enterprise: 'indigo'
  }
  
  return colors[props.plan.id] || 'gray'
})

const savingsPercentage = computed(() => {
  if (!props.plan.originalPrice) return 0
  
  return Math.round(((props.plan.originalPrice - props.plan.price) / props.plan.originalPrice) * 100)
})
</script>

<style scoped>
.pricing-card {
  transition: all 0.3s ease;
}

.pricing-card:hover {
  transform: translateY(-4px);
}

/* Animación para el badge popular */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.pricing-card .badge-popular {
  animation: pulse 2s infinite;
}

/* Estilos para características destacadas */
.feature-highlight {
  background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 0.375rem;
  padding: 0.5rem;
  margin: 0.25rem 0;
}

/* Efectos hover para botones */
.cta-button {
  position: relative;
  overflow: hidden;
}

.cta-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.cta-button:hover::before {
  left: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .pricing-card {
    margin-bottom: 1rem;
  }
  
  .pricing-card.transform.scale-105 {
    transform: none;
  }
}
</style>