/**
 * @component Parejas.vue
 * @description Componente principal para la gestión de parejas en un campeonato
 * @responsibilities 
 * - Gestionar la inscripción de parejas
 * - Mostrar listado de parejas inscritas
 * - Controlar el estado de inscripción
 */
<template>
  <!-- Contenedor principal que gestiona la vista de parejas -->
  <div class="container mx-auto p-4">
    <!-- Panel superior con información del campeonato y acciones principales -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
      <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Parejas del Campeonato
          </h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            {{ campeonatoActual?.nombre }}
          </p>
        </div>
        <!-- Grupo de botones contextuales según el estado de inscripción -->
        <div class="flex gap-4">
          <button
            v-if="!inscripcionCerrada"
            @click="cerrarInscripcion"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md"
          >
            Cerrar Inscripción
          </button>
          <button
            v-else
            @click="volverAtras"
            :disabled="hayResultados.value"
            :class="[
              hayResultados.value 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-yellow-600 hover:bg-yellow-700',
              'text-white px-4 py-2 rounded-md'
            ]"
          >
            Volver Atrás
          </button>
          <button
            v-if="!inscripcionCerrada"
            @click="showNewParejaModal = true"
            class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md"
          >
            Nueva Pareja
          </button>
        </div>
      </div>
    </div>

    <!-- Panel principal con listado de parejas -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Listado de Parejas Inscritas
        </h3>
      </div>

      <!-- Contenedor de estados y lista de parejas -->
      <div class="border-t border-gray-200">
        <div v-if="isLoading" class="text-center py-4">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
        </div>
        <div v-else-if="error" class="text-red-500 text-center py-4">
          {{ error }}
        </div>
        <div v-else-if="!campeonatoActual" class="text-center py-4 text-gray-500">
          Seleccione un campeonato para ver las parejas
        </div>
        <div v-else-if="!parejasOrdenadas.length" class="text-center py-4 text-gray-500">
          No hay parejas registradas
        </div>
        <!-- Lista de parejas con sus detalles y acciones -->
        <ul v-else role="list" class="divide-y divide-gray-200">
          <li
            v-for="pareja in parejasOrdenadas"
            :key="pareja.id"
            class="px-4 py-4 sm:px-6 hover:bg-gray-50"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <!-- Número de pareja -->
                <div class="flex-shrink-0">
                  <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-blue-100 text-blue-900 text-xl font-bold">
                    {{ pareja.numero }}
                  </span>
                </div>
                <!-- Nombre y club -->
                <div class="flex-grow">
                  <div class="flex items-center space-x-2">
                    <button 
                      @click="editarPareja(pareja)"
                      :disabled="inscripcionCerrada"
                      class="text-sm font-medium text-primary-600 hover:text-primary-900 hover:underline disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {{ pareja.nombre }}
                    </button>
                    <span class="text-gray-400">|</span>
                    <p class="text-sm text-gray-500">
                      {{ pareja.club || 'Sin club' }}
                    </p>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <span
                  :class="[
                    pareja.activa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800',
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
                  ]"
                >
                  {{ pareja.activa ? 'Activa' : 'Inactiva' }}
                </span>
                <button
                  @click="toggleParejaEstado(pareja)"
                  class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded shadow-sm text-white"
                  :class="pareja.activa ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'"
                >
                  {{ pareja.activa ? 'Desactivar' : 'Activar' }}
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Modales para gestión de parejas -->
    <NuevaPareja
      v-if="showNewParejaModal"
      :show="showNewParejaModal"
      :campeonato-id="campeonatoActual?.id"
      @close="showNewParejaModal = false"
      @created="onParejaCreated"
    />

    <EditarPareja
      v-if="parejaEnEdicion"
      :show="!!parejaEnEdicion"
      :pareja="parejaEnEdicion"
      @close="parejaEnEdicion = null"
      @updated="onParejaUpdated"
    />
  </div>
</template>

<script setup lang="ts">
/**
 * Importaciones necesarias para el funcionamiento del componente
 */
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useParejaStore } from '@/stores/pareja'
import NuevaPareja from '@/components/Parejas/NuevaPareja.vue'
import EditarPareja from '@/components/Parejas/EditarPareja.vue'
import type { Campeonato, Pareja } from '@/types'
import { useMesaStore } from '@/stores/mesa'
import { useResultadoStore } from '@/stores/resultado'
import { usePartidaStore } from '@/stores/partida'

/**
 * Inicialización de stores y router
 */
const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const parejaStore = useParejaStore()
const mesaStore = useMesaStore()
const resultadoStore = useResultadoStore()
const partidaStore = usePartidaStore()

/**
 * Estado reactivo del componente
 */
const parejas = ref<Pareja[]>([])
const showNewParejaModal = ref(false)
const isLoading = ref(true)
const error = ref('')
const parejaEnEdicion = ref<Pareja | null>(null)
const inscripcionEstado = ref(false)
const hayResultados = ref(false)

/**
 * Computed properties para datos derivados
 */
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

const inscripcionCerrada = computed(() => {
  return campeonatoActual.value?.partida_actual > 0
})

/**
 * @function loadParejas
 * @description Carga los datos de parejas y actualiza estados
 */
const loadParejas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const [parejasData, inscripcionData, resultados] = await Promise.all([
        parejaStore.fetchParejasCampeonato(campeonatoActual.value.id),
        mesaStore.getMesasAsignadas(campeonatoActual.value.id),
        resultadoStore.fetchResultados(campeonatoActual.value.id)
      ])
      
      parejas.value = parejasData
      inscripcionEstado.value = inscripcionData.length > 0
      
      // Verificar si hay resultados en la base de datos
      hayResultados.value = resultados && resultados.length > 0 && resultados.some(r => {
        // Considerar que hay resultados solo si hay valores diferentes a 0
        return r.PG !== 0 || r.PP !== 0
      })
    }
  } catch (e) {
    console.error('Error al cargar parejas:', e)
    error.value = 'Error al cargar las parejas'
  } finally {
    isLoading.value = false
  }
}

// Configurar el observador después de definir todas las funciones
onMounted(async () => {
  await campeonatoStore.loadCampeonatoActual()
  if (campeonatoActual.value) {
    await loadParejas()
  }
})

// Observar cambios en campeonatoActual manualmente
let previousCampeonatoId: number | null = null
setInterval(() => {
  const currentId = campeonatoActual.value?.id
  if (currentId !== previousCampeonatoId) {
    previousCampeonatoId = currentId
    if (currentId) {
      loadParejas()
    }
  }
}, 100)

/**
 * @computed parejasOrdenadas
 * @description Ordena las parejas por número
 */
const parejasOrdenadas = computed(() => {
  if (!Array.isArray(parejas.value)) return []
  return [...parejas.value]
    .filter(p => p && typeof p.numero === 'number')
    .sort((a, b) => (b.numero as number) - (a.numero as number))
})

/**
 * Funciones de gestión de parejas
 */
const toggleParejaEstado = async (pareja: Pareja) => {
  try {
    await parejaStore.toggleParejaEstado(pareja.id, !pareja.activa)
    await loadParejas()
  } catch (e) {
    console.error('Error al cambiar estado de la pareja:', e)
  }
}

const editarPareja = (pareja: Pareja) => {
  if (inscripcionCerrada.value) return
  parejaEnEdicion.value = pareja
}

/**
 * Manejadores de eventos para creación y actualización
 */
const onParejaCreated = async () => {
  showNewParejaModal.value = false
  await loadParejas()
}

const onParejaUpdated = async () => {
  parejaEnEdicion.value = null
  await loadParejas()
}

/**
 * @function volverAtras
 * @description Revierte el proceso de cierre de inscripción
 */
const volverAtras = async () => {
  try {
    if (!campeonatoActual.value) return
    
    if (hayResultados.value) {
      alert('No se puede volver atrás porque ya hay resultados registrados')
      return
    }

    // Confirmar la acción
    if (!confirm('¿Está seguro de volver atrás? Se eliminarán las asignaciones de mesas actuales.')) {
      return
    }

    // Eliminar asignaciones de mesas
    await mesaStore.eliminarMesas(campeonatoActual.value.id)
    
    // Actualizar campeonato (partida_actual = -1)
    await campeonatoStore.updateCampeonato(campeonatoActual.value.id, {
      partida_actual: -1
    })

    // Recargar datos
    await loadParejas()

    // Redirigir a la página de parejas
    router.push('/parejas')

    // Refrescar la página después de un breve delay para asegurar que la redirección se complete
    setTimeout(() => {
      window.location.reload()
    }, 100)
  } catch (error) {
    console.error('Error al volver atrás:', error)
    alert('Error al volver atrás. Por favor, inténtelo de nuevo.')
  }
}

/**
 * @function cerrarInscripcion
 * @description Finaliza el período de inscripción e inicia el campeonato
 */
const cerrarInscripcion = async () => {
  try {
    if (!campeonatoActual.value) return

    // Agregar confirmación
    if (!confirm('¿Está seguro de cerrar la inscripción? Esta acción no se puede deshacer.')) {
      return
    }

    // Verificar mínimo de parejas activas
    const parejasActivas = parejas.value.filter(p => p.activa)
    if (parejasActivas.length < 4) {
      alert('Se necesitan al menos 4 parejas activas para iniciar el campeonato')
      return
    }

    // Eliminar cualquier mesa existente primero
    await mesaStore.eliminarMesas(campeonatoActual.value.id)

    // IMPORTANTE: Primero actualizar el campeonato a partida 1
    await campeonatoStore.updateCampeonato(campeonatoActual.value.id, {
      partida_actual: 1
    })

    // Esperar a que el campeonato se actualice
    await campeonatoStore.loadCampeonatoActual()

    // Luego realizar el sorteo inicial de parejas
    await partidaStore.sortearParejas(campeonatoActual.value.id)

    // Cargar las mesas asignadas antes de redirigir
    await mesaStore.getMesasAsignadas(campeonatoActual.value.id)

    // Redirigir a la página de mesas
    router.push('/mesas/asignacion')
  } catch (error) {
    console.error('Error al cerrar inscripción:', error)
    alert('Error al cerrar la inscripción. Por favor, inténtelo de nuevo.')
  }
}
</script> 