from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.jugador import Jugador
from app.schemas.jugador import JugadorCreate, JugadorUpdate
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

class JugadorService:
    """
    Servicio que maneja todas las operaciones relacionadas con jugadores.
    Proporciona funcionalidad CRUD y validaciones específicas para jugadores.
    """

    def __init__(self, db: Session):
        """
        Constructor del servicio de jugadores.
        
        Args:
            db: Sesión de SQLAlchemy para interactuar con la base de datos
        """
        self.db = db

    def get_jugadores(
        self,
        skip: int = 0,
        limit: int = 100,
        campeonato_id: Optional[int] = None
    ) -> List[Jugador]:
        """
        Obtiene una lista paginada de jugadores, opcionalmente filtrada por campeonato.
        
        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Número máximo de registros a devolver
            campeonato_id: ID del campeonato para filtrar (opcional)
            
        Returns:
            Lista de objetos Jugador que cumplen los criterios
        """
        query = self.db.query(Jugador)
        if campeonato_id:
            query = query.filter(Jugador.campeonato_id == campeonato_id)
        return query.offset(skip).limit(limit).all()

    def get_jugador(self, jugador_id: int) -> Optional[Jugador]:
        """
        Obtiene un jugador específico por su ID.
        
        Args:
            jugador_id: ID del jugador a buscar
            
        Returns:
            Objeto Jugador si existe, None en caso contrario
        """
        return self.db.query(Jugador).filter(Jugador.id == jugador_id).first()

    def create_jugador(self, jugador: JugadorCreate) -> Jugador:
        """
        Crea un nuevo jugador en la base de datos.
        
        Args:
            jugador: Datos del jugador a crear
            
        Returns:
            Jugador creado
            
        Raises:
            HTTPException: Si ya existe un jugador con el mismo nombre en el campeonato
                         o si hay errores de integridad en la base de datos
        """
        # Verificar si ya existe un jugador con el mismo nombre y apellido en el campeonato
        existing = self.db.query(Jugador).filter(
            Jugador.nombre == jugador.nombre,
            Jugador.apellido == jugador.apellido,
            Jugador.campeonato_id == jugador.campeonato_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un jugador con el nombre {jugador.nombre} {jugador.apellido} en este campeonato"
            )

        db_jugador = Jugador(**jugador.model_dump())
        try:
            self.db.add(db_jugador)
            self.db.commit()
            self.db.refresh(db_jugador)
            return db_jugador
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error de integridad en la base de datos"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update_jugador(self, jugador_id: int, jugador: JugadorUpdate) -> Optional[Jugador]:
        """
        Actualiza los datos de un jugador existente.
        
        Args:
            jugador_id: ID del jugador a actualizar
            jugador: Nuevos datos del jugador
            
        Returns:
            Jugador actualizado o None si no existe
            
        Raises:
            HTTPException: Si ya existe otro jugador con el mismo nombre en el campeonato
                         o si hay errores en la actualización
        """
        db_jugador = self.get_jugador(jugador_id)
        if not db_jugador:
            return None

        # Verificar si el nuevo nombre/apellido ya existe en otro jugador del mismo campeonato
        if jugador.nombre or jugador.apellido:
            existing = self.db.query(Jugador).filter(
                Jugador.id != jugador_id,
                Jugador.campeonato_id == db_jugador.campeonato_id,
                Jugador.nombre == (jugador.nombre or db_jugador.nombre),
                Jugador.apellido == (jugador.apellido or db_jugador.apellido)
            ).first()

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otro jugador con ese nombre y apellido en este campeonato"
                )

        # Actualizar los campos modificados
        for key, value in jugador.model_dump(exclude_unset=True).items():
            setattr(db_jugador, key, value)

        try:
            self.db.commit()
            self.db.refresh(db_jugador)
            return db_jugador
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def delete_jugador(self, jugador_id: int) -> bool:
        """
        Elimina un jugador de la base de datos.
        
        Args:
            jugador_id: ID del jugador a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existe
            
        Raises:
            HTTPException: Si hay errores durante la eliminación
        """
        db_jugador = self.get_jugador(jugador_id)
        if not db_jugador:
            return False

        try:
            self.db.delete(db_jugador)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def get_jugadores_pareja(self, pareja_id: int) -> List[Jugador]:
        """
        Obtiene todos los jugadores asociados a una pareja específica.
        
        Args:
            pareja_id: ID de la pareja
            
        Returns:
            Lista de jugadores que pertenecen a la pareja
        """
        return self.db.query(Jugador).filter(
            Jugador.pareja_id == pareja_id
        ).all()

    def get_jugadores_campeonato(self, campeonato_id: int) -> List[Jugador]:
        """
        Obtiene todos los jugadores participantes en un campeonato específico.
        
        Args:
            campeonato_id: ID del campeonato
            
        Returns:
            Lista de jugadores participantes en el campeonato
        """
        return self.db.query(Jugador).filter(
            Jugador.campeonato_id == campeonato_id
        ).all() 