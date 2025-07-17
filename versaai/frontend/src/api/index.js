import axios from 'axios'
import router from '../router'
import { useToast } from 'vue-toastification'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Use lazy loading to avoid circular dependencies
    try {
      const { useAuthStore } = require('../stores/auth')
      const { useAppStore } = require('../stores/app')
      const authStore = useAuthStore()
      const appStore = useAppStore()
      
      // Add auth token if available
      if (authStore.token) {
        config.headers.Authorization = `Bearer ${authStore.token}`
      }
      
      // Add language header
      if (appStore.currentLanguage) {
        config.headers['Accept-Language'] = appStore.currentLanguage
      }
    } catch (error) {
      console.warn('Stores not available during request interceptor:', error)
    }
    
    // Add request timestamp for debugging
    config.metadata = { startTime: new Date() }
    
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, {
        params: config.params,
        data: config.data
      })
    }
    
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Calculate request duration
    if (response.config.metadata?.startTime) {
      const duration = new Date() - response.config.metadata.startTime
      response.duration = duration
      
      if (import.meta.env.DEV) {
        console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url} (${duration}ms)`, {
          status: response.status,
          data: response.data
        })
      }
    }
    
    // Update last activity timestamp (using lazy loading)
    try {
      const { useAuthStore } = require('../stores/auth')
      const authStore = useAuthStore()
      if (authStore.isAuthenticated && authStore.updateLastActivity) {
        authStore.updateLastActivity()
      }
    } catch (error) {
      // Ignore if stores are not available
    }
    
    return response
  },
  async (error) => {
    // Use lazy loading to avoid circular dependencies
    let authStore, appStore, toast
    try {
      const { useAuthStore } = require('../stores/auth')
      const { useAppStore } = require('../stores/app')
      authStore = useAuthStore()
      appStore = useAppStore()
      toast = useToast()
    } catch (storeError) {
      console.warn('Stores not available during error handling:', storeError)
      return Promise.reject(error)
    }
    
    const originalRequest = error.config
    
    // Calculate request duration for failed requests
    if (originalRequest?.metadata?.startTime) {
      const duration = new Date() - originalRequest.metadata.startTime
      error.duration = duration
      
      if (import.meta.env.DEV) {
        console.error(`❌ ${originalRequest.method?.toUpperCase()} ${originalRequest.url} (${duration}ms)`, {
          status: error.response?.status,
          error: error.response?.data
        })
      }
    }
    
    // Handle different error status codes
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Unauthorized - try to refresh token
          if (!originalRequest._retry && authStore.refreshToken) {
            originalRequest._retry = true
            
            try {
              await authStore.refreshToken()
              // Retry original request with new token
              originalRequest.headers.Authorization = `Bearer ${authStore.token}`
              return api(originalRequest)
            } catch (refreshError) {
              // Refresh failed, logout user
              authStore.logout()
              router.push('/auth/login')
              toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
              return Promise.reject(refreshError)
            }
          } else {
            // No refresh token or retry failed
            authStore.logout()
            router.push('/auth/login')
            toast.error('Acceso no autorizado')
          }
          break
          
        case 403:
          // Forbidden
          router.push('/errors/unauthorized')
          toast.error('No tienes permisos para realizar esta acción')
          break
          
        case 404:
          // Not found
          if (!originalRequest.url.includes('/api/v1/')) {
            router.push('/errors/not-found')
          }
          break
          
        case 422:
          // Validation error
          if (data?.detail) {
            if (Array.isArray(data.detail)) {
              // Multiple validation errors
              data.detail.forEach(err => {
                toast.error(`${err.loc?.join(' → ') || 'Error'}: ${err.msg}`)
              })
            } else {
              toast.error(data.detail)
            }
          }
          break
          
        case 429:
          // Rate limit exceeded
          toast.error('Demasiadas solicitudes. Por favor, espera un momento.')
          break
          
        case 500:
        case 502:
        case 503:
        case 504:
          // Server errors
          if (!originalRequest._serverErrorShown) {
            originalRequest._serverErrorShown = true
            router.push('/errors/server-error')
            toast.error('Error del servidor. Por favor, intenta más tarde.')
          }
          break
          
        default:
          // Other errors
          const message = data?.detail || data?.message || 'Error desconocido'
          toast.error(message)
      }
    } else if (error.request) {
      // Network error
      if (error.code === 'ECONNABORTED') {
        toast.error('La solicitud tardó demasiado tiempo. Por favor, intenta nuevamente.')
      } else {
        toast.error('Error de conexión. Verifica tu conexión a internet.')
      }
    } else {
      // Other errors
      toast.error('Error inesperado. Por favor, intenta nuevamente.')
    }
    
    return Promise.reject(error)
  }
)

// API helper functions
export const apiHelpers = {
  // Generic CRUD operations
  async get(url, params = {}, config = {}) {
    try {
      const response = await api.get(url, { params, ...config })
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  async post(url, data = {}, config = {}) {
    try {
      const response = await api.post(url, data, config)
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  async put(url, data = {}, config = {}) {
    try {
      const response = await api.put(url, data, config)
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  async patch(url, data = {}, config = {}) {
    try {
      const response = await api.patch(url, data, config)
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  async delete(url, config = {}) {
    try {
      const response = await api.delete(url, config)
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  // File upload helper
  async upload(url, file, onProgress = null, config = {}) {
    const formData = new FormData()
    
    if (file instanceof File) {
      formData.append('file', file)
    } else if (Array.isArray(file)) {
      file.forEach((f, index) => {
        formData.append(`files[${index}]`, f)
      })
    } else {
      // Assume it's an object with key-value pairs
      Object.keys(file).forEach(key => {
        formData.append(key, file[key])
      })
    }
    
    const uploadConfig = {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    }
    
    if (onProgress) {
      uploadConfig.onUploadProgress = (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        onProgress(percentCompleted)
      }
    }
    
    try {
      const response = await api.post(url, formData, uploadConfig)
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  // Download helper
  async download(url, filename = null, config = {}) {
    try {
      const response = await api.get(url, {
        responseType: 'blob',
        ...config
      })
      
      // Create download link
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      
      // Try to get filename from response headers
      const contentDisposition = response.headers['content-disposition']
      if (contentDisposition && !filename) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      link.setAttribute('download', filename || 'download')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(downloadUrl)
      
      return { success: true, data: response.data, response }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  },
  
  // Batch requests helper
  async batch(requests) {
    try {
      const responses = await Promise.allSettled(
        requests.map(req => {
          const { method, url, data, config } = req
          return api[method](url, data, config)
        })
      )
      
      const results = responses.map((response, index) => ({
        index,
        success: response.status === 'fulfilled',
        data: response.status === 'fulfilled' ? response.value.data : null,
        error: response.status === 'rejected' ? response.reason : null
      }))
      
      return { success: true, results }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },
  
  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health')
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }
}

// Request/Response logging for development
if (import.meta.env.DEV) {
  // Add request/response logging
  let requestCount = 0
  
  api.interceptors.request.use((config) => {
    config.requestId = ++requestCount
    console.group(`📡 Request #${config.requestId}`)
    console.log('URL:', config.url)
    console.log('Method:', config.method?.toUpperCase())
    console.log('Headers:', config.headers)
    if (config.params) console.log('Params:', config.params)
    if (config.data) console.log('Data:', config.data)
    console.groupEnd()
    return config
  })
  
  api.interceptors.response.use(
    (response) => {
      console.group(`✅ Response #${response.config.requestId}`)
      console.log('Status:', response.status)
      console.log('Headers:', response.headers)
      console.log('Data:', response.data)
      if (response.duration) console.log('Duration:', `${response.duration}ms`)
      console.groupEnd()
      return response
    },
    (error) => {
      console.group(`❌ Error #${error.config?.requestId}`)
      console.log('Status:', error.response?.status)
      console.log('Error:', error.response?.data || error.message)
      if (error.duration) console.log('Duration:', `${error.duration}ms`)
      console.groupEnd()
      return Promise.reject(error)
    }
  )
}

// Export axios instance and helpers
export default api
export { api }