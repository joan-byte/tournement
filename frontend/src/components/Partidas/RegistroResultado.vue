<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Registro de Resultado - Mesa {{ mesa?.numero }}
        </h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          {{ campeonatoActual?.nombre }} - Partida {{ campeonatoActual?.partida_actual }}
        </p>
      </div>

      <div class="border-t border-gray-200 px-4 py-5">
        <form @submit.prevent="handleSubmit">
          <!-- Pareja 1 -->
          <div class="mb-6">
            <div class="flex items-center space-x-4 mb-2">
              <span class="text-sm font-medium text-gray-900">{{ mesa?.pareja1?.numero }}</span>
              <span class="text-sm text-gray-500">{{ mesa?.pareja1?.nombre }}</span>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="pareja1_pg" class="block text-sm font-medium text-gray-700">Puntos Ganados</label>
                <input
                  type="number"
                  id="pareja1_pg"
                  name="pareja1_pg"
                  v-model="formData.pareja1.PG"
                  required
                  min="0"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <label for="pareja1_pp" class="block text-sm font-medium text-gray-700">Puntos Perdidos</label>
                <input
                  type="number"
                  id="pareja1_pp"
                  name="pareja1_pp"
                  v-model="formData.pareja1.PP"
                  required
                  min="0"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
            </div>
          </div>

          <!-- Pareja 2 -->
          <div v-if="mesa?.pareja2" class="mb-6">
            <div class="flex items-center space-x-4 mb-2">
              <span class="text-sm font-medium text-gray-900">{{ mesa.pareja2.numero }}</span>
              <span class="text-sm text-gray-500">{{ mesa.pareja2.nombre }}</span>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="pareja2_pg" class="block text-sm font-medium text-gray-700">Puntos Ganados</label>
                <input
                  type="number"
                  id="pareja2_pg"
                  name="pareja2_pg"
                  v-model="formData.pareja2.PG"
                  required
                  min="0"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <label for="pareja2_pp" class="block text-sm font-medium text-gray-700">Puntos Perdidos</label>
                <input
                  type="number"
                  id="pareja2_pp"
                  name="pareja2_pp"
                  v-model="formData.pareja2.PP"
                  required
                  min="0"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
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
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Guardar
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

const formData = ref({
  pareja1: {
    PG: 0,
    PP: 0
  },
  pareja2: {
    PG: 0,
    PP: 0
  }
})

const loadMesa = async () => {
  try {
    const mesaId = parseInt(route.params.mesaId as string)
    if (campeonatoActual.value) {
      const response = await mesaStore.getMesa(mesaId)
      mesa.value = response

      // Si hay resultados previos, cargarlos
      const resultados = await resultadoStore.getResultadoMesa(
        mesaId,
        campeonatoActual.value.partida_actual || 1
      )
      if (resultados) {
        formData.value = {
          pareja1: {
            PG: resultados.pareja1.PG,
            PP: resultados.pareja1.PP
          },
          pareja2: resultados.pareja2 ? {
            PG: resultados.pareja2.PG,
            PP: resultados.pareja2.PP
          } : { PG: 0, PP: 0 }
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

    const resultado = {
      mesa_id: mesa.value.id,
      campeonato_id: campeonatoActual.value.id,
      partida: campeonatoActual.value.partida_actual,
      resultados: {
        pareja1: {
          id_pareja: mesa.value.pareja1.id,
          PG: formData.value.pareja1.PG,
          PP: formData.value.pareja1.PP
        },
        pareja2: mesa.value.pareja2 ? {
          id_pareja: mesa.value.pareja2.id,
          PG: formData.value.pareja2.PG,
          PP: formData.value.pareja2.PP
        } : null
      }
    }

    await resultadoStore.saveResultado(resultado)
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