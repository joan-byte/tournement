export * from './resultado';

export interface Campeonato {
  id: number;
  nombre: string;
  partida_actual: number;
}

export interface Pareja {
  id: number;
  nombre: string;
  club?: string;
  activa: boolean;
  numero?: number;
  campeonato_id: number;
}

export interface Mesa {
  id: number;
  numero: number;
  pareja1_id: number;
  pareja2_id?: number;
  campeonato_id: number;
}

export interface ResultadoBase {
  id?: number;
  campeonato_id: number;
  partida: number;
  mesa_id: number;
  id_pareja: number;
  RP: number; // Resultado Partida
  PG: number; // Partidas Ganadas
  PP: number; // Puntos Partida
  GB: string; // Grupo (A/B)
}

export interface ResultadoResponse {
  pareja1: ResultadoBase;
  pareja2?: ResultadoBase;
}

export interface MesaConResultados extends Mesa {
  resultados?: ResultadoResponse;
  tieneResultados: boolean;
}

export interface Jugador {
  id: number;
  nombre: string;
  apellido: string;
  pareja_id: number;
  campeonato_id: number;
} 