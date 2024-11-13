<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" v-if="show">
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <form @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <!-- Nombre de la pareja (solo lectura) -->
              <div>
                <label for="nombre_pareja" class="block text-sm font-medium text-gray-700">
                  Nombre de la Pareja
                </label>
                <input
                  type="text"
                  id="nombre_pareja"
                  name="nombre_pareja"
                  :value="nombrePareja"
                  readonly
                  disabled
                  class="mt-1 block w-full rounded-md border-gray-300 bg-gray-100 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Club -->
              <div>
                <label for="club" class="block text-sm font-medium text-gray-700">
                  Club
                </label>
                <input
                  type="text"
                  id="club"
                  name="club"
                  v-model="formData.club"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

              <!-- Jugador 1 -->
              <div class="space-y-2">
                <h4 class="text-sm font-medium text-gray-700">Jugador 1</h4>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="jugador1_nombre" class="block text-sm font-medium text-gray-700">
                      Nombre
                    </label>
                    <input
                      type="text"
                      id="jugador1_nombre"
                      name="jugador1_nombre"
                      v-model="formData.jugador1.nombre"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label for="jugador1_apellido" class="block text-sm font-medium text-gray-700">
                      Apellido
                    </label>
                    <input
                      type="text"
                      id="jugador1_apellido"
                      name="jugador1_apellido"
                      v-model="formData.jugador1.apellido"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>

              <!-- Jugador 2 -->
              <div class="space-y-2">
                <h4 class="text-sm font-medium text-gray-700">Jugador 2</h4>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="jugador2_nombre" class="block text-sm font-medium text-gray-700">
                      Nombre
                    </label>
                    <input
                      type="text"
                      id="jugador2_nombre"
                      name="jugador2_nombre"
                      v-model="formData.jugador2.nombre"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                  <div>
                    <label for="jugador2_apellido" class="block text-sm font-medium text-gray-700">
                      Apellido
                    </label>
                    <input
                      type="text"
                      id="jugador2_apellido"
                      name="jugador2_apellido"
                      v-model="formData.jugador2.apellido"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
              <button
                type="submit"
                id="submit_button"
                name="submit_button"
                class="inline-flex w-full justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600 sm:col-start-2"
              >
                Crear
              </button>
              <button
                type="button"
                id="cancel_button"
                name="cancel_button"
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
import { ref, computed } from 'vue'
import { useParejaStore } from '@/stores/pareja'

const props = defineProps<{
  show: boolean
  campeonatoId?: number
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'created'): void
}>()

const parejaStore = useParejaStore()

const formData = ref({
  club: '',
  campeonato_id: props.campeonatoId,
  jugador1: {
    nombre: '',
    apellido: ''
  },
  jugador2: {
    nombre: '',
    apellido: ''
  }
})

const nombrePareja = computed(() => {
  const jugador1 = formData.value.jugador1
  const jugador2 = formData.value.jugador2
  
  if (!jugador1.nombre || !jugador1.apellido || !jugador2.nombre || !jugador2.apellido) {
    return ''
  }
  
  return `${jugador1.nombre} ${jugador1.apellido} Y ${jugador2.nombre} ${jugador2.apellido}`
})

const handleSubmit = async () => {
  try {
    if (!props.campeonatoId) {
      throw new Error('No se ha seleccionado un campeonato')
    }
    
    await parejaStore.createPareja({
      ...formData.value,
      nombre: nombrePareja.value,
      campeonato_id: props.campeonatoId
    })
    
    emit('created')
    emit('close')
    
    // Resetear el formulario
    formData.value = {
      club: '',
      campeonato_id: props.campeonatoId,
      jugador1: {
        nombre: '',
        apellido: ''
      },
      jugador2: {
        nombre: '',
        apellido: ''
      }
    }
  } catch (error) {
    console.error('Error al crear pareja:', error)
  }
}
</script> 