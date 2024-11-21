import { defineStore } from 'pinia'
import axios from 'axios'
import type { Pareja } from '@/types'

/**
 * Store de Pinia para gestionar el estado y las operaciones relacionadas con las parejas de jugadores
 * Permite realizar operaciones CRUD y gestionar el estado de las parejas en el campeonato
 */
export const useParejaStore = defineStore('pareja', {
  // Estado inicial del store
  state: () => ({
    parejas: [] as Pareja[] // Array que almacena las parejas del campeonato
  }),

  actions: {
    /**
     * Obtiene todas las parejas de un campeonato específico
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<Pareja[]>} Lista de parejas del campeonato
     * @throws {Error} Si hay un error en la petición
     */
    async fetchParejasCampeonato(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/parejas/campeonato/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching parejas:', error)
        throw error
      }
    },

    /**
     * Crea una nueva pareja en el sistema
     * @param {any} parejaData - Datos de la pareja a crear
     * @returns {Promise<Pareja>} Datos de la pareja creada
     * @throws {Error} Si hay un error en la creación
     */
    async createPareja(parejaData: any) {
      try {
        const response = await axios.post('/api/parejas', parejaData)
        return response.data
      } catch (error) {
        console.error('Error creating pareja:', error)
        throw error
      }
    },

    /**
     * Obtiene los jugadores asociados a una pareja específica
     * @param {number} parejaId - ID de la pareja
     * @returns {Promise<Array>} Array con los dos jugadores de la pareja
     * @throws {Error} Si hay un error en la petición o el formato de respuesta es inválido
     */
    async fetchJugadoresPareja(parejaId: number) {
      try {
        const response = await axios.get(`/api/parejas/${parejaId}/jugadores`)
        console.log('Respuesta del servidor:', response.data)
        
        if (!response.data || !Array.isArray(response.data) || response.data.length !== 2) {
          console.error('Formato de respuesta inválido:', response.data)
          throw new Error('Formato de respuesta inválido')
        }
        
        return response.data
      } catch (error) {
        console.error('Error fetching jugadores:', error)
        throw error
      }
    },

    /**
     * Actualiza el estado (activa/inactiva) de una pareja
     * @param {number} parejaId - ID de la pareja
     * @param {boolean} estado - Nuevo estado de la pareja
     * @throws {Error} Si hay un error al actualizar el estado
     */
    async toggleParejaEstado(parejaId: number, estado: boolean) {
      try {
        await axios.put(`/api/parejas/${parejaId}`, { activa: estado })
      } catch (error) {
        console.error('Error toggling pareja estado:', error)
        throw error
      }
    },

    /**
     * Actualiza los datos de una pareja existente
     * @param {number} parejaId - ID de la pareja
     * @param {any} data - Nuevos datos de la pareja
     * @returns {Promise<Pareja>} Datos actualizados de la pareja
     * @throws {Error} Si hay un error en la actualización
     */
    async updatePareja(parejaId: number, data: any) {
      try {
        const response = await axios.put(`/api/parejas/${parejaId}`, data)
        return response.data
      } catch (error) {
        console.error('Error updating pareja:', error)
        throw error
      }
    },

    /**
     * Elimina una pareja del sistema
     * @param {number} parejaId - ID de la pareja a eliminar
     * @throws {Error} Si hay un error en la eliminación
     */
    async deletePareja(parejaId: number) {
      try {
        await axios.delete(`/api/parejas/${parejaId}`)
      } catch (error) {
        console.error('Error deleting pareja:', error)
        throw error
      }
    }
  }
}) 