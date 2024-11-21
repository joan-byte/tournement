<template>
  <!-- Modal overlay con fondo semitransparente -->
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" v-if="show">
    <!-- Contenedor principal del modal -->
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <!-- Centrado vertical y horizontal del contenido -->
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <!-- Contenedor del formulario con estilos y animaciones -->
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <!-- Formulario de edición -->
          <form @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <!-- Número de pareja (solo lectura) -->
              <div>
                <label for="numero_pareja" class="block text-sm font-medium text-gray-700">
                  Número de Pareja
                </label>
                <input
                  type="text"
                  id="numero_pareja"
                  name="numero_pareja"
                  :value="pareja.numero"
                  readonly
                  disabled
                  class="mt-1 block w-full rounded-md border-gray-300 bg-gray-100 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>

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
            <div class="mt-5 sm:mt-6 grid grid-cols-3 gap-3">
              <button
                type="button"
                @click="borrarPareja"
                class="inline-flex justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500"
              >
                Eliminar
              </button>
              <button
                type="button"
                @click="$emit('close')"
                class="inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="inline-flex justify-center rounded-md bg-primary-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500"
              >
                Guardar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Importaciones necesarias
import { ref, computed, onMounted } from 'vue'
import { useParejaStore } from '@/stores/pareja'
import type { Pareja } from '@/types'

// Props del componente
const props = defineProps<{
  show: boolean            // Controla la visibilidad del modal
  pareja: Pareja          // Datos de la pareja a editar
}>()

// Eventos que puede emitir el componente
const emit = defineEmits<{
  (e: 'close'): void      // Evento para cerrar el modal
  (e: 'updated'): void    // Evento para notificar actualización exitosa
}>()

// Inicialización del store
const parejaStore = useParejaStore()

/**
 * Estado del formulario con los datos editables de la pareja
 * Incluye club y datos de ambos jugadores
 */
const formData = ref({
  club: props.pareja.club || '',
  jugador1: {
    nombre: '',
    apellido: ''
  },
  jugador2: {
    nombre: '',
    apellido: ''
  }
})

/**
 * Computed property que genera el nombre completo de la pareja
 * combinando los nombres y apellidos de ambos jugadores
 */
const nombrePareja = computed(() => {
  const jugador1 = formData.value.jugador1
  const jugador2 = formData.value.jugador2
  
  if (!jugador1.nombre || !jugador1.apellido || !jugador2.nombre || !jugador2.apellido) {
    return props.pareja.nombre
  }
  
  return `${jugador1.nombre} ${jugador1.apellido} Y ${jugador2.nombre} ${jugador2.apellido}`
})

/**
 * Hook que se ejecuta al montar el componente
 * Carga los datos de los jugadores desde el servidor
 */
onMounted(async () => {
  try {
    const jugadores = await parejaStore.fetchJugadoresPareja(props.pareja.id)
    console.log('Jugadores cargados:', jugadores)
    
    // Actualiza el formulario con los datos obtenidos
    if (jugadores && Array.isArray(jugadores) && jugadores.length === 2) {
      formData.value = {
        club: props.pareja.club || '',
        jugador1: {
          nombre: jugadores[0].nombre,
          apellido: jugadores[0].apellido
        },
        jugador2: {
          nombre: jugadores[1].nombre,
          apellido: jugadores[1].apellido
        }
      }
      console.log('FormData actualizado:', formData.value)
    } else {
      console.error('Formato de jugadores incorrecto:', jugadores)
    }
  } catch (error) {
    console.error('Error al cargar jugadores:', error)
  }
})

/**
 * Maneja el envío del formulario
 * Actualiza los datos de la pareja en el servidor
 */
const handleSubmit = async () => {
  try {
    const updateData = {
      ...formData.value,
      nombre: nombrePareja.value,
      campeonato_id: props.pareja.campeonato_id
    }
    await parejaStore.updatePareja(props.pareja.id, updateData)
    
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Error al actualizar pareja:', error)
  }
}

/**
 * Maneja la eliminación de la pareja
 * Solicita confirmación antes de proceder
 */
const borrarPareja = async () => {
  if (confirm('¿Está seguro de que desea eliminar esta pareja?')) {
    try {
      await parejaStore.deletePareja(props.pareja.id)
      emit('updated')
      emit('close')
    } catch (error) {
      console.error('Error al eliminar pareja:', error)
    }
  }
}
</script> 