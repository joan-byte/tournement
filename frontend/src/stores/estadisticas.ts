/**
 * Store de Estadísticas usando Pinia
 * Gestiona el estado y las operaciones relacionadas con las estadísticas de las parejas
 * en el campeonato, incluyendo puntos, partidas ganadas y otros indicadores
 */

// Importaciones necesarias para el store
import { defineStore } from 'pinia'
import axios from 'axios'
import type { ResultadoEstadisticas } from '@/types'

/**
 * Interface que define la estructura del estado del store
 * @property {Record<number, ResultadoEstadisticas>} estadisticasPorPareja - Objeto que almacena las estadísticas indexadas por ID de pareja
 */
interface EstadisticasState {
  estadisticasPorPareja: Record<number, ResultadoEstadisticas>;
}

/**
 * Store principal de estadísticas
 * Proporciona acceso y gestión de las estadísticas de las parejas
 */
export const useEstadisticasStore = defineStore('estadisticas', {
  /**
   * Estado inicial del store
   * Inicializa un objeto vacío para almacenar las estadísticas por pareja
   */
  state: (): EstadisticasState => ({
    estadisticasPorPareja: {}
  }),
  
  actions: {
    /**
     * Obtiene las estadísticas de una pareja específica en un campeonato
     * @param {number} parejaId - ID de la pareja
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<ResultadoEstadisticas>} Estadísticas de la pareja
     * @throws {Error} Si hay un error en la petición
     */
    async getEstadisticasPareja(parejaId: number, campeonatoId: number) {
      try {
        // Realiza la petición al servidor para obtener las estadísticas
        const response = await axios.get<ResultadoEstadisticas>(
          `/api/estadisticas/pareja/${parejaId}`,
          { params: { campeonato_id: campeonatoId } }
        )
        // Almacena las estadísticas en el estado
        this.estadisticasPorPareja[parejaId] = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching estadísticas:', error)
        throw error
      }
    }
  }
}) 