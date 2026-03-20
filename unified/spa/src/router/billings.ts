import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/BillingsPage/index.vue'

const moduleName = 'Billings'

const moduleRoutes: RouteRecordRaw = {
  path: '/billings',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/BillingsPage/main.vue'),
      meta: {
        title: 'Billings',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/BillingsPage/detail.vue'),
      meta: {
        title: 'Billing Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/BillingsPage/detail.vue'),
      meta: {
        title: 'New Billing',
      },
    },
  ],
}

export default moduleRoutes

