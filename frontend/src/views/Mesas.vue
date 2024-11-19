<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Asignación de Mesas
          </h3>
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual || 1 }}
          </span>
        </div>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <div class="border-t border-gray-200">
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!parejasOrdenadas.length" class="text-center py-4 text-gray-500">
          No hay mesas asignadas
        </div>
        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Número
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Club
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mesa
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="pareja in parejasOrdenadas" :key="pareja.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ pareja.numero }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ pareja.nombre }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ pareja.club || 'Sin club' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">
                  {{ pareja.mesa }}
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
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import type { Mesa } from '@/types'

const campeonatoStore = useCampeonatoStore()
const mesaStore = useMesaStore()

const isLoading = ref(true)
const error = ref('')
const mesas = ref<Mesa[]>([])
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

// Computed para obtener las parejas ordenadas con su mesa asignada
const parejasOrdenadas = computed(() => {
  const parejas: any[] = []
  
  mesas.value.forEach(mesa => {
    if (mesa.pareja1) {
      parejas.push({
        id: mesa.pareja1.id,
        numero: mesa.pareja1.numero,
        nombre: mesa.pareja1.nombre,
        club: mesa.pareja1.club,
        mesa: mesa.numero
      })
    }
    if (mesa.pareja2) {
      parejas.push({
        id: mesa.pareja2.id,
        numero: mesa.pareja2.numero,
        nombre: mesa.pareja2.nombre,
        club: mesa.pareja2.club,
        mesa: mesa.numero
      })
    }
  })

  return parejas.sort((a, b) => a.numero - b.numero)
})

onMounted(async () => {
  if (campeonatoActual.value) {
    await loadMesas()
  }
})

const loadMesas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const mesasResponse = await mesaStore.getMesasAsignadas(campeonatoActual.value.id)
      mesas.value = mesasResponse || []
    }
  } catch (e) {
    console.error('Error al cargar mesas:', e)
    error.value = 'Error al cargar las mesas'
  } finally {
    isLoading.value = false
  }
}
</script> 