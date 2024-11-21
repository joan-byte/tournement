from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

# Definición de tipos genéricos para el CRUD
# ModelType: Tipo del modelo SQLAlchemy
# CreateSchemaType: Esquema Pydantic para crear objetos
# UpdateSchemaType: Esquema Pydantic para actualizar objetos
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Clase base CRUD (Create, Read, Update, Delete) que implementa operaciones básicas de base de datos.
    Utiliza tipos genéricos para poder ser reutilizada con diferentes modelos y esquemas.
    """
    def __init__(self, model: Type[ModelType]):
        """
        Constructor de la clase CRUD.
        Args:
            model: Clase del modelo SQLAlchemy que se utilizará para las operaciones CRUD
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Obtiene un registro por su ID.
        Args:
            db: Sesión de la base de datos
            id: Identificador del registro a buscar
        Returns:
            El objeto encontrado o None si no existe
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Obtiene múltiples registros con paginación.
        Args:
            db: Sesión de la base de datos
            skip: Número de registros a saltar (offset)
            limit: Número máximo de registros a devolver
        Returns:
            Lista de objetos encontrados
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Crea un nuevo registro en la base de datos.
        Args:
            db: Sesión de la base de datos
            obj_in: Datos del objeto a crear (esquema Pydantic)
        Returns:
            El objeto creado
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Actualiza un registro existente.
        Args:
            db: Sesión de la base de datos
            db_obj: Objeto de la base de datos a actualizar
            obj_in: Datos de actualización (esquema Pydantic o diccionario)
        Returns:
            El objeto actualizado
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Elimina un registro de la base de datos.
        Args:
            db: Sesión de la base de datos
            id: Identificador del registro a eliminar
        Returns:
            El objeto eliminado
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
