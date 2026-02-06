# /app/db/seeding/_seed_sectors.py
"""
Seeder para la jerarquía de Sectores de la planta de demostración.
"""
import logging
from sqlalchemy.orm import Session

from app.sectors.models import Sector

logger = logging.getLogger(__name__)

async def seed_sectors(db: Session, context: dict):
    logger.info("--- [3/9] Poblando Sectores ---")
    
    demo_tenant = context["demo_tenant"]

    if db.query(Sector).filter(Sector.tenant_id == demo_tenant.id).first():
        logger.info("Los sectores ya existen, saltando.")
        # Cargar los sectores existentes en el contexto para los siguientes seeders
        context["sector_linea_1"] = db.query(Sector).filter(Sector.name == "Línea de Ensamblaje 1", Sector.tenant_id == demo_tenant.id).first()
        context["sector_empaquetado"] = db.query(Sector).filter(Sector.name == "Empaquetado", Sector.tenant_id == demo_tenant.id).first()
        return

    # 1. Crear Sector Raíz (Planta)
    planta_norte = Sector(name="Planta Norte", description="Planta principal de producción.", tenant_id=demo_tenant.id)
    db.add(planta_norte)
    db.flush()

    # 2. Crear Sectores Hijos
    linea_1 = Sector(name="Línea de Ensamblaje 1", description="Ensamblaje de chasis.", tenant_id=demo_tenant.id, parent_id=planta_norte.id)
    empaquetado = Sector(name="Empaquetado", description="Zona de empaquetado final.", tenant_id=demo_tenant.id, parent_id=planta_norte.id)
    
    db.add_all([linea_1, empaquetado])
    db.commit()

    # Guardar en el contexto para los siguientes seeders
    context["sector_linea_1"] = linea_1
    context["sector_empaquetado"] = empaquetado
