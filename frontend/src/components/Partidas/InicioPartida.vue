<!-- 
  InicioPartida.vue - Componente para la gestión del inicio de partidas en un campeonato
  Funcionalidades principales:
  - Muestra la lista de parejas inscritas en el campeonato actual
  - Permite iniciar una nueva partida o el campeonato completo
  - Gestiona el sorteo inicial de mesas y permite reiniciarlo
  - Controla el flujo entre partidas del campeonato
-->

<template>
  <div class="container mx-auto p-4">
    <!-- Panel principal que contiene toda la información de inicio de partida -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Cabecera con título y nombre del campeonato -->
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Inicio de Partida
        </h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">
          {{ campeonatoActual?.nombre }}
        </p>
      </div>

      <!-- Sección que muestra la lista de parejas inscritas -->
      <div class="border-t border-gray-200">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Listado de Parejas Inscritas
          </h3>
        </div>

        <!-- Contenedor de la lista con estados de carga y mensajes informativos -->
        <div class="border-t border-gray-200">
          <!-- Indicador de carga -->
          <div v-if="isLoading" class="text-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto"></div>
          </div>
          <!-- Mensaje de error si algo falla -->
          <div v-else-if="error" class="text-red-500 text-center py-4">
            {{ error }}
          </div>
          <!-- Mensaje cuando no hay campeonato seleccionado -->
          <div v-else-if="!campeonatoActual" class="text-center py-4 text-gray-500">
            Seleccione un campeonato para ver las parejas
          </div>
          <!-- Mensaje cuando no hay parejas registradas -->
          <div v-else-if="parejas.length === 0" class="text-center py-4 text-gray-500">
            No hay parejas registradas
          </div>
          <!-- Lista de parejas con su información -->
          <ul v-else role="list" class="divide-y divide-gray-200">
            <!-- Cada elemento de la lista representa una pareja -->
            <li
              v-for="pareja in parejasOrdenadas"
              :key="pareja.id"
              class="px-4 py-4 sm:px-6 hover:bg-gray-50"
            >
              <!-- Diseño de la información de cada pareja -->
              <div class="flex items-center justify-between">
                <!-- Lado izquierdo: número, nombre y club -->
                <div class="flex items-center space-x-4">
                  <!-- Número de la pareja en círculo -->
                  <div class="flex-shrink-0">
                    <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-blue-100 text-blue-900 text-xl font-bold">
                      {{ pareja.numero }}
                    </span>
                  </div>
                  <!-- Información textual de la pareja -->
                  <div class="flex-grow">
                    <div class="flex items-center space-x-2">
                      <p class="text-sm font-medium text-gray-900">
                        {{ pareja.nombre }}
                      </p>
                      <span class="text-gray-400">|</span>
                      <p class="text-sm text-gray-500">
                        {{ pareja.club || 'Sin club' }}
                      </p>
                    </div>
                  </div>
                </div>
                <!-- Lado derecho: estado de la pareja -->
                <div class="flex items-center space-x-4">
                  <span
                    :class="[
                      pareja.activa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800',
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
                    ]"
                  >
                    {{ pareja.activa ? 'Activa' : 'Inactiva' }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Panel de botones de control -->
      <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
        <!-- Botón de reinicio (visible solo cuando hay mesas asignadas) -->
        <button
          v-if="mesasAsignadas"
          type="button"
          @click="reiniciarSorteo"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Reiniciar Sorteo
        </button>
        <!-- Botón de inicio (visible cuando no hay mesas asignadas) -->
        <button
          v-else
          type="button"
          @click="iniciarPartida"
          :disabled="!puedeIniciar"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ esPrimeraPartida ? 'Iniciar Campeonato' : 'Iniciar Partida' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Importaciones necesarias para el funcionamiento del componente
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCampeonatoStore } from '@/stores/campeonato'
import { useParejaStore } from '@/stores/pareja'
import { useMesaStore } from '@/stores/mesa'
import type { Campeonato, Pareja } from '@/types'

// Inicialización de router y stores necesarios
const router = useRouter()
const campeonatoStore = useCampeonatoStore()
const parejaStore = useParejaStore()
const mesaStore = useMesaStore()

// Estado reactivo del componente
const campeonatoActual = ref<Campeonato | null>(null)  // Almacena el campeonato actual
const parejas = ref<Pareja[]>([])                      // Lista de parejas participantes
const isLoading = ref(true)                            // Control de estado de carga
const error = ref('')                                  // Mensajes de error
const mesasAsignadas = ref(false)                      // Control de asignación de mesas

/**
 * Computed: Ordena las parejas por número de mayor a menor
 * Filtra parejas válidas y las ordena numéricamente
 */
const parejasOrdenadas = computed(() => {
  if (!Array.isArray(parejas.value)) return []
  return [...parejas.value]
    .filter(p => p && typeof p.numero === 'number')
    .sort((a, b) => (b.numero as number) - (a.numero as number))
})

/**
 * Computed: Determina si se puede iniciar una partida
 * Requiere al menos 4 parejas activas
 */
const puedeIniciar = computed(() => {
  const parejasActivas = parejas.value.filter((p: Pareja) => p.activa)
  return parejasActivas.length >= 4
})

/**
 * Computed: Verifica si es la primera partida del campeonato
 */
const esPrimeraPartida = computed(() => {
  return campeonatoActual.value?.partida_actual === 0
})

/**
 * Hook: Se ejecuta al montar el componente
 * Carga el campeonato actual y sus parejas
 */
onMounted(async () => {
  campeonatoActual.value = campeonatoStore.getCurrentCampeonato()
  if (campeonatoActual.value) {
    await loadParejas()
  } else {
    router.push('/campeonatos')
  }
})

/**
 * Carga las parejas del campeonato actual desde el servidor
 * Maneja estados de carga y posibles errores
 */
const loadParejas = async () => {
  try {
    isLoading.value = true
    if (campeonatoActual.value) {
      const response = await parejaStore.fetchParejasCampeonato(campeonatoActual.value.id)
      parejas.value = Array.isArray(response) ? response : []
    }
  } catch (e) {
    console.error('Error al cargar parejas:', e)
    error.value = 'Error al cargar las parejas'
    parejas.value = []
  } finally {
    isLoading.value = false
  }
}

/**
 * Inicia una nueva partida o el campeonato
 * Si es la primera partida, realiza el sorteo de mesas
 * Si no, incrementa el contador de partidas y redirige
 */
const iniciarPartida = async () => {
  try {
    if (!campeonatoActual.value) return
    
    const partidaActual = campeonatoActual.value.partida_actual

    // Asignar mesas según corresponda
    await mesaStore.asignarMesas(
      campeonatoActual.value.id,
      partidaActual
    )

    if (esPrimeraPartida.value) {
      // Si es la primera partida, ya se hizo el sorteo
      mesasAsignadas.value = true
    } else {
      // Para las siguientes partidas, incrementar el contador
      await campeonatoStore.updateCampeonato(campeonatoActual.value.id, {
        partida_actual: partidaActual + 1
      })
      router.push('/partidas/registro')
    }
  } catch (e) {
    console.error('Error al iniciar partida:', e)
    error.value = 'Error al iniciar la partida'
  }
}

/**
 * Reinicia el sorteo de mesas
 * Elimina las asignaciones actuales y recarga las parejas
 */
const reiniciarSorteo = async () => {
  try {
    if (!campeonatoActual.value) return
    
    await mesaStore.eliminarMesas(campeonatoActual.value.id)
    mesasAsignadas.value = false
    
    await loadParejas()
  } catch (e) {
    console.error('Error al reiniciar sorteo:', e)
    error.value = 'Error al reiniciar el sorteo'
  }
}
</script> 