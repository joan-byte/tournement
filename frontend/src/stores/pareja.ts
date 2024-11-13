import { defineStore } from 'pinia'
import axios from 'axios'
import type { Pareja } from '@/types'

interface ParejaState {
  parejas: Pareja[];
}

interface CreateParejaData {
  nombre: string;
  club?: string;
  campeonato_id: number;
  numero?: number;
  jugador1: {
    nombre: string;
    apellido: string;
  };
  jugador2: {
    nombre: string;
    apellido: string;
  };
}

interface Jugador {
  id: number;
  nombre: string;
  apellido: string;
  pareja_id: number;
  campeonato_id: number;
}

export const useParejaStore = defineStore('pareja', {
  state: (): ParejaState => ({
    parejas: []
  }),
  
  actions: {
    async fetchParejasCampeonato(campeonatoId: number) {
      try {
        const response = await axios.get<Pareja[]>('/api/parejas/', {
          params: { campeonato_id: campeonatoId }
        })
        this.parejas = response.data
        return this.parejas
      } catch (error) {
        throw error
      }
    },

    async fetchJugadoresPareja(parejaId: number) {
      try {
        const response = await axios.get<{ jugadores: Jugador[] }>(`/api/parejas/${parejaId}/jugadores`)
        return response.data.jugadores
      } catch (error) {
        throw error
      }
    },

    async createPareja(data: CreateParejaData) {
      try {
        const response = await axios.post<Pareja>('/api/parejas/', data)
        this.parejas.push(response.data)
        return response.data
      } catch (error) {
        throw error
      }
    },

    async updatePareja(parejaId: number, data: Partial<CreateParejaData>) {
      try {
        const response = await axios.put<Pareja>(`/api/parejas/${parejaId}`, data)
        const index = this.parejas.findIndex((p: Pareja) => p.id === parejaId)
        if (index !== -1) {
          this.parejas[index] = response.data
        }
        return response.data
      } catch (error) {
        throw error
      }
    },

    async deletePareja(parejaId: number) {
      try {
        await axios.delete(`/api/parejas/${parejaId}`)
        this.parejas = this.parejas.filter((p: Pareja) => p.id !== parejaId)
      } catch (error) {
        throw error
      }
    },

    async toggleParejaEstado(parejaId: number, activa: boolean) {
      try {
        const response = await axios.put<Pareja>(`/api/parejas/${parejaId}`, { activa })
        const index = this.parejas.findIndex((p: Pareja) => p.id === parejaId)
        if (index !== -1) {
          this.parejas[index] = response.data
        }
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
}) 