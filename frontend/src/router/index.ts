/**
 * router/index.ts
 * Configuración principal del enrutador de Vue Router
 * Define todas las rutas disponibles en la aplicación y sus componentes asociados
 */

// Importaciones necesarias para la configuración del router
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

// Importaciones de componentes cargados de forma estática
import Home from '@/views/Home.vue'
import Campeonatos from '@/views/Campeonatos.vue'
import Mesas from '@/views/Mesas.vue'
import RegistroResultados from '@/views/RegistroResultados.vue'
import Podium from '@/components/Partidas/Podium.vue'

/**
 * Definición de rutas de la aplicación
 * Cada ruta especifica su path, nombre y componente asociado
 * Algunas rutas utilizan lazy loading para optimizar el rendimiento
 */
const routes: RouteRecordRaw[] = [
  // Ruta principal - página de inicio
  {
    path: '/',
    name: 'home',
    component: Home
  },
  
  // Gestión de campeonatos
  {
    path: '/campeonatos',
    name: 'campeonatos',
    component: Campeonatos
  },
  
  // Gestión de parejas - carga lazy
  {
    path: '/parejas',
    name: 'parejas',
    component: () => import('@/views/Parejas.vue')
  },
  
  // Visualización de resultados - carga lazy
  {
    path: '/resultados',
    name: 'resultados',
    component: () => import('@/views/Resultados.vue')
  },
  
  // Rutas relacionadas con partidas
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
  
  // Visualización del podio
  {
    path: '/podium',
    name: 'podium',
    component: Podium
  },
  
  // Rutas relacionadas con mesas
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

/**
 * Creación y configuración del router
 * Utiliza el modo history para URLs limpias
 * @type {Router}
 */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Exportación del router configurado
export default router 