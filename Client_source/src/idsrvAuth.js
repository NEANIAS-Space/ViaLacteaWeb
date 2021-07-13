import Vue from 'vue';

import { createOidcAuth, SignInType, LogLevel } from 'vlw-base/src/vue-oidc-client';
const appRootUrl = 'http://192.168.1.49:8080/';
const idsrvAuth = createOidcAuth(
  'main',
  SignInType.Popup,
  appRootUrl,
  {
    authority: 'https://sso.neanias.eu/auth/realms/neanias-development/',
    client_id: 'vlkb',
    response_type: 'code',
    scope: 'openid profile email api',
    client_secret: 'e1b4cda4-0ae5-46ba-86fd-1b05f58432e3',
    //redirect_uri: 'http://visivo-server.oact.inaf.it/vlw/',
    redirect_uri: 'http://192.168.1.49:8080/',
    //popup_redirect_uri: 'http://visivo-server.oact.inaf.it/vlw/',
    //   silent_redirect_uri: 'http://visivo-server.oact.inaf.it/vlw/',
    // test use
    //authority: 'https://demo.identityserver.io/',
    //client_id: 'interactive.confidential',
    //client_secret: 'secret',
    //response_type: 'code',
    // scope: 'openid profile email api',
    prompt: 'login',
  },
  console
);
Vue.prototype.$oidc = idsrvAuth;
export default idsrvAuth;
