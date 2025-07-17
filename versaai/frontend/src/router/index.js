import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layouts
import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'

// Public Views
import Home from '@/views/Home.vue'
import NotFound from '@/views/NotFound.vue'

// Auth Views
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import ForgotPassword from '@/views/auth/ForgotPassword.vue'
import ResetPassword from '@/views/auth/ResetPassword.vue'

// New Auth Views
import NewLogin from '@/views/auth/NewLogin.vue'
import NewRegister from '@/views/auth/NewRegister.vue'
import AuthDemo from '@/views/AuthDemo.vue'

// Dashboard Views
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Overview from '@/views/dashboard/Overview.vue'
import Chatbots from '@/views/dashboard/Chatbots.vue'
import ChatbotDetail from '@/views/dashboard/ChatbotDetail.vue'
import Chat from '@/views/dashboard/Chat.vue'
import Conversations from '@/views/dashboard/Conversations.vue'
import ConversationDetail from '@/views/dashboard/ConversationDetail.vue'
import KnowledgeBases from '@/views/dashboard/KnowledgeBases.vue'
import KnowledgeBaseDetail from '@/views/dashboard/KnowledgeBaseDetail.vue'
import Analytics from '@/views/dashboard/Analytics.vue'
import Users from '@/views/dashboard/Users.vue'
import Settings from '@/views/dashboard/Settings.vue'
import Profile from '@/views/dashboard/Profile.vue'
import Organization from '@/views/dashboard/Organization.vue'
import EnterpriseDashboard from '@/views/dashboard/EnterpriseDashboard.vue'
import OrganizationManagement from '@/views/dashboard/OrganizationManagement.vue'
import Integrations from '@/views/dashboard/Integrations.vue'
import SecurityCenter from '@/views/dashboard/SecurityCenter.vue'
import WidgetManager from '@/views/dashboard/WidgetManager.vue'
import Pricing from '@/views/dashboard/Pricing.vue'

// Mobile Views
import MobileDashboard from '@/views/mobile/MobileDashboard.vue'

// Error Views
import ServerError from '@/views/errors/ServerError.vue'
import Unauthorized from '@/views/errors/Unauthorized.vue'

// Widget Views
import WidgetDemo from '@/views/widget/WidgetDemo.vue'

// Test Views
import ExamplesView from '@/views/ExamplesView.vue'
import TestPage from '@/views/TestPage.vue'
import DiagnosticPage from '@/views/DiagnosticPage.vue'
import ApiTestingChat from '@/views/ApiTestingChat.vue'
import IntegrationTest from '@/views/IntegrationTest.vue'

const routes = [
  // Public Routes
  {
    path: '/',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: Home,
        meta: { title: 'VersaAI - Plataforma de Chatbots Empresariales' }
      },
      {
        path: 'widget-demo',
        name: 'WidgetDemo',
        component: WidgetDemo,
        meta: { title: 'Demo Widget - VersaAI' }
      },
      {
        path: 'auth-demo',
        name: 'AuthDemo',
        component: AuthDemo,
        meta: { title: 'Demo Autenticación - VersaAI' }
      }
    ]
  },

  // Auth Routes
  {
    path: '/auth',
    component: AuthLayout,
    meta: { requiresGuest: true },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { title: 'Iniciar Sesión - VersaAI' }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { title: 'Registro - VersaAI' }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: ForgotPassword,
        meta: { title: 'Recuperar Contraseña - VersaAI' }
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: ResetPassword,
        meta: { title: 'Restablecer Contraseña - VersaAI' }
      },
      {
        path: 'new-login',
        name: 'NewLogin',
        component: NewLogin,
        meta: { title: 'Nuevo Login - VersaAI' }
      },
      {
        path: 'new-register',
        name: 'NewRegister',
        component: NewRegister,
        meta: { title: 'Nuevo Registro - VersaAI' }
      }
    ]
  },

  // Dashboard Routes
  {
    path: '/dashboard',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: 'Dashboard - VersaAI' }
      },
      {
        path: 'overview',
        name: 'Overview',
        component: Overview,
        meta: { title: 'Resumen - VersaAI' }
      },
      {
        path: 'enterprise',
        name: 'EnterpriseDashboard',
        component: EnterpriseDashboard,
        meta: { 
          title: 'Dashboard Empresarial - VersaAI',
          requiresRole: ['admin', 'enterprise']
        }
      },
      
      // Chatbots
      {
        path: 'chatbots',
        name: 'Chatbots',
        component: Chatbots,
        meta: { title: 'Chatbots - VersaAI' }
      },
      {
        path: 'chatbots/:id',
        name: 'ChatbotDetail',
        component: ChatbotDetail,
        meta: { title: 'Detalle Chatbot - VersaAI' }
      },
      
      // Chat
      {
        path: 'chat',
        name: 'Chat',
        component: Chat,
        meta: { title: 'Chat - VersaAI' }
      },
      {
        path: 'chat/:chatbotId',
        name: 'ChatWithBot',
        component: Chat,
        meta: { title: 'Chat - VersaAI' }
      },
      
      // Conversations
      {
        path: 'conversations',
        name: 'Conversations',
        component: Conversations,
        meta: { title: 'Conversaciones - VersaAI' }
      },
      {
        path: 'conversations/:id',
        name: 'ConversationDetail',
        component: ConversationDetail,
        meta: { title: 'Detalle Conversación - VersaAI' }
      },
      
      // Knowledge Bases
      {
        path: 'knowledge-bases',
        name: 'KnowledgeBases',
        component: KnowledgeBases,
        meta: { title: 'Bases de Conocimiento - VersaAI' }
      },
      {
        path: 'knowledge-bases/:id',
        name: 'KnowledgeBaseDetail',
        component: KnowledgeBaseDetail,
        meta: { title: 'Detalle Base de Conocimiento - VersaAI' }
      },
      
      // Analytics
      {
        path: 'analytics',
        name: 'Analytics',
        component: Analytics,
        meta: { title: 'Analíticas - VersaAI' }
      },
      
      // Advanced Analytics
      {
        path: 'advanced-analytics',
        name: 'AdvancedAnalytics',
        component: () => import('@/components/dashboard/AdvancedAnalytics.vue'),
        meta: { 
          title: 'Analíticas Avanzadas - VersaAI',
          requiresRole: ['admin', 'manager', 'enterprise']
        }
      },
      
      // Organization Management
      {
        path: 'organizations',
        name: 'OrganizationManagement',
        component: OrganizationManagement,
        meta: { 
          title: 'Gestión de Organizaciones - VersaAI',
          requiresRole: ['admin', 'enterprise']
        }
      },
      
      // Integrations
      {
        path: 'integrations',
        name: 'Integrations',
        component: Integrations,
        meta: { 
          title: 'Integraciones - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      {
        path: 'integrations/hub',
        name: 'IntegrationsHub',
        component: () => import('@/views/IntegrationsHub.vue'),
        meta: { 
          title: 'Hub de Integraciones - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      {
        path: 'integrations/webhooks',
        name: 'WebhookManager',
        component: () => import('@/components/integrations/WebhookManager.vue'),
        meta: { 
          title: 'Gestión de Webhooks - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      {
        path: 'integrations/api-keys',
        name: 'APIKeyManager',
        component: () => import('@/components/integrations/APIKeyManager.vue'),
        meta: { 
          title: 'Gestión de API Keys - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      {
        path: 'integrations/slack',
        name: 'SlackIntegration',
        component: () => import('@/components/integrations/SlackIntegration.vue'),
        meta: { 
          title: 'Integración con Slack - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      
      // Security Center
      {
        path: 'security',
        name: 'SecurityCenter',
        component: SecurityCenter,
        meta: { 
          title: 'Centro de Seguridad - VersaAI',
          requiresRole: ['admin']
        }
      },
      
      // Widget Manager
      {
        path: 'widgets',
        name: 'WidgetManager',
        component: WidgetManager,
        meta: { 
          title: 'Gestión de Widgets - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      
      // Pricing
      {
        path: 'pricing',
        name: 'Pricing',
        component: Pricing,
        meta: { 
          title: 'Planes y Precios - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      
      // Customization
      {
        path: 'customization',
        name: 'Customization',
        component: () => import('@/components/dashboard/CustomizationSystem.vue'),
        meta: { 
          title: 'Personalización - VersaAI',
          requiresRole: ['admin', 'enterprise']
        }
      },
      
      // Users Management
      {
        path: 'users',
        name: 'Users',
        component: Users,
        meta: { 
          title: 'Gestión de Usuarios - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      },
      
      // Settings
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: { title: 'Configuración - VersaAI' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: { title: 'Perfil - VersaAI' }
      },
      {
        path: 'organization',
        name: 'Organization',
        component: Organization,
        meta: { 
          title: 'Organización - VersaAI',
          requiresRole: ['admin', 'manager']
        }
      }
    ]
  },

  // Mobile Routes
  {
    path: '/mobile',
    component: () => import('@/layouts/MobileLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'MobileDashboard',
        component: MobileDashboard,
        meta: { title: 'Dashboard Móvil - VersaAI' }
      }
    ]
  },

  // Development/Testing Routes
  {
    path: '/dev',
    component: PublicLayout,
    meta: { requiresAuth: false },
    children: [
      {
        path: 'examples',
        name: 'Examples',
        component: ExamplesView,
        meta: { title: 'Ejemplos - VersaAI Dev' }
      },
      {
        path: 'test',
        name: 'Test',
        component: TestPage,
        meta: { title: 'Pruebas - VersaAI Dev' }
      },
      {
        path: 'diagnostic',
        name: 'Diagnostic',
        component: DiagnosticPage,
        meta: { title: 'Diagnóstico - VersaAI Dev' }
      },
      {
        path: 'api-test',
        name: 'ApiTest',
        component: ApiTestingChat,
        meta: { title: 'Prueba API - VersaAI Dev' }
      },
      {
        path: 'integration-test',
        name: 'IntegrationTest',
        component: IntegrationTest,
        meta: { title: 'Prueba de Integración - VersaAI Dev' }
      }
    ]
  },

  // Error Routes
  {
    path: '/error',
    component: PublicLayout,
    children: [
      {
        path: '500',
        name: 'ServerError',
        component: ServerError,
        meta: { title: 'Error del Servidor - VersaAI' }
      },
      {
        path: '401',
        name: 'Unauthorized',
        component: Unauthorized,
        meta: { title: 'No Autorizado - VersaAI' }
      }
    ]
  },

  // Catch all 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Página no encontrada - VersaAI' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Try to restore session from localStorage
      await authStore.checkAuth()
      
      if (!authStore.isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
        return
      }
    }
    
    // Check role requirements
    if (to.meta.requiresRole) {
      const userRole = authStore.user?.role
      if (!userRole || !to.meta.requiresRole.includes(userRole)) {
        next({ name: 'Unauthorized' })
        return
      }
    }
  }
  
  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }
  
  next()
})

// Global error handler
router.onError((error) => {
  console.error('Router error:', error)
  // You could redirect to an error page here
})

export default router