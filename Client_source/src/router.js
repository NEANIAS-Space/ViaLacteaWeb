import Vue from 'vue';
import VueRouter from 'vue-router';
import App from 'vlw-base/src/components/core/App';
import Home from 'vlw-base/src/views/Home.vue';
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
    name: 'Home',
    component: Home,
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
