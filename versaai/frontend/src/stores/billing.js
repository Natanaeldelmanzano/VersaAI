import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useBillingStore = defineStore('billing', () => {
  // State
  const subscriptions = ref([])
  const plans = ref([])
  const transactions = ref([])
  const invoices = ref([])
  const paymentMethods = ref([])
  const billingSettings = ref({})
  const loading = ref(false)
  const error = ref(null)
  const revenueData = ref({
    monthly: 0,
    yearly: 0,
    growth: 0
  })
  const metrics = ref({
    arpu: 0,
    churnRate: 0,
    ltv: 0,
    mrr: 0,
    arr: 0
  })

  // Getters
  const activeSubscriptions = computed(() => 
    subscriptions.value.filter(s => s.status === 'active').length
  )

  const totalRevenue = computed(() => 
    transactions.value
      .filter(t => t.status === 'successful')
      .reduce((sum, t) => sum + t.amount, 0)
  )

  const monthlyRevenue = computed(() => {
    const now = new Date()
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    
    return transactions.value
      .filter(t => 
        t.status === 'successful' && 
        new Date(t.created_at) >= startOfMonth
      )
      .reduce((sum, t) => sum + t.amount, 0)
  })

  const pendingInvoices = computed(() => 
    invoices.value.filter(i => i.status === 'sent' || i.status === 'overdue').length
  )

  const overdueInvoices = computed(() => 
    invoices.value.filter(i => i.status === 'overdue').length
  )

  const recentTransactions = computed(() => 
    transactions.value
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, 10)
  )

  const subscriptionsByPlan = computed(() => {
    const planCounts = {}
    subscriptions.value.forEach(sub => {
      if (sub.status === 'active') {
        planCounts[sub.plan_id] = (planCounts[sub.plan_id] || 0) + 1
      }
    })
    
    return plans.value.map(plan => ({
      ...plan,
      subscribers: planCounts[plan.id] || 0
    }))
  })

  const revenueByPlan = computed(() => {
    const planRevenue = {}
    
    subscriptions.value.forEach(sub => {
      if (sub.status === 'active') {
        const plan = plans.value.find(p => p.id === sub.plan_id)
        if (plan) {
          planRevenue[plan.id] = (planRevenue[plan.id] || 0) + plan.price
        }
      }
    })
    
    return plans.value.map(plan => ({
      ...plan,
      revenue: planRevenue[plan.id] || 0
    }))
  })

  const billingStats = computed(() => ({
    totalSubscriptions: subscriptions.value.length,
    activeSubscriptions: activeSubscriptions.value,
    totalRevenue: totalRevenue.value,
    monthlyRevenue: monthlyRevenue.value,
    pendingInvoices: pendingInvoices.value,
    overdueInvoices: overdueInvoices.value,
    arpu: metrics.value.arpu,
    churnRate: metrics.value.churnRate,
    mrr: metrics.value.mrr,
    arr: metrics.value.arr
  }))

  // Actions
  const fetchSubscriptions = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/subscriptions')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      subscriptions.value = data.subscriptions || []
    } catch (err) {
      console.error('Error fetching subscriptions:', err)
      error.value = err.message
      
      // Fallback mock data
      subscriptions.value = [
        {
          id: 1,
          customer_id: 1,
          customer_name: 'Acme Corp',
          customer_email: 'billing@acme.com',
          plan_id: 2,
          plan_name: 'Profesional',
          status: 'active',
          current_period_start: '2024-01-01T00:00:00Z',
          current_period_end: '2024-02-01T00:00:00Z',
          created_at: '2024-01-01T00:00:00Z',
          trial_end: null,
          cancel_at_period_end: false
        },
        {
          id: 2,
          customer_id: 2,
          customer_name: 'TechStart Inc',
          customer_email: 'finance@techstart.com',
          plan_id: 3,
          plan_name: 'Empresarial',
          status: 'active',
          current_period_start: '2024-01-01T00:00:00Z',
          current_period_end: '2024-02-01T00:00:00Z',
          created_at: '2024-01-01T00:00:00Z',
          trial_end: null,
          cancel_at_period_end: false
        }
      ]
    } finally {
      loading.value = false
    }
  }

  const fetchPlans = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/plans')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      plans.value = data.plans || []
    } catch (err) {
      console.error('Error fetching plans:', err)
      error.value = err.message
      
      // Fallback mock data
      plans.value = [
        {
          id: 1,
          name: 'Básico',
          description: 'Plan básico para pequeñas empresas',
          price: 29.00,
          currency: 'USD',
          interval: 'month',
          interval_count: 1,
          status: 'active',
          features: [
            '5 chatbots',
            '1,000 conversaciones/mes',
            'Soporte por email',
            'Integraciones básicas'
          ],
          limits: {
            chatbots: 5,
            conversations: 1000,
            users: 3,
            storage: '1GB'
          },
          created_at: '2024-01-01T00:00:00Z'
        },
        {
          id: 2,
          name: 'Profesional',
          description: 'Plan profesional para empresas en crecimiento',
          price: 99.00,
          currency: 'USD',
          interval: 'month',
          interval_count: 1,
          status: 'active',
          features: [
            '25 chatbots',
            '10,000 conversaciones/mes',
            'Soporte prioritario',
            'Todas las integraciones',
            'Analytics avanzados'
          ],
          limits: {
            chatbots: 25,
            conversations: 10000,
            users: 10,
            storage: '10GB'
          },
          created_at: '2024-01-01T00:00:00Z'
        },
        {
          id: 3,
          name: 'Empresarial',
          description: 'Plan empresarial para grandes organizaciones',
          price: 299.00,
          currency: 'USD',
          interval: 'month',
          interval_count: 1,
          status: 'active',
          features: [
            'Chatbots ilimitados',
            'Conversaciones ilimitadas',
            'Soporte 24/7',
            'API personalizada',
            'Implementación dedicada'
          ],
          limits: {
            chatbots: -1, // unlimited
            conversations: -1, // unlimited
            users: -1, // unlimited
            storage: '100GB'
          },
          created_at: '2024-01-01T00:00:00Z'
        }
      ]
    } finally {
      loading.value = false
    }
  }

  const fetchTransactions = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/transactions')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      transactions.value = data.transactions || []
    } catch (err) {
      console.error('Error fetching transactions:', err)
      error.value = err.message
      
      // Fallback mock data
      transactions.value = [
        {
          id: 1,
          customer_id: 1,
          customer_name: 'Acme Corp',
          customer_email: 'billing@acme.com',
          subscription_id: 1,
          plan_id: 2,
          plan_name: 'Profesional',
          amount: 99.00,
          currency: 'USD',
          status: 'successful',
          payment_method: 'card',
          stripe_payment_intent_id: 'pi_1234567890',
          created_at: '2024-01-15T10:30:00Z',
          description: 'Suscripción mensual - Profesional'
        },
        {
          id: 2,
          customer_id: 2,
          customer_name: 'TechStart Inc',
          customer_email: 'finance@techstart.com',
          subscription_id: 2,
          plan_id: 3,
          plan_name: 'Empresarial',
          amount: 299.00,
          currency: 'USD',
          status: 'successful',
          payment_method: 'card',
          stripe_payment_intent_id: 'pi_0987654321',
          created_at: '2024-01-14T15:45:00Z',
          description: 'Suscripción mensual - Empresarial'
        },
        {
          id: 3,
          customer_id: 3,
          customer_name: 'Global Solutions',
          customer_email: 'payments@global.com',
          subscription_id: 3,
          plan_id: 1,
          plan_name: 'Básico',
          amount: 29.00,
          currency: 'USD',
          status: 'failed',
          payment_method: 'card',
          stripe_payment_intent_id: 'pi_1122334455',
          created_at: '2024-01-13T09:15:00Z',
          description: 'Suscripción mensual - Básico',
          failure_reason: 'Tarjeta declinada'
        }
      ]
    } finally {
      loading.value = false
    }
  }

  const fetchInvoices = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/invoices')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      invoices.value = data.invoices || []
    } catch (err) {
      console.error('Error fetching invoices:', err)
      error.value = err.message
      
      // Fallback mock data
      invoices.value = [
        {
          id: 1,
          number: 'INV-2024-001',
          customer_id: 1,
          customer_name: 'Acme Corp',
          customer_email: 'billing@acme.com',
          subscription_id: 1,
          amount: 99.00,
          currency: 'USD',
          status: 'paid',
          due_date: '2024-02-01T00:00:00Z',
          paid_at: '2024-01-15T10:30:00Z',
          created_at: '2024-01-15T10:30:00Z',
          stripe_invoice_id: 'in_1234567890',
          pdf_url: '/invoices/INV-2024-001.pdf'
        },
        {
          id: 2,
          number: 'INV-2024-002',
          customer_id: 2,
          customer_name: 'TechStart Inc',
          customer_email: 'finance@techstart.com',
          subscription_id: 2,
          amount: 299.00,
          currency: 'USD',
          status: 'paid',
          due_date: '2024-02-01T00:00:00Z',
          paid_at: '2024-01-14T15:45:00Z',
          created_at: '2024-01-14T15:45:00Z',
          stripe_invoice_id: 'in_0987654321',
          pdf_url: '/invoices/INV-2024-002.pdf'
        },
        {
          id: 3,
          number: 'INV-2024-003',
          customer_id: 3,
          customer_name: 'Global Solutions',
          customer_email: 'payments@global.com',
          subscription_id: 3,
          amount: 29.00,
          currency: 'USD',
          status: 'overdue',
          due_date: '2024-01-20T00:00:00Z',
          paid_at: null,
          created_at: '2024-01-13T09:15:00Z',
          stripe_invoice_id: 'in_1122334455',
          pdf_url: '/invoices/INV-2024-003.pdf'
        }
      ]
    } finally {
      loading.value = false
    }
  }

  const fetchMetrics = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/metrics')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      metrics.value = data.metrics || {}
      revenueData.value = data.revenue || {}
    } catch (err) {
      console.error('Error fetching metrics:', err)
      error.value = err.message
      
      // Fallback mock data
      metrics.value = {
        arpu: 142.33,
        churnRate: 2.3,
        ltv: 1420.50,
        mrr: 45000,
        arr: 540000
      }
      
      revenueData.value = {
        monthly: 45000,
        yearly: 540000,
        growth: 12.5
      }
    } finally {
      loading.value = false
    }
  }

  const createSubscription = async (subscriptionData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/subscriptions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(subscriptionData)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const newSubscription = await response.json()
      subscriptions.value.push(newSubscription)
      
      return newSubscription
    } catch (err) {
      console.error('Error creating subscription:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateSubscription = async (subscriptionId, updates) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/billing/subscriptions/${subscriptionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const updatedSubscription = await response.json()
      const index = subscriptions.value.findIndex(s => s.id === subscriptionId)
      
      if (index !== -1) {
        subscriptions.value[index] = updatedSubscription
      }
      
      return updatedSubscription
    } catch (err) {
      console.error('Error updating subscription:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const cancelSubscription = async (subscriptionId, cancelAtPeriodEnd = true) => {
    return await updateSubscription(subscriptionId, {
      cancel_at_period_end: cancelAtPeriodEnd
    })
  }

  const createPlan = async (planData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/billing/plans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(planData)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const newPlan = await response.json()
      plans.value.push(newPlan)
      
      return newPlan
    } catch (err) {
      console.error('Error creating plan:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const updatePlan = async (planId, updates) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/billing/plans/${planId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const updatedPlan = await response.json()
      const index = plans.value.findIndex(p => p.id === planId)
      
      if (index !== -1) {
        plans.value[index] = updatedPlan
      }
      
      return updatedPlan
    } catch (err) {
      console.error('Error updating plan:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const retryFailedTransaction = async (transactionId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/billing/transactions/${transactionId}/retry`, {
        method: 'POST'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const retriedTransaction = await response.json()
      const index = transactions.value.findIndex(t => t.id === transactionId)
      
      if (index !== -1) {
        transactions.value[index] = retriedTransaction
      }
      
      return retriedTransaction
    } catch (err) {
      console.error('Error retrying transaction:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const downloadInvoice = async (invoiceId) => {
    try {
      const response = await fetch(`/api/v1/billing/invoices/${invoiceId}/download`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      
      const invoice = invoices.value.find(i => i.id === invoiceId)
      a.download = `${invoice?.number || `invoice-${invoiceId}`}.pdf`
      
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      return true
    } catch (err) {
      console.error('Error downloading invoice:', err)
      error.value = err.message
      return false
    }
  }

  const sendInvoice = async (invoiceId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/billing/invoices/${invoiceId}/send`, {
        method: 'POST'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      
      // Update invoice status
      const index = invoices.value.findIndex(i => i.id === invoiceId)
      if (index !== -1) {
        invoices.value[index].status = 'sent'
      }
      
      return result
    } catch (err) {
      console.error('Error sending invoice:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const exportBillingData = async (format = 'csv', dateRange = {}) => {
    try {
      const params = new URLSearchParams({
        format,
        ...dateRange
      })
      
      const response = await fetch(`/api/v1/billing/export?${params}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `billing_export_${new Date().toISOString().split('T')[0]}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      return true
    } catch (err) {
      console.error('Error exporting billing data:', err)
      error.value = err.message
      return false
    }
  }

  const initializeBilling = async () => {
    await Promise.all([
      fetchPlans(),
      fetchSubscriptions(),
      fetchTransactions(),
      fetchInvoices(),
      fetchMetrics()
    ])
  }

  return {
    // State
    subscriptions,
    plans,
    transactions,
    invoices,
    paymentMethods,
    billingSettings,
    loading,
    error,
    revenueData,
    metrics,
    
    // Getters
    activeSubscriptions,
    totalRevenue,
    monthlyRevenue,
    pendingInvoices,
    overdueInvoices,
    recentTransactions,
    subscriptionsByPlan,
    revenueByPlan,
    billingStats,
    
    // Actions
    fetchSubscriptions,
    fetchPlans,
    fetchTransactions,
    fetchInvoices,
    fetchMetrics,
    createSubscription,
    updateSubscription,
    cancelSubscription,
    createPlan,
    updatePlan,
    retryFailedTransaction,
    downloadInvoice,
    sendInvoice,
    exportBillingData,
    initializeBilling
  }
})