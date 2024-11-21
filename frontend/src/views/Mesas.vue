<template>
  <!-- Vista principal para mostrar la asignación de mesas en un campeonato -->
  <!-- Muestra una tabla con las parejas y sus mesas asignadas -->
  <div class="container mx-auto p-4">
    <!-- Contenedor principal con espaciado y centrado -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Encabezado de la tarjeta con información del campeonato -->
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

      <!-- Sección principal de la tabla -->
      <div class="border-t border-gray-200">
        <!-- Estados de carga y error -->
        <!-- Spinner de carga -->
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <!-- Mensaje de error si existe -->
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <!-- Mensaje cuando no hay mesas asignadas -->
        <div v-else-if="!parejasOrdenadas.length" class="text-center py-4 text-gray-500">
          No hay mesas asignadas
        </div>
        <!-- Tabla de mesas y parejas -->
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
// Importaciones necesarias de Vue y stores
import { ref, onMounted, computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useMesaStore } from '@/stores/mesa'
import type { Mesa } from '@/types'

// Inicialización de los stores necesarios
const campeonatoStore = useCampeonatoStore()
const mesaStore = useMesaStore()

// Referencias reactivas para el estado de la vista
const isLoading = ref(true)
const error = ref('')
const mesas = ref<Mesa[]>([])

// Computed property para obtener el campeonato actual
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

// Computed property que procesa y ordena las parejas con sus mesas asignadas
// Retorna un array de parejas ordenado por número de pareja
const parejasOrdenadas = computed(() => {
  const parejas: any[] = []
  
  // Procesa cada mesa y extrae la información de ambas parejas
  mesas.value.forEach(mesa => {
    // Añade la pareja 1 si existe
    if (mesa.pareja1) {
      parejas.push({
        id: mesa.pareja1.id,
        numero: mesa.pareja1.numero,
        nombre: mesa.pareja1.nombre,
        club: mesa.pareja1.club,
        mesa: mesa.numero
      })
    }
    // Añade la pareja 2 si existe
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

  // Ordena las parejas por número antes de retornarlas
  return parejas.sort((a, b) => a.numero - b.numero)
})

// Hook del ciclo de vida que se ejecuta al montar el componente
onMounted(async () => {
  if (campeonatoActual.value) {
    await loadMesas()
  }
})

// Función para cargar las mesas asignadas del campeonato actual
// Maneja los estados de carga y errores
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