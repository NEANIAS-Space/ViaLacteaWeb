<template>
  <div id="app">
    <div id="nav">
    
     
      
      <a href="#" @click="$oidc.signOut()" v-if="$oidc.isAuthenticated"
        >Signout</a>
      <a href="#" @click="$oidc.signIn()" v-if="!$oidc.isAuthenticated"
        >SignIn</a
      >
    </div>
    <router-view />
 
   <h2>ViaLacteaWeb</h2>
   <p>Welcome fellow astronomer! To start using the service please authenticate using your NEANIAS credentials</p>
   <a href="/vlw">Go to VLW</a>
  
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>