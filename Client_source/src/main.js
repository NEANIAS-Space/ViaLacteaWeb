// Import polyfills
import 'core-js/modules/es7.promise.finally';
import 'core-js/modules/web.immediate';

import Vue from 'vue';
import Vuex from 'vuex';

import App from 'vlw-base/src/components/core/App';
//import App from 'vlw-base/src/App.vue';
import vuetify from 'vlw-base/src/plugins/vuetify.js';
import store from 'vlw-base/src/store';
//import router from 'vlw-base/src/router';
import idsrvAuth from 'vlw-base/src/idsrvAuth';

/* eslint-disable-next-line import/extensions */
import 'typeface-roboto';
import 'vuetify/dist/vuetify.min.css';
//import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css';
Vue.use(Vuex);

Vue.config.devtools = true;
Vue.config.performance = true;
Vue.config.performance = process.env.NODE_ENV !== 'production';

idsrvAuth.startup().then((ok) => {
  if (ok) {
    new Vue({
      vuetify,
      store,
    //  router,
      render: (h) => h(App),
    }).$mount('#app');
    console.log('Startup is set');
  } else {
    console.log('Startup was not ok');
  }
});
