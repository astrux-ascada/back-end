# /app/dependencies/services.py
"""
Dependency Injection para los servicios de los módulos de Astruxa.

Este archivo define una función "getter" para cada servicio de negocio.
FastAPI usa estas funciones para inyectar instancias de los servicios
en los endpoints de la API, gestionando la sesión de la base de datos.
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

# --- Importar los servicios de los nuevos módulos de Astruxa ---
from app.identity.auth_service import AuthService
from app.assets.service import AssetService
from app.telemetry.service import TelemetryService
from app.procurement.service import ProcurementService
from app.maintenance.service import MaintenanceService
from app.core_engine.service import CoreEngineService


# --- Inyectores para Módulos de Astruxa ---

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Proporciona una instancia del AuthService."""
    return AuthService(db)

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    """Proporciona una instancia del AssetService."""
    return AssetService(db)

def get_telemetry_service(db: Session = Depends(get_db)) -> TelemetryService:
    """Proporciona una instancia del TelemetryService."""
    return TelemetryService(db)

def get_procurement_service(db: Session = Depends(get_db)) -> ProcurementService:
    """Proporciona una instancia del ProcurementService."""
    return ProcurementService(db)

def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceService:
    """Proporciona una instancia del MaintenanceService."""
    return MaintenanceService(db)

def get_core_engine_service(db: Session = Depends(get_db)) -> CoreEngineService:
    """
    Proporciona una instancia del CoreEngineService para la API.
    Nota: El servicio de runtime con todas sus dependencias se inicializa
    en el ciclo de vida de la aplicación (main.py).
    """
    # Para los endpoints de la API, solo necesitamos la funcionalidad CRUD,
    # que no requiere el telemetry_service.
    # El telemetry_service se inyecta manualmente en main.py para el servicio de fondo.
    return CoreEngineService(db, telemetry_service=None)
