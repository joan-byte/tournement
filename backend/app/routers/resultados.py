from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.pareja import Pareja
from app.models.campeonato import Campeonato
from typing import List
from app.schemas.resultado import RankingResultado

router = APIRouter()

@router.get("/ranking/{campeonato_id}", response_model=List[RankingResultado])
def get_ranking(campeonato_id: int, db: Session = Depends(get_db)):
    try:
        # Obtener todas las parejas activas
        parejas = db.query(Pareja).filter(
            Pareja.campeonato_id == campeonato_id,
            Pareja.activa == True
        ).all()

        if not parejas:
            return []

        ranking = []
        for pareja in parejas:
            # Obtener todos los resultados de la pareja en este campeonato
            resultados = db.query(Resultado).filter(
                Resultado.campeonato_id == campeonato_id,
                Resultado.id_pareja == pareja.id
            ).all()

            # Calcular sumatorios
            total_pg = sum(1 for r in resultados if r.PG == 1)
            total_pp = sum(r.PP for r in resultados if r.PP > 0)
            ultima_partida = max([r.partida for r in resultados]) if resultados else 1

            # Crear item del ranking
            ranking_item = RankingResultado(
                posicion=0,  # Se actualizará después
                GB='A',  # Por ahora siempre es A
                PG=total_pg,
                PP=total_pp,
                ultima_partida=ultima_partida,
                numero=pareja.numero,
                nombre=pareja.nombre,
                pareja_id=pareja.id,
                club=pareja.club
            )
            ranking.append(ranking_item)

        # Ordenar según los criterios especificados:
        # 1. GB ascendente
        # 2. PG descendente
        # 3. PP descendente
        ranking.sort(key=lambda x: (
            x.GB,      # GB ascendente
            -x.PG,     # PG descendente
            -x.PP      # PP descendente
        ))

        # Actualizar posiciones después de ordenar
        for idx, item in enumerate(ranking, 1):
            item.posicion = idx

        return ranking

    except Exception as e:
        print(f"Error obteniendo ranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))