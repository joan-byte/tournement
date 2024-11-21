/**
 * Store de Exportación usando Pinia
 * Gestiona la exportación de rankings y resultados del campeonato en diferentes formatos
 */

// Importaciones necesarias
import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * Store principal de exportación
 * Proporciona métodos para exportar datos en PDF y Excel
 */
export const useExportacionStore = defineStore('exportacion', {
  actions: {
    /**
     * Exporta el ranking actual del campeonato
     * @param {number} campeonatoId - ID del campeonato a exportar
     * @param {'pdf' | 'excel'} formato - Formato de exportación deseado
     * @throws {Error} Si hay un error en la exportación
     */
    async exportarRanking(campeonatoId: number, formato: 'pdf' | 'excel') {
      try {
        // Realiza la petición al servidor para obtener el archivo
        const response = await axios.get(
          `/api/exportar/ranking/${campeonatoId}`,
          {
            params: { formato },
            responseType: 'blob' // Especifica que la respuesta es un archivo binario
          }
        )
        
        // Crea una URL temporal para el archivo descargado
        const url = window.URL.createObjectURL(new Blob([response.data]))
        // Crea un elemento <a> temporal para la descarga
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `ranking_${campeonatoId}.${formato}`)
        document.body.appendChild(link)
        link.click() // Inicia la descarga
        link.remove() // Limpia el elemento temporal
      } catch (error) {
        console.error('Error exportando ranking:', error)
        throw error
      }
    },

    /**
     * Exporta los resultados detallados del campeonato
     * @param {number} campeonatoId - ID del campeonato a exportar
     * @param {'pdf' | 'excel'} formato - Formato de exportación deseado
     * @throws {Error} Si hay un error en la exportación
     */
    async exportarResultados(campeonatoId: number, formato: 'pdf' | 'excel') {
      try {
        // Realiza la petición al servidor para obtener el archivo
        const response = await axios.get(
          `/api/exportar/resultados/${campeonatoId}`,
          {
            params: { formato },
            responseType: 'blob' // Especifica que la respuesta es un archivo binario
          }
        )
        
        // Crea una URL temporal para el archivo descargado
        const url = window.URL.createObjectURL(new Blob([response.data]))
        // Crea un elemento <a> temporal para la descarga
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `resultados_${campeonatoId}.${formato}`)
        document.body.appendChild(link)
        link.click() // Inicia la descarga
        link.remove() // Limpia el elemento temporal
      } catch (error) {
        console.error('Error exportando resultados:', error)
        throw error
      }
    }
  }
}) 