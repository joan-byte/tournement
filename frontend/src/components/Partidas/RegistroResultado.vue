<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 class="text-2xl font-bold mb-6">Registro de Resultado - Mesa {{ mesa?.numero }}</h2>
      
      <div v-if="isLoading" class="text-center">
        Cargando datos...
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <form v-else @submit.prevent="guardarResultado" class="space-y-6">
        <!-- Pareja 1 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-4">
            <h3 class="text-lg font-semibold">{{ obtenerNombrePareja(mesa?.pareja1_id) }}</h3>
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">
                Resultado Parcial
              </label>
              <input
                v-model.number="resultado1.RP"
                type="number"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              >
            </div>
          </div>

          <!-- Pareja 2 -->
          <div v-if="mesa?.pareja2_id" class="space-y-4">
            <h3 class="text-lg font-semibold">{{ obtenerNombrePareja(mesa.pareja2_id) }}</h3>
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">
                Resultado Parcial
              </label>
              <input
                v-model.number="resultado2.RP"
                type="number"
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              >
            </div>
          </div>
        </div>

        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="$router.back()"
            class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Guardar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMesaStore } from '@/stores/mesa'
import { useParejaStore } from '@/stores/pareja'
import { useResultadoStore } from '@/stores/resultado'
import type { Mesa, ResultadoBase } from '@/types'

const route = useRoute()
const router = useRouter()
const mesaStore = useMesaStore()
const parejaStore = useParejaStore()
const resultadoStore = useResultadoStore()

const mesa = ref<Mesa | null>(null)
const isLoading = ref(true)
const error = ref('')

const resultado1 = ref<ResultadoBase>({
  campeonato_id: Number(route.query.campeonato),
  P: Number(route.query.partida),
  M: Number(route.params.mesaId),
  id_pareja: 0,
  RP: 0,
  PG: 0,
  PP: 0,
  GB: 'A'
})

const resultado2 = ref<ResultadoBase>({
  campeonato_id: Number(route.query.campeonato),
  P: Number(route.query.partida),
  M: Number(route.params.mesaId),
  id_pareja: 0,
  RP: 0,
  PG: 0,
  PP: 0,
  GB: 'A'
})

onMounted(async () => {
  try {
    await cargarDatos()
  } catch (e) {
    error.value = 'Error al cargar los datos'
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const cargarDatos = async () => {
  const mesas = await mesaStore.fetchMesas(Number(route.query.campeonato))
  mesa.value = mesas.find(m => m.id === Number(route.params.mesaId)) || null
  
  if (mesa.value) {
    resultado1.value.id_pareja = mesa.value.pareja1_id
    if (mesa.value.pareja2_id) {
      resultado2.value.id_pareja = mesa.value.pareja2_id
    }
  }
}

const obtenerNombrePareja = (parejaId: number | null) => {
  if (!parejaId) return '-'
  const pareja = parejaStore.parejas.find(p => p.id === parejaId)
  return pareja ? pareja.nombre : 'Desconocida'
}

const guardarResultado = async () => {
  if (!resultadoStore.validarResultados(resultado1.value, resultado2.value)) {
    error.value = 'Los resultados no son válidos'
    return
  }

  try {
    const resultadosCalculados = resultadoStore.calcularResultados(
      resultado1.value,
      mesa.value?.pareja2_id ? resultado2.value : null
    )

    await resultadoStore.guardarResultados({
      campeonato_id: Number(route.query.campeonato),
      pareja1: resultadosCalculados.pareja1,
      pareja2: resultadosCalculados.pareja2
    })

    router.back()
  } catch (e) {
    error.value = 'Error al guardar los resultados'
    console.error(e)
  }
}
</script> 