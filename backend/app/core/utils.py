from typing import List, Dict, Any
from app.core.constants import PORCENTAJE_GRUPO_B, MINIMO_PAREJAS_GRUPO_B
from app.models.pareja import Pareja
from app.models.resultado import Resultado

def calcular_grupos(parejas: List[Pareja]) -> Dict[str, List[Pareja]]:
    """
    Calcula la distribución de parejas en grupos A y B.
    """
    # Ordenar parejas por PG (descendente) y PP (ascendente)
    parejas_ordenadas = sorted(
        parejas,
        key=lambda p: (-sum(r.PG for r in p.resultados), sum(r.PP for r in p.resultados))
    )
    
    total_parejas = len(parejas_ordenadas)
    if total_parejas < MINIMO_PAREJAS_GRUPO_B * 2:
        return {
            'A': parejas_ordenadas,
            'B': []
        }
    
    # Calcular el punto de corte para el grupo B
    corte_grupo_b = int(total_parejas * PORCENTAJE_GRUPO_B)
    
    return {
        'A': parejas_ordenadas[:corte_grupo_b],
        'B': parejas_ordenadas[corte_grupo_b:]
    }

def validar_resultados_mesa(resultado1: Resultado, resultado2: Resultado | None) -> bool:
    """
    Valida que los resultados de una mesa sean correctos.
    """
    # Si solo hay una pareja, su RP debe ser 150
    if resultado2 is None:
        return resultado1.RP == 150
    
    # Los RP no pueden ser iguales
    if resultado1.RP == resultado2.RP:
        return False
    
    # Validar PG y PP
    if resultado1.RP > resultado2.RP:
        return resultado1.PG == 1 and resultado2.PG == 0
    else:
        return resultado1.PG == 0 and resultado2.PG == 1

def generar_nombre_pareja(jugador1_nombre: str, jugador2_nombre: str) -> str:
    """
    Genera el nombre de una pareja a partir de los nombres de sus jugadores.
    """
    return f"{jugador1_nombre} y {jugador2_nombre}" 