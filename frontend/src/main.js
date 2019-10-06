import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router'
import vuetify from './plugins/vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

// custom plugins
import BackendAPI from './services/BackendAPI'

Vue.config.productionTip = false

Vue.use(VueRouter)
Vue.use(BackendAPI)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
