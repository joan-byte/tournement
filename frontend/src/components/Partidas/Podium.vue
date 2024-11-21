<!-- 
  Podium.vue - Componente para mostrar el podio y ranking final del campeonato
  Muestra las tres primeras parejas en un podio visual y una tabla completa
  con todas las parejas participantes ordenadas por posición.
-->

<template>
  <div class="container mx-auto p-4">
    <!-- Panel principal con el contenido del podio -->
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <!-- Cabecera con título y nombre del campeonato -->
      <div class="px-4 py-5 sm:px-6">
        <h2 class="text-2xl font-bold text-center mb-4">
          🏆 Podium del Campeonato 🏆
        </h2>
        <p class="text-center text-gray-600">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <!-- Mensaje cuando el campeonato no ha finalizado -->
      <div v-if="!campeonatoFinalizado" class="text-center py-8 text-red-600">
        <p class="text-lg font-medium">El campeonato aún no ha finalizado</p>
        <p class="text-sm mt-2">El podium estará disponible cuando se complete la última partida</p>
      </div>

      <!-- Indicador de carga -->
      <div v-else-if="isLoading" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
      </div>

      <!-- Mensaje de error si algo falla -->
      <div v-else-if="error" class="text-red-500 text-center py-8">
        {{ error }}
      </div>

      <!-- Contenido principal del podio y ranking -->
      <div v-else>
        <!-- Visualización del Podio -->
        <div class="flex justify-center items-end space-x-12 py-8">
          <!-- Segundo Lugar - Medalla de Plata -->
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

          <!-- Primer Lugar - Trofeo de Oro -->
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

          <!-- Tercer Lugar - Medalla de Bronce -->
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

        <!-- Tabla completa del Ranking -->
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
// Importaciones necesarias para el componente
import { ref, onMounted, computed } from 'vue'
import { useRankingStore } from '@/stores/ranking'
import { useCampeonatoStore } from '@/stores/campeonato'

// Inicialización de los stores necesarios
const rankingStore = useRankingStore()
const campeonatoStore = useCampeonatoStore()

// Estado reactivo del componente
const ranking = ref([])           // Almacena los datos del ranking
const isLoading = ref(true)       // Control de estado de carga
const error = ref('')             // Mensajes de error

/**
 * Computed: Obtiene el campeonato actual del store
 */
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

/**
 * Computed: Determina si el campeonato ha finalizado
 * Compara la partida actual con el número total de partidas
 */
const campeonatoFinalizado = computed(() => {
  return campeonatoActual.value?.partida_actual >= campeonatoActual.value?.numero_partidas
})

/**
 * Hook: Se ejecuta al montar el componente
 * Carga el ranking si el campeonato está finalizado
 */
onMounted(async () => {
  if (campeonatoFinalizado.value) {
    await cargarRanking()
  } else {
    isLoading.value = false
  }
})

/**
 * Carga los datos del ranking final desde el servidor
 * Maneja estados de carga y posibles errores
 */
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

/**
 * Extrae el nombre antes del separador "Y" de una pareja
 * @param nombre - Nombre completo de la pareja
 * @returns Nombre del primer jugador
 */
const nombreAntes = (nombre: string) => {
  return nombre.split(' Y ')[0]
}

/**
 * Extrae el nombre después del separador "Y" de una pareja
 * @param nombre - Nombre completo de la pareja
 * @returns Nombre del segundo jugador
 */
const nombreDespues = (nombre: string) => {
  return nombre.split(' Y ')[1]
}
</script> 