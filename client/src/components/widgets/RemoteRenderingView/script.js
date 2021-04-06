import vtkRemoteView from 'vtk.js/Sources/Rendering/Misc/RemoteView';
//import vtkFPSMonitor from 'vtk.js/Sources/Interaction/UI/FPSMonitor';

//import controlPanel from './controller.html';

export default {
  name: 'RemoteRenderView',
  props: {
    viewId: {
      type: String,
      default: '-1',
    },
    client: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      connected: false,
    };
  },
  created() {
    this.view = vtkRemoteView.newInstance({
      rpcWheelEvent: 'viewport.mouse.zoom.wheel',
    });
    // default of 0.5 causes 2x size labels on high-DPI screens. 1 good for demo, not for production.
    if (location.hostname.split('.')[0] === 'localhost') {
      this.view.setInteractiveRatio(1);
    }
    //var rend=this.view.getRenderer()
    //https://kitware.github.io/vtk-js/examples/Cone.html
    /*var inter=this.view.getInteractor();
    var win=inter.getRenderWindow();
    const fpsMonitor = vtkFPSMonitor.newInstance();
    const fpsElm = fpsMonitor.getFpsMonitorContainer();
    fpsElm.style.position = 'absolute';
    fpsElm.style.left = '10px';
    fpsElm.style.bottom = '10px';
    fpsElm.style.background = 'rgba(255,255,255,0.5)';
    fpsElm.style.borderRadius = '5px';

    //var cont=this.view.getContainer();
    //const divMain = document.createElement('div');
    //this.$el.appendChild(divMain);

    fpsMonitor.setContainer(document.querySelector('body'));
    //document.querySelector('.v-main__wrap')

    //fpsMonitor.setContainer(divMain);
    fpsMonitor.setRenderWindow(win);*/

  },
  mounted() {
    this.view.setContainer(this.$el);

    window.addEventListener('resize', this.view.resize);
    this.connect();
  },
  methods: {
    connect() {
      if (this.client) {
        //console.log('RemoteRenderView', this.viewId);
        const session = this.client.getConnection().getSession();
        this.view.setSession(session);
        this.view.setViewId(this.viewId);
        this.connected = true;
        this.view.render();
      }
    },
    handleClick(event) {
      this.onClick(event);
    },
  },
  watch: {
    client() {
      this.connect();
    },
    viewId(id) {
      //console.log('RemoteRenderView', id);
        //https://kitware.github.io/paraviewweb/api/React_Renderers_VtkGeometryRenderer.html
      if (this.connected) {
        this.view.setViewId(id);
        this.view.render();
      }
    },
    enablePicking(value) {
      this.view.getInteractorStyle().setSendMouseMove(value);
    },
  },
  beforeDestroy() {
    if (this.subscription) {
      this.subscription.unsubscribe();
      this.subscription = null;
    }
    window.removeEventListener('resize', this.view.resize);
    this.view.delete();
  },
};
