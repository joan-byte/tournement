import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'
import type { MesaStore, MesaState } from '@/types/store'
import { useResultadoStore } from './resultado'

// Interfaz para el ranking
interface RankingItem {
  pareja_id: number
  posicion: number
  // ... otros campos del ranking si los hay
}

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
     * Realiza el sorteo inicial de mesas (solo para la primera partida)
     * @param campeonatoId - ID del campeonato
     */
    async sortearMesas(campeonatoId: number) {
      try {
        await axios.post(`/api/mesas/sorteo/${campeonatoId}`)
      } catch (error) {
        console.error('Error en sorteo de mesas:', error)
        throw error
      }
    },

    /**
     * Asigna mesas según el ranking actual (para partidas después de la primera)
     * @param campeonatoId - ID del campeonato
     */
    async asignarMesasPorRanking(campeonatoId: number) {
      try {
        // 1. Obtener el ranking actual
        const resultadoStore = useResultadoStore()
        const ranking = await resultadoStore.fetchResultados(campeonatoId)

        // 2. Ordenar parejas por posición en el ranking
        const parejasOrdenadas = ranking.sort((a: RankingItem, b: RankingItem) => 
          a.posicion - b.posicion
        )

        // 3. Crear las asignaciones de mesas
        const asignaciones = []
        let numeroMesa = 1

        // Procesar parejas de dos en dos hasta que quede una o ninguna
        for (let i = 0; i < parejasOrdenadas.length - 1; i += 2) {
          asignaciones.push({
            mesa_numero: numeroMesa,
            pareja1_id: parejasOrdenadas[i].pareja_id,
            pareja2_id: parejasOrdenadas[i + 1].pareja_id
          })
          numeroMesa++
        }

        // Si queda una pareja impar, asignarla a la última mesa sola
        if (parejasOrdenadas.length % 2 !== 0) {
          const ultimaPareja = parejasOrdenadas[parejasOrdenadas.length - 1]
          asignaciones.push({
            mesa_numero: numeroMesa,
            pareja1_id: ultimaPareja.pareja_id,
            pareja2_id: null // Indica que esta pareja juega sola
          })
        }

        // 4. Enviar las asignaciones al servidor
        await axios.post(`/api/mesas/asignar/${campeonatoId}`, {
          asignaciones: asignaciones
        })

      } catch (error) {
        console.error('Error al asignar mesas por ranking:', error)
        throw error
      }
    },

    /**
     * Asigna mesas según corresponda (sorteo para primera partida, ranking para las demás)
     * @param campeonatoId - ID del campeonato
     * @param partidaActual - Número de partida actual
     */
    async asignarMesas(campeonatoId: number, partidaActual: number) {
      if (partidaActual === 1) {
        // Primera partida: sorteo aleatorio
        await this.sortearMesas(campeonatoId)
      } else {
        // Demás partidas: asignación por ranking
        await this.asignarMesasPorRanking(campeonatoId)
      }
    },

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