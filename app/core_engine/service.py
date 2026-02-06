# /app/core_engine/service.py
"""
Capa de Servicio para el Core Engine.
"""
import logging
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core_engine import models, schemas
from app.core_engine.repository import CoreEngineRepository
from app.core_engine.connectors.modbus_connector import ModbusConnector
from app.telemetry.service import TelemetryService
from app.core.exceptions import NotFoundException, ConflictException
from app.auditing.service import AuditService
from app.identity.models import User

logger = logging.getLogger("app.core_engine.service")

class CoreEngineService:
    """Servicio de negocio para el Core Engine, gestionando DataSources y conectores."""

    def __init__(self, db: Session, telemetry_service: TelemetryService, audit_service: AuditService):
        self.db = db
        self.telemetry_service = telemetry_service
        self.audit_service = audit_service
        self.core_engine_repo = CoreEngineRepository(self.db)
        self.active_connectors: Dict[uuid.UUID, ModbusConnector] = {}

    def create_data_source(self, ds_in: schemas.DataSourceCreate, tenant_id: uuid.UUID, user: User) -> models.DataSource:
        # Asumiendo que el repo tiene este método
        existing_ds = self.core_engine_repo.db.query(models.DataSource).filter_by(name=ds_in.name, tenant_id=tenant_id).first()
        if existing_ds:
            raise ConflictException(f"Ya existe una fuente de datos con el nombre '{ds_in.name}'.")
        
        new_ds = self.core_engine_repo.create_data_source(ds_in, tenant_id)
        self.audit_service.log_operation(user, "CREATE_DATA_SOURCE", new_ds)
        return new_ds

    def get_data_source(self, ds_id: uuid.UUID, tenant_id: uuid.UUID) -> models.DataSource:
        db_ds = self.core_engine_repo.get_data_source(ds_id, tenant_id)
        if not db_ds:
            raise NotFoundException("Fuente de datos no encontrada.")
        return db_ds

    def list_data_sources(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.DataSource]:
        return self.core_engine_repo.list_data_sources(tenant_id, skip, limit)

    def update_data_source(self, ds_id: uuid.UUID, ds_in: schemas.DataSourceUpdate, tenant_id: uuid.UUID, user: User) -> models.DataSource:
        db_ds = self.get_data_source(ds_id, tenant_id)
        updated_ds = self.core_engine_repo.update_data_source(db_ds, ds_in)
        self.audit_service.log_operation(user, "UPDATE_DATA_SOURCE", updated_ds, details=ds_in.model_dump(exclude_unset=True))
        return updated_ds

    def delete_data_source(self, ds_id: uuid.UUID, tenant_id: uuid.UUID, user: User) -> models.DataSource:
        db_ds = self.get_data_source(ds_id, tenant_id)
        deleted_ds = self.core_engine_repo.delete_data_source(db_ds)
        self.audit_service.log_operation(user, "DELETE_DATA_SOURCE", deleted_ds)
        return deleted_ds

    def start_connector(self, data_source: models.DataSource):
        """Inicia un conector para una fuente de datos específica."""
        if data_source.protocol == "modbus_tcp":
            connector = ModbusConnector(data_source.connection_params, self.telemetry_service)
            self.active_connectors[data_source.id] = connector
            connector.start()
            logger.info(f"Conector Modbus TCP iniciado para {data_source.name}")
        else:
            logger.warning(f"Protocolo {data_source.protocol} no soportado para iniciar conector.")

    def stop_connector(self, data_source_id: uuid.UUID):
        """Detiene un conector activo."""
        connector = self.active_connectors.pop(data_source_id, None)
        if connector:
            connector.stop()
            logger.info(f"Conector detenido para {data_source_id}")

    def start_all_connectors(self):
        """Inicia conectores para todas las fuentes de datos activas en la BD."""
        logger.info("Iniciando todos los conectores de datos activos...")
        active_data_sources = self.db.query(models.DataSource).filter(models.DataSource.is_active == True).all()
        for ds in active_data_sources:
            self.start_connector(ds)
        logger.info(f"{len(self.active_connectors)} conectores iniciados.")

    def stop_all_connectors(self):
        """Detiene todos los conectores activos."""
        logger.info("Deteniendo todos los conectores de datos activos...")
        for ds_id in list(self.active_connectors.keys()):
            self.stop_connector(ds_id)
        logger.info("Todos los conectores han sido detenidos.")
