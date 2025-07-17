import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../../src/App.vue'

// Create router for testing
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } }
  ]
})

describe('App.vue', () => {
  it('renders properly', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.exists()).toBe(true)
  })

  it('has router-view', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.find('router-view').exists()).toBe(true)
  })
})