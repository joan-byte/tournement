from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate, CampeonatoResponse
from app.services.campeonato_service import CampeonatoService

router = APIRouter()

@router.get("/", response_model=List[CampeonatoResponse])
def get_campeonatos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtener lista de campeonatos.
    """
    return CampeonatoService(db).get_campeonatos(skip=skip, limit=limit)

@router.post("/", response_model=CampeonatoResponse)
def create_campeonato(
    campeonato: CampeonatoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo campeonato.
    """
    return CampeonatoService(db).create_campeonato(campeonato)

@router.get("/{campeonato_id}", response_model=CampeonatoResponse)
def get_campeonato(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un campeonato específico por ID.
    """
    campeonato = CampeonatoService(db).get_campeonato(campeonato_id)
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    return campeonato

@router.put("/{campeonato_id}", response_model=CampeonatoResponse)
def update_campeonato(
    campeonato_id: int,
    campeonato: CampeonatoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un campeonato.
    """
    updated = CampeonatoService(db).update_campeonato(campeonato_id, campeonato)
    if not updated:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    return updated

@router.post("/{campeonato_id}/iniciar-partida")
def iniciar_partida(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Iniciar una nueva partida en el campeonato.
    """
    return CampeonatoService(db).iniciar_partida(campeonato_id)

@router.post("/{campeonato_id}/finalizar-partida")
def finalizar_partida(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Finalizar la partida actual del campeonato.
    """
    return CampeonatoService(db).finalizar_partida(campeonato_id)

@router.post("/{campeonato_id}/actualizar-ranking")
def actualizar_ranking(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Actualizar el ranking del campeonato.
    """
    return CampeonatoService(db).actualizar_ranking(campeonato_id)

@router.get("/{campeonato_id}/ranking", response_model=List[dict])
def get_ranking(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener el ranking actual del campeonato.
    """
    return CampeonatoService(db).get_ranking(campeonato_id)

@router.post("/{campeonato_id}/cerrar")
def cerrar_campeonato(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Cerrar un campeonato y generar el ranking final.
    """
    return CampeonatoService(db).cerrar_campeonato(campeonato_id)
