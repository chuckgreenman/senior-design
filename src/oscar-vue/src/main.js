import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import About from './components/About.vue'
import Home from './components/Home.vue'
import Search from './components/Search.vue'

Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [
  { path: '/about', component: About },
  { path: '/home', component: Home },
  { path: '/search', component: Search}
]

const router = new VueRouter({
  routes
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

