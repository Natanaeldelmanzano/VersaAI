import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const authStore = useAuthStore()
    const toast = useToast()
    
    if (error.response?.status === 401) {
      // Token expired or invalid
      authStore.logout()
      toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.')
      window.location.href = '/login'
    } else if (error.response?.status === 403) {
      toast.error('No tienes permisos para realizar esta acción.')
    } else if (error.response?.status === 404) {
      toast.error('Recurso no encontrado.')
    } else if (error.response?.status >= 500) {
      toast.error('Error del servidor. Por favor, intenta más tarde.')
    } else if (error.code === 'ECONNABORTED') {
      toast.error('Tiempo de espera agotado. Verifica tu conexión.')
    } else {
      toast.error(error.response?.data?.detail || 'Error inesperado')
    }
    
    return Promise.reject(error)
  }
)

export default api

// API Services
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  refreshToken: () => api.post('/auth/refresh'),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  resetPassword: (token, password) => api.post('/auth/reset-password', { token, password }),
  verifyEmail: (token) => api.post('/auth/verify-email', { token }),
  getCurrentUser: () => api.get('/auth/me')
}

export const usersAPI = {
  getUsers: (params) => api.get('/users', { params }),
  getUser: (id) => api.get(`/users/${id}`),
  createUser: (userData) => api.post('/users', userData),
  updateUser: (id, userData) => api.put(`/users/${id}`, userData),
  deleteUser: (id) => api.delete(`/users/${id}`),
  updateProfile: (userData) => api.put('/users/profile', userData),
  changePassword: (passwordData) => api.put('/users/change-password', passwordData),
  uploadAvatar: (formData) => api.post('/users/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const organizationsAPI = {
  getOrganizations: () => api.get('/organizations'),
  getOrganization: (id) => api.get(`/organizations/${id}`),
  createOrganization: (orgData) => api.post('/organizations', orgData),
  updateOrganization: (id, orgData) => api.put(`/organizations/${id}`, orgData),
  deleteOrganization: (id) => api.delete(`/organizations/${id}`),
  getMembers: (id) => api.get(`/organizations/${id}/members`),
  addMember: (id, memberData) => api.post(`/organizations/${id}/members`, memberData),
  removeMember: (id, userId) => api.delete(`/organizations/${id}/members/${userId}`),
  updateMemberRole: (id, userId, role) => api.put(`/organizations/${id}/members/${userId}`, { role })
}

export const chatbotsAPI = {
  getChatbots: (params) => api.get('/chatbots', { params }),
  getChatbot: (id) => api.get(`/chatbots/${id}`),
  createChatbot: (chatbotData) => api.post('/chatbots', chatbotData),
  updateChatbot: (id, chatbotData) => api.put(`/chatbots/${id}`, chatbotData),
  deleteChatbot: (id) => api.delete(`/chatbots/${id}`),
  toggleChatbot: (id, status) => api.patch(`/chatbots/${id}/status`, { status }),
  testChatbot: (id, message) => api.post(`/chatbots/${id}/test`, { message }),
  getChatbotStats: (id) => api.get(`/chatbots/${id}/stats`),
  getChatbotConversations: (id, params) => api.get(`/chatbots/${id}/conversations`, { params }),
  exportChatbot: (id) => api.get(`/chatbots/${id}/export`),
  importChatbot: (formData) => api.post('/chatbots/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const conversationsAPI = {
  getConversations: (params) => api.get('/conversations', { params }),
  getConversation: (id) => api.get(`/conversations/${id}`),
  createConversation: (conversationData) => api.post('/conversations', conversationData),
  updateConversation: (id, conversationData) => api.put(`/conversations/${id}`, conversationData),
  deleteConversation: (id) => api.delete(`/conversations/${id}`),
  getMessages: (id, params) => api.get(`/conversations/${id}/messages`, { params }),
  sendMessage: (id, messageData) => api.post(`/conversations/${id}/messages`, messageData),
  rateConversation: (id, rating) => api.post(`/conversations/${id}/rate`, { rating }),
  exportConversation: (id) => api.get(`/conversations/${id}/export`)
}

export const knowledgeBaseAPI = {
  getDocuments: (params) => api.get('/knowledge-base/documents', { params }),
  getDocument: (id) => api.get(`/knowledge-base/documents/${id}`),
  uploadDocument: (formData) => api.post('/knowledge-base/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateDocument: (id, documentData) => api.put(`/knowledge-base/documents/${id}`, documentData),
  deleteDocument: (id) => api.delete(`/knowledge-base/documents/${id}`),
  searchDocuments: (query, params) => api.get('/knowledge-base/search', { params: { q: query, ...params } }),
  getCollections: () => api.get('/knowledge-base/collections'),
  createCollection: (collectionData) => api.post('/knowledge-base/collections', collectionData),
  updateCollection: (id, collectionData) => api.put(`/knowledge-base/collections/${id}`, collectionData),
  deleteCollection: (id) => api.delete(`/knowledge-base/collections/${id}`)
}

export const analyticsAPI = {
  getOverview: (params) => api.get('/analytics/overview', { params }),
  getChatbotAnalytics: (params) => api.get('/analytics/chatbots', { params }),
  getConversationAnalytics: (params) => api.get('/analytics/conversations', { params }),
  getUsageAnalytics: (params) => api.get('/analytics/usage', { params }),
  getUserAnalytics: (params) => api.get('/analytics/users', { params }),
  getPerformanceMetrics: (params) => api.get('/analytics/performance', { params }),
  exportReport: (type, params) => api.get(`/analytics/export/${type}`, { params, responseType: 'blob' }),
  getRealtimeMetrics: () => api.get('/analytics/realtime')
}

export const settingsAPI = {
  getSettings: () => api.get('/settings'),
  updateSettings: (settingsData) => api.put('/settings', settingsData),
  getSystemSettings: () => api.get('/settings/system'),
  updateSystemSettings: (settingsData) => api.put('/settings/system', settingsData),
  getAISettings: () => api.get('/settings/ai'),
  updateAISettings: (settingsData) => api.put('/settings/ai', settingsData),
  getNotificationSettings: () => api.get('/settings/notifications'),
  updateNotificationSettings: (settingsData) => api.put('/settings/notifications', settingsData),
  getSecuritySettings: () => api.get('/settings/security'),
  updateSecuritySettings: (settingsData) => api.put('/settings/security', settingsData),
  resetSettings: () => api.post('/settings/reset'),
  exportSettings: () => api.get('/settings/export', { responseType: 'blob' }),
  importSettings: (formData) => api.post('/settings/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getRecentActivity: (params) => api.get('/dashboard/activity', { params }),
  getQuickMetrics: () => api.get('/dashboard/metrics'),
  getSystemHealth: () => api.get('/dashboard/health'),
  getNotifications: (params) => api.get('/dashboard/notifications', { params })
}

export const notificationsAPI = {
  getNotifications: (params) => api.get('/notifications', { params }),
  markAsRead: (id) => api.patch(`/notifications/${id}/read`),
  markAllAsRead: () => api.patch('/notifications/read-all'),
  deleteNotification: (id) => api.delete(`/notifications/${id}`),
  getUnreadCount: () => api.get('/notifications/unread-count'),
  updatePreferences: (preferences) => api.put('/notifications/preferences', preferences)
}

export const systemAPI = {
  getSystemInfo: () => api.get('/system/info'),
  getSystemHealth: () => api.get('/system/health'),
  getSystemLogs: (params) => api.get('/system/logs', { params }),
  getSystemMetrics: () => api.get('/system/metrics'),
  performMaintenance: (action) => api.post('/system/maintenance', { action }),
  backupSystem: () => api.post('/system/backup'),
  restoreSystem: (backupId) => api.post('/system/restore', { backup_id: backupId })
}

export const widgetsAPI = {
  getWidgets: () => api.get('/widgets'),
  getWidget: (id) => api.get(`/widgets/${id}`),
  createWidget: (widgetData) => api.post('/widgets', widgetData),
  updateWidget: (id, widgetData) => api.put(`/widgets/${id}`, widgetData),
  deleteWidget: (id) => api.delete(`/widgets/${id}`),
  getWidgetCode: (id) => api.get(`/widgets/${id}/code`),
  getWidgetStats: (id) => api.get(`/widgets/${id}/stats`)
}