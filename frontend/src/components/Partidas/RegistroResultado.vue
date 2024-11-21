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
import type { Mesa } from '@/types'
import type { MesaStore } from '@/types/store'

// Inicialización de stores y router
const route = useRoute()
const router = useRouter()
const mesaStore = useMesaStore() as MesaStore
const resultadoStore = useResultadoStore()

// Estado reactivo del componente
const mesa = ref<Mesa | null>(null)
const isLoading = ref(true)
const error = ref('')

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

    // Manejo especial para mesa con una sola pareja (descansa)
    if (mesaData && mesaData.pareja1 && !mesaData.pareja2) {
      formData.value = {
        pareja1: {
          RP: 150,  // La pareja que juega recibe 150 puntos
          PG: 1,    // Gana la partida
          PP: 150,  // Puntos de partida igual a RP
          GB: 'A'
        },
        pareja2: {
          RP: 0,    // La pareja que no existe recibe 0
          PG: 0,    // No gana la partida
          PP: 0,    // No recibe puntos
          GB: 'A'
        }
      }
      // Guardar automáticamente el resultado
      await handleSubmit()
    }

    // Carga de resultados previos si existen
    const resultado = await resultadoStore.getResultadoMesa(mesaId, mesaData.campeonato_id)
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
    console.error('Error al cargar mesa:', e)
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
    if (!mesa.value) return

    const resultado = {
      pareja1: {
        campeonato_id: mesa.value.campeonato_id,
        partida_actual: mesa.value.campeonato_id,
        mesa_id: mesa.value.id,
        id_pareja: mesa.value.pareja1_id,
        ...formData.value.pareja1
      },
      pareja2: mesa.value.pareja2_id ? {
        campeonato_id: mesa.value.campeonato_id,
        partida_actual: mesa.value.campeonato_id,
        mesa_id: mesa.value.id,
        id_pareja: mesa.value.pareja2_id,
        ...formData.value.pareja2
      } : undefined
    }

    await resultadoStore.saveResultado(resultado)
    router.push('/mesas/resultados')
  } catch (e) {
    console.error('Error al guardar resultado:', e)
    error.value = 'Error al guardar el resultado'
  }
}

// Cargar datos al montar el componente
onMounted(loadMesa)
</script>

<!-- Template con formulario de registro de resultados -->
<template>
  <!-- Contenedor principal -->
  <div class="container mx-auto p-4">
    <!-- Tarjeta principal con información y formulario -->
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
                  <label for="rp1" class="block text-sm font-medium text-gray-700">
                    Resultado Partida (RP)
                  </label>
                  <input
                    type="number"
                    id="rp1"
                    v-model="formData.pareja1.RP"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="pg1" class="block text-sm font-medium text-gray-700">
                    Partidas Ganadas (PG)
                  </label>
                  <input
                    type="number"
                    id="pg1"
                    v-model="formData.pareja1.PG"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="pp1" class="block text-sm font-medium text-gray-700">
                    Puntos Partida (PP)
                  </label>
                  <input
                    type="number"
                    id="pp1"
                    v-model="formData.pareja1.PP"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="gb1" class="block text-sm font-medium text-gray-700">
                    Grupo (GB)
                  </label>
                  <select
                    id="gb1"
                    v-model="formData.pareja1.GB"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="A">A</option>
                    <option value="B">B</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Pareja 2 (si existe) -->
            <div v-if="mesa?.pareja2" class="bg-gray-50 p-4 rounded-lg">
              <div class="mb-4">
                <h4 class="text-lg font-medium text-gray-900">
                  Pareja {{ mesa.pareja2.numero }}
                </h4>
                <p class="text-sm text-gray-500">{{ mesa.pareja2.nombre }}</p>
              </div>
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
                <div>
                  <label for="rp2" class="block text-sm font-medium text-gray-700">
                    Resultado Partida (RP)
                  </label>
                  <input
                    type="number"
                    id="rp2"
                    v-model="formData.pareja2.RP"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="pg2" class="block text-sm font-medium text-gray-700">
                    Partidas Ganadas (PG)
                  </label>
                  <input
                    type="number"
                    id="pg2"
                    v-model="formData.pareja2.PG"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="pp2" class="block text-sm font-medium text-gray-700">
                    Puntos Partida (PP)
                  </label>
                  <input
                    type="number"
                    id="pp2"
                    v-model="formData.pareja2.PP"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label for="gb2" class="block text-sm font-medium text-gray-700">
                    Grupo (GB)
                  </label>
                  <select
                    id="gb2"
                    v-model="formData.pareja2.GB"
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="A">A</option>
                    <option value="B">B</option>
                  </select>
                </div>
              </div>
            </div>

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
                class="inline-flex justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
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