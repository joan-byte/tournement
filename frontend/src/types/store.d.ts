import type { Campeonato, Pareja, Mesa } from './index'

export interface CampeonatoStoreState {
  campeonatoActual: Campeonato | null
  campeonatos: Campeonato[]
  parejasCampeonatoActual: Pareja[]
}

export interface CampeonatoStoreActions {
  getCurrentCampeonato: () => Campeonato | null
  loadCampeonatoActual: () => Promise<Campeonato | null>
  fetchCampeonatos: () => Promise<Campeonato[]>
  createCampeonato: (data: Partial<Campeonato>) => Promise<Campeonato>
  updateCampeonato: (id: number, data: Partial<Campeonato>) => Promise<Campeonato>
  deleteCampeonato: (id: number) => Promise<void>
  fetchParejasCampeonato: (campeonatoId: number) => Promise<Pareja[]>
  setCampeonatoActual: (campeonato: Campeonato | null) => Promise<void>
}

export type CampeonatoStore = CampeonatoStoreState & CampeonatoStoreActions

export interface MesaState {
  mesas: Mesa[]
}

export interface MesaStoreActions {
  getMesasAsignadas: (campeonatoId: number) => Promise<Mesa[]>
  getMesa: (mesaId: number) => Promise<Mesa>
  sortearMesas: (campeonatoId: number) => Promise<any>
  eliminarMesas: (campeonatoId: number) => Promise<any>
}

export type MesaStore = MesaState & MesaStoreActions

declare module 'pinia' {
  export interface PiniaCustomProperties {
    campeonatoStore: CampeonatoStore
    mesaStore: MesaStore
  }
} 