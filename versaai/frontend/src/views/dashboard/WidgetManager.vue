<template>
  <div class="widget-manager">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Gestión de Widgets</h1>
            <p class="text-sm text-gray-600 mt-1">Crea, configura y gestiona tus widgets embebibles</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="exportAllWidgets"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              Exportar Todo
            </button>
            <button
              @click="createNewWidget"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon class="w-4 h-4 mr-2" />
              Nuevo Widget
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Estadísticas -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <CubeIcon class="w-5 h-5 text-blue-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Widgets</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.totalWidgets }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckCircleIcon class="w-5 h-5 text-green-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Widgets Activos</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.activeWidgets }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <ChatBubbleLeftRightIcon class="w-5 h-5 text-purple-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Conversaciones Hoy</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.conversationsToday }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <EyeIcon class="w-5 h-5 text-yellow-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Vistas Totales</p>
              <p class="text-2xl font-bold text-gray-900">{{ formatNumber(stats.totalViews) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros y Búsqueda -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Buscar</label>
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                v-model="filters.search"
                type="text"
                placeholder="Buscar widgets..."
                class="pl-10 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Estado</label>
            <select
              v-model="filters.status"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
              <option value="">Todos los estados</option>
              <option value="active">Activo</option>
              <option value="inactive">Inactivo</option>
              <option value="draft">Borrador</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Dominio</label>
            <select
              v-model="filters.domain"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
              <option value="">Todos los dominios</option>
              <option v-for="domain in uniqueDomains" :key="domain" :value="domain">
                {{ domain }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Ordenar por</label>
            <select
              v-model="filters.sortBy"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
              <option value="created_at">Fecha de creación</option>
              <option value="name">Nombre</option>
              <option value="conversations">Conversaciones</option>
              <option value="views">Vistas</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Lista de Widgets -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900">Widgets ({{ filteredWidgets.length }})</h3>
            <div class="flex items-center space-x-2">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'p-2 rounded-md',
                  viewMode === 'grid' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <Squares2X2Icon class="w-5 h-5" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'p-2 rounded-md',
                  viewMode === 'list' ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-gray-600'
                ]"
              >
                <ListBulletIcon class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <!-- Vista Grid -->
        <div v-if="viewMode === 'grid'" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="widget in paginatedWidgets"
              :key="widget.id"
              class="widget-card bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow duration-200"
            >
              <!-- Widget Preview -->
              <div class="relative h-48 bg-gray-50 rounded-t-lg overflow-hidden">
                <div class="absolute inset-0 flex items-center justify-center">
                  <div 
                    class="widget-preview-mini"
                    :style="{
                      backgroundColor: widget.config.primaryColor,
                      width: '60px',
                      height: '60px',
                      borderRadius: widget.config.buttonShape === 'circle' ? '50%' : widget.config.buttonShape === 'rounded' ? '12px' : '0'
                    }"
                  >
                    <ChatBubbleLeftRightIcon class="w-6 h-6 text-white" />
                  </div>
                </div>
                <div class="absolute top-3 right-3">
                  <span
                    :class="[
                      'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                      widget.status === 'active' ? 'bg-green-100 text-green-800' :
                      widget.status === 'inactive' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    ]"
                  >
                    {{ getStatusLabel(widget.status) }}
                  </span>
                </div>
              </div>
              
              <!-- Widget Info -->
              <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="text-lg font-medium text-gray-900 truncate">{{ widget.name }}</h4>
                  <div class="ml-2 flex-shrink-0">
                    <div class="relative">
                      <button
                        @click="toggleWidgetMenu(widget.id)"
                        class="p-1 rounded-full hover:bg-gray-100"
                      >
                        <EllipsisVerticalIcon class="w-5 h-5 text-gray-400" />
                      </button>
                      
                      <!-- Menú desplegable -->
                      <div
                        v-if="activeWidgetMenu === widget.id"
                        class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-10"
                      >
                        <div class="py-1">
                          <button
                            @click="editWidget(widget)"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            <PencilIcon class="w-4 h-4 inline mr-2" />
                            Editar
                          </button>
                          <button
                            @click="duplicateWidget(widget)"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            <DocumentDuplicateIcon class="w-4 h-4 inline mr-2" />
                            Duplicar
                          </button>
                          <button
                            @click="viewAnalytics(widget)"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            <ChartBarIcon class="w-4 h-4 inline mr-2" />
                            Analytics
                          </button>
                          <button
                            @click="getEmbedCode(widget)"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            <CodeBracketIcon class="w-4 h-4 inline mr-2" />
                            Código
                          </button>
                          <hr class="my-1">
                          <button
                            @click="toggleWidgetStatus(widget)"
                            :class="[
                              'block w-full text-left px-4 py-2 text-sm hover:bg-gray-100',
                              widget.status === 'active' ? 'text-red-700' : 'text-green-700'
                            ]"
                          >
                            <component :is="widget.status === 'active' ? PauseIcon : PlayIcon" class="w-4 h-4 inline mr-2" />
                            {{ widget.status === 'active' ? 'Desactivar' : 'Activar' }}
                          </button>
                          <button
                            @click="deleteWidget(widget)"
                            class="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-gray-100"
                          >
                            <TrashIcon class="w-4 h-4 inline mr-2" />
                            Eliminar
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <p class="text-sm text-gray-600 mb-3">{{ widget.domain }}</p>
                
                <!-- Métricas -->
                <div class="grid grid-cols-2 gap-4 mb-3">
                  <div class="text-center">
                    <p class="text-lg font-semibold text-gray-900">{{ formatNumber(widget.metrics.conversations) }}</p>
                    <p class="text-xs text-gray-500">Conversaciones</p>
                  </div>
                  <div class="text-center">
                    <p class="text-lg font-semibold text-gray-900">{{ formatNumber(widget.metrics.views) }}</p>
                    <p class="text-xs text-gray-500">Vistas</p>
                  </div>
                </div>
                
                <!-- Fecha -->
                <p class="text-xs text-gray-500">
                  Creado: {{ formatDate(widget.created_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Vista Lista -->
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Widget
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Dominio
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Conversaciones
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vistas
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Creado
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="widget in paginatedWidgets" :key="widget.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div 
                      class="flex-shrink-0 w-10 h-10 flex items-center justify-center text-white"
                      :style="{
                        backgroundColor: widget.config.primaryColor,
                        borderRadius: widget.config.buttonShape === 'circle' ? '50%' : widget.config.buttonShape === 'rounded' ? '8px' : '0'
                      }"
                    >
                      <ChatBubbleLeftRightIcon class="w-5 h-5" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ widget.name }}</div>
                      <div class="text-sm text-gray-500">{{ widget.config.botName }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                      widget.status === 'active' ? 'bg-green-100 text-green-800' :
                      widget.status === 'inactive' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    ]"
                  >
                    {{ getStatusLabel(widget.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ widget.domain }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatNumber(widget.metrics.conversations) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatNumber(widget.metrics.views) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(widget.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end space-x-2">
                    <button
                      @click="editWidget(widget)"
                      class="text-primary-600 hover:text-primary-900"
                    >
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="viewAnalytics(widget)"
                      class="text-gray-600 hover:text-gray-900"
                    >
                      <ChartBarIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="getEmbedCode(widget)"
                      class="text-gray-600 hover:text-gray-900"
                    >
                      <CodeBracketIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div v-if="totalPages > 1" class="px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-700">
              Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a {{ Math.min(currentPage * itemsPerPage, filteredWidgets.length) }} de {{ filteredWidgets.length }} widgets
            </div>
            <div class="flex items-center space-x-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </button>
              <span class="px-3 py-2 text-sm text-gray-700">
                Página {{ currentPage }} de {{ totalPages }}
              </span>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Configuración -->
    <div v-if="showConfigModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeConfigModal"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-6xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900">
                {{ editingWidget ? 'Editar Widget' : 'Nuevo Widget' }}
              </h3>
              <button @click="closeConfigModal" class="text-gray-400 hover:text-gray-600">
                <XMarkIcon class="w-6 h-6" />
              </button>
            </div>
            
            <WidgetConfigurator
              v-if="showConfigModal"
              :widget="editingWidget"
              @save="handleWidgetSave"
              @cancel="closeConfigModal"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  PlusIcon,
  ArrowDownTrayIcon,
  CubeIcon,
  CheckCircleIcon,
  ChatBubbleLeftRightIcon,
  EyeIcon,
  MagnifyingGlassIcon,
  Squares2X2Icon,
  ListBulletIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  DocumentDuplicateIcon,
  ChartBarIcon,
  CodeBracketIcon,
  PlayIcon,
  PauseIcon,
  TrashIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import WidgetConfigurator from '@/components/dashboard/WidgetConfigurator.vue'

const router = useRouter()

// Estado reactivo
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = ref(12)
const activeWidgetMenu = ref(null)
const showConfigModal = ref(false)
const editingWidget = ref(null)

// Filtros
const filters = ref({
  search: '',
  status: '',
  domain: '',
  sortBy: 'created_at'
})

// Estadísticas
const stats = ref({
  totalWidgets: 24,
  activeWidgets: 18,
  conversationsToday: 1247,
  totalViews: 45623
})

// Datos de widgets (mock)
const widgets = ref([
  {
    id: 1,
    name: 'Widget Principal',
    domain: 'ejemplo.com',
    status: 'active',
    created_at: '2024-01-15T10:30:00Z',
    config: {
      botName: 'Asistente Virtual',
      primaryColor: '#3B82F6',
      buttonShape: 'circle'
    },
    metrics: {
      conversations: 1247,
      views: 8934
    }
  },
  {
    id: 2,
    name: 'Widget Soporte',
    domain: 'soporte.ejemplo.com',
    status: 'active',
    created_at: '2024-01-10T14:20:00Z',
    config: {
      botName: 'Soporte Técnico',
      primaryColor: '#10B981',
      buttonShape: 'rounded'
    },
    metrics: {
      conversations: 892,
      views: 5621
    }
  },
  {
    id: 3,
    name: 'Widget Ventas',
    domain: 'tienda.ejemplo.com',
    status: 'inactive',
    created_at: '2024-01-08T09:15:00Z',
    config: {
      botName: 'Asesor de Ventas',
      primaryColor: '#F59E0B',
      buttonShape: 'square'
    },
    metrics: {
      conversations: 456,
      views: 3210
    }
  },
  {
    id: 4,
    name: 'Widget Beta',
    domain: 'beta.ejemplo.com',
    status: 'draft',
    created_at: '2024-01-05T16:45:00Z',
    config: {
      botName: 'Beta Assistant',
      primaryColor: '#8B5CF6',
      buttonShape: 'circle'
    },
    metrics: {
      conversations: 123,
      views: 890
    }
  }
])

// Computed properties
const uniqueDomains = computed(() => {
  return [...new Set(widgets.value.map(w => w.domain))]
})

const filteredWidgets = computed(() => {
  let filtered = widgets.value
  
  // Filtro de búsqueda
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    filtered = filtered.filter(widget => 
      widget.name.toLowerCase().includes(search) ||
      widget.domain.toLowerCase().includes(search) ||
      widget.config.botName.toLowerCase().includes(search)
    )
  }
  
  // Filtro de estado
  if (filters.value.status) {
    filtered = filtered.filter(widget => widget.status === filters.value.status)
  }
  
  // Filtro de dominio
  if (filters.value.domain) {
    filtered = filtered.filter(widget => widget.domain === filters.value.domain)
  }
  
  // Ordenamiento
  filtered.sort((a, b) => {
    switch (filters.value.sortBy) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'conversations':
        return b.metrics.conversations - a.metrics.conversations
      case 'views':
        return b.metrics.views - a.metrics.views
      case 'created_at':
      default:
        return new Date(b.created_at) - new Date(a.created_at)
    }
  })
  
  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredWidgets.value.length / itemsPerPage.value)
})

const paginatedWidgets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredWidgets.value.slice(start, end)
})

// Métodos
const formatNumber = (num) => {
  return new Intl.NumberFormat('es-ES').format(num)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getStatusLabel = (status) => {
  const labels = {
    active: 'Activo',
    inactive: 'Inactivo',
    draft: 'Borrador'
  }
  return labels[status] || status
}

const toggleWidgetMenu = (widgetId) => {
  activeWidgetMenu.value = activeWidgetMenu.value === widgetId ? null : widgetId
}

const createNewWidget = () => {
  editingWidget.value = null
  showConfigModal.value = true
}

const editWidget = (widget) => {
  editingWidget.value = { ...widget }
  showConfigModal.value = true
  activeWidgetMenu.value = null
}

const duplicateWidget = (widget) => {
  const newWidget = {
    ...widget,
    id: Date.now(),
    name: `${widget.name} (Copia)`,
    status: 'draft',
    created_at: new Date().toISOString(),
    metrics: {
      conversations: 0,
      views: 0
    }
  }
  widgets.value.unshift(newWidget)
  activeWidgetMenu.value = null
}

const viewAnalytics = (widget) => {
  router.push(`/dashboard/widgets/${widget.id}/analytics`)
  activeWidgetMenu.value = null
}

const getEmbedCode = (widget) => {
  const embedCode = `
<!-- VersaAI Chat Widget -->
<script>
  window.VersaAIConfig = ${JSON.stringify(widget.config, null, 2)};
<\/script>
<script src="https://cdn.versaai.com/widget/versaai-widget.js"><\/script>
<!-- End VersaAI Chat Widget -->`
  
  navigator.clipboard.writeText(embedCode).then(() => {
    alert('Código de integración copiado al portapapeles')
  })
  activeWidgetMenu.value = null
}

const toggleWidgetStatus = (widget) => {
  const index = widgets.value.findIndex(w => w.id === widget.id)
  if (index !== -1) {
    widgets.value[index].status = widget.status === 'active' ? 'inactive' : 'active'
  }
  activeWidgetMenu.value = null
}

const deleteWidget = (widget) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el widget "${widget.name}"?`)) {
    const index = widgets.value.findIndex(w => w.id === widget.id)
    if (index !== -1) {
      widgets.value.splice(index, 1)
    }
  }
  activeWidgetMenu.value = null
}

const exportAllWidgets = () => {
  const exportData = {
    widgets: widgets.value,
    exportDate: new Date().toISOString(),
    version: '1.0'
  }
  
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'widgets-export.json'
  a.click()
  URL.revokeObjectURL(url)
}

const closeConfigModal = () => {
  showConfigModal.value = false
  editingWidget.value = null
}

const handleWidgetSave = (widgetData) => {
  if (editingWidget.value) {
    // Actualizar widget existente
    const index = widgets.value.findIndex(w => w.id === editingWidget.value.id)
    if (index !== -1) {
      widgets.value[index] = { ...widgets.value[index], ...widgetData }
    }
  } else {
    // Crear nuevo widget
    const newWidget = {
      id: Date.now(),
      name: widgetData.name || 'Nuevo Widget',
      domain: widgetData.domain || 'ejemplo.com',
      status: 'draft',
      created_at: new Date().toISOString(),
      config: widgetData.config || {},
      metrics: {
        conversations: 0,
        views: 0
      }
    }
    widgets.value.unshift(newWidget)
  }
  
  closeConfigModal()
}

// Event listeners
const handleClickOutside = (event) => {
  if (!event.target.closest('.widget-menu')) {
    activeWidgetMenu.value = null
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.widget-card {
  transition: all 0.2s ease;
}

.widget-card:hover {
  transform: translateY(-2px);
}

.widget-preview-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.widget-preview-mini:hover {
  transform: scale(1.1);
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.widget-card {
  animation: fadeIn 0.3s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
  .widget-card {
    margin-bottom: 1rem;
  }
}
</style>