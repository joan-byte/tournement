export interface Campeonato {
  id: number;
  nombre: string;
  fecha_inicio: string;
  dias_duracion: number;
  numero_partidas: number;
  grupo_b: boolean;
  partida_actual: number;
}

export interface Pareja {
  id: number;
  numero: number;
  nombre: string;
  club?: string;
  activa: boolean;
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
  P: number;  // Partida
  M: number;  // Mesa
  id_pareja: number;
  RP: number; // Resultado Parcial
  PG: number; // Puntos Ganados
  PP: number; // Puntos Perdidos
  GB: string; // Grupo (A/B)
}

export interface Resultado extends ResultadoBase {
  pareja_id: number;
  nombre_pareja: string;
  club?: string;
}

export interface ResultadoResponse {
  pareja1: ResultadoBase;
  pareja2?: ResultadoBase;
}

export interface MesaConResultados extends Mesa {
  resultados?: ResultadoResponse;
  tieneResultados: boolean;
}

// Nuevas interfaces para estadísticas e historial
export interface ResultadoEstadisticas {
  total_partidas: number;
  victorias: number;
  derrotas: number;
  promedio_PP: number;
  mejor_resultado: number;
  peor_resultado: number;
  resultados_por_grupo: Record<string, number>;  // {'A': count, 'B': count}
}

export interface ResultadoHistorico extends ResultadoBase {
  fecha: string;
  mesa_numero: number;
  rival_nombre: string | null;
  rival_resultado: number | null;
}

export interface RankingFinal {
  pareja_id: number;
  nombre_pareja: string;
  club?: string;
  PG_total: number;
  PP_total: number;
  GB_final: string;
  posicion_final: number;
  premio?: string;
} 