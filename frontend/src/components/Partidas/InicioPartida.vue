<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Inicio de Partida
        </h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <!-- Lista de parejas -->
      <div class="border-t border-gray-200">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Listado de Parejas Inscritas
          </h3>
        </div>

        <div class="border-t border-gray-200">
          <div v-if="isLoading" class="text-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          </div>
          <div v-else-if="error" class="text-red-500 text-center py-4">
            {{ error }}
          </div>
          <div v-else-if="!campeonatoActual" class="text-center py-4 text-gray-500">
            Seleccione un campeonato para ver las parejas
          </div>
          <div v-else-if="parejas.length === 0" class="text-center py-4 text-gray-500">
            No hay parejas registradas
          </div>
          <ul v-else role="list" class="divide-y divide-gray-200">
            <li
              v-for="pareja in parejasOrdenadas"
              :key="pareja.id"
              class="px-4 py-4 sm:px-6 hover:bg-gray-50"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <!-- Número de pareja -->
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-blue-100 text-blue-900 text-xl font-bold">
                      {{ pareja.numero }}
                    </span>
                  </div>
                  <!-- Nombre y club -->
                  <div class="flex-grow">
                    <div class="flex items-center space-x-2">
                      <p class="text-sm font-medium text-gray-900">
                        {{ pareja.nombre }}
                      </p>
                      <span class="text-gray-400">|</span>
                      <p class="text-sm text-gray-500">
                        {{ pareja.club || 'Sin club' }}
                      </p>
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-4">
                  <span
                    :class="[
                      pareja.activa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800',
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
                    ]"
                  >
                    {{ pareja.activa ? 'Activa' : 'Inactiva' }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Botón de inicio/reinicio -->
      <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
        <button
          v-if="mesasAsignadas"
          type="button"
          @click="reiniciarSorteo"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Reiniciar Sorteo
        </button>
        <button
          v-else
          type="button"
          @click="iniciarPartida"
          :disabled="!puedeIniciar"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ esPrimeraPartida ? 'Iniciar Campeonato' : 'Iniciar Partida' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useParejaStore } from '@/stores/pareja'
import { useMesaStore } from '@/stores/mesa'
import type { Campeonato, Pareja } from '@/types'

const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const parejaStore = useParejaStore()
const mesaStore = useMesaStore()

const campeonatoActual = ref<Campeonato | null>(null)
const parejas = ref<Pareja[]>([])
const isLoading = ref(true)
const error = ref('')
const mesasAsignadas = ref(false)

const parejasOrdenadas = computed(() => {
  if (!Array.isArray(parejas.value)) return []
  return [...parejas.value]
    .filter(p => p && typeof p.numero === 'number')
    .sort((a, b) => (b.numero as number) - (a.numero as number))
})

const puedeIniciar = computed(() => {
  const parejasActivas = parejas.value.filter((p: Pareja) => p.activa)
  return parejasActivas.length >= 4
})

const esPrimeraPartida = computed(() => {
  return campeonatoActual.value?.partida_actual === 0
})

onMounted(async () => {
  campeonatoActual.value = campeonatoStore.getCurrentCampeonato()
  if (campeonatoActual.value) {
    await loadParejas()
  } else {
    router.push('/campeonatos')
  }
})

const loadParejas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const response = await parejaStore.fetchParejasCampeonato(campeonatoActual.value.id)
      parejas.value = Array.isArray(response) ? response : []
    }
  } catch (e) {
    console.error('Error al cargar parejas:', e)
    error.value = 'Error al cargar las parejas'
    parejas.value = []
  } finally {
    isLoading.value = false
  }
}

const iniciarPartida = async () => {
  try {
    if (!campeonatoActual.value) return
    
    if (esPrimeraPartida.value) {
      await mesaStore.sortearMesas(campeonatoActual.value.id)
      mesasAsignadas.value = true
    } else {
      await campeonatoStore.updateCampeonato(campeonatoActual.value.id, {
        partida_actual: campeonatoActual.value.partida_actual + 1
      })
      router.push('/partidas/registro')
    }
  } catch (e) {
    console.error('Error al iniciar partida:', e)
    error.value = 'Error al iniciar la partida'
  }
}

const reiniciarSorteo = async () => {
  try {
    if (!campeonatoActual.value) return
    
    // Eliminar las asignaciones de mesas
    await mesaStore.eliminarMesas(campeonatoActual.value.id)
    mesasAsignadas.value = false
    
    // Recargar las parejas para actualizar la vista
    await loadParejas()
  } catch (e) {
    console.error('Error al reiniciar sorteo:', e)
    error.value = 'Error al reiniciar el sorteo'
  }
}
</script> 