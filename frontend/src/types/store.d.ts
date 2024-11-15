import type { Campeonato, Pareja } from './index'

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

declare module 'pinia' {
  export interface PiniaCustomProperties {
    campeonatoStore: CampeonatoStore
  }
} 