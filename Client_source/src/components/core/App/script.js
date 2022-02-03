import { mapGetters, mapActions } from 'vuex';
import logo from 'vlw-base/src/assets/colorize.png';
import RemoteRenderingView from 'vlw-base/src/components/widgets/RemoteRenderingView';
//import { createOidcAuth, SignInType } from 'vlw-base/src/vue-oidc-client';
//import protocols from 'vlw-base/src/protocols';
import idsrvAuth from 'vlw-base/src/idsrvAuth';




//const dirTree = require("directory-tree");
// ----------------------------------------------------------------------------
// Component API
// ----------------------------------------------------------------------------

export default {
  name: 'App',
  components: {
    RemoteRenderingView,
  },
    meta: {
      authName: idsrvAuth.authName,
    },

  data() {
    return {
      dialog: false,
      lfDialog:false,
      mes:"Loading",
      overlay: true,
      
      /*toggle_one: 1,*/
      logo,
      ex1: { label: 'Threshold', val: 3.0, color: 'orange darken-3' },
      ex2: { label: 'Cutting planes', val: 1, color: 'green lighten-1' },
      ex3: { label: 'Lower bound', val: 50, color: 'red' },
      ex4: { label: 'Level', val: 50, color: 'red' },
      drawer: true,
      mini: true,
      myImage: require('@/assets/OPEN_LOCAL.png'),

      right: null,
      rtoken:'',
      

      //GetInitial data
      singleSelect: true,
      selected: [{ url: 'FOR_INSTANCE' }],
      search: '',
      headers: [
        /*  {
          text: 'Dessert (100g serving)',
          align: 'left',
          sortable: false,
          value: 'name'
        },*/
        { text: 'Survey/species', value: 'survey' },
        { text: 'Desc', value: 'overlap' },
      ],
      items: [],
      weatherDataList: [],
    };
  },
  computed: {
    ...mapGetters({
      client: 'WS_CLIENT',
      busy: 'WS_BUSY',
      resolution: 'CONE_RESOLUTION',
      planes: 'CONE_PLANES',
      contours: 'CONE_CONTOURS',
      p1: 'CONE_P1',
      p2: 'CONE_P2',
      r1: 'CONE_R1',
      r2: 'CONE_R2',
      dl: 'CONE_DL',
      db: 'CONE_DB',
      out_json: 'WS_JSON',
      params: 'WS_PARAMS',
      toggle_cam: 'CONE_CAMERA',
      rotateX: 'CONE_ROTATE',
      is2D: 'CONE_2D',
      out_files:'WS_JSONFILES',
      main_session:'WS_MAIN_SESSION',
    }),
  },
  methods: {
    ...mapActions({
      setResolution: 'CONE_RESOLUTION_UPDATE',
      setPlanes: 'CONE_PLANES_UPDATE',
      setContours: 'CONE_CONTOURS_UPDATE',
      resetCamera: 'WS_RESET_CAMERA',
      connect: 'WS_CONNECT',
      loadData: 'CONE_XMLFITS_UPDATE',
      loadDataShort: 'WS_FITS_UPDATE',
      keyLogOut: 'WS_LOGOUT',
      updateToken: 'WS_UPDATE_TOKEN',
      setP1: 'CONE_SETP1',
      setP2: 'CONE_SETP2',
      setR1: 'CONE_SETR1',
      setDl: 'CONE_SETDL',
      setDb: 'CONE_SETDB',
      setCameraView: 'CONE_SETCAMERAVIEW',
      setRotate: 'CONE_SETROTATE',
      set2D:'CONE_SET2D',
      updateFitslocal:'WS_UPDATELOCALFITS',

      
     
    }),
    onSetCamera() {
      //this.dialog=true;
      //alert(this.toggle_one);
    },
    //TODO: future 3D/2D
    gotoOther(url) {
      this.$appName =  "New value";
      this.$color = 'session_id'
      var param="/vlw2"+"?id="+this.main_session+'&url='+encodeURIComponent(url);
      
      
      var route = this.$router.resolve({ path: param });
     // setTimeout(function() {
        //your code to be executed after 1 second
       
        window.open(route.href,"_blank");
     // }, 1000);
      
    },
   testFile() {
      if (this.active.length>0)
    {
      var l=this.active.length-1
      console.log('TEST', this.active[l])
      //this.active.splice(0, 1)
    }
    },
    loadFile(item)
    {      this.lfDialog = false;
            var fullp=item.path+"/"+item.name;
            console.log(fullp)
            //TODO integrate file opening
            //this.gotoOther("testFile_url");
            this.updateFitslocal(fullp)
    },
    
    //GetInitial data
    getData() {
      //
      this.mini = !this.mini;
      this.overlay=false
      this.loadData();

      //.Cone.loadXMLFITS(res)
      /*fetch("data.json")
        .then(response => response.json())
        .then(data => (this.items = data));*/
    },
    onLoadToken()
    {
      //getTokenId
      
      var token=this.$oidc.accessToken;
      //alert(token);
      var s=this.$oidc.authName;
      console.log("Update token timeout")
      console.log(s);
      this.updateToken(token);
      this.$oidc.resetUpdate(); //set back to false
    },
    onLogOut()
    {
      //getTokenId


      //alert(token);
      //var s=this.$oidc.authName;
      //console.log("Log out start")
      //alert(this.rtoken);
      this.keyLogOut(this.rtoken);
      this.$oidc.resetUpdate(); //set back to false
      this.$oidc.signOut();
    },
    checkToken()
       {
         //getTokenId
         
        var s=this.$oidc.needsUpdate;
        //alert(s)
        if(s)
        {
          setTimeout(this.onLoadToken,2500);
        }
          
       },
    onButtonClick(item) {
      this.mini = !this.mini;
      var is3D=parseInt(item.species)
      console.log(is3D)
      if (is3D==0) {
        //this.loadDataShort(item.url); //3d loading
        alert ("2D to be implemented")
        this.loadDataShort(item.url);
      } else {
        //TODO check data transmission
        this.gotoOther(item.url);
      }
      //.then(
      //    function(configResponse) {
      //        return alert("Done");
      //    }
      //)
      //alert('click on ' + item.url)
    },

    hideDialogAndProceed: function () {
      //this.getData();
      this.dialog = false;
      this.loadData();
    },
  },
    
   // created: function() {
   //   if(!this.$oidc.isAuthenticated){
  //         this.$oidc.signIn();
   //      }
  //  },

  mounted() {
   // if(!this.$oidc.isAuthenticated){
 //     this.$oidc.signIn();
 //   }
      
  //  else{
      //this.onLoadToken();
      var token=this.$oidc.accessToken;
      this.rtoken=this.$oidc.refreshToken;

      //this.callFunction();
      //this.updateToken(token);
      console.log("begin")
      this.connect(token);
      //this.mes="2D window";
      setInterval(this.checkToken,1000);
      
      //
      //setInterval(this.onLoadToken,1500);
      //setInterval(this.onLoadToken, 900000);
      
      //this.onLoadToken();
      
      //Loading directory tree
      //const dirTree = require("directory-tree");
     // const tree = dirTree("/home/evgeniya/Documents/GitHub/files/");
      //alert (tree);//JSON.stringify(tree));
      //const tree = dirTree('/home/evgeniya/Documents/GitHub/files', {extensions:/\.fits$/}, null, (item, PATH, stats) => {
     //   console.log(tree);
      //});
 //   }
    
  },
};
