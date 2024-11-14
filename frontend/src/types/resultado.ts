export interface RankingResultado {
  id: number;
  pareja_id: number;
  nombre_pareja: string;
  club?: string;
  PG: number;  // Partidas Ganadas
  PP: number;  // Puntos Partida
  GB: string;  // Grupo (A/B)
  posicion?: number;
}

export type Resultado = RankingResultado; 