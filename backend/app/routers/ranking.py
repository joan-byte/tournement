# Importaciones necesarias para el manejo del ranking
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Resultado, Pareja
from sqlalchemy import func

# Creación del enrutador para las rutas relacionadas con el ranking
router = APIRouter()

@router.get("/{campeonato_id}/final")
async def get_ranking_final(campeonato_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el ranking final del campeonato con todas las estadísticas acumuladas.
    
    Args:
        campeonato_id: ID del campeonato del cual se quiere obtener el ranking
        db: Sesión de la base de datos (inyectada automáticamente)
    
    Returns:
        Lista ordenada de parejas con sus estadísticas finales, ordenada por PG y PP
    
    Raises:
        HTTPException: Si ocurre un error al procesar la solicitud
    """
    try:
        # Obtener todas las parejas con sus resultados acumulados
        # Utilizamos func.sum para calcular los totales de cada estadística
        ranking = db.query(
            Resultado.id_pareja,
            func.sum(Resultado.PG).label('total_PG'),    # Total de partidas ganadas
            func.sum(Resultado.PP).label('total_PP'),    # Total de puntos perdidos
            func.sum(Resultado.RP).label('total_RP')     # Total de resultados parciales
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja
        ).all()

        # Obtener información de las parejas y construir el resultado final
        resultados = []
        for r in ranking:
            # Buscar la información de la pareja correspondiente
            pareja = db.query(Pareja).filter(Pareja.id == r.id_pareja).first()
            if pareja:
                # Construir el diccionario con toda la información necesaria
                resultados.append({
                    'id': pareja.id,
                    'numero': pareja.numero,
                    'nombre': pareja.nombre,
                    'club': pareja.club,
                    'PG': int(r.total_PG),      # Convertir a entero para asegurar el tipo
                    'PP': int(r.total_PP),
                    'RP': int(r.total_RP)
                })

        # Ordenar el ranking por PG (descendente) y PP (descendente)
        # Esto asegura que las parejas con más partidas ganadas aparezcan primero
        # y en caso de empate, se ordenen por puntos perdidos
        resultados.sort(key=lambda x: (x['PG'], x['PP']), reverse=True)
        return resultados

    except Exception as e:
        # Capturar cualquier error y devolver una respuesta apropiada
        raise HTTPException(status_code=500, detail=str(e)) 