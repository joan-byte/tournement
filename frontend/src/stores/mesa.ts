import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'

export const useMesaStore = defineStore('mesa', {
  state: () => ({
    mesas: [] as Mesa[]
  }),

  actions: {
    async sortearMesas(campeonatoId: number): Promise<any> {
      try {
        const response = await axios.post(`/api/partidas/${campeonatoId}/sorteo-inicial`)
        return response.data
      } catch (error) {
        console.error('Error al sortear mesas:', error)
        throw error
      }
    },

    async eliminarMesas(campeonatoId: number): Promise<any> {
      try {
        const response = await axios.delete(`/api/partidas/${campeonatoId}/mesas`)
        return response.data
      } catch (error) {
        console.error('Error al eliminar mesas:', error)
        throw error
      }
    },

    async getMesasAsignadas(campeonatoId: number): Promise<Mesa[]> {
      try {
        const response = await axios.get(`/api/partidas/${campeonatoId}/mesas`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo mesas asignadas:', error)
        throw error
      }
    },

    async getMesa(mesaId: number): Promise<Mesa> {
      try {
        const response = await axios.get(`/api/partidas/mesa/${mesaId}`)
        return response.data
      } catch (error) {
        console.error('Error al obtener mesa:', error)
        throw error
      }
    },

    async cerrarPartida(campeonatoId: number): Promise<any> {
      try {
        const response = await axios.post(`/api/partidas/${campeonatoId}/cerrar-partida`)
        return response.data
      } catch (error) {
        console.error('Error cerrando partida:', error)
        throw error
      }
    }
  }
}) 