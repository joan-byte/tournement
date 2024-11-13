import { defineStore } from 'pinia'
import axios from 'axios'
import type { ResultadoHistorico } from '@/types'

interface HistorialState {
  historialPorPareja: Record<number, ResultadoHistorico[]>;
}

export const useHistorialStore = defineStore('historial', {
  state: (): HistorialState => ({
    historialPorPareja: {}
  }),
  
  actions: {
    async getHistorialPareja(parejaId: number, campeonatoId: number) {
      try {
        const response = await axios.get<ResultadoHistorico[]>(
          `/api/historial/pareja/${parejaId}`,
          { params: { campeonato_id: campeonatoId } }
        )
        this.historialPorPareja[parejaId] = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching historial:', error)
        throw error
      }
    }
  }
}) 