<template>
  <nav class="bg-primary-800">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <img class="h-8 w-auto" src="@/assets/logo.png" alt="Logo" />
          </div>
          <div class="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              v-for="item in navigationItems"
              :key="item.name"
              :to="item.href"
              :class="[
                isActive(item.href)
                  ? 'border-primary-500 text-white'
                  : 'border-transparent text-primary-300 hover:border-primary-300 hover:text-white',
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
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'

const route = useRoute()
const campeonatoStore = useCampeonatoStore()

const navigationItems = computed(() => {
  const items = [
    { name: 'Campeonatos', href: '/campeonatos' }
  ]

  const campeonato = campeonatoStore.getCurrentCampeonato()
  if (campeonato) {
    items.push(
      { name: 'Parejas', href: '/parejas' },
      { name: 'Mesas', href: '/mesas' },
      { name: 'Resultados', href: '/mesas/resultados' },
      { name: 'Podium', href: '/podium' }
    )
  }

  return items
})

const isActive = (path: string) => {
  return route.path.startsWith(path)
}
</script> 