<template>
  <div id="app">
    <div class="menu">
      <img id="logo" src="./assets/oscar_logo.png" alt="Oscar logo"> 
      <div class="items">
        <div class="item"><router-link to="/home">Home</router-link></div>
        <div class="item"><router-link to="/about">About</router-link></div>
        <div class="item"><router-link to="/search">Search</router-link></div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.menu {
  display: flex;
  justify-content: space-between;
}

.items {
  display: flex;
}

.item {
  margin-left: 10px;
  margin-right: 10px;
  display: flex;
  align-items: center;
}

#logo {
  max-height: 50px;
}
</style>
