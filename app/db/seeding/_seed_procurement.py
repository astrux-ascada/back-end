# /app/db/seeding/_seed_procurement.py
"""
Seeder para el módulo de Compras (Proveedores y Repuestos).
"""
import logging
from sqlalchemy.orm import Session

from app.procurement.models.provider import Provider
from app.procurement.models.spare_part import SparePart

logger = logging.getLogger(__name__)

async def seed_procurement(db: Session, context: dict):
    logger.info("--- [5/9] Poblando Compras (Proveedores y Repuestos) ---")
    
    demo_tenant = context["demo_tenant"]

    # 1. Crear Proveedor
    provider = db.query(Provider).filter(Provider.name == "Soluciones Industriales ACME", Provider.tenant_id == demo_tenant.id).first()
    if not provider:
        provider = Provider(
            tenant_id=demo_tenant.id,
            name="Soluciones Industriales ACME",
            contact_info="ventas@acme.com",
            specialty="Robótica",
            performance_score=95.0
        )
        db.add(provider)
        db.flush()

    # 2. Crear Repuesto
    spare_part = db.query(SparePart).filter(SparePart.part_number == "SKF-6204-2RS", SparePart.tenant_id == demo_tenant.id).first()
    if not spare_part:
        spare_part = SparePart(
            tenant_id=demo_tenant.id,
            name="Rodamiento de bolas 6204-2RS",
            part_number="SKF-6204-2RS",
            stock_quantity=10,
            price=15.50
            # Eliminados campos que no existen en el modelo actual: min_stock_level, provider_id
        )
        db.add(spare_part)
        db.commit()
    
    context["spare_part_rodamiento"] = spare_part
