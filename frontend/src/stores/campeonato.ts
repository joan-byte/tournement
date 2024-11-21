/**
 * Store de Campeonato usando Pinia
 * Gestiona el estado y las operaciones relacionadas con los campeonatos
 * Incluye la gestión del campeonato actual y sus parejas asociadas
 */

// Importaciones necesarias
import { defineStore } from 'pinia'
import axios from 'axios'
import type { Campeonato, Pareja } from '@/types'
import type { CampeonatoStoreState } from '@/types/store'

/**
 * Store principal de campeonatos
 * Maneja el estado global relacionado con campeonatos y sus operaciones CRUD
 */
export const useCampeonatoStore = defineStore('campeonato', {
  /**
   * Estado inicial del store
   * @property {Campeonato|null} campeonatoActual - Campeonato seleccionado actualmente
   * @property {Campeonato[]} campeonatos - Lista de todos los campeonatos
   * @property {Pareja[]} parejasCampeonatoActual - Parejas del campeonato actual
   */
  state: (): CampeonatoStoreState => ({
    campeonatoActual: null,
    campeonatos: [],
    parejasCampeonatoActual: []
  }),

  actions: {
    /**
     * Obtiene el campeonato actual desde localStorage o lo carga si es necesario
     * @returns {Campeonato|null} Campeonato actual o null si no hay ninguno seleccionado
     */
    getCurrentCampeonato() {
      const storedId = localStorage.getItem('campeonato_id')
      const currentId = this.campeonatoActual?.id?.toString()
      
      if (storedId && (!currentId || storedId !== currentId)) {
        this.loadCampeonatoActual()
      }
      return this.campeonatoActual
    },

    /**
     * Obtiene todos los campeonatos desde el servidor
     * @returns {Promise<Campeonato[]>} Lista de campeonatos
     */
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

    /**
     * Crea un nuevo campeonato
     * @param {Partial<Campeonato>} campeonatoData - Datos del nuevo campeonato
     * @returns {Promise<Campeonato>} Campeonato creado
     */
    async createCampeonato(campeonatoData: Partial<Campeonato>) {
      try {
        const response = await axios.post<Campeonato>('/api/campeonatos', campeonatoData)
        return response.data
      } catch (error) {
        console.error('Error creating campeonato:', error)
        throw error
      }
    },

    /**
     * Actualiza un campeonato existente
     * @param {number} id - ID del campeonato a actualizar
     * @param {Partial<Campeonato>} campeonatoData - Datos a actualizar
     * @returns {Promise<Campeonato>} Campeonato actualizado
     */
    async updateCampeonato(id: number, campeonatoData: Partial<Campeonato>) {
      try {
        const response = await axios.put<Campeonato>(`/api/campeonatos/${id}`, campeonatoData)
        return response.data
      } catch (error) {
        console.error('Error updating campeonato:', error)
        throw error
      }
    },

    /**
     * Elimina un campeonato
     * @param {number} id - ID del campeonato a eliminar
     */
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

    /**
     * Obtiene las parejas asociadas a un campeonato
     * @param {number} campeonatoId - ID del campeonato
     * @returns {Promise<Pareja[]>} Lista de parejas del campeonato
     */
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

    /**
     * Establece el campeonato actual y carga sus datos relacionados
     * @param {Campeonato|null} campeonato - Campeonato a establecer como actual
     */
    async setCampeonatoActual(campeonato: Campeonato | null) {
      try {
        await this.resetState()

        if (campeonato) {
          const [campeonatoData, parejasData] = await Promise.all([
            axios.get(`/api/campeonatos/${campeonato.id}`),
            axios.get(`/api/parejas/campeonato/${campeonato.id}`)
          ])

          const campeonatoActualizado = campeonatoData.data
          this.parejasCampeonatoActual = parejasData.data

          // Almacena los datos en localStorage
          const storageData = {
            'campeonato_id': campeonatoActualizado.id.toString(),
            'campeonato_nombre': campeonatoActualizado.nombre,
            'currentCampeonato': JSON.stringify(campeonatoActualizado),
            'parejasCampeonato': JSON.stringify(this.parejasCampeonatoActual)
          }
          Object.entries(storageData).forEach(([key, value]) => localStorage.setItem(key, value))

          this.campeonatoActual = campeonatoActualizado
        }
      } catch (error) {
        console.error('Error setting current campeonato:', error)
        await this.resetState()
        throw error
      }
    },

    /**
     * Reinicia el estado del store y limpia localStorage
     */
    resetState() {
      const keysToRemove = ['campeonato_id', 'campeonato_nombre', 'currentCampeonato', 'parejasCampeonato']
      keysToRemove.forEach(key => localStorage.removeItem(key))
      this.campeonatoActual = null
      this.parejasCampeonatoActual = []
    },

    /**
     * Carga el campeonato actual desde localStorage
     * @returns {Promise<Campeonato|null>} Campeonato cargado o null si no existe
     */
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

/**
 * Tipo del store para uso en componentes
 */
export type CampeonatoStore = ReturnType<typeof useCampeonatoStore> 