import { defineStore } from 'pinia'
import axios from 'axios'

export const useRankingStore = defineStore('ranking', {
  state: () => ({
    rankingFinal: []
  }),

  actions: {
    async fetchRankingFinal(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/ranking/${campeonatoId}/final`)
        return response.data
      } catch (error) {
        console.error('Error fetching ranking final:', error)
        throw error
      }
    }
  }
}) 