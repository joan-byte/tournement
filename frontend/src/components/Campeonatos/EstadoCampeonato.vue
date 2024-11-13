<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Estado del Campeonato
      </h3>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">
        Información detallada del campeonato actual
      </p>
    </div>
    <div class="border-t border-gray-200">
      <dl>
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Nombre</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ campeonato?.nombre }}
          </dd>
        </div>
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Fecha de inicio</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ formatDate(campeonato?.fecha_inicio) }}
          </dd>
        </div>
        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Partida actual</dt>
          <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
            {{ campeonato?.partida_actual }} / {{ campeonato?.numero_partidas }}
          </dd>
        </div>
        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm font-medium text-gray-500">Estado</dt>
          <dd class="mt-1 text-sm sm:mt-0 sm:col-span-2">
            <span
              :class="[
                campeonato?.partida_actual === campeonato?.numero_partidas
                  ? 'bg-green-100 text-green-800'
                  : campeonato?.partida_actual > 0
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-gray-100 text-gray-800',
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
import { computed } from 'vue'
import { useCampeonatoStore } from '@/stores/campeonato'

const campeonatoStore = useCampeonatoStore()
const campeonato = computed(() => campeonatoStore.getCurrentCampeonato())

const formatDate = (dateString?: string) => {
  if (!dateString) return 'No definida'
  return new Date(dateString).toLocaleDateString()
}

const getEstado = computed(() => {
  if (!campeonato.value) return 'No seleccionado'
  if (campeonato.value.partida_actual === 0) return 'No iniciado'
  if (campeonato.value.partida_actual === campeonato.value.numero_partidas) return 'Finalizado'
  return 'En curso'
})
</script> 