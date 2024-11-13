from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.jugador import JugadorCreate, JugadorUpdate, JugadorResponse
from app.services.jugador_service import JugadorService

router = APIRouter()

@router.get("/", response_model=List[JugadorResponse])
def get_jugadores(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    campeonato_id: int = None
):
    """
    Obtener lista de jugadores, opcionalmente filtrados por campeonato.
    """
    return JugadorService(db).get_jugadores(
        skip=skip,
        limit=limit,
        campeonato_id=campeonato_id
    )

@router.post("/", response_model=JugadorResponse)
def create_jugador(
    jugador: JugadorCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo jugador.
    """
    return JugadorService(db).create_jugador(jugador)

@router.get("/{jugador_id}", response_model=JugadorResponse)
def get_jugador(
    jugador_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un jugador específico por ID.
    """
    jugador = JugadorService(db).get_jugador(jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.put("/{jugador_id}", response_model=JugadorResponse)
def update_jugador(
    jugador_id: int,
    jugador: JugadorUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un jugador.
    """
    updated = JugadorService(db).update_jugador(jugador_id, jugador)
    if not updated:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated

@router.delete("/{jugador_id}")
def delete_jugador(
    jugador_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un jugador.
    """
    deleted = JugadorService(db).delete_jugador(jugador_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador eliminado"}

@router.get("/pareja/{pareja_id}", response_model=List[JugadorResponse])
def get_jugadores_pareja(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener los jugadores de una pareja específica.
    """
    return JugadorService(db).get_jugadores_pareja(pareja_id)

@router.get("/campeonato/{campeonato_id}", response_model=List[JugadorResponse])
def get_jugadores_campeonato(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los jugadores de un campeonato.
    """
    return JugadorService(db).get_jugadores_campeonato(campeonato_id)
