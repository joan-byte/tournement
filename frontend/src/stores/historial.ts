/**
 * Store de Historial usando Pinia
 * Gestiona el historial de resultados de las parejas en el campeonato
 */

// Importaciones necesarias para el store
import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * Interface que define la estructura del estado del store
 * @property {Record<number, ResultadoHistorico[]>} historialPorPareja - Objeto que almacena el historial de resultados indexado por ID de pareja
 */

interface ResultadoHistorico {
  id: number;
  fecha: string;
  puntuacion: number;
}

interface HistorialState {
  historialPorPareja: Record<number, ResultadoHistorico[]>;
}

/**
 * Store principal de historial
 * Proporciona acceso y gestión del historial de resultados de las parejas
 */
export const useHistorialStore = defineStore('historial', {
  /**
   * Estado inicial del store
   * Inicializa un objeto vacío para almacenar el historial por pareja
   */
  state: (): HistorialState => ({
    historialPorPareja: {}
  }),
  
  actions: {
    /**
     * Obtiene el historial de resultados de una pareja específica en un campeonato
     * @param {number} parejaId - ID de la pareja
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<ResultadoHistorico[]>} Array con el historial de resultados
     * @throws {Error} Si hay un error en la petición
     */
    async getHistorialPareja(parejaId: number, campeonatoId: number) {
      try {
        // Realiza la petición al servidor para obtener el historial
        const response = await axios.get<ResultadoHistorico[]>(
          `/api/historial/pareja/${parejaId}`,
          { params: { campeonato_id: campeonatoId } }
        )
        // Almacena el historial en el estado
        this.historialPorPareja[parejaId] = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching historial:', error)
        throw error
      }
    }
  }
}) 