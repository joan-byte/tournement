import { defineStore } from 'pinia'
import axios from 'axios'
import type { Campeonato } from '@/types'

export const useCampeonatoStore = defineStore('campeonato', {
  state: () => ({
    campeonatoActual: null as Campeonato | null,
    campeonatos: [] as Campeonato[]
  }),

  actions: {
    getCurrentCampeonato() {
      return this.campeonatoActual
    },

    async fetchCampeonatos() {
      try {
        const response = await axios.get('/api/campeonatos')
        this.campeonatos = response.data
        return this.campeonatos
      } catch (error) {
        console.error('Error fetching campeonatos:', error)
        throw error
      }
    },

    async createCampeonato(campeonatoData: Partial<Campeonato>) {
      try {
        const response = await axios.post('/api/campeonatos', campeonatoData)
        this.campeonatos.push(response.data)
        return response.data
      } catch (error) {
        console.error('Error creating campeonato:', error)
        throw error
      }
    },

    async updateCampeonato(id: number, data: Partial<Campeonato>) {
      try {
        const response = await axios.put(`/api/campeonatos/${id}`, data)
        if (this.campeonatoActual?.id === id) {
          this.campeonatoActual = response.data
        }
        return response.data
      } catch (error) {
        console.error('Error updating campeonato:', error)
        throw error
      }
    },

    setCampeonatoActual(campeonato: Campeonato | null) {
      this.campeonatoActual = campeonato
      if (campeonato) {
        localStorage.setItem('campeonato_id', campeonato.id.toString())
        localStorage.setItem('campeonato_nombre', campeonato.nombre)
      } else {
        localStorage.removeItem('campeonato_id')
        localStorage.removeItem('campeonato_nombre')
      }
    },

    async loadCampeonatoActual() {
      const campeonatoId = localStorage.getItem('campeonato_id')
      if (campeonatoId) {
        try {
          const response = await axios.get(`/api/campeonatos/${campeonatoId}`)
          this.setCampeonatoActual(response.data)
        } catch (error) {
          console.error('Error loading current campeonato:', error)
          this.setCampeonatoActual(null)
        }
      }
    }
  }
}) 