<template>
  <div 
    :class="containerClasses"
    :style="containerStyle"
    role="status"
    :aria-label="ariaLabel"
  >
    <!-- Spinner SVG -->
    <svg
      :class="spinnerClasses"
      :width="size"
      :height="size"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        class="animate-spin origin-center"
        :style="{
          animationDuration: `${duration}ms`,
          transformOrigin: '50% 50%'
        }"
      />
    </svg>

    <!-- Texto de carga (opcional) -->
    <div v-if="text" :class="textClasses">
      {{ text }}
    </div>

    <!-- Slot para contenido personalizado -->
    <slot></slot>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'LoadingSpinner',
  props: {
    // Tamaño del spinner
    size: {
      type: [String, Number],
      default: 24,
      validator: (value) => {
        const num = typeof value === 'string' ? parseInt(value) : value
        return num > 0 && num <= 200
      }
    },
    // Color del spinner
    color: {
      type: String,
      default: 'primary',
      validator: (value) => {
        return ['primary', 'secondary', 'white', 'gray', 'success', 'warning', 'error'].includes(value)
      }
    },
    // Grosor del trazo
    strokeWidth: {
      type: [String, Number],
      default: 2
    },
    // Duración de la animación en ms
    duration: {
      type: Number,
      default: 1000
    },
    // Texto de carga
    text: {
      type: String,
      default: ''
    },
    // Centrar el spinner
    centered: {
      type: Boolean,
      default: false
    },
    // Overlay completo
    overlay: {
      type: Boolean,
      default: false
    },
    // Tamaño del texto
    textSize: {
      type: String,
      default: 'sm',
      validator: (value) => ['xs', 'sm', 'base', 'lg', 'xl'].includes(value)
    }
  },
  setup(props) {
    // Calcular circunferencia para la animación
    const circumference = computed(() => 2 * Math.PI * 10)
    const dashOffset = computed(() => circumference.value * 0.25)

    // Clases del contenedor
    const containerClasses = computed(() => {
      const classes = ['loading-spinner']
      
      if (props.centered) {
        classes.push('flex', 'items-center', 'justify-center')
      }
      
      if (props.overlay) {
        classes.push(
          'fixed', 'inset-0', 'z-50', 
          'bg-white/80', 'dark:bg-gray-900/80',
          'backdrop-blur-sm',
          'flex', 'items-center', 'justify-center'
        )
      }
      
      if (props.text) {
        classes.push('flex', 'flex-col', 'items-center', 'gap-3')
      }
      
      return classes
    })

    // Estilo del contenedor
    const containerStyle = computed(() => {
      if (props.centered && !props.overlay) {
        return {
          minHeight: `${props.size * 2}px`
        }
      }
      return {}
    })

    // Clases del spinner
    const spinnerClasses = computed(() => {
      const colorMap = {
        primary: 'text-blue-600 dark:text-blue-400',
        secondary: 'text-purple-600 dark:text-purple-400',
        white: 'text-white',
        gray: 'text-gray-600 dark:text-gray-400',
        success: 'text-green-600 dark:text-green-400',
        warning: 'text-yellow-600 dark:text-yellow-400',
        error: 'text-red-600 dark:text-red-400'
      }
      
      return [
        'animate-spin',
        colorMap[props.color] || colorMap.primary
      ]
    })

    // Clases del texto
    const textClasses = computed(() => {
      const sizeMap = {
        xs: 'text-xs',
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl'
      }
      
      const colorMap = {
        primary: 'text-blue-600 dark:text-blue-400',
        secondary: 'text-purple-600 dark:text-purple-400',
        white: 'text-white',
        gray: 'text-gray-600 dark:text-gray-400',
        success: 'text-green-600 dark:text-green-400',
        warning: 'text-yellow-600 dark:text-yellow-400',
        error: 'text-red-600 dark:text-red-400'
      }
      
      return [
        'font-medium',
        sizeMap[props.textSize] || sizeMap.sm,
        colorMap[props.color] || 'text-gray-600 dark:text-gray-400'
      ]
    })

    // Aria label para accesibilidad
    const ariaLabel = computed(() => {
      return props.text || 'Cargando...'
    })

    return {
      circumference,
      dashOffset,
      containerClasses,
      containerStyle,
      spinnerClasses,
      textClasses,
      ariaLabel
    }
  }
}
</script>

<style scoped>
/* Animación personalizada para el spinner */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Estilos para el overlay */
.loading-spinner {
  transition: all 0.2s ease-in-out;
}

/* Mejoras de accesibilidad */
@media (prefers-reduced-motion: reduce) {
  .animate-spin {
    animation: none;
  }
}
</style>