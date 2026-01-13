import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/video/:id',
    name: 'video-detail',
    component: () => import('../views/VideoDetailView.vue')
  },
  {
    path: '/upload',
    name: 'video-upload',
    component: () => import('../views/VideoUploadView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 