<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <div class="flex justify-between items-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Registro de Resultados
          </h3>
          <span class="text-lg font-medium text-gray-900">
            Partida {{ campeonatoActual?.partida_actual || 1 }}
          </span>
        </div>
        <div v-if="todasMesasRegistradas" class="mt-4">
          <button
            @click="cerrarPartida"
            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Cerrar Partida
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

interface Pareja {
  id: number
  numero: number
  nombre: string
}

interface Mesa {
  id: number
  numero: number
  pareja1: Pareja | null
  pareja2: Pareja | null
  tieneResultado: boolean
}

const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const mesaStore = useMesaStore()

const isLoading = ref(true)
const error = ref('')
const mesas = ref<Mesa[]>([])

const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

const mesasOrdenadas = computed(() => {
  return [...mesas.value].sort((a, b) => a.numero - b.numero)
})

const loadMesas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const response = await mesaStore.getMesasAsignadas(campeonatoActual.value.id)
      // Transformar la respuesta al formato que necesitamos
      mesas.value = response.map((mesa: any) => ({
        id: mesa.id,
        numero: mesa.numero,
        pareja1: mesa.pareja1 ? {
          id: mesa.pareja1.id,
          numero: mesa.pareja1.numero,
          nombre: mesa.pareja1.nombre
        } : null,
        pareja2: mesa.pareja2 ? {
          id: mesa.pareja2.id,
          numero: mesa.pareja2.numero,
          nombre: mesa.pareja2.nombre
        } : null,
        tieneResultado: mesa.tieneResultado || false
      }))
    }
  } catch (e) {
    console.error('Error al cargar mesas:', e)
    error.value = 'Error al cargar las mesas'
  } finally {
    isLoading.value = false
  }
}

const registrarResultado = (mesa: Mesa) => {
  router.push(`/partidas/resultado/${mesa.id}`)
}

const todasMesasRegistradas = computed(() => {
  return mesas.value.length > 0 && mesas.value.every(mesa => mesa.tieneResultado)
})

const cerrarPartida = async () => {
  try {
    if (!campeonatoActual.value) return

    await mesaStore.cerrarPartida(campeonatoActual.value.id)
    const nuevoCampeonato = await campeonatoStore.loadCampeonatoActual()
    if (nuevoCampeonato !== null) {
      campeonatoActual.value = nuevoCampeonato
      await loadMesas()
    }
  } catch (error) {
    console.error('Error al cerrar partida:', error)
  }
}

onMounted(async () => {
  await loadMesas()
})
</script> 