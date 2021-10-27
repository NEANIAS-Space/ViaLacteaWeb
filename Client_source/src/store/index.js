// import Vue from 'vue';
import Vuex from 'vuex';

import vlw from 'vlw-base/src/store/vlw';
import wslink from 'vlw-base/src/store/wslink';

/* eslint-enable no-param-reassign */

function createStore() {
  return new Vuex.Store({
    modules: {
      vlw,
      wslink,
    },
  });
}

export default createStore;
