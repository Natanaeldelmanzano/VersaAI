import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Plugins
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import createAuthPlugin from './plugins/auth.js'

// Styles
import './style.css'
import './assets/styles/main.css'

// Icons
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faUser, 
  faLock, 
  faEye, 
  faEyeSlash, 
  faEnvelope,
  faHome,
  faChartBar,
  faRobot,
  faComments,
  faDatabase,
  faCog,
  faUsers,
  faSignOutAlt,
  faBars,
  faTimes,
  faPlus,
  faEdit,
  faTrash,
  faSearch,
  faFilter,
  faDownload,
  faUpload,
  faSave,
  faSpinner,
  faCheck,
  faExclamationTriangle,
  faInfoCircle,
  faBell,
  faUserCircle,
  faBuilding,
  faGlobe,
  faMobile,
  faDesktop,
  faCode,
  faChevronDown,
  faChevronUp,
  faChevronLeft,
  faChevronRight,
  faPaperPlane,
  faClipboard,
  faLink,
  faExternalLinkAlt
} from '@fortawesome/free-solid-svg-icons'

// Add icons to library
library.add(
  faUser, faLock, faEye, faEyeSlash, faEnvelope,
  faHome, faChartBar, faRobot, faComments, faDatabase,
  faCog, faUsers, faSignOutAlt, faBars, faTimes,
  faPlus, faEdit, faTrash, faSearch, faFilter,
  faDownload, faUpload, faSave, faSpinner, faCheck,
  faExclamationTriangle, faInfoCircle, faBell, faUserCircle,
  faBuilding, faGlobe, faMobile, faDesktop, faCode,
  faChevronDown, faChevronUp, faChevronLeft, faChevronRight,
  faPaperPlane, faClipboard, faLink, faExternalLinkAlt
)

// Toast configuration
const toastOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
}

console.log('🚀 Iniciando aplicación VersaAI...')

const app = createApp(App)
const pinia = createPinia()

console.log('📦 Configurando Pinia...')
app.use(pinia)

console.log('🛣️ Configurando Router...')
app.use(router)

console.log('🍞 Configurando Toast...')
app.use(Toast, toastOptions)

console.log('🔐 Configurando Auth Plugin...')
app.use(createAuthPlugin({ autoCheck: true, sessionMonitoring: true }))

console.log('🎨 Configurando FontAwesome...')
app.component('font-awesome-icon', FontAwesomeIcon)

// Global properties
app.config.globalProperties.$appName = 'VersaAI'
app.config.globalProperties.$version = '1.0.0'

// Error handling
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err)
  console.error('Component:', vm)
  console.error('Info:', info)
}

// Performance monitoring
if (import.meta.env.DEV) {
  app.config.performance = true
}

console.log('🎯 Montando aplicación...')
app.mount('#app')

console.log('✅ Aplicación VersaAI montada exitosamente')

// Service Worker registration (for production)
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered: ', registration)
      })
      .catch((registrationError) => {
        console.log('SW registration failed: ', registrationError)
      })
  })
}
