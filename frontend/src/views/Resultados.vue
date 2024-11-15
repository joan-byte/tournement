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
      </div>

      <div class="border-t border-gray-200">
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!resultados.length" class="text-center py-4 text-gray-500">
          No hay resultados disponibles
        </div>
        <div v-else>
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pos.
                </th>
                <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Part.
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
                <td class="px-3 py-4 whitespace-nowrap text-sm font-medium">
                  {{ resultado.posicion }}
                </td>
                <td class="px-2 py-4 whitespace-nowrap text-sm text-center font-medium"
                    :class="getPartidaClass(resultado.ultima_partida)">
                  {{ resultado.ultima_partida }}
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
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useResultadoStore } from '@/stores/resultado'
import type { Campeonato } from '@/types'
import type { RankingResultado } from '@/types/resultado'

const campeonatoStore = useCampeonatoStore()
const resultadoStore = useResultadoStore()

const campeonatoActual = ref<Campeonato | null>(null)
const resultados = ref<RankingResultado[]>([])
const isLoading = ref(true)
const error = ref('')

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

const getPartidaClass = (partida: number) => {
  if (!campeonatoActual.value) return ''
  
  if (partida === campeonatoActual.value.partida_actual) {
    return 'text-green-700 font-bold'
  }
  if (partida < campeonatoActual.value.partida_actual) {
    return 'text-red-700 font-semibold'
  }
  return ''
}

const loadResultados = async () => {
  try {
    if (campeonatoActual.value) {
      resultados.value = await resultadoStore.fetchResultados(campeonatoActual.value.id)
    }
  } catch (e) {
    console.error('Error al cargar resultados:', e)
    error.value = 'Error al cargar los resultados'
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  const camp = campeonatoStore.getCurrentCampeonato()
  if (camp) {
    campeonatoActual.value = camp
    await loadResultados()
  }
})
</script>

<style scoped>
.text-green-700 {
  color: #15803d !important;
}

.text-red-700 {
  color: #b91c1c !important;
}
</style> 