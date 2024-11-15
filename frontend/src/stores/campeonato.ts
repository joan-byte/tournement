import { defineStore } from 'pinia'
import axios from 'axios'
import type { Campeonato, Pareja } from '@/types'
import type { CampeonatoStoreState } from '@/types/store'

export const useCampeonatoStore = defineStore('campeonato', {
  state: (): CampeonatoStoreState => ({
    campeonatoActual: null,
    campeonatos: [],
    parejasCampeonatoActual: []
  }),

  actions: {
    getCurrentCampeonato() {
      const storedId = localStorage.getItem('campeonato_id')
      const currentId = this.campeonatoActual?.id?.toString()
      
      if (storedId && (!currentId || storedId !== currentId)) {
        this.loadCampeonatoActual()
      }
      return this.campeonatoActual
    },

    async fetchCampeonatos() {
      try {
        const response = await axios.get<Campeonato[]>('/api/campeonatos')
        this.campeonatos = response.data
        return this.campeonatos
      } catch (error) {
        console.error('Error fetching campeonatos:', error)
        throw error
      }
    },

    async createCampeonato(campeonatoData: Partial<Campeonato>) {
      try {
        const response = await axios.post<Campeonato>('/api/campeonatos', campeonatoData)
        return response.data
      } catch (error) {
        console.error('Error creating campeonato:', error)
        throw error
      }
    },

    async updateCampeonato(id: number, campeonatoData: Partial<Campeonato>) {
      try {
        const response = await axios.put<Campeonato>(`/api/campeonatos/${id}`, campeonatoData)
        return response.data
      } catch (error) {
        console.error('Error updating campeonato:', error)
        throw error
      }
    },

    async deleteCampeonato(id: number): Promise<void> {
      try {
        await axios.delete(`/api/campeonatos/${id}`)
        if (this.campeonatoActual?.id === id) {
          await this.setCampeonatoActual(null)
        }
        this.campeonatos = this.campeonatos.filter((c: Campeonato) => c.id !== id)
      } catch (error) {
        console.error('Error deleting campeonato:', error)
        throw error
      }
    },

    async fetchParejasCampeonato(campeonatoId: number) {
      try {
        const response = await axios.get(`/api/parejas/campeonato/${campeonatoId}`)
        this.parejasCampeonatoActual = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching parejas del campeonato:', error)
        throw error
      }
    },

    async setCampeonatoActual(campeonato: Campeonato | null) {
      try {
        localStorage.removeItem('campeonato_id')
        localStorage.removeItem('campeonato_nombre')
        localStorage.removeItem('currentCampeonato')
        localStorage.removeItem('parejasCampeonato')
        this.campeonatoActual = null
        this.parejasCampeonatoActual = []

        if (campeonato) {
          const [campeonatoResponse, parejasResponse] = await Promise.all([
            axios.get(`/api/campeonatos/${campeonato.id}`),
            axios.get(`/api/parejas/campeonato/${campeonato.id}`)
          ])

          const campeonatoActualizado = campeonatoResponse.data
          this.parejasCampeonatoActual = parejasResponse.data

          localStorage.setItem('campeonato_id', campeonatoActualizado.id.toString())
          localStorage.setItem('campeonato_nombre', campeonatoActualizado.nombre)
          localStorage.setItem('currentCampeonato', JSON.stringify(campeonatoActualizado))
          localStorage.setItem('parejasCampeonato', JSON.stringify(this.parejasCampeonatoActual))

          this.campeonatoActual = campeonatoActualizado
        }
      } catch (error) {
        console.error('Error setting current campeonato:', error)
        localStorage.removeItem('campeonato_id')
        localStorage.removeItem('campeonato_nombre')
        localStorage.removeItem('currentCampeonato')
        localStorage.removeItem('parejasCampeonato')
        this.campeonatoActual = null
        this.parejasCampeonatoActual = []
        throw error
      }
    },

    async loadCampeonatoActual() {
      const campeonatoId = localStorage.getItem('campeonato_id')
      if (campeonatoId) {
        try {
          const [campeonatoResponse, parejasResponse] = await Promise.all([
            axios.get(`/api/campeonatos/${campeonatoId}`),
            axios.get(`/api/parejas/campeonato/${campeonatoId}`)
          ])

          const campeonatoActualizado = campeonatoResponse.data
          this.parejasCampeonatoActual = parejasResponse.data
          
          this.campeonatoActual = campeonatoActualizado
          localStorage.setItem('campeonato_id', campeonatoActualizado.id.toString())
          localStorage.setItem('campeonato_nombre', campeonatoActualizado.nombre)
          localStorage.setItem('currentCampeonato', JSON.stringify(campeonatoActualizado))
          localStorage.setItem('parejasCampeonato', JSON.stringify(this.parejasCampeonatoActual))
          
          return campeonatoActualizado
        } catch (error) {
          console.error('Error loading current campeonato:', error)
          localStorage.removeItem('campeonato_id')
          localStorage.removeItem('campeonato_nombre')
          localStorage.removeItem('currentCampeonato')
          localStorage.removeItem('parejasCampeonato')
          this.campeonatoActual = null
          this.parejasCampeonatoActual = []
        }
      }
      return null
    }
  }
})

// Tipo del store
export type CampeonatoStore = ReturnType<typeof useCampeonatoStore> 