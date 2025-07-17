# 💼 PLAN DE IMPLEMENTACIÓN - SEMANA 2
## Funcionalidades Empresariales VersaAI

---

## 📋 OVERVIEW SEMANA 2

**Objetivo:** Implementar funcionalidades empresariales críticas para monetización inmediata
**Duración:** 7 días
**Enfoque:** Revenue Generation + Enterprise Features
**Resultado Esperado:** Plataforma lista para clientes empresariales y monetización

---

## 🎯 FUNCIONALIDADES CRÍTICAS

### 💼 Dashboard Empresarial
- Panel de métricas en tiempo real
- KPIs empresariales
- Gestión de equipos y roles
- Reportes exportables

### 💰 Sistema de Monetización
- Planes y precios dinámicos
- Gestión de suscripciones
- Pasarela de pagos
- Dashboard de facturación

### 🏢 Integraciones Empresariales
- SSO (Single Sign-On)
- APIs de terceros
- Webhooks
- Conectores CRM

### 🔧 Widget Embebible
- Chat widget independiente
- Configurador visual
- SDK para desarrolladores
- Personalización de marca

---

## 📅 CRONOGRAMA DETALLADO

### 💼 DÍA 1-3: DASHBOARD EMPRESARIAL

#### 📊 Día 1: Métricas en Tiempo Real

##### 1. Store de Analytics Empresarial
```typescript
// src/stores/analytics.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

interface MetricData {
  label: string
  value: number
  change: number
  trend: 'up' | 'down' | 'stable'
}

interface ChartData {
  labels: string[]
  datasets: {
    label: string
    data: number[]
    borderColor: string
    backgroundColor: string
  }[]
}

export const useAnalyticsStore = defineStore('analytics', () => {
  const metrics = ref<MetricData[]>([])
  const chartData = ref<ChartData | null>(null)
  const loading = ref(false)
  const dateRange = ref({ start: '', end: '' })

  const totalUsers = computed(() => 
    metrics.value.find(m => m.label === 'Total Users')?.value || 0
  )
  
  const activeConversations = computed(() => 
    metrics.value.find(m => m.label === 'Active Conversations')?.value || 0
  )
  
  const revenue = computed(() => 
    metrics.value.find(m => m.label === 'Monthly Revenue')?.value || 0
  )

  const fetchMetrics = async (range?: { start: string; end: string }) => {
    loading.value = true
    try {
      const params = range || dateRange.value
      const response = await api.get('/analytics/enterprise-metrics', { params })
      metrics.value = response.data.metrics
      chartData.value = response.data.chartData
    } catch (error) {
      console.error('Error fetching metrics:', error)
    } finally {
      loading.value = false
    }
  }

  const exportReport = async (format: 'pdf' | 'excel') => {
    try {
      const response = await api.post('/analytics/export', {
        format,
        dateRange: dateRange.value,
        metrics: metrics.value
      }, { responseType: 'blob' })
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `analytics-report.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error exporting report:', error)
    }
  }

  return {
    metrics,
    chartData,
    loading,
    dateRange,
    totalUsers,
    activeConversations,
    revenue,
    fetchMetrics,
    exportReport
  }
})
```

##### 2. Componente de Métricas
```vue
<!-- src/components/dashboard/MetricsGrid.vue -->
<template>
  <div class="metrics-grid">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <MetricCard
        v-for="metric in metrics"
        :key="metric.label"
        :metric="metric"
        :loading="loading"
      />
    </div>
    
    <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
      <ChartCard
        title="Conversaciones por Día"
        :chart-data="conversationChart"
        type="line"
      />
      <ChartCard
        title="Revenue Mensual"
        :chart-data="revenueChart"
        type="bar"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import MetricCard from './MetricCard.vue'
import ChartCard from './ChartCard.vue'

const analyticsStore = useAnalyticsStore()
const { metrics, loading, fetchMetrics } = analyticsStore

const conversationChart = computed(() => ({
  labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  datasets: [{
    label: 'Conversaciones',
    data: [120, 190, 300, 500, 200, 300, 450],
    borderColor: 'rgb(59, 130, 246)',
    backgroundColor: 'rgba(59, 130, 246, 0.1)'
  }]
}))

const revenueChart = computed(() => ({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [{
    label: 'Revenue ($)',
    data: [1200, 1900, 3000, 5000, 2000, 3000],
    backgroundColor: 'rgba(34, 197, 94, 0.8)'
  }]
}))

onMounted(() => {
  fetchMetrics()
})
</script>
```

#### 👥 Día 2: Gestión de Equipos

##### 1. Store de Teams
```typescript
// src/stores/teams.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

interface TeamMember {
  id: string
  name: string
  email: string
  role: 'admin' | 'manager' | 'agent' | 'viewer'
  avatar?: string
  lastActive: string
  status: 'active' | 'inactive' | 'pending'
}

interface Team {
  id: string
  name: string
  description: string
  members: TeamMember[]
  permissions: string[]
  createdAt: string
}

export const useTeamsStore = defineStore('teams', () => {
  const teams = ref<Team[]>([])
  const currentTeam = ref<Team | null>(null)
  const loading = ref(false)

  const fetchTeams = async () => {
    loading.value = true
    try {
      const response = await api.get('/teams')
      teams.value = response.data
    } catch (error) {
      console.error('Error fetching teams:', error)
    } finally {
      loading.value = false
    }
  }

  const createTeam = async (teamData: Partial<Team>) => {
    try {
      const response = await api.post('/teams', teamData)
      teams.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Error creating team:', error)
      throw error
    }
  }

  const inviteMember = async (teamId: string, email: string, role: string) => {
    try {
      const response = await api.post(`/teams/${teamId}/invite`, { email, role })
      const team = teams.value.find(t => t.id === teamId)
      if (team) {
        team.members.push(response.data)
      }
      return response.data
    } catch (error) {
      console.error('Error inviting member:', error)
      throw error
    }
  }

  const updateMemberRole = async (teamId: string, memberId: string, role: string) => {
    try {
      await api.patch(`/teams/${teamId}/members/${memberId}`, { role })
      const team = teams.value.find(t => t.id === teamId)
      if (team) {
        const member = team.members.find(m => m.id === memberId)
        if (member) {
          member.role = role as TeamMember['role']
        }
      }
    } catch (error) {
      console.error('Error updating member role:', error)
      throw error
    }
  }

  return {
    teams,
    currentTeam,
    loading,
    fetchTeams,
    createTeam,
    inviteMember,
    updateMemberRole
  }
})
```

#### 📈 Día 3: Reportes Exportables

##### 1. Componente de Reportes
```vue
<!-- src/components/dashboard/ReportsPanel.vue -->
<template>
  <div class="reports-panel">
    <div class="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700">
      <div class="p-6 border-b border-gray-200 dark:border-dark-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Generar Reportes
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Exporta datos y métricas en diferentes formatos
        </p>
      </div>
      
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Configuración de Reporte -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Tipo de Reporte
              </label>
              <select v-model="reportConfig.type" class="input">
                <option value="analytics">Analytics Completo</option>
                <option value="conversations">Conversaciones</option>
                <option value="users">Usuarios</option>
                <option value="revenue">Revenue</option>
                <option value="performance">Performance</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Rango de Fechas
              </label>
              <div class="grid grid-cols-2 gap-2">
                <input
                  v-model="reportConfig.startDate"
                  type="date"
                  class="input"
                />
                <input
                  v-model="reportConfig.endDate"
                  type="date"
                  class="input"
                />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Formato
              </label>
              <div class="flex space-x-4">
                <label class="flex items-center">
                  <input
                    v-model="reportConfig.format"
                    type="radio"
                    value="pdf"
                    class="mr-2"
                  />
                  PDF
                </label>
                <label class="flex items-center">
                  <input
                    v-model="reportConfig.format"
                    type="radio"
                    value="excel"
                    class="mr-2"
                  />
                  Excel
                </label>
                <label class="flex items-center">
                  <input
                    v-model="reportConfig.format"
                    type="radio"
                    value="csv"
                    class="mr-2"
                  />
                  CSV
                </label>
              </div>
            </div>
          </div>
          
          <!-- Preview -->
          <div class="bg-gray-50 dark:bg-dark-900 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 dark:text-white mb-3">
              Vista Previa
            </h4>
            <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <div>Tipo: {{ reportConfig.type }}</div>
              <div>Período: {{ formatDateRange }}</div>
              <div>Formato: {{ reportConfig.format.toUpperCase() }}</div>
              <div>Estimado: {{ estimatedSize }}</div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end space-x-3">
          <button
            @click="generatePreview"
            class="btn-secondary"
            :disabled="generating"
          >
            Vista Previa
          </button>
          <button
            @click="generateReport"
            class="btn-primary"
            :disabled="generating || !isValidConfig"
          >
            <LoadingSpinner v-if="generating" size="sm" color="white" class="mr-2" />
            Generar Reporte
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const analyticsStore = useAnalyticsStore()
const generating = ref(false)

const reportConfig = ref({
  type: 'analytics',
  startDate: '',
  endDate: '',
  format: 'pdf'
})

const formatDateRange = computed(() => {
  if (!reportConfig.value.startDate || !reportConfig.value.endDate) {
    return 'No seleccionado'
  }
  return `${reportConfig.value.startDate} - ${reportConfig.value.endDate}`
})

const estimatedSize = computed(() => {
  const sizes = {
    pdf: '2-5 MB',
    excel: '1-3 MB',
    csv: '500KB - 1MB'
  }
  return sizes[reportConfig.value.format] || 'Desconocido'
})

const isValidConfig = computed(() => {
  return reportConfig.value.startDate && 
         reportConfig.value.endDate && 
         reportConfig.value.type && 
         reportConfig.value.format
})

const generatePreview = async () => {
  // Implementar vista previa
}

const generateReport = async () => {
  generating.value = true
  try {
    await analyticsStore.exportReport(reportConfig.value.format)
  } catch (error) {
    console.error('Error generating report:', error)
  } finally {
    generating.value = false
  }
}
</script>
```

---

### 💰 DÍA 4-5: SISTEMA DE MONETIZACIÓN

#### 💳 Día 4: Planes y Precios

##### 1. Store de Billing
```typescript
// src/stores/billing.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

interface Plan {
  id: string
  name: string
  description: string
  price: number
  interval: 'month' | 'year'
  features: string[]
  limits: {
    conversations: number
    users: number
    storage: number // GB
    apiCalls: number
  }
  popular?: boolean
  enterprise?: boolean
}

interface Subscription {
  id: string
  planId: string
  status: 'active' | 'canceled' | 'past_due' | 'trialing'
  currentPeriodStart: string
  currentPeriodEnd: string
  cancelAtPeriodEnd: boolean
}

export const useBillingStore = defineStore('billing', () => {
  const plans = ref<Plan[]>([])
  const currentSubscription = ref<Subscription | null>(null)
  const loading = ref(false)

  const activePlan = computed(() => {
    if (!currentSubscription.value) return null
    return plans.value.find(p => p.id === currentSubscription.value?.planId)
  })

  const fetchPlans = async () => {
    loading.value = true
    try {
      const response = await api.get('/billing/plans')
      plans.value = response.data
    } catch (error) {
      console.error('Error fetching plans:', error)
    } finally {
      loading.value = false
    }
  }

  const fetchSubscription = async () => {
    try {
      const response = await api.get('/billing/subscription')
      currentSubscription.value = response.data
    } catch (error) {
      console.error('Error fetching subscription:', error)
    }
  }

  const subscribeToPlan = async (planId: string, paymentMethodId: string) => {
    try {
      const response = await api.post('/billing/subscribe', {
        planId,
        paymentMethodId
      })
      currentSubscription.value = response.data
      return response.data
    } catch (error) {
      console.error('Error subscribing to plan:', error)
      throw error
    }
  }

  const cancelSubscription = async () => {
    try {
      await api.post('/billing/cancel')
      if (currentSubscription.value) {
        currentSubscription.value.cancelAtPeriodEnd = true
      }
    } catch (error) {
      console.error('Error canceling subscription:', error)
      throw error
    }
  }

  return {
    plans,
    currentSubscription,
    loading,
    activePlan,
    fetchPlans,
    fetchSubscription,
    subscribeToPlan,
    cancelSubscription
  }
})
```

##### 2. Componente de Pricing
```vue
<!-- src/views/Pricing.vue -->
<template>
  <div class="pricing-page">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Planes que se adaptan a tu negocio
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Desde startups hasta empresas, tenemos el plan perfecto para potenciar tu IA conversacional
        </p>
        
        <!-- Toggle Anual/Mensual -->
        <div class="mt-8 flex justify-center">
          <div class="bg-gray-100 dark:bg-dark-800 p-1 rounded-lg">
            <button
              @click="billingInterval = 'month'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingInterval === 'month'
                  ? 'bg-white dark:bg-dark-700 text-gray-900 dark:text-white shadow-sm'
                  : 'text-gray-500 dark:text-gray-400'
              ]"
            >
              Mensual
            </button>
            <button
              @click="billingInterval = 'year'"
              :class="[
                'px-4 py-2 rounded-md text-sm font-medium transition-colors',
                billingInterval === 'year'
                  ? 'bg-white dark:bg-dark-700 text-gray-900 dark:text-white shadow-sm'
                  : 'text-gray-500 dark:text-gray-400'
              ]"
            >
              Anual
              <span class="ml-1 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                -20%
              </span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Plans Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <PlanCard
          v-for="plan in filteredPlans"
          :key="plan.id"
          :plan="plan"
          :current="activePlan?.id === plan.id"
          @select="selectPlan"
        />
      </div>
      
      <!-- Enterprise CTA -->
      <div class="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl p-8 text-center text-white">
        <h3 class="text-2xl font-bold mb-4">¿Necesitas algo más personalizado?</h3>
        <p class="text-lg mb-6 opacity-90">
          Nuestro plan Enterprise incluye integraciones personalizadas, soporte dedicado y SLA garantizado
        </p>
        <button class="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
          Contactar Ventas
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBillingStore } from '@/stores/billing'
import PlanCard from '@/components/billing/PlanCard.vue'

const billingStore = useBillingStore()
const { plans, activePlan, fetchPlans, subscribeToPlan } = billingStore

const billingInterval = ref('month')

const filteredPlans = computed(() => {
  return plans.value.filter(plan => 
    plan.interval === billingInterval.value && !plan.enterprise
  )
})

const selectPlan = async (planId: string) => {
  try {
    // Redirigir a checkout o abrir modal de pago
    await subscribeToPlan(planId, 'payment_method_id')
  } catch (error) {
    console.error('Error selecting plan:', error)
  }
}

onMounted(() => {
  fetchPlans()
})
</script>
```

#### 💳 Día 5: Integración de Pagos

##### 1. Componente de Checkout
```vue
<!-- src/components/billing/CheckoutModal.vue -->
<template>
  <Modal v-model="isOpen" size="lg">
    <div class="checkout-modal">
      <div class="p-6 border-b border-gray-200 dark:border-dark-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Completar Suscripción
        </h3>
      </div>
      
      <div class="p-6">
        <!-- Plan Summary -->
        <div class="bg-gray-50 dark:bg-dark-900 rounded-lg p-4 mb-6">
          <div class="flex justify-between items-center">
            <div>
              <h4 class="font-medium text-gray-900 dark:text-white">{{ selectedPlan?.name }}</h4>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedPlan?.description }}</p>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-gray-900 dark:text-white">
                ${{ selectedPlan?.price }}
              </div>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                /{{ selectedPlan?.interval === 'month' ? 'mes' : 'año' }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Payment Form -->
        <form @submit.prevent="processPayment">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Información de Facturación
              </label>
              <div class="grid grid-cols-2 gap-4">
                <input
                  v-model="billingInfo.firstName"
                  type="text"
                  placeholder="Nombre"
                  class="input"
                  required
                />
                <input
                  v-model="billingInfo.lastName"
                  type="text"
                  placeholder="Apellido"
                  class="input"
                  required
                />
              </div>
              <input
                v-model="billingInfo.email"
                type="email"
                placeholder="Email"
                class="input mt-2"
                required
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Método de Pago
              </label>
              <div class="border border-gray-300 dark:border-dark-600 rounded-lg p-4">
                <!-- Stripe Elements se montará aquí -->
                <div id="card-element" class="stripe-element"></div>
                <div id="card-errors" class="text-red-500 text-sm mt-2"></div>
              </div>
            </div>
            
            <div class="flex items-center">
              <input
                v-model="acceptTerms"
                type="checkbox"
                id="terms"
                class="mr-2"
                required
              />
              <label for="terms" class="text-sm text-gray-600 dark:text-gray-400">
                Acepto los 
                <a href="/terms" class="text-primary-600 hover:underline">términos y condiciones</a>
                y la 
                <a href="/privacy" class="text-primary-600 hover:underline">política de privacidad</a>
              </label>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              @click="$emit('close')"
              class="btn-secondary"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="processing || !acceptTerms"
            >
              <LoadingSpinner v-if="processing" size="sm" color="white" class="mr-2" />
              Suscribirse (${{ selectedPlan?.price }}/{{ selectedPlan?.interval === 'month' ? 'mes' : 'año' }})
            </button>
          </div>
        </form>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import Modal from '@/components/ui/Modal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const props = defineProps({
  isOpen: Boolean,
  selectedPlan: Object
})

const emit = defineEmits(['close', 'success'])

const stripe = ref(null)
const elements = ref(null)
const cardElement = ref(null)
const processing = ref(false)
const acceptTerms = ref(false)

const billingInfo = ref({
  firstName: '',
  lastName: '',
  email: ''
})

const initializeStripe = async () => {
  stripe.value = await loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)
  elements.value = stripe.value.elements()
  
  cardElement.value = elements.value.create('card', {
    style: {
      base: {
        fontSize: '16px',
        color: '#424770',
        '::placeholder': {
          color: '#aab7c4',
        },
      },
    },
  })
  
  cardElement.value.mount('#card-element')
  
  cardElement.value.on('change', (event) => {
    const displayError = document.getElementById('card-errors')
    if (event.error) {
      displayError.textContent = event.error.message
    } else {
      displayError.textContent = ''
    }
  })
}

const processPayment = async () => {
  processing.value = true
  
  try {
    const { error, paymentMethod } = await stripe.value.createPaymentMethod({
      type: 'card',
      card: cardElement.value,
      billing_details: {
        name: `${billingInfo.value.firstName} ${billingInfo.value.lastName}`,
        email: billingInfo.value.email,
      },
    })
    
    if (error) {
      console.error('Payment method creation failed:', error)
      return
    }
    
    // Procesar suscripción en el backend
    const response = await api.post('/billing/create-subscription', {
      planId: props.selectedPlan.id,
      paymentMethodId: paymentMethod.id,
      billingInfo: billingInfo.value
    })
    
    emit('success', response.data)
    emit('close')
  } catch (error) {
    console.error('Payment processing failed:', error)
  } finally {
    processing.value = false
  }
}

watch(() => props.isOpen, (newValue) => {
  if (newValue && !stripe.value) {
    initializeStripe()
  }
})

onMounted(() => {
  if (props.isOpen) {
    initializeStripe()
  }
})
</script>
```

---

### 🔧 DÍA 6-7: WIDGET EMBEBIBLE

#### 🎨 Día 6: Chat Widget Independiente

##### 1. Widget Principal
```vue
<!-- src/widget/ChatWidget.vue -->
<template>
  <div class="chat-widget" :class="widgetClasses">
    <!-- Widget Button -->
    <button
      v-if="!isOpen"
      @click="toggleWidget"
      class="widget-button"
      :style="buttonStyles"
    >
      <ChatBubbleLeftRightIcon class="w-6 h-6" />
      <span v-if="unreadCount > 0" class="unread-badge">
        {{ unreadCount }}
      </span>
    </button>
    
    <!-- Widget Container -->
    <div v-if="isOpen" class="widget-container" :style="containerStyles">
      <!-- Header -->
      <div class="widget-header" :style="headerStyles">
        <div class="flex items-center space-x-3">
          <img
            v-if="config.avatar"
            :src="config.avatar"
            :alt="config.name"
            class="w-8 h-8 rounded-full"
          />
          <div>
            <h3 class="font-medium text-white">{{ config.name || 'Asistente IA' }}</h3>
            <p class="text-xs text-white/80">{{ config.subtitle || 'En línea' }}</p>
          </div>
        </div>
        <button @click="toggleWidget" class="text-white/80 hover:text-white">
          <XMarkIcon class="w-5 h-5" />
        </button>
      </div>
      
      <!-- Messages -->
      <div class="widget-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="text-center p-4">
            <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <ChatBubbleLeftRightIcon class="w-6 h-6 text-primary-600" />
            </div>
            <h4 class="font-medium text-gray-900 mb-1">{{ config.welcomeTitle || '¡Hola!' }}</h4>
            <p class="text-sm text-gray-600">{{ config.welcomeMessage || '¿En qué puedo ayudarte hoy?' }}</p>
          </div>
        </div>
        
        <div
          v-for="message in messages"
          :key="message.id"
          class="message"
          :class="message.sender === 'user' ? 'user-message' : 'bot-message'"
        >
          <div class="message-content">
            <p>{{ message.content }}</p>
            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
          </div>
        </div>
        
        <div v-if="isTyping" class="typing-indicator">
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      
      <!-- Input -->
      <div class="widget-input">
        <div class="flex space-x-2 p-3 border-t border-gray-200">
          <input
            v-model="currentMessage"
            @keypress.enter="sendMessage"
            type="text"
            placeholder="Escribe tu mensaje..."
            class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            :disabled="isTyping"
          />
          <button
            @click="sendMessage"
            :disabled="!currentMessage.trim() || isTyping"
            class="bg-primary-600 text-white p-2 rounded-lg hover:bg-primary-700 disabled:opacity-50"
          >
            <PaperAirplaneIcon class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import {
  ChatBubbleLeftRightIcon,
  XMarkIcon,
  PaperAirplaneIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({})
  }
})

const isOpen = ref(false)
const messages = ref([])
const currentMessage = ref('')
const isTyping = ref(false)
const unreadCount = ref(0)
const messagesContainer = ref(null)

const widgetClasses = computed(() => ({
  'widget-bottom-right': props.config.position === 'bottom-right',
  'widget-bottom-left': props.config.position === 'bottom-left',
  'widget-top-right': props.config.position === 'top-right',
  'widget-top-left': props.config.position === 'top-left'
}))

const buttonStyles = computed(() => ({
  backgroundColor: props.config.primaryColor || '#3B82F6',
  color: props.config.textColor || '#FFFFFF'
}))

const headerStyles = computed(() => ({
  backgroundColor: props.config.primaryColor || '#3B82F6'
}))

const containerStyles = computed(() => ({
  width: props.config.width || '350px',
  height: props.config.height || '500px'
}))

const toggleWidget = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    unreadCount.value = 0
    nextTick(() => {
      scrollToBottom()
    })
  }
}

const sendMessage = async () => {
  if (!currentMessage.value.trim()) return
  
  const userMessage = {
    id: Date.now(),
    content: currentMessage.value,
    sender: 'user',
    timestamp: new Date()
  }
  
  messages.value.push(userMessage)
  const messageText = currentMessage.value
  currentMessage.value = ''
  
  scrollToBottom()
  
  // Simular respuesta del bot
  isTyping.value = true
  
  try {
    const response = await fetch(`${props.config.apiUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.config.apiKey}`
      },
      body: JSON.stringify({
        message: messageText,
        sessionId: props.config.sessionId
      })
    })
    
    const data = await response.json()
    
    const botMessage = {
      id: Date.now() + 1,
      content: data.response,
      sender: 'bot',
      timestamp: new Date()
    }
    
    messages.value.push(botMessage)
    
    if (!isOpen.value) {
      unreadCount.value++
    }
  } catch (error) {
    console.error('Error sending message:', error)
    const errorMessage = {
      id: Date.now() + 1,
      content: 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.',
      sender: 'bot',
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  // Inicializar widget con configuración
  if (props.config.autoOpen) {
    setTimeout(() => {
      isOpen.value = true
    }, props.config.autoOpenDelay || 3000)
  }
})
</script>

<style scoped>
.chat-widget {
  position: fixed;
  z-index: 9999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.widget-bottom-right {
  bottom: 20px;
  right: 20px;
}

.widget-bottom-left {
  bottom: 20px;
  left: 20px;
}

.widget-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
  position: relative;
}

.widget-button:hover {
  transform: scale(1.05);
}

.unread-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #EF4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.widget-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.widget-header {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.widget-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  max-height: 400px;
}

.message {
  margin-bottom: 12px;
}

.user-message {
  text-align: right;
}

.bot-message {
  text-align: left;
}

.message-content {
  display: inline-block;
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.4;
}

.user-message .message-content {
  background: #3B82F6;
  color: white;
}

.bot-message .message-content {
  background: #F3F4F6;
  color: #374151;
}

.message-time {
  display: block;
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
}

.typing-indicator {
  text-align: left;
  margin-bottom: 12px;
}

.typing-dots {
  display: inline-block;
  background: #F3F4F6;
  padding: 12px 16px;
  border-radius: 12px;
}

.typing-dots span {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #9CA3AF;
  margin: 0 2px;
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}
</style>
```

#### ⚙️ Día 7: SDK y Configurador

##### 1. SDK JavaScript
```javascript
// src/widget/sdk.js
class VersaAIWidget {
  constructor(config) {
    this.config = {
      apiUrl: 'https://api.versaai.com',
      position: 'bottom-right',
      primaryColor: '#3B82F6',
      textColor: '#FFFFFF',
      width: '350px',
      height: '500px',
      autoOpen: false,
      autoOpenDelay: 3000,
      name: 'Asistente IA',
      subtitle: 'En línea',
      welcomeTitle: '¡Hola!',
      welcomeMessage: '¿En qué puedo ayudarte hoy?',
      ...config
    }
    
    this.widget = null
    this.isLoaded = false
    
    this.init()
  }
  
  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.render())
    } else {
      this.render()
    }
  }
  
  render() {
    // Crear contenedor del widget
    const container = document.createElement('div')
    container.id = 'versaai-widget'
    document.body.appendChild(container)
    
    // Cargar estilos
    this.loadStyles()
    
    // Renderizar widget Vue
    this.renderVueWidget(container)
    
    this.isLoaded = true
  }
  
  loadStyles() {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = `${this.config.apiUrl}/widget/styles.css`
    document.head.appendChild(link)
  }
  
  renderVueWidget(container) {
    // Importar Vue y el componente del widget
    import('./ChatWidget.vue').then(({ default: ChatWidget }) => {
      const { createApp } = Vue
      
      const app = createApp(ChatWidget, {
        config: this.config
      })
      
      app.mount(container)
      this.widget = app
    })
  }
  
  // API pública
  open() {
    if (this.widget) {
      this.widget.isOpen = true
    }
  }
  
  close() {
    if (this.widget) {
      this.widget.isOpen = false
    }
  }
  
  toggle() {
    if (this.widget) {
      this.widget.toggleWidget()
    }
  }
  
  sendMessage(message) {
    if (this.widget) {
      this.widget.currentMessage = message
      this.widget.sendMessage()
    }
  }
  
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig }
    if (this.widget) {
      this.widget.config = this.config
    }
  }
  
  destroy() {
    if (this.widget) {
      this.widget.unmount()
      const container = document.getElementById('versaai-widget')
      if (container) {
        container.remove()
      }
    }
  }
}

// Función de inicialización global
window.VersaAI = {
  init: (config) => new VersaAIWidget(config)
}

// Auto-inicialización si hay configuración en el script
if (window.versaAIConfig) {
  window.VersaAI.widget = new VersaAIWidget(window.versaAIConfig)
}

export default VersaAIWidget
```

##### 2. Configurador Visual
```vue
<!-- src/views/WidgetConfigurator.vue -->
<template>
  <div class="widget-configurator">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Configuración -->
        <div class="space-y-6">
          <div class="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Configuración del Widget
            </h3>
            
            <!-- Apariencia -->
            <div class="space-y-4">
              <h4 class="font-medium text-gray-900 dark:text-white">Apariencia</h4>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Color Primario
                  </label>
                  <input
                    v-model="config.primaryColor"
                    type="color"
                    class="w-full h-10 border border-gray-300 rounded-md"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Posición
                  </label>
                  <select v-model="config.position" class="input">
                    <option value="bottom-right">Abajo Derecha</option>
                    <option value="bottom-left">Abajo Izquierda</option>
                    <option value="top-right">Arriba Derecha</option>
                    <option value="top-left">Arriba Izquierda</option>
                  </select>
                </div>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Ancho
                  </label>
                  <input
                    v-model="config.width"
                    type="text"
                    placeholder="350px"
                    class="input"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Alto
                  </label>
                  <input
                    v-model="config.height"
                    type="text"
                    placeholder="500px"
                    class="input"
                  />
                </div>
              </div>
            </div>
            
            <!-- Contenido -->
            <div class="space-y-4 mt-6">
              <h4 class="font-medium text-gray-900 dark:text-white">Contenido</h4>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Nombre del Asistente
                </label>
                <input
                  v-model="config.name"
                  type="text"
                  placeholder="Asistente IA"
                  class="input"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Mensaje de Bienvenida
                </label>
                <textarea
                  v-model="config.welcomeMessage"
                  placeholder="¿En qué puedo ayudarte hoy?"
                  class="input"
                  rows="3"
                ></textarea>
              </div>
            </div>
            
            <!-- Comportamiento -->
            <div class="space-y-4 mt-6">
              <h4 class="font-medium text-gray-900 dark:text-white">Comportamiento</h4>
              
              <div class="flex items-center">
                <input
                  v-model="config.autoOpen"
                  type="checkbox"
                  id="autoOpen"
                  class="mr-2"
                />
                <label for="autoOpen" class="text-sm text-gray-700 dark:text-gray-300">
                  Abrir automáticamente
                </label>
              </div>
              
              <div v-if="config.autoOpen">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Retraso (ms)
                </label>
                <input
                  v-model.number="config.autoOpenDelay"
                  type="number"
                  placeholder="3000"
                  class="input"
                />
              </div>
            </div>
          </div>
          
          <!-- Código de Integración -->
          <div class="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Código de Integración
            </h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  HTML
                </label>
                <textarea
                  :value="htmlCode"
                  readonly
                  class="input font-mono text-sm"
                  rows="8"
                ></textarea>
                <button
                  @click="copyToClipboard(htmlCode)"
                  class="mt-2 btn-secondary text-sm"
                >
                  Copiar HTML
                </button>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  JavaScript
                </label>
                <textarea
                  :value="jsCode"
                  readonly
                  class="input font-mono text-sm"
                  rows="6"
                ></textarea>
                <button
                  @click="copyToClipboard(jsCode)"
                  class="mt-2 btn-secondary text-sm"
                >
                  Copiar JavaScript
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Preview -->
        <div class="lg:sticky lg:top-8">
          <div class="bg-white dark:bg-dark-800 rounded-lg shadow-sm border border-gray-200 dark:border-dark-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Vista Previa
            </h3>
            
            <div class="relative bg-gray-100 dark:bg-dark-900 rounded-lg" style="height: 400px; overflow: hidden;">
              <!-- Simulación del widget -->
              <div
                class="absolute"
                :class="{
                  'bottom-4 right-4': config.position === 'bottom-right',
                  'bottom-4 left-4': config.position === 'bottom-left',
                  'top-4 right-4': config.position === 'top-right',
                  'top-4 left-4': config.position === 'top-left'
                }"
              >
                <button
                  class="w-12 h-12 rounded-full flex items-center justify-center shadow-lg"
                  :style="{ backgroundColor: config.primaryColor }"
                >
                  <ChatBubbleLeftRightIcon class="w-6 h-6 text-white" />
                </button>
              </div>
              
              <div class="absolute inset-4 text-center flex items-center justify-center">
                <div class="text-gray-500 dark:text-gray-400">
                  <p class="text-sm">Vista previa del widget</p>
                  <p class="text-xs mt-1">Posición: {{ config.position }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'

const config = ref({
  apiUrl: 'https://api.versaai.com',
  apiKey: 'your-api-key',
  position: 'bottom-right',
  primaryColor: '#3B82F6',
  width: '350px',
  height: '500px',
  autoOpen: false,
  autoOpenDelay: 3000,
  name: 'Asistente IA',
  welcomeMessage: '¿En qué puedo ayudarte hoy?'
})

const htmlCode = computed(() => `<!-- VersaAI Chat Widget -->
<script>
  window.versaAIConfig = ${JSON.stringify(config.value, null, 2)};
</script>
<script src="https://cdn.versaai.com/widget/v1/widget.js"></script>`)

const jsCode = computed(() => `// Inicialización programática
const widget = VersaAI.init(${JSON.stringify(config.value, null, 2)});

// API del widget
widget.open();     // Abrir widget
widget.close();    // Cerrar widget
widget.toggle();   // Alternar widget
widget.sendMessage('Hola'); // Enviar mensaje`)

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    // Mostrar notificación de éxito
    console.log('Código copiado al portapapeles')
  } catch (error) {
    console.error('Error copying to clipboard:', error)
  }
}
</script>
```

---

## 📊 MÉTRICAS DE SEGUIMIENTO SEMANA 2

### 🎯 KPIs por Funcionalidad

#### 💼 Dashboard Empresarial
- **Tiempo de carga:** < 2s
- **Métricas en tiempo real:** 100% funcional
- **Exportación de reportes:** PDF + Excel
- **Gestión de equipos:** CRUD completo

#### 💰 Sistema de Monetización
- **Conversión de checkout:** > 85%
- **Tiempo de procesamiento:** < 5s
- **Integración Stripe:** 100% funcional
- **Planes configurables:** Dinámicos

#### 🔧 Widget Embebible
- **Tiempo de carga:** < 1s
- **Compatibilidad:** 95% navegadores
- **Personalización:** 100% configurable
- **SDK funcional:** Documentado

### 📈 Herramientas de Monitoreo
```bash
# Scripts de validación
npm run test:enterprise     # Tests funcionalidades empresariales
npm run test:billing        # Tests sistema de pagos
npm run test:widget         # Tests widget embebible
npm run validate:api        # Validación APIs
```

---

## 🚀 ENTREGABLES SEMANA 2

### ✅ Funcionalidades Completadas
1. **Dashboard Empresarial completo**
   - Métricas en tiempo real
   - Gestión de equipos y roles
   - Reportes exportables
   - Analytics avanzados

2. **Sistema de Monetización funcional**
   - Planes y precios dinámicos
   - Checkout con Stripe
   - Gestión de suscripciones
   - Dashboard de facturación

3. **Widget Embebible listo**
   - Chat widget independiente
   - Configurador visual
   - SDK JavaScript
   - Documentación completa

4. **Integraciones Empresariales básicas**
   - API endpoints preparados
   - Estructura para SSO
   - Webhooks configurables

### 📋 Documentación Entregada
- Guía de integración del widget
- API documentation
- Manual de configuración empresarial
- Guía de monetización

---

## 🎯 OBJETIVOS DE REVENUE

### 💰 Modelo de Monetización Implementado

#### Planes de Suscripción
- **Starter:** $29/mes - Pequeñas empresas
- **Professional:** $99/mes - Empresas medianas
- **Enterprise:** $299/mes - Grandes empresas
- **Custom:** Precio personalizado

#### Métricas de Conversión Esperadas
- **Free to Paid:** 15-20%
- **Trial to Paid:** 25-30%
- **Churn Rate:** < 5% mensual
- **LTV/CAC Ratio:** > 3:1

### 📈 Proyección de Ingresos (30 días)
- **Mes 1:** $5,000 - $10,000
- **Mes 2:** $15,000 - $25,000
- **Mes 3:** $30,000 - $50,000
- **Mes 6:** $100,000+ MRR

---

## 🔄 PLAN DE MIGRACIÓN GRADUAL

### 🎯 Fases Futuras (Post-Semana 2)

#### Fase 3: Optimización y Escalabilidad (Semanas 3-4)
- Optimización de performance
- Escalabilidad de infraestructura
- A/B testing de conversión
- Analytics avanzados

#### Fase 4: Funcionalidades Avanzadas (Semanas 5-8)
- SSO completo (SAML, OAuth)
- Integraciones CRM (Salesforce, HubSpot)
- API marketplace
- White-label solutions

#### Fase 5: Migración a Next.js (Opcional - Meses 3-6)
- Migración gradual por módulos
- Mantenimiento de funcionalidad
- Optimización SEO
- Server-side rendering

---

## ✅ CHECKLIST FINAL SEMANA 2

### 🔍 Validación Técnica
- [ ] Dashboard empresarial 100% funcional
- [ ] Sistema de pagos integrado y probado
- [ ] Widget embebible desplegado
- [ ] APIs documentadas y probadas
- [ ] Tests automatizados pasando
- [ ] Performance optimizado
- [ ] Seguridad validada
- [ ] Documentación completa

### 💼 Validación de Negocio
- [ ] Planes de precios configurados
- [ ] Proceso de checkout optimizado
- [ ] Métricas de conversión implementadas
- [ ] Dashboard de analytics funcional
- [ ] Reportes empresariales disponibles
- [ ] Widget personalizable
- [ ] SDK documentado
- [ ] Soporte técnico preparado

### 🚀 Preparación para Lanzamiento
- [ ] Entorno de producción configurado
- [ ] Monitoreo y alertas activos
- [ ] Backup y recuperación probados
- [ ] Escalabilidad validada
- [ ] Equipo de soporte entrenado
- [ ] Materiales de marketing preparados
- [ ] Estrategia de lanzamiento definida
- [ ] Métricas de éxito establecidas

---

## 🎉 RESULTADO ESPERADO

**Al final de la Semana 2, VersaAI será una plataforma empresarial completa y lista para monetización, con:**

✅ **Frontend optimizado** (Semana 1)
✅ **Funcionalidades empresariales** (Semana 2)
✅ **Sistema de monetización funcional**
✅ **Widget embebible listo para distribución**
✅ **APIs empresariales documentadas**
✅ **Métricas y analytics implementados**
✅ **Documentación completa**
✅ **Preparado para generar revenue inmediato**

**🎯 Objetivo Final:** Plataforma lista para clientes empresariales y generación de ingresos recurrentes desde el primer mes.

---

**📅 Cronograma Total:** 14 días
**💰 Inversión en Desarrollo:** 2 semanas
**📈 ROI Esperado:** 300%+ en 6 meses
**🚀 Time to Market:** Inmediato post-implementación