<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="handleBackdropClick">
    <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-lg shadow-lg rounded-md bg-white">
      <!-- Header -->
      <div class="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">
            {{ editingCategory ? 'Editar Categoría' : 'Nueva Categoría' }}
          </h3>
          <p class="text-sm text-gray-600 mt-1">
            {{ editingCategory ? 'Modifica la información de la categoría' : 'Crea una nueva categoría para organizar documentos' }}
          </p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="saveCategory" class="mt-6 space-y-6">
        <!-- Category Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
            Nombre de la Categoría *
          </label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Ej: Políticas, Procedimientos, Manuales"
          />
        </div>

        <!-- Category Key -->
        <div>
          <label for="key" class="block text-sm font-medium text-gray-700 mb-2">
            Clave de Categoría *
          </label>
          <input
            id="key"
            v-model="form.key"
            type="text"
            required
            pattern="[a-z0-9_-]+"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="ej: politicas, procedimientos, manuales"
          />
          <p class="text-xs text-gray-500 mt-1">
            Solo letras minúsculas, números, guiones y guiones bajos
          </p>
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
            Descripción
          </label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Descripción de la categoría y qué tipo de documentos incluye..."
          ></textarea>
        </div>

        <!-- Color Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">
            Color de la Categoría
          </label>
          <div class="grid grid-cols-6 gap-3">
            <button
              v-for="color in availableColors"
              :key="color.name"
              type="button"
              @click="form.color = color.name"
              :class="[
                'w-10 h-10 rounded-full border-2 transition-all duration-200',
                color.bg,
                form.color === color.name
                  ? 'border-gray-900 ring-2 ring-offset-2 ring-gray-900'
                  : 'border-gray-300 hover:border-gray-400'
              ]"
              :title="color.label"
            >
              <CheckIcon
                v-if="form.color === color.name"
                class="h-5 w-5 text-white mx-auto"
              />
            </button>
          </div>
          <p class="text-xs text-gray-500 mt-2">
            El color ayuda a identificar visualmente la categoría
          </p>
        </div>

        <!-- Icon Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">
            Icono de la Categoría
          </label>
          <div class="grid grid-cols-6 gap-3">
            <button
              v-for="icon in availableIcons"
              :key="icon.name"
              type="button"
              @click="form.icon = icon.name"
              :class="[
                'w-10 h-10 rounded-lg border-2 transition-all duration-200 flex items-center justify-center',
                form.icon === icon.name
                  ? 'border-blue-500 bg-blue-50 text-blue-600'
                  : 'border-gray-300 hover:border-gray-400 text-gray-600'
              ]"
              :title="icon.label"
            >
              <component :is="icon.component" class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Category Preview -->
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Vista Previa</h4>
          <div class="flex items-center space-x-3">
            <div :class="[
              'w-12 h-12 rounded-lg flex items-center justify-center',
              getColorClasses(form.color).bg,
              getColorClasses(form.color).text
            ]">
              <component :is="getIconComponent(form.icon)" class="h-6 w-6" />
            </div>
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <h5 class="text-sm font-medium text-gray-900">
                  {{ form.name || 'Nombre de la categoría' }}
                </h5>
                <span :class="[
                  'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                  getColorClasses(form.color).badge
                ]">
                  {{ form.key || 'clave' }}
                </span>
              </div>
              <p class="text-xs text-gray-600 mt-1">
                {{ form.description || 'Descripción de la categoría' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Category Settings -->
        <div class="space-y-4">
          <h4 class="text-sm font-medium text-gray-900">Configuración</h4>
          
          <div class="space-y-3">
            <label class="flex items-center">
              <input
                v-model="form.isDefault"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="ml-3 text-sm text-gray-700">
                Categoría por defecto para nuevos documentos
              </span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="form.requiresApproval"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="ml-3 text-sm text-gray-700">
                Requiere aprobación para publicar documentos
              </span>
            </label>
            
            <label class="flex items-center">
              <input
                v-model="form.isActive"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="ml-3 text-sm text-gray-700">
                Categoría activa (visible para usuarios)
              </span>
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <span v-if="isLoading">{{ editingCategory ? 'Actualizando...' : 'Creando...' }}</span>
            <span v-else>{{ editingCategory ? 'Actualizar' : 'Crear' }} Categoría</span>
            <CheckIcon v-if="!isLoading" class="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  XMarkIcon,
  CheckIcon,
  FolderIcon,
  DocumentTextIcon,
  ShieldCheckIcon,
  AcademicCapIcon,
  QuestionMarkCircleIcon,
  CogIcon,
  UserGroupIcon,
  ChartBarIcon,
  BanknotesIcon,
  GlobeAltIcon,
  BuildingOfficeIcon,
  TruckIcon
} from '@heroicons/vue/24/outline'

// Props
const props = defineProps({
  category: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['close', 'save'])

// Reactive state
const isLoading = ref(false)
const editingCategory = computed(() => !!props.category)

const form = ref({
  name: '',
  key: '',
  description: '',
  color: 'blue',
  icon: 'folder',
  isDefault: false,
  requiresApproval: false,
  isActive: true
})

const availableColors = ref([
  { name: 'blue', label: 'Azul', bg: 'bg-blue-500', badge: 'bg-blue-100 text-blue-800' },
  { name: 'green', label: 'Verde', bg: 'bg-green-500', badge: 'bg-green-100 text-green-800' },
  { name: 'yellow', label: 'Amarillo', bg: 'bg-yellow-500', badge: 'bg-yellow-100 text-yellow-800' },
  { name: 'red', label: 'Rojo', bg: 'bg-red-500', badge: 'bg-red-100 text-red-800' },
  { name: 'purple', label: 'Morado', bg: 'bg-purple-500', badge: 'bg-purple-100 text-purple-800' },
  { name: 'gray', label: 'Gris', bg: 'bg-gray-500', badge: 'bg-gray-100 text-gray-800' },
  { name: 'indigo', label: 'Índigo', bg: 'bg-indigo-500', badge: 'bg-indigo-100 text-indigo-800' },
  { name: 'pink', label: 'Rosa', bg: 'bg-pink-500', badge: 'bg-pink-100 text-pink-800' },
  { name: 'orange', label: 'Naranja', bg: 'bg-orange-500', badge: 'bg-orange-100 text-orange-800' },
  { name: 'teal', label: 'Verde azulado', bg: 'bg-teal-500', badge: 'bg-teal-100 text-teal-800' },
  { name: 'cyan', label: 'Cian', bg: 'bg-cyan-500', badge: 'bg-cyan-100 text-cyan-800' },
  { name: 'emerald', label: 'Esmeralda', bg: 'bg-emerald-500', badge: 'bg-emerald-100 text-emerald-800' }
])

const availableIcons = ref([
  { name: 'folder', label: 'Carpeta', component: FolderIcon },
  { name: 'document', label: 'Documento', component: DocumentTextIcon },
  { name: 'shield', label: 'Escudo', component: ShieldCheckIcon },
  { name: 'academic', label: 'Académico', component: AcademicCapIcon },
  { name: 'question', label: 'Pregunta', component: QuestionMarkCircleIcon },
  { name: 'settings', label: 'Configuración', component: CogIcon },
  { name: 'users', label: 'Usuarios', component: UserGroupIcon },
  { name: 'chart', label: 'Gráfico', component: ChartBarIcon },
  { name: 'money', label: 'Dinero', component: BanknotesIcon },
  { name: 'globe', label: 'Globo', component: GlobeAltIcon },
  { name: 'building', label: 'Edificio', component: BuildingOfficeIcon },
  { name: 'truck', label: 'Camión', component: TruckIcon }
])

// Computed properties
const isFormValid = computed(() => {
  return form.value.name && form.value.key && form.value.color && form.value.icon
})

// Methods
const handleBackdropClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close')
  }
}

const getColorClasses = (colorName) => {
  const color = availableColors.value.find(c => c.name === colorName)
  if (!color) {
    return {
      bg: 'bg-gray-100',
      text: 'text-gray-600',
      badge: 'bg-gray-100 text-gray-800'
    }
  }
  
  return {
    bg: color.bg.replace('bg-', 'bg-').replace('-500', '-100'),
    text: color.bg.replace('bg-', 'text-').replace('-500', '-600'),
    badge: color.badge
  }
}

const getIconComponent = (iconName) => {
  const icon = availableIcons.value.find(i => i.name === iconName)
  return icon ? icon.component : FolderIcon
}

const generateKey = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, '_')
    .substring(0, 20)
}

const saveCategory = async () => {
  if (!isFormValid.value) return
  
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const categoryData = {
      ...form.value,
      id: editingCategory.value ? props.category.id : Date.now()
    }
    
    emit('save', categoryData)
    emit('close')
  } catch (error) {
    console.error('Error saving category:', error)
    alert('Error al guardar la categoría. Inténtalo de nuevo.')
  } finally {
    isLoading.value = false
  }
}

// Watch for name changes to auto-generate key
watch(() => form.value.name, (newName) => {
  if (newName && !editingCategory.value) {
    form.value.key = generateKey(newName)
  }
})

// Initialize form with category data if editing
onMounted(() => {
  if (editingCategory.value) {
    form.value = {
      name: props.category.name || '',
      key: props.category.key || '',
      description: props.category.description || '',
      color: props.category.color || 'blue',
      icon: props.category.icon || 'folder',
      isDefault: props.category.isDefault || false,
      requiresApproval: props.category.requiresApproval || false,
      isActive: props.category.isActive !== false
    }
  }
})
</script>