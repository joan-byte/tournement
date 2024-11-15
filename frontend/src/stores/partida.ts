import { defineStore } from 'pinia'
import axios from 'axios'

interface PartidaState {
  mesasAsignadas: any[];
}

export const usePartidaStore = defineStore('partida', {
  state: (): PartidaState => ({
    mesasAsignadas: []
  }),
  
  actions: {
    async sortearParejas(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/sortear-parejas/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error al sortear parejas:', error)
        throw error
      }
    },

    async iniciarPartida(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/partidas/iniciar/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error al iniciar partida:', error)
        throw error
      }
    }
  }
}) 