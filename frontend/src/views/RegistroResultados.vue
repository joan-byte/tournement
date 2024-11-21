/**
 * @component RegistroResultados
 * @description Vista principal para el registro de resultados de las partidas en curso
 * @responsibilities 
 * - Mostrar todas las mesas activas y su estado
 * - Permitir registrar/modificar resultados por mesa
 * - Gestionar el cierre de partidas y finalización del campeonato
 */
<template>
  <div class="container mx-auto p-4">
    <!-- Panel principal con información del registro de resultados -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <!-- Título de la sección -->
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Registro de Resultados
          </h3>
          <!-- Indicador de partida actual -->
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual }}
          </span>
        </div>
        <!-- Botón de cierre de partida o finalización de campeonato -->
        <div v-if="todasMesasRegistradas" class="mt-4">
          <button
            @click="esUltimaPartida ? finalizarCampeonato() : cerrarPartida()"
            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white"
            :class="esUltimaPartida ? 'bg-green-600 hover:bg-green-700' : 'bg-primary-600 hover:bg-primary-700'"
          >
            {{ esUltimaPartida ? 'Finalizar Campeonato' : 'Cerrar Partida' }}
          </button>
        </div>
      </div>

      <!-- Listado de mesas y sus estados -->
      <div class="border-t border-gray-200">
        <!-- Estados de visualización -->
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!mesas.length" class="text-center py-4 text-gray-500">
          No hay mesas asignadas
        </div>
        <!-- Lista de mesas con sus parejas y botones de acción -->
        <div v-else class="divide-y divide-gray-200">
          <div v-for="mesa in mesas" :key="mesa.id" class="mb-4">
            <div class="flex justify-between items-center p-4 bg-white rounded-lg shadow">
              <div class="grid grid-cols-12 gap-4 items-center flex-grow mr-8">
                <span class="font-medium col-span-2">Mesa {{ mesa.numero }}</span>
                <span class="text-gray-600 col-span-4 text-left">
                  {{ mesa.pareja1?.numero }} - {{ mesa.pareja1?.nombre }}
                </span>
                <span v-if="mesa.pareja2" class="text-gray-500 col-span-2 text-center">vs</span>
                <span v-if="mesa.pareja2" class="text-gray-600 col-span-4 text-left">
                  {{ mesa.pareja2.numero }} - {{ mesa.pareja2.nombre }}
                </span>
              </div>
              <button
                @click="registrarResultado(mesa)"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white"
                :class="mesa.tieneResultado ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-primary-600 hover:bg-primary-700'"
              >
                {{ mesa.tieneResultado ? 'Modificar' : 'Registrar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Importaciones necesarias para el componente
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import { useRouter } from 'vue-router'
import { usePartidaStore } from '@/stores/partida'
import type { Campeonato, Mesa } from '@/types'
import type { CampeonatoStore } from '@/types/store'

// Inicialización de stores y router
const router = useRouter()
const campeonatoStore = useCampeonatoStore() as CampeonatoStore
const mesaStore = useMesaStore()
const partidaStore = usePartidaStore()

// Estado reactivo del componente
const isLoading = ref(true)          // Control de estado de carga
const error = ref('')                // Mensaje de error si existe
const mesas = ref<Mesa[]>([])        // Lista de mesas activas
const campeonatoActual = ref<Campeonato | null>(null)  // Campeonato en curso

/**
 * @function loadResultados
 * @description Carga las mesas asignadas y sus resultados
 * @async
 */
const loadResultados = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const mesasResponse = await mesaStore.getMesasAsignadas(campeonatoActual.value.id)
      mesas.value = mesasResponse
    }
  } catch (e) {
    console.error('Error al cargar resultados:', e)
    error.value = 'Error al cargar los resultados'
  } finally {
    isLoading.value = false
  }
}

/**
 * @function cerrarPartida
 * @description Cierra la partida actual y prepara la siguiente
 * @async
 */
const cerrarPartida = async () => {
  try {
    if (!campeonatoActual.value) return

    const campeonatoActualizado = {
      ...campeonatoActual.value,
      partida_actual: (campeonatoActual.value.partida_actual || 0) + 1,
      fecha_inicio: campeonatoActual.value.fecha_inicio,
      dias_duracion: campeonatoActual.value.dias_duracion,
      numero_partidas: campeonatoActual.value.numero_partidas
    } as Campeonato;

    await campeonatoStore.updateCampeonato(
      campeonatoActual.value.id,
      campeonatoActualizado
    )

    await partidaStore.sortearParejas(campeonatoActual.value.id)

    campeonatoActual.value = campeonatoActualizado
    await campeonatoStore.setCampeonatoActual(campeonatoActualizado)

    router.push('/mesas')
  } catch (error) {
    console.error('Error al cerrar partida:', error)
  }
}

// Computed properties
const mesasOrdenadas = computed(() => {
  return [...mesas.value].sort((a, b) => a.numero - b.numero)
})

/**
 * @function registrarResultado
 * @description Navega a la vista de registro de resultado para una mesa específica
 */
const registrarResultado = (mesa: Mesa) => {
  router.push(`/partidas/resultado/${mesa.id}`)
}

/**
 * @computed todasMesasRegistradas
 * @description Verifica si todas las mesas tienen resultados registrados
 */
const todasMesasRegistradas = computed(() => {
  return mesas.value.length > 0 && mesas.value.every(mesa => mesa.tieneResultado)
})

/**
 * @computed esUltimaPartida
 * @description Determina si es la última partida del campeonato
 */
const esUltimaPartida = computed(() => {
  return campeonatoActual.value?.partida_actual === campeonatoActual.value?.numero_partidas
})

/**
 * @function finalizarCampeonato
 * @description Finaliza el campeonato y redirige al podium
 */
const finalizarCampeonato = async () => {
  try {
    if (!campeonatoActual.value) return
    router.push('/podium')
  } catch (error) {
    console.error('Error al finalizar campeonato:', error)
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