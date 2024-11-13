from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generar __tablename__ automáticamente basado en el nombre de la clase
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> dict:
        """
        Convertir el modelo a un diccionario.
        Sobrescribir en las clases hijas si se necesita una implementación específica.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
