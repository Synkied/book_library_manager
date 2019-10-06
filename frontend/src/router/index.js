import Vue from 'vue'
import VueRouter from 'vue-router'

const routing = [
  { path: '/', component: 'Home', name: 'home' },
]

let routes = routing.map(route => {
    return {
        ...route,
        component: () => import(`@/components/${route.component}.vue`)
    }
})

Vue.use(VueRouter)

export default new VueRouter({
  routes,
  mode: 'history'
})
