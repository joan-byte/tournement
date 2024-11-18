<template>
  <div class="container mx-auto p-4">
    <!-- Panel superior con botones -->
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
            :disabled="hayResultados"
            :class="[
              hayResultados 
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

    <!-- Lista de parejas -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Listado de Parejas Inscritas
        </h3>
      </div>

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

    <!-- Modales -->
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useParejaStore } from '@/stores/pareja'
import NuevaPareja from '@/components/Parejas/NuevaPareja.vue'
import EditarPareja from '@/components/Parejas/EditarPareja.vue'
import type { Campeonato, Pareja } from '@/types'
import { useMesaStore } from '@/stores/mesa'
import { useResultadoStore } from '@/stores/resultado'

const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const parejaStore = useParejaStore()
const mesaStore = useMesaStore()
const resultadoStore = useResultadoStore()

const parejas = ref<Pareja[]>([])
const showNewParejaModal = ref(false)
const isLoading = ref(true)
const error = ref('')
const parejaEnEdicion = ref<Pareja | null>(null)
const inscripcionEstado = ref(false)

// Computed para obtener el campeonato actual
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

// Computed para verificar si la inscripción está cerrada
const inscripcionCerrada = computed(() => {
  return campeonatoActual.value?.partida_actual > 0
})

// Computed para verificar si hay resultados registrados
const hayResultados = computed(async () => {
  if (!campeonatoActual.value) return false
  try {
    const resultados = await resultadoStore.fetchResultados(campeonatoActual.value.id)
    return resultados && resultados.length > 0
  } catch (error) {
    console.error('Error al verificar resultados:', error)
    return false
  }
})

// Definir loadParejas antes de usarlo en cualquier otro lugar
const loadParejas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const [parejasData, inscripcionData] = await Promise.all([
        parejaStore.fetchParejasCampeonato(campeonatoActual.value.id),
        mesaStore.getMesasAsignadas(campeonatoActual.value.id)
      ])
      
      parejas.value = parejasData
      inscripcionEstado.value = inscripcionData.length > 0
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

const parejasOrdenadas = computed(() => {
  if (!Array.isArray(parejas.value)) return []
  return [...parejas.value]
    .filter(p => p && typeof p.numero === 'number')
    .sort((a, b) => (b.numero as number) - (a.numero as number))
})

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

const onParejaCreated = async () => {
  showNewParejaModal.value = false
  await loadParejas()
}

const onParejaUpdated = async () => {
  parejaEnEdicion.value = null
  await loadParejas()
}

const volverAtras = () => {
  router.push('/campeonatos')
}
</script> 