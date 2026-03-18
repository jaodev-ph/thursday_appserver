import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/TenantPage/index.vue'

const moduleName = 'Tenant'

const moduleRoutes: RouteRecordRaw = {
  path: 'tenants',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`
  },
  redirect: { name: 'TenantMain' },
  children: [
    {
      path: '',
      name: 'TenantMain',
      component: () => import('@/views/TenantPage/main.vue'),
      meta: {
        title: 'Tenant',
      },
    },
    {
      path: ':_id',
      name: 'TenantDetail',
      component: () => import('@/views/TenantPage/detail.vue'),
      meta: {
        title: 'Tenant Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: 'TenantNew',
      component: () => import('@/views/TenantPage/detail.vue'),
      meta: {
        title: 'New Tenant',
      },
    },
  ],
}

export default moduleRoutes