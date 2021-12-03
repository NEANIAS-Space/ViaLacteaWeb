import Vue from 'vue';
import { createOidcAuth, SignInType, LogLevel } from 'vlw-base/src/vue-oidc-client.js';

const loco = window.location;
const appRootUrl = `${loco.protocol}//${loco.host}${process.env.BASE_URL}`;
const idsrvAuth = createOidcAuth(
  'main',
  SignInType.Window,
  appRootUrl,
  {
    authority: 'https://sso.neanias.eu/auth/realms/neanias-production/',
    client_id: 'vlkb',
    response_type: 'code',
    scope: 'openid profile email',
    client_secret: 'b6f98dba-a409-432a-bb21-13b692d86172',
  //   authority: 'https://sso.neanias.eu/auth/realms/neanias-development/',
   //   client_id: 'vlkb',
   //   response_type: 'code',
  //    scope: 'openid profile email',
   //  client_secret: 'e1b4cda4-0ae5-46ba-86fd-1b05f58432e3',
    
    //redirect_uri: `${appRootUrl}main`,
    //redirect_uri: 'http://visivo-server.oact.inaf.it/auth/signinwin/main',
    //redirect_uri: 'http://192.168.1.49:8080',
    //popup_redirect_uri: 'http://192.168.1.49:8080',
    //silent_redirect_uri: `${appRootUrl}main`,
    // test use
    //authority: 'https://demo.identityserver.io/',
   // client_id: 'interactive.confidential',
   // client_secret: 'secret',
   // response_type: 'code',
   //  scope: 'openid profile email api',
   // prompt: 'login',
  },
  console,
  LogLevel.Debug
)



// a little something extra
Vue.prototype.$oidc = idsrvAuth

export default idsrvAuth
