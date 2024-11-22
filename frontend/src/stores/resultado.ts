import { defineStore } from 'pinia'
import axios from 'axios'

// Interfaces necesarias
interface BaseResultado {
  pareja_id: number
  GB: string
  PG: number
  PP: number
  RP: number
  nombre_pareja?: string
  club?: string
}

interface RankingResultado extends BaseResultado {
  PG_total: number
  PP_total: number
  posicion: number
}

interface ResultadoAcumulado {
  [key: number]: RankingResultado
}

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
    resultados: [] as BaseResultado[] // Array que almacena temporalmente los resultados de las partidas
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
        const response = await axios.post('/api/resultados/', resultado)
        return response.data
      } catch (error: any) {
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
    async fetchResultados(campeonatoId: number): Promise<RankingResultado[]> {
      try {
        const response = await axios.get(`/api/resultados/ranking/${campeonatoId}`)
        console.log('Datos crudos del servidor:', response.data)
        
        const resultados = (response.data as BaseResultado[]).map(resultado => {
          const resultadoMapeado = {
            ...resultado,
            PP: resultado.PP !== null ? Number(resultado.PP) : 0,
            PG: resultado.PG !== null ? Number(resultado.PG) : 0
          }
          console.log('Resultado mapeado:', {
            pareja_id: resultado.pareja_id,
            PP_original: resultado.PP,
            PP_convertido: resultadoMapeado.PP
          })
          return resultadoMapeado
        })

        const parejasTotales = resultados.reduce((acc: ResultadoAcumulado, curr: BaseResultado) => {
          if (!acc[curr.pareja_id]) {
            acc[curr.pareja_id] = {
              ...curr,
              PG_total: 0,
              PP_total: 0,
              posicion: 0
            }
          }

          acc[curr.pareja_id].PG_total += curr.PG
          const PP_previo = acc[curr.pareja_id].PP_total
          acc[curr.pareja_id].PP_total = Number(acc[curr.pareja_id].PP_total) + Number(curr.PP)
          
          console.log('Acumulación PP para pareja', curr.pareja_id, {
            PP_previo,
            PP_nuevo: curr.PP,
            PP_total_final: acc[curr.pareja_id].PP_total
          })

          return acc
        }, {} as ResultadoAcumulado)

        const resultadosOrdenados = Object.values(parejasTotales).sort((a, b) => {
          if (a.GB !== b.GB) return a.GB.localeCompare(b.GB)
          if (a.PG_total !== b.PG_total) return b.PG_total - a.PG_total
          return b.PP_total - a.PP_total
        })

        return resultadosOrdenados.map((resultado: RankingResultado, index: number) => ({
          ...resultado,
          PP: resultado.PP_total,
          PG: resultado.PG_total,
          posicion: index + 1
        }))

      } catch (error) {
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
        throw error
      }
    }
  }
}) 