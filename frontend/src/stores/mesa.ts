import { defineStore } from 'pinia'
import axios from 'axios'

export const useMesaStore = defineStore('mesa', {
  state: () => ({
    mesas: []
  }),

  actions: {
    async sortearMesas(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/${campeonatoId}/sorteo-inicial`)
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
    },

    async getMesasAsignadas(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/partidas/${campeonatoId}/mesas`)
        return response.data
      } catch (error) {
        console.error('Error al obtener mesas asignadas:', error)
        throw error
      }
    },

    async getMesa(mesaId: number) {
      try {
        const response = await axios.get(`/api/partidas/mesa/${mesaId}`)
        return response.data
      } catch (error) {
        console.error('Error al obtener mesa:', error)
        throw error
      }
    }
  }
}) 