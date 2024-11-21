# Importaciones necesarias para el servicio de campeonatos
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campeonato import Campeonato
from app.models.resultado import Resultado
from app.schemas.campeonato import CampeonatoCreate, CampeonatoUpdate
from sqlalchemy import func, case
from typing import List, Optional

class CampeonatoService:
    """
    Servicio que maneja todas las operaciones relacionadas con los campeonatos.
    Proporciona una capa de abstracción entre los controladores y la base de datos.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_campeonatos(self, skip: int = 0, limit: int = 100) -> List[Campeonato]:
        """
        Obtiene una lista paginada de campeonatos.
        
        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Número máximo de registros a devolver
        
        Returns:
            Lista de objetos Campeonato
        """
        return self.db.query(Campeonato).offset(skip).limit(limit).all()

    def get_campeonato(self, campeonato_id: int) -> Optional[Campeonato]:
        """
        Obtiene un campeonato específico por su ID.
        
        Args:
            campeonato_id: ID del campeonato a buscar
        
        Returns:
            Objeto Campeonato si existe, None en caso contrario
        """
        return self.db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()

    def create_campeonato(self, campeonato: CampeonatoCreate) -> Campeonato:
        """
        Crea un nuevo campeonato en la base de datos.
        
        Args:
            campeonato: Datos del campeonato a crear
        
        Returns:
            Campeonato creado
            
        Raises:
            HTTPException: Si hay error en la creación
        """
        db_campeonato = Campeonato(**campeonato.model_dump())
        self.db.add(db_campeonato)
        try:
            self.db.commit()
            self.db.refresh(db_campeonato)
            return db_campeonato
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def update_campeonato(self, campeonato_id: int, campeonato: CampeonatoUpdate) -> Optional[Campeonato]:
        """
        Actualiza un campeonato existente.
        
        Args:
            campeonato_id: ID del campeonato a actualizar
            campeonato: Datos actualizados del campeonato
            
        Returns:
            Campeonato actualizado o None si no existe
            
        Raises:
            HTTPException: Si hay error en la actualización
        """
        db_campeonato = self.get_campeonato(campeonato_id)
        if not db_campeonato:
            return None
        
        for key, value in campeonato.model_dump(exclude_unset=True).items():
            setattr(db_campeonato, key, value)
        
        try:
            self.db.commit()
            self.db.refresh(db_campeonato)
            return db_campeonato
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def iniciar_partida(self, campeonato_id: int) -> dict:
        """
        Inicia una nueva partida en el campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Diccionario con mensaje de confirmación y número de partida
            
        Raises:
            HTTPException: Si el campeonato no existe o ya ha finalizado
        """
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual >= campeonato.numero_partidas:
            raise HTTPException(status_code=400, detail="El campeonato ya ha finalizado")
        
        campeonato.partida_actual += 1
        self.db.commit()
        
        return {
            "message": "Partida iniciada correctamente",
            "partida_actual": campeonato.partida_actual
        }

    def finalizar_partida(self, campeonato_id: int) -> dict:
        """
        Finaliza la partida actual del campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Diccionario con mensaje de confirmación y número de partida
            
        Raises:
            HTTPException: Si el campeonato no existe o no hay partida activa
        """
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual == 0:
            raise HTTPException(status_code=400, detail="No hay partida activa")
        
        return {
            "message": "Partida finalizada correctamente",
            "partida_actual": campeonato.partida_actual
        }

    def get_ranking(self, campeonato_id: int) -> List[dict]:
        """
        Obtiene el ranking actual del campeonato.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de diccionarios con las estadísticas de cada pareja,
            ordenada por partidas ganadas y perdidas
        """
        # Obtener los resultados agrupados por pareja
        resultados = self.db.query(
            Resultado.id_pareja,
            func.sum(Resultado.PG).label('total_PG'),
            func.sum(Resultado.PP).label('total_PP'),
            func.max(case(
                (Resultado.GB == 'B', 'B'),
                else_='A'
            )).label('GB')
        ).filter(
            Resultado.campeonato_id == campeonato_id
        ).group_by(
            Resultado.id_pareja
        ).all()

        # Convertir los resultados a diccionarios y ordenarlos
        ranking = [
            {
                'pareja_id': r.id_pareja,
                'PG': r.total_PG,
                'PP': r.total_PP,
                'GB': r.GB
            }
            for r in resultados
        ]
        
        ranking.sort(key=lambda x: (-x['PG'], x['PP']))
        return ranking

    def cerrar_campeonato(self, campeonato_id: int) -> dict:
        """
        Cierra un campeonato una vez finalizado.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Diccionario con mensaje de confirmación
            
        Raises:
            HTTPException: Si el campeonato no existe o no se han completado todas las partidas
        """
        campeonato = self.get_campeonato(campeonato_id)
        if not campeonato:
            raise HTTPException(status_code=404, detail="Campeonato no encontrado")
        
        if campeonato.partida_actual != campeonato.numero_partidas:
            raise HTTPException(
                status_code=400,
                detail="No se puede cerrar el campeonato hasta completar todas las partidas"
            )
        
        return {"message": "Campeonato cerrado correctamente"} 