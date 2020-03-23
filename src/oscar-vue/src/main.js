import Vue from 'vue'
import App from './App.vue'
import {Tabs, Tab} from 'vue-tabs-component';
 
Vue.component('tabs', Tabs);
Vue.component('tab', Tab);

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
