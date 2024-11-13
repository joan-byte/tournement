from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campeonato import Campeonato
from app.models.resultado import Resultado
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate
from sqlalchemy import func, case
from typing import List, Optional

class CampeonatoService:
    def __init__(self, db: Session):
        self.db = db

    def get_campeonatos(self, skip: int = 0, limit: int = 100) -> List[Campeonato]:
        return self.db.query(Campeonato).offset(skip).limit(limit).all()

    def get_campeonato(self, campeonato_id: int) -> Optional[Campeonato]:
        return self.db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()

    def create_campeonato(self, campeonato: CampeonatoCreate) -> Campeonato:
        db_campeonato = Campeonato(**campeonato.model_dump())
        self.db.add(db_campeonato)
        try:
            self.db.commit()
            self.db.refresh(db_campeonato)
            return db_campeonato
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def update_campeonato(self, campeonato_id: int, campeonato: CampeonatoUpdate) -> Optional[Campeonato]:
        db_campeonato = self.get_campeonato(campeonato_id)
        if not db_campeonato:
            return None
        
        for key, value in campeonato.model_dump(exclude_unset=True).items():
            setattr(db_campeonato, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_campeonato)
            return db_campeonato
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def iniciar_partida(self, campeonato_id: int) -> dict:
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual >= campeonato.numero_partidas:
            raise HTTPException(status_code=400, detail="El campeonato ya ha finalizado")
        
        campeonato.partida_actual += 1
        self.db.commit()
        
        return {
            "message": "Partida iniciada correctamente",
            "partida_actual": campeonato.partida_actual
        }

    def finalizar_partida(self, campeonato_id: int) -> dict:
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual == 0:
            raise HTTPException(status_code=400, detail="No hay partida activa")
        
        # Aquí podrías agregar lógica adicional para verificar que todos los resultados están registrados
        
        return {
            "message": "Partida finalizada correctamente",
            "partida_actual": campeonato.partida_actual
        }

    def get_ranking(self, campeonato_id: int) -> List[dict]:
        # Obtener los resultados agrupados por pareja
        resultados = self.db.query(
            Resultado.id_pareja,
            func.sum(Resultado.PG).label('total_PG'),
            func.sum(Resultado.PP).label('total_PP'),
            func.max(case(
                (Resultado.GB == 'B', 'B'),
                else_='A'
            )).label('GB')
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja
        ).all()

        # Convertir los resultados a diccionarios y ordenarlos
        ranking = [
            {
                'pareja_id': r.id_pareja,
                'PG': r.total_PG,
                'PP': r.total_PP,
                'GB': r.GB
            }
            for r in resultados
        ]
        
        # Ordenar por PG (descendente) y PP (ascendente)
        ranking.sort(key=lambda x: (-x['PG'], x['PP']))
        
        return ranking

    def cerrar_campeonato(self, campeonato_id: int) -> dict:
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual != campeonato.numero_partidas:
            raise HTTPException(
                status_code=400,
                detail="No se puede cerrar el campeonato hasta completar todas las partidas"
            )
        
        # Aquí podrías agregar lógica para guardar el ranking final
        
        return {"message": "Campeonato cerrado correctamente"} 