import { defineStore } from 'pinia'
import axios from 'axios'
import type { Resultado } from '@/types/resultado'

export const useResultadoStore = defineStore('resultado', {
  state: () => ({
    resultados: []
  }),

  actions: {
    async saveResultado(resultado: any) {
      try {
        const response = await axios.post('/api/resultados', resultado)
        return response.data
      } catch (error) {
        console.error('Error guardando resultado:', error)
        throw error
      }
    },

    async getResultadoMesa(mesaId: number, partida: number) {
      try {
        const response = await axios.get(`/api/resultados/${mesaId}/${partida}`)
        return response.data
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 404) {
          return null
        }
        throw error
      }
    },

    async fetchResultados(campeonatoId: number): Promise<Resultado[]> {
      try {
        const response = await axios.get(`/api/resultados/ranking/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error obteniendo resultados:', error)
        throw error
      }
    }
  }
}) 