import { z } from 'zod'

// Esquemas base reutilizables
const emailSchema = z
  .string()
  .min(1, 'El email es requerido')
  .email('Formato de email inválido')
  .max(255, 'El email es demasiado largo')

const passwordSchema = z
  .string()
  .min(8, 'La contraseña debe tener al menos 8 caracteres')
  .max(128, 'La contraseña es demasiado larga')
  .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 
    'La contraseña debe contener al menos una minúscula, una mayúscula y un número')

const nameSchema = z
  .string()
  .min(2, 'El nombre debe tener al menos 2 caracteres')
  .max(100, 'El nombre es demasiado largo')
  .regex(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/, 'El nombre solo puede contener letras y espacios')

// Esquemas de autenticación
export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, 'La contraseña es requerida'),
  remember: z.boolean().optional().default(false)
})

export const registerSchema = z.object({
  name: nameSchema,
  email: emailSchema,
  password: passwordSchema,
  password_confirmation: z.string().min(1, 'Confirma tu contraseña'),
  terms_accepted: z.boolean().refine(val => val === true, {
    message: 'Debes aceptar los términos y condiciones'
  })
}).refine(data => data.password === data.password_confirmation, {
  message: 'Las contraseñas no coinciden',
  path: ['password_confirmation']
})

export const forgotPasswordSchema = z.object({
  email: emailSchema
})

export const resetPasswordSchema = z.object({
  token: z.string().min(1, 'Token requerido'),
  email: emailSchema,
  password: passwordSchema,
  password_confirmation: z.string().min(1, 'Confirma tu contraseña')
}).refine(data => data.password === data.password_confirmation, {
  message: 'Las contraseñas no coinciden',
  path: ['password_confirmation']
})

export const changePasswordSchema = z.object({
  current_password: z.string().min(1, 'La contraseña actual es requerida'),
  new_password: passwordSchema,
  new_password_confirmation: z.string().min(1, 'Confirma tu nueva contraseña')
}).refine(data => data.new_password === data.new_password_confirmation, {
  message: 'Las contraseñas no coinciden',
  path: ['new_password_confirmation']
}).refine(data => data.current_password !== data.new_password, {
  message: 'La nueva contraseña debe ser diferente a la actual',
  path: ['new_password']
})

// Esquemas de perfil de usuario
export const updateProfileSchema = z.object({
  name: nameSchema.optional(),
  email: emailSchema.optional(),
  avatar: z.string().url('URL de avatar inválida').optional().or(z.literal('')),
  preferences: z.object({
    theme: z.enum(['light', 'dark', 'auto']).optional(),
    language: z.string().min(2).max(5).optional(),
    notifications: z.boolean().optional()
  }).optional()
})

// Esquemas de chatbot
export const chatbotSchema = z.object({
  name: z.string()
    .min(2, 'El nombre debe tener al menos 2 caracteres')
    .max(100, 'El nombre es demasiado largo'),
  description: z.string()
    .min(10, 'La descripción debe tener al menos 10 caracteres')
    .max(500, 'La descripción es demasiado larga'),
  model: z.enum(['gpt-3.5-turbo', 'gpt-4', 'claude-3-sonnet', 'claude-3-haiku'], {
    errorMap: () => ({ message: 'Selecciona un modelo válido' })
  }),
  temperature: z.number()
    .min(0, 'La temperatura mínima es 0')
    .max(2, 'La temperatura máxima es 2')
    .default(0.7),
  max_tokens: z.number()
    .min(1, 'Mínimo 1 token')
    .max(4096, 'Máximo 4096 tokens')
    .default(1000),
  system_prompt: z.string()
    .min(10, 'El prompt del sistema debe tener al menos 10 caracteres')
    .max(2000, 'El prompt del sistema es demasiado largo'),
  is_public: z.boolean().default(false),
  tags: z.array(z.string().min(1).max(50)).max(10, 'Máximo 10 tags').optional(),
  avatar: z.string().url('URL de avatar inválida').optional().or(z.literal('')),
  welcome_message: z.string()
    .min(5, 'El mensaje de bienvenida debe tener al menos 5 caracteres')
    .max(200, 'El mensaje de bienvenida es demasiado largo')
    .optional(),
  fallback_message: z.string()
    .min(5, 'El mensaje de fallback debe tener al menos 5 caracteres')
    .max(200, 'El mensaje de fallback es demasiado largo')
    .optional()
})

export const updateChatbotSchema = chatbotSchema.partial()

// Alias para compatibilidad
export const chatbotConfigSchema = chatbotSchema
export const userProfileSchema = updateProfileSchema

// Esquemas de conversación
export const messageSchema = z.object({
  content: z.string()
    .min(1, 'El mensaje no puede estar vacío')
    .max(4000, 'El mensaje es demasiado largo'),
  type: z.enum(['text', 'image', 'file']).default('text'),
  metadata: z.object({
    file_url: z.string().url().optional(),
    file_name: z.string().optional(),
    file_size: z.number().optional(),
    image_url: z.string().url().optional()
  }).optional()
})

export const conversationSchema = z.object({
  title: z.string()
    .min(1, 'El título es requerido')
    .max(200, 'El título es demasiado largo')
    .optional(),
  chatbot_id: z.string().uuid('ID de chatbot inválido'),
  is_pinned: z.boolean().default(false),
  tags: z.array(z.string().min(1).max(50)).max(5, 'Máximo 5 tags').optional()
})

// Esquemas de organización
export const organizationSchema = z.object({
  name: z.string()
    .min(2, 'El nombre debe tener al menos 2 caracteres')
    .max(100, 'El nombre es demasiado largo'),
  description: z.string()
    .max(500, 'La descripción es demasiado larga')
    .optional(),
  website: z.string().url('URL inválida').optional().or(z.literal('')),
  logo: z.string().url('URL de logo inválida').optional().or(z.literal('')),
  settings: z.object({
    max_chatbots: z.number().min(1).max(1000).default(10),
    max_conversations_per_month: z.number().min(100).max(1000000).default(1000),
    allowed_models: z.array(z.string()).min(1, 'Selecciona al menos un modelo'),
    custom_branding: z.boolean().default(false),
    api_access: z.boolean().default(false),
    sso_enabled: z.boolean().default(false)
  }).optional()
})

export const inviteUserSchema = z.object({
  email: emailSchema,
  role: z.enum(['admin', 'moderator', 'user'], {
    errorMap: () => ({ message: 'Selecciona un rol válido' })
  }),
  message: z.string()
    .max(500, 'El mensaje es demasiado largo')
    .optional()
})

// Esquemas de documentos
export const documentSchema = z.object({
  title: z.string()
    .min(2, 'El título debe tener al menos 2 caracteres')
    .max(200, 'El título es demasiado largo'),
  content: z.string()
    .min(10, 'El contenido debe tener al menos 10 caracteres')
    .max(50000, 'El contenido es demasiado largo'),
  type: z.enum(['text', 'markdown', 'pdf', 'docx'], {
    errorMap: () => ({ message: 'Tipo de documento inválido' })
  }),
  tags: z.array(z.string().min(1).max(50)).max(10, 'Máximo 10 tags').optional(),
  is_public: z.boolean().default(false),
  chatbot_ids: z.array(z.string().uuid()).optional(),
  metadata: z.object({
    file_url: z.string().url().optional(),
    file_size: z.number().optional(),
    page_count: z.number().optional(),
    language: z.string().optional()
  }).optional()
})

// Esquemas de configuración
export const settingsSchema = z.object({
  general: z.object({
    site_name: z.string().min(1).max(100),
    site_description: z.string().max(500).optional(),
    contact_email: emailSchema,
    support_url: z.string().url().optional().or(z.literal('')),
    terms_url: z.string().url().optional().or(z.literal('')),
    privacy_url: z.string().url().optional().or(z.literal(''))
  }).optional(),
  
  ai: z.object({
    default_model: z.string().min(1),
    max_tokens_per_request: z.number().min(1).max(8192),
    rate_limit_per_minute: z.number().min(1).max(1000),
    enable_content_filter: z.boolean().default(true),
    allowed_file_types: z.array(z.string()).optional()
  }).optional(),
  
  security: z.object({
    session_timeout: z.number().min(5).max(1440), // minutos
    max_login_attempts: z.number().min(3).max(10),
    require_email_verification: z.boolean().default(true),
    enable_2fa: z.boolean().default(false),
    password_expiry_days: z.number().min(30).max(365).optional()
  }).optional(),
  
  notifications: z.object({
    email_notifications: z.boolean().default(true),
    push_notifications: z.boolean().default(false),
    slack_webhook: z.string().url().optional().or(z.literal('')),
    discord_webhook: z.string().url().optional().or(z.literal(''))
  }).optional()
})

// Esquemas de búsqueda y filtros
export const searchSchema = z.object({
  query: z.string().min(1, 'Ingresa un término de búsqueda').max(200),
  filters: z.object({
    type: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
    date_from: z.string().datetime().optional(),
    date_to: z.string().datetime().optional(),
    author: z.string().optional()
  }).optional(),
  sort: z.enum(['relevance', 'date', 'name', 'popularity']).default('relevance'),
  order: z.enum(['asc', 'desc']).default('desc'),
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(20)
})

// Esquemas de API y webhooks
export const webhookSchema = z.object({
  name: z.string().min(1).max(100),
  url: z.string().url('URL inválida'),
  events: z.array(z.enum([
    'conversation.created',
    'conversation.updated',
    'message.sent',
    'message.received',
    'chatbot.created',
    'chatbot.updated',
    'user.registered',
    'user.updated'
  ])).min(1, 'Selecciona al menos un evento'),
  secret: z.string().min(8).max(128).optional(),
  is_active: z.boolean().default(true),
  headers: z.record(z.string()).optional()
})

export const apiKeySchema = z.object({
  name: z.string().min(1).max(100),
  permissions: z.array(z.enum([
    'read:chatbots',
    'write:chatbots',
    'read:conversations',
    'write:conversations',
    'read:documents',
    'write:documents',
    'read:analytics',
    'admin:all'
  ])).min(1, 'Selecciona al menos un permiso'),
  expires_at: z.string().datetime().optional()
})

// Tipos TypeScript derivados de los esquemas
export type LoginData = z.infer<typeof loginSchema>
export type RegisterData = z.infer<typeof registerSchema>
export type ForgotPasswordData = z.infer<typeof forgotPasswordSchema>
export type ResetPasswordData = z.infer<typeof resetPasswordSchema>
export type ChangePasswordData = z.infer<typeof changePasswordSchema>
export type UpdateProfileData = z.infer<typeof updateProfileSchema>
export type ChatbotData = z.infer<typeof chatbotSchema>
export type UpdateChatbotData = z.infer<typeof updateChatbotSchema>
export type MessageData = z.infer<typeof messageSchema>
export type ConversationData = z.infer<typeof conversationSchema>
export type OrganizationData = z.infer<typeof organizationSchema>
export type InviteUserData = z.infer<typeof inviteUserSchema>
export type DocumentData = z.infer<typeof documentSchema>
export type SettingsData = z.infer<typeof settingsSchema>
export type SearchData = z.infer<typeof searchSchema>
export type WebhookData = z.infer<typeof webhookSchema>
export type ApiKeyData = z.infer<typeof apiKeySchema>

// Función helper para validación
export const validateData = <T>(
  schema: z.ZodSchema<T>,
  data: unknown
): { success: true; data: T } | { success: false; errors: string[] } => {
  try {
    const validatedData = schema.parse(data)
    return { success: true, data: validatedData }
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errors = error.errors.map(err => {
        const path = err.path.join('.')
        return path ? `${path}: ${err.message}` : err.message
      })
      return { success: false, errors }
    }
    return { success: false, errors: ['Error de validación desconocido'] }
  }
}

// Función helper para validación segura (no lanza errores)
export const safeValidate = <T>(
  schema: z.ZodSchema<T>,
  data: unknown
): T | null => {
  try {
    return schema.parse(data)
  } catch {
    return null
  }
}

// Función helper para validación parcial
export const validatePartial = <T>(
  schema: z.ZodSchema<T>,
  data: unknown
): Partial<T> | null => {
  try {
    return schema.partial().parse(data)
  } catch {
    return null
  }
}