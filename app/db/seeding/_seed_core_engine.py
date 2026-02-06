# /app/db/seeding/_seed_core_engine.py
"""
Seeder para el Core Engine (Fuentes de Datos).
"""
import logging
from sqlalchemy.orm import Session

from app.core_engine.models import DataSource

logger = logging.getLogger(__name__)

async def seed_core_engine(db: Session, context: dict):
    logger.info("--- [8/9] Poblando Core Engine (Fuentes de Datos) ---")
    
    demo_tenant = context["demo_tenant"]
    brazo_robotico = context["brazo_robotico"]

    # Crear Fuente de Datos Modbus TCP
    ds = db.query(DataSource).filter(DataSource.name == "Modbus Brazo Robótico", DataSource.tenant_id == demo_tenant.id).first()
    if not ds:
        ds = DataSource(
            tenant_id=demo_tenant.id,
            name="Modbus Brazo Robótico",
            protocol="modbus_tcp",
            connection_params={"host": "192.168.1.10", "port": 502},
            is_active=True
        )
        db.add(ds)
        db.commit()
