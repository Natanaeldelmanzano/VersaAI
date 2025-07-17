<template>
  <teleport to="body">
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="modelValue"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click="handleBackdropClick"
      >
        <!-- Backdrop -->
        <div 
          class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
          :class="backdropClasses"
        ></div>
        
        <!-- Modal container -->
        <div class="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
          <transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div
              v-if="modelValue"
              :class="[
                'relative transform overflow-hidden text-left shadow-xl transition-all',
                modalClasses
              ]"
              @click.stop
            >
              <!-- Close button -->
              <button
                v-if="showCloseButton"
                @click="close"
                class="absolute top-4 right-4 z-10 rounded-full p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <XMarkIcon class="h-5 w-5" aria-hidden="true" />
              </button>
              
              <!-- Header -->
              <div v-if="$slots.header || title" :class="headerClasses">
                <slot name="header">
                  <div class="flex items-center justify-between">
                    <h3 :class="titleClasses">{{ title }}</h3>
                    <p v-if="subtitle" :class="subtitleClasses">{{ subtitle }}</p>
                  </div>
                </slot>
              </div>
              
              <!-- Body -->
              <div :class="bodyClasses">
                <slot />
              </div>
              
              <!-- Footer -->
              <div v-if="$slots.footer || showDefaultFooter" :class="footerClasses">
                <slot name="footer">
                  <div class="flex justify-end space-x-3">
                    <EnhancedButton
                      v-if="showCancelButton"
                      variant="ghost"
                      @click="cancel"
                    >
                      {{ cancelText }}
                    </EnhancedButton>
                    <EnhancedButton
                      v-if="showConfirmButton"
                      :variant="confirmVariant"
                      :loading="loading"
                      @click="confirm"
                    >
                      {{ confirmText }}
                    </EnhancedButton>
                  </div>
                </slot>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { computed, watch, onUnmounted } from 'vue'
import EnhancedButton from './EnhancedButton.vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', '2xl', 'full'].includes(value)
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'glass', 'minimal'].includes(value)
  },
  persistent: {
    type: Boolean,
    default: false
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  showDefaultFooter: {
    type: Boolean,
    default: false
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  showConfirmButton: {
    type: Boolean,
    default: true
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  confirmVariant: {
    type: String,
    default: 'primary'
  },
  loading: {
    type: Boolean,
    default: false
  },
  centered: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close', 'cancel', 'confirm'])

const modalClasses = computed(() => {
  const sizeClasses = {
    xs: 'sm:max-w-xs sm:w-full',
    sm: 'sm:max-w-sm sm:w-full',
    md: 'sm:max-w-md sm:w-full',
    lg: 'sm:max-w-lg sm:w-full',
    xl: 'sm:max-w-xl sm:w-full',
    '2xl': 'sm:max-w-2xl sm:w-full',
    full: 'sm:max-w-full sm:w-full sm:h-full'
  }
  
  const variantClasses = {
    default: 'bg-white rounded-xl shadow-2xl',
    glass: 'glass rounded-xl shadow-2xl border border-white/20',
    minimal: 'bg-white rounded-lg shadow-lg'
  }
  
  return `${sizeClasses[props.size]} ${variantClasses[props.variant]}`
})

const backdropClasses = computed(() => {
  if (props.variant === 'glass') {
    return 'backdrop-blur-md'
  }
  return 'backdrop-blur-sm'
})

const headerClasses = computed(() => {
  const base = 'px-6 py-4'
  if (props.variant === 'minimal') {
    return `${base} border-b border-gray-200`
  }
  return `${base} border-b border-gray-100`
})

const bodyClasses = computed(() => {
  return 'px-6 py-4'
})

const footerClasses = computed(() => {
  const base = 'px-6 py-4'
  if (props.variant === 'minimal') {
    return `${base} border-t border-gray-200 bg-gray-50`
  }
  return `${base} border-t border-gray-100 bg-gray-50/50`
})

const titleClasses = computed(() => {
  return 'text-lg font-semibold text-gray-900'
})

const subtitleClasses = computed(() => {
  return 'text-sm text-gray-600 mt-1'
})

const close = () => {
  emit('update:modelValue', false)
  emit('close')
}

const cancel = () => {
  emit('cancel')
  if (!props.persistent) {
    close()
  }
}

const confirm = () => {
  emit('confirm')
}

const handleBackdropClick = () => {
  if (!props.persistent) {
    close()
  }
}

// Handle escape key
const handleEscape = (event) => {
  if (event.key === 'Escape' && props.modelValue && !props.persistent) {
    close()
  }
}

// Add/remove event listeners
const addEventListeners = () => {
  document.addEventListener('keydown', handleEscape)
  document.body.style.overflow = 'hidden'
}

const removeEventListeners = () => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
}

// Watch for modal open/close
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    addEventListeners()
  } else {
    removeEventListeners()
  }
})

// Cleanup on unmount
onUnmounted(() => {
  removeEventListeners()
})
</script>

<style scoped>
/* Custom scrollbar for modal content */
.modal-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.7);
}
</style>