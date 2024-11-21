/**
 * Archivo de exportación de tipos
 * Centraliza todas las exportaciones de interfaces y tipos del proyecto
 */
export * from './mesa' 
// ... otras interfaces existentes ...

/**
 * Interface que define la estructura de un resultado histórico
 * @interface ResultadoHistorico
 * @property {number} id - Identificador único del resultado histórico
 * @property {string} fecha - Fecha en la que se registró el resultado
 * @property {number} puntuacion - Puntuación obtenida en el resultado
 */
export interface ResultadoHistorico {
  id: number;        // Identificador único del resultado
  fecha: string;     // Fecha del resultado en formato string
  puntuacion: number; // Puntos obtenidos en este resultado
}

/**
 * Interface que define la estructura de un campeonato
 * @interface Campeonato
 * @property {number} id - Identificador único del campeonato
 * @property {string} nombre - Nombre del campeonato
 * @property {string} fecha_inicio - Fecha de inicio del campeonato
 * @property {number} dias_duracion - Días de duración del campeonato
 * @property {number} numero_partidas - Número total de partidas del campeonato
 * @property {number} partida_actual - Partida actual del campeonato
 * @property {boolean} grupo_b - Indica si el campeonato es de grupo B
 */
export interface Campeonato {
  id: number;
  nombre: string;
  fecha_inicio: string;
  dias_duracion: number;
  numero_partidas: number;
  partida_actual: number;
  grupo_b: boolean;
}