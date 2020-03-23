<template>
  <div id="app">
    <img alt="OSCAR logo" src="./assets/oscar_logo.png">    
    <OscarHeader/>
    <MainTable/>
  </div>
</template>

<script>
import OscarHeader from './components/Header.vue'
import MainTable from './components/MainTable.vue'

export default {
  name: 'App',
  components: {    
    OscarHeader,
    MainTable
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
