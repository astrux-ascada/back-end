"""
Módulo de agregación para los routers de la API v1.
"""

from fastapi import APIRouter

# --- Routers de Módulos de Astruxa ---
from app.identity import api as identity_api
from app.assets import api as assets_api
from app.telemetry import api as telemetry_api
from app.procurement import api as procurement_api
from app.maintenance import api as maintenance_api
from app.core_engine import api as core_engine_api

# --- Routers antiguos (se irán eliminando) ---
from . import (
    address,
    addiction,
    allergy,
    analytics,
    client,
    contact,
    dicom,
    disease,
    emerg_data,
    files,
    health,
    infectious_disease,
    medical_codes,
    medical_history,
    menstrual_cycle,
    panic,
    pregnancy,
    psychiatric_condition,
    public_profile,
    push_notifications,
    vital_sign,
)

api_router = APIRouter(prefix="/api/v1")

# --- REGISTRO DE ROUTERS NUEVOS ---
api_router.include_router(identity_api.router, prefix="/auth")
api_router.include_router(assets_api.router) # El prefijo "/assets" ya está en el router
api_router.include_router(telemetry_api.router) # El prefijo "/telemetry" ya está en el router
api_router.include_router(procurement_api.router) # El prefijo "/procurement" ya está en el router
api_router.include_router(maintenance_api.router) # El prefijo "/maintenance" ya está en el router
api_router.include_router(core_engine_api.router) # El prefijo "/core-engine" ya está en el router


# --- REGISTRO DE ROUTERS ANTIGUOS ---
api_router.include_router(address.router, prefix="/addresses")
api_router.include_router(allergy.router, prefix="/allergies")
api_router.include_router(analytics.router, prefix="/analytics")
api_router.include_router(client.router, prefix="/clients")
api_router.include_router(contact.router, prefix="/contacts")
api_router.include_router(dicom.router, prefix="/dicom")
api_router.include_router(disease.router, prefix="/diseases")
api_router.include_router(emerg_data.router, prefix="/emerg-data")
api_router.include_router(files.router, prefix="/files")
api_router.include_router(medical_codes.router, prefix="/medical-codes")
api_router.include_router(medical_history.router, prefix="/medical-history")
api_router.include_router(public_profile.router)
api_router.include_router(push_notifications.router)
api_router.include_router(vital_sign.router)
api_router.include_router(addiction.router)
api_router.include_router(infectious_disease.router)
api_router.include_router(menstrual_cycle.router)
api_router.include_router(panic.router)
api_router.include_router(pregnancy.router)
api_router.include_router(psychiatric_condition.router)
api_router.include_router(health.router)
