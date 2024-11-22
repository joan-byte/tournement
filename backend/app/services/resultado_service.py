from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.resultado import Resultado
from app.models.pareja import Pareja
from app.schemas.resultado import ResultadoCreate, ResultadoResponse
from sqlalchemy import func, case
from typing import List, Dict, Any

class ResultadoService:
    """
    Servicio que maneja todas las operaciones relacionadas con los resultados de las partidas.
    Proporciona funcionalidad para crear, consultar y gestionar resultados de las parejas.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de resultados.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def create_resultado(self, resultado: ResultadoCreate) -> ResultadoResponse:
        """
        Crea nuevos resultados para una partida.
        
        Args:
            resultado: Datos de los resultados a crear (pareja1 y opcionalmente pareja2)
            
        Returns:
            ResultadoResponse con los resultados creados
            
        Raises:
            HTTPException: Si hay error en la creación de los resultados
            
        Note:
            Crea resultados para ambas parejas si es una mesa completa,
            o solo para pareja1 si es mesa libre
        """
        try:
            # Crear resultado para pareja 1
            db_resultado1 = Resultado(
                campeonato_id=resultado.campeonato_id,
                partida=resultado.partida,
                mesa_id=resultado.mesa_id,
                id_pareja=resultado.pareja1.id,
                RP=resultado.pareja1.RP,
                PG=resultado.pareja1.PG,
                PP=resultado.pareja1.PP,  # Este PP ya viene con el signo correcto
                GB=resultado.pareja1.GB
            )
            self.db.add(db_resultado1)
            
            db_resultado2 = None
            # Crear resultado para pareja 2 si existe
            if resultado.pareja2:
                db_resultado2 = Resultado(
                    campeonato_id=resultado.campeonato_id,
                    partida=resultado.partida,
                    mesa_id=resultado.mesa_id,
                    id_pareja=resultado.pareja2.id,
                    RP=resultado.pareja2.RP,
                    PG=resultado.pareja2.PG,
                    PP=resultado.pareja2.PP,  # Este PP ya viene con el signo correcto
                    GB=resultado.pareja2.GB
                )
                self.db.add(db_resultado2)
            
            try:
                self.db.commit()
                self.db.refresh(db_resultado1)
                if db_resultado2:
                    self.db.refresh(db_resultado2)
                
                return ResultadoResponse(
                    pareja1=db_resultado1,
                    pareja2=db_resultado2
                )
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=str(e))

        except Exception as e:
            logger.error(f"Error al crear resultado: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_resultados(
        self,
        mesa_id: int,
        partida: int,
        campeonato_id: int
    ) -> ResultadoResponse:
        """
        Obtiene los resultados de una mesa específica en una partida.
        
        Args:
            mesa_id: ID de la mesa
            partida: Número de la partida
            campeonato_id: ID del campeonato
            
        Returns:
            ResultadoResponse con los resultados de ambas parejas
            
        Raises:
            HTTPException: Si no se encuentran resultados
        """
        # Buscar resultados que coincidan con los criterios
        resultados = self.db.query(Resultado).filter(
            Resultado.M == mesa_id,
            Resultado.P == partida,
            Resultado.campeonato_id == campeonato_id
        ).all()
        
        if not resultados:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron resultados para la mesa {mesa_id}, partida {partida}"
            )
        
        return ResultadoResponse(
            pareja1=resultados[0] if resultados else None,
            pareja2=resultados[1] if len(resultados) > 1 else None
        )

    def obtener_ranking(self, campeonato_id: int) -> List[Dict]:
        """
        Obtiene el ranking actual del campeonato.
        """
        try:
            # Subconsulta para obtener la última partida de cada pareja
            ultima_partida_subquery = (
                self.db.query(
                    Resultado.id_pareja,
                    func.max(Resultado.partida).label('ultima_partida')
                )
                .filter(Resultado.campeonato_id == campeonato_id)
                .group_by(Resultado.id_pareja)
                .subquery()
            )

            # Consulta principal
            resultados = self.db.query(
                Resultado.id_pareja,
                Pareja.nombre.label('nombre_pareja'),
                Pareja.club,
                Pareja.numero,
                func.sum(Resultado.PG).label('PG'),
                # Obtener el PP de la última partida
                func.first_value(Resultado.PP).over(
                    partition_by=Resultado.id_pareja,
                    order_by=Resultado.partida.desc()
                ).label('PP'),
                Resultado.GB,
                ultima_partida_subquery.c.ultima_partida
            ).join(
                Pareja, Resultado.id_pareja == Pareja.id
            ).join(
                ultima_partida_subquery,
                Resultado.id_pareja == ultima_partida_subquery.c.id_pareja
            ).filter(
                Resultado.campeonato_id == campeonato_id
            ).group_by(
                Resultado.id_pareja,
                Pareja.nombre,
                Pareja.club,
                Pareja.numero,
                Resultado.PP,
                Resultado.GB,
                ultima_partida_subquery.c.ultima_partida,
                Resultado.partida
            ).all()

            # Convertir resultados a formato de respuesta
            ranking = []
            for r in resultados:
                ranking.append({
                    'pareja_id': r.id_pareja,
                    'nombre_pareja': r.nombre_pareja,
                    'club': r.club,
                    'numero': r.numero,
                    'PG': r.PG or 0,
                    'PP': r.PP,  # PP de la última partida
                    'GB': r.GB,
                    'ultima_partida': r.ultima_partida
                })

            # Ordenar según los criterios especificados
            return sorted(
                ranking,
                key=lambda x: (
                    x['GB'],                # 1. GB ascendente (A antes que B)
                    -(x['PG'] or 0),        # 2. Suma de PG descendente
                    -(x['PP'] or 0)         # 3. PP descendente
                )
            )

        except Exception as e:
            logger.error(f"Error al obtener ranking: {str(e)}")
            raise

    def actualizar_gb(
        self,
        campeonato_id: int,
        pareja_id: int,
        gb: str,
        partida_actual: int
    ) -> Dict[str, str]:
        """
        Actualiza el grupo (GB) de una pareja para las partidas actuales y futuras.
        
        Args:
            campeonato_id: ID del campeonato
            pareja_id: ID de la pareja
            gb: Nuevo valor de GB ('A' o 'B')
            partida_actual: Número de partida actual
            
        Returns:
            Mensaje de confirmación
            
        Raises:
            HTTPException: Si hay error en la actualización
        """
        try:
            # Actualizar GB en resultados actuales y futuros
            self.db.query(Resultado).filter(
                Resultado.campeonato_id == campeonato_id,
                Resultado.id_pareja == pareja_id,
                Resultado.P >= partida_actual
            ).update({"GB": gb})
            
            self.db.commit()
            return {"message": "GB actualizado correctamente"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))