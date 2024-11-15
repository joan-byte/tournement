<template>
  <div v-if="show" class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity">
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <form @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <!-- Nombre del campeonato -->
              <div>
                <label for="nombre" class="block text-sm font-medium text-gray-700">
                  Nombre del Campeonato
                </label>
                <input
                  type="text"
                  id="nombre"
                  name="nombre"
                  v-model="formData.nombre"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Fecha de inicio -->
              <div>
                <label for="fecha_inicio" class="block text-sm font-medium text-gray-700">
                  Fecha de Inicio
                </label>
                <input
                  type="date"
                  id="fecha_inicio"
                  name="fecha_inicio"
                  v-model="formData.fecha_inicio"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Días de duración -->
              <div>
                <label for="dias_duracion" class="block text-sm font-medium text-gray-700">
                  Días de Duración
                </label>
                <input
                  type="number"
                  id="dias_duracion"
                  name="dias_duracion"
                  v-model="formData.dias_duracion"
                  required
                  min="1"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Número de partidas -->
              <div>
                <label for="numero_partidas" class="block text-sm font-medium text-gray-700">
                  Número de Partidas
                </label>
                <input
                  type="number"
                  id="numero_partidas"
                  name="numero_partidas"
                  v-model="formData.numero_partidas"
                  required
                  min="1"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Grupo B -->
              <div class="flex items-center">
                <input
                  type="checkbox"
                  id="grupo_b"
                  name="grupo_b"
                  v-model="formData.grupo_b"
                  class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <label for="grupo_b" class="ml-2 block text-sm text-gray-900">
                  Incluir Grupo B
                </label>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
              <button
                type="submit"
                class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 sm:col-start-2"
              >
                Crear
              </button>
              <button
                type="button"
                @click="$emit('close')"
                class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { CampeonatoStore } from '@/types/store'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'created'): void
}>()

const campeonatoStore = useCampeonatoStore() as CampeonatoStore

const formData = ref({
  nombre: '',
  fecha_inicio: '',
  dias_duracion: 1,
  numero_partidas: 1,
  grupo_b: false
})

const handleSubmit = async () => {
  try {
    await campeonatoStore.createCampeonato(formData.value)
    formData.value = {
      nombre: '',
      fecha_inicio: '',
      dias_duracion: 1,
      numero_partidas: 1,
      grupo_b: false
    }
    emit('created')
  } catch (error) {
    console.error('Error al crear campeonato:', error)
  }
}
</script> 