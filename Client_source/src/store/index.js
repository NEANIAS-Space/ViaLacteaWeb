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
      state: {
        $color: 'green'
      },
      mutations: {
        update$color: function(state, newColor) { state.$color = newColor; }
      }
  });
}

export default createStore;
