# /app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# --- Creación del Engine de SQLAlchemy ---
# Esta es la configuración central para la conexión a la base de datos.
# Usamos los parámetros de pooling definidos en la configuración para
# gestionar las conexiones de manera eficiente.
engine = create_engine(
    str(settings.DATABASE_URL),  # La URL de conexión viene de la configuración
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
)

# --- Fábrica de Sesiones de Base de Datos ---
# SessionLocal es una clase que creará nuevas sesiones de BD cuando sea instanciada.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Dependencia de FastAPI para la Sesión de BD ---
def get_db() -> Session:
    """
    Dependencia de FastAPI que inyecta una sesión de SQLAlchemy en las rutas.
    Asegura que la sesión de la base de datos se cierre correctamente después de cada request.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
