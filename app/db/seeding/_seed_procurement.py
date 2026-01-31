# /app/db/seeding/_seed_procurement.py
"""
Script para sembrar la base de datos con datos de Compras (Proveedores y Repuestos).
"""
import logging
from sqlalchemy.orm import Session
from app.procurement.models import Provider, SparePart

logger = logging.getLogger(__name__)

def seed_procurement(db: Session):
    """
    Crea proveedores y repuestos de ejemplo.
    """
    logger.info("Iniciando siembra de datos para Compras...")

    # --- 1. Crear Proveedores ---
    providers_data = [
        {"name": "ACME Industrial Solutions", "specialty": "Componentes Mecánicos", "performance_score": 92.5},
        {"name": "Global Robotics & Automation", "specialty": "Sensores y Actuadores", "performance_score": 98.1},
        {"name": "Filtros y Partes Express", "specialty": "Consumibles", "performance_score": 88.0},
    ]
    
    created_providers = {}
    for provider_data in providers_data:
        if not db.query(Provider).filter_by(name=provider_data["name"]).first():
            provider = Provider(**provider_data)
            db.add(provider)
            logger.info(f"Creando proveedor: {provider.name}")
            created_providers[provider.name] = provider
    db.commit()

    # Para asegurar que tenemos los IDs, los volvemos a consultar
    for name in created_providers:
        created_providers[name] = db.query(Provider).filter_by(name=name).first()


    # --- 2. Crear Repuestos ---
    spare_parts_data = [
        {"name": "Rodamiento de bolas 6204-2RS", "part_number": "SKF-6204", "current_stock": 50, "min_stock_level": 10, "unit_cost": 15.75, "provider_name": "ACME Industrial Solutions"},
        {"name": "Sensor de proximidad inductivo", "part_number": "SN04-N", "current_stock": 25, "min_stock_level": 5, "unit_cost": 25.50, "provider_name": "Global Robotics & Automation"},
        {"name": "Filtro de aire P-500", "part_number": "FP-500", "current_stock": 100, "min_stock_level": 20, "unit_cost": 8.99, "provider_name": "Filtros y Partes Express"},
        {"name": "Grasa lubricante de litio", "part_number": "GL-LITIO-500G", "current_stock": 40, "min_stock_level": 15, "unit_cost": 12.00, "provider_name": None},
    ]

    for part_data in spare_parts_data:
        if not db.query(SparePart).filter_by(part_number=part_data["part_number"]).first():
            provider_name = part_data.pop("provider_name")
            provider = created_providers.get(provider_name)
            if provider:
                part_data["provider_id"] = provider.id
            
            part = SparePart(**part_data)
            db.add(part)
            logger.info(f"Creando repuesto: {part.name}")
            
    db.commit()
    logger.info("Siembra de datos para Compras completada.")
