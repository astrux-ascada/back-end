# /app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Crea el motor de SQLAlchemy usando la URL de la base de datos desde la configuración
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

# Crea una clase SessionLocal que será la fábrica de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
