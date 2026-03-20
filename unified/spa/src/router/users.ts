import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/UsersPage/index.vue'

const moduleName = 'Users'

const moduleRoutes: RouteRecordRaw = {
  path: '/users',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/UsersPage/main.vue'),
      meta: {
        title: 'Users',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/UsersPage/detail.vue'),
      meta: {
        title: 'User Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/UsersPage/detail.vue'),
      meta: {
        title: 'New User',
      },
    },
  ],
}

export default moduleRoutes

