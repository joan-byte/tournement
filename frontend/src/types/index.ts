// Definición de la interfaz Campeonato
export interface Campeonato {
  id: number
  nombre: string
  fecha_inicio: string
  dias_duracion: number
  numero_partidas: number
  partida_actual: number
  grupo_b: boolean
}

// Resto de interfaces
export interface Pareja {
  id: number
  nombre: string
  club?: string
  activa: boolean
  numero?: number
  campeonato_id: number
}

export interface Mesa {
  id: number
  numero: number
  campeonato_id: number
  partida: number
  pareja1_id: number
  pareja2_id?: number
  tieneResultado?: boolean
  pareja1?: Pareja
  pareja2?: Pareja
}

export interface ResultadoBase {
  id?: number
  campeonato_id: number
  partida: number
  mesa_id: number
  id_pareja: number
  RP: number
  PG: number
  PP: number
  GB: string
}

export interface ResultadoResponse {
  pareja1: ResultadoBase
  pareja2?: ResultadoBase
}

export interface MesaConResultados extends Mesa {
  resultados?: ResultadoResponse
  tieneResultados: boolean
}

export interface Jugador {
  id: number
  nombre: string
  apellido: string
  pareja_id: number
  campeonato_id: number
}

// Asegurarnos de que los tipos se exportan correctamente
declare module '@/types' {
  interface Campeonato {
    id: number
    nombre: string
    fecha_inicio: string
    dias_duracion: number
    numero_partidas: number
    partida_actual: number
    grupo_b: boolean
  }
} 