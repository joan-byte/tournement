from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

def init_db() -> None:
    """
    Inicializar la base de datos creando todas las tablas.
    """
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    """
    Eliminar todas las tablas de la base de datos.
    Solo usar en desarrollo/testing.
    """
    Base.metadata.drop_all(bind=engine)

def get_db():
    """
    Generador de sesiones de base de datos.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def check_db_connected() -> bool:
    """
    Verificar si la conexión a la base de datos está funcionando.
    """
    try:
        # Intentar ejecutar una consulta simple
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False

def create_first_superuser() -> None:
    """
    Crear el primer superusuario si no existe.
    """
    from app.core.security import get_password_hash
    from app.models.user import User
    
    db = Session(engine)
    try:
        # Verificar si ya existe un superusuario
        user = db.query(User).filter(User.is_superuser == True).first()
        if not user:
            # Crear superusuario
            superuser = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
                is_active=True
            )
            db.add(superuser)
            db.commit()
            print("Superusuario creado exitosamente")
    except Exception as e:
        print(f"Error creando superusuario: {e}")
    finally:
        db.close() 