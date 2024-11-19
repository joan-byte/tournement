from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.resultado import Resultado
from app.models.mesa import Mesa
from app.models.pareja import Pareja
from app.models.campeonato import Campeonato
from typing import List, Dict, Any
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

        # Obtener solo los resultados con valores reales (no iniciales)
        resultados = db.query(Resultado).filter(
            Resultado.campeonato_id == campeonato_id,
            # Asegurarse de que al menos uno de los valores sea diferente de 0
            (Resultado.PG != 0) | (Resultado.PP != 0) | (Resultado.RP != 0)
        ).all()

        # Si no hay resultados reales, devolver lista vacía
        if not resultados:
            return []

        ranking = []
        for pareja in parejas:
            # Filtrar resultados de esta pareja
            resultados_pareja = [r for r in resultados if r.id_pareja == pareja.id]
            
            if resultados_pareja:  # Solo incluir parejas con resultados reales
                # Calcular sumatorios
                total_pg = sum(1 for r in resultados_pareja if r.PG == 1)
                total_pp = sum(r.PP for r in resultados_pareja if r.PP > 0)
                ultima_partida = max([r.partida for r in resultados_pareja])

                # Crear item del ranking
                ranking_item = RankingResultado(
                    posicion=0,
                    GB='A',
                    PG=total_pg,
                    PP=total_pp,
                    ultima_partida=ultima_partida,
                    numero=pareja.numero,
                    nombre=pareja.nombre,
                    pareja_id=pareja.id,
                    club=pareja.club
                )
                ranking.append(ranking_item)

        # Ordenar según los criterios
        ranking.sort(key=lambda x: (x.GB, -x.PG, -x.PP))

        # Actualizar posiciones
        for idx, item in enumerate(ranking, 1):
            item.posicion = idx

        return ranking

    except Exception as e:
        print(f"Error obteniendo ranking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mesa_id}/{partida}")
def get_resultado_mesa(mesa_id: int, partida: int, db: Session = Depends(get_db)):
    try:
        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Obtener resultados
        resultados = db.query(Resultado).filter(
            Resultado.mesa_id == mesa_id,
            Resultado.partida == partida
        ).all()
        
        if not resultados:
            return None
            
        # Formatear la respuesta
        response = {
            "pareja1": next((r.to_dict() for r in resultados if r.id_pareja == mesa.pareja1_id), None),
            "pareja2": next((r.to_dict() for r in resultados if r.id_pareja == mesa.pareja2_id), None) if mesa.pareja2_id else None
        }
        
        return response
            
    except Exception as e:
        print(f"Error en get_resultado_mesa: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def save_resultado(data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        # Validar datos requeridos
        if not all(key in data for key in ['mesa_id', 'campeonato_id', 'pareja1']):
            raise HTTPException(status_code=400, detail="Faltan campos requeridos")

        # Verificar que la mesa existe
        mesa = db.query(Mesa).filter(Mesa.id == data['mesa_id']).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")

        # Obtener el campeonato para la partida actual
        campeonato = db.query(Campeonato).filter(
            Campeonato.id == data['campeonato_id']
        ).first()
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")

        # Eliminar resultados previos si existen
        db.query(Resultado).filter(
            Resultado.mesa_id == data['mesa_id'],
            Resultado.partida == campeonato.partida_actual
        ).delete()

        # Guardar resultado de pareja 1
        resultado1 = Resultado(
            mesa_id=data['mesa_id'],
            campeonato_id=data['campeonato_id'],
            partida=campeonato.partida_actual,
            id_pareja=mesa.pareja1_id,
            GB='A',
            RP=data['pareja1']['RP'],
            PP=data['pareja1']['PP'],
            PG=data['pareja1']['PG']
        )
        db.add(resultado1)

        # Solo guardar resultado de pareja 2 si existe en la mesa y en los datos
        if mesa.pareja2_id and 'pareja2' in data:
            resultado2 = Resultado(
                mesa_id=data['mesa_id'],
                campeonato_id=data['campeonato_id'],
                partida=campeonato.partida_actual,
                id_pareja=mesa.pareja2_id,
                GB='A',
                RP=data['pareja2']['RP'],
                PP=data['pareja2']['PP'],
                PG=data['pareja2']['PG']
            )
            db.add(resultado2)

        db.commit()
        return {"message": "Resultados guardados correctamente"}

    except Exception as e:
        db.rollback()
        print(f"Error guardando resultado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))