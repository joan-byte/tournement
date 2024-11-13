from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campeonato import Campeonato
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.models.resultado import Resultado
from typing import List, Dict, Any
import random

class PartidaService:
    def __init__(self, db: Session):
        self.db = db

    def iniciar_partida(self, campeonato_id: int) -> Dict[str, Any]:
        campeonato = self.db.query(Campeonato).filter(
            Campeonato.id == campeonato_id
        ).first()

        if not campeonato:
            raise HTTPException(
                status_code=404,
                detail="Campeonato no encontrado"
            )

        if campeonato.partida_actual >= campeonato.numero_partidas:
            raise HTTPException(
                status_code=400,
                detail="El campeonato ya ha finalizado"
            )

        campeonato.partida_actual += 1

        try:
            self.db.commit()
            return {
                "message": "Partida iniciada correctamente",
                "partida_actual": campeonato.partida_actual
            }
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def finalizar_partida(self, campeonato_id: int) -> Dict[str, Any]:
        campeonato = self.db.query(Campeonato).filter(
            Campeonato.id == campeonato_id
        ).first()

        if not campeonato:
            raise HTTPException(
                status_code=404,
                detail="Campeonato no encontrado"
            )

        if not self.verificar_partida_completa(
            campeonato_id,
            campeonato.partida_actual
        ):
            raise HTTPException(
                status_code=400,
                detail="No se pueden registrar todos los resultados de la partida"
            )

        try:
            self.db.commit()
            return {
                "message": "Partida finalizada correctamente",
                "partida_actual": campeonato.partida_actual
            }
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def verificar_partida_completa(
        self,
        campeonato_id: int,
        partida: int
    ) -> bool:
        # Obtener todas las mesas de la partida
        mesas = self.db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id,
            Mesa.partida == partida
        ).all()

        if not mesas:
            return False

        # Verificar que cada mesa tenga resultados
        for mesa in mesas:
            resultados = self.db.query(Resultado).filter(
                Resultado.campeonato_id == campeonato_id,
                Resultado.P == partida,
                Resultado.M == mesa.id
            ).all()

            # Si es mesa con dos parejas, debe tener dos resultados
            if mesa.pareja2_id and len(resultados) != 2:
                return False
            # Si es mesa con una pareja, debe tener un resultado
            elif not mesa.pareja2_id and len(resultados) != 1:
                return False

        return True

    def get_mesas_asignadas(self, campeonato_id: int) -> List[Dict[str, Any]]:
        campeonato = self.db.query(Campeonato).filter(
            Campeonato.id == campeonato_id
        ).first()

        if not campeonato:
            raise HTTPException(
                status_code=404,
                detail="Campeonato no encontrado"
            )

        mesas = self.db.query(Mesa).filter(
            Mesa.campeonato_id == campeonato_id,
            Mesa.partida == campeonato.partida_actual
        ).all()

        mesas_info = []
        for mesa in mesas:
            pareja1 = self.db.query(Pareja).filter(
                Pareja.id == mesa.pareja1_id
            ).first()
            pareja2 = self.db.query(Pareja).filter(
                Pareja.id == mesa.pareja2_id
            ).first() if mesa.pareja2_id else None

            mesas_info.append({
                "mesa_id": mesa.id,
                "numero": mesa.numero,
                "pareja1": {
                    "id": pareja1.id,
                    "nombre": pareja1.nombre
                } if pareja1 else None,
                "pareja2": {
                    "id": pareja2.id,
                    "nombre": pareja2.nombre
                } if pareja2 else None
            })

        return mesas_info

    def sortear_parejas(self, campeonato_id: int) -> List[Dict[str, Any]]:
        # Obtener parejas activas
        parejas = self.db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if len(parejas) < 2:
            raise HTTPException(
                status_code=400,
                detail="No hay suficientes parejas activas para realizar el sorteo"
            )

        # Mezclar parejas aleatoriamente
        random.shuffle(parejas)

        # Crear mesas y asignar parejas
        mesas_creadas = []
        for i in range(0, len(parejas), 2):
            mesa = Mesa(
                campeonato_id=campeonato_id,
                numero=i//2 + 1,
                pareja1_id=parejas[i].id,
                pareja2_id=parejas[i+1].id if i+1 < len(parejas) else None
            )
            self.db.add(mesa)
            mesas_creadas.append({
                "numero": mesa.numero,
                "pareja1_id": mesa.pareja1_id,
                "pareja2_id": mesa.pareja2_id
            })

        try:
            self.db.commit()
            return mesas_creadas
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e)) 