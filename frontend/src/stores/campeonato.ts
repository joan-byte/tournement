import { defineStore } from 'pinia'
import axios from 'axios'
import type { Campeonato, Pareja } from '@/types'

export const useCampeonatoStore = defineStore('campeonato', {
  state: () => ({
    campeonatoActual: null as Campeonato | null,
    campeonatos: [] as Campeonato[],
    parejasCampeonatoActual: [] as Pareja[]
  }),

  actions: {
    getCurrentCampeonato() {
      // Verificar si el estado coincide con localStorage
      const storedId = localStorage.getItem('campeonato_id')
      const currentId = this.campeonatoActual?.id?.toString()
      
      if (storedId && (!currentId || storedId !== currentId)) {
        // Si no coinciden, cargar desde localStorage
        this.loadCampeonatoActual()
      }
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
        // Limpiar el estado actual
        localStorage.removeItem('campeonato_id')
        localStorage.removeItem('campeonato_nombre')
        localStorage.removeItem('currentCampeonato')
        localStorage.removeItem('parejasCampeonato')
        this.campeonatoActual = null
        this.parejasCampeonatoActual = []

        if (campeonato) {
          // Obtener datos frescos del servidor
          const [campeonatoResponse, parejasResponse] = await Promise.all([
            axios.get(`/api/campeonatos/${campeonato.id}`),
            axios.get(`/api/parejas/campeonato/${campeonato.id}`)
          ])

          const campeonatoActualizado = campeonatoResponse.data
          this.parejasCampeonatoActual = parejasResponse.data

          // Actualizar localStorage
          localStorage.setItem('campeonato_id', campeonatoActualizado.id.toString())
          localStorage.setItem('campeonato_nombre', campeonatoActualizado.nombre)
          localStorage.setItem('currentCampeonato', JSON.stringify(campeonatoActualizado))
          localStorage.setItem('parejasCampeonato', JSON.stringify(this.parejasCampeonatoActual))

          // Actualizar el estado
          this.campeonatoActual = campeonatoActualizado

          console.log('Estado actualizado:', {
            localStorage: {
              id: localStorage.getItem('campeonato_id'),
              nombre: localStorage.getItem('campeonato_nombre'),
              currentCampeonato: localStorage.getItem('currentCampeonato'),
              parejas: localStorage.getItem('parejasCampeonato')
            },
            storeState: {
              campeonato: this.campeonatoActual,
              parejas: this.parejasCampeonatoActual
            }
          })
        }
      } catch (error) {
        console.error('Error setting current campeonato:', error)
        // Limpiar todo en caso de error
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
          
          // Actualizar todo el estado
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