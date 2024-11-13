import { defineStore } from 'pinia'
import axios from 'axios'
import type { Pareja } from '@/types'

export const useParejaStore = defineStore('pareja', {
  state: () => ({
    parejas: [] as Pareja[]
  }),

  actions: {
    async fetchParejasCampeonato(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/parejas/campeonato/${campeonatoId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching parejas:', error)
        throw error
      }
    },

    async createPareja(parejaData: any) {
      try {
        const response = await axios.post('/api/parejas', parejaData)
        return response.data
      } catch (error) {
        console.error('Error creating pareja:', error)
        throw error
      }
    },

    async fetchJugadoresPareja(parejaId: number) {
      try {
        const response = await axios.get(`/api/parejas/${parejaId}/jugadores`)
        console.log('Respuesta del servidor:', response.data)
        
        if (!response.data || !Array.isArray(response.data) || response.data.length !== 2) {
          console.error('Formato de respuesta inválido:', response.data)
          throw new Error('Formato de respuesta inválido')
        }
        
        return response.data
      } catch (error) {
        console.error('Error fetching jugadores:', error)
        throw error
      }
    },

    async toggleParejaEstado(parejaId: number, estado: boolean) {
      try {
        await axios.put(`/api/parejas/${parejaId}`, { activa: estado })
      } catch (error) {
        console.error('Error toggling pareja estado:', error)
        throw error
      }
    },

    async updatePareja(parejaId: number, data: any) {
      try {
        const response = await axios.put(`/api/parejas/${parejaId}`, data)
        return response.data
      } catch (error) {
        console.error('Error updating pareja:', error)
        throw error
      }
    },

    async deletePareja(parejaId: number) {
      try {
        await axios.delete(`/api/parejas/${parejaId}`)
      } catch (error) {
        console.error('Error deleting pareja:', error)
        throw error
      }
    }
  }
}) 