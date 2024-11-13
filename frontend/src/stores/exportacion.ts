import { defineStore } from 'pinia'
import axios from 'axios'

export const useExportacionStore = defineStore('exportacion', {
  actions: {
    async exportarRanking(campeonatoId: number, formato: 'pdf' | 'excel') {
      try {
        const response = await axios.get(
          `/api/exportar/ranking/${campeonatoId}`,
          {
            params: { formato },
            responseType: 'blob'
          }
        )
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `ranking_${campeonatoId}.${formato}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (error) {
        console.error('Error exportando ranking:', error)
        throw error
      }
    },

    async exportarResultados(campeonatoId: number, formato: 'pdf' | 'excel') {
      try {
        const response = await axios.get(
          `/api/exportar/resultados/${campeonatoId}`,
          {
            params: { formato },
            responseType: 'blob'
          }
        )
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `resultados_${campeonatoId}.${formato}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (error) {
        console.error('Error exportando resultados:', error)
        throw error
      }
    }
  }
}) 