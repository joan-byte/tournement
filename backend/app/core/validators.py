from datetime import date
from typing import List
from app.core.constants import (
    VALIDACIONES,
    MINIMO_PAREJAS_TORNEO,
    MAXIMO_PAREJAS_POR_MESA
)
from app.core.exceptions import ValidationError
from app.models.pareja import Pareja
from app.models.resultado import Resultado

def validar_nombre(nombre: str) -> None:
    if len(nombre) < VALIDACIONES["NOMBRE_MIN_LENGTH"]:
        raise ValidationError(
            f"El nombre debe tener al menos {VALIDACIONES['NOMBRE_MIN_LENGTH']} caracteres"
        )
    if len(nombre) > VALIDACIONES["NOMBRE_MAX_LENGTH"]:
        raise ValidationError(
            f"El nombre no puede tener más de {VALIDACIONES['NOMBRE_MAX_LENGTH']} caracteres"
        )

def validar_club(club: str) -> None:
    if len(club) > VALIDACIONES["CLUB_MAX_LENGTH"]:
        raise ValidationError(
            f"El nombre del club no puede tener más de {VALIDACIONES['CLUB_MAX_LENGTH']} caracteres"
        )

def validar_fecha_inicio(fecha: date) -> None:
    if fecha < date.today():
        raise ValidationError("La fecha de inicio no puede ser anterior a hoy")

def validar_dias_duracion(dias: int) -> None:
    if dias < VALIDACIONES["MIN_DIAS"]:
        raise ValidationError(
            f"El campeonato debe durar al menos {VALIDACIONES['MIN_DIAS']} día"
        )
    if dias > VALIDACIONES["MAX_DIAS"]:
        raise ValidationError(
            f"El campeonato no puede durar más de {VALIDACIONES['MAX_DIAS']} días"
        )

def validar_numero_partidas(partidas: int) -> None:
    if partidas < VALIDACIONES["MIN_PARTIDAS"]:
        raise ValidationError(
            f"El campeonato debe tener al menos {VALIDACIONES['MIN_PARTIDAS']} partida"
        )
    if partidas > VALIDACIONES["MAX_PARTIDAS"]:
        raise ValidationError(
            f"El campeonato no puede tener más de {VALIDACIONES['MAX_PARTIDAS']} partidas"
        )

def validar_parejas_suficientes(parejas: List[Pareja]) -> None:
    if len(parejas) < MINIMO_PAREJAS_TORNEO:
        raise ValidationError(
            f"Se necesitan al menos {MINIMO_PAREJAS_TORNEO} parejas para iniciar el campeonato"
        )

def validar_parejas_por_mesa(parejas: List[Pareja]) -> None:
    if len(parejas) > MAXIMO_PAREJAS_POR_MESA:
        raise ValidationError(
            f"No pueden haber más de {MAXIMO_PAREJAS_POR_MESA} parejas por mesa"
        )

def validar_resultados_mesa(resultado1: Resultado, resultado2: Resultado | None) -> None:
    # Si solo hay una pareja, su RP debe ser 150
    if resultado2 is None:
        if resultado1.RP != 150:
            raise ValidationError(
                "En una mesa con una sola pareja, el RP debe ser 150"
            )
        return

    # Los RP no pueden ser iguales
    if resultado1.RP == resultado2.RP:
        raise ValidationError("Los resultados parciales no pueden ser iguales")

    # Validar PG y PP
    if resultado1.RP > resultado2.RP:
        if resultado1.PG != 1 or resultado2.PG != 0:
            raise ValidationError("Los puntos ganados no coinciden con los resultados")
    else:
        if resultado1.PG != 0 or resultado2.PG != 1:
            raise ValidationError("Los puntos ganados no coinciden con los resultados") 