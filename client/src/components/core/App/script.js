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
    }),
  },
  methods: {
    ...mapActions({
      setResolution: 'CONE_RESOLUTION_UPDATE',
      resetCamera: 'WS_RESET_CAMERA',
      connect: 'WS_CONNECT',
    }),
  },
  mounted() {
    this.connect();
  },
};
