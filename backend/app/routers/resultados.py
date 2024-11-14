from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from typing import Optional

router = APIRouter()

@router.get("/")
def get_resultados(db: Session = Depends(get_db)):
    return db.query(Resultado).all()

@router.get("/{mesa_id}/{partida}")
def get_resultado_mesa(
    mesa_id: int,
    partida: int,
    db: Session = Depends(get_db)
):
    try:
        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        if partida < 1:
            raise HTTPException(
                status_code=400, 
                detail="El número de partida debe ser mayor que 0"
            )
            
        resultados = db.query(Resultado).filter(
            Resultado.mesa_id == mesa_id,
            Resultado.partida == partida
        ).all()
        
        if not resultados:
            return None
            
        # Formatear la respuesta
        response = {
            "pareja1": next((r for r in resultados if r.id_pareja == mesa.pareja1_id), None),
            "pareja2": next((r for r in resultados if r.id_pareja == mesa.pareja2_id), None) if mesa.pareja2_id else None
        }
        
        return response
            
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error en get_resultado_mesa: {str(e)}")  # Log para depuración
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/")
async def save_resultado(resultado: dict, db: Session = Depends(get_db)):
    try:
        # Implementar la lógica de guardado
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 