(function(e){function t(t){for(var r,o,c=t[0],s=t[1],u=t[2],l=0,d=[];l<c.length;l++)o=c[l],a[o]&&d.push(a[o][0]),a[o]=0;for(r in s)Object.prototype.hasOwnProperty.call(s,r)&&(e[r]=s[r]);p&&p(t);while(d.length)d.shift()();return i.push.apply(i,u||[]),n()}function n(){for(var e,t=0;t<i.length;t++){for(var n=i[t],r=!0,o=1;o<n.length;o++){var c=n[o];0!==a[c]&&(r=!1)}r&&(i.splice(t--,1),e=s(s.s=n[0]))}return e}var r={},o={app:0},a={app:0},i=[];function c(e){return s.p+"js/"+({about:"about"}[e]||e)+"."+{about:"676507bb"}[e]+".js"}function s(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.e=function(e){var t=[],n={about:1};o[e]?t.push(o[e]):0!==o[e]&&n[e]&&t.push(o[e]=new Promise((function(t,n){for(var r="css/"+({about:"about"}[e]||e)+"."+{about:"2f4deaba"}[e]+".css",a=s.p+r,i=document.getElementsByTagName("link"),c=0;c<i.length;c++){var u=i[c],l=u.getAttribute("data-href")||u.getAttribute("href");if("stylesheet"===u.rel&&(l===r||l===a))return t()}var d=document.getElementsByTagName("style");for(c=0;c<d.length;c++){u=d[c],l=u.getAttribute("data-href");if(l===r||l===a)return t()}var p=document.createElement("link");p.rel="stylesheet",p.type="text/css",p.onload=t,p.onerror=function(t){var r=t&&t.target&&t.target.src||a,i=new Error("Loading CSS chunk "+e+" failed.\n("+r+")");i.code="CSS_CHUNK_LOAD_FAILED",i.request=r,delete o[e],p.parentNode.removeChild(p),n(i)},p.href=a;var f=document.getElementsByTagName("head")[0];f.appendChild(p)})).then((function(){o[e]=0})));var r=a[e];if(0!==r)if(r)t.push(r[2]);else{var i=new Promise((function(t,n){r=a[e]=[t,n]}));t.push(r[2]=i);var u,l=document.createElement("script");l.charset="utf-8",l.timeout=120,s.nc&&l.setAttribute("nonce",s.nc),l.src=c(e),u=function(t){l.onerror=l.onload=null,clearTimeout(d);var n=a[e];if(0!==n){if(n){var r=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src,i=new Error("Loading chunk "+e+" failed.\n("+r+": "+o+")");i.type=r,i.request=o,n[1](i)}a[e]=void 0}};var d=setTimeout((function(){u({type:"timeout",target:l})}),12e4);l.onerror=l.onload=u,document.head.appendChild(l)}return Promise.all(t)},s.m=e,s.c=r,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)s.d(n,r,function(t){return e[t]}.bind(null,r));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/",s.oe=function(e){throw console.error(e),e};var u=window["webpackJsonp"]=window["webpackJsonp"]||[],l=u.push.bind(u);u.push=t,u=u.slice();for(var d=0;d<u.length;d++)t(u[d]);var p=l;i.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";n("85ec")},"06f2":function(e,t,n){"use strict";var r=n("7627"),o=n.n(r);n.d(t,"default",(function(){return o.a}))},1:function(e,t){},2612:function(e,t,n){e.exports={app:"style_app_3H3QR",nav:"style_nav_3XyWa","router-link-exact-active":"style_router-link-exact-active_3bJqb"}},3447:function(e,t){e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1gQJEgAaYvsyvAAABDpJREFUOMvVlW1sU1UYx3/3rmPrNlwLZWMbo0BwIhM2CKsjW5wSZjIXs2jZGpEQZWACMX4aGg2oJH7SYVSiUUSykOFcARMC7IPgGKS81Qlx0A1xNowVujcKd91Y13t7jx92NyqSSPzmSZ7cnJtzfud//+e5zwP/tyHFTzzF1NFLDYPkAzALH7m4S89T/5/Anhew04G7JHG+g40bobAQolHwemHPHs4kDXpZSk1pCz2PyH1sQukcLginU4itW0UERB+IARAREKK2VoiyMuGZw4VHhGZXu5xC8hRTVxK0f8KaNfTs3IkJMAEyoANRoHPTOlruJnPevEjVpQTVZh7y5aTddH9X3/CgRbZql3Nw3dr1bZInB2/Jxg+KlB07CBlQk7HqbrqZXatchFZuprIoi8ezUlFjgq7eMEfb+9ACR7z5Nl9N/UeHewBLtct5Z93a9VRVVZ0zMUg+ixfTZwB1QDPAX6xyYXO+zZIZyexuuYY2PgKSjGlaCi8W5xLIcDl8F5vdcLg8Dkq1y7lSBiASQY+DRgHPinxuF28my5pEw9F21DFl6nu18RF+bO3ANn0aUetzjmqXU4mDcqD5UJrMLHx4vVgM6GS0zXVQsTyT/Sd+B6GD0BFCIPQYQo8BcMzTyQz/1zwANQOjMrm4aWwky+n8G/iKeRHzMlOIjoYmgEKAroGukSSNsyz1Kvah7x+EJgIRALn0PPVnFiqjXL/OkooK0uI8jqr6fbV6DD2mkW1WKJ1xlWULbby55a14qCluKwmeBuqsz5dW9l4JkNV6GUtlJbPLy+kwaWiZT9F5Q0FXI6RPizI3LUzhzBAfbtuOLCdQUFDA6NgwvdLsdv9FzzfxeScDNdnLX8a67R6X31f5RTnC2X1fsvjKMX66NMBqRx66ppKRHObZPBPvvfMuwWCQvLw8Dhx00292kJnUcwhIiAebgPxUq53+a3dIKYHpZSDLMEfycenYbm4NbqZiaTJWfYhXXBsIBoOYzWbaTp2kq9vPzT/7fzv9Q9NeIAkYB2KTYCQRQdcm3ggB0kQSUvt0M1+1RVHNdl6q3UQ4HEYIwcjIMOe8Xs76eq4Ffce3A1ZD6GTWChnwhW93IsnpaFHQNNBU0KKQlBDh9RVNWFICtJ78GYvFgqIofLbrc9HT233i9KF9W/64GrwLmIFkw1ppUrF7wH+8KGNBNYHOPcg6SEYxVVXQY7AgW6Y/dIGdH1/0RzTL4Hgk0t24t6nBUBeL+6/0qcsrfY36oYDXe08ZIOeJV0FKm1CsgikhhXlPrmb+LB/Jowe7/DfGvlWGh9vbWk81AyOAAoSMGDUO0O/X4wbsgHtmzhJH5rxCUtNtIDRGQr3cut5BwO//tcXDG7uaGAISAWEoHQfGjKc66e8/O0gDdUANGB0EfLrOgWc28KlhW6KxZ/KSVAM0BXxoa/qXTiPFrRdx8dDxF6jb88UGx8hVAAAAAElFTkSuQmCC"},"56d7":function(e,t,n){"use strict";n.r(t);n("cadf"),n("551c"),n("f751"),n("097d"),n("130f");var r=n("2b0e"),o=n("2f62"),a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"app"}},[n("div",{attrs:{id:"nav"}},[e.$oidc.isAuthenticated?n("a",{attrs:{href:"#"},on:{click:function(t){return e.$oidc.signOut()}}},[e._v("Signout")]):e._e(),e.$oidc.isAuthenticated?e._e():n("a",{attrs:{href:"#"},on:{click:function(t){return e.$oidc.signIn()}}},[e._v("SignIn")])]),n("router-view")],1)},i=[],c=(n("034f"),n("2877")),s={},u=Object(c["a"])(s,a,i,!1,null,null,null),l=u.exports,d=n("ce5b"),p=n.n(d);r["default"].use(p.a,{});var f=new p.a({}),v=(n("c5f6"),n("96cf"),n("3b8d")),h={state:{resolution:3,planes:1,p1:0,p2:0,r1:.1,r2:0,dl:0,db:0,toggle_cam:1,rotateX:!0,contours:!1},getters:{CONE_RESOLUTION:function(e){return e.resolution},CONE_CAMERA:function(e){return e.toggle_cam},CONE_ROTATE:function(e){return e.toggle_cam},CONE_PLANES:function(e){return e.planes},CONE_CONTOURS:function(e){return e.contours},CONE_P1:function(e){return e.p1},CONE_P2:function(e){return e.p2},CONE_R2:function(e){return e.r2},CONE_DL:function(e){return e.dl},CONE_DB:function(e){return e.db},CONE_R1:function(e){return console.log("Start loading fitx with parameters "),e.r1}},actions:{CONE_SETP1:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r=t.state,o=Number(n),r.p1=o;case 3:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETP2:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r=t.state,o=Number(n),r.p2=o;case 3:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETR1:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r=t.state,o=Number(n),r.r1=o;case 3:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETDL:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r=t.state,o=Number(n),r.dl=o;case 3:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETDB:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r=t.state,o=Number(n),r.db=o;case 3:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_RESOLUTION_UPDATE:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=t.state,o=t.dispatch,a=Number(n),r.resolution=a,e.abrupt("return",o("WS_UPDATE_RESOLUTION",a));case 4:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_PLANES_UPDATE:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=t.state,o=t.dispatch,a=Number(n),r.planes=a,e.abrupt("return",o("WS_UPDATE_PLANES",a));case 4:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_CONTOURS_UPDATE:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=t.state,o=t.dispatch,a=Boolean(n),r.contours=a,e.abrupt("return",o("WS_UPDATE_CONTOURS",a));case 4:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETCAMERAVIEW:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=t.state,o=t.dispatch,a=Number(n),r.toggle_cam=n,e.abrupt("return",o("WS_UPDATE_CAMERAVIEW",a));case 4:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_SETROTATE:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t,n){var r,o,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=t.state,o=t.dispatch,a=Boolean(n),r.rotateX=!n,e.abrupt("return",o("WS_UPDATE_ROTATE",a));case 4:case"end":return e.stop()}}),e)})));function t(t,n){return e.apply(this,arguments)}return t}(),CONE_XMLFITS_UPDATE:function(){var e=Object(v["a"])(regeneratorRuntime.mark((function e(t){var n,r,o,a,i,c,s,u;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=t.state,r=t.dispatch,o=n.r1,a=n.p1,i=n.p2,c=n.dl,s=n.db,u=String(a)+","+String(i)+","+String(o)+","+String(c)+","+String(s),e.abrupt("return",r("WS_UPDATE_XMLFITS",u));case 8:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()}},g=n("520e"),m=n("f91f");function b(e){return{createVisualization:function(t){return e.call("vtk.initialize",[t])},logOut:function(t){return e.call("vtk.initialize.logout",[t])},loadURL:function(){return e.call("vtk.cone.url",[])},resetCamera:function(){return e.call("vtk.camera.reset",[])},updateResolution:function(t){return e.call("vtk.cone.resolution.update",[t])},updatePlanes:function(t){return e.call("vtk.cone.planes.update",[t])},updateContours:function(t){return e.call("vtk.cone.contours.update",[t])},updateFits:function(t){return e.call("vtk.cone.fits.update",[t])},updateCamView:function(t){return e.call("vtk.cone.camview.update",[t])},updateRotateAxis:function(t){return e.call("vtk.cone.rotate.update",[t])},loadXMLFITS:function(t){return e.call("vtk.cone.urlfits",[t])},getDataCubeData:function(){return e.call("vtk.cone.loadcubedata",[])},setToken:function(t){return e.call("vtk.initialize.token",[t])}}}var A={VLWBase:b},w=n("3033");g["a"].setSmartConnectClass(m["a"]);var _={state:{client:null,config:null,busy:!1,json:"[{}]",dc_params:[1,10,1,1060]},getters:{WS_CLIENT:function(e){return e.client},WS_JSON:function(e){return e.json},WS_PARAMS:function(e){return e.dc_params},WS_CONFIG:function(e){return e.config},WS_BUSY:function(e){return!!e.busy}},mutations:{WS_CLIENT_SET:function(e,t){e.client=t},WS_JSON_SET:function(e,t){e.json=t},WS_CONFIG_SET:function(e,t){e.config=t},WS_BUSY_SET:function(e,t){console.log("BUSY"),e.busy=t}},actions:{WS_CONNECT:function(e,t){var n=e.state,r=e.commit,o=e.dispatch,a={application:"cone"};"443"===location.port&&(a.sessionURL="wss://${location.hostname}:443/proxy?sessionId=${id}&path=ws");var i=n.client;i&&i.isConnected()&&i.disconnect(-1);var c=i;c||(c=g["a"].newInstance({protocols:A})),c.onBusyChange((function(e){r("WS_BUSY_SET",e)})),c.beginBusy(),c.onConnectionError((function(e){var t=e&&e.response&&e.response.error||"Connection error";console.error(t),console.log(e)})),c.onConnectionClose((function(e){var t=e&&e.response&&e.response.error||"Connection close";console.error(t),console.log(e)})),c.connect(a).then((function(e){Object(w["a"])(e.getConnection().getSession()),r("WS_CLIENT_SET",e),c.endBusy(),o("WS_INITIALIZE_SERVER",t)})).catch((function(e){console.error(e)}))},WS_INITIALIZE_SERVER:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.createVisualization(t).catch(console.error)},WS_LOADURL:function(e){var t=e.state;t.client&&t.client.getRemote().VLWBase.loadURL().catch(console.error)},WS_LOGOUT:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.logOut(t).catch(console.error)},WS_UPDATE_RESOLUTION:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.updateResolution(t).catch(console.error)},WS_UPDATE_PLANES:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.updatePlanes(t).catch(console.error)},WS_UPDATE_CONTOURS:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.updateContours(t).catch(console.error)},WS_UPDATE_CAMERAVIEW:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.updateCamView(t).catch(console.error)},WS_UPDATE_ROTATE:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.updateRotateAxis(t).catch(console.error)},WS_UPDATE_TOKEN:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.setToken(t).catch(console.error)},WS_FITS_UPDATE:function(e,t){var n=e.state;n.client&&(n.client,n.client.getRemote().VLWBase.updateFits(t).then((function(e){if(!e)return alert("No datacube, the old data would be kept");n.client.getRemote().VLWBase.getDataCubeData().then((function(e){return n.dc_params=e,n.dc_params}))})))},WS_UPDATE_XMLFITS:function(e,t){var n=e.state;n.client&&n.client.getRemote().VLWBase.loadXMLFITS(t).then((function(e){return console.log("result "+e),n.json=e,n.json})).then((function(){n.client.getRemote().VLWBase.getDataCubeData().then((function(e){return n.dc_params=e,n.dc_params}))}))},WS_RESET_CAMERA:function(e){var t=e.state;t.client&&(console.log("Start"),t.client.getRemote().VLWBase.resetCamera().catch(console.error),console.log("END"))}}};function E(){return new o["a"].Store({modules:{vlw:h,wslink:_}})}var S=E,O=n("8c4f"),y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",[n("v-app-bar",{attrs:{app:"","shrink-on-scroll":"",height:"60"}},[n("v-btn",{attrs:{color:"primary",text:""},on:{click:e.onLogOut}},[e._v(" LogOut ")]),n("v-spacer"),n("v-switch",{staticClass:"d-md-none",attrs:{label:"Rotate axis"},on:{change:e.setRotate},model:{value:e.rotateX,callback:function(t){e.rotateX=t},expression:"rotateX"}}),n("v-btn",{attrs:{color:"primary",text:""},on:{click:e.setCameraView},model:{value:e.toggle_cam,callback:function(t){e.toggle_cam=t},expression:"toggle_cam"}},[e._v(" Reset Camera ")]),n("v-container",{staticStyle:{width:"35%"}},[n("div",{staticClass:"d-none d-md-block",staticStyle:{margin:"10px",padding:"0px"}},[n("v-slider",{attrs:{label:e.ex1.label,"thumb-label":"always","hide-details":"",value:e.resolution,max:e.params[1],min:e.params[0],step:.1},on:{input:e.setResolution}})],1),n("div",{staticClass:"d-md-none"},[n("v-text-field",{staticStyle:{margin:"0px",padding:"0px",width:"80px"},attrs:{label:"Threshold",type:"number",value:e.resolution,max:e.params[0],min:e.params[1],step:.1},on:{input:e.setResolution}})],1)]),n("v-container",{staticStyle:{width:"35%"}},[n("div",{staticClass:"d-none d-md-block",staticStyle:{margin:"10px",padding:"0px"}},[n("v-slider",{attrs:{label:e.ex2.label,"thumb-label":"always","hide-details":"",value:e.planes,max:e.params[3],min:e.params[2],step:1},on:{input:e.setPlanes}})],1),n("div",{staticClass:"d-md-none"},[n("v-text-field",{staticClass:"' text-caption text-sm-body-2 text-md-body-1 text-lg-h6'",staticStyle:{margin:"0px",padding:"0px",width:"80px"},attrs:{label:"Cut planes",type:"number",value:e.planes,max:e.params[3],min:e.params[2],step:1},on:{input:e.setPlanes}})],1)]),n("v-switch",{staticClass:"v-input--reverse",attrs:{label:"Use contours"},on:{change:e.setContours},model:{value:e.contours,callback:function(t){e.contours=t},expression:"contours"}}),n("div",{staticClass:"text-center"},[n("v-dialog",{attrs:{width:"500"},scopedSlots:e._u([{key:"activator",fn:function(t){var r=t.on,o=t.attrs;return[n("v-btn",e._g(e._b({},"v-btn",o,!1),r),[n("v-icon",[e._v(" mdi-settings ")])],1)]}}]),model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[n("v-card",[n("v-card-title",{staticClass:"text-h5 grey lighten-2"},[e._v(" Settings ")]),n("v-card-text",[n("v-switch",{attrs:{label:"Theme"},on:{click:function(t){e.$vuetify.theme.dark=!e.$vuetify.theme.dark}}})],1),n("v-divider"),n("v-card-actions",[n("v-spacer"),n("v-btn",{attrs:{color:"primary",text:""},on:{click:function(t){e.dialog=!1}}},[e._v(" Close ")])],1)],1)],1)],1),n("v-progress-linear",{attrs:{active:e.busy,indeterminate:e.busy,absolute:"",bottom:""}})],1),n("v-navigation-drawer",{attrs:{"mini-variant":e.mini,"hide-overlay":!0,"disable-resize-watcher":!1,"mini-variant-width":"45",permanent:"",app:"",width:350},on:{"update:miniVariant":function(t){e.mini=t},"update:mini-variant":function(t){e.mini=t}},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[n("v-divider"),n("v-container",{attrs:{fluid:"",align:"center"}},[n("v-list",[n("v-list-item",[n("v-list-item-title",[e._v("VLKB")]),n("v-btn",{staticStyle:{margin:"5px",padding:"12px"},attrs:{icon:""},on:{click:function(t){t.stopPropagation(),e.mini=!e.mini}}},[n("v-icon",[e._v("mdi-chevron-left")])],1)],1),n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v(" mdi-database-search ")])],1),n("v-list-item-content",[n("v-list-item-title",[e._v("Coordinates")]),n("v-text-field",{attrs:{label:"glon",value:e.p1,type:"number",max:"360",min:"0"},on:{input:e.setP1}}),n("v-text-field",{attrs:{label:"glat",value:e.p2,type:"number",max:"90",min:"-90"},on:{input:e.setP2}}),n("v-row",{attrs:{align:"right"}},[n("v-col",[n("v-text-field",{attrs:{label:"radius",value:e.r1,type:"number",max:"4",min:"0"},on:{input:e.setR1}})],1),n("v-col",[n("v-text-field",{attrs:{label:"dl",value:e.dl,type:"number",max:"4",min:"0"},on:{input:e.setDl}})],1),n("v-col",[n("v-text-field",{attrs:{label:"db",value:e.db,type:"number",max:"4",min:"0"},on:{input:e.setDb}})],1)],1),n("button",{on:{click:e.getData}},[e._v("Query")])],1)],1),n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v(" mdi-magnify ")])],1),n("v-list-item-content",[n("v-text-field",{attrs:{label:"Search","single-line":"","hide-details":""},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}}),n("v-data-table",{attrs:{headers:e.headers,items:JSON.parse(e.out_json),search:e.search},on:{"click:row":e.onButtonClick},scopedSlots:e._u([{key:"items",fn:function(t){return[n("td",{staticClass:"text-xs-right"},[e._v(e._s(t.item.survey))]),n("td",{staticClass:"text-xs-right"},[n("a",{attrs:{href:t.item.url}},[e._v(" "+e._s(t.item.overlap))])])]}}])},[n("v-alert",{attrs:{slot:"no-results",value:!0,color:"error",icon:"warning"},slot:"no-results"},[e._v(' Your search for "'+e._s(e.search)+'" found no results. ')])],1)],1)],1)],1),n("v-row",{attrs:{align:"left",justify:"center"}},[n("v-col")],1)],1)],1),n("v-main",{class:e.$style.appContent},[n("div",{staticStyle:{position:"relative",width:"100%",height:"100%"}},[n("remote-rendering-view",{attrs:{client:e.client}})],1)])],1)},R=[],C=(n("1c01"),n("58b2"),n("8e6e"),n("f3e2"),n("d25f"),n("ac6a"),n("456d"),n("bd86")),N=n("3447"),T=n.n(N),x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.container})},k=[],L=(n("28a5"),n("b497"),{name:"RemoteRenderView",props:{viewId:{type:String,default:"-1"},client:{type:Object,default:null}},data:function(){return{connected:!1}},created:function(){this.view=w["b"].newInstance({rpcWheelEvent:"viewport.mouse.zoom.wheel",rpcGestureEvent:"viewport.gesture",rpcMouseEvent:"viewport.mouse.move"}),"localhost"===location.hostname.split(".")[0]&&this.view.setInteractiveRatio(1)},mounted:function(){this.view.setContainer(this.$el),window.addEventListener("resize",this.view.resize),this.connect()},methods:{connect:function(){if(this.client){var e=this.client.getConnection().getSession();this.view.setSession(e),this.view.setViewId(this.viewId),this.connected=!0,this.view.render()}},handleClick:function(e){this.onClick(e)}},watch:{client:function(){this.connect()},viewId:function(e){this.connected&&(this.view.setViewId(e),this.view.render())},enablePicking:function(e){this.view.getInteractorStyle().setSendMouseMove(e)}},beforeDestroy:function(){this.subscription&&(this.subscription.unsubscribe(),this.subscription=null),window.removeEventListener("resize",this.view.resize),this.view.delete()}}),W=L,P=n("99fd");function D(e){this["$style"]=P["default"].locals||P["default"]}var U,j,M=Object(c["a"])(W,x,k,!1,D,null,null),I=M.exports,B=(n("3b2b"),n("a481"),n("759f"),n("dd17"));function V(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function F(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?V(Object(n),!0).forEach((function(t){Object(C["a"])(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):V(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function z(e,t,n,a,i,c){if(!e)throw new Error("Auth name is required.");if(t!==U.Window&&t!==U.Popup)throw new Error("Only window or popup are valid default signin types.");if(!n)throw new Error("App base url is required.");if(!a)throw new Error("No config provided to oidc auth.");B["Log"].logger=i||console,B["Log"].level=c||j.Error;var s=Z(e),u=F({response_type:"id_token",scope:"openid profile",automaticSilentRenew:!0,userStore:new B["WebStorageStateStore"]({store:sessionStorage}),post_logout_redirect_uri:n,redirect_uri:"".concat(n).concat(s),popup_post_logout_redirect_uri:"".concat(n,"auth/signoutpop/").concat(s),popup_redirect_uri:"".concat(n,"auth/signinpop/").concat(s),silent_redirect_uri:"".concat(n).concat(s)},a);B["Log"].debug("Creating new oidc auth as ".concat(e));var l=new B["UserManager"](u),d=!1,p=new r["default"]({store:S,data:function(){return{user:null,myRouter:null,store:null,needs_update:!1}},created:function(){},computed:{appUrl:function(){return n},authName:function(){return e},isAuthenticated:function(){return!!this.user&&!this.user.expired},accessToken:function(){return this.user&&!this.user.expired?this.user.access_token:""},refreshToken:function(){return this.user?this.user.refresh_token:""},needsUpdate:function(){return this.needs_update},userProfile:function(){return this.user&&!this.user.expired?this.user.profile:{iss:"",sub:"",aud:"",exp:0,iat:0}},events:function(){return l.events}},methods:F(F({},Object(o["b"])({updateToken:"WS_UPDATE_TOKEN"})),{},{updateToken2:function(){},resetUpdate:function(){this.needs_update=!1},startup:function(){var t=this,n=!1;return X(u.popup_redirect_uri)?(B["Log"].debug("".concat(e," Popup signin callback")),l.signinPopupCallback(),n=!0):X(u.popup_post_logout_redirect_uri)&&(B["Log"].debug("".concat(e," Popup logout callback")),l.signoutPopupCallback(),n=!0),n?Promise.resolve(!1):d?Promise.resolve(!0):l.getUser().then((function(e){return d=!0,e&&!e.expired&&(t.user=e,console.log("Stat"),console.log(t.user.profile)),!0})).catch((function(e){return B["Log"].warn("Auth startup err = ".concat(e)),!1}))},useRouter:function(r){var o=this;if(this.myRouter=r,r.beforeEach((function(n,r,a){n.matched.some((function(e){return e.meta.authName===o.authName}))?o.isAuthenticated?(B["Log"].debug("".concat(e," auth authenticated user entering protected route ").concat(n.fullPath)),a()):(B["Log"].debug("".concat(e," auth anon user entering protected route ").concat(n.fullPath)),v(t,{state:{to:n}}).then((function(){t===U.Window?a(!1):a()})).catch((function(){return a(!1)}))):a()})),u.redirect_uri){G(u.redirect_uri).substring((r.options.base||"/").length);r.addRoute({path:"/main",name:"signinwin-".concat(s),component:{render:function(e){return e("div")},created:function(){l.signinRedirectCallback().then((function(t){B["Log"].debug("".concat(e," Window signin callback success"),t);var o=t.state?t.state.to:null;r?r.replace(o||"/"):window.location.href=n})).catch((function(t){B["Log"].error("".concat(e," Window signin callback error"),t),r?r.replace("/"):window.location.href=n}))}}})}},signIn:function(e){return v(t,e)},signOut:function(e){if(t===U.Popup){var n=this.myRouter;return l.signoutPopup(e).then((function(){h(n)})).catch((function(){h(n)}))}return l.signoutRedirect(e)},startSilentRenew:function(){l.startSilentRenew()},stopSilentRenew:function(){l.stopSilentRenew()}})});function f(){if(p.myRouter){var n=p.myRouter.currentRoute;n&&n.meta.authName===e&&(B["Log"].debug("".concat(e," auth page re-signin with ").concat(t)),v(t,{state:{current:n}}).then((function(){})).catch((function(){setTimeout(f,5e5)})))}}function v(e,t){switch(e){case U.Popup:return l.signinPopup(t);case U.Silent:return l.signinSilent(t)}return l.signinRedirect(t)}function h(t){if(t){var r=t.currentRoute;if(r&&r.meta.authName===e)return void t.replace("/")}n&&(window.location.href=n)}function g(){l.events.addUserLoaded((function(e){p.user=e})),l.events.addUserUnloaded((function(){p.user=null,B["Log"].debug("".concat(p.authName," auth user unloaded")),f()})),l.events.addAccessTokenExpiring((function(){p.needs_update=!0})),l.events.addAccessTokenExpired((function(){B["Log"].debug("".concat(p.authName," auth token expired, user is authenticated=").concat(p.isAuthenticated)),p.user=null,f()})),l.events.addSilentRenewError((function(e){B["Log"].debug("".concat(p.authName," auth silent renew error ").concat(e)),p.isAuthenticated?setTimeout((function(){B["Log"].debug("".concat(p.authName," auth silent renew retry")),l.signinSilent()}),5e5):f()})),l.events.addUserSignedOut((function(){B["Log"].debug("".concat(p.authName," auth user signed out")),p.user=null,f()}))}return g(),p}function G(e){var t=document.createElement("a");t.href=e;var n=t.pathname;return"/"!==n[0]&&(n="/"+n),n}function X(e){return window.location.pathname.toLocaleLowerCase()===G(e).toLocaleLowerCase()}function Z(e){e=e.replace(/^\s+|\s+$/g,""),e=e.toLowerCase();for(var t="ãàáäâáº½èéëêìíïîõòóöôùúüûñç·/_,:;",n="aaaaaeeeeeiiiiooooouuuunc------",r=0,o=t.length;r<o;r++)e=e.replace(new RegExp(t.charAt(r),"g"),n.charAt(r));return e=e.replace(/[^a-z0-9 -]/g,"").replace(/\s+/g,"-").replace(/-+/g,"-"),e}(function(e){e[e["Window"]=0]="Window",e[e["Popup"]=1]="Popup"})(U||(U={})),function(e){e[e["None"]=0]="None",e[e["Error"]=1]="Error",e[e["Warn"]=2]="Warn",e[e["Info"]=3]="Info",e[e["Debug"]=4]="Debug"}(j||(j={}));var K=window.location,Q="".concat(K.protocol,"//").concat(K.host).concat("/"),J=z("main",U.Window,Q,{authority:"https://sso.neanias.eu/auth/realms/neanias-production/",client_id:"vlkb",response_type:"code",scope:"openid profile email",client_secret:"b6f98dba-a409-432a-bb21-13b692d86172"},console,j.Debug);r["default"].prototype.$oidc=J;var H=J;function Y(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function q(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?Y(Object(n),!0).forEach((function(t){Object(C["a"])(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Y(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var $={name:"App",components:{RemoteRenderingView:I},meta:{authName:H.authName},data:function(){return{dialog:!1,logo:T.a,ex1:{label:"Threshold",val:3,color:"orange darken-3"},ex2:{label:"Cutting planes",val:1,color:"green lighten-1"},ex3:{label:"Lower bound",val:50,color:"red"},ex4:{label:"Level",val:50,color:"red"},drawer:!0,mini:!0,myImage:n("6ba0"),right:null,rtoken:"",singleSelect:!0,selected:[{url:"FOR_INSTANCE"}],search:"",headers:[{text:"Survey/species",value:"survey"},{text:"Desc",value:"overlap"}],items:[],weatherDataList:[]}},computed:q({},Object(o["c"])({client:"WS_CLIENT",busy:"WS_BUSY",resolution:"CONE_RESOLUTION",planes:"CONE_PLANES",contours:"CONE_CONTOURS",p1:"CONE_P1",p2:"CONE_P2",r1:"CONE_R1",r2:"CONE_R2",dl:"CONE_DL",db:"CONE_DB",out_json:"WS_JSON",params:"WS_PARAMS",toggle_cam:"CONE_CAMERA",rotateX:"CONE_ROTATE"})),methods:q(q({},Object(o["b"])({setResolution:"CONE_RESOLUTION_UPDATE",setPlanes:"CONE_PLANES_UPDATE",setContours:"CONE_CONTOURS_UPDATE",resetCamera:"WS_RESET_CAMERA",connect:"WS_CONNECT",loadData:"CONE_XMLFITS_UPDATE",loadDataShort:"WS_FITS_UPDATE",keyLogOut:"WS_LOGOUT",updateToken:"WS_UPDATE_TOKEN",setP1:"CONE_SETP1",setP2:"CONE_SETP2",setR1:"CONE_SETR1",setDl:"CONE_SETDL",setDb:"CONE_SETDB",setCameraView:"CONE_SETCAMERAVIEW",setRotate:"CONE_SETROTATE"})),{},{onSetCamera:function(){},getData:function(){this.mini=!this.mini,this.loadData()},onLoadToken:function(){var e=this.$oidc.accessToken,t=this.$oidc.authName;console.log("Update token timeout"),console.log(t),this.updateToken(e),this.$oidc.resetUpdate()},onLogOut:function(){console.log("Log out start"),this.keyLogOut(this.rtoken),this.$oidc.resetUpdate(),this.$oidc.signOut()},checkToken:function(){var e=this.$oidc.needsUpdate;e&&setTimeout(this.onLoadToken,2500)},onButtonClick:function(e){this.mini=!this.mini,this.loadDataShort(e.url)},hideDialogAndProceed:function(){this.dialog=!1,this.loadData()}}),mounted:function(){var e=this.$oidc.accessToken;this.rtoken=this.$oidc.refreshToken,this.connect(e),setInterval(this.checkToken,1e3)}},ee=$,te=n("06f2");function ne(e){this["$style"]=te["default"].locals||te["default"]}var re=Object(c["a"])(ee,y,R,!1,ne,null,null),oe=re.exports,ae=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",[n("h2",[e._v("ViaLacteaWeb")]),n("p",[e._v("Welcome fellow astronomer! To start using the service please authenticate using your NEANIAS credentials")]),n("a",{attrs:{href:"/vlw"}},[e._v("Go to VLW")])])},ie=[],ce=n("dea2"),se={};function ue(e){this["$style"]=ce["default"].locals||ce["default"]}var le=Object(c["a"])(se,ae,ie,!1,ue,null,null),de=le.exports;r["default"].use(O["a"]);var pe=[{path:"/",name:"Hello",component:de},{path:"/vlw",name:"App",meta:{authName:H.authName},component:oe},{path:"/main2",name:"VLW2",meta:{authName:H.authName},component:function(){return n.e("about").then(n.bind(null,"b073"))}}],fe=new O["a"]({mode:"history",base:"/",routes:pe});H.useRouter(fe);var ve=fe;n("d4b8"),n("bf40"),n("5363");r["default"].use(o["a"]),r["default"].config.devtools=!0,r["default"].config.performance=!0,r["default"].config.performance=!1,H.startup().then((function(e){e?(new r["default"]({vuetify:f,store:S,router:ve,render:function(e){return e(l)}}).$mount("#app"),console.log("Startup is set")):console.log("Startup was not ok")})),r["default"].prototype.$store=S},"6ba0":function(e,t){e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAABuvAAAbrwFeGpEcAAAACXZwQWcAAABAAAAAQADq8/hgAAAGM0lEQVR42u2bTWxdRxmGn/ebmXv9k8RpqNI6VdMABqGqCARSBUgIFqCyZsUqiC1sQEJiAdusYNFN2FaUihVij2DDBqQIhBALVKUSSSNwcOK/2PdeX58z87E45yZ2YsdulOL44Ec6i6N7fuZ75/uZmTMXTjjhhBNOOOGEE/5P0c6Ty1dvARjwPHD6kM+ogbvAAODt77181DY9mQCt8QK+CfzA4cVDPmMs+DPwZoG/2jET4WEBzgO/lvjyVBLSwQ/IBcaVA/wJ+D5wjWMkwsMCfMzhtzM9LXzmUo+ZvuEHPGC7cq4vViyt52MpQtxTFUE/ianEgQJMJ/GplxLucOde/iLwJvAT4Mblq7cO4UP/G9TkqiVg9IsdHbOnAO5QF6cqOlgBYKonPnkh4jh375UvOPwK2OChJHuExuNQ0bTrp5ev3tqaeGfc76ZcnJwPYX1LP4mFFyNSrY2RvyB44agNn1ActmvHnW8BbwM3J7/t7QE0ya0uzqFcoKWXxMJ8pK4Pf8+HjSS2Kufdf9WMK+8/bPPeHuATD/igr3MM6MVnwvNbAZrObMPgkZh8RIDJhbk4uXyQ/n92yWV/K/bJAX4/BPZS7bgwaXvTkb6nHftWgVycOh9X03eT245s2WXU46tAB0JArS37GfKYKuCNcsdcgUkS3I/HeADUhU64wOM8+cAy2AH7Gw94khCou5EDWw/QRI+DBQAoxelIEWhzwN7GPGYyxINR0XFmkgMOCgG1qx/u7g6MtgtmR936p0Mpk0E6LmmXFPrcj66dq+tyts7Z58/NXfrImdm38PLKqBpSvDzZG58xTMZ0mgHZ+ysbg+/8e3n9nzEExWhrsRT/JfAJM7Oltc20ujmaB6hLbv2mA4lAEG0LYL7K+S0zq9wpufj1KPSNFGVnZxPRtCPk01E3+8MgQboooMqFe6P88WjBts7OxOlvf/VCdX6u78Udd6K7h6Nu7dNGUpao3V03l4a931y7sxWD2VpB02sjqn6furjw4lPZ1TkBgqjMNN6uSlxcq1JxrcVgWq4zF95drOo7m2Hs7iru0Z3+UTf4aSORzWw8GI25cXuoKvtyjDGMcFgelJJFbutlWww7kADv40hyiby+mcvyRg2yUUwhrOdSELIQAji4l1aAbiHJZQbIZCKarUdJt4OZS1IKzdK2F5N3ZAywWwCTmSFJrc23YzBbLu5IKEUBopSCe0eGgbsFwExIyMwwaTn2UhxWdS4mrBcFglKk0j0HwAxMwoQFs5JiGMZgWilmtYSliEzyXHR/FaULaXCSzYJJElIjQB1MK1HSkplVgtSLwkzUWYTSvSRoJkxCYGZWSVqKKYZh4/QoRQhBmKRcutD3uwlBqJn4KgYrKdow9lMYFqdCmo5BSlEuROimACqOkBSCVf0UhlHSajAbCZ2NAfWbjRHKWZ2I/wkOxCDqRgELZiNJqxFprTnBgqF+kkCdWQ7bSQiIGkmNAEhrcbYfqyF5LAwz1IuiFGQdFCAGKWeXECnaeKYfqtjvha1x5ZuSZEK9JEqR6tKNEjjBgRRgq8LakeBmvxe2Yi4MJFtrlgSlFEWVBbl7k6EYJGAyGFjLhUFMweoUGbUfRJsL2ou6hUAoF0wyUmSUgtU2dyrmFG1oJnJul069U11/H3fIGTMTKdpw7lTM8fR0rFbulRUzJxfk7nJQB2fDuKM6u4VmIrRyejpWduWdxVrSapCRC+Yg3LvqAZYLoZ0Sr155Z7GOb7x+jqleGFa140juyLuV/R4IgMtdIQXzFDV84/VzxFdf7jE7bRs5ez3bl21Xxaq6qIMRAKCZnsL8cyGHoI1TfRFfu5hwWBaqK3dbHWzHre36+H8TfAgHzKTnT/X00nNpXNyXRSB+9rXIjfeGg9nZ6Xo7M5NiDlX9DO1ze4qYifNnItNReXMwGlxamCF+NEg/vPLzxS995Wt/m5ub+/QZoHtfBB5QbcDd9fW///EPv1/82Y+/K9EsDsy/svDq1+fmzn6+lPq0u4eujQUkXFI2ixvr99b+cvP6P35XSl6cGDkNXAQWaPb4zgKB7lQDBzLNv1r+A7wHvA+MJgaK5mvobHtM7RDguKfD+5tfga1WhAHN7vFHBjzacXQR33GccALwXwSLy/clRf4tAAAAJXRFWHRjcmVhdGUtZGF0ZQAyMDA5LTEyLTA4VDEzOjAyOjExLTA3OjAwS/nD7QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxMC0wMS0xMVQwOTozMjozMy0wNzowMGo+/0sAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTAtMDEtMTFUMDk6MzI6MzMtMDc6MDAbY0f3AAAAZ3RFWHRMaWNlbnNlAGh0dHA6Ly9jcmVhdGl2ZWNvbW1vbnMub3JnL2xpY2Vuc2VzL2J5LXNhLzMuMC8gb3IgaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbGljZW5zZXMvTEdQTC8yLjEvW488YwAAACV0RVh0bW9kaWZ5LWRhdGUAMjAwOS0xMi0wOFQxMzowMjoxMS0wNzowMBRItdkAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAE3RFWHRTb3VyY2UAT3h5Z2VuIEljb25z7Biu6AAAACd0RVh0U291cmNlX1VSTABodHRwOi8vd3d3Lm94eWdlbi1pY29ucy5vcmcv7zeqywAAAABJRU5ErkJggg=="},7627:function(e,t,n){e.exports={appContent:"style_appContent_3npNh","v-input--reverse":"style_v-input--reverse_CsIpe","v-input__slot":"style_v-input__slot_2eQci","v-application--is-ltr":"style_v-application--is-ltr_QHG-K","v-input--selection-controls__input":"style_v-input--selection-controls__input_22YXA","v-application--is-rtl":"style_v-application--is-rtl_TNpE0","v-input--expand":"style_v-input--expand_1JaRx","v-label":"style_v-label_2CFdy",logo:"style_logo_3JvB7",slider:"style_slider_282Iv",switch:"style_switch_1N6l1","v-btn-toggle":"style_v-btn-toggle_2AsnX","v-btn":"style_v-btn_3RaEO","v-size--default":"style_v-size--default_3cJ52",danger:"style_danger_2Vco2",success:"style_success_zVwvy",info:"style_info_SBzPj"}},"85ec":function(e,t,n){},9174:function(e,t,n){e.exports={container:"style_container_xgDbF"}},"99fd":function(e,t,n){"use strict";var r=n("9174"),o=n.n(r);n.d(t,"default",(function(){return o.a}))},dea2:function(e,t,n){"use strict";var r=n("2612"),o=n.n(r);n.d(t,"default",(function(){return o.a}))}});
//# sourceMappingURL=app.6e4f6627.js.map