# /app/telemetry/schemas.py
"""
Esquemas Pydantic para el módulo de Telemetría.

Define los contratos de datos para la ingesta y consulta de lecturas de sensores.
"""
import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# --- Esquema para una Lectura de Sensor Individual ---

class SensorReadingBase(BaseModel):
    asset_id: uuid.UUID = Field(..., description="ID del activo que genera la lectura.")
    timestamp: datetime = Field(..., description="Timestamp exacto de la medición.")
    metric_name: str = Field(..., example="temperature_celsius")
    value: float = Field(..., example=45.7)

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingRead(SensorReadingBase):
    class Config:
        from_attributes = True


# --- Esquema para Ingesta Masiva (Entrada) ---

class BulkSensorReadingCreate(BaseModel):
    readings: List[SensorReadingCreate]


# --- Esquema para Respuesta de Ingesta Masiva (Salida) ---

class BulkIngestionResponse(BaseModel):
    message: str = Field(..., example="25 lecturas recibidas y encoladas para procesamiento.")
    received_count: int = Field(..., example=25)


# --- DTO para Consultas de Dashboard (Salida) ---

class AggregatedReadingDTO(BaseModel):
    """Representa un punto de datos agregado para un gráfico de series temporales."""
    bucket: datetime = Field(..., description="El inicio del intervalo de tiempo para la agregación.")
    avg_value: float = Field(..., description="El valor promedio de la métrica en el intervalo.")
    min_value: float = Field(..., description="El valor mínimo de la métrica en el intervalo.")
    max_value: float = Field(..., description="El valor máximo de la métrica en el intervalo.")

    class Config:
        from_attributes = True
