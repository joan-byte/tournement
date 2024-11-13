from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.mesa import MesaCreate, MesaResponse, MesaConParejas
from app.services.mesa_service import MesaService

router = APIRouter()

@router.get("/campeonato/{campeonato_id}", response_model=List[MesaResponse])
def get_mesas_campeonato(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las mesas de un campeonato.
    """
    return MesaService(db).get_mesas_campeonato(campeonato_id)

@router.post("/crear", response_model=List[MesaResponse])
def crear_mesas(
    campeonato_id: int,
    partida: int,
    db: Session = Depends(get_db)
):
    """
    Crear mesas para una nueva partida.
    """
    return MesaService(db).crear_mesas(campeonato_id, partida)

@router.get("/resultados/{campeonato_id}/{partida}", response_model=List[MesaConParejas])
def get_mesas_con_resultados(
    campeonato_id: int,
    partida: int,
    db: Session = Depends(get_db)
):
    """
    Obtener mesas con sus resultados para una partida específica.
    """
    return MesaService(db).get_mesas_con_resultados(campeonato_id, partida)

@router.get("/{mesa_id}", response_model=MesaResponse)
def get_mesa(
    mesa_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una mesa específica por ID.
    """
    mesa = MesaService(db).get_mesa(mesa_id)
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return mesa

@router.post("/asignar-parejas/{mesa_id}")
def asignar_parejas_mesa(
    mesa_id: int,
    pareja1_id: int,
    pareja2_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Asignar parejas a una mesa.
    """
    return MesaService(db).asignar_parejas(mesa_id, pareja1_id, pareja2_id)

@router.get("/verificar-resultados/{mesa_id}")
def verificar_resultados_mesa(
    mesa_id: int,
    partida: int,
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Verificar si una mesa ya tiene resultados registrados.
    """
    return {
        "tiene_resultados": MesaService(db).verificar_resultados(
            mesa_id, partida, campeonato_id
        )
    }

@router.post("/sortear/{campeonato_id}")
def sortear_mesas(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Realizar el sorteo inicial de mesas para un campeonato.
    """
    try:
        return MesaService(db).sortear_mesas(campeonato_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/campeonato/{campeonato_id}")
def eliminar_mesas(
    campeonato_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar todas las mesas de un campeonato.
    """
    try:
        MesaService(db).eliminar_mesas(campeonato_id)
        return {"message": "Mesas eliminadas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
