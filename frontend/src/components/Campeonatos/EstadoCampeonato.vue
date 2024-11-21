<!-- 
  Componente que muestra el estado actual de un campeonato.
  Presenta información detallada como nombre, fecha de inicio,
  progreso de partidas y estado actual.
-->
<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <!-- Encabezado del componente -->
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Estado del Campeonato
      </h3>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">
        Información detallada del campeonato actual
      </p>
    </div>

    <!-- Lista de detalles del campeonato -->
    <div class="border-t border-gray-200">
      <dl>
        <!-- Nombre del campeonato -->
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Nombre</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ campeonato?.nombre }}
          </dd>
        </div>

        <!-- Fecha de inicio -->
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Fecha de inicio</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ formatDate(campeonato?.fecha_inicio) }}
          </dd>
        </div>

        <!-- Progreso de partidas -->
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Partida actual</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ campeonato?.partida_actual }} / {{ campeonato?.numero_partidas }}
          </dd>
        </div>

        <!-- Estado del campeonato con indicador visual -->
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Estado</dt>
          <dd class="mt-1 text-sm sm:mt-0 sm:col-span-2">
            <!-- Badge que cambia de color según el estado -->
            <span
              :class="[
                campeonato?.partida_actual === campeonato?.numero_partidas
                  ? 'bg-green-100 text-green-800'  // Verde para campeonato finalizado
                  : campeonato?.partida_actual > 0
                  ? 'bg-yellow-100 text-yellow-800'  // Amarillo para campeonato en curso
                  : 'bg-gray-100 text-gray-800',     // Gris para campeonato no iniciado
                'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium'
              ]"
            >
              {{ getEstado }}
            </span>
          </dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup lang="ts">
// Importaciones necesarias
import { computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'

// Inicialización del store de campeonatos
const campeonatoStore = useCampeonatoStore()

// Computed property para obtener el campeonato actual
const campeonato = computed(() => campeonatoStore.getCurrentCampeonato())

/**
 * Formatea una fecha para mostrarla en formato local.
 * 
 * @param dateString - Fecha en formato string
 * @returns Fecha formateada o "No definida" si no hay fecha
 */
const formatDate = (dateString?: string) => {
  if (!dateString) return 'No definida'
  return new Date(dateString).toLocaleDateString()
}

/**
 * Computed property que determina el estado del campeonato.
 * 
 * @returns Estado actual del campeonato:
 *          - "No seleccionado" si no hay campeonato
 *          - "No iniciado" si partida_actual es 0
 *          - "Finalizado" si se completaron todas las partidas
 *          - "En curso" en cualquier otro caso
 */
const getEstado = computed(() => {
  if (!campeonato.value) return 'No seleccionado'
  if (campeonato.value.partida_actual === 0) return 'No iniciado'
  if (campeonato.value.partida_actual === campeonato.value.numero_partidas) return 'Finalizado'
  return 'En curso'
})
</script> 