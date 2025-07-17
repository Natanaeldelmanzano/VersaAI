import { createPinia } from 'pinia'
import { markRaw } from 'vue'
import router from '../router'

// Create pinia instance
const pinia = createPinia()

// Add router to pinia context
pinia.use(({ store }) => {
  store.router = markRaw(router)
})

// Plugin to persist certain stores to localStorage
const persistPlugin = ({ store }) => {
  // List of stores to persist
  const persistedStores = ['auth', 'app']
  
  if (persistedStores.includes(store.$id)) {
    // Load persisted state
    const persistedState = localStorage.getItem(`pinia-${store.$id}`)
    if (persistedState) {
      try {
        const parsed = JSON.parse(persistedState)
        store.$patch(parsed)
      } catch (error) {
        console.warn(`Failed to parse persisted state for ${store.$id}:`, error)
      }
    }
    
    // Subscribe to changes and persist
    store.$subscribe((mutation, state) => {
      // Only persist certain fields for each store
      let stateToPersist = {}
      
      if (store.$id === 'auth') {
        stateToPersist = {
          user: state.user,
          token: state.token,
          refreshToken: state.refreshToken,
          isAuthenticated: state.isAuthenticated,
          permissions: state.permissions
        }
      } else if (store.$id === 'app') {
        stateToPersist = {
          currentTheme: state.currentTheme,
          currentLanguage: state.currentLanguage,
          isSidebarOpen: state.isSidebarOpen
        }
      }
      
      localStorage.setItem(`pinia-${store.$id}`, JSON.stringify(stateToPersist))
    })
  }
}

// Add persistence plugin
pinia.use(persistPlugin)

// Plugin to add global error handling
const errorHandlingPlugin = ({ store }) => {
  // Wrap actions with error handling
  Object.keys(store).forEach(key => {
    if (typeof store[key] === 'function' && (key.startsWith('fetch') || key.startsWith('create') || key.startsWith('update') || key.startsWith('delete'))) {
      const originalAction = store[key]
      
      store[key] = async (...args) => {
        try {
          return await originalAction.apply(store, args)
        } catch (error) {
          // Log error for debugging
          console.error(`Error in ${store.$id}.${key}:`, error)
          
          // Handle specific error types without circular dependencies
          if (error.response?.status === 401) {
            // Unauthorized - let the API interceptor handle this
            console.warn('Unauthorized access detected in store action')
          } else if (error.response?.status === 403) {
            // Forbidden - let the API interceptor handle this
            console.warn('Forbidden access detected in store action')
          } else if (error.response?.status >= 500) {
            // Server error - let the API interceptor handle this
            console.warn('Server error detected in store action')
          }
          
          // Re-throw error for component handling
          throw error
        }
      }
    }
  })
}

// Add error handling plugin
pinia.use(errorHandlingPlugin)

// Plugin to add loading states
const loadingPlugin = ({ store }) => {
  // Add global loading state
  if (!store.isLoading) {
    store.isLoading = false
  }
  
  // Track async actions
  const asyncActions = Object.keys(store).filter(key => 
    typeof store[key] === 'function' && (
      key.startsWith('fetch') || 
      key.startsWith('create') || 
      key.startsWith('update') || 
      key.startsWith('delete') ||
      key.startsWith('send') ||
      key.startsWith('upload')
    )
  )
  
  asyncActions.forEach(actionName => {
    const originalAction = store[actionName]
    
    store[actionName] = async (...args) => {
      // Set loading state
      const loadingKey = `is${actionName.charAt(0).toUpperCase() + actionName.slice(1)}Loading`
      if (store[loadingKey] !== undefined) {
        store[loadingKey] = true
      } else {
        store.isLoading = true
      }
      
      try {
        const result = await originalAction.apply(store, args)
        return result
      } finally {
        // Clear loading state
        if (store[loadingKey] !== undefined) {
          store[loadingKey] = false
        } else {
          store.isLoading = false
        }
      }
    }
  })
}

// Add loading plugin
pinia.use(loadingPlugin)

// Export pinia instance
export default pinia

// Export store composables for easy importing
export { useAuthStore } from './auth'
export { useChatbotsStore } from './chatbots'
export { useConversationsStore } from './conversations'
export { useKnowledgeBasesStore } from './knowledgeBases'
export { useAnalyticsStore } from './analytics'
export { useUsersStore } from './users'
export { useSettingsStore } from './settings'
export { useAppStore } from './app'

// Helper function to reset all stores
export const resetAllStores = () => {
  const authStore = useAuthStore()
  const chatbotsStore = useChatbotsStore()
  const conversationsStore = useConversationsStore()
  const knowledgeBasesStore = useKnowledgeBasesStore()
  const analyticsStore = useAnalyticsStore()
  const usersStore = useUsersStore()
  const settingsStore = useSettingsStore()
  const appStore = useAppStore()
  
  // Reset each store
  authStore.$reset()
  chatbotsStore.$reset()
  conversationsStore.$reset()
  knowledgeBasesStore.$reset()
  analyticsStore.$reset()
  usersStore.$reset()
  settingsStore.$reset()
  appStore.resetAppState()
  
  // Clear localStorage
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith('pinia-')) {
      localStorage.removeItem(key)
    }
  })
}

// Helper function to initialize all stores
export const initializeStores = async () => {
  try {
    // Wait for pinia to be ready
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Import stores dynamically to avoid circular dependencies
    const { useAppStore } = await import('./app')
    const { useAuthStore } = await import('./auth')
    
    // Now we can safely use stores
    const appStore = useAppStore()
    const authStore = useAuthStore()
    
    // Initialize app first
    await appStore.initializeApp()
    
    // If user is authenticated, the user data is already loaded by checkAuth
    // No need to fetch user profile again
    
    return { success: true }
  } catch (error) {
    console.error('Failed to initialize stores:', error)
    return { success: false, error }
  }
}

// Helper function to check if stores are ready
export const areStoresReady = async () => {
  try {
    const { useAppStore } = await import('./app')
    const appStore = useAppStore()
    return !appStore.isLoading
  } catch (error) {
    console.error('Error checking if stores are ready:', error)
    return false
  }
}

// Helper function to get store by name
export const getStore = async (storeName) => {
  try {
    const storeModules = {
      auth: () => import('./auth').then(m => m.useAuthStore),
      chatbots: () => import('./chatbots').then(m => m.useChatbotsStore),
      conversations: () => import('./conversations').then(m => m.useConversationsStore),
      knowledgeBases: () => import('./knowledgeBases').then(m => m.useKnowledgeBasesStore),
      analytics: () => import('./analytics').then(m => m.useAnalyticsStore),
      users: () => import('./users').then(m => m.useUsersStore),
      settings: () => import('./settings').then(m => m.useSettingsStore),
      app: () => import('./app').then(m => m.useAppStore)
    }
    
    const storeComposable = await storeModules[storeName]?.()
    return storeComposable?.()
  } catch (error) {
    console.error(`Error getting store ${storeName}:`, error)
    return null
  }
}

// Helper function to subscribe to store changes
export const subscribeToStore = async (storeName, callback) => {
  try {
    const store = await getStore(storeName)
    if (store) {
      return store.$subscribe(callback)
    }
    return null
  } catch (error) {
    console.error(`Error subscribing to store ${storeName}:`, error)
    return null
  }
}

// Helper function to watch specific store state
export const watchStoreState = async (storeName, statePath, callback) => {
  try {
    const store = await getStore(storeName)
    if (store) {
      return store.$subscribe((mutation, state) => {
        const value = statePath.split('.').reduce((obj, key) => obj?.[key], state)
        callback(value, mutation)
      })
    }
    return null
  } catch (error) {
    console.error(`Error watching store state ${storeName}.${statePath}:`, error)
    return null
  }
}

// Development helpers
if (import.meta.env.DEV) {
  // Add stores to window for debugging (using dynamic imports to avoid circular dependencies)
  window.__PINIA_STORES__ = {
    auth: async () => (await import('./auth')).useAuthStore(),
    chatbots: async () => (await import('./chatbots')).useChatbotsStore(),
    conversations: async () => (await import('./conversations')).useConversationsStore(),
    knowledgeBases: async () => (await import('./knowledgeBases')).useKnowledgeBasesStore(),
    analytics: async () => (await import('./analytics')).useAnalyticsStore(),
    users: async () => (await import('./users')).useUsersStore(),
    settings: async () => (await import('./settings')).useSettingsStore(),
    app: async () => (await import('./app')).useAppStore()
  }
  
  // Add helper functions to window
  window.__PINIA_HELPERS__ = {
    resetAllStores,
    initializeStores,
    areStoresReady,
    getStore,
    subscribeToStore,
    watchStoreState
  }
  
  console.log('🍍 Pinia stores initialized with debugging helpers')
  console.log('Available stores:', Object.keys(window.__PINIA_STORES__))
  console.log('Helper functions:', Object.keys(window.__PINIA_HELPERS__))
}