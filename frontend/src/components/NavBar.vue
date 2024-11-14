<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-xl font-bold text-gray-800">Torneo de Dominó</h1>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              v-for="item in regularItems"
              :key="item.name"
              :to="item.href"
              :class="[
                isCurrentRoute(item.href)
                  ? 'border-primary-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
              ]"
            >
              {{ item.name }}
            </router-link>

            <div class="relative inline-flex items-center">
              <button
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
                :class="[isMesasRoute ? 'border-primary-500 text-gray-900' : 'border-transparent']"
                @click="toggleMesasMenu"
              >
                Mesas
                <svg class="ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>

              <div
                v-show="showMesasMenu"
                class="absolute top-full left-0 z-10 mt-1 w-56 origin-top-left rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              >
                <div class="py-1">
                  <router-link
                    v-for="item in mesasItems"
                    :key="item.name"
                    :to="item.href"
                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    @click="showMesasMenu = false"
                  >
                    {{ item.name }}
                  </router-link>
                </div>
              </div>
            </div>

            <router-link
              v-for="item in afterMesasItems"
              :key="item.name"
              :to="item.href"
              :class="[
                isCurrentRoute(item.href)
                  ? 'border-primary-500 text-gray-900'
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
              ]"
            >
              {{ item.name }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showMesasMenu = ref(false)

const regularItems = [
  { name: 'Inicio', href: '/' },
  { name: 'Campeonatos', href: '/campeonatos' },
  { name: 'Parejas', href: '/parejas' },
]

const mesasItems = [
  { 
    name: 'Asignación de Mesas', 
    href: '/mesas/asignacion',
  },
  { 
    name: 'Registro de Resultados', 
    href: '/mesas/resultados',
  }
]

const afterMesasItems = [
  { name: 'Resultados', href: '/resultados' }
]

const isCurrentRoute = (path: string) => route.path === path

const isMesasRoute = computed(() => {
  return route.path.startsWith('/mesas')
})

const toggleMesasMenu = () => {
  showMesasMenu.value = !showMesasMenu.value
}

// Cerrar el menú cuando se hace clic fuera
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showMesasMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script> 