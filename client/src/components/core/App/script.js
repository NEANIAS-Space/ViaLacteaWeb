import { mapGetters, mapActions } from 'vuex';
import logo from 'vue-vtkjs-pvw-template/src/assets/colorize.png';
import RemoteRenderingView from 'vue-vtkjs-pvw-template/src/components/widgets/RemoteRenderingView';

// ----------------------------------------------------------------------------
// Component API
// ----------------------------------------------------------------------------

export default {
  name: 'App',
  components: {
    RemoteRenderingView,
  },
  data() {
    return {
      dialog: true,
      logo,
      myImage: require('@/assets/OPEN_LOCAL.png'),
      items: [
         { title: 'Dashboard', icon: 'mdi-view-dashboard' },
         { title: 'Photos', icon: 'mdi-image' },
         { title: 'About', icon: 'mdi-help-box' },
       ],
       right: null,
    };
  },
  computed: {
    ...mapGetters({
      client: 'WS_CLIENT',
      busy: 'WS_BUSY',
      resolution: 'CONE_RESOLUTION',
      p1:'CONE_P1',
      p2:'CONE_P2',
      r1:'CONE_R1',
      r2:'CONE_R2',
    }),
  },
  methods: {
    ...mapActions({
      setResolution: 'CONE_RESOLUTION_UPDATE',
      resetCamera: 'WS_RESET_CAMERA',
      connect: 'WS_CONNECT',
      loadData:'CONE_XMLFITS_UPDATE',
      setP1:'CONE_SETP1',
      setP2:'CONE_SETP2',
      setR1:'CONE_SETR1',

    }),
    hideDialogAndProceed: function()
    {
        this.dialog=false;
        this.loadData();
    }

  },
  mounted() {
    this.connect();
  },
};
