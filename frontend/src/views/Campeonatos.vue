<template>
  <div class="container mx-auto p-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Campeonatos
        </h3>
        <button
          @click="showNewCampeonatoModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Nuevo Campeonato
        </button>
      </div>
      <div class="border-t border-gray-200">
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!campeonatosArray.length" class="text-center py-4 text-gray-500">
          No hay campeonatos registrados
        </div>
        <ul v-else role="list" class="divide-y divide-gray-200">
          <li
            v-for="campeonato in campeonatosArray"
            :key="campeonato.id"
            class="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer"
            @click="seleccionarCampeonato(campeonato)"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-primary-600 truncate">
                  {{ campeonato.nombre }}
                </p>
                <div class="mt-2 sm:flex sm:justify-between">
                  <div class="sm:flex">
                    <p class="flex items-center text-sm text-gray-500">
                      <span>Inicio: {{ formatearFecha(campeonato.fecha_inicio) }}</span>
                    </p>
                    <p class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                      <span>Duración: {{ campeonato.dias_duracion }} días</span>
                    </p>
                  </div>
                </div>
              </div>
              <div class="flex flex-col items-end">
                <span
                  :class="[
                    campeonato.partida_actual > 0 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800',
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
                  ]"
                >
                  {{ campeonato.partida_actual > 0 ? 'En curso' : 'No iniciado' }}
                </span>
                <p class="mt-2 text-sm text-gray-500">
                  Partida: {{ campeonato.partida_actual }}/{{ campeonato.numero_partidas }}
                </p>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Modal de nuevo campeonato -->
    <NuevoCampeonato
      :show="showNewCampeonatoModal"
      @close="showNewCampeonatoModal = false"
      @created="onCampeonatoCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import NuevoCampeonato from '@/components/Campeonatos/NuevoCampeonato.vue'
import type { Campeonato } from '@/types'

const router = useRouter()
const campeonatoStore = useCampeonatoStore()

const campeonatos = ref<Campeonato[]>([])
const showNewCampeonatoModal = ref(false)
const isLoading = ref(true)
const error = ref('')

// Computed property para asegurar que siempre trabajamos con un array
const campeonatosArray = computed(() => {
  return Array.isArray(campeonatos.value) ? campeonatos.value : []
})

onMounted(async () => {
  await loadCampeonatos()
})

const loadCampeonatos = async () => {
  try {
    isLoading.value = true
    const response = await campeonatoStore.fetchCampeonatos()
    campeonatos.value = Array.isArray(response) ? response : []
  } catch (e) {
    console.error('Error al cargar campeonatos:', e)
    error.value = 'Error al cargar los campeonatos'
    campeonatos.value = []
  } finally {
    isLoading.value = false
  }
}

const formatearFecha = (dateString: string) => {
  if (!dateString) return ''
  const fecha = new Date(dateString)
  if (isNaN(fecha.getTime())) return ''
  return fecha.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const seleccionarCampeonato = async (campeonato: Campeonato) => {
  try {
    campeonatoStore.setCampeonatoActual(campeonato)
    router.push('/parejas')
  } catch (error) {
    console.error('Error al seleccionar campeonato:', error)
  }
}

const onCampeonatoCreated = async () => {
  showNewCampeonatoModal.value = false
  await loadCampeonatos()
}
</script> 