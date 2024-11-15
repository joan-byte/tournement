<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:px-6">
        <h2 class="text-2xl font-bold text-center mb-4">
          🏆 Podium del Campeonato 🏆
        </h2>
        <p class="text-center text-gray-600">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <div v-if="!campeonatoFinalizado" class="text-center py-8 text-red-600">
        <p class="text-lg font-medium">El campeonato aún no ha finalizado</p>
        <p class="text-sm mt-2">El podium estará disponible cuando se complete la última partida</p>
      </div>

      <div v-else-if="isLoading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
      </div>
      <div v-else-if="error" class="text-red-500 text-center py-8">
        {{ error }}
      </div>
      <div v-else>
        <!-- Podium Display -->
        <div class="flex justify-center items-end space-x-12 py-8">
          <!-- Segundo Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[1]">
            <div class="text-xl font-bold">🥈</div>
            <div class="w-48">
              <div class="bg-gray-200 p-4 rounded-t-lg">
                <div class="text-center">
                  <div class="font-bold text-lg">Pareja {{ ranking[1].numero }}</div>
                  <div class="flex flex-col items-center space-y-1">
                    <span class="text-sm font-medium">{{ nombreAntes(ranking[1].nombre) }}</span>
                    <span class="text-sm font-medium">Y</span>
                    <span class="text-sm font-medium">{{ nombreDespues(ranking[1].nombre) }}</span>
                  </div>
                  <div class="text-sm text-gray-600 mt-2">{{ ranking[1].club || 'Sin club' }}</div>
                </div>
              </div>
              <div class="bg-gray-300 h-24 p-3">
                <div class="text-center text-white">
                  <div class="font-bold text-xl">PG: {{ ranking[1].PG }}</div>
                  <div class="font-bold text-xl">PP: {{ ranking[1].PP }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Primer Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[0]">
            <div class="text-xl font-bold">🏆</div>
            <div class="w-48">
              <div class="bg-yellow-200 p-4 rounded-t-lg">
                <div class="text-center">
                  <div class="font-bold text-lg">Pareja {{ ranking[0].numero }}</div>
                  <div class="flex flex-col items-center space-y-1">
                    <span class="text-sm font-medium">{{ nombreAntes(ranking[0].nombre) }}</span>
                    <span class="text-sm font-medium">Y</span>
                    <span class="text-sm font-medium">{{ nombreDespues(ranking[0].nombre) }}</span>
                  </div>
                  <div class="text-sm text-gray-600 mt-2">{{ ranking[0].club || 'Sin club' }}</div>
                </div>
              </div>
              <div class="bg-yellow-300 h-28 p-3">
                <div class="text-center text-white">
                  <div class="font-bold text-xl">PG: {{ ranking[0].PG }}</div>
                  <div class="font-bold text-xl">PP: {{ ranking[0].PP }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tercer Lugar -->
          <div class="flex flex-col items-center" v-if="ranking[2]">
            <div class="text-xl font-bold">🥉</div>
            <div class="w-48">
              <div class="bg-orange-200 p-4 rounded-t-lg">
                <div class="text-center">
                  <div class="font-bold text-lg">Pareja {{ ranking[2].numero }}</div>
                  <div class="flex flex-col items-center space-y-1">
                    <span class="text-sm font-medium">{{ nombreAntes(ranking[2].nombre) }}</span>
                    <span class="text-sm font-medium">Y</span>
                    <span class="text-sm font-medium">{{ nombreDespues(ranking[2].nombre) }}</span>
                  </div>
                  <div class="text-sm text-gray-600 mt-2">{{ ranking[2].club || 'Sin club' }}</div>
                </div>
              </div>
              <div class="bg-orange-300 h-20 p-3">
                <div class="text-center text-white">
                  <div class="font-bold text-xl">PG: {{ ranking[2].PG }}</div>
                  <div class="font-bold text-xl">PP: {{ ranking[2].PP }}</div>
                </div>
              </div>
            </div>
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
                    Nombre
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Club
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    PG
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    PP
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(pareja, index) in ranking" :key="pareja.id"
                    :class="{
                      'bg-yellow-200': index === 0,
                      'bg-gray-200': index === 1,
                      'bg-orange-200': index === 2
                    }">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <span class="text-lg font-bold text-gray-900 bg-gray-100 rounded-full w-8 h-8 flex items-center justify-center">
                        {{ index + 1 }}
                      </span>
                      <span v-if="index < 3" class="ml-2">
                        {{ index === 0 ? '🏆' : index === 1 ? '🥈' : '🥉' }}
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ pareja.numero }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.nombre }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.club || 'Sin club' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.PG }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ pareja.PP }}
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
import { ref, onMounted, computed } from 'vue'
import { useRankingStore } from '@/stores/ranking'
import { useCampeonatoStore } from '@/stores/campeonato'

const rankingStore = useRankingStore()
const campeonatoStore = useCampeonatoStore()

const ranking = ref([])
const isLoading = ref(true)
const error = ref('')

const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

const campeonatoFinalizado = computed(() => {
  return campeonatoActual.value?.partida_actual >= campeonatoActual.value?.numero_partidas
})

onMounted(async () => {
  if (campeonatoFinalizado.value) {
    await cargarRanking()
  } else {
    isLoading.value = false
  }
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

// Funciones para separar el nombre
const nombreAntes = (nombre: string) => {
  return nombre.split(' Y ')[0]
}

const nombreDespues = (nombre: string) => {
  return nombre.split(' Y ')[1]
}
</script> 