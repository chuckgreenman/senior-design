<template>
  <v-app>       
    <v-content>
      <Header/>
      <MainTabs/>
    </v-content>
  </v-app>
</template>

<script>
import MainTabs from './components/MainTabs';
import Header from './components/Header'

export default {
  name: 'App',

  components: {
    Header,
    MainTabs
  },

  data: () => ({
    //
  }),
};
</script>

