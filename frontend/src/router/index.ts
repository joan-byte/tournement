import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import Campeonatos from '@/views/Campeonatos.vue'
import Mesas from '@/views/Mesas.vue'
import RegistroResultados from '@/views/RegistroResultados.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/campeonatos',
    name: 'campeonatos',
    component: Campeonatos
  },
  {
    path: '/parejas',
    name: 'parejas',
    component: () => import('@/views/Parejas.vue')
  },
  {
    path: '/resultados',
    name: 'resultados',
    component: () => import('@/views/Resultados.vue')
  },
  {
    path: '/partidas/inicio',
    name: 'inicio-partida',
    component: () => import('@/components/Partidas/InicioPartida.vue')
  },
  {
    path: '/partidas/registro',
    name: 'registro-partida',
    component: () => import('@/components/Partidas/RegistroPartida.vue')
  },
  {
    path: '/partidas/resultado/:mesaId',
    name: 'registro-resultado',
    component: () => import('@/components/Partidas/RegistroResultado.vue')
  },
  {
    path: '/podium',
    name: 'podium',
    component: () => import('@/components/Partidas/Podium.vue')
  },
  {
    path: '/mesas',
    name: 'mesas',
    component: Mesas
  },
  {
    path: '/mesas/asignacion',
    name: 'asignacion-mesas',
    component: () => import('@/views/Mesas.vue')
  },
  {
    path: '/mesas/resultados',
    name: 'registro-resultados',
    component: RegistroResultados
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router 