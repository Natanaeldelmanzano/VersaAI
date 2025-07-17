<template>
  <component
    :is="tag"
    :to="to"
    :href="href"
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loading spinner -->
    <div v-if="loading" class="spinner w-4 h-4 mr-2"></div>
    
    <!-- Icon (left) -->
    <component 
      v-else-if="iconLeft" 
      :is="iconLeft" 
      class="w-4 h-4 mr-2" 
      aria-hidden="true" 
    />
    
    <!-- Content -->
    <span v-if="$slots.default">
      <slot />
    </span>
    <span v-else>{{ label }}</span>
    
    <!-- Icon (right) -->
    <component 
      v-if="iconRight && !loading" 
      :is="iconRight" 
      class="w-4 h-4 ml-2" 
      aria-hidden="true" 
    />
    
    <!-- Badge -->
    <span 
      v-if="badge && !loading"
      :class="badgeClasses"
    >
      {{ badge }}
    </span>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary', 'secondary', 'success', 'warning', 'error', 
      'ghost', 'outline', 'link', 'gradient'
    ].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  iconLeft: {
    type: [Object, Function],
    default: null
  },
  iconRight: {
    type: [Object, Function],
    default: null
  },
  badge: {
    type: [String, Number],
    default: null
  },
  to: {
    type: [String, Object],
    default: null
  },
  href: {
    type: String,
    default: null
  },
  type: {
    type: String,
    default: 'button'
  },
  animation: {
    type: String,
    default: 'default',
    validator: (value) => ['none', 'default', 'bounce', 'pulse', 'glow'].includes(value)
  }
})

const emit = defineEmits(['click'])

const tag = computed(() => {
  if (props.to) return 'router-link'
  if (props.href) return 'a'
  return 'button'
})

const buttonClasses = computed(() => {
  const classes = ['btn']
  
  // Base variant classes
  const variants = {
    primary: 'btn-primary bg-gradient-primary text-white',
    secondary: 'btn-secondary bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200',
    success: 'btn-success bg-gradient-success text-white',
    warning: 'btn-warning bg-gradient-warning text-white',
    error: 'btn-error bg-gradient-error text-white',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100',
    outline: 'bg-transparent border-2 border-primary-500 text-primary-500 hover:bg-primary-500 hover:text-white',
    link: 'bg-transparent text-primary-500 hover:text-primary-600 underline-offset-4 hover:underline p-0',
    gradient: 'bg-gradient-primary text-white shadow-glow'
  }
  
  classes.push(variants[props.variant])
  
  // Size classes
  const sizes = {
    xs: 'btn-sm px-2 py-1 text-xs',
    sm: 'btn-sm px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'btn-lg px-6 py-3 text-base',
    xl: 'btn-lg px-8 py-4 text-lg'
  }
  
  classes.push(sizes[props.size])
  
  // Rounded classes
  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    full: 'rounded-full'
  }
  
  classes.push(roundedClasses[props.rounded])
  
  // Full width
  if (props.fullWidth) {
    classes.push('w-full')
  }
  
  // Animation classes
  const animations = {
    default: 'transition-all duration-200 ease-in-out hover:transform hover:-translate-y-0.5',
    bounce: 'transition-all duration-200 ease-in-out hover:animate-bounce-soft',
    pulse: 'transition-all duration-200 ease-in-out hover:animate-pulse-fast',
    glow: 'transition-all duration-200 ease-in-out hover:animate-glow',
    none: ''
  }
  
  classes.push(animations[props.animation])
  
  // Disabled state
  if (props.disabled || props.loading) {
    classes.push('opacity-50 cursor-not-allowed transform-none')
  }
  
  // Loading state
  if (props.loading) {
    classes.push('cursor-wait')
  }
  
  return classes.join(' ')
})

const badgeClasses = computed(() => {
  const base = 'ml-2 inline-flex items-center justify-center px-2 py-0.5 rounded-full text-xs font-medium'
  
  const variantBadgeColors = {
    primary: 'bg-white text-primary-600',
    secondary: 'bg-primary-100 text-primary-600',
    success: 'bg-white text-success-600',
    warning: 'bg-white text-warning-600',
    error: 'bg-white text-error-600',
    ghost: 'bg-primary-100 text-primary-600',
    outline: 'bg-primary-100 text-primary-600',
    link: 'bg-primary-100 text-primary-600',
    gradient: 'bg-white text-primary-600'
  }
  
  return `${base} ${variantBadgeColors[props.variant]}`
})

const handleClick = (event) => {
  if (props.disabled || props.loading) {
    event.preventDefault()
    return
  }
  emit('click', event)
}
</script>

<style scoped>
.btn {
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.3s ease, height 0.3s ease;
}

.btn:active::before {
  width: 300px;
  height: 300px;
}

.btn-primary:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-success:hover {
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
}

.btn-warning:hover {
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.btn-error:hover {
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
}

.btn:disabled,
.btn[disabled] {
  transform: none !important;
  box-shadow: none !important;
}
</style>