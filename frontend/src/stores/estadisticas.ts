import { defineStore } from 'pinia'
import axios from 'axios'
import type { ResultadoEstadisticas } from '@/types'

interface EstadisticasState {
  estadisticasPorPareja: Record<number, ResultadoEstadisticas>;
}

export const useEstadisticasStore = defineStore('estadisticas', {
  state: (): EstadisticasState => ({
    estadisticasPorPareja: {}
  }),
  
  actions: {
    async getEstadisticasPareja(parejaId: number, campeonatoId: number) {
      try {
        const response = await axios.get<ResultadoEstadisticas>(
          `/api/estadisticas/pareja/${parejaId}`,
          { params: { campeonato_id: campeonatoId } }
        )
        this.estadisticasPorPareja[parejaId] = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching estadísticas:', error)
        throw error
      }
    }
  }
}) 