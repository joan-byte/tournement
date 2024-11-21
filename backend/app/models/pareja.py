from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Pareja(Base):
    """
    Modelo que representa una pareja de jugadores en un campeonato.
    Gestiona la información y relaciones de las parejas participantes.
    
    Attributes:
        id (int): Identificador único de la pareja
        nombre (str): Nombre de la pareja (generalmente combinación de nombres de jugadores)
        club (str): Club al que pertenece la pareja (opcional)
        activa (bool): Estado de la pareja en el campeonato
        numero (int): Número asignado a la pareja en el campeonato
        campeonato_id (int): ID del campeonato al que pertenece
    """
    __tablename__ = "parejas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    club = Column(String, nullable=True)
    activa = Column(Boolean, default=True)
    numero = Column(Integer)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))

    jugadores = relationship("Jugador", back_populates="pareja")
    campeonato = relationship("Campeonato", back_populates="parejas")
    mesas_como_pareja1 = relationship("Mesa", foreign_keys="Mesa.pareja1_id", back_populates="pareja1")
    mesas_como_pareja2 = relationship("Mesa", foreign_keys="Mesa.pareja2_id", back_populates="pareja2")
    resultados = relationship("Resultado", back_populates="pareja")

    def __repr__(self):
        """
        Representación en string del objeto Pareja.
        
        Returns:
            str: Representación legible de la pareja
        
        Example:
            <Pareja Juan Pérez y María García>
        """
        return f"<Pareja {self.nombre}>"
