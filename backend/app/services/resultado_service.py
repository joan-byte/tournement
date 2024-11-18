from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.resultado import Resultado
from app.models.pareja import Pareja
from app.schemas.resultado import ResultadoCreate, ResultadoResponse
from sqlalchemy import func, case
from typing import List, Dict, Any

class ResultadoService:
    def __init__(self, db: Session):
        self.db = db

    def create_resultado(self, resultado: ResultadoCreate) -> ResultadoResponse:
        # Crear resultado para pareja 1
        db_resultado1 = Resultado(
            campeonato_id=resultado.campeonato_id,
            P=resultado.pareja1.P,
            M=resultado.pareja1.M,
            id_pareja=resultado.pareja1.id_pareja,
            RP=resultado.pareja1.RP,
            PG=resultado.pareja1.PG,
            PP=resultado.pareja1.PP,
            GB=resultado.pareja1.GB
        )
        self.db.add(db_resultado1)
        
        db_resultado2 = None
        if resultado.pareja2:
            db_resultado2 = Resultado(
                campeonato_id=resultado.campeonato_id,
                P=resultado.pareja2.P,
                M=resultado.pareja2.M,
                id_pareja=resultado.pareja2.id_pareja,
                RP=resultado.pareja2.RP,
                PG=resultado.pareja2.PG,
                PP=resultado.pareja2.PP,
                GB=resultado.pareja2.GB
            )
            self.db.add(db_resultado2)
        
        try:
            self.db.commit()
            self.db.refresh(db_resultado1)
            if db_resultado2:
                self.db.refresh(db_resultado2)
            
            return ResultadoResponse(
                pareja1=db_resultado1,
                pareja2=db_resultado2
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_resultados(
        self,
        mesa_id: int,
        partida: int,
        campeonato_id: int
    ) -> ResultadoResponse:
        resultados = self.db.query(Resultado).filter(
            Resultado.M == mesa_id,
            Resultado.P == partida,
            Resultado.campeonato_id == campeonato_id
        ).all()
        
        if not resultados:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron resultados para la mesa {mesa_id}, partida {partida}"
            )
        
        return ResultadoResponse(
            pareja1=resultados[0] if resultados else None,
            pareja2=resultados[1] if len(resultados) > 1 else None
        )

    def obtener_ranking(self, campeonato_id: int) -> List[Dict]:
        resultados = self.db.query(
            Resultado.id_pareja,
            Pareja.nombre.label('nombre_pareja'),
            Pareja.club,
            func.sum(Resultado.PG).label('total_PG'),
            func.sum(Resultado.PP).label('total_PP'),
            Resultado.GB
        ).join(
            Pareja, Resultado.id_pareja == Pareja.id
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja,
            Pareja.nombre,
            Pareja.club,
            Resultado.GB
        ).all()

        ranking = [{
            'pareja_id': r.id_pareja,
            'nombre_pareja': r.nombre_pareja,
            'club': r.club,
            'PG': r.total_PG,
            'PP': r.total_PP,
            'GB': r.GB
        } for r in resultados]
        
        return sorted(ranking, key=lambda x: (-x['PG'], x['PP']))

    def ajustar_pg(
        self,
        campeonato_id: int,
        pareja_id: int,
        nuevo_pg: int
    ) -> Dict[str, str]:
        # Obtener el último resultado de la pareja
        resultado = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja_id
        ).order_by(Resultado.P.desc()).first()

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="No se encontró el resultado para ajustar"
            )

        resultado.PG = nuevo_pg
        try:
            self.db.commit()
            return {"message": "PG actualizado correctamente"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def verificar_ultima_partida(
        self,
        campeonato_id: int,
        pareja1_id: int,
        pareja2_id: int
    ) -> Dict[str, Any]:
        # Obtener últimos resultados de ambas parejas
        pareja1 = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja1_id
        ).order_by(Resultado.P.desc()).first()

        pareja2 = self.db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            Resultado.id_pareja == pareja2_id
        ).order_by(Resultado.P.desc()).first()

        if not pareja1 or not pareja2:
            return {
                "debe_jugar": True,
                "razon": None
            }

        # Verificar diferencias de PG y PP
        diferencia_pg = pareja1.PG - pareja2.PG
        diferencia_pp = pareja1.PP - pareja2.PP

        debe_jugar = True
        razon = None

        if diferencia_pg > 1:
            debe_jugar = False
            razon = "Diferencia de PG mayor a 1"
        elif diferencia_pg == 1 and diferencia_pp > 300:
            debe_jugar = False
            razon = "Diferencia de PP mayor a 300 con PG=1"

        return {
            "debe_jugar": debe_jugar,
            "razon": razon,
            "diferencia_pg": diferencia_pg,
            "diferencia_pp": diferencia_pp
        }

    def actualizar_gb(
        self,
        campeonato_id: int,
        pareja_id: int,
        gb: str,
        partida_actual: int
    ) -> Dict[str, str]:
        try:
            # Actualizar GB en resultados actuales y futuros
            self.db.query(Resultado).filter(
                Resultado.campeonato_id == campeonato_id,
                Resultado.id_pareja == pareja_id,
                Resultado.P >= partida_actual
            ).update({"GB": gb})
            
            self.db.commit()
            return {"message": "GB actualizado correctamente"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))