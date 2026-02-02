# /app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# --- Creación del Engine de SQLAlchemy (Síncrono) ---
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
)

# --- Fábrica de Sesiones de Base de Datos (Síncrona) ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Creación del Engine de SQLAlchemy (Asíncrono) ---
# Necesario para scripts que usan asyncio o endpoints async de FastAPI
async_engine = create_async_engine(
    str(settings.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://"),
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_OVERFLOW,
)

# --- Fábrica de Sesiones de Base de Datos (Asíncrona) ---
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

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
