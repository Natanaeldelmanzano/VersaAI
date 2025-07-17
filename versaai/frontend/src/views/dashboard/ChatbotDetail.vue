<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <button
              @click="$router.go(-1)"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <ArrowLeftIcon class="-ml-0.5 mr-2 h-4 w-4" aria-hidden="true" />
              Back
            </button>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ chatbot.name }}</h1>
              <p class="text-sm text-gray-500">{{ chatbot.description }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <span
              :class="[
                'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                chatbot.status === 'active'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              ]"
            >
              {{ chatbot.status }}
            </span>
            <button
              @click="toggleChatbot"
              :class="[
                'inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2',
                chatbot.status === 'active'
                  ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
                  : 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
              ]"
            >
              {{ chatbot.status === 'active' ? 'Deactivate' : 'Activate' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ChatBubbleLeftRightIcon class="h-6 w-6 text-gray-400" aria-hidden="true" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Conversations</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.totalConversations }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <ClockIcon class="h-6 w-6 text-gray-400" aria-hidden="true" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Avg Response Time</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.avgResponseTime }}ms</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <FaceSmileIcon class="h-6 w-6 text-gray-400" aria-hidden="true" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Satisfaction Rate</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.satisfactionRate }}%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <CalendarIcon class="h-6 w-6 text-gray-400" aria-hidden="true" />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Last Active</dt>
                <dd class="text-lg font-medium text-gray-900">{{ formatDate(chatbot.lastActive) }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Configuration -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Configuration</h3>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label class="block text-sm font-medium text-gray-700">Model</label>
            <p class="mt-1 text-sm text-gray-900">{{ chatbot.model }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Temperature</label>
            <p class="mt-1 text-sm text-gray-900">{{ chatbot.temperature }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Max Tokens</label>
            <p class="mt-1 text-sm text-gray-900">{{ chatbot.maxTokens }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Created</label>
            <p class="mt-1 text-sm text-gray-900">{{ formatDate(chatbot.createdAt) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Conversations -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Recent Conversations</h3>
          <router-link
            :to="`/conversations?chatbot=${chatbot.id}`"
            class="text-sm font-medium text-primary-600 hover:text-primary-500"
          >
            View all
          </router-link>
        </div>
        <div class="flow-root">
          <ul role="list" class="-mb-8">
            <li v-for="(conversation, idx) in recentConversations" :key="conversation.id">
              <div class="relative pb-8">
                <span
                  v-if="idx !== recentConversations.length - 1"
                  class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                  aria-hidden="true"
                />
                <div class="relative flex space-x-3">
                  <div>
                    <span class="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center ring-8 ring-white">
                      <ChatBubbleLeftRightIcon class="h-5 w-5 text-white" aria-hidden="true" />
                    </span>
                  </div>
                  <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                    <div>
                      <p class="text-sm text-gray-500">
                        Conversation with <span class="font-medium text-gray-900">{{ conversation.user }}</span>
                      </p>
                      <p class="text-sm text-gray-500">{{ conversation.lastMessage }}</p>
                    </div>
                    <div class="text-right text-sm whitespace-nowrap text-gray-500">
                      <time :datetime="conversation.timestamp">{{ formatDate(conversation.timestamp) }}</time>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeftIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  FaceSmileIcon,
  CalendarIcon
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'

const route = useRoute()
const chatbotId = computed(() => route.params.id)

const chatbot = ref({
  id: '1',
  name: 'Customer Support Bot',
  description: 'AI assistant for customer support inquiries',
  status: 'active',
  model: 'gpt-3.5-turbo',
  temperature: 0.7,
  maxTokens: 2048,
  createdAt: new Date('2024-01-15'),
  lastActive: new Date()
})

const stats = ref({
  totalConversations: 1247,
  avgResponseTime: 850,
  satisfactionRate: 94,
})

const recentConversations = ref([
  {
    id: '1',
    user: 'John Doe',
    lastMessage: 'Thank you for your help!',
    timestamp: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
  },
  {
    id: '2',
    user: 'Jane Smith',
    lastMessage: 'How can I reset my password?',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
  },
  {
    id: '3',
    user: 'Bob Johnson',
    lastMessage: 'What are your business hours?',
    timestamp: new Date(Date.now() - 1000 * 60 * 60 * 4) // 4 hours ago
  }
])

const formatDate = (date) => {
  return format(new Date(date), 'MMM d, yyyy h:mm a')
}

const toggleChatbot = () => {
  chatbot.value.status = chatbot.value.status === 'active' ? 'inactive' : 'active'
}

onMounted(() => {
  // Load chatbot data based on route params
  console.log('Loading chatbot:', chatbotId.value)
})
</script>