export default {
  state: {
    resolution: 6,
    p1:0.0,
    p2:0.0,
    r1:0.0,
    r2:0.0,
  },
  getters: {
    CONE_RESOLUTION(state) {
      return state.resolution;
    },
    CONE_P1(state) {
          return state.p1;
    },
    CONE_P2(state) {
              return state.p2;
    },
    CONE_R2(state) {
                  return state.r2;
    },
    CONE_R1(state) {
             console.log("Start loading fitx with parameters ");
                  return state.r1;
    },
  },
  actions: {
        async CONE_SETP1({ state}, p1) {
          const p11 = Number(p1);
          state.p1 = p11;

        },
        async CONE_SETP2({ state}, p2) {
          const p22 = Number(p2);
          state.p2 = p22;

        },
        async CONE_SETR1({ state}, r1) {
          const r11 = Number(r1);
          state.r1 = r11;

        },
    async CONE_RESOLUTION_UPDATE({ state, dispatch }, resolution) {
      const r = Number(resolution);
      state.resolution = r;
      return dispatch('WS_UPDATE_RESOLUTION', r);
    },
    async CONE_XMLFITS_UPDATE({ state, dispatch }) {

          const r11=state.r1;
          const r22=state.r2;
          const p11=state.p1;
          const p22=state.p2;
          this.dialog = false;

            var res =String(p11)+','+String(p22)+','+String(r11)+','+String(r22)


          return dispatch('WS_UPDATE_XMLFITS', res);
        },
  },
};
