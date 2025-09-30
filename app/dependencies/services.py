# /app/dependencies/services.py
"""
Dependency Injection for the services of Astruxa's modules.

This file defines a "getter" function for each business service.
FastAPI uses these functions to inject service instances into the API endpoints,
managing the database session and other dependencies.
"""

import redis
from fastapi import Depends
from sqlalchemy.orm import Session

# --- Import core dependency getters ---
from app.core.database import get_db
from app.core.redis import get_redis_client

# --- Import services from Astruxa's modules ---
from app.identity.auth_service import AuthService
from app.assets.service import AssetService
from app.telemetry.service import TelemetryService
from app.procurement.service import ProcurementService
from app.maintenance.service import MaintenanceService
from app.core_engine.service import CoreEngineService
from app.sectors.service import SectorService


# --- Service Injectors for Astruxa Modules ---

def get_auth_service(db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis_client)) -> AuthService:
    """Provides an instance of the AuthService with its dependencies."""
    return AuthService(db=db, redis_client=redis_client)

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    """Provides an instance of the AssetService."""
    return AssetService(db)

def get_telemetry_service(db: Session = Depends(get_db)) -> TelemetryService:
    """Provides an instance of the TelemetryService."""
    return TelemetryService(db)

def get_procurement_service(db: Session = Depends(get_db)) -> ProcurementService:
    """Provides an instance of the ProcurementService."""
    return ProcurementService(db)

def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceService:
    """Provides an instance of the MaintenanceService."""
    return MaintenanceService(db)

def get_core_engine_service(db: Session = Depends(get_db)) -> CoreEngineService:
    """
    Provides an instance of the CoreEngineService for the API.
    Note: The runtime service with all its dependencies is initialized
    in the application's lifespan (main.py).
    """
    # For API endpoints, we only need CRUD functionality,
    # which doesn't require the telemetry_service.
    return CoreEngineService(db, telemetry_service=None)

def get_sector_service(db: Session = Depends(get_db)) -> SectorService:
    """Provides an instance of the SectorService."""
    return SectorService(db)
