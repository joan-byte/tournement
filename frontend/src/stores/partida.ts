// Importaciones necesarias para el store
import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * Interface que define la estructura del estado de la partida
 */
interface PartidaState {
  mesasAsignadas: any[]; // Array que almacena las mesas asignadas a la partida
}

/**
 * Store de Pinia para gestionar el estado y las operaciones relacionadas con las partidas
 * Permite gestionar el sorteo de parejas y el inicio de partidas en un campeonato
 */
export const usePartidaStore = defineStore('partida', {
  // Estado inicial del store
  state: (): PartidaState => ({
    mesasAsignadas: [] // Inicialización del array de mesas asignadas
  }),
  
  actions: {
    /**
     * Realiza el sorteo de parejas para un campeonato específico
     * @param {number} campeonatoId - ID del campeonato donde se realizará el sorteo
     * @returns {Promise<any>} Resultado del sorteo de parejas
     * @throws {Error} Si hay un error durante el proceso de sorteo
     */
    async sortearParejas(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/sortear-parejas/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error al sortear parejas:', error)
        throw error
      }
    },

    /**
     * Inicia una nueva partida en un campeonato específico
     * @param {number} campeonatoId - ID del campeonato donde se iniciará la partida
     * @returns {Promise<any>} Datos de la partida iniciada
     * @throws {Error} Si hay un error al iniciar la partida
     */
    async iniciarPartida(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/iniciar/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error al iniciar partida:', error)
        throw error
      }
    }
  }
}) 