// The error comes from two key issues:
// 1. You are trying to define errorhandler as a single object, but your code is a list of objects (array elements), which is a syntax error.
// 2. The import paths (using "@") may not be correctly resolved depending on your project's configuration.
// Here is the corrected code, defining errorhandler as an array of route objects:

const errorhandler = [
  // 404 Not Found
  {
    path: '/:pathMatch(.*)*',
    name: 'Page404',
    component: () => import(/* webpackChunkName: "Page404" */ '@/views/ErrorsPage/Page404.vue'),
    meta: {
      title: 'Page Not Found',
    },
  },
  // 401 Unauthorized
  {
    path: '/401',
    name: 'Page401',
    component: () => import(/* webpackChunkName: "Page401" */ '@/views/ErrorsPage/Page401.vue'),
    meta: {
      title: 'Unauthorized',
    },
  },
  // 412 Precondition Failed
  {
    path: '/412',
    name: 'Page412',
    component: () => import(/* webpackChunkName: "Page404" */ '@/views/ErrorsPage/Page412.vue'),
    meta: {
      title: 'Precondition Failed',
    },
  },
  // 500 Internal Server Error
  {
    path: '/500',
    name: 'Page500',
    component: () => import(/* webpackChunkName: "Page404" */ '@/views/ErrorsPage/Page500.vue'),
    meta: {
      title: 'Internal Server Error',
    },
  },
];
