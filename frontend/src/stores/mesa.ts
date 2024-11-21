import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'
import type { MesaStore, MesaState } from '@/types/store'

/**
 * Store de Pinia para gestionar el estado y las operaciones relacionadas con las mesas de juego
 * @returns {MesaStore} Store tipado para mesas
 */
export const useMesaStore = defineStore('mesa', {
  // Estado inicial del store
  state: (): MesaState => ({
    mesas: [] // Array que almacena las mesas del campeonato
  }),

  actions: {
    /**
     * Obtiene todas las mesas asignadas a un campeonato específico
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<Mesa[]>} Array de mesas asignadas
     * @throws {Error} Si hay un error en la petición
     */
    async getMesasAsignadas(campeonatoId: number) {
      try {
        const response = await axios.get<Mesa[]>(`/api/partidas/${campeonatoId}/mesas`)
        this.mesas = response.data
        return response.data
      } catch (error) {
        console.error('Error obteniendo mesas asignadas:', error)
        throw error
      }
    },

    /**
     * Obtiene los detalles de una mesa específica
     * @param {number} mesaId - ID de la mesa
     * @returns {Promise<Mesa>} Detalles de la mesa
     * @throws {Error} Si hay un error en la petición
     */
    async getMesa(mesaId: number) {
      try {
        const response = await axios.get<Mesa>(`/api/mesas/${mesaId}`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo mesa:', error)
        throw error
      }
    },

    /**
     * Elimina todas las mesas asociadas a un campeonato
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<any>} Resultado de la operación
     * @throws {Error} Si hay un error en la petición
     */
    async eliminarMesas(campeonatoId: number) {
      try {
        const response = await axios.delete(`/api/partidas/${campeonatoId}/mesas`)
        return response.data
      } catch (error) {
        console.error('Error al eliminar mesas:', error)
        throw error
      }
    }
  }
}) as unknown as () => MesaStore 