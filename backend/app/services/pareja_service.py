from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.pareja import Pareja
from app.models.jugador import Jugador
from app.schemas.pareja import ParejaCreate, ParejaUpdate
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

class ParejaService:
    def __init__(self, db: Session):
        self.db = db

    def get_parejas(
        self,
        skip: int = 0,
        limit: int = 100,
        campeonato_id: int = None
    ) -> List[dict]:
        query = self.db.query(Pareja)
        
        if campeonato_id:
            query = query.filter(Pareja.campeonato_id == campeonato_id)
        
        query = query.order_by(Pareja.numero.desc())
        parejas = query.offset(skip).limit(limit).all()
        
        return [
            {
                "id": p.id,
                "numero": p.numero,
                "nombre": p.nombre,
                "club": p.club,
                "activa": p.activa,
                "campeonato_id": p.campeonato_id
            }
            for p in parejas
        ]

    def get_pareja(self, pareja_id: int) -> Optional[Pareja]:
        return self.db.query(Pareja).filter(Pareja.id == pareja_id).first()

    def create_pareja(self, pareja: ParejaCreate) -> Pareja:
        # Obtener el último número de pareja para este campeonato
        ultimo_numero = self.db.query(Pareja).filter(
            Pareja.campeonato_id == pareja.campeonato_id
        ).order_by(Pareja.numero.desc()).first()

        # Asignar el siguiente número
        nuevo_numero = 1 if not ultimo_numero else ultimo_numero.numero + 1

        # Crear la pareja con el nuevo número
        db_pareja = Pareja(
            nombre=pareja.nombre,
            club=pareja.club,
            campeonato_id=pareja.campeonato_id,
            numero=nuevo_numero  # Asignar el nuevo número
        )
        self.db.add(db_pareja)
        
        try:
            self.db.flush()  # Para obtener el ID de la pareja
            
            # Crear los jugadores
            jugador1 = Jugador(
                nombre=pareja.jugador1.nombre,
                apellido=pareja.jugador1.apellido,
                pareja_id=db_pareja.id,
                campeonato_id=pareja.campeonato_id
            )
            jugador2 = Jugador(
                nombre=pareja.jugador2.nombre,
                apellido=pareja.jugador2.apellido,
                pareja_id=db_pareja.id,
                campeonato_id=pareja.campeonato_id
            )
            
            self.db.add(jugador1)
            self.db.add(jugador2)
            self.db.commit()
            self.db.refresh(db_pareja)
            return db_pareja
            
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error de integridad en la base de datos"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_pareja(self, pareja_id: int, pareja: ParejaUpdate) -> Optional[Pareja]:
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        for key, value in pareja.model_dump(exclude_unset=True).items():
            if key not in ['jugador1', 'jugador2']:
                setattr(db_pareja, key, value)

        try:
            self.db.commit()
            self.db.refresh(db_pareja)
            return db_pareja
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def delete_pareja(self, pareja_id: int) -> bool:
        try:
            # Primero eliminamos los jugadores asociados
            self.db.query(Jugador).filter(Jugador.pareja_id == pareja_id).delete()
            
            # Luego eliminamos la pareja
            result = self.db.query(Pareja).filter(Pareja.id == pareja_id).delete()
            
            self.db.commit()
            return result > 0
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"No se puede eliminar la pareja: {str(e)}"
            )

    def activar_pareja(self, pareja_id: int) -> Optional[Pareja]:
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        db_pareja.activa = True
        self.db.commit()
        self.db.refresh(db_pareja)
        return db_pareja

    def desactivar_pareja(self, pareja_id: int) -> Optional[Pareja]:
        db_pareja = self.get_pareja(pareja_id)
        if not db_pareja:
            return None

        db_pareja.activa = False
        self.db.commit()
        self.db.refresh(db_pareja)
        return db_pareja

    def get_parejas_activas(self, campeonato_id: int) -> List[Pareja]:
        return self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

    def get_parejas_campeonato(self, campeonato_id: int):
        # Obtener las parejas ordenadas por número descendente
        parejas = self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id
        ).order_by(Pareja.numero.desc()).all()
        
        if not parejas:
            return []
        
        return parejas

    def get_pareja_con_jugadores(self, pareja_id: int):
        """
        Obtener una pareja con sus jugadores.
        """
        pareja = self.db.query(Pareja).filter(Pareja.id == pareja_id).first()
        if not pareja:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")
        
        jugadores = self.db.query(Jugador).filter(
            Jugador.pareja_id == pareja_id
        ).order_by(Jugador.id).all()
        
        return {
            "id": pareja.id,
            "numero": pareja.numero,
            "nombre": pareja.nombre,
            "club": pareja.club,
            "activa": pareja.activa,
            "campeonato_id": pareja.campeonato_id,
            "jugadores": [
                {
                    "id": j.id,
                    "nombre": j.nombre,
                    "apellido": j.apellido,
                    "campeonato_id": j.campeonato_id  # Añadir campeonato_id
                }
                for j in jugadores
            ]
        }
  