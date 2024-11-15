<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Ranking del Torneo
          </h3>
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual || 1 }}
          </span>
        </div>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <div class="border-t border-gray-200">
        <div v-if="!campeonatoActual" class="text-center py-4 text-gray-500">
          Seleccione un campeonato para ver el ranking
        </div>
        <div v-else>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pos.
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    GB
                  </th>
                  <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    PG
                  </th>
                  <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    PP
                  </th>
                  <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Partida
                  </th>
                  <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nº
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Club
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="resultado in parejasVisibles" :key="resultado.pareja_id" 
                    :class="getPosicionClass(resultado.posicion)">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    {{ resultado.posicion }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    {{ resultado.GB }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {{ resultado.PG }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {{ resultado.PP }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {{ resultado.ultima_partida }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {{ resultado.numero }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    {{ resultado.nombre }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ resultado.club || 'Sin club' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useResultadoStore } from '@/stores/resultado'
import type { Campeonato } from '@/types'
import type { RankingResultado } from '@/types/resultado'

const campeonatoStore = useCampeonatoStore()
const resultadoStore = useResultadoStore()

const resultados = ref<RankingResultado[]>([])
const campeonatoActual = ref<Campeonato | null>(null)
const currentPage = ref(0)
const intervalId = ref<number | null>(null)
const checkIntervalId = ref<number | null>(null)
const ITEMS_PER_PAGE = 20
const ROTATION_INTERVAL = 10000 // 10 segundos

const parejasVisibles = computed(() => {
  const start = currentPage.value * ITEMS_PER_PAGE
  const end = start + ITEMS_PER_PAGE
  return resultados.value.slice(start, end)
})

const startRotation = () => {
  if (resultados.value.length <= ITEMS_PER_PAGE) return

  // Limpiar intervalo existente si hay uno
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }

  intervalId.value = window.setInterval(() => {
    const totalPages = Math.ceil(resultados.value.length / ITEMS_PER_PAGE)
    currentPage.value = (currentPage.value + 1) % totalPages
  }, ROTATION_INTERVAL)
}

const getPosicionClass = (posicion: number) => {
  switch (posicion) {
    case 1:
      return 'bg-yellow-50'
    case 2:
      return 'bg-gray-50'
    case 3:
      return 'bg-orange-50'
    default:
      return ''
  }
}

const loadResultados = async () => {
  if (campeonatoActual.value) {
    resultados.value = await resultadoStore.fetchResultados(campeonatoActual.value.id)
    currentPage.value = 0
    startRotation()
  }
}

const updateCampeonato = async () => {
  const newCampeonato = campeonatoStore.getCurrentCampeonato()
  if (newCampeonato?.id !== campeonatoActual.value?.id) {
    campeonatoActual.value = newCampeonato
    if (newCampeonato) {
      await loadResultados()
    }
  }
}

onMounted(async () => {
  await updateCampeonato()
  startRotation()
  
  // Iniciar verificación periódica de cambios en el campeonato
  checkIntervalId.value = window.setInterval(updateCampeonato, 5000)
})

onUnmounted(() => {
  // Limpiar todos los intervalos
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }
  if (checkIntervalId.value) {
    clearInterval(checkIntervalId.value)
  }
})
</script> 