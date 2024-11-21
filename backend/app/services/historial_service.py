# Importaciones necesarias para el servicio de historial
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.schemas.resultado import ResultadoHistorico
from typing import List

class HistorialService:
    """
    Servicio que maneja el historial de resultados de las parejas en el campeonato.
    Proporciona funcionalidad para obtener el historial completo de una pareja.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de historial.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_historial_pareja(self, pareja_id: int, campeonato_id: int) -> List[ResultadoHistorico]:
        """
        Obtiene el historial completo de resultados de una pareja en un campeonato específico.
        
        Args:
            pareja_id: ID de la pareja
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de ResultadoHistorico con todos los resultados de la pareja
            
        Note:
            La consulta incluye:
            - Información de la mesa donde jugó
            - Nombre del rival
            - Resultado del rival
            Los resultados se ordenan por número de partida
        """
        # Consulta compleja que obtiene todos los resultados de la pareja
        # junto con la información de la mesa y el rival
        resultados = (
            self.db.query(
                Resultado,                                    # Resultado principal
                Mesa,                                        # Información de la mesa
                Pareja.nombre.label('rival_nombre'),         # Nombre del rival
                Resultado.RP.label('rival_resultado')        # Puntos del rival
            )
            .join(Mesa, (Mesa.id == Resultado.M) & (Mesa.partida == Resultado.P))  # Join con mesa
            .outerjoin(                                      # Join con pareja rival
                Pareja,
                case(
                    (Mesa.pareja1_id == pareja_id, Mesa.pareja2_id),  # Si es pareja1, buscar pareja2
                    else_=Mesa.pareja1_id                              # Si no, buscar pareja1
                ) == Pareja.id
            )
            .filter(                                         # Filtros de búsqueda
                Resultado.id_pareja == pareja_id,
                Resultado.campeonato_id == campeonato_id
            )
            .order_by(Resultado.P)                          # Ordenar por número de partida
            .all()
        )

        # Transformar los resultados al formato de respuesta esperado
        return [
            ResultadoHistorico(
                **resultado[0].to_dict(),                    # Datos del resultado principal
                fecha=resultado[1].fecha_creacion,           # Fecha de la mesa
                mesa_numero=resultado[1].numero,             # Número de mesa
                rival_nombre=resultado[2],                   # Nombre del rival
                rival_resultado=resultado[3]                 # Resultado del rival
            )
            for resultado in resultados
        ] 