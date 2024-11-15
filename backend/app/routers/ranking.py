from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Resultado, Pareja
from sqlalchemy import func

router = APIRouter()

@router.get("/{campeonato_id}/final")
async def get_ranking_final(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener todas las parejas con sus resultados acumulados
        ranking = db.query(
            Resultado.id_pareja,
            func.sum(Resultado.PG).label('total_PG'),
            func.sum(Resultado.PP).label('total_PP'),
            func.sum(Resultado.RP).label('total_RP')
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja
        ).all()

        # Obtener información de las parejas
        resultados = []
        for r in ranking:
            pareja = db.query(Pareja).filter(Pareja.id == r.id_pareja).first()
            if pareja:
                resultados.append({
                    'id': pareja.id,
                    'numero': pareja.numero,
                    'nombre': pareja.nombre,
                    'club': pareja.club,
                    'PG': int(r.total_PG),
                    'PP': int(r.total_PP),
                    'RP': int(r.total_RP)
                })

        # Ordenar por PG y luego por PP
        resultados.sort(key=lambda x: (x['PG'], x['PP']), reverse=True)
        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 