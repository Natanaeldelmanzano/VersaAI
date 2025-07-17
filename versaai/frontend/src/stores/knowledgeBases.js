import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

export const useKnowledgeBasesStore = defineStore('knowledgeBases', () => {
  // State
  const knowledgeBases = ref([])
  const currentKnowledgeBase = ref(null)
  const documents = ref([])
  const isLoading = ref(false)
  const isUploading = ref(false)
  const uploadProgress = ref(0)
  const pagination = ref({
    page: 1,
    per_page: 12,
    total: 0,
    pages: 0
  })
  const filters = ref({
    search: '',
    status: 'all',
    sort_by: 'created_at',
    sort_order: 'desc'
  })
  const stats = ref({
    total_documents: 0,
    active_bases: 0,
    storage_used: 0,
    processing_items: 0
  })

  const toast = useToast()

  // Getters
  const totalKnowledgeBases = computed(() => knowledgeBases.value.length)
  const hasKnowledgeBases = computed(() => knowledgeBases.value.length > 0)
  const isLastPage = computed(() => pagination.value.page >= pagination.value.pages)
  const formattedStorageUsed = computed(() => {
    const bytes = stats.value.storage_used
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  })

  // Actions
  const fetchKnowledgeBases = async (params = {}) => {
    try {
      isLoading.value = true
      
      const queryParams = {
        page: pagination.value.page,
        per_page: pagination.value.per_page,
        ...filters.value,
        ...params
      }

      // Remove null/empty values
      Object.keys(queryParams).forEach(key => {
        if (queryParams[key] === null || queryParams[key] === '' || queryParams[key] === 'all') {
          delete queryParams[key]
        }
      })

      const response = await axios.get('/api/v1/knowledge-base/', {
        params: queryParams
      })

      knowledgeBases.value = response.data.items
      pagination.value = {
        page: response.data.page,
        per_page: response.data.per_page,
        total: response.data.total,
        pages: response.data.pages
      }

      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch knowledge bases error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las bases de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const fetchKnowledgeBase = async (id) => {
    try {
      isLoading.value = true
      
      const response = await axios.get(`/api/v1/knowledge-base/${id}`)
      currentKnowledgeBase.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al cargar la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const createKnowledgeBase = async (kbData) => {
    try {
      isLoading.value = true
      
      const response = await axios.post('/api/v1/knowledge-base/', kbData)
      
      // Add to local state
      knowledgeBases.value.unshift(response.data)
      pagination.value.total += 1
      
      toast.success('Base de conocimiento creada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Create knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al crear la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const updateKnowledgeBase = async (id, kbData) => {
    try {
      isLoading.value = true
      
      const response = await axios.put(`/api/v1/knowledge-base/${id}`, kbData)
      
      // Update in local state
      const index = knowledgeBases.value.findIndex(kb => kb.id === id)
      if (index !== -1) {
        knowledgeBases.value[index] = response.data
      }
      
      // Update current knowledge base if it's the one being edited
      if (currentKnowledgeBase.value?.id === id) {
        currentKnowledgeBase.value = response.data
      }
      
      toast.success('Base de conocimiento actualizada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al actualizar la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const deleteKnowledgeBase = async (id) => {
    try {
      await axios.delete(`/api/v1/knowledge-base/${id}`)
      
      // Remove from local state
      const index = knowledgeBases.value.findIndex(kb => kb.id === id)
      if (index !== -1) {
        knowledgeBases.value.splice(index, 1)
        pagination.value.total -= 1
      }
      
      // Clear current knowledge base if it was deleted
      if (currentKnowledgeBase.value?.id === id) {
        currentKnowledgeBase.value = null
      }
      
      toast.success('Base de conocimiento eliminada exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Delete knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al eliminar la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const duplicateKnowledgeBase = async (id) => {
    try {
      isLoading.value = true
      
      const response = await axios.post(`/api/v1/knowledge-base/${id}/duplicate`)
      
      // Add to local state
      knowledgeBases.value.unshift(response.data)
      pagination.value.total += 1
      
      toast.success('Base de conocimiento duplicada exitosamente')
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Duplicate knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al duplicar la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isLoading.value = false
    }
  }

  const reprocessKnowledgeBase = async (id) => {
    try {
      await axios.post(`/api/v1/knowledge-base/${id}/reprocess`)
      
      // Update status in local state
      const index = knowledgeBases.value.findIndex(kb => kb.id === id)
      if (index !== -1) {
        knowledgeBases.value[index].status = 'processing'
      }
      
      if (currentKnowledgeBase.value?.id === id) {
        currentKnowledgeBase.value.status = 'processing'
      }
      
      toast.success('Reprocesamiento iniciado exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Reprocess knowledge base error:', error)
      const message = error.response?.data?.detail || 'Error al reprocesar la base de conocimiento'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const fetchDocuments = async (kbId, params = {}) => {
    try {
      const response = await axios.get(`/api/v1/knowledge-base/${kbId}/documents`, {
        params
      })
      
      documents.value = response.data.items || response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch documents error:', error)
      const message = error.response?.data?.detail || 'Error al cargar los documentos'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const uploadDocuments = async (kbId, files, onProgress = null) => {
    try {
      isUploading.value = true
      uploadProgress.value = 0
      
      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })
      
      const response = await axios.post(
        `/api/v1/knowledge-base/${kbId}/documents/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            uploadProgress.value = progress
            if (onProgress) {
              onProgress(progress)
            }
          }
        }
      )
      
      // Update document count in knowledge base
      const kbIndex = knowledgeBases.value.findIndex(kb => kb.id === kbId)
      if (kbIndex !== -1) {
        knowledgeBases.value[kbIndex].document_count += response.data.uploaded_count
      }
      
      if (currentKnowledgeBase.value?.id === kbId) {
        currentKnowledgeBase.value.document_count += response.data.uploaded_count
      }
      
      toast.success(`${response.data.uploaded_count} documento(s) subido(s) exitosamente`)
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Upload documents error:', error)
      const message = error.response?.data?.detail || 'Error al subir los documentos'
      toast.error(message)
      return { success: false, error: message }
    } finally {
      isUploading.value = false
      uploadProgress.value = 0
    }
  }

  const deleteDocument = async (kbId, documentId) => {
    try {
      await axios.delete(`/api/v1/knowledge-base/${kbId}/documents/${documentId}`)
      
      // Remove from local state
      const index = documents.value.findIndex(doc => doc.id === documentId)
      if (index !== -1) {
        documents.value.splice(index, 1)
      }
      
      // Update document count
      const kbIndex = knowledgeBases.value.findIndex(kb => kb.id === kbId)
      if (kbIndex !== -1) {
        knowledgeBases.value[kbIndex].document_count -= 1
      }
      
      if (currentKnowledgeBase.value?.id === kbId) {
        currentKnowledgeBase.value.document_count -= 1
      }
      
      toast.success('Documento eliminado exitosamente')
      
      return { success: true }
    } catch (error) {
      console.error('Delete document error:', error)
      const message = error.response?.data?.detail || 'Error al eliminar el documento'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const searchDocuments = async (kbId, query, params = {}) => {
    try {
      const response = await axios.get(`/api/v1/knowledge-base/${kbId}/search`, {
        params: {
          query,
          ...params
        }
      })
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Search documents error:', error)
      const message = error.response?.data?.detail || 'Error al buscar en los documentos'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/v1/knowledge-base/stats')
      
      stats.value = response.data
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Fetch knowledge base stats error:', error)
      const message = error.response?.data?.detail || 'Error al cargar las estadísticas'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  // Utility functions
  const setPage = (page) => {
    pagination.value.page = page
  }

  const setPerPage = (perPage) => {
    pagination.value.per_page = perPage
    pagination.value.page = 1 // Reset to first page
  }

  const setFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Reset to first page when filtering
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      status: 'all',
      sort_by: 'created_at',
      sort_order: 'desc'
    }
    pagination.value.page = 1
  }

  const clearKnowledgeBases = () => {
    knowledgeBases.value = []
    currentKnowledgeBase.value = null
    documents.value = []
    pagination.value = {
      page: 1,
      per_page: 12,
      total: 0,
      pages: 0
    }
  }

  const clearCurrentKnowledgeBase = () => {
    currentKnowledgeBase.value = null
    documents.value = []
  }

  return {
    // State
    knowledgeBases,
    currentKnowledgeBase,
    documents,
    isLoading,
    isUploading,
    uploadProgress,
    pagination,
    filters,
    stats,
    
    // Getters
    totalKnowledgeBases,
    hasKnowledgeBases,
    isLastPage,
    formattedStorageUsed,
    
    // Actions
    fetchKnowledgeBases,
    fetchKnowledgeBase,
    createKnowledgeBase,
    updateKnowledgeBase,
    deleteKnowledgeBase,
    duplicateKnowledgeBase,
    reprocessKnowledgeBase,
    fetchDocuments,
    uploadDocuments,
    deleteDocument,
    searchDocuments,
    fetchStats,
    
    // Utilities
    setPage,
    setPerPage,
    setFilters,
    resetFilters,
    clearKnowledgeBases,
    clearCurrentKnowledgeBase
  }
})