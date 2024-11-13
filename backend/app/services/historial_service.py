from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.schemas.resultado import ResultadoHistorico
from typing import List

class HistorialService:
    def __init__(self, db: Session):
        self.db = db

    def get_historial_pareja(self, pareja_id: int, campeonato_id: int) -> List[ResultadoHistorico]:
        # Obtener todos los resultados de la pareja con información de la mesa y rival
        resultados = (
            self.db.query(
                Resultado,
                Mesa,
                Pareja.nombre.label('rival_nombre'),
                Resultado.RP.label('rival_resultado')
            )
            .join(Mesa, (Mesa.id == Resultado.M) & (Mesa.partida == Resultado.P))
            .outerjoin(
                Pareja,
                case(
                    (Mesa.pareja1_id == pareja_id, Mesa.pareja2_id),
                    else_=Mesa.pareja1_id
                ) == Pareja.id
            )
            .filter(
                Resultado.id_pareja == pareja_id,
                Resultado.campeonato_id == campeonato_id
            )
            .order_by(Resultado.P)
            .all()
        )

        return [
            ResultadoHistorico(
                **resultado[0].to_dict(),
                fecha=resultado[1].fecha_creacion,
                mesa_numero=resultado[1].numero,
                rival_nombre=resultado[2],
                rival_resultado=resultado[3]
            )
            for resultado in resultados
        ] 