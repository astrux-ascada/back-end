# /app/dependencies/services.py
"""
Dependency Injection for Services.
"""
from fastapi import Depends
from sqlalchemy.orm import Session

# --- Inyectores para Módulos Nuevos ---
from app.identity.auth_service import AuthService
from app.assets.service import AssetService
from app.telemetry.service import TelemetryService
from app.procurement.service import ProcurementService
from app.maintenance.service import MaintenanceService
from app.core_engine.service import CoreEngineService
 
 

# --- Dependencias antiguas (se irán eliminando a medida que refactoricemos) ---
from app.contracts.IContactService import IContactService
from app.contracts.IClientService import IClientService
from app.contracts.IAddressService import IAddressService
from app.contracts.IEmergDataService import IEmergDataService
from app.contracts.IAllergyService import IAllergyService
from app.contracts.IDiseaseService import IDiseaseService
from app.contracts.IPublicProfileService import IPublicProfileService
from app.contracts.IMedicalHistoryService import IMedicalHistoryService
from app.contracts.IAnalyticsService import IAnalyticsService
from app.contracts.IStorageService import IStorageService
from app.contracts.IPushNotificationService import IPushNotificationService
from app.contracts.IVitalSignService import IVitalSignService
from app.contracts.external.IGoogleTranslateService import IGoogleTranslateService
from app.core.database import get_db
from app.services.address_service import AddressService
from app.services.allergy_service import AllergyService
from app.services.analytics_service import AnalyticsService
from app.services.client_service import ClientService
from app.services.contact_service import ContactService
from app.services.disease_service import DiseaseService
from app.services.emerg_data_service import EmergDataService
from app.services.external.factory import ExternalServiceFactory
from app.services.external.google_translate import get_google_translate_service
from app.services.medical_history_service import MedicalHistoryService
from app.services.public_profile_service import PublicProfileService
from app.services.push_notification_service import PushNotificationService
from app.services.storage import StorageService
from app.services.vital_sign_service import VitalSignService


# --- Inyectores para Módulos de Astruxa ---

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)

def get_asset_service(db: Session = Depends(get_db)) -> AssetService:
    return AssetService(db)

def get_telemetry_service(db: Session = Depends(get_db)) -> TelemetryService:
    return TelemetryService(db)

def get_procurement_service(db: Session = Depends(get_db)) -> ProcurementService:
    return ProcurementService(db)

def get_maintenance_service(db: Session = Depends(get_db)) -> MaintenanceService:
  
    return MaintenanceService(db)

def get_core_engine_service(db: Session = Depends(get_db)) -> CoreEngineService:
    return CoreEngineService(db)

 

# --- Inyectores antiguos (se irán eliminando) ---

_medical_codes_factory_instance = ExternalServiceFactory()

def get_medical_codes_service_factory() -> ExternalServiceFactory:
    return _medical_codes_factory_instance

def get_storage_service() -> IStorageService:
    return StorageService()

def get_client_service(
        db: Session = Depends(get_db),
        storage_service: IStorageService = Depends(get_storage_service),
        translator: IGoogleTranslateService = Depends(get_google_translate_service),
) -> IClientService:
    return ClientService(db=db, storage_service=storage_service, translator=translator)

def get_contact_service(db: Session = Depends(get_db)) -> IContactService:
    return ContactService(db)

def get_address_service(db: Session = Depends(get_db)) -> IAddressService:
    return AddressService(db)

def get_emerg_data_service(db: Session = Depends(get_db)) -> IEmergDataService:
    return EmergDataService(db)

def get_allergy_service(db: Session = Depends(get_db)) -> IAllergyService:
    return AllergyService(db)

def get_disease_service(db: Session = Depends(get_db)) -> IDiseaseService:
    return DiseaseService(db)

def get_public_profile_service(db: Session = Depends(get_db)) -> IPublicProfileService:
    return PublicProfileService(db)

def get_medical_history_service(
    db: Session = Depends(get_db),
    storage_service: IStorageService = Depends(get_storage_service),
) -> IMedicalHistoryService:
    return MedicalHistoryService(db=db, storage_service=storage_service)

def get_analytics_service(db: Session = Depends(get_db)) -> IAnalyticsService:
    return AnalyticsService(db)

def get_push_notification_service(db: Session = Depends(get_db)) -> IPushNotificationService:
    return PushNotificationService(db)

def get_vital_sign_service(db: Session = Depends(get_db)) -> IVitalSignService:
    return VitalSignService(db)
