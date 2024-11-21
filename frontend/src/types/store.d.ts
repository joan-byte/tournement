/**
 * Archivo de definición de tipos para los stores de Pinia
 * Contiene las interfaces que definen la estructura de los diferentes stores
 */

import type { Campeonato, Pareja, Mesa } from './index'

/**
 * Interface que define el estado del store de Campeonato
 * @interface CampeonatoStoreState
 */
export interface CampeonatoStoreState {
  campeonatoActual: Campeonato | null    // Campeonato seleccionado actualmente
  campeonatos: Campeonato[]              // Lista de todos los campeonatos
  parejasCampeonatoActual: Pareja[]      // Parejas del campeonato actual
}

/**
 * Interface que define las acciones disponibles en el store de Campeonato
 * @interface CampeonatoStoreActions
 */
export interface CampeonatoStoreActions {
  getCurrentCampeonato: () => Campeonato | null                              // Obtiene el campeonato actual
  loadCampeonatoActual: () => Promise<Campeonato | null>                    // Carga el campeonato actual desde el servidor
  fetchCampeonatos: () => Promise<Campeonato[]>                             // Obtiene todos los campeonatos
  createCampeonato: (data: Partial<Campeonato>) => Promise<Campeonato>      // Crea un nuevo campeonato
  updateCampeonato: (id: number, data: Partial<Campeonato>) => Promise<Campeonato>  // Actualiza un campeonato existente
  deleteCampeonato: (id: number) => Promise<void>                           // Elimina un campeonato
  fetchParejasCampeonato: (campeonatoId: number) => Promise<Pareja[]>       // Obtiene las parejas de un campeonato
  setCampeonatoActual: (campeonato: Campeonato | null) => Promise<void>     // Establece el campeonato actual
}

/**
 * Tipo que combina el estado y las acciones del store de Campeonato
 * @typedef {CampeonatoStoreState & CampeonatoStoreActions} CampeonatoStore
 */
export type CampeonatoStore = CampeonatoStoreState & CampeonatoStoreActions

/**
 * Interface que define el estado del store de Mesa
 * @interface MesaState
 */
export interface MesaState {
  mesas: Mesa[]     // Lista de mesas en el sistema
}

/**
 * Interface que define las acciones disponibles en el store de Mesa
 * @interface MesaStoreActions
 */
export interface MesaStoreActions {
  getMesasAsignadas: (campeonatoId: number) => Promise<Mesa[]>    // Obtiene las mesas asignadas a un campeonato
  getMesa: (mesaId: number) => Promise<Mesa>                      // Obtiene una mesa específica
  sortearMesas: (campeonatoId: number) => Promise<any>           // Realiza el sorteo de mesas
  eliminarMesas: (campeonatoId: number) => Promise<any>          // Elimina las mesas de un campeonato
}

/**
 * Tipo que combina el estado y las acciones del store de Mesa
 * @typedef {MesaState & MesaStoreActions} MesaStore
 */
export type MesaStore = MesaState & MesaStoreActions

/**
 * Extensión del módulo Pinia para incluir las propiedades personalizadas
 * Permite el acceso tipado a los stores desde cualquier componente
 */
declare module 'pinia' {
  export interface PiniaCustomProperties {
    campeonatoStore: CampeonatoStore    // Store global de campeonatos
    mesaStore: MesaStore                // Store global de mesas
  }
} 