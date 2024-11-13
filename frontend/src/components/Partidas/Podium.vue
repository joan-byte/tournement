<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:px-6">
        <h2 class="text-2xl font-bold text-center mb-4">
          🏆 Podium del Campeonato 🏆
        </h2>
      </div>

      <div v-if="isLoading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
      </div>
      <div v-else-if="error" class="text-red-500 text-center py-8">
        {{ error }}
      </div>
      <div v-else>
        <!-- Podium Display -->
        <div class="flex justify-center items-end space-x-4 py-8">
          <!-- Segundo Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[1]">
            <div class="text-xl font-bold">🥈</div>
            <div class="bg-gray-200 w-24 h-32 flex items-center justify-center rounded-t-lg">
              <div class="text-center">
                <div class="font-bold">{{ ranking[1].nombre_pareja }}</div>
                <div class="text-sm">PG: {{ ranking[1].PG }}</div>
                <div class="text-sm">PP: {{ ranking[1].PP }}</div>
              </div>
            </div>
            <div class="bg-gray-300 h-20 w-24"></div>
          </div>

          <!-- Primer Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[0]">
            <div class="text-xl font-bold">🏆</div>
            <div class="bg-yellow-200 w-24 h-40 flex items-center justify-center rounded-t-lg">
              <div class="text-center">
                <div class="font-bold">{{ ranking[0].nombre_pareja }}</div>
                <div class="text-sm">PG: {{ ranking[0].PG }}</div>
                <div class="text-sm">PP: {{ ranking[0].PP }}</div>
              </div>
            </div>
            <div class="bg-yellow-300 h-24 w-24"></div>
          </div>

          <!-- Tercer Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[2]">
            <div class="text-xl font-bold">🥉</div>
            <div class="bg-orange-200 w-24 h-24 flex items-center justify-center rounded-t-lg">
              <div class="text-center">
                <div class="font-bold">{{ ranking[2].nombre_pareja }}</div>
                <div class="text-sm">PG: {{ ranking[2].PG }}</div>
                <div class="text-sm">PP: {{ ranking[2].PP }}</div>
              </div>
            </div>
            <div class="bg-orange-300 h-16 w-24"></div>
          </div>
        </div>

        <!-- Ranking Table -->
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Ranking Final</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Posición
                  </th>
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
                <tr v-for="(pareja, index) in ranking" :key="pareja.pareja_id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ index + 1 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">
                      {{ pareja.nombre_pareja }}
                    </div>
                    <div class="text-sm text-gray-500" v-if="pareja.club">
                      {{ pareja.club }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.PG }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.PP }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.GB }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="px-4 py-4 sm:px-6 flex justify-end">
        <button
          @click="finalizarCampeonato"
          class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
        >
          Finalizar Campeonato
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRankingStore } from '@/stores/ranking'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { Resultado } from '@/types'

const router = useRouter()
const rankingStore = useRankingStore()
const campeonatoStore = useCampeonatoStore()

const ranking = ref<Resultado[]>([])
const isLoading = ref(true)
const error = ref('')

onMounted(async () => {
  await cargarRanking()
})

const cargarRanking = async () => {
  try {
    const campeonato = campeonatoStore.getCurrentCampeonato()
    if (!campeonato) {
      error.value = 'No hay campeonato seleccionado'
      return
    }

    ranking.value = await rankingStore.fetchRankingFinal(campeonato.id)
  } catch (e) {
    console.error('Error al cargar el ranking:', e)
    error.value = 'Error al cargar el ranking'
  } finally {
    isLoading.value = false
  }
}

const finalizarCampeonato = async () => {
  try {
    const campeonato = campeonatoStore.getCurrentCampeonato()
    if (!campeonato) return

    await rankingStore.actualizarRanking(campeonato.id)
    router.push('/')
  } catch (e) {
    console.error('Error al finalizar el campeonato:', e)
    error.value = 'Error al finalizar el campeonato'
  }
}
</script> 