import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/ConversationsPage/index.vue'

const moduleName = 'Conversations'

const moduleRoutes: RouteRecordRaw = {
  path: '/conversations',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/ConversationsPage/main.vue'),
      meta: {
        title: 'Conversations',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/ConversationsPage/detail.vue'),
      meta: {
        title: 'Conversation Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/ConversationsPage/detail.vue'),
      meta: {
        title: 'New Conversation',
      },
    },
  ],
}

export default moduleRoutes

