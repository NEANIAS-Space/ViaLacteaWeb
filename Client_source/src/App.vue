<template>
  <div id="app">
   
    <router-view />
    
 </div>
  <!---- <h2>ViaLacteaWeb</h2>
   <p>Welcome fellow astronomer! To start using the service please authenticate using your NEANIAS credentials</p>
   <a href="/vlw">Go to VLW</a> -->
  
  
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav2 {
  padding: 0px;
}

#nav2 a {
  font-weight: bold;
  color: #2c3e50;
}

#nav2 a.router-link-exact-active {
  color: #42b983;
}
</style>