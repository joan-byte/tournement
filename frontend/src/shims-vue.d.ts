/**
 * @file shims-vue.d.ts
 * @description Archivo de declaraciones de tipos para TypeScript
 * @responsibilities
 * - Definir tipos para archivos .vue
 * - Extender tipos de Vue
 * - Declarar tipos para módulos personalizados
 */

// Declaración para archivos .vue
/// <reference types="vite/client" />

/**
 * Declaración del módulo para archivos .vue
 * Permite importar componentes Vue como módulos TypeScript
 */
declare module '*.vue' {
  import type { ComponentOptions } from 'vue'
  const component: ComponentOptions
  export default component
}

/**
 * Extensión del módulo 'vue'
 * Define tipos para características core de Vue
 */
declare module 'vue' {
  // Interfaz para referencias reactivas
  interface Ref<T = any> {
    value: T
  }
  // Funciones fundamentales de Vue
  export function ref<T>(value: T): Ref<T>
  export function computed<T>(getter: () => T): Ref<T>
  export function onMounted(callback: () => void): void
  export function onUnmounted(callback: () => void): void
  export const createApp: any
}

/**
 * Declaración del módulo vue-router
 * Define tipos para funcionalidades del router
 */
declare module 'vue-router' {
  export function useRouter(): any
  export function useRoute(): any
  export function createRouter(options: any): any
  export function createWebHistory(base?: string): any
  // Interfaz para definición de rutas
  export interface RouteRecordRaw {
    path: string
    name?: string
    component: any
    children?: RouteRecordRaw[]
  }
}

/**
 * Declaración para módulos de stores
 * Permite importar stores dinámicamente
 */
declare module '@/stores/*' {
  const store: any
  export default store
}

/**
 * Declaración de tipos personalizados de la aplicación
 * Define interfaces para las entidades principales
 */
declare module '@/types' {
  // Interfaz para la entidad Campeonato
  export interface Campeonato {
    id: number
    nombre: string
    fecha_inicio: string
    dias_duracion: number
    numero_partidas: number
    partida_actual: number
    grupo_b: boolean
  }

  // Interfaz para la entidad Pareja
  export interface Pareja {
    id: number
    nombre: string
    club?: string
    activa: boolean
    numero?: number
    campeonato_id: number
    // ... otros campos
  }

  // Interfaz para la entidad Mesa
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

  // Interfaz para estadísticas de resultados
  export interface ResultadoEstadisticas {
    id: number;                 // ID único del resultado
    pareja_id: number;         // ID de la pareja
    campeonato_id: number;     // ID del campeonato
    puntos_totales: number;    // Total de puntos acumulados
    partidas_ganadas: number;  // Número de partidas ganadas
    partidas_jugadas: number;  // Número total de partidas jugadas
  }
}

/**
 * Declaración del store de campeonato
 * Define tipos para las funciones del store
 */
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

/**
 * Declaración del store de pareja
 * Define tipos para la gestión de parejas
 */
declare module '@/stores/pareja' {
  export function useParejaStore(): {
    fetchParejasCampeonato: (id: number) => Promise<Pareja[]>
    createPareja: (data: any) => Promise<Pareja>
    toggleParejaEstado: (id: number, estado: boolean) => Promise<void>
    fetchJugadoresPareja: (id: number) => Promise<any[]>
    updatePareja: (id: number, data: any) => Promise<void>
    deletePareja: (id: number) => Promise<void>
    fetchParejas: () => Promise<Pareja[]>
  }
}

/**
 * Declaración del store de mesa
 * Define tipos para la gestión de mesas
 */
declare module '@/stores/mesa' {
  export function useMesaStore(): {
    mesas: Mesa[]
    sortearMesas: (campeonatoId: number) => Promise<any>
    eliminarMesas: (campeonatoId: number) => Promise<any>
    getMesasAsignadas: (campeonatoId: number) => Promise<Mesa[]>
    getMesa: (mesaId: number) => Promise<Mesa>
    cerrarPartida: (campeonatoId: number) => Promise<any>
    fetchMesasConResultados: (campeonatoId: number, partidaActual: number) => Promise<MesaConResultados[]>
  }
}

/**
 * Declaración del store de resultado
 * Define tipos para la gestión de resultados
 */
declare module '@/stores/resultado' {
  export function useResultadoStore(): {
    resultados: any[]
    saveResultado: (resultado: any) => Promise<any>
    getResultadoMesa: (mesaId: number, partida: number) => Promise<any>
    fetchResultados: (campeonatoId: number) => Promise<Resultado[]>
  }
}
