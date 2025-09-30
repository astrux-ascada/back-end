# /app/db/seeding/_seed_sectors.py
"""
Script de siembra para el módulo de Sectores.

Pobla la base de datos con sectores de ejemplo para la planta imaginaria.
"""

import logging
from sqlalchemy.orm import Session

from app.sectors.models import Sector

logger = logging.getLogger(__name__)

def seed_sectors(db: Session):
    """
    Crea sectores de ejemplo si no existen.
    """
    logger.info("Iniciando siembra de datos para Sectores...")

    sectors_data = [
        {"name": "Línea de Estampado 1", "description": "Primera línea de producción de piezas de carrocería."},
        {"name": "Línea de Estampado 2", "description": "Segunda línea de producción idéntica a la primera."},
        {"name": "Almacén de Bobinas", "description": "Área de almacenamiento de materia prima (acero)."},
        {"name": "Área de Mantenimiento", "description": "Zona dedicada a la reparación y mantenimiento de equipos."},
        {"name": "Control de Calidad", "description": "Estación de inspección de piezas estampadas."},
    ]

    for sector_data in sectors_data:
        existing_sector = db.query(Sector).filter(Sector.name == sector_data["name"]).first()
        if not existing_sector:
            db_sector = Sector(**sector_data)
            db.add(db_sector)
            logger.info(f"Sector creado: {sector_data["name"]}")
        else:
            logger.debug(f"Sector ya existe: {sector_data["name"]}. Saltando.")
    
    db.commit()
    logger.info("Siembra de datos para Sectores completada.")
