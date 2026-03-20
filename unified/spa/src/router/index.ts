import { createRouter, createWebHistory } from 'vue-router'
import tenants from './tenants'
import bots from './bots'
import customers from './customers'
import conversations from './conversations'
import messages from './messages'
import users from './users'
import billings from './billings'
import aclProfiles from './aclProfiles'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  tenants,
  bots,
  customers,
  conversations,
  messages,
  users,
  billings,
  aclProfiles,
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
