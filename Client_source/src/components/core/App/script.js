import { mapGetters, mapActions } from 'vuex';
import logo from 'vlw-base/src/assets/colorize.png';
import RemoteRenderingView from 'vlw-base/src/components/widgets/RemoteRenderingView';
//import { createOidcAuth, SignInType } from 'vlw-base/src/vue-oidc-client';
//import protocols from 'vlw-base/src/protocols';
import idsrvAuth from 'vlw-base/src/idsrvAuth';
import Sortable from 'sortablejs';




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
      headers2: [
        {
          text: ' ',
          align: 'start',
          sortable: false,
          value: 'name',
        },
      ],
      palettes: ["Default","Default Step","EField","Glow","Gray","MinMax","PhysicsContour","PureRed","PureGreen","PureBlue","Run1","Run2","Sar","Temperature","TenStep","VolRenGlow","VolRenRGB","VolRenRGB","VolRenTwoLev","AllYellow","AllCyane","AllViolet","AllWhite","AllBlack","AllRed","AllGreen","AllBlu"
      ],
      
      images: [
        {
           name: 'Make a query to load image',
            selected:true,
            visibility: true,
            opacity: 100,
            palette: "Gray",
            scale:1,
            id:0,
            
         },
        
      ],
      imOpacity:100,
      imPalette:"Gray",
      paletteScaleLog:false,
      editedIndex: -1,
      editedItem:[
      {
        name: 'image layer 1',
        visibility: true,
        selected: false,
        opacity: 100,
        palette: "Gray",
        scale:1,
        id:0,
      },],
      formTitle:"Default title",
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
      fist_image:'WS_IMAGEDESC',
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
      loadImage:'WS_LOADIMAGE',
      getInfoImage:'WS_GETINFO',
      movedLayersRow:'WS_MOVELAYERSROW',
      changeOpacity:'WS_CHANGEOPACITY',
      changeVisibility:'WS_CHANGEVISIBILITY',
      changePalette:'WS_CHANGEPALETTE',
      changeSelection:'WS_CHANGESELECTED',
      
     
    }),
    addTest()
    {
      var l=this.images.length-1;
      this.addImage("Test image"+String(l), "test");
    },
    setOpacity()
       {
         
         //var id=this.images[this.editedIndex].id
         var res=String(this.editedIndex)+","+String(this.imOpacity)
         console.log("Opacity for ", res )
         this.images[this.editedIndex].opacity=this.imOpacity;
         console.log(this.editedIndex," with opacity ", this.images[this.editedIndex].opacity)
         this.changeOpacity(res)
       },
       setPaletteScale()
       { //this.paletteScaleLog=!this.paletteScaleLog;
         console.log(this.paletteScaleLog);
         this.images[this.editedIndex].scale=this.paletteScaleLog;
         this.setPalette()
       },
     setPalette()
        {
          //var l=this.images.length-1;
          var id=this.images[this.editedIndex].id
          var sc=String("Log")
          if (this.paletteScaleLog){
            sc=String("Linear")
          }
          var res=String(this.editedIndex)+","+String(id)+","+String(this.imPalette)+","+sc
          //console.log("Palette for ", res )
          this.images[this.editedIndex].palette=this.imPalette;
          this.changePalette(res)
        },
      setVisibilityOn(item)
               {
      this.editedIndex = this.images.indexOf(item)
      this.editedItem = Object.assign({}, item)
      
      //var id=this.images[this.editedIndex].id
     
      var res=String(this.editedIndex)+",true"
      console.log("Visibility for ", res )
      this.images[this.editedIndex].visibility=true;
      this.changeVisibility(res)
               },
  setVisibilityOff(item)
  {
    this.editedIndex = this.images.indexOf(item)
    this.editedItem = Object.assign({}, item)
    //var id=item.id;
    
    var res=String(this.editedIndex)+",false"
    console.log(" Visibility for ", res )
    this.images[this.editedIndex].visibility=false;
    this.changeVisibility(res)
  },
    
    
    
        setSelectionOn(item)
                 {
        this.editedIndex = this.images.indexOf(item)
        this.editedItem = Object.assign({}, item)
        
        //var id=this.images[this.editedIndex].id
       
        var res=String(this.editedIndex)+",true"
        console.log("Selection for ", res )
        for (let i=0;i<this.images.length;i++)
        {
          this.images[i].selected=false;
        }
        this.images[this.editedIndex].selected=true;
        this.changeSelection(this.editedIndex)
                 },

    
    
    editItem (item) {
      this.formTitle=item.name;
      this.editedIndex = this.images.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.imOpacity=this.images[this.editedIndex].opacity;
      this.imPalette=this.images[this.editedIndex].palette;
      this.paletteScaleLog=this.images[this.editedIndex].scale;
      console.log(this.paletteScaleLog)
      this.dialog = true
    },
    
    deleteItem (item) {
      this.editedIndex = this.images.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },
    
    deleteItemConfirm () {
      this.images.splice(this.editedIndex, 1)
      //Add remote call to delete image
      this.closeDelete()
    },
    
    close () {
      this.dialog = false
      this.$nextTick(() => {
        
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
      this.editedItem = Object.assign({}, this.defaultItem)
      this.editedIndex = -1
    },
    
    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    
    onSetCamera() {
      //this.dialog=true;
      //alert(this.toggle_one);
    },
    saveOrder (event) {
         const movedItem = this.images.splice(event.oldIndex, 1)[0];
         this.images.splice(event.newIndex, 0, movedItem);
         //compute propper indexes
         var l=this.images.length-1;
         var oldI=this.images[event.oldIndex].id;
         var newI=this.images[event.newIndex].id;
         oldI=event.oldIndex;//l-oldI;
         newI=event.newIndex;//l-newI;
         //alert ("Moved from "+event.oldIndex+" to "+event.newIndex)
         var param=String(oldI)+','+String(newI)+','+String(newI);
         console.log (param)
         this.movedLayersRow(param);
       },
    //TODO: future 3D/2D
    gotoOther(url) {
      this.$appName =  "New value";
      this.$color = 'session_id'
      var param="/vlw2"+"?id="+this.main_session+'&local=False'+'&url='+encodeURIComponent(url);
      
      
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
            
            //this.updateFitslocal(fullp)
            
            var param="/vlw2"+"?id="+this.main_session+'&local=True'+'&url='+encodeURIComponent(fullp);
                 
                 
                 var route = this.$router.resolve({ path: param });
                // setTimeout(function() {
                   //your code to be executed after 1 second
                  
                   window.open(route.href,"_blank");
    },
    
    //GetInitial data
    getData() {
      //
      this.mini = !this.mini;
      this.overlay=false
      this.loadData().then((result) => {
             console.log("GetImageData");
             
             setTimeout(this.setFirstName,1500);
          
           });
    
      //.Cone.loadXMLFITS(res)
      /*fetch("data.json")
        .then(response => response.json())
        .then(data => (this.items = data));*/
    },
    setFirstName() {
        //
       if(this.fist_image==''){
         setTimeout(this.setFirstName,500);
       } else{
               this.images[0].name=this.fist_image;
               console.log("Setting image");
               console.log(this.fist_image);
             }
           },
   
    addImage(desc, url)
    {
      //images.length
      console.log("Images ")
      
      var l=this.images.length
      var name={"name": desc, "visibility": true, "selected":false,"opacity":100, "palette": "Gray", "scale": false, "id":l}
      this.images.push(name)
      //this.images.unshift(name)// - adds image on top
      console.log(this.images.length)
      this.loadImage(url);
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
        //alert ("2D to be implemented")
        var desc=item.survey+" "+item.overlap;
        this.addImage(desc, item.url);
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
      //console.log("begin")
      this.connect(token);
      //.then(() => {
      //  this.images[0].name=this.fist_image;
     // });
     
      
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
  directives: {
    sortableDataTable: {
      bind (el, binding, vnode) {
        const options = {
          animation: 150,
          onUpdate: function (event) {
            vnode.child.$emit('sorted', event)
          }
        }
        Sortable.create(el.getElementsByTagName('tbody')[0], options)
      }
    }
  },
};
