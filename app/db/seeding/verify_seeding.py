# /app/db/seeding/verify_seeding.py
from sqlalchemy import func
from app.core.database import SessionLocal
from app.identity.models import User, Tenant, Role
from app.assets.models import Asset
from app.maintenance.models import WorkOrder
# Importamos AlarmRule para que SQLAlchemy lo registre y resuelva la relación en Asset
from app.alarming.models.alarm_rule import AlarmRule

def verify():
    db = SessionLocal()
    try:
        print("\n--- Verificación de Datos ---")
        
        tenant_count = db.query(func.count(Tenant.id)).scalar()
        print(f"Tenants: {tenant_count}")
        
        user_count = db.query(func.count(User.id)).scalar()
        print(f"Usuarios: {user_count}")
        
        role_count = db.query(func.count(Role.id)).scalar()
        print(f"Roles: {role_count}")
        
        asset_count = db.query(func.count(Asset.id)).scalar()
        print(f"Activos: {asset_count}")
        
        wo_count = db.query(func.count(WorkOrder.id)).scalar()
        print(f"Órdenes de Trabajo: {wo_count}")
        
        print("-----------------------------\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    verify()
