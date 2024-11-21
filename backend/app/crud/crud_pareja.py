from sqlalchemy.orm import Session
from app.models.jugador import Jugador
from app.models.pareja import Pareja
from app.schemas.jugador import ParejaCreate, ParejaUpdate

def get_pareja(db: Session, pareja_id: int):
    """
    Obtiene una pareja específica por su ID.
    Args:
        db: Sesión de la base de datos
        pareja_id: Identificador único de la pareja
    Returns:
        Objeto Pareja si existe, None en caso contrario
    """
    return db.query(Pareja).filter(Pareja.id == pareja_id).first()

def get_parejas(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista paginada de parejas.
    Args:
        db: Sesión de la base de datos
        skip: Número de registros a saltar (para paginación)
        limit: Número máximo de registros a devolver
    Returns:
        Lista de objetos Pareja
    """
    return db.query(Pareja).offset(skip).limit(limit).all()

def create_pareja(db: Session, pareja: ParejaCreate) -> Pareja:
    """
    Crea una nueva pareja en la base de datos.
    
    El proceso incluye:
    1. Obtener los datos de ambos jugadores
    2. Generar un nombre compuesto para la pareja
    3. Crear y persistir el nuevo registro de pareja
    
    Args:
        db: Sesión de la base de datos
        pareja: Esquema Pydantic con los datos de la pareja a crear
    
    Returns:
        Objeto Pareja creado y persistido en la base de datos
    
    Note:
        El nombre de la pareja se genera automáticamente combinando
        los nombres y apellidos de ambos jugadores
    """
    # Obtener los jugadores
    jugador1 = db.query(Jugador).filter(Jugador.id == pareja.jugador1_id).first()
    jugador2 = db.query(Jugador).filter(Jugador.id == pareja.jugador2_id).first()
    
    # Generar el nombre de la pareja
    nombre_pareja = f"{jugador1.nombre} {jugador1.apellido} y {jugador2.nombre} {jugador2.apellido}"
    
    # Crear la pareja
    db_pareja = Pareja(
        jugador1_id=pareja.jugador1_id,
        jugador2_id=pareja.jugador2_id,
        club=pareja.club,
        activa=pareja.activa,
        campeonato_id=pareja.campeonato_id,
        nombre=nombre_pareja
    )
    
    db.add(db_pareja)
    db.commit()
    db.refresh(db_pareja)
    return db_pareja
