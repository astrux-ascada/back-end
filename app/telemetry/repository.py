# /app/telemetry/repository.py
"""
Capa de Repositorio para el módulo de Telemetría.

Optimizado para la inserción masiva de datos de series temporales.
"""

from typing import List
from sqlalchemy.orm import Session

from app.telemetry import models, schemas


class TelemetryRepository:
    """Realiza operaciones CRUD en la base de datos para la telemetría."""

    def __init__(self, db: Session):
        self.db = db

    def create_bulk_readings(self, readings_in: List[schemas.SensorReadingCreate]) -> int:
        """
        Inserta una lista de lecturas de sensores en la base de datos de forma masiva.

        Este es el método preferido para la ingesta de telemetría por su alto rendimiento.

        Args:
            readings_in: Una lista de esquemas Pydantic con los datos de las lecturas.

        Returns:
            El número de registros insertados.
        """
        # Convierte la lista de esquemas Pydantic a una lista de diccionarios.
        db_readings_data = [r.model_dump() for r in readings_in]

        # Crea las instancias del modelo SQLAlchemy.
        db_objects = [models.SensorReading(**data) for data in db_readings_data]

        # Añade todos los objetos a la sesión en una sola operación.
        self.db.add_all(db_objects)
        self.db.commit()

        return len(db_objects)
