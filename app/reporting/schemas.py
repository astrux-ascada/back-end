# /app/reporting/schemas.py
"""
Esquemas Pydantic para el módulo de Reporting.
"""
from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class MachineStateDTO(BaseModel):
    """Representa el estado operacional actual de una máquina."""
    asset_id: UUID = Field(..., description="ID único del activo.")
    state: str = Field(..., description="Estado actual (RUNNING, STOPPED, UNKNOWN).")
    
    class Config:
        from_attributes = True

# --- NUEVOS ESQUEMAS PARA REPORTING DE PARADAS ---

class StoppageEventDTO(BaseModel):
    """DTO para un evento de parada individual."""
    start_time: datetime = Field(..., description="Inicio de la parada.")
    end_time: datetime = Field(..., description="Fin de la parada.")
    duration_seconds: float = Field(..., description="Duración de la parada en segundos.")

    class Config:
        from_attributes = True


class StoppageKpisDTO(BaseModel):
    """DTO para los KPIs de paradas de un activo en un período."""
    asset_id: UUID
    total_stoppages: int = Field(..., description="Número total de paradas en el período.")
    total_stoppage_duration_seconds: float = Field(..., description="Suma de la duración de todas las paradas en segundos.")
    availability: float = Field(..., description="Disponibilidad del activo en el período (0.0 a 1.0).")
    mtbf: float | None = Field(None, description="Tiempo Medio Entre Fallos (Mean Time Between Failures) en horas. Null si no hay suficientes datos.")
    stoppage_events: List[StoppageEventDTO] = Field(..., description="Lista de los eventos de parada individuales.")
