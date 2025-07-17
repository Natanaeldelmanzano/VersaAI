import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const isLoading = ref(false)
  const isSidebarOpen = ref(true)
  const isMobileMenuOpen = ref(false)
  const currentTheme = ref('light')
  const currentLanguage = ref('es')
  const isOnline = ref(true)
  
  const pageTitle = ref('VersaAI')
  const pageDescription = ref('Plataforma de chatbots con IA')
  
  const appInfo = ref({
    name: 'VersaAI',
    version: '1.0.0',
    description: 'Plataforma de chatbots con IA',
    author: 'VersaAI Team',
    license: 'MIT'
  })

  // Getters
  const isDarkMode = computed(() => currentTheme.value === 'dark')

  // Actions
  const setLoading = (loading) => {
    isLoading.value = loading
  }
  
  const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
  }
  
  const setSidebarOpen = (open) => {
    isSidebarOpen.value = open
  }
  
  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  }
  
  const setMobileMenuOpen = (open) => {
    isMobileMenuOpen.value = open
  }
  
  const setTheme = (theme) => {
    currentTheme.value = theme
    localStorage.setItem('theme', theme)
    
    // Apply theme to document
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }
  
  const toggleTheme = () => {
    const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }
  
  const setLanguage = (language) => {
    currentLanguage.value = language
    localStorage.setItem('language', language)
  }
  
  const setPageInfo = (title, description = '') => {
    pageTitle.value = title
    pageDescription.value = description
    document.title = `${title} - ${appInfo.value.name}`
  }
  
  const setOnlineStatus = (online) => {
    isOnline.value = online
  }
  
  // FUNCIÓN FALTANTE - Agregar para compatibilidad
  const setAppVisibility = (visible) => {
    console.log('🔧 App visibility set to:', visible)
    // Implementar lógica de visibilidad si es necesaria
    if (visible !== undefined) {
      // Aquí se puede agregar lógica específica de visibilidad
      console.log('App visibility updated')
    }
  }
  
  // Alias para compatibilidad con código existente
  const setAppVis = setAppVisibility
  
  // Initialize theme from localStorage
  const initializeTheme = () => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    setTheme(savedTheme)
  }
  
  // Initialize language from localStorage
  const initializeLanguage = () => {
    const savedLanguage = localStorage.getItem('language') || 'es'
    setLanguage(savedLanguage)
  }
  
  // Initialize app
  const initialize = () => {
    console.log('🔧 Initializing app store...')
    initializeTheme()
    initializeLanguage()
    setOnlineStatus(navigator.onLine)
    console.log('✅ App store initialized!')
  }

  return {
    // State
    isLoading,
    isSidebarOpen,
    isMobileMenuOpen,
    currentTheme,
    currentLanguage,
    isOnline,
    pageTitle,
    pageDescription,
    appInfo,
    
    // Getters
    isDarkMode,
    
    // Actions
    setLoading,
    toggleSidebar,
    setSidebarOpen,
    toggleMobileMenu,
    setMobileMenuOpen,
    setTheme,
    toggleTheme,
    setLanguage,
    setPageInfo,
    setOnlineStatus,
    setAppVisibility,
    setAppVis, // Alias para compatibilidad
    initialize
  }
})