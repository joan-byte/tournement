<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Registro de Resultados
          </h3>
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual }}
          </span>
        </div>
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

      <div class="border-t border-gray-200">
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!mesas.length" class="text-center py-4 text-gray-500">
          No hay mesas asignadas
        </div>
        <div v-else class="divide-y divide-gray-200">
          <div v-for="mesa in mesasOrdenadas" :key="mesa.numero" class="px-4 py-4">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-4">
                  <!-- Número de mesa -->
                  <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-gray-100 text-gray-900 text-xl font-bold">
                    {{ mesa.numero }}
                  </span>
                  <!-- Información de las parejas -->
                  <div class="flex-1 grid grid-cols-2 gap-4">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm font-medium text-gray-900">{{ mesa.pareja1?.numero }}</span>
                      <span class="text-sm text-gray-500">{{ mesa.pareja1?.nombre }}</span>
                    </div>
                    <div v-if="mesa.pareja2" class="flex items-center space-x-2">
                      <span class="text-sm font-medium text-gray-900">{{ mesa.pareja2?.numero }}</span>
                      <span class="text-sm text-gray-500">{{ mesa.pareja2?.nombre }}</span>
                    </div>
                    <div v-else class="text-sm text-gray-500 italic">
                      Descansa
                    </div>
                  </div>
                </div>
              </div>
              <!-- Botón de registro/modificación -->
              <button
                @click="registrarResultado(mesa)"
                :class="[
                  mesa.tieneResultado 
                    ? 'bg-yellow-600 hover:bg-yellow-700' 
                    : 'bg-primary-600 hover:bg-primary-700',
                  'inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
                ]"
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
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import { useRouter } from 'vue-router'
import { usePartidaStore } from '@/stores/partida'
import type { Campeonato, Mesa } from '@/types'
import type { CampeonatoStore } from '@/types/store'

const router = useRouter()
const campeonatoStore = useCampeonatoStore() as CampeonatoStore
const mesaStore = useMesaStore()
const partidaStore = usePartidaStore()

const isLoading = ref(true)
const error = ref('')
const mesas = ref<Mesa[]>([])
const campeonatoActual = ref<Campeonato | null>(null)

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

onMounted(async () => {
  const camp = campeonatoStore.getCurrentCampeonato()
  if (camp) {
    campeonatoActual.value = camp
    await loadResultados()
  }
})

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

const mesasOrdenadas = computed(() => {
  return [...mesas.value].sort((a, b) => a.numero - b.numero)
})

const registrarResultado = (mesa: Mesa) => {
  router.push(`/partidas/resultado/${mesa.id}`)
}

const todasMesasRegistradas = computed(() => {
  return mesas.value.length > 0 && mesas.value.every(mesa => mesa.tieneResultado)
})

const esUltimaPartida = computed(() => {
  return campeonatoActual.value?.partida_actual === campeonatoActual.value?.numero_partidas
})

const finalizarCampeonato = async () => {
  try {
    if (!campeonatoActual.value) return

    // Redirigir al podium
    router.push('/podium')
  } catch (error) {
    console.error('Error al finalizar campeonato:', error)
  }
}
</script> 