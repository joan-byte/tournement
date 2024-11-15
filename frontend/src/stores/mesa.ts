import { defineStore } from 'pinia'
import axios from 'axios'
import type { Mesa } from '@/types'

export const useMesaStore = defineStore('mesa', {
  state: () => ({
    mesas: [] as Mesa[]
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
    }
  }
}) 