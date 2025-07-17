import { ref, computed } from 'vue'
import axios from 'axios'

// Configuración de la API de Groq
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY

// Estado global para el composable
const loading = ref(false)
const error = ref(null)
const lastResponse = ref(null)

export function useGroqAPI() {
  // Función principal para enviar mensajes a Groq
  const sendToGroq = async (message, options = {}) => {
    loading.value = true
    error.value = null
    
    try {
      // Validar que tenemos la API key
      if (!GROQ_API_KEY) {
        console.warn('GROQ_API_KEY no está configurada, usando respuesta mock')
        const mockResponse = generateMockResponse(message)
        const mockData = {
          id: `mock-${Date.now()}`,
          object: 'chat.completion',
          created: Math.floor(Date.now() / 1000),
          model: options.model || 'mixtral-8x7b-32768',
          choices: [{
            index: 0,
            message: {
              role: 'assistant',
              content: mockResponse
            },
            finish_reason: 'stop'
          }],
          usage: {
            prompt_tokens: message.length / 4,
            completion_tokens: mockResponse.length / 4,
            total_tokens: (message.length + mockResponse.length) / 4
          }
        }
        lastResponse.value = mockData
        return { success: true, data: mockData, content: mockResponse }
      }
      
      // Configuración por defecto
      const defaultOptions = {
        model: 'mixtral-8x7b-32768', // Modelo por defecto de Groq
        temperature: 0.7,
        max_tokens: 1024,
        top_p: 1,
        stream: false
      }
      
      const config = { ...defaultOptions, ...options }
      
      // Preparar el payload para Groq
      const payload = {
        model: config.model,
        messages: [
          {
            role: 'user',
            content: message
          }
        ],
        temperature: config.temperature,
        max_tokens: config.max_tokens,
        top_p: config.top_p,
        stream: config.stream
      }
      
      try {
        // Realizar la petición a Groq
        const response = await axios.post(GROQ_API_URL, payload, {
          headers: {
            'Authorization': `Bearer ${GROQ_API_KEY}`,
            'Content-Type': 'application/json'
          },
          timeout: 30000 // 30 segundos de timeout
        })
        
        // Extraer la respuesta
        const aiResponse = response.data.choices[0]?.message?.content || 'Lo siento, no pude generar una respuesta.'
        lastResponse.value = response.data
        
        return { success: true, data: response.data, content: aiResponse }
      } catch (apiError) {
        console.warn('Groq API no disponible, usando respuesta mock:', apiError)
        const mockResponse = generateMockResponse(message)
        const mockData = {
          id: `mock-${Date.now()}`,
          object: 'chat.completion',
          created: Math.floor(Date.now() / 1000),
          model: config.model,
          choices: [{
            index: 0,
            message: {
              role: 'assistant',
              content: mockResponse
            },
            finish_reason: 'stop'
          }],
          usage: {
            prompt_tokens: message.length / 4,
            completion_tokens: mockResponse.length / 4,
            total_tokens: (message.length + mockResponse.length) / 4
          }
        }
        lastResponse.value = mockData
        return { success: true, data: mockData, content: mockResponse }
      }
      
    } catch (err) {
      console.error('Error en Groq API:', err)
      error.value = err.message || 'Error desconocido'
      
      // Usar respuesta mock como fallback
      const mockResponse = generateMockResponse(message)
      const mockData = {
        id: `mock-${Date.now()}`,
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model: options.model || 'mixtral-8x7b-32768',
        choices: [{
          index: 0,
          message: {
            role: 'assistant',
            content: mockResponse
          },
          finish_reason: 'stop'
        }],
        usage: {
          prompt_tokens: message.length / 4,
          completion_tokens: mockResponse.length / 4,
          total_tokens: (message.length + mockResponse.length) / 4
        }
      }
      lastResponse.value = mockData
      return { success: false, data: mockData, content: mockResponse, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Generar respuestas mock para propósitos de demo
  const generateMockResponse = (userMessage) => {
    const responses = [
      '¡Hola! Soy tu asistente de IA. Estoy aquí para ayudarte con cualquier pregunta que tengas.',
      'Entiendo tu consulta. Aunque estoy en modo demo, puedo ayudarte con información general.',
      'Esa es una excelente pregunta. Te ayudo a encontrar la información que necesitas.',
      'Gracias por tu mensaje. Estoy procesando tu solicitud y te daré la mejor respuesta posible.',
      'Me complace poder asistirte. ¿Hay algo específico en lo que pueda ayudarte hoy?',
      'Comprendo lo que me preguntas. Permíteme darte una respuesta útil basada en mi conocimiento.',
      'Esa es una consulta interesante. Te proporciono la mejor información disponible.',
      'Perfecto, puedo ayudarte con eso. Déjame explicarte de manera clara y concisa.'
    ]
    
    const lowerMessage = userMessage.toLowerCase()
    
    if (lowerMessage.includes('hola') || lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      return '¡Hola! 👋 Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?'
    }
    
    if (lowerMessage.includes('ayuda') || lowerMessage.includes('help')) {
      return 'Por supuesto, estoy aquí para ayudarte. Puedes preguntarme sobre cualquier tema y haré mi mejor esfuerzo para darte una respuesta útil. ¿Qué necesitas saber?'
    }
    
    if (lowerMessage.includes('gracias') || lowerMessage.includes('thank')) {
      return '¡De nada! Me alegra poder ayudarte. Si tienes más preguntas, no dudes en hacérmelas. 😊'
    }
    
    if (lowerMessage.includes('adiós') || lowerMessage.includes('bye') || lowerMessage.includes('hasta luego')) {
      return '¡Hasta luego! Que tengas un excelente día. Siempre estaré aquí cuando necesites ayuda. 👋'
    }
    
    if (lowerMessage.includes('cómo estás') || lowerMessage.includes('how are you')) {
      return '¡Estoy muy bien, gracias por preguntar! Listo para ayudarte con lo que necesites. ¿En qué puedo asistirte?'
    }
    
    if (lowerMessage.includes('qué puedes hacer') || lowerMessage.includes('what can you do')) {
      return 'Puedo ayudarte con una gran variedad de tareas: responder preguntas, explicar conceptos, ayudar con problemas técnicos, dar consejos, y mucho más. ¿Qué te gustaría saber?'
    }
    
    // Retornar una respuesta aleatoria para otros mensajes
    return responses[Math.floor(Math.random() * responses.length)]
  }
  
  // Función especializada para generar respuestas de chatbot
  const generateChatbotResponse = async (userMessage, chatbotType = 'general', context = {}) => {
    // Prompts especializados según el tipo de chatbot
    const systemPrompts = {
      general: 'Eres un asistente virtual útil y amigable. Responde de manera clara y concisa.',
      sales: 'Eres un asistente comercial especializado en ventas. Tu objetivo es ayudar a los clientes a encontrar productos que satisfagan sus necesidades y guiarlos hacia una compra.',
      support: 'Eres un especialista en soporte técnico. Tu objetivo es resolver problemas y dudas técnicas de manera eficiente y clara.',
      technical: 'Eres un experto técnico especializado en desarrollo y configuraciones. Proporciona soluciones detalladas y precisas.',
      customer_service: 'Eres un agente de atención al cliente. Tu prioridad es resolver consultas y mantener la satisfacción del cliente.',
      educational: 'Eres un tutor educativo. Explica conceptos de manera didáctica y adaptada al nivel del estudiante.'
    }
    
    const systemPrompt = systemPrompts[chatbotType] || systemPrompts.general
    
    // Construir el mensaje con contexto
    let enhancedMessage = userMessage
    
    if (context.previousMessages && context.previousMessages.length > 0) {
      const contextMessages = context.previousMessages.slice(-3) // Últimos 3 mensajes para contexto
      const contextString = contextMessages.map(msg => 
        `${msg.isUser ? 'Usuario' : 'Asistente'}: ${msg.text}`
      ).join('\n')
      
      enhancedMessage = `Contexto de la conversación:\n${contextString}\n\nNuevo mensaje del usuario: ${userMessage}`
    }
    
    // Configuración específica según el tipo de chatbot
    const chatbotConfigs = {
      general: { temperature: 0.7, max_tokens: 1024 },
      sales: { temperature: 0.8, max_tokens: 1200 },
      support: { temperature: 0.5, max_tokens: 1500 },
      technical: { temperature: 0.3, max_tokens: 2000 },
      customer_service: { temperature: 0.6, max_tokens: 1000 },
      educational: { temperature: 0.7, max_tokens: 1800 }
    }
    
    const config = chatbotConfigs[chatbotType] || chatbotConfigs.general
    
    try {
      // Enviar mensaje con prompt del sistema
      const fullMessage = `${systemPrompt}\n\nUsuario: ${enhancedMessage}`
      return await sendToGroq(fullMessage, config)
    } catch (error) {
      console.error('Error generating chatbot response:', error)
      
      // Respuestas de fallback específicas por tipo
      const fallbackResponses = {
        general: 'Disculpa, estoy experimentando dificultades técnicas. ¿Podrías reformular tu pregunta?',
        sales: 'Lo siento, no puedo procesar tu consulta en este momento. Un representante de ventas se pondrá en contacto contigo pronto.',
        support: 'Estamos experimentando problemas técnicos. Por favor, contacta a nuestro equipo de soporte directamente.',
        technical: 'Error en el sistema. Por favor, consulta la documentación técnica o contacta al administrador.',
        customer_service: 'Disculpa las molestias. Un agente se pondrá en contacto contigo para resolver tu consulta.',
        educational: 'Lo siento, no puedo explicar ese concepto en este momento. Te sugiero consultar los materiales de estudio.'
      }
      
      return fallbackResponses[chatbotType] || fallbackResponses.general
    }
  }
  
  // Función para obtener modelos disponibles
  const getAvailableModels = async () => {
    try {
      const response = await axios.get('https://api.groq.com/openai/v1/models', {
        headers: {
          'Authorization': `Bearer ${GROQ_API_KEY}`,
          'Content-Type': 'application/json'
        }
      })
      
      return response.data.data || []
    } catch (error) {
      console.error('Error fetching models:', error)
      return [
        { id: 'mixtral-8x7b-32768', name: 'Mixtral 8x7B' },
        { id: 'llama2-70b-4096', name: 'Llama 2 70B' },
        { id: 'gemma-7b-it', name: 'Gemma 7B' }
      ]
    }
  }
  
  // Función para validar la configuración
  const validateConfiguration = () => {
    const issues = []
    
    if (!GROQ_API_KEY) {
      issues.push('GROQ_API_KEY no está configurada')
    }
    
    if (GROQ_API_KEY && GROQ_API_KEY.length < 10) {
      issues.push('GROQ_API_KEY parece ser inválida')
    }
    
    return {
      isValid: issues.length === 0,
      issues
    }
  }
  
  // Función para limpiar el estado
  const clearState = () => {
    loading.value = false
    error.value = null
    lastResponse.value = null
  }
  
  // Computed properties
  const isConfigured = computed(() => {
    return !!GROQ_API_KEY
  })
  
  const hasError = computed(() => {
    return !!error.value
  })
  
  const isLoading = computed(() => {
    return loading.value
  })
  
  // Función para generar respuestas inteligentes basadas en patrones
  const generateSmartResponse = async (message, chatbotType = 'general') => {
    const lowerMessage = message.toLowerCase()
    
    // Patrones de respuesta rápida
    const quickResponses = {
      greeting: {
        patterns: ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'saludos'],
        responses: {
          general: '¡Hola! ¿En qué puedo ayudarte hoy?',
          sales: '¡Bienvenido! ¿Te interesa conocer nuestros productos?',
          support: 'Hola, ¿qué problema puedo ayudarte a resolver?',
          technical: 'Saludos, ¿necesitas ayuda técnica?'
        }
      },
      thanks: {
        patterns: ['gracias', 'muchas gracias', 'te agradezco', 'thanks'],
        responses: {
          general: '¡De nada! ¿Hay algo más en lo que pueda ayudarte?',
          sales: '¡Un placer ayudarte! ¿Te interesa algún otro producto?',
          support: 'Me alegra haber podido ayudarte. ¿Necesitas algo más?',
          technical: 'Perfecto. ¿Alguna otra consulta técnica?'
        }
      },
      goodbye: {
        patterns: ['adiós', 'hasta luego', 'nos vemos', 'chao', 'bye'],
        responses: {
          general: '¡Hasta luego! Que tengas un excelente día.',
          sales: '¡Gracias por tu interés! Esperamos verte pronto.',
          support: '¡Hasta pronto! No dudes en contactarnos si necesitas más ayuda.',
          technical: 'Hasta la próxima. ¡Que tengas éxito con tu proyecto!'
        }
      }
    }
    
    // Verificar patrones de respuesta rápida
    for (const [category, data] of Object.entries(quickResponses)) {
      if (data.patterns.some(pattern => lowerMessage.includes(pattern))) {
        return data.responses[chatbotType] || data.responses.general
      }
    }
    
    // Si no hay patrón rápido, usar Groq API
    return await generateChatbotResponse(message, chatbotType)
  }
  
  return {
    // Estado
    loading: isLoading,
    error,
    lastResponse,
    isConfigured,
    hasError,
    
    // Métodos principales
    sendToGroq,
    generateChatbotResponse,
    generateSmartResponse,
    
    // Métodos auxiliares
    getAvailableModels,
    validateConfiguration,
    clearState
  }
}

// Exportar también como default para mayor flexibilidad
export default useGroqAPI