import vtkWSLinkClient from 'vtk.js/Sources/IO/Core/WSLinkClient';
import SmartConnect from 'wslink/src/SmartConnect';

import protocols from 'vlw-base/src/protocols';

import { connectImageStream } from 'vtk.js/Sources/Rendering/Misc/RemoteView';

// Bind vtkWSLinkClient to our SmartConnect
vtkWSLinkClient.setSmartConnectClass(SmartConnect);

export default {
  state: {
    client: null,
    config: null,
    busy: false,
    json: '[{}]',
  },
  getters: {
    WS_CLIENT(state) {
      return state.client;
    },
    WS_JSON(state) {
      return state.json;
    },
    WS_CONFIG(state) {
      return state.config;
    },
    WS_BUSY(state) {
      return !!state.busy;
    },
  },
  mutations: {
    WS_CLIENT_SET(state, client) {
      state.client = client;
    },
    WS_JSON_SET(state, json) {
      state.json = json;
    },
    WS_CONFIG_SET(state, config) {
      state.config = config;
    },
    WS_BUSY_SET(state, busy) {
      console.log('BUSY');
      state.busy = busy;
    },
  },
  actions: {
    WS_CONNECT({ state, commit, dispatch }) {
      // Initiate network connection
      const config = { application: 'cone' };

      // Custom setup for development (http:8080 / ws:1234)
      if (location.port === '8080') {
        // We suppose that we have dev server and that ParaView/VTK is running on port 1234
        config.sessionURL = `ws://${location.hostname}:1234/ws`;
        //config.sessionURL="ws://${location.hostname}/proxy?sessionId=${id}&path=ws";
        // config.sessionURL = `ws://192.168.1.49:1234/ws`;
        //  config.sessionURL = `ws://visivo-server.oact.inaf.it:1234/ws`;
      }

      const { client } = state;
      if (client && client.isConnected()) {
        client.disconnect(-1);
      }
      let clientToConnect = client;
      if (!clientToConnect) {
        clientToConnect = vtkWSLinkClient.newInstance({ protocols });
      }

      // Connect to busy store
      clientToConnect.onBusyChange((count) => {
        commit('WS_BUSY_SET', count);
      });
      clientToConnect.beginBusy();

      // Error
      clientToConnect.onConnectionError((httpReq) => {
        const message =
          (httpReq && httpReq.response && httpReq.response.error) ||
          `Connection error`;
        console.error(message);
        console.log(httpReq);
      });

      // Close
      clientToConnect.onConnectionClose((httpReq) => {
        const message =
          (httpReq && httpReq.response && httpReq.response.error) ||
          `Connection close`;
        console.error(message);
        console.log(httpReq);
      });

      // Connect
      clientToConnect
        .connect(config)
        .then((validClient) => {
          connectImageStream(validClient.getConnection().getSession());
          commit('WS_CLIENT_SET', validClient);
          clientToConnect.endBusy();

          // Now that the client is ready let's setup the server for us
          dispatch('WS_INITIALIZE_SERVER');
        })
        .catch((error) => {
          console.error(error);
        });
    },
    WS_INITIALIZE_SERVER({ state }) {
      if (state.client) {
        state.client
          .getRemote()
          .VLWBase.createVisualization()
          .catch(console.error);
      }
    },
    //new for relaunching
    WS_LOADURL({ state }) {
      if (state.client) {
        state.client.getRemote().VLWBase.loadURL().catch(console.error);
      }
    },
    WS_UPDATE_RESOLUTION({ state }, resolution) {
      if (state.client) {
        // var t0 = performance.now();

        //clientToConnect.beginBusy();
        state.client
          .getRemote()
          .VLWBase.updateResolution(resolution)
          .catch(console.error);
        //clientToConnect.endBusy();
        // var t1 = performance.now();
        //  console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.");
      }
    },
    WS_UPDATE_PLANES({ state }, planes) {
      if (state.client) {
        // var t0 = performance.now();

        //clientToConnect.beginBusy();
        state.client
          .getRemote()
          .VLWBase.updatePlanes(planes)
          .catch(console.error);
        //clientToConnect.endBusy();
        // var t1 = performance.now();
        //  console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.");
      }
    },
    WS_UPDATE_CAMERAVIEW({ state }, v) {
      if (state.client) {
        // var t0 = performance.now();

        //clientToConnect.beginBusy();
        state.client.getRemote().VLWBase.updateCamView(v).catch(console.error);
      }
    },
    WS_UPDATE_ROTATE({ state }, v) {
      if (state.client) {
        // var t0 = performance.now();

        //clientToConnect.beginBusy();
        state.client
          .getRemote()
          .VLWBase.updateRotateAxis(v)
          .catch(console.error);
      }
    },
    WS_FITS_UPDATE({ state }, url) {
      if (state.client) {
        state.client.getRemote().VLWBase.updateFits(url).catch(console.error);
      }
    },
    WS_UPDATE_XMLFITS({ state }, res) {
      if (state.client) {
        // console.log("Start loading fitx with parameters2 " + res);

        state.client
          .getRemote()
          .VLWBase.loadXMLFITS(res)
          .then((result) => {
            console.log('result ' + result);
            //if(!result)
            //alert(result);
            //commit('WS_JSON_SET', result);
            state.json = result;
            //alert(state.json);

            return state.json;
            //https://stackoverflow.com/questions/59699813/vuetify-data-table-and-binding-data-coming-from-json-object - get a table from json
            //also https://codepen.io/isogunro/pen/VQRoax
          });
        //
      }
    },
    WS_RESET_CAMERA({ state }) {
      if (state.client) {
        console.log('Start');
        state.client.getRemote().VLWBase.resetCamera().catch(console.error);
        console.log('END');
      }
    },
  },
};
