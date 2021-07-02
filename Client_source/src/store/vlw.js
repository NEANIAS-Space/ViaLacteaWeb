export default {
  state: {
    resolution: 3,
    planes: 1,
    p1:0.0,
    p2:0.0,
    r1:0.1,
    r2:0.0,
    dl:0.0,
    db:0.0,
    toggle_cam:1,
    rotateX:true
  },
  getters: {
    CONE_RESOLUTION(state) {
      return state.resolution;
    },
    CONE_CAMERA(state) {
      return state.toggle_cam;
    },
    CONE_ROTATE(state) {
      return state.toggle_cam;
    },
      
    CONE_PLANES(state) {
      return state.planes;
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
    CONE_DL(state) {
                  return state.dl;
    },
    CONE_DB(state) {
                  return state.db;
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
        async CONE_SETDL({ state}, dl) {
          const dl1 = Number(dl);
          state.dl = dl1;

        },
        async CONE_SETDB({ state}, db) {
          const db1 = Number(db);
          state.db = db1;

        },
    async CONE_RESOLUTION_UPDATE({ state, dispatch }, resolution) {
      const r = Number(resolution);
      state.resolution = r;
      return dispatch('WS_UPDATE_RESOLUTION', r);
    },
    async CONE_PLANES_UPDATE({ state, dispatch }, planes) {
      const r = Number(planes);
      state.planes = r;
      
      return dispatch('WS_UPDATE_PLANES', r);
    },
    async CONE_SETCAMERAVIEW({ state, dispatch },toggle_cam) {
      const t = Number(toggle_cam);
      state.toggle_cam=toggle_cam;
      return dispatch('WS_UPDATE_CAMERAVIEW', t);
      //alert("camVal="+toggle_cam);
      //return dispatch('WS_UPDATE_PLANES', r);
    },
    async CONE_SETROTATE({ state, dispatch },rotateX) {
     const t = Boolean(rotateX);
      state.rotateX=!rotateX;
      return dispatch('WS_UPDATE_ROTATE', t);
      // alert(rotateX);
      
    },
    async CONE_XMLFITS_UPDATE({ state, dispatch }) {

          const r11=state.r1;
         
          const p11=state.p1;
          const p22=state.p2;
          
          const dl1=state.dl;
          const db1=state.db;
         

          var res =String(p11)+','+String(p22)+','+String(r11)+','+String(dl1)+','+String(db1);


          return dispatch('WS_UPDATE_XMLFITS', res);
        },
     
  },
};
