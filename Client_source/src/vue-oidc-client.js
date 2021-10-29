import { mapGetters, mapActions } from 'vuex';
import Vue from 'vue';
import { Log, UserManager, WebStorageStateStore } from 'oidc-client';
import store from 'vlw-base/src/store';
/**
 * Indicates the sign in behavior.
 */
export var SignInType;
(function (SignInType) {
    /**
     * Uses the main browser window to do sign-in.
     */
    SignInType[SignInType["Window"] = 0] = "Window";
    /**
     * Uses a popup window to do sign-in.
     */
    SignInType[SignInType["Popup"] = 1] = "Popup";
})(SignInType || (SignInType = {}));
/**
 * Logging level values used by createOidcAuth().
 */
export var LogLevel;
(function (LogLevel) {
    /**
     * No logs messages.
     */
    LogLevel[LogLevel["None"] = 0] = "None";
    /**
     * Only error messages.
     */
    LogLevel[LogLevel["Error"] = 1] = "Error";
    /**
     * Error and warning messages.
     */
    LogLevel[LogLevel["Warn"] = 2] = "Warn";
    /**
     * Error, warning, and info messages.
     */
    LogLevel[LogLevel["Info"] = 3] = "Info";
    /**
     * Everything.
     */
    LogLevel[LogLevel["Debug"] = 4] = "Debug";
})(LogLevel || (LogLevel = {}));
/**
 * Creates an openid-connect auth instance.
 * @param authName - short alpha-numeric name that identifies the auth instance for routing purposes.
 * This is used to generate default redirect urls (slugified) and identifying routes that needs auth.
 * @param defaultSignInType - the signin behavior when `signIn()` and `signOut()` are called.
 * @param appUrl - url to the app using this instance for routing purposes. Something like `https://domain/app/`.
 * @param oidcConfig - config object for oidc-client.
 * See https://github.com/IdentityModel/oidc-client-js/wiki#configuration for details.
 * @param logger - logger used by oidc-client. Defaults to console.
 * @param logLevel - minimum level to log. Defaults to LogLevel.Error.
 */
export function createOidcAuth(authName, defaultSignInType, appUrl, oidcConfig, logger, logLevel) {
    // arg check
    if (!authName) {
        throw new Error('Auth name is required.');
    }
    if (defaultSignInType !== SignInType.Window &&
        defaultSignInType !== SignInType.Popup) {
        throw new Error('Only window or popup are valid default signin types.');
    }
    if (!appUrl) {
        throw new Error('App base url is required.');
    }
    if (!oidcConfig) {
        throw new Error('No config provided to oidc auth.');
    }
    Log.logger = logger || console;
    Log.level = logLevel || LogLevel.Error;
    const nameSlug = slugify(authName);
    // merge passed oidcConfig with defaults
    const config = {
        response_type: 'id_token',
        scope: 'openid profile',
        automaticSilentRenew: true,
        userStore: new WebStorageStateStore({
            store: sessionStorage
        }),
        post_logout_redirect_uri: appUrl,
        redirect_uri: `${appUrl}${nameSlug}`,
        popup_post_logout_redirect_uri: `${appUrl}auth/signoutpop/${nameSlug}`,
        popup_redirect_uri: `${appUrl}auth/signinpop/${nameSlug}`,
        silent_redirect_uri: `${appUrl}${nameSlug}`,
        ...oidcConfig // everything can be overridden!
    };
    Log.debug(`Creating new oidc auth as ${authName}`);
    const mgr = new UserManager(config);
    let _inited = false;
    const auth = new Vue({
        store,  
        data() {
            return {
                user: null,
                myRouter: null,
                store:null,
                needs_update:false
            };
        },
        created: () => {
            //this.store=store;
       
               //console.log(store);
           },
        computed: {
            appUrl() {
                return appUrl;
            },
            authName() {
                return authName;
            },
            isAuthenticated() {
                return !!this.user && !this.user.expired;
            },
            accessToken() {
                return !!this.user && !this.user.expired ? this.user.access_token : '';
            },
            needsUpdate() {
                return this.needs_update;
            },
            userProfile() {
                return !!this.user && !this.user.expired
                    ? this.user.profile
                    : {
                        iss: '',
                        sub: '',
                        aud: '',
                        exp: 0,
                        iat: 0
                    };
            },
            events() {
                return mgr.events;
            }
        },
        methods: {
           ...mapActions({            
             updateToken: 'WS_UPDATE_TOKEN',
             }),
            updateToken2(){
             //  console.log(this.$store)
           },
            resetUpdate(){this.needs_update=false;},
            
            startup() {
                let isCB = false; // CB = callback
                if (matchesPath(config.popup_redirect_uri)) {
                    Log.debug(`${authName} Popup signin callback`);
                    mgr.signinPopupCallback();
                    isCB = true;
                }
               // else if (matchesPath(config.silent_redirect_uri)) {
               //     Log.debug(`${authName} Silent signin callback`);
               //     alert("Call of silent redirect")
               //     mgr.signinSilentCallback();
                //    
               //     isCB = true;
               // }
                else if (matchesPath(config.popup_post_logout_redirect_uri)) {
                    Log.debug(`${authName} Popup logout callback`);
                    mgr.signoutPopupCallback();
                    isCB = true;
                }
                if (isCB)
                    return Promise.resolve(false);
                if (_inited) {
                    return Promise.resolve(true);
                }
                else {
                    // load user from storage
                    return mgr
                        .getUser()
                        .then(test => {
                        _inited = true;
                        if (test && !test.expired) {
                            this.user = test;
                            console.log("Stat")
                            console.log(this.user.profile)
                            //console.log(this.$store);
                            //this.updateToken();
                            //this.$store.state.wslink.dispatch('WS_UPDATE_TOKEN',this.user.access_token);
                           //this.updateToken(this.user.access_token);
                           // alert("token callsed")
                            //VLWBase.setToken(this.user.access_token);
                            
                        }
                        
                        return true;
                    })
                        .catch(err => {
                        Log.warn(`Auth startup err = ${err}`);
                        return false;
                    });
                }
            },
            useRouter(router) {
                this.myRouter = router;
                router.beforeEach((to, from, next) => {
                    if (to.matched.some(record => record.meta.authName === this.authName)) {
                        if (this.isAuthenticated) {
                            Log.debug(`${authName} auth authenticated user entering protected route ${to.fullPath}`);
                            next();
                        }
                        else {
                            Log.debug(`${authName} auth anon user entering protected route ${to.fullPath}`);
                            signInReal(defaultSignInType, { state: { to } })
                                .then(() => {
                                if (defaultSignInType === SignInType.Window) {
                                    next(false);
                                }
                                else {
                                    next();
                                }
                            })
                                .catch(() => next(false));
                        }
                    }
                    else {
                        next();
                    }
                });
                if (config.redirect_uri) {
                    const vroutePath = '/' +
                        getUrlPath(config.redirect_uri).substring((router.options.base || '/').length);
                    router.addRoute({
                        path: '/main', /*vroutePath*/
                        name: `signinwin-${nameSlug}`,
                        component: {
                            render: h => h('div'),
                            created() {
                                mgr
                                    .signinRedirectCallback()
                                    .then(data => {
                                    Log.debug(`${authName} Window signin callback success`, data);
                                    // need to manually redirect for window type
                                    // goto original secure route or root
                                    const redirect = data.state ? data.state.to : null;
                                    if (router)
                                        router.replace(redirect || '/');
                                    else
                                        window.location.href = appUrl;
                                })
                                    .catch(err => {
                                    Log.error(`${authName} Window signin callback error`, err);
                                    if (router)
                                        router.replace('/');
                                    else
                                        window.location.href = appUrl;
                                });
                            }
                        }
                    });
                }
            },
            signIn(args) {
                return signInReal(defaultSignInType, args);
            },
            signOut(args) {
                if (defaultSignInType === SignInType.Popup) {
                    const router = this.myRouter;
                    return mgr
                        .signoutPopup(args)
                        .then(() => {
                        redirectAfterSignout(router);
                    })
                        .catch(() => {
                        // could be window closed
                        redirectAfterSignout(router);
                    });
                }
                return mgr.signoutRedirect(args);
            },
            startSilentRenew() {
                mgr.startSilentRenew();
            },
            stopSilentRenew() {
                mgr.stopSilentRenew();
            }
        }
    });
    function signInIfNecessary() {
        if (auth.myRouter) {
            const current = auth.myRouter.currentRoute;
            if (current && current.meta.authName === authName) {
                Log.debug(`${authName} auth page re-signin with ${defaultSignInType}`);
                signInReal(defaultSignInType, { state: { current } })
                    .then(() => {
                    // auth.myRouter()
                })
                    .catch(() => {
                    setTimeout(signInIfNecessary, 500000);
                });
                // window.location.reload();
                // auth.myRouter.go(); //replace('/');
            }
        }
    }
    function signInReal(type, args) {
        switch (type) {
            case SignInType.Popup:
                return mgr.signinPopup(args);
             case SignInType.Silent:
                 //alert("start silent")
               return mgr.signinSilent(args)
        }
        return mgr.signinRedirect(args);
    }
    function redirectAfterSignout(router) {
        if (router) {
            const current = router.currentRoute;
            if (current && current.meta.authName === authName) {
                router.replace('/');
                return;
            }
        }
        //   window.location.reload(true);
        if (appUrl)
            window.location.href = appUrl;
    }
    /**
     * Translates user manager events to vue events and perform default actions
     * if necessary.
     */
    function handleManagerEvents() {
        mgr.events.addUserLoaded(user => {
            auth.user = user;
           // alert("user.access_token");
           // VLWBase.setToken(user.access_token);
        });
        mgr.events.addUserUnloaded(() => {
            auth.user = null;
            // redirect if on protected route (best method here?)
            Log.debug(`${auth.authName} auth user unloaded`);
            signInIfNecessary();
        });
        mgr.events.addAccessTokenExpiring(() => {
            //setTimeout(alert("about to expire"),600);
            auth.needs_update=true; //needs update
        });
        
        mgr.events.addAccessTokenExpired(() => {
            Log.debug(`${auth.authName} auth token expired, user is authenticated=${auth.isAuthenticated}`);
            auth.user = null;
            //alert("token expired")
            signInIfNecessary();
            // if (auth.isAuthenticated) {
            //   mgr
            //     .signinSilent()
            //     .then(() => {
            //       Log.debug(`${authName} auth silent signin after token expiration`)
            //     })
            //     .catch(() => {
            //       Log.debug(
            //         `${authName} auth silent signin error after token expiration`
            //       )
            //       signInIfNecessary()
            //     })
            // }
        });
        mgr.events.addSilentRenewError(e => {
            Log.debug(`${auth.authName} auth silent renew error ${e}`);
            // TODO: need to restart renew manually?
            if (auth.isAuthenticated) {
                setTimeout(() => {
                    Log.debug(`${auth.authName} auth silent renew retry`);
                    mgr.signinSilent();
                }, 500000);
            }
            else {
                signInIfNecessary();
            }
        });
        mgr.events.addUserSignedOut(() => {
            Log.debug(`${auth.authName} auth user signed out`);
            auth.user = null;
            signInIfNecessary();
        });
    }
    handleManagerEvents();
    return auth;
}
// general utilities
/**
 * Gets the path portion of a url.
 * @param url - full url
 * @returns
 */
function getUrlPath(url) {
    const a = document.createElement('a');
    a.href = url;
    let p = a.pathname;
    if (p[0] !== '/')
        p = '/' + p;
    return p;
}
/**
 * Checks if current url's path matches given url's path.
 * @param {String} testUrl - url to test against.
 */
function matchesPath(testUrl) {
    return (window.location.pathname.toLocaleLowerCase() ===
        getUrlPath(testUrl).toLocaleLowerCase());
}
function slugify(str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
    // remove accents, swap ñ for n, etc
    const from = 'ãàáäâáº½èéëêìíïîõòóöôùúüûñç·/_,:;';
    const to = 'aaaaaeeeeeiiiiooooouuuunc------';
    for (let i = 0, l = from.length; i < l; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }
    str = str
        .replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes
    return str;
}
//# sourceMappingURL=vue-oidc-client.js.map

