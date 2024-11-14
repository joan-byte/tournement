<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Resultados del Torneo
      </h3>
    </div>
    <div class="border-t border-gray-200">
      <div class="px-4 py-5 sm:p-6">
        <div class="grid grid-cols-1 gap-6">
          <div v-if="!campeonatoActual" class="text-center text-gray-500">
            Seleccione un campeonato para ver los resultados
          </div>
          <div v-else>
            <!-- Tabla de resultados -->
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Pareja
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PG
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      PP
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Grupo
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="resultado in resultados" :key="resultado.pareja_id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ resultado.nombre_pareja }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ resultado.PG }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ resultado.PP }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ resultado.GB }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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