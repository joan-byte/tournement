from enum import Enum

class GrupoJuego(str, Enum):
    A = "A"
    B = "B"

class EstadoPartida(str, Enum):
    NO_INICIADA = "no_iniciada"
    EN_CURSO = "en_curso"
    FINALIZADA = "finalizada"

class EstadoCampeonato(str, Enum):
    INSCRIPCION = "inscripcion"
    ACTIVO = "activo"
    FINALIZADO = "finalizado"

# Configuración del juego
PUNTOS_VICTORIA_MESA_LIBRE = 150
PUNTOS_MINIMOS_DIFERENCIA = 1
DIFERENCIA_PP_MAXIMA = 300
MINIMO_PAREJAS_TORNEO = 4
MAXIMO_PAREJAS_POR_MESA = 2

# Configuración de grupos
PORCENTAJE_GRUPO_B = 0.5  # 50% de las parejas van al grupo B
MINIMO_PAREJAS_GRUPO_B = 4

# Mensajes de error comunes
ERRORES = {
    "CAMPEONATO_NO_ENCONTRADO": "Campeonato no encontrado",
    "PAREJA_NO_ENCONTRADA": "Pareja no encontrada",
    "MESA_NO_ENCONTRADA": "Mesa no encontrada",
    "RESULTADO_NO_ENCONTRADO": "Resultado no encontrado",
    "PAREJAS_INSUFICIENTES": "No hay suficientes parejas para iniciar el campeonato",
    "PARTIDA_NO_INICIADA": "La partida no ha sido iniciada",
    "PARTIDA_YA_FINALIZADA": "La partida ya ha sido finalizada",
    "RESULTADOS_INCOMPLETOS": "Faltan resultados por registrar",
    "ERROR_INTEGRIDAD": "Error de integridad en la base de datos",
}

# Configuración de validaciones
VALIDACIONES = {
    "NOMBRE_MIN_LENGTH": 3,
    "NOMBRE_MAX_LENGTH": 100,
    "CLUB_MAX_LENGTH": 50,
    "MIN_PARTIDAS": 1,
    "MAX_PARTIDAS": 50,
    "MIN_DIAS": 1,
    "MAX_DIAS": 30,
} 