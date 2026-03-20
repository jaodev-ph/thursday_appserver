import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/MessagesPage/index.vue'

const moduleName = 'Messages'

const moduleRoutes: RouteRecordRaw = {
  path: '/messages',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/MessagesPage/main.vue'),
      meta: {
        title: 'Messages',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/MessagesPage/detail.vue'),
      meta: {
        title: 'Message Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/MessagesPage/detail.vue'),
      meta: {
        title: 'New Message',
      },
    },
  ],
}

export default moduleRoutes

