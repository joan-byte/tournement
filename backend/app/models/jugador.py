from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Jugador(Base):
    __tablename__ = "jugadores"
    __table_args__ = (
        UniqueConstraint('nombre', 'apellido', 'campeonato_id', name='uq_jugador_campeonato'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    pareja_id = Column(Integer, ForeignKey("parejas.id"))
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))

    pareja = relationship("Pareja", back_populates="jugadores")
    campeonato = relationship("Campeonato", back_populates="jugadores")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "pareja_id": self.pareja_id,
            "campeonato_id": self.campeonato_id
        }

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
