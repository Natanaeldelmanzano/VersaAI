import axios from 'axios'

// Configuración base de Axios
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para requests
axiosInstance.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// Interceptor para responses
axiosInstance.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error(`❌ API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, error.response?.data || error.message)
    
    // Solo simular respuestas si hay error de conexión (ECONNREFUSED, Network Error, etc.)
    if (import.meta.env.DEV && (error.code === 'ECONNREFUSED' || error.message === 'Network Error' || !error.response)) {
      console.warn('🔧 Backend no disponible, usando respuestas simuladas')
      return handleDevModeError(error)
    }
    
    return Promise.reject(error)
  }
)

// Simular respuestas en modo desarrollo
const handleDevModeError = (error) => {
  const { method, url } = error.config
  
  console.log(`🔧 Dev Mode: Simulando respuesta para ${method?.toUpperCase()} ${url}`)
  
  // Simular respuestas exitosas para endpoints comunes
  const mockResponses = {
    'GET /api/v1/auth/me': {
      data: {
        id: 1,
        email: 'demo@versaai.com',
        first_name: 'Demo',
        last_name: 'User',
        role: 'user',
        organization: 'VersaAI Demo',
        avatar: null,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    },
    'GET /api/v1/system/info': {
      data: {
        name: 'VersaAI',
        version: '1.0.0',
        description: 'Plataforma de chatbots con IA',
        environment: 'development'
      }
    },
    'GET /api/v1/system/status': {
      data: {
        status: 'operational',
        uptime: 3600,
        services: {
          api: 'operational',
          database: 'operational',
          ai_service: 'operational',
          storage: 'operational'
        }
      }
    },
    'GET /api/v1/notifications': {
      data: {
        items: [
          {
            id: 1,
            title: 'Bienvenido a VersaAI',
            message: 'Tu cuenta ha sido creada exitosamente',
            type: 'info',
            read: false,
            created_at: new Date().toISOString()
          }
        ],
        total: 1
      }
    },
    'GET /api/v1/conversations/': {
      data: {
        items: [
          {
            id: 1,
            title: 'Conversación de ejemplo',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            message_count: 2,
            last_message: 'Hola, ¿en qué puedo ayudarte?'
          }
        ],
        total: 1,
        page: 1,
        per_page: 20
      }
    },
    'POST /api/v1/conversations/': {
      data: {
        id: 2,
        title: 'Nueva conversación',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        message_count: 0
      }
    },
    'POST /api/v1/conversations/chat': {
      data: {
        message: {
          id: Date.now(),
          content: 'Esta es una respuesta simulada del asistente de IA. En producción, aquí aparecería la respuesta real del modelo de IA.',
          role: 'assistant',
          created_at: new Date().toISOString()
        },
        conversation_id: 1,
        message_id: Date.now(),
        sources: [],
        confidence: 0.95,
        response_time: 1.2,
        tokens_used: 150,
        model: 'groq-llama'
      }
    }
  }
  
  const key = `${method?.toUpperCase()} ${url}`
  const mockResponse = mockResponses[key]
  
  if (mockResponse) {
    return Promise.resolve({
      ...mockResponse,
      status: 200,
      statusText: 'OK',
      config: error.config
    })
  }
  
  // Para otros endpoints, devolver error simulado
  return Promise.reject({
    ...error,
    response: {
      status: 404,
      data: { detail: `Endpoint ${url} no implementado en modo desarrollo` }
    }
  })
}

export default axiosInstance