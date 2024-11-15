import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'
import type { MesaStore, MesaState } from '@/types/store'

export const useMesaStore = defineStore('mesa', {
  state: (): MesaState => ({
    mesas: []
  }),

  actions: {
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

    async getMesa(mesaId: number) {
      try {
        const response = await axios.get<Mesa>(`/api/mesas/${mesaId}`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo mesa:', error)
        throw error
      }
    },

    async sortearMesas(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/sortear-parejas/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error al sortear mesas:', error)
        throw error
      }
    },

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