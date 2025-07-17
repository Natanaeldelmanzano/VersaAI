import { ref, computed, watch } from 'vue'

// Estado global del modo oscuro
const isDark = ref(false)
const isInitialized = ref(false)

// Clave para localStorage
const STORAGE_KEY = 'versaai-dark-mode'

export function useDarkMode() {
  // Inicializar solo una vez
  if (!isInitialized.value) {
    initializeDarkMode()
    isInitialized.value = true
  }

  // Computed para el tema actual
  const theme = computed(() => isDark.value ? 'dark' : 'light')

  // Función para alternar modo oscuro
  const toggleDarkMode = () => {
    isDark.value = !isDark.value
  }

  // Función para establecer modo oscuro
  const setDarkMode = (value) => {
    isDark.value = value
  }

  // Función para detectar preferencia del sistema
  const getSystemPreference = () => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  // Función para aplicar el tema
  const applyTheme = (dark) => {
    const html = document.documentElement
    
    if (dark) {
      html.classList.add('dark')
      html.setAttribute('data-theme', 'dark')
    } else {
      html.classList.remove('dark')
      html.setAttribute('data-theme', 'light')
    }
  }

  // Función para guardar en localStorage
  const saveToStorage = (value) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        isDark: value,
        timestamp: Date.now()
      }))
    } catch (error) {
      console.warn('No se pudo guardar la preferencia de tema:', error)
    }
  }

  // Función para cargar desde localStorage
  const loadFromStorage = () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const parsed = JSON.parse(stored)
        return parsed.isDark
      }
    } catch (error) {
      console.warn('No se pudo cargar la preferencia de tema:', error)
    }
    return null
  }

  // Función de inicialización
  const initializeDarkMode = () => {
    // Intentar cargar desde localStorage
    const storedPreference = loadFromStorage()
    
    if (storedPreference !== null) {
      isDark.value = storedPreference
    } else {
      // Si no hay preferencia guardada, usar la del sistema
      isDark.value = getSystemPreference()
    }

    // Aplicar el tema inicial
    applyTheme(isDark.value)

    // Escuchar cambios en la preferencia del sistema
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleSystemChange = (e) => {
      // Solo cambiar si no hay preferencia guardada
      const stored = loadFromStorage()
      if (stored === null) {
        isDark.value = e.matches
      }
    }

    // Agregar listener para cambios del sistema
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleSystemChange)
    } else {
      // Fallback para navegadores más antiguos
      mediaQuery.addListener(handleSystemChange)
    }
  }

  // Watcher para aplicar cambios y guardar en localStorage
  watch(isDark, (newValue) => {
    applyTheme(newValue)
    saveToStorage(newValue)
  }, { immediate: false })

  return {
    isDark: computed(() => isDark.value),
    theme,
    toggleDarkMode,
    setDarkMode,
    getSystemPreference
  }
}

// Función para usar en componentes que necesiten solo lectura
export function useDarkModeState() {
  return {
    isDark: computed(() => isDark.value),
    theme: computed(() => isDark.value ? 'dark' : 'light')
  }
}