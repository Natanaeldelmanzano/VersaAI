<template>
  <transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="show"
      :class="[
        'max-w-sm w-full shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden',
        notificationClasses
      ]"
    >
      <div class="p-4">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <component
              :is="iconComponent"
              :class="[
                'h-6 w-6',
                iconClasses
              ]"
              aria-hidden="true"
            />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p :class="titleClasses">{{ title }}</p>
            <p v-if="message" :class="messageClasses">{{ message }}</p>
            <div v-if="actions && actions.length > 0" class="mt-3 flex space-x-3">
              <EnhancedButton
                v-for="action in actions"
                :key="action.label"
                :variant="action.variant || 'ghost'"
                size="sm"
                @click="handleAction(action)"
              >
                {{ action.label }}
              </EnhancedButton>
            </div>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="close"
              :class="[
                'rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2',
                closeButtonClasses
              ]"
            >
              <span class="sr-only">Cerrar</span>
              <XMarkIcon class="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Progress bar for auto-dismiss -->
      <div
        v-if="autoClose && duration > 0"
        class="h-1 bg-gray-200"
      >
        <div
          :class="[
            'h-full transition-all ease-linear',
            progressBarClasses
          ]"
          :style="{ width: progressWidth + '%' }"
        ></div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import EnhancedButton from './EnhancedButton.vue'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    default: ''
  },
  actions: {
    type: Array,
    default: () => []
  },
  autoClose: {
    type: Boolean,
    default: true
  },
  duration: {
    type: Number,
    default: 5000
  },
  persistent: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'action'])

const show = ref(true)
const progressWidth = ref(100)
let timer = null
let progressTimer = null

const iconComponent = computed(() => {
  const icons = {
    success: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon,
    info: InformationCircleIcon
  }
  return icons[props.type]
})

const notificationClasses = computed(() => {
  const classes = {
    success: 'bg-white border-l-4 border-success-400',
    warning: 'bg-white border-l-4 border-warning-400',
    error: 'bg-white border-l-4 border-error-400',
    info: 'bg-white border-l-4 border-primary-400'
  }
  return classes[props.type]
})

const iconClasses = computed(() => {
  const classes = {
    success: 'text-success-400',
    warning: 'text-warning-400',
    error: 'text-error-400',
    info: 'text-primary-400'
  }
  return classes[props.type]
})

const titleClasses = computed(() => {
  return 'text-sm font-medium text-gray-900'
})

const messageClasses = computed(() => {
  return 'mt-1 text-sm text-gray-500'
})

const closeButtonClasses = computed(() => {
  const classes = {
    success: 'focus:ring-success-500',
    warning: 'focus:ring-warning-500',
    error: 'focus:ring-error-500',
    info: 'focus:ring-primary-500'
  }
  return classes[props.type]
})

const progressBarClasses = computed(() => {
  const classes = {
    success: 'bg-success-400',
    warning: 'bg-warning-400',
    error: 'bg-error-400',
    info: 'bg-primary-400'
  }
  return classes[props.type]
})

const close = () => {
  show.value = false
  clearTimers()
  setTimeout(() => {
    emit('close')
  }, 300) // Wait for transition to complete
}

const handleAction = (action) => {
  emit('action', action)
  if (action.closeOnClick !== false) {
    close()
  }
}

const clearTimers = () => {
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const startAutoClose = () => {
  if (!props.autoClose || props.persistent || props.duration <= 0) return

  timer = setTimeout(() => {
    close()
  }, props.duration)

  // Update progress bar
  const interval = 50 // Update every 50ms
  const steps = props.duration / interval
  const decrement = 100 / steps
  
  progressTimer = setInterval(() => {
    progressWidth.value -= decrement
    if (progressWidth.value <= 0) {
      clearInterval(progressTimer)
      progressTimer = null
    }
  }, interval)
}

const pauseAutoClose = () => {
  clearTimers()
}

const resumeAutoClose = () => {
  if (!props.autoClose || props.persistent) return
  
  const remainingTime = (progressWidth.value / 100) * props.duration
  if (remainingTime > 0) {
    timer = setTimeout(() => {
      close()
    }, remainingTime)
    
    const interval = 50
    const steps = remainingTime / interval
    const decrement = progressWidth.value / steps
    
    progressTimer = setInterval(() => {
      progressWidth.value -= decrement
      if (progressWidth.value <= 0) {
        clearInterval(progressTimer)
        progressTimer = null
      }
    }, interval)
  }
}

onMounted(() => {
  startAutoClose()
})

onUnmounted(() => {
  clearTimers()
})

// Expose methods for parent components
defineExpose({
  close,
  pauseAutoClose,
  resumeAutoClose
})
</script>

<style scoped>
/* Additional custom styles if needed */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>