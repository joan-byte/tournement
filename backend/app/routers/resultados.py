from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from typing import Optional, Dict, Any

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
        print(f"Error en get_resultado_mesa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/")
async def save_resultado(data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        # Validar datos requeridos
        if not all(key in data for key in ['mesa_id', 'campeonato_id', 'partida', 'resultados']):
            raise HTTPException(status_code=400, detail="Faltan campos requeridos")

        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == data['mesa_id']).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Eliminar resultados previos si existen
        db.query(Resultado).filter(
            Resultado.mesa_id == data['mesa_id'],
            Resultado.partida == data['partida']
        ).delete()

        # Obtener los RP de ambas parejas
        rp1 = data['resultados']['pareja1']['RP']
        rp2 = data['resultados']['pareja2']['RP'] if data['resultados'].get('pareja2') else 0

        # Calcular PP para cada pareja (diferencia entre su RP y el RP contrario)
        pp1 = rp1 - rp2
        pp2 = rp2 - rp1 if data['resultados'].get('pareja2') else 0

        # Guardar resultado de pareja 1
        resultado1 = Resultado(
            mesa_id=data['mesa_id'],
            campeonato_id=data['campeonato_id'],
            partida=data['partida'],
            id_pareja=data['resultados']['pareja1']['id_pareja'],
            GB='A',  # Por ahora siempre es 'A'
            RP=rp1,
            PP=pp1  # El PG se calculará automáticamente en el modelo
        )
        db.add(resultado1)

        # Guardar resultado de pareja 2 si existe
        if data['resultados'].get('pareja2'):
            resultado2 = Resultado(
                mesa_id=data['mesa_id'],
                campeonato_id=data['campeonato_id'],
                partida=data['partida'],
                id_pareja=data['resultados']['pareja2']['id_pareja'],
                GB='A',  # Por ahora siempre es 'A'
                RP=rp2,
                PP=pp2  # El PG se calculará automáticamente en el modelo
            )
            db.add(resultado2)

        db.commit()
        return {"message": "Resultados guardados correctamente"}

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error guardando resultado: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error guardando resultado: {str(e)}")