<template>
  <nav class="sidebar-nav">
    <div class="space-y-1">
      <router-link
        v-for="item in navigation"
        :key="item.name"
        :to="item.href"
        :class="[
          item.current
            ? 'sidebar-nav-item-active'
            : 'sidebar-nav-item-inactive',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        ]"
      >
        <component
          :is="item.icon"
          :class="[
            item.current ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500',
            'mr-3 flex-shrink-0 h-6 w-6'
          ]"
          aria-hidden="true"
        />
        {{ item.name }}
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  BookOpenIcon,
  ChartBarIcon,
  UsersIcon,
  CogIcon,
  BuildingOfficeIcon,
  SparklesIcon,
  LinkIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()

const navigation = computed(() => [
  {
    name: 'Resumen',
    href: '/dashboard',
    icon: HomeIcon,
    current: route.path === '/dashboard'
  },
  {
    name: 'Chat AI',
    href: '/dashboard/chat',
    icon: SparklesIcon,
    current: route.path.startsWith('/dashboard/chat')
  },
  {
    name: 'Chatbots',
    href: '/dashboard/chatbots',
    icon: ChatBubbleLeftRightIcon,
    current: route.path.startsWith('/dashboard/chatbots')
  },
  {
    name: 'Conversaciones',
    href: '/dashboard/conversations',
    icon: ChatBubbleLeftRightIcon,
    current: route.path.startsWith('/dashboard/conversations')
  },
  {
    name: 'Base de Conocimiento',
    href: '/dashboard/knowledge-bases',
    icon: BookOpenIcon,
    current: route.path.startsWith('/dashboard/knowledge-bases')
  },
  {
    name: 'Analíticas',
    href: '/dashboard/analytics',
    icon: ChartBarIcon,
    current: route.path.startsWith('/dashboard/analytics')
  },
  {
    name: 'Integraciones',
    href: '/dashboard/integrations',
    icon: LinkIcon,
    current: route.path.startsWith('/dashboard/integrations')
  },
  {
    name: 'Usuarios',
    href: '/dashboard/users',
    icon: UsersIcon,
    current: route.path.startsWith('/dashboard/users')
  },
  {
    name: 'Organización',
    href: '/dashboard/organization',
    icon: BuildingOfficeIcon,
    current: route.path.startsWith('/dashboard/organization')
  },
  {
    name: 'Configuración',
    href: '/dashboard/settings',
    icon: CogIcon,
    current: route.path.startsWith('/dashboard/settings')
  }
])
</script>

<style scoped>
.sidebar-nav-item-active {
  @apply bg-primary-100 text-primary-900;
}

.sidebar-nav-item-inactive {
  @apply text-gray-600 hover:bg-gray-50 hover:text-gray-900;
}
</style>