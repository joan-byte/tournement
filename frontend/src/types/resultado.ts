/**
 * Definición de tipos e interfaces relacionadas con los resultados del ranking
 */

/**
 * Interface que define la estructura de un resultado en el ranking
 * @interface RankingResultado
 */
export interface RankingResultado {
  id: number;            // Identificador único del resultado
  pareja_id: number;     // Identificador de la pareja
  nombre_pareja: string; // Nombre de la pareja participante
  club?: string;         // Club al que pertenece la pareja (opcional)
  PG: number;           // Partidas Ganadas en el campeonato
  PP: number;           // Puntos Partida acumulados
  GB: string;           // Grupo (A/B) al que pertenece la pareja
  posicion?: number;     // Posición en el ranking (opcional)
}

/**
 * Tipo que representa un resultado genérico
 * Actualmente es un alias de RankingResultado
 * @typedef {RankingResultado} Resultado
 */
export type Resultado = RankingResultado; 