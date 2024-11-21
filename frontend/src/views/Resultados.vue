/**
 * @component Resultados.vue
 * @description Componente que muestra el ranking actual del torneo
 * @responsibilities 
 * - Mostrar la clasificación actual de parejas
 * - Visualizar estadísticas (PG, PP, GB)
 * - Destacar posiciones relevantes (podium)
 */
<template>
  <!-- Contenedor principal del ranking -->
  <div class="container mx-auto p-4">
    <!-- Panel principal con sombra y bordes redondeados -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Cabecera con título y número de partida actual -->
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Ranking del Torneo
          </h3>
          <!-- Indicador de partida actual -->
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual || 1 }}
          </span>
        </div>
      </div>

      <!-- Sección de la tabla de resultados -->
      <div class="border-t border-gray-200">
        <!-- Estados de visualización -->
        <!-- Spinner de carga -->
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <!-- Mensaje de error si existe -->
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <!-- Mensaje cuando no hay resultados -->
        <div v-else-if="!resultados.length" class="text-center py-4 text-gray-500">
          No hay resultados disponibles
        </div>
        <!-- Tabla de resultados -->
        <div v-else>
          <!-- Encabezados de la tabla -->
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <!-- Pos: Posición actual en el ranking -->
                <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Pos.
                </th>
                <!-- Part: Última partida jugada -->
                <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Part.
                </th>
                <!-- GB: Games Behind (diferencia con el líder) -->
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  GB
                </th>
                <!-- PG: Partidas Ganadas -->
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  PG
                </th>
                <!-- PP: Partidas Perdidas -->
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  PP
                </th>
                <!-- Nº: Número de pareja -->
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nº
                </th>
                <!-- Nombre de la pareja -->
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <!-- Club al que pertenece -->
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Club
                </th>
              </tr>
            </thead>
            <!-- Cuerpo de la tabla con los resultados -->
            <tbody class="bg-white divide-y divide-gray-200">
              <!-- Iteración sobre cada resultado -->
              <tr v-for="resultado in resultados" :key="resultado.pareja_id" 
                  :class="getPosicionClass(resultado.posicion)">
                <!-- Columnas con la información de cada pareja -->
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
// Importaciones necesarias para el componente
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useResultadoStore } from '@/stores/resultado'
import type { Campeonato } from '@/types'
import type { RankingResultado } from '@/types/resultado'

// Inicialización de stores
const campeonatoStore = useCampeonatoStore()
const resultadoStore = useResultadoStore()

// Estado reactivo del componente
const campeonatoActual = ref<Campeonato | null>(null)  // Campeonato actual
const resultados = ref<RankingResultado[]>([])         // Lista de resultados
const isLoading = ref(true)                           // Estado de carga
const error = ref('')                                 // Mensaje de error

/**
 * @function getPosicionClass
 * @description Asigna clases CSS según la posición en el ranking
 * @param posicion Posición actual de la pareja
 * @returns Clase CSS correspondiente al podium
 */
const getPosicionClass = (posicion: number) => {
  switch (posicion) {
    case 1:
      return 'bg-yellow-50'  // Color para el primer lugar
    case 2:
      return 'bg-gray-50'    // Color para el segundo lugar
    case 3:
      return 'bg-orange-50'  // Color para el tercer lugar
    default:
      return ''
  }
}

/**
 * @function getPartidaClass
 * @description Asigna clases CSS según el estado de la partida
 * @param partida Número de la última partida jugada
 * @returns Clase CSS correspondiente al estado
 */
const getPartidaClass = (partida: number) => {
  if (!campeonatoActual.value) return ''
  
  if (partida === campeonatoActual.value.partida_actual) {
    return 'text-green-700 font-bold'      // Partida actual
  }
  if (partida < campeonatoActual.value.partida_actual) {
    return 'text-red-700 font-semibold'    // Partida anterior
  }
  return ''
}

/**
 * @function loadResultados
 * @description Carga los resultados del campeonato actual
 * @async
 */
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

// Inicialización al montar el componente
onMounted(async () => {
  const camp = campeonatoStore.getCurrentCampeonato()
  if (camp) {
    campeonatoActual.value = camp
    await loadResultados()
  }
})
</script>

/**
 * Estilos específicos para estados de partidas
 */
<style scoped>
.text-green-700 {
  color: #15803d !important;  /* Color para partida actual */
}

.text-red-700 {
  color: #b91c1c !important;  /* Color para partida anterior */
}
</style> 