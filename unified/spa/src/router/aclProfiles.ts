import type { RouteRecordRaw } from 'vue-router'
import BaseRoute from '@/views/AclProfilesPage/index.vue'

const moduleName = 'AclProfiles'

const moduleRoutes: RouteRecordRaw = {
  path: '/acl-profiles',
  component: BaseRoute,
  meta: {
    name: `${moduleName}Base`,
  },
  redirect: { name: `${moduleName}Main` },
  children: [
    {
      path: '',
      name: `${moduleName}Main`,
      component: () => import('@/views/AclProfilesPage/main.vue'),
      meta: {
        title: 'ACL Profiles',
      },
    },
    {
      path: ':_id',
      name: `${moduleName}Detail`,
      component: () => import('@/views/AclProfilesPage/detail.vue'),
      meta: {
        title: 'ACL Profile Detail',
      },
      props: true,
    },
    {
      path: 'new',
      name: `${moduleName}New`,
      component: () => import('@/views/AclProfilesPage/detail.vue'),
      meta: {
        title: 'New ACL Profile',
      },
    },
  ],
}

export default moduleRoutes

