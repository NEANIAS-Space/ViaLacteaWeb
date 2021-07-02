import vtkRemoteView from 'vtk.js/Sources/Rendering/Misc/RemoteView';
import vtkInteractorStyleRemoteMouse from 'vtk.js/Sources/Interaction/Style/InteractorStyleRemoteMouse';

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
      rpcGestureEvent: 'viewport.gesture',
     // rpcMouseEvent: 'viewport.mouse.move',
    });
    // default of 0.5 causes 2x size labels on high-DPI screens. 1 good for demo, not for production.
    if (location.hostname.split('.')[0] === 'localhost') {
      this.view.setInteractiveRatio(1);
    }
    // this.view.interactorStyle = vtkInteractorStyleRemoteMouse.newInstance();
    // this.view.interactor.setInteractorStyle(this.view.interactorStyle);
        
   // this.view.interactorStyle.onRemoteGestureEvent((e) => {
   // if (this.view.getSession() && this.view.rpcGestureEvent) {
   //   this.view.getSession().call(this.view.rpcGestureEvent, [e]);
   //   alert("Gesture called");
      
  //  }
  //});
  //https://kitware.github.io/vtk-js/api/Rendering_Misc_RemoteView.htmls
  //https://github.com/Kitware/vtk-js/blob/master/Sources/Interaction/Style/InteractorStyleRemoteMouse/index.js#L309
  },
  mounted() {
    this.view.setContainer(this.$el);
    window.addEventListener('resize', this.view.resize);
    this.connect();
  },
  methods: {
    connect() {
      if (this.client) {
        // console.log('RemoteRenderView', this.viewId);
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
      // console.log('RemoteRenderView', id);
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
