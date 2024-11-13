from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.pareja import ParejaCreate, ParejaUpdate, ParejaResponse
from app.services.pareja_service import ParejaService

router = APIRouter()

@router.get("/", response_model=List[ParejaResponse])
def get_parejas(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    campeonato_id: int = None
):
    """
    Obtener lista de parejas, opcionalmente filtradas por campeonato.
    """
    return ParejaService(db).get_parejas(
        skip=skip,
        limit=limit,
        campeonato_id=campeonato_id
    )

@router.post("/", response_model=ParejaResponse)
def create_pareja(
    pareja: ParejaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva pareja.
    """
    return ParejaService(db).create_pareja(pareja)

@router.get("/{pareja_id}", response_model=ParejaResponse)
def get_pareja(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una pareja específica por ID.
    """
    pareja = ParejaService(db).get_pareja(pareja_id)
    if not pareja:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return pareja

@router.put("/{pareja_id}", response_model=ParejaResponse)
def update_pareja(
    pareja_id: int,
    pareja: ParejaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una pareja.
    """
    updated = ParejaService(db).update_pareja(pareja_id, pareja)
    if not updated:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return updated

@router.delete("/{pareja_id}")
def delete_pareja(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una pareja y sus jugadores asociados.
    """
    try:
        deleted = ParejaService(db).delete_pareja(pareja_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Pareja no encontrada")
        return {"message": "Pareja eliminada correctamente"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al eliminar la pareja: {str(e)}"
        )

@router.post("/{pareja_id}/activar")
def activar_pareja(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Activar una pareja.
    """
    activated = ParejaService(db).activar_pareja(pareja_id)
    if not activated:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return activated

@router.post("/{pareja_id}/desactivar")
def desactivar_pareja(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Desactivar una pareja.
    """
    deactivated = ParejaService(db).desactivar_pareja(pareja_id)
    if not deactivated:
        raise HTTPException(status_code=404, detail="Pareja no encontrada")
    return deactivated

@router.get("/campeonato/{campeonato_id}/activas", response_model=List[ParejaResponse])
def get_parejas_activas(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener parejas activas de un campeonato.
    """
    return ParejaService(db).get_parejas_activas(campeonato_id)

@router.get("/{pareja_id}/jugadores", response_model=ParejaResponse)
def get_pareja_con_jugadores(
    pareja_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una pareja con sus jugadores.
    """
    return ParejaService(db).get_pareja_con_jugadores(pareja_id)
