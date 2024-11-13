from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.session import get_db
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from typing import List
from app.schemas.jugador import JugadorCreate, ParejaCreate, JugadorResponse, ParejaUpdate
from sqlalchemy import func

router = APIRouter()

@router.get("/jugadores")
def get_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()

@router.get("/jugadores/{jugador_id}")
def get_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.get("/parejas")
def get_parejas(db: Session = Depends(get_db)):
    return db.query(Pareja).all()

@router.get("/parejas/campeonato/{campeonato_id}")
def get_parejas_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    parejas = db.query(Pareja).filter(
        Pareja.campeonato_id == campeonato_id
    ).order_by(Pareja.numero.desc()).all()
    
    if not parejas:
        return []
    
    return parejas

@router.get("/parejas/{pareja_id}")
def get_pareja(pareja_id: int, db: Session = Depends(get_db)):
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if not pareja:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return pareja

@router.get("/parejas/{pareja_id}/jugadores")
def get_jugadores_pareja(pareja_id: int, db: Session = Depends(get_db)):
    # Obtener la pareja con sus jugadores
    pareja = db.query(Pareja).options(
        joinedload(Pareja.jugadores)
    ).filter(Pareja.id == pareja_id).first()
    
    if not pareja:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    
    # Ordenar los jugadores por ID para mantener consistencia
    jugadores = sorted(pareja.jugadores, key=lambda x: x.id)
    
    if not jugadores:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores para esta pareja")
    
    # Asegurarnos de que devolvemos exactamente dos jugadores
    if len(jugadores) != 2:
        raise HTTPException(
            status_code=500, 
            detail="La pareja debe tener exactamente dos jugadores"
        )
    
    # Devolver los jugadores en el formato esperado por el frontend
    return [
        {
            "id": jugador.id,
            "nombre": jugador.nombre,
            "apellido": jugador.apellido,
            "pareja_id": jugador.pareja_id,
            "campeonato_id": jugador.campeonato_id
        }
        for jugador in jugadores
    ]

@router.post("/parejas")
async def create_pareja(pareja_data: ParejaCreate, db: Session = Depends(get_db)):
    try:
        # Obtener el último número de pareja para este campeonato
        ultimo_numero = db.query(func.max(Pareja.numero))\
            .filter(Pareja.campeonato_id == pareja_data.campeonato_id)\
            .scalar()
        
        # Si no hay parejas, empezar desde 1, si no, incrementar el último número
        nuevo_numero = 1 if ultimo_numero is None else ultimo_numero + 1

        # Crear la pareja con el nuevo número
        nueva_pareja = Pareja(
            nombre=f"{pareja_data.jugador1.nombre} {pareja_data.jugador1.apellido} Y {pareja_data.jugador2.nombre} {pareja_data.jugador2.apellido}",
            club=pareja_data.club,
            activa=True,
            campeonato_id=pareja_data.campeonato_id,
            numero=nuevo_numero  # Asignar el número correlativo
        )
        db.add(nueva_pareja)
        db.flush()  # Para obtener el ID de la pareja

        # Crear los jugadores
        jugador1 = Jugador(
            nombre=pareja_data.jugador1.nombre,
            apellido=pareja_data.jugador1.apellido,
            pareja_id=nueva_pareja.id,
            campeonato_id=pareja_data.campeonato_id
        )
        jugador2 = Jugador(
            nombre=pareja_data.jugador2.nombre,
            apellido=pareja_data.jugador2.apellido,
            pareja_id=nueva_pareja.id,
            campeonato_id=pareja_data.campeonato_id
        )

        db.add(jugador1)
        db.add(jugador2)
        db.commit()
        db.refresh(nueva_pareja)
        
        return nueva_pareja
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 

@router.put("/parejas/{pareja_id}")
async def update_pareja(
    pareja_id: int,
    pareja_data: ParejaUpdate,
    db: Session = Depends(get_db)
):
    try:
        # Obtener la pareja con sus jugadores
        pareja = db.query(Pareja).options(
            joinedload(Pareja.jugadores)
        ).filter(Pareja.id == pareja_id).first()
        
        if not pareja:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")

        # Actualizar datos básicos de la pareja
        if pareja_data.club is not None:
            pareja.club = pareja_data.club
        if pareja_data.activa is not None:
            pareja.activa = pareja_data.activa

        # Actualizar jugadores si se proporcionan datos
        jugadores = sorted(pareja.jugadores, key=lambda x: x.id)
        
        if pareja_data.jugador1 and jugadores:
            jugadores[0].nombre = pareja_data.jugador1.nombre
            jugadores[0].apellido = pareja_data.jugador1.apellido

        if pareja_data.jugador2 and len(jugadores) > 1:
            jugadores[1].nombre = pareja_data.jugador2.nombre
            jugadores[1].apellido = pareja_data.jugador2.apellido

        # Actualizar el nombre de la pareja
        if pareja_data.jugador1 or pareja_data.jugador2:
            pareja.nombre = f"{jugadores[0].nombre} {jugadores[0].apellido} Y {jugadores[1].nombre} {jugadores[1].apellido}"

        try:
            db.commit()
            db.refresh(pareja)
            return {
                **pareja.__dict__,
                "jugadores": [j.to_dict() for j in jugadores]
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error al actualizar la base de datos: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 

@router.delete("/parejas/{pareja_id}")
async def delete_pareja(pareja_id: int, db: Session = Depends(get_db)):
    try:
        # Primero, obtener la pareja y sus jugadores
        pareja = db.query(Pareja).options(
            joinedload(Pareja.jugadores)
        ).filter(Pareja.id == pareja_id).first()
        
        if not pareja:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")

        # Eliminar primero los jugadores asociados
        for jugador in pareja.jugadores:
            db.delete(jugador)

        # Luego eliminar la pareja
        db.delete(pareja)
        db.commit()
        
        return {"message": "Pareja eliminada correctamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) 