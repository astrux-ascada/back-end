# /app/db/seeding/_seed_assets.py
"""
Seeder para los Activos de la planta de demostración.
"""
import logging
from sqlalchemy.orm import Session

from app.assets.models import Asset, AssetType

logger = logging.getLogger(__name__)

async def seed_assets(db: Session, context: dict):
    logger.info("--- [4/9] Poblando Activos ---")
    
    demo_tenant = context["demo_tenant"]
    sector_linea_1 = context["sector_linea_1"]

    # 1. Crear o buscar el Tipo de Activo (AssetType)
    robot_type = db.query(AssetType).filter(
        AssetType.name == "Robot de Soldadura",
        AssetType.tenant_id == demo_tenant.id
    ).first()
    
    if not robot_type:
        robot_type = AssetType(
            tenant_id=demo_tenant.id, # Asignar tenant_id
            name="Robot de Soldadura",
            description="Brazo robótico industrial de 6 ejes",
            manufacturer="KUKA",
            model_number="KR 210",
            category="Robot"
        )
        db.add(robot_type)
        db.commit()
        db.refresh(robot_type)

    # 2. Crear el Activo Físico (Asset)
    # Verificamos si ya existe por su número de serie (que es único)
    brazo_robotico = db.query(Asset).filter(Asset.serial_number == "KR210-2023-001").first()
    
    if not brazo_robotico:
        brazo_robotico = Asset(
            tenant_id=demo_tenant.id,
            asset_type_id=robot_type.id,  # Vinculamos al tipo
            serial_number="KR210-2023-001",
            location="Línea de Ensamblaje 1 - Estación 4",
            status="OPERATIONAL",
            sector_id=sector_linea_1.id,
            properties={"voltaje": 480, "ejes": 6, "firmware": "v4.5.2"}
        )
        db.add(brazo_robotico)
        db.commit()
        db.refresh(brazo_robotico)
    else:
        logger.info("El activo 'Brazo Robótico' ya existe, saltando.")

    # Guardar en el contexto
    context["brazo_robotico"] = brazo_robotico
