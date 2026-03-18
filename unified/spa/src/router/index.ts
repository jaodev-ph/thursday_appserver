import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  // Placeholder routes so the sidebar links work.
  // Replace these with real CRUD pages later.
  { path: '/tenants', name: 'tenants', component: () => import('@/views/HomeView.vue') },
  { path: '/bots', name: 'bots', component: () => import('@/views/HomeView.vue') },
  { path: '/customers', name: 'customers', component: () => import('@/views/HomeView.vue') },
  { path: '/conversations', name: 'conversations', component: () => import('@/views/HomeView.vue') },
  { path: '/messages', name: 'messages', component: () => import('@/views/HomeView.vue') },
  { path: '/users', name: 'users', component: () => import('@/views/HomeView.vue') },
  { path: '/billings', name: 'billings', component: () => import('@/views/HomeView.vue') },
  { path: '/acl-profiles', name: 'acl-profiles', component: () => import('@/views/HomeView.vue') },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
