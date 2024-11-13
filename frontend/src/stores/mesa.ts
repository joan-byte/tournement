import { defineStore } from 'pinia'
import axios from 'axios'

interface MesaState {
  mesas: any[];
}

export const useMesaStore = defineStore('mesa', {
  state: (): MesaState => ({
    mesas: []
  }),
  
  actions: {
    async sortearMesas(campeonatoId: number) {
      try {
        const response = await axios.post(`/api/mesas/sortear/${campeonatoId}`)
        this.mesas = response.data
        return response.data
      } catch (error) {
        throw error
      }
    },

    async eliminarMesas(campeonatoId: number) {
      try {
        await axios.delete(`/api/mesas/campeonato/${campeonatoId}`)
        this.mesas = []
      } catch (error) {
        throw error
      }
    }
  }
}) 