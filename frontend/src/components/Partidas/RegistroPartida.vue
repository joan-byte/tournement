<!-- 
  RegistroPartida.vue - Componente para gestionar el registro de resultados de partidas
  Permite visualizar y registrar los resultados de las parejas en cada mesa durante una partida.
  Muestra el estado de registro de cada mesa y permite finalizar la partida cuando todos los resultados están registrados.
-->

<template>
  <!-- Contenedor principal con diseño responsivo -->
  <div class="container mx-auto p-4">
    <!-- Cabecera con título y controles -->
    <div class="flex justify-between items-center mb-4">
      <!-- Título principal -->
      <h1 class="text-2xl font-bold">Registro de Partidas</h1>
      
      <!-- Controles de navegación y estado -->
      <div class="flex items-center">
        <!-- Botón de finalizar partida (visible solo cuando todos los resultados están registrados) -->
        <button 
          v-if="todasParejasRegistradas"
          @click="finalizarPartida"
          class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mr-4"
        >
          {{ esUltimaPartida ? 'Cierre Campeonato' : 'Finalizar Partida' }}
        </button>
        <!-- Indicador de partida actual -->
        <div class="text-xl font-semibold">
          Partida {{ partidaActual }}
        </div>
      </div>
    </div>

    <!-- Estados de carga y error -->
    <div v-if="isLoading">Cargando mesas y parejas...</div>
    <div v-else-if="error">{{ error }}</div>

    <!-- Tabla de mesas y resultados -->
    <table v-else class="min-w-full bg-white border border-gray-300">
      <!-- Encabezados de la tabla -->
      <thead>
        <tr class="bg-gray-100">
          <th class="py-2 px-4 border-b text-center">Mesa</th>
          <th class="py-2 px-4 border-b text-center">Pareja 1</th>
          <th class="py-2 px-4 border-b text-center">Pareja 2</th>
          <th class="py-2 px-4 border-b text-center">Acciones</th>
        </tr>
      </thead>
      <!-- Cuerpo de la tabla con datos de mesas -->
      <tbody>
        <tr v-for="mesa in mesas" :key="mesa.id" class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b text-center">{{ mesa.numero }}</td>
          <td class="py-2 px-4 border-b text-center">
            {{ obtenerNombrePareja(mesa.pareja1_id) }}
          </td>
          <td class="py-2 px-4 border-b text-center">
            {{ obtenerNombrePareja(mesa.pareja2_id) }}
          </td>
          <td class="py-2 px-4 border-b text-center">
            <button
              @click="registrarResultado(mesa)"
              class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-1 px-3 rounded"
              :disabled="mesa.tieneResultados"
            >
              {{ mesa.tieneResultados ? 'Registrado' : 'Registrar' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
// Importaciones necesarias para el componente
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMesaStore } from '@/stores/mesa'
import { useParejaStore } from '@/stores/pareja'
import { usePartidaStore } from '@/stores/partida'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { Mesa, MesaConResultados, Pareja } from '@/types/mesa'

// Inicialización de router y stores
const router = useRouter()
const mesaStore = useMesaStore()
const parejaStore = useParejaStore()
const partidaStore = usePartidaStore()
const campeonatoStore = useCampeonatoStore()

// Estado reactivo del componente
const mesas = ref<MesaConResultados[]>([])    // Lista de mesas con sus resultados
const parejas = ref<Pareja[]>([])             // Lista de parejas participantes
const isLoading = ref(true)                   // Control de estado de carga
const error = ref('')                         // Mensajes de error

/**
 * Computed: Obtiene el campeonato actual
 */
const campeonatoActual = computed(() => campeonatoStore.getCurrentCampeonato())

/**
 * Computed: Obtiene el número de partida actual
 */
const partidaActual = computed(() => campeonatoActual.value?.partida_actual || 0)

/**
 * Computed: Determina si es la última partida del campeonato
 */
const esUltimaPartida = computed(() => {
  if (!campeonatoActual.value) return false
  return partidaActual.value === campeonatoActual.value.numero_partidas
})

/**
 * Computed: Verifica si todas las parejas tienen resultados registrados
 */
const todasParejasRegistradas = computed(() => {
  return mesas.value.every(mesa => mesa.tieneResultados)
})

/**
 * Hook: Se ejecuta al montar el componente
 * Carga los datos iniciales de mesas y parejas
 */
onMounted(async () => {
  try {
    if (!campeonatoActual.value) {
      error.value = 'No hay campeonato seleccionado'
      return
    }

    await Promise.all([
      cargarMesas(),
      cargarParejas()
    ])
  } catch (e) {
    error.value = 'Error al cargar los datos'
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

/**
 * Carga las mesas con sus resultados desde el servidor
 */
const cargarMesas = async () => {
  if (!campeonatoActual.value) return
  mesas.value = await mesaStore.fetchMesasConResultados(
    campeonatoActual.value.id,
    partidaActual.value
  )
}

/**
 * Carga las parejas participantes desde el servidor
 */
const cargarParejas = async () => {
  parejas.value = await parejaStore.fetchParejas()
}

/**
 * Obtiene el nombre de una pareja por su ID
 * @param parejaId - ID de la pareja
 * @returns Nombre de la pareja o '-' si no se encuentra
 */
const obtenerNombrePareja = (parejaId: number | null) => {
  if (!parejaId) return '-'
  const pareja = parejas.value.find(p => p.id === parejaId)
  return pareja ? pareja.nombre : 'Desconocida'
}

/**
 * Navega a la pantalla de registro de resultado para una mesa específica
 * @param mesa - Mesa seleccionada para registrar resultado
 */
const registrarResultado = (mesa: MesaConResultados) => {
  router.push({
    name: 'registro-resultado',
    params: { mesaId: mesa.id },
    query: { 
      partida: partidaActual.value.toString(),
      campeonato: campeonatoActual.value?.id.toString()
    }
  })
}

/**
 * Finaliza la partida actual y redirige según corresponda
 * Si es la última partida, va al podio; si no, a inicio de nueva partida
 */
const finalizarPartida = async () => {
  if (!campeonatoActual.value) return
  
  try {
    await partidaStore.finalizarPartida(campeonatoActual.value.id)
    if (esUltimaPartida.value) {
      router.push({ name: 'podium' })
    } else {
      router.push({ name: 'inicio-partida' })
    }
  } catch (e) {
    error.value = 'Error al finalizar la partida'
    console.error(e)
  }
}
</script> 