from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Jugador(Base):
    """
    Modelo que representa un jugador en la base de datos.
    Hereda de Base para obtener funcionalidad común de SQLAlchemy.
    
    Attributes:
        id (int): Identificador único del jugador
        nombre (str): Nombre del jugador
        apellido (str): Apellido del jugador
        pareja_id (int): ID de la pareja a la que pertenece el jugador
        campeonato_id (int): ID del campeonato en el que participa
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = "jugadores"
    
    # Restricciones de la tabla
    __table_args__ = (
        # Asegura que no haya dos jugadores con el mismo nombre y apellido en un campeonato
        UniqueConstraint('nombre', 'apellido', 'campeonato_id', name='uq_jugador_campeonato'),
        {'extend_existing': True}
    )

    # Definición de columnas
    id = Column(Integer, primary_key=True, index=True)                     # ID único del jugador
    nombre = Column(String, index=True)                                    # Nombre del jugador (indexado para búsquedas)
    apellido = Column(String, index=True)                                 # Apellido del jugador (indexado para búsquedas)
    pareja_id = Column(Integer, ForeignKey("parejas.id"))                # Referencia a la tabla parejas
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))        # Referencia a la tabla campeonatos

    # Relaciones con otros modelos
    pareja = relationship("Pareja", back_populates="jugadores")          # Relación bidireccional con Pareja
    campeonato = relationship("Campeonato", back_populates="jugadores")  # Relación bidireccional con Campeonato

    def to_dict(self):
        """
        Convierte el objeto Jugador a un diccionario.
        Útil para serialización y respuestas API.
        
        Returns:
            dict: Diccionario con los atributos del jugador
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "pareja_id": self.pareja_id,
            "campeonato_id": self.campeonato_id
        }

    @property
    def nombre_completo(self):
        """
        Propiedad que devuelve el nombre completo del jugador.
        
        Returns:
            str: Nombre y apellido del jugador concatenados
        
        Example:
            Si nombre="Juan" y apellido="Pérez", retorna "Juan Pérez"
        """
        return f"{self.nombre} {self.apellido}"
