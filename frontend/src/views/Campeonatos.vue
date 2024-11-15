<template>
  <div class="container mx-auto p-4">
    <!-- Panel superior con botones -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Campeonatos
          </h3>
        </div>
        <button
          @click="showNewCampeonatoModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Nuevo Campeonato
        </button>
      </div>
    </div>

    <!-- Lista de campeonatos -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div v-if="isLoading" class="p-4 text-center">
        <p>Cargando campeonatos...</p>
      </div>
      <div v-else-if="error" class="p-4 text-center text-red-600">
        {{ error }}
      </div>
      <div v-else-if="campeonatos.length === 0" class="p-4 text-center">
        <p>No hay campeonatos registrados</p>
      </div>
      <ul v-else role="list" class="divide-y divide-gray-200">
        <li v-for="campeonato in campeonatos" :key="campeonato.id" class="px-4 py-4 sm:px-6">
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <p 
                class="text-sm font-medium text-primary-600 hover:text-primary-700 cursor-pointer"
                @click="seleccionarCampeonato(campeonato)"
              >
                {{ campeonato.nombre }}
              </p>
              <p class="text-sm text-gray-500">
                Fecha inicio: {{ formatearFecha(campeonato.fecha_inicio) }}
              </p>
              <p class="text-sm text-gray-500">
                {{ 
                  campeonato.partida_actual === 0 
                    ? 'No iniciado' 
                    : `Partida ${campeonato.partida_actual} de ${campeonato.numero_partidas}` 
                }}
              </p>
            </div>
            <div class="flex gap-2">
              <button
                @click.stop="modificarCampeonato(campeonato)"
                class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Modificar
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Modal de nuevo campeonato -->
    <nuevo-campeonato
      v-if="showNewCampeonatoModal"
      :show="showNewCampeonatoModal"
      @close="showNewCampeonatoModal = false"
      @created="onCampeonatoCreated"
    />

    <!-- Modal de modificación -->
    <ModificarCampeonato
      v-if="showModificarModal"
      :campeonato="campeonatoSeleccionado!"
      @close="closeModificarModal"
      @updated="onCampeonatoUpdated"
      @deleted="onCampeonatoDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import NuevoCampeonato from '@/components/Campeonatos/NuevoCampeonato.vue'
import ModificarCampeonato from '@/components/Campeonatos/ModificarCampeonato.vue'
import type { Campeonato } from '@/types'
import type { CampeonatoStore } from '@/types/store'

const router = useRouter()
const campeonatoStore = useCampeonatoStore() as CampeonatoStore

const campeonatos = ref<Campeonato[]>([])
const showNewCampeonatoModal = ref(false)
const isLoading = ref(true)
const error = ref('')
const showModificarModal = ref(false)
const campeonatoSeleccionado = ref<Campeonato | null>(null)

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
    const campeonatoCompleto = {
      id: campeonato.id,
      nombre: campeonato.nombre,
      fecha_inicio: campeonato.fecha_inicio,
      dias_duracion: campeonato.dias_duracion,
      numero_partidas: campeonato.numero_partidas,
      partida_actual: campeonato.partida_actual,
      grupo_b: campeonato.grupo_b
    } as Campeonato;

    await campeonatoStore.setCampeonatoActual(null)
    await campeonatoStore.setCampeonatoActual(campeonatoCompleto)
    
    const currentCampeonato = campeonatoStore.getCurrentCampeonato()
    if (currentCampeonato?.id !== campeonato.id) {
      throw new Error('Error al actualizar el campeonato actual')
    }
    
    router.push('/parejas')
  } catch (error) {
    console.error('Error al seleccionar campeonato:', error)
  }
}

const onCampeonatoCreated = async () => {
  showNewCampeonatoModal.value = false
  await loadCampeonatos()
}

const modificarCampeonato = (campeonato: Campeonato) => {
  console.log('Modificando campeonato:', campeonato) // Para debug
  campeonatoSeleccionado.value = { ...campeonato } // Crear una copia del objeto
  showModificarModal.value = true
}

const closeModificarModal = () => {
  console.log('Cerrando modal') // Para debug
  showModificarModal.value = false
  campeonatoSeleccionado.value = null
}

const onCampeonatoUpdated = async () => {
  console.log('Campeonato actualizado') // Para debug
  await loadCampeonatos()
  closeModificarModal()
}

const onCampeonatoDeleted = async () => {
  console.log('Campeonato eliminado') // Para debug
  await loadCampeonatos()
  closeModificarModal()
}
</script> 