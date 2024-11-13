<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Registro de Partidas</h1>
      <div class="flex items-center">
        <button 
          v-if="todasParejasRegistradas"
          @click="finalizarPartida"
          class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mr-4"
        >
          {{ esUltimaPartida ? 'Cierre Campeonato' : 'Finalizar Partida' }}
        </button>
        <div class="text-xl font-semibold">
          Partida {{ partidaActual }}
        </div>
      </div>
    </div>

    <div v-if="isLoading">Cargando mesas y parejas...</div>
    <div v-else-if="error">{{ error }}</div>
    <table v-else class="min-w-full bg-white border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-center">Mesa</th>
          <th class="py-2 px-4 border-b text-center">Pareja 1</th>
          <th class="py-2 px-4 border-b text-center">Pareja 2</th>
          <th class="py-2 px-4 border-b text-center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mesa in mesas" :key="mesa.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center">{{ mesa.numero }}</td>
          <td class="py-2 px-4 border-b text-center">
            {{ obtenerNombrePareja(mesa.pareja1_id) }}
          </td>
          <td class="py-2 px-4 border-b text-center">
            {{ obtenerNombrePareja(mesa.pareja2_id) }}
          </td>
          <td class="py-2 px-4 border-b text-center">
            <button
              @click="registrarResultado(mesa)"
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-1 px-3 rounded"
              :disabled="mesa.tieneResultados"
            >
              {{ mesa.tieneResultados ? 'Registrado' : 'Registrar' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMesaStore } from '@/stores/mesa'
import { useParejaStore } from '@/stores/pareja'
import { usePartidaStore } from '@/stores/partida'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { Mesa, MesaConResultados, Pareja } from '@/types'

const router = useRouter()
const mesaStore = useMesaStore()
const parejaStore = useParejaStore()
const partidaStore = usePartidaStore()
const campeonatoStore = useCampeonatoStore()

const mesas = ref<MesaConResultados[]>([])
const parejas = ref<Pareja[]>([])
const isLoading = ref(true)
const error = ref('')

const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())
const partidaActual = computed(() => campeonatoActual.value?.partida_actual || 0)
const esUltimaPartida = computed(() => {
  if (!campeonatoActual.value) return false
  return partidaActual.value === campeonatoActual.value.numero_partidas
})

const todasParejasRegistradas = computed(() => {
  return mesas.value.every(mesa => mesa.tieneResultados)
})

onMounted(async () => {
  try {
    if (!campeonatoActual.value) {
      error.value = 'No hay campeonato seleccionado'
      return
    }

    await Promise.all([
      cargarMesas(),
      cargarParejas()
    ])
  } catch (e) {
    error.value = 'Error al cargar los datos'
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const cargarMesas = async () => {
  if (!campeonatoActual.value) return
  mesas.value = await mesaStore.fetchMesasConResultados(
    campeonatoActual.value.id,
    partidaActual.value
  )
}

const cargarParejas = async () => {
  parejas.value = await parejaStore.fetchParejas()
}

const obtenerNombrePareja = (parejaId: number | null) => {
  if (!parejaId) return '-'
  const pareja = parejas.value.find(p => p.id === parejaId)
  return pareja ? pareja.nombre : 'Desconocida'
}

const registrarResultado = (mesa: MesaConResultados) => {
  router.push({
    name: 'registro-resultado',
    params: { mesaId: mesa.id },
    query: { 
      partida: partidaActual.value.toString(),
      campeonato: campeonatoActual.value?.id.toString()
    }
  })
}

const finalizarPartida = async () => {
  if (!campeonatoActual.value) return
  
  try {
    await partidaStore.finalizarPartida(campeonatoActual.value.id)
    if (esUltimaPartida.value) {
      router.push({ name: 'podium' })
    } else {
      router.push({ name: 'inicio-partida' })
    }
  } catch (e) {
    error.value = 'Error al finalizar la partida'
    console.error(e)
  }
}
</script> 