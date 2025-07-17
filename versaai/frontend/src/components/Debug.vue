<template>
  <div class="fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 border border-gray-200 z-50 min-w-[300px]">
    <h3 class="text-lg font-semibold text-gray-900 mb-3">Debug Info</h3>
    
    <div class="space-y-2 text-sm">
      <div class="flex justify-between items-center">
        <span class="text-gray-600">App Loading:</span>
        <span :class="appStore.isLoading ? 'text-red-600' : 'text-green-600'">
          {{ appStore.isLoading ? 'TRUE' : 'FALSE' }}
        </span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-gray-600">Initializing:</span>
        <span :class="isInitializing ? 'text-red-600' : 'text-green-600'">
          {{ isInitializing ? 'TRUE' : 'FALSE' }}
        </span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-gray-600">Auth Status:</span>
        <span :class="authStore.isAuthenticated ? 'text-green-600' : 'text-yellow-600'">
          {{ authStore.isAuthenticated ? 'AUTHENTICATED' : 'NOT AUTH' }}
        </span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-gray-600">Current Route:</span>
        <span class="text-blue-600 font-mono">
          {{ route.path }}
        </span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-gray-600">Router View:</span>
        <span :class="(!appStore.isLoading && !isInitializing) ? 'text-green-600' : 'text-red-600'">
          {{ (!appStore.isLoading && !isInitializing) ? 'VISIBLE' : 'HIDDEN' }}
        </span>
      </div>
      
      <div class="flex justify-between items-center">
        <span class="text-gray-600">Online:</span>
        <span :class="appStore.isOnline ? 'text-green-600' : 'text-red-600'">
          {{ appStore.isOnline ? 'YES' : 'NO' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

// Get injected state
const isInitializing = inject('isInitializing')

// Stores and route
const route = useRoute()
const authStore = useAuthStore()
const appStore = useAppStore()
</script>