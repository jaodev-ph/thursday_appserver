import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/CustomersPage/index.vue'

const moduleName = 'Customers'

const moduleRoutes: RouteRecordRaw = {
  path: '/customers',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/CustomersPage/main.vue'),
      meta: {
        title: 'Customers',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/CustomersPage/detail.vue'),
      meta: {
        title: 'Customer Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/CustomersPage/detail.vue'),
      meta: {
        title: 'New Customer',
      },
    },
  ],
}

export default moduleRoutes

