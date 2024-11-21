import { defineStore } from 'pinia'
import axios from 'axios'
import type { Resultado } from '@/types/resultado'

/**
 * Store de Pinia para gestionar los resultados de las partidas del campeonato
 * Proporciona funcionalidades para:
 * - Guardar nuevos resultados
 * - Consultar resultados por mesa
 * - Obtener rankings
 * - Gestionar resultados por campeonato
 */
export const useResultadoStore = defineStore('resultado', {
  // Estado inicial del store que mantiene los resultados en memoria
  state: () => ({
    resultados: [] // Array que almacena temporalmente los resultados de las partidas
  }),

  actions: {
    /**
     * Guarda un nuevo resultado de partida en el servidor
     * @param {any} resultado - Objeto con los datos del resultado (puntuaciones, mesa, parejas, etc)
     * @returns {Promise<any>} Promesa con los datos del resultado guardado
     * @throws {Error} Si hay un error en la comunicación con el servidor
     */
    async saveResultado(resultado: any) {
      try {
        const response = await axios.post('/api/resultados', resultado)
        return response.data
      } catch (error) {
        console.error('Error guardando resultado:', error)
        throw error
      }
    },

    /**
     * Obtiene el resultado específico de una mesa en una partida determinada
     * @param {number} mesaId - Identificador de la mesa
     * @param {number} partida - Número de la partida
     * @returns {Promise<any|null>} Resultado de la mesa o null si no existe
     * @throws {Error} Si hay un error en la petición (excepto 404)
     */
    async getResultadoMesa(mesaId: number, partida: number) {
      try {
        const response = await axios.get(`/api/resultados/${mesaId}/${partida}`)
        return response.data
      } catch (error) {
        // Si no se encuentra el resultado, retornamos null en lugar de lanzar error
        if (axios.isAxiosError(error) && error.response?.status === 404) {
          return null
        }
        throw error
      }
    },

    /**
     * Obtiene el ranking de resultados de un campeonato específico
     * @param {number} campeonatoId - Identificador del campeonato
     * @returns {Promise<Resultado[]>} Array con los resultados ordenados por ranking
     * @throws {Error} Si hay un error al obtener los resultados del servidor
     */
    async fetchResultados(campeonatoId: number): Promise<Resultado[]> {
      try {
        const response = await axios.get(`/api/resultados/ranking/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo resultados:', error)
        throw error
      }
    },

    /**
     * Recupera todos los resultados asociados a un campeonato específico
     * @param {number} campeonatoId - Identificador del campeonato
     * @returns {Promise<any>} Datos completos de todos los resultados del campeonato
     * @throws {Error} Si hay un error en la comunicación con el servidor
     */
    async getResultadosCampeonato(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/resultados/campeonato/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo resultados del campeonato:', error)
        throw error
      }
    }
  }
}) 