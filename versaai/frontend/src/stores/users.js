import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useUsersStore = defineStore('users', () => {
  // State
  const users = ref([])
  const currentUser = ref(null)
  const userProfile = ref(null)
  const invitations = ref([])
  
  const isLoading = ref(false)
  const isCreating = ref(false)
  const isUpdating = ref(false)
  const isDeleting = ref(false)
  const isSendingInvitation = ref(false)
  
  const pagination = ref({
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 0
  })
  
  const filters = ref({
    search: '',
    role: '',
    status: '',
    sort_by: 'created_at',
    sort_order: 'desc'
  })
  
  const statistics = ref({
    total_users: 0,
    active_users: 0,
    pending_users: 0,
    admin_users: 0,
    recent_registrations: 0,
    growth_rate: 0
  })
  
  const toast = useToast()

  // Getters
  const hasUsers = computed(() => users.value.length > 0)
  
  const activeUsers = computed(() => {
    return users.value.filter(user => user.status === 'active')
  })
  
  const pendingUsers = computed(() => {
    return users.value.filter(user => user.status === 'pending')
  })
  
  const adminUsers = computed(() => {
    return users.value.filter(user => user.role === 'admin')
  })
  
  const filteredUsers = computed(() => {
    let filtered = [...users.value]
    
    // Apply search filter
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      filtered = filtered.filter(user => 
        user.name?.toLowerCase().includes(search) ||
        user.email?.toLowerCase().includes(search)
      )
    }
    
    // Apply role filter
    if (filters.value.role) {
      filtered = filtered.filter(user => user.role === filters.value.role)
    }
    
    // Apply status filter
    if (filters.value.status) {
      filtered = filtered.filter(user => user.status === filters.value.status)
    }
    
    return filtered
  })
  
  const hasNextPage = computed(() => {
    return pagination.value.page < pagination.value.totalPages
  })
  
  const hasPrevPage = computed(() => {
    return pagination.value.page > 1
  })

  // Actions
  const fetchUsers = async (params = {}) => {
    try {
      isLoading.value = true
      
      const queryParams = {
        page: pagination.value.page,
        limit: pagination.value.limit,
        ...filters.value,
        ...params
      }
      
      // Remove empty values
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === '' || queryParams[key] === null) {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/users', {
        params: queryParams
      })
      
      users.value = response.data.items || response.data
      
      if (response.data.pagination) {
        pagination.value = {
          ...pagination.value,
          ...response.data.pagination
        }
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch users error:', error)
      const message = error.response?.data?.detail || 'Error al cargar los usuarios'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchUser = async (userId) => {
    try {
      const response = await axios.get(`/api/v1/users/${userId}`)
      currentUser.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch user error:', error)
      const message = error.response?.data?.detail || 'Error al cargar el usuario'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const createUser = async (userData) => {
    try {
      isCreating.value = true
      
      const response = await axios.post('/api/v1/users', userData)
      
      // Add to local state
      users.value.unshift(response.data)
      
      // Update statistics
      statistics.value.total_users += 1
      if (response.data.status === 'active') {
        statistics.value.active_users += 1
      } else if (response.data.status === 'pending') {
        statistics.value.pending_users += 1
      }
      if (response.data.role === 'admin') {
        statistics.value.admin_users += 1
      }
      
      toast.success('Usuario creado exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Create user error:', error)
      const message = error.response?.data?.detail || 'Error al crear el usuario'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isCreating.value = false
    }
  }
  
  const updateUser = async (userId, userData) => {
    try {
      isUpdating.value = true
      
      const response = await axios.put(`/api/v1/users/${userId}`, userData)
      
      // Update in local state
      const index = users.value.findIndex(user => user.id === userId)
      if (index !== -1) {
        const oldUser = users.value[index]
        users.value[index] = response.data
        
        // Update statistics if status or role changed
        if (oldUser.status !== response.data.status) {
          if (oldUser.status === 'active') statistics.value.active_users -= 1
          if (oldUser.status === 'pending') statistics.value.pending_users -= 1
          if (response.data.status === 'active') statistics.value.active_users += 1
          if (response.data.status === 'pending') statistics.value.pending_users += 1
        }
        
        if (oldUser.role !== response.data.role) {
          if (oldUser.role === 'admin') statistics.value.admin_users -= 1
          if (response.data.role === 'admin') statistics.value.admin_users += 1
        }
      }
      
      // Update current user if it's the same
      if (currentUser.value?.id === userId) {
        currentUser.value = response.data
      }
      
      toast.success('Usuario actualizado exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update user error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar el usuario'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isUpdating.value = false
    }
  }
  
  const deleteUser = async (userId) => {
    try {
      isDeleting.value = true
      
      await axios.delete(`/api/v1/users/${userId}`)
      
      // Remove from local state
      const index = users.value.findIndex(user => user.id === userId)
      if (index !== -1) {
        const user = users.value[index]
        users.value.splice(index, 1)
        
        // Update statistics
        statistics.value.total_users -= 1
        if (user.status === 'active') statistics.value.active_users -= 1
        if (user.status === 'pending') statistics.value.pending_users -= 1
        if (user.role === 'admin') statistics.value.admin_users -= 1
      }
      
      toast.success('Usuario eliminado exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Delete user error:', error)
      const message = error.response?.data?.detail || 'Error al eliminar el usuario'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isDeleting.value = false
    }
  }
  
  const toggleUserStatus = async (userId) => {
    try {
      const user = users.value.find(u => u.id === userId)
      if (!user) return { success: false, error: 'Usuario no encontrado' }
      
      const newStatus = user.status === 'active' ? 'inactive' : 'active'
      
      const response = await axios.patch(`/api/v1/users/${userId}/status`, {
        status: newStatus
      })
      
      // Update in local state
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        const oldStatus = users.value[index].status
        users.value[index] = response.data
        
        // Update statistics
        if (oldStatus === 'active') statistics.value.active_users -= 1
        if (oldStatus === 'pending') statistics.value.pending_users -= 1
        if (response.data.status === 'active') statistics.value.active_users += 1
        if (response.data.status === 'pending') statistics.value.pending_users += 1
      }
      
      const statusText = newStatus === 'active' ? 'activado' : 'desactivado'
      toast.success(`Usuario ${statusText} exitosamente`)
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Toggle user status error:', error)
      const message = error.response?.data?.detail || 'Error al cambiar el estado del usuario'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const inviteUser = async (invitationData) => {
    try {
      isSendingInvitation.value = true
      
      const response = await axios.post('/api/v1/users/invite', invitationData)
      
      // Add to invitations list
      invitations.value.unshift(response.data)
      
      toast.success('Invitación enviada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Invite user error:', error)
      const message = error.response?.data?.detail || 'Error al enviar la invitación'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isSendingInvitation.value = false
    }
  }
  
  const fetchInvitations = async (params = {}) => {
    try {
      const response = await axios.get('/api/v1/users/invitations', {
        params
      })
      
      invitations.value = response.data.items || response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch invitations error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las invitaciones'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const resendInvitation = async (invitationId) => {
    try {
      const response = await axios.post(`/api/v1/users/invitations/${invitationId}/resend`)
      
      // Update invitation in local state
      const index = invitations.value.findIndex(inv => inv.id === invitationId)
      if (index !== -1) {
        invitations.value[index] = response.data
      }
      
      toast.success('Invitación reenviada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Resend invitation error:', error)
      const message = error.response?.data?.detail || 'Error al reenviar la invitación'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const cancelInvitation = async (invitationId) => {
    try {
      await axios.delete(`/api/v1/users/invitations/${invitationId}`)
      
      // Remove from local state
      const index = invitations.value.findIndex(inv => inv.id === invitationId)
      if (index !== -1) {
        invitations.value.splice(index, 1)
      }
      
      toast.success('Invitación cancelada exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Cancel invitation error:', error)
      const message = error.response?.data?.detail || 'Error al cancelar la invitación'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchUserProfile = async (userId) => {
    try {
      const response = await axios.get(`/api/v1/users/${userId}/profile`)
      userProfile.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch user profile error:', error)
      const message = error.response?.data?.detail || 'Error al cargar el perfil del usuario'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const updateUserProfile = async (userId, profileData) => {
    try {
      const response = await axios.put(`/api/v1/users/${userId}/profile`, profileData)
      
      userProfile.value = response.data
      
      // Update in users list if present
      const index = users.value.findIndex(user => user.id === userId)
      if (index !== -1) {
        users.value[index] = { ...users.value[index], ...response.data }
      }
      
      toast.success('Perfil actualizado exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update user profile error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar el perfil'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const fetchUserStatistics = async (params = {}) => {
    try {
      const response = await axios.get('/api/v1/users/statistics', {
        params
      })
      
      statistics.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch user statistics error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las estadísticas de usuarios'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  const exportUsers = async (format = 'csv', params = {}) => {
    try {
      const queryParams = {
        format,
        ...filters.value,
        ...params
      }
      
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === '' || queryParams[key] === null) {
          delete queryParams[key]
        }
      })
      
      const response = await axios.get('/api/v1/users/export', {
        params: queryParams,
        responseType: 'blob'
      })
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `users.${format}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
      
      toast.success('Lista de usuarios exportada exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Export users error:', error)
      const message = error.response?.data?.detail || 'Error al exportar los usuarios'
      toast.error(message)
      return { success: false, error: message }
    }
  }
  
  // Utility functions
  const setPage = (page) => {
    pagination.value.page = page
  }
  
  const setLimit = (limit) => {
    pagination.value.limit = limit
    pagination.value.page = 1 // Reset to first page
  }
  
  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Reset to first page when filtering
  }
  
  const clearFilters = () => {
    filters.value = {
      search: '',
      role: '',
      status: '',
      sort_by: 'created_at',
      sort_order: 'desc'
    }
    pagination.value.page = 1
  }
  
  const clearCurrentUser = () => {
    currentUser.value = null
  }
  
  const clearUserProfile = () => {
    userProfile.value = null
  }
  
  const refreshUsers = async () => {
    return await fetchUsers()
  }

  return {
    // State
    users,
    currentUser,
    userProfile,
    invitations,
    isLoading,
    isCreating,
    isUpdating,
    isDeleting,
    isSendingInvitation,
    pagination,
    filters,
    statistics,
    
    // Getters
    hasUsers,
    activeUsers,
    pendingUsers,
    adminUsers,
    filteredUsers,
    hasNextPage,
    hasPrevPage,
    
    // Actions
    fetchUsers,
    fetchUser,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    inviteUser,
    fetchInvitations,
    resendInvitation,
    cancelInvitation,
    fetchUserProfile,
    updateUserProfile,
    fetchUserStatistics,
    exportUsers,
    
    // Utilities
    setPage,
    setLimit,
    setFilters,
    clearFilters,
    clearCurrentUser,
    clearUserProfile,
    refreshUsers
  }
})