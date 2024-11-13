import { defineStore } from 'pinia'
import axios from 'axios'
import type { Resultado, ResultadoBase, ResultadoResponse } from '@/types'

interface ResultadoState {
  resultados: Resultado[];
  pareja1: ResultadoBase | null;
  pareja2: ResultadoBase | null;
}

export const useResultadoStore = defineStore('resultado', {
  state: (): ResultadoState => ({
    resultados: [],
    pareja1: null,
    pareja2: null
  }),
  
  actions: {
    async fetchResultados(campeonatoId: number) {
      try {
        const response = await axios.get<Resultado[]>(`/api/resultados/campeonato/${campeonatoId}`)
        this.resultados = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching resultados:', error)
        throw error
      }
    },

    async getResultadosMesa(mesaId: number, partida: number, campeonatoId: number) {
      try {
        const response = await axios.get<ResultadoResponse>(
          `/api/resultados/${mesaId}/${partida}`,
          {
            params: {
              campeonato_id: campeonatoId
            }
          }
        )
        this.pareja1 = response.data.pareja1
        this.pareja2 = response.data.pareja2 || null
        return response.data
      } catch (error) {
        console.error('Error fetching resultados de mesa:', error)
        throw error
      }
    },

    async guardarResultados(payload: {
      campeonato_id: number;
      pareja1: ResultadoBase;
      pareja2?: ResultadoBase;
    }) {
      try {
        const response = await axios.post('/api/resultados/', payload)
        return response.data
      } catch (error) {
        console.error('Error guardando resultados:', error)
        throw error
      }
    },

    async actualizarRanking(campeonatoId: number) {
      try {
        await axios.post(`/api/campeonatos/${campeonatoId}/actualizar-ranking`)
      } catch (error) {
        console.error('Error actualizando ranking:', error)
        throw error
      }
    },

    calcularResultados(pareja1: ResultadoBase, pareja2: ResultadoBase | null) {
      if (!pareja2 || pareja2.id_pareja === null) {
        // Caso de mesa con una sola pareja
        pareja1.RP = 150
        pareja1.PG = 1
        pareja1.PP = 150
        
        if (pareja2) {
          pareja2.RP = 0
          pareja2.PG = 0
          pareja2.PP = -150
        }
      } else {
        // Lógica normal para dos parejas
        if (pareja1.RP > pareja2.RP) {
          pareja1.PG = 1
          pareja2.PG = 0
        } else if (pareja1.RP < pareja2.RP) {
          pareja1.PG = 0
          pareja2.PG = 1
        } else {
          pareja2.RP = pareja1.RP - 1
          pareja1.PG = 1
          pareja2.PG = 0
        }

        pareja1.PP = pareja1.RP - pareja2.RP
        pareja2.PP = pareja2.RP - pareja1.RP
      }

      return { pareja1, pareja2 }
    },

    validarResultados(pareja1: ResultadoBase, pareja2: ResultadoBase | null): boolean {
      // Validar que ambos RP no sean 0 al mismo tiempo
      if (pareja1.RP === 0 && (!pareja2 || pareja2.RP === 0)) {
        return false
      }

      // Validar que los RP sean diferentes si hay dos parejas
      if (pareja2 && pareja2.id_pareja !== null && pareja1.RP === pareja2.RP) {
        return false
      }

      return true
    }
  }
}) 