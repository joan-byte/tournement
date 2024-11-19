<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Registro de Resultado - Mesa {{ mesa?.numero }}
          </h3>
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual || 1 }}
          </span>
        </div>
      </div>

      <div class="border-t border-gray-200 px-4 py-5">
        <form @submit.prevent="handleSubmit">
          <!-- Pareja 1 -->
          <div class="mb-6">
            <div class="flex items-center space-x-4 mb-2">
              <span class="text-sm font-medium text-gray-900">{{ mesa?.pareja1?.numero }}</span>
              <span class="text-sm text-gray-500">{{ mesa?.pareja1?.nombre }}</span>
            </div>
            <div class="grid grid-cols-4 gap-4">
              <div>
                <label for="pareja1_rp" class="block text-sm font-medium text-gray-700">
                  Resultado Partida <span class="text-xs text-gray-500">(RP)</span>
                </label>
                <input
                  type="number"
                  id="pareja1_rp"
                  name="pareja1_rp"
                  v-model="formData.pareja1.RP"
                  required
                  min="0"
                  max="300"
                  @input="calcularResultados"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Puntos Partida <span class="text-xs text-gray-500">(PP)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja1.PP }}
                </div>
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Partidas Ganadas <span class="text-xs text-gray-500">(PG)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja1.PG }}
                </div>
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Grupo <span class="text-xs text-gray-500">(GB)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja1.GB }}
                </div>
              </div>
            </div>
          </div>

          <!-- Pareja 2 -->
          <div v-if="mesa?.pareja2" class="mb-6">
            <div class="flex items-center space-x-4 mb-2">
              <span class="text-sm font-medium text-gray-900">{{ mesa.pareja2.numero }}</span>
              <span class="text-sm text-gray-500">{{ mesa.pareja2.nombre }}</span>
            </div>
            <div class="grid grid-cols-4 gap-4">
              <div>
                <label for="pareja2_rp" class="block text-sm font-medium text-gray-700">
                  Resultado Partida <span class="text-xs text-gray-500">(RP)</span>
                </label>
                <input
                  type="number"
                  id="pareja2_rp"
                  name="pareja2_rp"
                  v-model="formData.pareja2.RP"
                  required
                  min="0"
                  max="300"
                  @input="calcularResultados"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Puntos Partida <span class="text-xs text-gray-500">(PP)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja2.PP }}
                </div>
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Partidas Ganadas <span class="text-xs text-gray-500">(PG)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja2.PG }}
                </div>
              </div>
              <div>
                <div class="block text-sm font-medium text-gray-700">
                  Grupo <span class="text-xs text-gray-500">(GB)</span>
                </div>
                <div class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-50 rounded-md text-sm">
                  {{ formData.pareja2.GB }}
                </div>
              </div>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="$router.back()"
              class="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white"
              :class="tieneResultadoPrevio ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-primary-600 hover:bg-primary-700'"
            >
              {{ tieneResultadoPrevio ? 'Modificar' : 'Registrar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import { useResultadoStore } from '@/stores/resultado'

const route = useRoute()
const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const mesaStore = useMesaStore()
const resultadoStore = useResultadoStore()

const mesa = ref<any>(null)
const isLoading = ref(true)
const error = ref('')

const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

interface ResultadoPareja {
  RP: number
  PP: number
  PG: number
  GB: string
  id_pareja: number
}

// Definir la interfaz para los datos del resultado
interface ResultadoData {
  mesa_id: number
  campeonato_id: number
  pareja1: ResultadoPareja
  pareja2?: ResultadoPareja  // Hacerlo opcional con ?
}

const formData = ref({
  pareja1: {
    RP: 0,
    PP: 0,
    PG: 0,
    GB: 'A',
    id_pareja: 0
  } as ResultadoPareja,
  pareja2: {
    RP: 0,
    PP: 0,
    PG: 0,
    GB: 'A',
    id_pareja: 0
  } as ResultadoPareja
})

const calcularResultados = () => {
  // Convertir a números
  const rp1 = Number(formData.value.pareja1.RP)
  const rp2 = Number(formData.value.pareja2.RP)

  // Validaciones
  if (rp1 === rp2 && rp1 !== 0) {
    alert('Los resultados de las parejas no pueden ser iguales')
    // Determinar cuál fue el último número introducido y solo borrar ese
    const lastModified = document.activeElement?.id
    if (lastModified === 'pareja2_rp') {
      formData.value.pareja2.RP = 0
    } else {
      formData.value.pareja1.RP = 0
    }
    return false
  }

  if (rp1 < 0 || rp2 < 0) {
    alert('Los resultados no pueden ser negativos')
    if (rp1 < 0) formData.value.pareja1.RP = 0
    if (rp2 < 0) formData.value.pareja2.RP = 0
    return false
  }

  if (rp1 > 300 || rp2 > 300) {
    alert('Los resultados no pueden ser mayores a 300')
    if (rp1 > 300) formData.value.pareja1.RP = 0
    if (rp2 > 300) formData.value.pareja2.RP = 0
    return false
  }

  // Calcular PP (diferencia entre RP propio y RP contrario)
  formData.value.pareja1.PP = rp1 - rp2
  formData.value.pareja2.PP = rp2 - rp1

  // Calcular PG (1 si PP es positivo, 0 si es negativo)
  formData.value.pareja1.PG = formData.value.pareja1.PP > 0 ? 1 : 0
  formData.value.pareja2.PG = formData.value.pareja2.PP > 0 ? 1 : 0

  // GB siempre es 'A' por ahora
  formData.value.pareja1.GB = 'A'
  formData.value.pareja2.GB = 'A'

  return true
}

const tieneResultadoPrevio = ref(false)

// Agregar función para verificar si hay resultados en la partida actual
const verificarResultadosPartida = async () => {
  try {
    if (!campeonatoActual.value) return false

    const resultados = await resultadoStore.fetchResultados(campeonatoActual.value.id)
    
    // Verificar si hay resultados para la partida actual
    return resultados && resultados.some(r => 
      r.partida === campeonatoActual.value?.partida_actual &&
      (r.PG !== 0 || r.PP !== 0 || r.RP !== 0)
    )
  } catch (error) {
    console.error('Error al verificar resultados:', error)
    return false
  }
}

const loadMesa = async () => {
  try {
    const mesaId = parseInt(route.params.mesaId as string)
    if (campeonatoActual.value) {
      // Cargar datos de la mesa
      const mesaResponse = await mesaStore.getMesa(mesaId)
      mesa.value = mesaResponse

      // Cargar resultados existentes si los hay
      const resultados = await resultadoStore.getResultadoMesa(
        mesaId,
        campeonatoActual.value.partida_actual
      )

      // Verificar si hay resultados para esta mesa o para cualquier otra en la partida actual
      tieneResultadoPrevio.value = !!resultados || await verificarResultadosPartida()

      if (resultados) {
        // Si hay resultados existentes, cargarlos en el formulario
        formData.value = {
          pareja1: {
            RP: resultados.pareja1.RP,
            PP: resultados.pareja1.PP,
            PG: resultados.pareja1.PG,
            GB: resultados.pareja1.GB,
            id_pareja: resultados.pareja1.id_pareja
          },
          pareja2: resultados.pareja2 ? {
            RP: resultados.pareja2.RP,
            PP: resultados.pareja2.PP,
            PG: resultados.pareja2.PG,
            GB: resultados.pareja2.GB,
            id_pareja: resultados.pareja2.id_pareja
          } : {
            RP: 0,
            PP: 0,
            PG: 0,
            GB: 'A',
            id_pareja: 0
          }
        }
      } else {
        // Si no hay resultados, inicializar con los IDs de las parejas
        formData.value = {
          pareja1: {
            ...formData.value.pareja1,
            id_pareja: mesa.value.pareja1.id
          },
          pareja2: mesa.value.pareja2 ? {
            ...formData.value.pareja2,
            id_pareja: mesa.value.pareja2.id
          } : formData.value.pareja2
        }
      }
    }
  } catch (e) {
    console.error('Error al cargar mesa:', e)
    error.value = 'Error al cargar los datos de la mesa'
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  try {
    if (!campeonatoActual.value || !mesa.value) return

    if (!calcularResultados()) return

    const resultadoData: ResultadoData = {
      mesa_id: mesa.value.id,
      campeonato_id: mesa.value.campeonato_id,
      pareja1: {
        ...formData.value.pareja1,
        id_pareja: mesa.value.pareja1.id
      }
    }

    // Solo incluir pareja2 si existe
    if (mesa.value.pareja2) {
      resultadoData.pareja2 = {
        ...formData.value.pareja2,
        id_pareja: mesa.value.pareja2.id
      }
    }

    await resultadoStore.saveResultado(resultadoData)
    router.push('/mesas/resultados')
  } catch (e) {
    console.error('Error al guardar resultado:', e)
    error.value = 'Error al guardar el resultado'
  }
}

onMounted(async () => {
  await loadMesa()
})
</script> 