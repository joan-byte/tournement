/**
 * @component RegistroResultado.vue
 * @description Componente para registrar los resultados de una partida entre dos parejas
 * @responsibilities 
 * - Mostrar formulario de registro de resultados
 * - Manejar casos especiales (parejas que descansan)
 * - Validar y guardar resultados
 */
<script setup lang="ts">
// Importaciones necesarias para el componente
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMesaStore } from '@/stores/mesa'
import { useResultadoStore } from '@/stores/resultado'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { Mesa, Campeonato } from '@/types'
import type { MesaStore } from '@/types/store'

// Inicialización de stores y router
const route = useRoute()
const router = useRouter()
const mesaStore = useMesaStore() as MesaStore
const resultadoStore = useResultadoStore()
const campeonatoStore = useCampeonatoStore()

// Estado reactivo del componente
const mesa = ref<Mesa | null>(null)
const isLoading = ref(true)
const error = ref('')

// Agregar esta computed property
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

/**
 * @description Estructura inicial del formulario de resultados
 * RP: Resultado Partida
 * PG: Partidas Ganadas
 * PP: Puntos Partida
 * GB: Grupo (A/B)
 */
const formData = ref({
  pareja1: {
    RP: 0,
    PG: 0,
    PP: 0,
    GB: 'A'
  },
  pareja2: {
    RP: 0,
    PG: 0,
    PP: 0,
    GB: 'A'
  }
})

// Agregar computed properties para los cálculos en tiempo real
const calculosPareja1 = computed(() => {
  const rp1 = Number(formData.value.pareja1.RP)
  const rp2 = Number(formData.value.pareja2.RP)
  const diferencia = rp1 - rp2
  return {
    PG: rp1 > rp2 ? 1 : 0,
    PP: diferencia // Positivo si gana, negativo si pierde
  }
})

const calculosPareja2 = computed(() => {
  const rp1 = Number(formData.value.pareja1.RP)
  const rp2 = Number(formData.value.pareja2.RP)
  const diferencia = rp2 - rp1
  return {
    PG: rp2 > rp1 ? 1 : 0,
    PP: diferencia // Positivo si gana, negativo si pierde
  }
})

// Computed para validaciones en tiempo real
const validaciones = computed(() => {
  const rp1 = Number(formData.value.pareja1.RP)
  const rp2 = Number(formData.value.pareja2.RP)
  const sumaTotal = rp1 + rp2
  
  return {
    excede300: rp1 > 300 || rp2 > 300,
    esNegativo: rp1 < 0 || rp2 < 0,
    sonIguales: rp1 === rp2 && (rp1 !== 0 || rp2 !== 0),
    sumaInvalida: (sumaTotal < 1 || sumaTotal > 599) && (rp1 !== 0 || rp2 !== 0),
    sumaActual: sumaTotal
  }
})

/**
 * @function loadMesa
 * @description Carga los datos de la mesa y sus resultados previos si existen
 * @async
 */
const loadMesa = async () => {
  try {
    const mesaId = Number(route.params.mesaId)
    const mesaData = await mesaStore.getMesa(mesaId)
    mesa.value = mesaData

    if (mesaData && mesaData.pareja1 && !mesaData.pareja2) {
      formData.value = {
        pareja1: {
          RP: 150,
          PG: 1,
          PP: 150,
          GB: 'A'
        },
        pareja2: {
          RP: 0,
          PG: 0,
          PP: 0,
          GB: 'A'
        }
      }
      await handleSubmit()
    }

    const resultado = await resultadoStore.getResultadoMesa(
      mesaId, 
      campeonatoActual.value?.partida_actual || 0
    )
    if (resultado) {
      formData.value = {
        pareja1: {
          RP: resultado.pareja1.RP,
          PG: resultado.pareja1.PG,
          PP: resultado.pareja1.PP,
          GB: resultado.pareja1.GB
        },
        pareja2: resultado.pareja2 ? {
          RP: resultado.pareja2.RP,
          PG: resultado.pareja2.PG,
          PP: resultado.pareja2.PP,
          GB: resultado.pareja2.GB
        } : {
          RP: 0,
          PG: 0,
          PP: 0,
          GB: 'A'
        }
      }
    }
  } catch (e) {
    error.value = 'Error al cargar la mesa'
  } finally {
    isLoading.value = false
  }
}

/**
 * @function handleSubmit
 * @description Maneja el envío del formulario y guarda los resultados
 * @async
 */
const handleSubmit = async () => {
  try {
    if (!mesa.value || !campeonatoActual.value) return

    const partidaActual = campeonatoActual.value.partida_actual

    const resultado = {
      mesa_id: mesa.value.id,
      campeonato_id: campeonatoActual.value.id,
      partida: partidaActual,
      pareja1: {
        id: mesa.value.pareja1.id,
        RP: Number(formData.value.pareja1.RP),
        PG: calculosPareja1.value.PG,
        PP: calculosPareja1.value.PP,
        GB: formData.value.pareja1.GB
      },
      pareja2: {
        id: mesa.value.pareja2.id,
        RP: Number(formData.value.pareja2.RP),
        PG: calculosPareja2.value.PG,
        PP: calculosPareja2.value.PP,
        GB: formData.value.pareja2.GB
      }
    }

    await resultadoStore.saveResultado(resultado)
    router.push('/mesas/resultados')
  } catch (e) {
    error.value = 'Error al guardar el resultado'
  }
}

// Cargar datos al montar el componente
onMounted(loadMesa)
</script>

<!-- Template con formulario de registro de resultados -->
<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Cabecera con información de la mesa -->
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Registro de Resultado - Mesa {{ mesa?.numero }}
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          Partida {{ campeonatoActual?.partida_actual }}
        </p>
      </div>

      <!-- Estados de carga y error -->
      <div v-if="isLoading" class="p-4 text-center">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
      </div>
      <div v-else-if="error" class="p-4 text-center text-red-600">
        {{ error }}
      </div>

      <!-- Formulario de registro de resultados -->
      <div v-else class="border-t border-gray-200">
        <form @submit.prevent="handleSubmit" class="p-4">
          <div class="space-y-6">
            <!-- Pareja 1 -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900">
                  Pareja {{ mesa?.pareja1?.numero }}
                </h4>
                <p class="text-sm text-gray-500">{{ mesa?.pareja1?.nombre }}</p>
              </div>
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
                <div>
                  <label for="pareja1-rp" class="block text-sm font-medium text-gray-700">
                    Resultado Partida (RP)
                  </label>
                  <input
                    type="number"
                    id="pareja1-rp"
                    v-model="formData.pareja1.RP"
                    required
                    min="0"
                    max="300"
                    step="1"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <span class="block text-sm font-medium text-gray-700">
                    Partidas Ganadas (PG)
                  </span>
                  <div class="mt-2 text-sm text-gray-900">
                    {{ calculosPareja1.PG }}
                  </div>
                </div>
                <div>
                  <span class="block text-sm font-medium text-gray-700">
                    Puntos Partida (PP)
                  </span>
                  <div class="mt-2 text-sm text-gray-900">
                    {{ calculosPareja1.PP }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Pareja 2 -->
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900">
                  Pareja {{ mesa?.pareja2?.numero }}
                </h4>
                <p class="text-sm text-gray-500">{{ mesa?.pareja2?.nombre }}</p>
              </div>
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
                <div>
                  <label for="pareja2-rp" class="block text-sm font-medium text-gray-700">
                    Resultado Partida (RP)
                  </label>
                  <input
                    type="number"
                    id="pareja2-rp"
                    v-model="formData.pareja2.RP"
                    required
                    min="0"
                    max="300"
                    step="1"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <span class="block text-sm font-medium text-gray-700">
                    Partidas Ganadas (PG)
                  </span>
                  <div class="mt-2 text-sm text-gray-900">
                    {{ calculosPareja2.PG }}
                  </div>
                </div>
                <div>
                  <span class="block text-sm font-medium text-gray-700">
                    Puntos Partida (PP)
                  </span>
                  <div class="mt-2 text-sm text-gray-900">
                    {{ calculosPareja2.PP }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Validaciones generales -->
            <div v-if="formData.pareja1.RP && formData.pareja2.RP" class="text-sm text-red-600">
              <p v-if="validaciones.sonIguales">Los resultados no pueden ser iguales</p>
              <p v-if="validaciones.sumaInvalida">
                La suma debe estar entre 1 y 599 (actual: {{ validaciones.sumaActual }})
              </p>
            </div>

            <!-- Botones de acción -->
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="$router.push('/mesas/resultados')"
                class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="validaciones.excede300 || validaciones.esNegativo || validaciones.sonIguales || validaciones.sumaInvalida"
                class="inline-flex justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Guardar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template> 