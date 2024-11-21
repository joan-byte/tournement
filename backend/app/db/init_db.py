from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    
    Esta función debe ejecutarse cuando se inicia la aplicación por primera vez
    o cuando se necesita recrear todas las tablas.
    
    Note:
        Utiliza el engine global y los modelos registrados en Base.metadata
    """
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    """
    Elimina todas las tablas de la base de datos.
    
    ADVERTENCIA: Esta función es destructiva y eliminará todos los datos.
    Solo debe utilizarse en entornos de desarrollo o testing.
    
    Note:
        Utiliza el engine global y elimina todas las tablas registradas en Base.metadata
    """
    Base.metadata.drop_all(bind=engine)

def get_db():
    """
    Generador de contexto para obtener sesiones de base de datos.
    
    Yields:
        Session: Una sesión de SQLAlchemy activa
    
    Note:
        La sesión se cierra automáticamente al final del contexto,
        incluso si ocurre una excepción
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def check_db_connected() -> bool:
    """
    Verifica si la conexión a la base de datos está funcionando.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    
    Note:
        Ejecuta una consulta simple (SELECT 1) para probar la conexión
        e imprime el error si la conexión falla
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return False

def create_first_superuser() -> None:
    """
    Crea el primer superusuario en la base de datos si no existe.
    
    Esta función:
    1. Verifica si ya existe un superusuario
    2. Si no existe, crea uno nuevo usando las credenciales de configuración
    
    Note:
        - Utiliza las configuraciones FIRST_SUPERUSER y FIRST_SUPERUSER_PASSWORD
        - Maneja automáticamente el hash de la contraseña
        - Imprime mensajes de éxito o error según corresponda
    """
    from app.core.security import get_password_hash
    from app.models.user import User
    
    db = Session(engine)
    try:
        user = db.query(User).filter(User.is_superuser == True).first()
        if not user:
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