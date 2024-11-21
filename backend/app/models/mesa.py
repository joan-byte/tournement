# Importaciones necesarias para el modelo
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Mesa(Base):
    """
    Modelo que representa una mesa de juego en un campeonato.
    Cada mesa representa un enfrentamiento entre dos parejas en una partida específica.
    
    Attributes:
        id (int): Identificador único de la mesa
        numero (int): Número asignado a la mesa en el campeonato
        campeonato_id (int): ID del campeonato al que pertenece la mesa
        partida (int): Número de la partida en la que se juega
        pareja1_id (int): ID de la primera pareja asignada a la mesa
        pareja2_id (int): ID de la segunda pareja asignada a la mesa (puede ser null)
    """
    # Nombre de la tabla en la base de datos
    __tablename__ = "mesas"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)                     # ID único de la mesa
    numero = Column(Integer, nullable=False)                               # Número de mesa en el campeonato
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))         # Referencia al campeonato
    partida = Column(Integer, nullable=False)                             # Número de partida
    pareja1_id = Column(Integer, ForeignKey("parejas.id"))                # Referencia a la primera pareja
    pareja2_id = Column(Integer, ForeignKey("parejas.id"), nullable=True) # Referencia a la segunda pareja (opcional)

    # Relaciones con otros modelos
    campeonato = relationship("Campeonato", back_populates="mesas")       # Relación con el campeonato
    pareja1 = relationship(
        "Pareja", 
        foreign_keys=[pareja1_id], 
        back_populates="mesas_como_pareja1"
    )  # Relación con la primera pareja
    pareja2 = relationship(
        "Pareja", 
        foreign_keys=[pareja2_id], 
        back_populates="mesas_como_pareja2"
    )  # Relación con la segunda pareja
    resultados = relationship("Resultado", back_populates="mesa")         # Relación con los resultados

    def to_dict(self):
        """
        Convierte el objeto Mesa a un diccionario.
        Incluye información básica de la mesa y los nombres de las parejas.
        
        Returns:
            dict: Diccionario con los atributos de la mesa y nombres de parejas
        
        Note:
            Los nombres de las parejas solo se incluyen si las parejas existen
        """
        return {
            "id": self.id,
            "numero": self.numero,
            "campeonato_id": self.campeonato_id,
            "partida": self.partida,
            "pareja1_id": self.pareja1_id,
            "pareja2_id": self.pareja2_id,
            "pareja1_nombre": self.pareja1.nombre if self.pareja1 else None,
            "pareja2_nombre": self.pareja2.nombre if self.pareja2 else None
        }
