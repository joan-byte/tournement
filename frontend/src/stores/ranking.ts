import { defineStore } from 'pinia'
import axios from 'axios'
import type { Resultado } from '@/types'

interface RankingState {
  ranking: Resultado[];
  rankingFinal: Resultado[];
}

export const useRankingStore = defineStore('ranking', {
  state: (): RankingState => ({
    ranking: [],
    rankingFinal: []
  }),
  
  actions: {
    async fetchRanking(campeonatoId: number) {
      try {
        const response = await axios.get<Resultado[]>(`/api/ranking/${campeonatoId}`)
        this.ranking = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching ranking:', error)
        throw error
      }
    },

    async fetchRankingFinal(campeonatoId: number) {
      try {
        const response = await axios.get<Resultado[]>(
          `/api/ranking/${campeonatoId}/final`
        )
        this.rankingFinal = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching ranking final:', error)
        throw error
      }
    },

    async actualizarRanking(campeonatoId: number) {
      try {
        await axios.post(`/api/ranking/${campeonatoId}/actualizar`)
      } catch (error) {
        console.error('Error actualizando ranking:', error)
        throw error
      }
    }
  }
}) 