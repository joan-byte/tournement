/**
 * Definición de tipos y interfaces relacionadas con las parejas y mesas del campeonato
 */

/**
 * Interface que define la estructura de una Pareja en el campeonato
 * @interface Pareja
 * @property {number} id - Identificador único de la pareja
 * @property {string} nombre - Nombre de la pareja
 * @property {string} [club] - Club al que pertenece la pareja (opcional)
 * @property {boolean} activa - Estado de la pareja (activa/inactiva)
 * @property {number} [numero] - Número asignado a la pareja en el campeonato (opcional)
 * @property {number} campeonato_id - ID del campeonato al que pertenece la pareja
 */
export interface Pareja {
  id: number
  nombre: string
  club?: string
  activa: boolean
  numero?: number
  campeonato_id: number
}

/**
 * Interface que define la estructura básica de una Mesa de juego
 * @interface Mesa
 * @property {number} id - Identificador único de la mesa
 * @property {number} numero - Número de la mesa en el campeonato
 * @property {number} campeonato_id - ID del campeonato al que pertenece la mesa
 * @property {number} partida - Número de la partida actual
 * @property {number} pareja1_id - ID de la primera pareja asignada
 * @property {number} [pareja2_id] - ID de la segunda pareja asignada (opcional)
 * @property {boolean} [tieneResultado] - Indica si la mesa tiene resultado registrado
 * @property {Pareja} [pareja1] - Objeto con los datos de la primera pareja
 * @property {Pareja} [pareja2] - Objeto con los datos de la segunda pareja
 */
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

/**
 * Interface que define la estructura base de un Resultado
 * @interface ResultadoBase
 * @property {number} [id] - Identificador único del resultado
 * @property {number} campeonato_id - ID del campeonato
 * @property {number} partida - Número de la partida
 * @property {number} mesa_id - ID de la mesa donde se jugó
 * @property {number} id_pareja - ID de la pareja a la que pertenece el resultado
 * @property {number} RP - Puntos de resultado
 * @property {number} PG - Partidas ganadas
 * @property {number} PP - Partidas perdidas
 * @property {string} GB - Diferencial de juegos (Game Balance)
 */
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

/**
 * Interface que define la estructura de respuesta de un Resultado
 * @interface ResultadoResponse
 * @property {ResultadoBase} pareja1 - Resultado de la primera pareja
 * @property {ResultadoBase} [pareja2] - Resultado de la segunda pareja (opcional)
 */
export interface ResultadoResponse {
  pareja1: ResultadoBase
  pareja2?: ResultadoBase
}

/**
 * Interface que extiende Mesa para incluir los resultados
 * @interface MesaConResultados
 * @extends Mesa
 * @property {ResultadoResponse} [resultados] - Objeto con los resultados de ambas parejas
 * @property {boolean} tieneResultados - Indica si la mesa tiene resultados registrados
 */
export interface MesaConResultados extends Mesa {
  resultados?: ResultadoResponse
  tieneResultados: boolean
} 