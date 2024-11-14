<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Asignación de Mesas
        </h3>
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
        <div v-else-if="!parejasMesas.length" class="text-center py-4 text-gray-500">
          No hay mesas asignadas
        </div>
        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Número Pareja
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nombre
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Club
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mesa
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="pareja in parejasVisibles" :key="pareja.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ pareja.numero }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ pareja.nombre }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ pareja.club || 'Sin club' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ pareja.mesa_numero }}
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
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import type { Pareja } from '@/types'

const campeonatoStore = useCampeonatoStore()
const mesaStore = useMesaStore()

const isLoading = ref(true)
const error = ref('')
const parejasMesas = ref<any[]>([])
const currentIndex = ref(0)
const intervalId = ref<number | null>(null)

const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

const parejasVisibles = computed(() => {
  const start = currentIndex.value
  const end = start + 20
  return parejasMesas.value.slice(start, end)
})

const loadMesas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const response = await mesaStore.getMesasAsignadas(campeonatoActual.value.id)
      parejasMesas.value = response.sort((a, b) => a.numero - b.numero)
    }
  } catch (e) {
    console.error('Error al cargar mesas:', e)
    error.value = 'Error al cargar las mesas asignadas'
  } finally {
    isLoading.value = false
  }
}

const startRotation = () => {
  intervalId.value = window.setInterval(() => {
    currentIndex.value = (currentIndex.value + 20) % parejasMesas.value.length
    if (currentIndex.value === 0) {
      // Si volvemos al inicio, esperamos un ciclo adicional
      setTimeout(() => {
        currentIndex.value = 20
      }, 10000)
    }
  }, 10000)
}

onMounted(async () => {
  await loadMesas()
  if (parejasMesas.value.length > 20) {
    startRotation()
  }
})

onUnmounted(() => {
  if (intervalId.value) {
    clearInterval(intervalId.value)
  }
})
</script> 