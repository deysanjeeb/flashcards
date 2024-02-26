import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '../views/HelloWorld.vue'
import signUp from '../views/signUp.vue'
import Dashboard from '../views/Dashboard.vue'
import Review from '../views/Review.vue'
import Deck from '../views/Deck.vue'
import Card from '../views/Card.vue'
import Management from '../views/Management.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HelloWorld
  },
  
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  },
  {
      path: '/deck',
      name: 'deck',
      component: Deck
    },
    {
      path: '/card',
      name: 'card',
      component: Card
    },
    { 
      path: '/review', 
      name: 'review',
      component: Review 
    },

    {
      path: '/management',
      name: 'management',
      component: Management
    },
    {
      path: '/signup',
      name: 'signup',
      component: signUp
    },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
