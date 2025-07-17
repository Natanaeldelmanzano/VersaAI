<template>
  <Menu as="div" class="relative inline-block text-left">
    <div>
      <MenuButton class="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
        <span class="sr-only">Open user menu</span>
        <img
          class="h-8 w-8 rounded-full"
          :src="user.avatar || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(user.name) + '&background=6366f1&color=fff'"
          :alt="user.name"
        />
      </MenuButton>
    </div>

    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <MenuItems class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
        <div class="py-1">
          <div class="px-4 py-3">
            <p class="text-sm">Signed in as</p>
            <p class="text-sm font-medium text-gray-900 truncate">{{ user.email }}</p>
          </div>
          
          <div class="border-t border-gray-100"></div>
          
          <MenuItem v-slot="{ active }">
            <router-link
              to="/profile"
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'flex items-center px-4 py-2 text-sm'
              ]"
            >
              <UserIcon class="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
              Your Profile
            </router-link>
          </MenuItem>
          
          <MenuItem v-slot="{ active }">
            <router-link
              to="/settings"
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'flex items-center px-4 py-2 text-sm'
              ]"
            >
              <CogIcon class="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
              Settings
            </router-link>
          </MenuItem>
          
          <div class="border-t border-gray-100"></div>
          
          <MenuItem v-slot="{ active }">
            <button
              @click="handleSignOut"
              :class="[
                active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                'flex w-full items-center px-4 py-2 text-left text-sm'
              ]"
            >
              <ArrowRightOnRectangleIcon class="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
              Sign out
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import {
  UserIcon,
  CogIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const user = computed(() => authStore.user || {
  name: 'John Doe',
  email: 'john@example.com',
  avatar: null
})

const handleSignOut = async () => {
  try {
    await authStore.logout()
    toast.success('Successfully signed out')
    router.push('/login')
  } catch (error) {
    console.error('Sign out error:', error)
    toast.error('Failed to sign out')
  }
}
</script>