import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/BotsPage/index.vue'

const moduleName = 'Bots'

const moduleRoutes: RouteRecordRaw = {
  path: '/bots',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/BotsPage/main.vue'),
      meta: {
        title: 'Bots',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/BotsPage/detail.vue'),
      meta: {
        title: 'Bot Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/BotsPage/detail.vue'),
      meta: {
        title: 'New Bot',
      },
    },
  ],
}

export default moduleRoutes

