# Importaciones necesarias para la clase base
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Decorador que marca esta clase como la clase base declarativa para SQLAlchemy
@as_declarative()
class Base:
    """
    Clase base abstracta para todos los modelos SQLAlchemy de la aplicación.
    Proporciona funcionalidad común que heredarán todos los modelos.
    
    Atributos:
        id: Identificador único para cada modelo (implementado en las clases hijas)
        __name__: Nombre de la clase del modelo
    """
    id: Any
    __name__: str

    # Método que genera automáticamente el nombre de la tabla en la base de datos
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Genera el nombre de la tabla en la base de datos automáticamente
        basándose en el nombre de la clase en minúsculas.
        
        Returns:
            str: Nombre de la tabla generado automáticamente
        
        Ejemplo:
            Clase 'Usuario' -> tabla 'usuario'
            Clase 'OrdenCompra' -> tabla 'ordencompra'
        """
        return cls.__name__.lower()

    def to_dict(self) -> dict:
        """
        Convierte una instancia del modelo a un diccionario.
        Útil para serialización y API responses.
        
        Returns:
            dict: Diccionario con los campos del modelo y sus valores
        
        Note:
            Este método puede ser sobrescrito en las clases hijas si se necesita
            una implementación específica de serialización.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
