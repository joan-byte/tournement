// Importaciones necesarias para el store
import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * Store de Pinia para gestionar el ranking final del campeonato
 * Permite obtener y gestionar la clasificación final de los participantes
 */
export const useRankingStore = defineStore('ranking', {
  // Estado inicial del store
  state: () => ({
    rankingFinal: [] // Array que almacena la clasificación final del campeonato
  }),

  actions: {
    /**
     * Obtiene el ranking final de un campeonato específico
     * @param {number} campeonatoId - ID del campeonato del cual se quiere obtener el ranking
     * @returns {Promise<any>} Datos del ranking final del campeonato
     * @throws {Error} Si hay un error al obtener el ranking
     */
    async fetchRankingFinal(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/ranking/${campeonatoId}/final`)
        return response.data
      } catch (error) {
        console.error('Error fetching ranking final:', error)
        throw error
      }
    }
  }
}) 