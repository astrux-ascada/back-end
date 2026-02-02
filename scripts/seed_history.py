import asyncio
import sys
import os
import random
from datetime import datetime, timedelta

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from sqlalchemy import text

# --- CORRECCIÓN ---
# Usar números de serie que son creados por el script de sembrado --core
# para asegurar que los activos ya existan.
MACHINES = ["SCH-L1-001", "KUK-L1-001"] 
DAYS_TO_SIMULATE = 7

async def seed_history():
    print(f"🌱 Sembrando {DAYS_TO_SIMULATE} días de historia para {len(MACHINES)} máquinas...")

    async with AsyncSessionLocal() as session:
        try:
            # 1. Obtener IDs de las máquinas
            machine_ids = {}
            for serial_num in MACHINES:
                result = await session.execute(
                    text("SELECT id FROM assets WHERE serial_number = :serial_num"),
                    {"serial_num": serial_num}
                )
                machine_id = result.scalar()
                
                # Este bloque de "creación al vuelo" no debería ejecutarse si --core se ejecutó primero,
                # pero lo corregimos para que sea robusto.
                if not machine_id:
                    print(f"⚠️ Máquina con serial {serial_num} no existe. Creándola...")
                    
                    # Buscamos un tipo de activo 'MACHINE' para asociarlo
                    asset_type_result = await session.execute(text("SELECT id FROM asset_types WHERE category = 'MACHINE' LIMIT 1"))
                    asset_type_id = asset_type_result.scalar()
                    if not asset_type_id:
                        raise Exception("No se encontró un AssetType de categoría 'MACHINE' para crear el activo.")

                    # --- CORRECCIÓN: Se eliminó la columna 'name' del INSERT ---
                    result = await session.execute(
                        text("""
                            INSERT INTO assets (serial_number, asset_type_id, location, status)
                            VALUES (:serial_num, :asset_type_id, 'Simulated Location', 'operational')
                            RETURNING id
                        """),
                        {
                            "serial_num": serial_num,
                            "asset_type_id": asset_type_id
                        }
                    )
                    machine_id = result.scalar()
                
                machine_ids[serial_num] = machine_id

            # 2. Generar datos día por día
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=DAYS_TO_SIMULATE)
            
            current_time = start_date
            total_records = 0

            while current_time < end_date:
                for serial_num, m_id in machine_ids.items():
                    is_running = random.random() > 0.1
                    value = random.uniform(40, 90) if is_running else random.uniform(0, 5)
                    
                    await session.execute(
                        text("""
                            INSERT INTO sensor_readings (timestamp, asset_id, metric_name, value)
                            VALUES (:time, :asset_id, 'process_speed', :value)
                        """),
                        {
                            "time": current_time,
                            "asset_id": m_id,
                            "value": value
                        }
                    )

                current_time += timedelta(minutes=15)
                total_records += len(MACHINES)
                
                if total_records % 100 == 0:
                    print(f"⏳ Generados {total_records} registros...")

            await session.commit()
            print(f"✅ ¡Éxito! Se insertaron aprox {total_records} registros históricos.")

        except Exception as e:
            print(f"❌ Error sembrando datos: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_history())
