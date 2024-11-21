from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Resultado(Base):
    """
    Modelo que representa el resultado de una partida en un campeonato.
    Almacena información sobre el desempeño de una pareja en una partida específica.
    
    Attributes:
        id (int): Identificador único del resultado
        campeonato_id (int): ID del campeonato al que pertenece el resultado
        mesa_id (int): ID de la mesa donde se jugó la partida
        partida (int): Número de la partida
        id_pareja (int): ID de la pareja que jugó la partida
        GB (str): Información sobre el grupo B (si aplica)
        PG (int): Partidas ganadas
        PP (int): Partidas perdidas
        RP (int): Resultados de puntos
    """
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    partida = Column(Integer)
    id_pareja = Column(Integer, ForeignKey("parejas.id"))
    GB = Column(String)
    PG = Column(Integer)
    PP = Column(Integer)
    RP = Column(Integer)

    # Relaciones
    campeonato = relationship("Campeonato", back_populates="resultados")
    mesa = relationship("Mesa", back_populates="resultados")
    pareja = relationship("Pareja", back_populates="resultados")

    def to_dict(self):
        """
        Convierte el objeto Resultado a un diccionario.
        Útil para serialización y respuestas API.
        
        Returns:
            dict: Diccionario con los atributos del resultado
        """
        return {
            "id": self.id,
            "campeonato_id": self.campeonato_id,
            "mesa_id": self.mesa_id,
            "partida": self.partida,
            "id_pareja": self.id_pareja,
            "GB": self.GB,
            "PG": self.PG,
            "PP": self.PP,
            "RP": self.RP
        }

@event.listens_for(Resultado, 'before_insert')
@event.listens_for(Resultado, 'before_update')
def calcular_campos(mapper, connection, target):
    """
    Calcula y actualiza campos específicos antes de insertar o actualizar un resultado.
    
    Args:
        mapper: El mapeador de SQLAlchemy
        connection: La conexión de la base de datos
        target: La instancia de Resultado que se está procesando
    
    Note:
        - Establece PG a 1 si PP es mayor que 0, de lo contrario a 0
        - Este cálculo se realiza automáticamente antes de guardar el resultado
    """
    target.PG = 1 if target.PP > 0 else 0
