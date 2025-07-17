<template>
  <nav class="flex" aria-label="Breadcrumb">
    <ol role="list" class="flex items-center space-x-4">
      <li>
        <div>
          <router-link to="/dashboard" class="text-gray-400 hover:text-gray-500">
            <HomeIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
            <span class="sr-only">Inicio</span>
          </router-link>
        </div>
      </li>
      <li v-for="(page, index) in pages" :key="page.name">
        <div class="flex items-center">
          <ChevronRightIcon class="h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
          <router-link
            v-if="page.href"
            :to="page.href"
            :class="[
              index === pages.length - 1
                ? 'text-gray-500'
                : 'text-gray-400 hover:text-gray-500',
              'ml-4 text-sm font-medium'
            ]"
            :aria-current="index === pages.length - 1 ? 'page' : undefined"
          >
            {{ page.name }}
          </router-link>
          <span
            v-else
            class="ml-4 text-sm font-medium text-gray-500"
            :aria-current="index === pages.length - 1 ? 'page' : undefined"
          >
            {{ page.name }}
          </span>
        </div>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

const route = useRoute()

const pages = computed(() => {
  const pathSegments = route.path.split('/').filter(Boolean)
  const breadcrumbs = []
  
  // Skip the first segment if it's 'dashboard'
  const segments = pathSegments[0] === 'dashboard' ? pathSegments.slice(1) : pathSegments
  
  let currentPath = '/dashboard'
  
  segments.forEach((segment, index) => {
    currentPath += `/${segment}`
    
    // Convert segment to readable name
    const name = segment
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
    
    breadcrumbs.push({
      name,
      href: index === segments.length - 1 ? null : currentPath
    })
  })
  
  return breadcrumbs
})
</script>