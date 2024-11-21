/**
 * Vista principal de Campeonatos
 * Gestiona la visualización, creación y modificación de campeonatos
 */

<template>
  <div class="container mx-auto p-4">
    <!-- Panel superior con título y botón de nuevo campeonato -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Campeonatos
          </h3>
        </div>
        <!-- Botón para crear nuevo campeonato -->
        <button
          @click="showNewCampeonatoModal = true"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Nuevo Campeonato
        </button>
      </div>
    </div>

    <!-- Lista de campeonatos con estados de carga y error -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Estado de carga -->
      <div v-if="isLoading" class="p-4 text-center">
        <p>Cargando campeonatos...</p>
      </div>
      <!-- Estado de error -->
      <div v-else-if="error" class="p-4 text-center text-red-600">
        {{ error }}
      </div>
      <!-- Estado sin campeonatos -->
      <div v-else-if="campeonatos.length === 0" class="p-4 text-center">
        <p>No hay campeonatos registrados</p>
      </div>
      <!-- Lista de campeonatos existentes -->
      <ul v-else role="list" class="divide-y divide-gray-200">
        <li v-for="campeonato in campeonatos" :key="campeonato.id" class="px-4 py-4 sm:px-6">
          <div class="flex items-center justify-between">
            <!-- Información del campeonato -->
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
            <!-- Botones de acción -->
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

    <!-- Modales para gestión de campeonatos -->
    <nuevo-campeonato
      v-if="showNewCampeonatoModal"
      :show="showNewCampeonatoModal"
      @close="showNewCampeonatoModal = false"
      @created="onCampeonatoCreated"
    />

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
/**
 * Configuración y lógica del componente Campeonatos
 */

// Importaciones necesarias
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import NuevoCampeonato from '@/components/Campeonatos/NuevoCampeonato.vue'
import ModificarCampeonato from '@/components/Campeonatos/ModificarCampeonato.vue'
import type { Campeonato } from '@/types'
import type { CampeonatoStore } from '@/types/store'

// Inicialización de router y store
const router = useRouter()
const campeonatoStore = useCampeonatoStore() as CampeonatoStore

// Referencias reactivas
const campeonatos = ref<Campeonato[]>([])
const showNewCampeonatoModal = ref(false)
const isLoading = ref(true)
const error = ref('')
const showModificarModal = ref(false)
const campeonatoSeleccionado = ref<Campeonato | null>(null)

/**
 * Computed property para asegurar que siempre trabajamos con un array
 */
const campeonatosArray = computed(() => {
  return Array.isArray(campeonatos.value) ? campeonatos.value : []
})

// Carga inicial de datos
onMounted(async () => {
  await loadCampeonatos()
})

/**
 * Carga los campeonatos desde el servidor
 */
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

/**
 * Formatea una fecha para mostrarla en español
 * @param dateString - Fecha en formato string
 * @returns Fecha formateada en español
 */
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

/**
 * Selecciona un campeonato y navega a la vista de parejas
 * @param campeonato - Campeonato seleccionado
 */
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

/**
 * Manejadores de eventos para el modal de nuevo campeonato
 */
const onCampeonatoCreated = async () => {
  showNewCampeonatoModal.value = false
  await loadCampeonatos()
}

/**
 * Manejadores de eventos para el modal de modificación
 */
const modificarCampeonato = (campeonato: Campeonato) => {
  console.log('Modificando campeonato:', campeonato)
  campeonatoSeleccionado.value = { ...campeonato }
  showModificarModal.value = true
}

const closeModificarModal = () => {
  console.log('Cerrando modal')
  showModificarModal.value = false
  campeonatoSeleccionado.value = null
}

const onCampeonatoUpdated = async () => {
  console.log('Campeonato actualizado')
  await loadCampeonatos()
  closeModificarModal()
}

const onCampeonatoDeleted = async () => {
  console.log('Campeonato eliminado')
  await loadCampeonatos()
  closeModificarModal()
}
</script> 