from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from typing import List

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

@router.get("/parejas/{pareja_id}")
def get_pareja(pareja_id: int, db: Session = Depends(get_db)):
    pareja = db.query(Pareja).filter(Pareja.id == pareja_id).first()
    if not pareja:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return pareja 