<template>
  <div 
    :class="[
      'card',
      {
        'stat-card': variant === 'stat',
        'glass': variant === 'glass',
        'glass-dark': variant === 'glass-dark',
        'shadow-soft': shadow === 'soft',
        'shadow-strong': shadow === 'strong',
        'shadow-glow': shadow === 'glow'
      },
      sizeClasses,
      colorClasses
    ]"
    :style="customStyles"
  >
    <!-- Header -->
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <div class="flex items-center justify-between">
          <h3 :class="titleClasses">{{ title }}</h3>
          <div v-if="$slots.actions" class="flex items-center space-x-2">
            <slot name="actions" />
          </div>
        </div>
        <p v-if="subtitle" :class="subtitleClasses">{{ subtitle }}</p>
      </slot>
    </div>

    <!-- Body -->
    <div class="card-body">
      <slot />
    </div>

    <!-- Footer -->
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>

    <!-- Loading overlay -->
    <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'stat', 'glass', 'glass-dark'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'white',
    validator: (value) => ['white', 'primary', 'secondary', 'success', 'warning', 'error'].includes(value)
  },
  shadow: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'soft', 'strong', 'glow', 'none'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: true
  },
  animated: {
    type: Boolean,
    default: true
  }
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl'
  }
  return sizes[props.size]
})

const colorClasses = computed(() => {
  if (props.color === 'white') return ''
  
  const colors = {
    primary: 'bg-primary-50 border-primary-200',
    secondary: 'bg-secondary-50 border-secondary-200',
    success: 'bg-success-50 border-success-200',
    warning: 'bg-warning-50 border-warning-200',
    error: 'bg-error-50 border-error-200'
  }
  return colors[props.color] || ''
})

const titleClasses = computed(() => {
  const base = 'font-semibold text-gray-900'
  const sizes = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-xl',
    xl: 'text-2xl'
  }
  return `${base} ${sizes[props.size]}`
})

const subtitleClasses = computed(() => {
  const base = 'text-gray-600 mt-1'
  const sizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  }
  return `${base} ${sizes[props.size]}`
})

const customStyles = computed(() => {
  const styles = {}
  
  if (props.animated) {
    styles.transition = 'all 0.2s ease-in-out'
  }
  
  return styles
})
</script>

<style scoped>
.card {
  position: relative;
}

.card:hover {
  @apply transform -translate-y-1;
}

.card.shadow-none {
  box-shadow: none;
}

.card.shadow-glow:hover {
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}
</style>