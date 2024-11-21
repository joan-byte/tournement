<!-- 
  NuevaPareja.vue - Componente modal para crear una nueva pareja
  Este componente presenta un formulario para registrar una nueva pareja en el sistema,
  permitiendo ingresar los datos de dos jugadores y el club al que pertenecen.
-->

<template>
  <!-- Modal overlay con fondo semitransparente -->
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" v-if="show">
    <!-- Contenedor principal del modal -->
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <!-- Centrado vertical y horizontal del contenido -->
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <!-- Panel del modal con estilos y animaciones -->
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <!-- Formulario de registro de nueva pareja -->
          <form @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <!-- Campo de nombre de pareja (autogenerado y solo lectura) -->
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

              <!-- Campo para el club -->
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

              <!-- Sección de datos del Jugador 1 -->
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

              <!-- Sección de datos del Jugador 2 -->
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

            <!-- Sección de botones de acción -->
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
// Importaciones necesarias para el componente
import { ref, computed } from 'vue'
import { useParejaStore } from '@/stores/pareja'

// Props del componente
const props = defineProps<{
  show: boolean,           // Controla la visibilidad del modal
  campeonatoId?: number   // ID del campeonato al que se asociará la pareja
}>()

// Eventos que puede emitir el componente
const emit = defineEmits<{
  (e: 'close'): void      // Evento para cerrar el modal
  (e: 'created'): void    // Evento para notificar creación exitosa
}>()

// Inicialización del store de parejas
const parejaStore = useParejaStore()

/**
 * Estado del formulario que almacena los datos de la nueva pareja
 * Incluye club, ID del campeonato y datos de ambos jugadores
 */
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

/**
 * Computed property que genera automáticamente el nombre de la pareja
 * combinando los nombres y apellidos de ambos jugadores
 * @returns {string} Nombre completo de la pareja formateado
 */
const nombrePareja = computed(() => {
  const jugador1 = formData.value.jugador1
  const jugador2 = formData.value.jugador2
  
  // Retorna cadena vacía si faltan datos
  if (!jugador1.nombre || !jugador1.apellido || !jugador2.nombre || !jugador2.apellido) {
    return ''
  }
  
  // Formato: "Nombre1 Apellido1 Y Nombre2 Apellido2"
  return `${jugador1.nombre} ${jugador1.apellido} Y ${jugador2.nombre} ${jugador2.apellido}`
})

/**
 * Maneja el envío del formulario para crear una nueva pareja
 * Valida, envía los datos al servidor y maneja la respuesta
 */
const handleSubmit = async () => {
  try {
    // Validación del ID del campeonato
    if (!props.campeonatoId) {
      throw new Error('No se ha seleccionado un campeonato')
    }
    
    // Envío de datos al servidor
    await parejaStore.createPareja({
      ...formData.value,
      nombre: nombrePareja.value,
      campeonato_id: props.campeonatoId
    })
    
    // Notificación de éxito y cierre del modal
    emit('created')
    emit('close')
    
    // Reinicio del formulario a su estado inicial
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