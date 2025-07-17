import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserManagementStore = defineStore('userManagement', () => {
  // State
  const users = ref([])
  const organizations = ref([])
  const roles = ref([
    { id: 'admin', name: 'Administrador', permissions: ['all'] },
    { id: 'manager', name: 'Manager', permissions: ['read', 'write', 'manage_users'] },
    { id: 'user', name: 'Usuario', permissions: ['read', 'write'] },
    { id: 'viewer', name: 'Visualizador', permissions: ['read'] }
  ])
  const loading = ref(false)
  const error = ref(null)
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
    organization: ''
  })

  // Getters
  const totalUsers = computed(() => users.value.length)
  const activeUsers = computed(() => users.value.filter(u => u.status === 'active').length)
  const inactiveUsers = computed(() => users.value.filter(u => u.status === 'inactive').length)
  const adminUsers = computed(() => users.value.filter(u => u.role === 'admin').length)
  const newUsersThisMonth = computed(() => {
    const now = new Date()
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    return users.value.filter(u => new Date(u.created_at) >= startOfMonth).length
  })

  const filteredUsers = computed(() => {
    let filtered = users.value

    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      filtered = filtered.filter(user => 
        user.name.toLowerCase().includes(search) ||
        user.email.toLowerCase().includes(search) ||
        user.organization?.toLowerCase().includes(search)
      )
    }

    if (filters.value.role) {
      filtered = filtered.filter(user => user.role === filters.value.role)
    }

    if (filters.value.status) {
      filtered = filtered.filter(user => user.status === filters.value.status)
    }

    if (filters.value.organization) {
      filtered = filtered.filter(user => user.organization === filters.value.organization)
    }

    return filtered
  })

  const paginatedUsers = computed(() => {
    const start = (pagination.value.page - 1) * pagination.value.limit
    const end = start + pagination.value.limit
    return filteredUsers.value.slice(start, end)
  })

  const userStats = computed(() => ({
    total: totalUsers.value,
    active: activeUsers.value,
    inactive: inactiveUsers.value,
    admins: adminUsers.value,
    newThisMonth: newUsersThisMonth.value,
    byRole: roles.value.map(role => ({
      role: role.id,
      name: role.name,
      count: users.value.filter(u => u.role === role.id).length
    })),
    byOrganization: organizations.value.map(org => ({
      organization: org.id,
      name: org.name,
      count: users.value.filter(u => u.organization_id === org.id).length
    }))
  }))

  // Actions
  const fetchUsers = async (params = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const queryParams = new URLSearchParams({
        page: params.page || pagination.value.page,
        limit: params.limit || pagination.value.limit,
        ...filters.value,
        ...params
      })

      const response = await fetch(`/api/v1/users?${queryParams}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      users.value = data.users || []
      pagination.value = {
        page: data.page || 1,
        limit: data.limit || 10,
        total: data.total || 0,
        totalPages: data.totalPages || 0
      }
    } catch (err) {
      console.error('Error fetching users:', err)
      error.value = err.message
      
      // Fallback mock data
      users.value = [
        {
          id: 1,
          name: 'Juan Pérez',
          email: 'juan@example.com',
          role: 'admin',
          status: 'active',
          last_login: '2024-01-15T10:30:00Z',
          created_at: '2024-01-01T00:00:00Z',
          organization_id: 1,
          organization: 'Acme Corp',
          avatar: null,
          permissions: ['all']
        },
        {
          id: 2,
          name: 'María García',
          email: 'maria@example.com',
          role: 'manager',
          status: 'active',
          last_login: '2024-01-14T15:45:00Z',
          created_at: '2024-01-05T00:00:00Z',
          organization_id: 2,
          organization: 'TechStart Inc',
          avatar: null,
          permissions: ['read', 'write', 'manage_users']
        },
        {
          id: 3,
          name: 'Carlos López',
          email: 'carlos@example.com',
          role: 'user',
          status: 'active',
          last_login: '2024-01-13T09:15:00Z',
          created_at: '2024-01-10T00:00:00Z',
          organization_id: 3,
          organization: 'Global Solutions',
          avatar: null,
          permissions: ['read', 'write']
        },
        {
          id: 4,
          name: 'Ana Martínez',
          email: 'ana@example.com',
          role: 'viewer',
          status: 'inactive',
          last_login: '2024-01-10T14:20:00Z',
          created_at: '2024-01-15T00:00:00Z',
          organization_id: 1,
          organization: 'Acme Corp',
          avatar: null,
          permissions: ['read']
        },
        {
          id: 5,
          name: 'Luis Rodríguez',
          email: 'luis@example.com',
          role: 'user',
          status: 'active',
          last_login: '2024-01-15T11:00:00Z',
          created_at: '2024-01-20T00:00:00Z',
          organization_id: 2,
          organization: 'TechStart Inc',
          avatar: null,
          permissions: ['read', 'write']
        }
      ]
      
      pagination.value = {
        page: 1,
        limit: 10,
        total: 5,
        totalPages: 1
      }
    } finally {
      loading.value = false
    }
  }

  const fetchOrganizations = async () => {
    try {
      const response = await fetch('/api/v1/organizations')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      organizations.value = data.organizations || []
    } catch (err) {
      console.error('Error fetching organizations:', err)
      
      // Fallback mock data
      organizations.value = [
        { id: 1, name: 'Acme Corp', users_count: 2 },
        { id: 2, name: 'TechStart Inc', users_count: 2 },
        { id: 3, name: 'Global Solutions', users_count: 1 }
      ]
    }
  }

  const createUser = async (userData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const newUser = await response.json()
      users.value.push(newUser)
      
      return newUser
    } catch (err) {
      console.error('Error creating user:', err)
      error.value = err.message
      
      // Mock creation for demo
      const newUser = {
        id: Math.max(...users.value.map(u => u.id)) + 1,
        ...userData,
        status: 'active',
        created_at: new Date().toISOString(),
        last_login: null,
        avatar: null,
        permissions: roles.value.find(r => r.id === userData.role)?.permissions || ['read']
      }
      
      users.value.push(newUser)
      return newUser
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (userId, userData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const updatedUser = await response.json()
      const index = users.value.findIndex(u => u.id === userId)
      
      if (index !== -1) {
        users.value[index] = updatedUser
      }
      
      return updatedUser
    } catch (err) {
      console.error('Error updating user:', err)
      error.value = err.message
      
      // Mock update for demo
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        users.value[index] = {
          ...users.value[index],
          ...userData,
          permissions: roles.value.find(r => r.id === userData.role)?.permissions || users.value[index].permissions
        }
        return users.value[index]
      }
    } finally {
      loading.value = false
    }
  }

  const deleteUser = async (userId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/v1/users/${userId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      users.value = users.value.filter(u => u.id !== userId)
      
      return true
    } catch (err) {
      console.error('Error deleting user:', err)
      error.value = err.message
      
      // Mock deletion for demo
      users.value = users.value.filter(u => u.id !== userId)
      return true
    } finally {
      loading.value = false
    }
  }

  const toggleUserStatus = async (userId) => {
    const user = users.value.find(u => u.id === userId)
    if (!user) return
    
    const newStatus = user.status === 'active' ? 'inactive' : 'active'
    return await updateUser(userId, { status: newStatus })
  }

  const bulkUpdateUsers = async (userIds, updates) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/v1/users/bulk', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_ids: userIds, updates })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const updatedUsers = await response.json()
      
      // Update local state
      updatedUsers.forEach(updatedUser => {
        const index = users.value.findIndex(u => u.id === updatedUser.id)
        if (index !== -1) {
          users.value[index] = updatedUser
        }
      })
      
      return updatedUsers
    } catch (err) {
      console.error('Error bulk updating users:', err)
      error.value = err.message
      
      // Mock bulk update for demo
      userIds.forEach(userId => {
        const index = users.value.findIndex(u => u.id === userId)
        if (index !== -1) {
          users.value[index] = { ...users.value[index], ...updates }
        }
      })
      
      return users.value.filter(u => userIds.includes(u.id))
    } finally {
      loading.value = false
    }
  }

  const exportUsers = async (format = 'csv') => {
    try {
      const response = await fetch(`/api/v1/users/export?format=${format}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `users_export_${new Date().toISOString().split('T')[0]}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      return true
    } catch (err) {
      console.error('Error exporting users:', err)
      error.value = err.message
      return false
    }
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Reset to first page when filtering
  }

  const setPagination = (newPagination) => {
    pagination.value = { ...pagination.value, ...newPagination }
  }

  const clearFilters = () => {
    filters.value = {
      search: '',
      role: '',
      status: '',
      organization: ''
    }
    pagination.value.page = 1
  }

  const getUserById = (userId) => {
    return users.value.find(u => u.id === userId)
  }

  const getUsersByRole = (role) => {
    return users.value.filter(u => u.role === role)
  }

  const getUsersByOrganization = (organizationId) => {
    return users.value.filter(u => u.organization_id === organizationId)
  }

  const hasPermission = (userId, permission) => {
    const user = getUserById(userId)
    if (!user) return false
    
    return user.permissions.includes('all') || user.permissions.includes(permission)
  }

  return {
    // State
    users,
    organizations,
    roles,
    loading,
    error,
    pagination,
    filters,
    
    // Getters
    totalUsers,
    activeUsers,
    inactiveUsers,
    adminUsers,
    newUsersThisMonth,
    filteredUsers,
    paginatedUsers,
    userStats,
    
    // Actions
    fetchUsers,
    fetchOrganizations,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    bulkUpdateUsers,
    exportUsers,
    setFilters,
    setPagination,
    clearFilters,
    getUserById,
    getUsersByRole,
    getUsersByOrganization,
    hasPermission
  }
})