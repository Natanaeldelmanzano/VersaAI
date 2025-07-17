// VersaAI API Configuration - VERSIÓN CORREGIDA
import axios from 'axios'

// Configuración base de la API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

console.log('🔧 Configurando API con URL base:', API_BASE_URL)

// Crear instancia de axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Interceptor para requests
apiClient.interceptors.request.use(
  (config) => {
    console.log('📡 Enviando petición:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      headers: config.headers,
      data: config.data
    })
    return config
  },
  (error) => {
    console.error('❌ Error en request interceptor:', error)
    return Promise.reject(error)
  }
)

// Interceptor para responses
apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ Respuesta recibida:', {
      status: response.status,
      statusText: response.statusText,
      url: response.config.url,
      data: response.data
    })
    return response
  },
  (error) => {
    console.error('❌ Error en response interceptor:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      data: error.response?.data
    })

    // Manejar errores específicos
    if (error.response?.status === 401) {
      console.warn('🔐 Token expirado o inválido')
      // Limpiar localStorage y redirigir al login
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_data')
      window.location.href = '/auth/login'
    }

    return Promise.reject(error)
  }
)

// API endpoints
const api = {
  // Authentication
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (userData) => apiClient.post('/auth/register', userData),
    logout: () => apiClient.post('/auth/logout'),
    refreshToken: (refreshToken) => apiClient.post('/auth/refresh', { refresh_token: refreshToken }),
    refresh: () => apiClient.post('/auth/refresh'),
    me: () => apiClient.get('/auth/me'),
    forgotPassword: (data) => apiClient.post('/auth/forgot-password', data),
    resetPassword: (data) => apiClient.post('/auth/reset-password', data)
  },

  // Users
  users: {
    getProfile: () => apiClient.get('/users/profile'),
    updateProfile: (data) => apiClient.put('/users/profile', data),
    changePassword: (data) => apiClient.post('/users/change-password', data)
  },

  // Organizations
  organizations: {
    list: () => apiClient.get('/organizations'),
    get: (id) => apiClient.get(`/organizations/${id}`),
    create: (data) => apiClient.post('/organizations', data),
    update: (id, data) => apiClient.put(`/organizations/${id}`, data),
    delete: (id) => apiClient.delete(`/organizations/${id}`)
  },

  // Chatbots
  chatbots: {
    list: () => apiClient.get('/chatbots'),
    get: (id) => apiClient.get(`/chatbots/${id}`),
    create: (data) => apiClient.post('/chatbots', data),
    update: (id, data) => apiClient.put(`/chatbots/${id}`, data),
    delete: (id) => apiClient.delete(`/chatbots/${id}`),
    train: (id, data) => apiClient.post(`/chatbots/${id}/train`, data)
  },

  // Conversations
  conversations: {
    list: (chatbotId) => apiClient.get(`/conversations?chatbot_id=${chatbotId}`),
    get: (id) => apiClient.get(`/conversations/${id}`),
    create: (data) => apiClient.post('/conversations', data),
    sendMessage: (conversationId, message) => 
      apiClient.post(`/conversations/${conversationId}/messages`, { content: message })
  },

  // Documents
  documents: {
    list: () => apiClient.get('/documents'),
    upload: (file, chatbotId) => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('chatbot_id', chatbotId)
      return apiClient.post('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    },
    delete: (id) => apiClient.delete(`/documents/${id}`)
  },

  // Analytics
  analytics: {
    getDashboard: () => apiClient.get('/analytics/dashboard'),
    getChatbotStats: (chatbotId) => apiClient.get(`/analytics/chatbots/${chatbotId}`),
    getConversationStats: () => apiClient.get('/analytics/conversations')
  },

  // Settings
  settings: {
    getGlobal: () => apiClient.get('/settings/global'),
    updateGlobal: (data) => apiClient.put('/settings/global', data),
    getUser: () => apiClient.get('/settings/user'),
    updateUser: (data) => apiClient.put('/settings/user', data)
  }
}

// Health check
export const healthCheck = () => {
  return axios.get(`${API_BASE_URL}/health`)
}

// Exportar configuraciones específicas
export const authAPI = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  register: (userData) => apiClient.post('/auth/register', userData),
  logout: () => apiClient.post('/auth/logout'),
  me: () => apiClient.get('/auth/me'),
  refreshToken: () => apiClient.post('/auth/refresh')
}

export const chatbotAPI = {
  list: () => apiClient.get('/chatbots'),
  create: (data) => apiClient.post('/chatbots', data),
  update: (id, data) => apiClient.put(`/chatbots/${id}`, data),
  delete: (id) => apiClient.delete(`/chatbots/${id}`)
}

export const conversationAPI = {
  list: () => apiClient.get('/conversations'),
  create: (data) => apiClient.post('/conversations', data),
  messages: (id) => apiClient.get(`/conversations/${id}/messages`)
}

// Exportar la instancia configurada y los endpoints
export { api }
export default apiClient

// Export configuration
export const config = {
  API_BASE_URL,
  TIMEOUT: 10000
}