from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoEstadisticas

class EstadisticasService:
    """
    Servicio que maneja el cálculo y procesamiento de estadísticas de las parejas
    en un campeonato. Proporciona métodos para obtener métricas y análisis de rendimiento.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de estadísticas.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_estadisticas_pareja(self, pareja_id: int, campeonato_id: int) -> ResultadoEstadisticas:
        """
        Calcula y devuelve las estadísticas completas de una pareja en un campeonato específico.
        
        Args:
            pareja_id: ID de la pareja a analizar
            campeonato_id: ID del campeonato del que se quieren las estadísticas
        
        Returns:
            ResultadoEstadisticas: Objeto con todas las estadísticas calculadas
            
        Note:
            Si no hay resultados, devuelve un objeto con valores por defecto (0)
        """
        # Obtener todos los resultados de la pareja en el campeonato
        resultados = self.db.query(Resultado).filter(
            Resultado.id_pareja == pareja_id,
            Resultado.campeonato_id == campeonato_id
        ).all()

        # Si no hay resultados, devolver estadísticas con valores por defecto
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

        # Cálculo de estadísticas básicas
        total_partidas = len(resultados)                                    # Total de partidas jugadas
        victorias = sum(1 for r in resultados if r.PG > 0)                 # Número de victorias
        derrotas = total_partidas - victorias                              # Número de derrotas
        promedio_PP = sum(r.PP for r in resultados) / total_partidas      # Promedio de puntos perdidos
        mejor_resultado = max(r.RP for r in resultados)                    # Mejor resultado obtenido
        peor_resultado = min(r.RP for r in resultados)                    # Peor resultado obtenido
        
        # Conteo de resultados por grupo (A y B)
        resultados_por_grupo = {
            'A': sum(1 for r in resultados if r.GB == 'A'),               # Resultados en grupo A
            'B': sum(1 for r in resultados if r.GB == 'B')                # Resultados en grupo B
        }

        # Construcción y retorno del objeto de estadísticas
        return ResultadoEstadisticas(
            total_partidas=total_partidas,
            victorias=victorias,
            derrotas=derrotas,
            promedio_PP=promedio_PP,
            mejor_resultado=mejor_resultado,
            peor_resultado=peor_resultado,
            resultados_por_grupo=resultados_por_grupo
        ) 