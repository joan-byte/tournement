from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoEstadisticas

class EstadisticasService:
    def __init__(self, db: Session):
        self.db = db

    def get_estadisticas_pareja(self, pareja_id: int, campeonato_id: int) -> ResultadoEstadisticas:
        # Obtener todos los resultados de la pareja
        resultados = self.db.query(Resultado).filter(
            Resultado.id_pareja == pareja_id,
            Resultado.campeonato_id == campeonato_id
        ).all()

        if not resultados:
            return ResultadoEstadisticas(
                total_partidas=0,
                victorias=0,
                derrotas=0,
                promedio_PP=0.0,
                mejor_resultado=0,
                peor_resultado=0,
                resultados_por_grupo={'A': 0, 'B': 0}
            )

        # Calcular estadísticas
        total_partidas = len(resultados)
        victorias = sum(1 for r in resultados if r.PG > 0)
        derrotas = total_partidas - victorias
        promedio_PP = sum(r.PP for r in resultados) / total_partidas if total_partidas > 0 else 0
        mejor_resultado = max(r.RP for r in resultados)
        peor_resultado = min(r.RP for r in resultados)
        
        # Contar resultados por grupo
        resultados_por_grupo = {
            'A': sum(1 for r in resultados if r.GB == 'A'),
            'B': sum(1 for r in resultados if r.GB == 'B')
        }

        return ResultadoEstadisticas(
            total_partidas=total_partidas,
            victorias=victorias,
            derrotas=derrotas,
            promedio_PP=promedio_PP,
            mejor_resultado=mejor_resultado,
            peor_resultado=peor_resultado,
            resultados_por_grupo=resultados_por_grupo
        ) 