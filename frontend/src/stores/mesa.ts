import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'
import type { MesaStore, MesaState } from '@/types/store'
import { useResultadoStore } from './resultado'

interface RankingItem {
  pareja_id: number
  posicion: number
}

export const useMesaStore = defineStore('mesa', {
  state: (): MesaState => ({
    mesas: []
  }),

  actions: {
    async sortearMesas(campeonatoId: number) {
      try {
        await axios.post(`/api/mesas/sorteo/${campeonatoId}`)
      } catch (error) {
        throw error
      }
    },

    async asignarMesasPorRanking(campeonatoId: number) {
      try {
        const resultadoStore = useResultadoStore()
        const ranking = await resultadoStore.fetchResultados(campeonatoId)
        const parejasOrdenadas = ranking.sort((a: RankingItem, b: RankingItem) => 
          a.posicion - b.posicion
        )

        const asignaciones = []
        let numeroMesa = 1

        for (let i = 0; i < parejasOrdenadas.length - 1; i += 2) {
          asignaciones.push({
            mesa_numero: numeroMesa,
            pareja1_id: parejasOrdenadas[i].pareja_id,
            pareja2_id: parejasOrdenadas[i + 1].pareja_id
          })
          numeroMesa++
        }

        if (parejasOrdenadas.length % 2 !== 0) {
          const ultimaPareja = parejasOrdenadas[parejasOrdenadas.length - 1]
          asignaciones.push({
            mesa_numero: numeroMesa,
            pareja1_id: ultimaPareja.pareja_id,
            pareja2_id: null
          })
        }

        await axios.post(`/api/mesas/asignar/${campeonatoId}`, {
          asignaciones: asignaciones
        })

      } catch (error) {
        throw error
      }
    },

    async asignarMesas(campeonatoId: number, partidaActual: number) {
      try {
        if (partidaActual === 0) {
          await this.sortearMesas(campeonatoId)
        } else {
          await this.asignarMesasPorRanking(campeonatoId)
        }
      } catch (error) {
        throw error
      }
    },

    async getMesasAsignadas(campeonatoId: number) {
      try {
        const response = await axios.get<Mesa[]>(`/api/partidas/${campeonatoId}/mesas`)
        this.mesas = response.data
        return response.data
      } catch (error) {
        throw error
      }
    },

    async getMesa(mesaId: number) {
      try {
        const response = await axios.get<Mesa>(`/api/mesas/${mesaId}`)
        return response.data
      } catch (error) {
        throw error
      }
    },

    async eliminarMesas(campeonatoId: number) {
      try {
        const response = await axios.delete(`/api/partidas/${campeonatoId}/mesas`)
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
}) as unknown as () => MesaStore 