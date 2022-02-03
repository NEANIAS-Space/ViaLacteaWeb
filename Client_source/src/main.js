// Import polyfills
import 'core-js/modules/es7.promise.finally';
import 'core-js/modules/web.immediate';

import Vue from 'vue';
import Vuex from 'vuex';


//import App from 'vlw-base/src/components/core/App';
import App from 'vlw-base/src/App.vue';
import vuetify from 'vlw-base/src/plugins/vuetify.js';
import store from 'vlw-base/src/store';
import router from 'vlw-base/src/router';
import idsrvAuth from 'vlw-base/src/idsrvAuth';

/* eslint-disable-next-line import/extensions */
import 'typeface-roboto';
import 'vuetify/dist/vuetify.min.css';
//import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css';
import TreeView from "vue-json-tree-view"

Vue.use(Vuex);
Vue.use(vuetify)
Vue.use(TreeView)
Vue.config.devtools = true;
Vue.config.performance = true;
Vue.config.performance = process.env.NODE_ENV !== 'production';

let globalData = new Vue({
  data: { $color: 'green' }
});
Vue.mixin({
  computed: {
    $color: {
      get: function () { return globalData.$data.$color },
      set: function (newColor) { globalData.$data.$color = newColor; }
    }
  }
})
Vue.prototype.$appName = 'test';

idsrvAuth.startup().then((ok) => {
  if (ok) {
    new Vue({
      vuetify,
      store,
      router,
      render: (h) => h(App),
    }).$mount('#app');
    console.log('Startup is set');
    
    //console.log(dirTree);
    //const tree = dirTree('/home/evgeniya/Documents/GitHub/files');
   // const tree = dirTree('/home/evgeniya/Documents/GitHub/files', {extensions:/\.fits$/}, (item, PATH, stats) => {
   //   console.log(item);
   // });
    
  
    //alert (store)
   // console.log('Files browsed');
  } else {
    console.log('Startup was not ok');
  }
  
  
  //const dirTree = require("directory-tree");
  //const tree = dirTree("/home/evgeniya/Documents/GitHub/files/");
  //alert (tree);//JSON.stringify(tree));
  
});



Vue.prototype.$store = store
