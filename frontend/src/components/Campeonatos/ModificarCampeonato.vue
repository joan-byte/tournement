<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity">
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <div class="absolute right-0 top-0 hidden pr-4 pt-4 sm:block">
            <button
              type="button"
              @click="$emit('close')"
              class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
            >
              <span class="sr-only">Cerrar</span>
              <XMarkIcon class="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg font-medium leading-6 text-gray-900">
                Modificar Campeonato
              </h3>
              <div class="mt-4">
                <form @submit.prevent="handleSubmit">
                  <div class="space-y-4">
                    <div>
                      <label for="nombre" class="block text-sm font-medium text-gray-700">
                        Nombre
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
                    <div>
                      <label for="fecha_inicio" class="block text-sm font-medium text-gray-700">
                        Fecha de inicio
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
                    <div>
                      <label for="dias_duracion" class="block text-sm font-medium text-gray-700">
                        Días de duración
                      </label>
                      <input
                        type="number"
                        id="dias_duracion"
                        name="dias_duracion"
                        v-model="formData.dias_duracion"
                        min="1"
                        required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label for="numero_partidas" class="block text-sm font-medium text-gray-700">
                        Número de partidas
                      </label>
                      <input
                        type="number"
                        id="numero_partidas"
                        name="numero_partidas"
                        v-model="formData.numero_partidas"
                        min="1"
                        required
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label for="grupo_b" class="inline-flex items-center">
                        <input
                          type="checkbox"
                          id="grupo_b"
                          name="grupo_b"
                          v-model="formData.grupo_b"
                          class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <span class="ml-2 block text-sm font-medium text-gray-700">
                          Grupo B
                        </span>
                      </label>
                    </div>
                  </div>
                  <div class="mt-5 sm:mt-4 flex justify-between">
                    <button
                      type="button"
                      @click="confirmarEliminar"
                      class="inline-flex justify-center rounded-md border border-transparent bg-red-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:text-sm"
                    >
                      Eliminar
                    </button>
                    <div class="flex gap-2">
                      <button
                        type="button"
                        @click="$emit('close')"
                        class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:text-sm"
                      >
                        Cancelar
                      </button>
                      <button
                        type="submit"
                        class="inline-flex justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:text-sm"
                      >
                        Guardar
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <div v-if="showConfirmDelete" class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity z-20">
      <div class="fixed inset-0 z-30 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <ExclamationTriangleIcon class="h-6 w-6 text-red-600" aria-hidden="true" />
              </div>
              <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                <h3 class="text-base font-semibold leading-6 text-gray-900">
                  Eliminar Campeonato
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    ¿Estás seguro que deseas eliminar este campeonato? Esta acción eliminará todos los datos relacionados (parejas, jugadores, mesas, resultados) y no se puede deshacer.
                  </p>
                </div>
              </div>
            </div>
            <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
              <button
                type="button"
                @click="eliminarCampeonato"
                class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
              >
                Eliminar
              </button>
              <button
                type="button"
                @click="showConfirmDelete = false"
                class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { XMarkIcon, ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import { useCampeonatoStore } from '@/stores/campeonato'
import type { Campeonato } from '@/types'
import type { CampeonatoStore } from '@/types/store'

const props = defineProps<{
  campeonato: Campeonato
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated'): void
  (e: 'deleted'): void
}>()

const campeonatoStore = useCampeonatoStore() as CampeonatoStore
const showConfirmDelete = ref(false)

const formData = ref({
  nombre: '',
  fecha_inicio: '',
  dias_duracion: 1,
  numero_partidas: 1,
  grupo_b: false
})

onMounted(() => {
  formData.value = {
    nombre: props.campeonato.nombre,
    fecha_inicio: props.campeonato.fecha_inicio,
    dias_duracion: props.campeonato.dias_duracion,
    numero_partidas: props.campeonato.numero_partidas,
    grupo_b: props.campeonato.grupo_b || false
  }
})

const handleSubmit = async () => {
  try {
    await campeonatoStore.updateCampeonato(props.campeonato.id, formData.value)
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Error al modificar campeonato:', error)
  }
}

const confirmarEliminar = () => {
  showConfirmDelete.value = true
}

const eliminarCampeonato = async () => {
  try {
    await campeonatoStore.deleteCampeonato(props.campeonato.id)
    emit('deleted')
    emit('close')
  } catch (error) {
    console.error('Error al eliminar campeonato:', error)
  }
}
</script> 