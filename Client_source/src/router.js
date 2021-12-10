import Vue from 'vue';
import VueRouter from 'vue-router';
import App from 'vlw-base/src/components/core/App';
import App2 from 'vlw-base/src/components/core/App2';
import Hello from 'vlw-base/src/components/core/Hello';
import idsrvAuth from 'vlw-base/src/idsrvAuth';
Vue.use(VueRouter);
const routes = [
  //  {
  //    path: '/',
  //    name: 'App',
  //meta: {
  //  authName: idsrvAuth.authName,
  //},
  //    component: App,
  //  },
  {
    path: '/',
    name: 'Hello',
    component: Hello,
  },
  {
    path: '/vlw',
    name: 'App',
    meta: {
      authName: idsrvAuth.authName,
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: App,
  },
    {
      path: '/vlw2',
      name: 'App2',
      meta: {
        authName: idsrvAuth.authName,
      },
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: App2,
    },
  {
    path: '/main2',
    name: 'VLW2',
    meta: {
      authName: idsrvAuth.authName,
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ 'vlw-base/src/views/VLW.vue'),
  },
];
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
idsrvAuth.useRouter(router);
export default router;
//# sourceMappingURL=router.js.map
