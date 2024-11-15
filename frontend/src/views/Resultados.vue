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
                <tr v-for="resultado in resultados" :key="resultado.pareja_id" 
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
import { ref, onMounted } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useResultadoStore } from '@/stores/resultado'
import type { Campeonato } from '@/types'
import type { RankingResultado as Resultado } from '@/types/resultado'

const campeonatoStore = useCampeonatoStore()
const resultadoStore = useResultadoStore()

const resultados = ref<Resultado[]>([])
const campeonatoActual = ref<Campeonato | null>(null)

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

onMounted(async () => {
  campeonatoActual.value = campeonatoStore.getCurrentCampeonato()
  if (campeonatoActual.value) {
    await loadResultados()
  }
})

const loadResultados = async () => {
  if (campeonatoActual.value) {
    resultados.value = await resultadoStore.fetchResultados(campeonatoActual.value.id)
  }
}
</script> 