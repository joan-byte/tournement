/// <reference types="vite/client" />

declare module '*.vue' {
  import type { ComponentOptions } from 'vue'
  const component: ComponentOptions
  export default component
}

declare module 'vue' {
  interface Ref<T = any> {
    value: T
  }
  export function ref<T>(value: T): Ref<T>
  export function computed<T>(getter: () => T): Ref<T>
  export function onMounted(callback: () => void): void
  export function onUnmounted(callback: () => void): void
  export const createApp: any
}

declare module 'vue-router' {
  export function useRouter(): any
  export function useRoute(): any
  export function createRouter(options: any): any
  export function createWebHistory(base?: string): any
  export interface RouteRecordRaw {
    path: string
    name?: string
    component: any
    children?: RouteRecordRaw[]
  }
}

declare module '@/stores/*' {
  const store: any
  export default store
}

declare module '@/types' {
  export interface Campeonato {
    id: number
    nombre: string
    partida_actual: number
    // ... otros campos
  }

  export interface Pareja {
    id: number
    nombre: string
    club?: string
    activa: boolean
    numero?: number
    campeonato_id: number
    // ... otros campos
  }

  export interface Mesa {
    id: number
    numero: number
    campeonato_id: number
    pareja1_id: number
    pareja2_id?: number
    tieneResultado?: boolean
    pareja1?: Pareja
    pareja2?: Pareja
  }
}

declare module '@/stores/campeonato' {
  export function useCampeonatoStore(): {
    campeonatoActual: Campeonato | null
    campeonatos: Campeonato[]
    getCurrentCampeonato: () => Campeonato | null
    loadCampeonatoActual: () => Promise<Campeonato | null>
    fetchCampeonatos: () => Promise<Campeonato[]>
    createCampeonato: (data: Partial<Campeonato>) => Promise<Campeonato>
    updateCampeonato: (id: number, data: Partial<Campeonato>) => Promise<Campeonato>
    setCampeonatoActual: (campeonato: Campeonato | null) => void
  }
}

declare module '@/stores/pareja' {
  export function useParejaStore(): {
    fetchParejasCampeonato: (id: number) => Promise<Pareja[]>
    createPareja: (data: any) => Promise<Pareja>
    toggleParejaEstado: (id: number, estado: boolean) => Promise<void>
    fetchJugadoresPareja: (id: number) => Promise<any[]>
    updatePareja: (id: number, data: any) => Promise<void>
    deletePareja: (id: number) => Promise<void>
  }
}

declare module '@/stores/mesa' {
  export function useMesaStore(): {
    mesas: Mesa[]
    sortearMesas: (campeonatoId: number) => Promise<any>
    eliminarMesas: (campeonatoId: number) => Promise<any>
    getMesasAsignadas: (campeonatoId: number) => Promise<Mesa[]>
    getMesa: (mesaId: number) => Promise<Mesa>
    cerrarPartida: (campeonatoId: number) => Promise<any>
  }
}

declare module '@/stores/resultado' {
  export function useResultadoStore(): {
    resultados: any[]
    saveResultado: (resultado: any) => Promise<any>
    getResultadoMesa: (mesaId: number, partida: number) => Promise<any>
    fetchResultados: (campeonatoId: number) => Promise<Resultado[]>
  }
}
