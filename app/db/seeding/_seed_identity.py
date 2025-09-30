# /app/db/seeding/_seed_identity.py
"""
Script de siembra para el módulo de Identidad (Permissions, Roles, Users).
"""

import logging
from sqlalchemy.orm import Session

from app.identity.models import Permission, Role, User
from app.sectors.models import Sector
from app.core.security import hash_password

logger = logging.getLogger(__name__)

# --- Datos de Siembra Predefinidos ---

PERMISSIONS_DATA = {
    "admin:full-access": "Acceso total a todas las funcionalidades.",
    "user:read": "Leer información de usuarios.",
    "user:create": "Crear nuevos usuarios.",
    "asset:read": "Leer información de activos.",
    "asset:create": "Crear nuevos activos.",
    "asset:update": "Actualizar información de activos.",
    "workorder:read": "Leer órdenes de trabajo.",
    "workorder:create": "Crear nuevas órdenes de trabajo.",
    "workorder:assign": "Asignar órdenes de trabajo a técnicos o proveedores.",
}

ROLES_DATA = {
    "Administrator": ["admin:full-access"],
    "Supervisor": ["asset:read", "workorder:read", "workorder:create", "workorder:assign"],
    "Technician": ["asset:read", "workorder:read"],
    "Operator": ["asset:read"],
}

USERS_DATA = [
    {
        "email": "admin@astruxa.com",
        "name": "Alice Admin",
        "password": "admin_password",
        "roles": ["Administrator"],
        "sectors": ["Línea de Estampado 1", "Línea de Estampado 2", "Control de Calidad", "Área de Mantenimiento"]
    },
    {
        "email": "supervisor@astruxa.com",
        "name": "Bob Supervisor",
        "password": "supervisor_password",
        "roles": ["Supervisor"],
        "sectors": ["Línea de Estampado 1", "Línea de Estampado 2"]
    },
    {
        "email": "tech@astruxa.com",
        "name": "Charlie Technician",
        "password": "tech_password",
        "roles": ["Technician"],
        "sectors": ["Área de Mantenimiento"]
    }
]

def seed_identity(db: Session):
    logger.info("Iniciando siembra de datos para Identidad...")

    # 1. Sembrar Permisos
    for name, desc in PERMISSIONS_DATA.items():
        if not db.query(Permission).filter(Permission.name == name).first():
            db.add(Permission(name=name, description=desc))
    db.commit()
    logger.info("Permisos sembrados.")

    # 2. Sembrar Roles y asignar Permisos
    for name, perm_names in ROLES_DATA.items():
        if not db.query(Role).filter(Role.name == name).first():
            permissions = db.query(Permission).filter(Permission.name.in_(perm_names)).all()
            db_role = Role(name=name, permissions=permissions)
            db.add(db_role)
    db.commit()
    logger.info("Roles y asignación de permisos sembrados.")

    # 3. Sembrar Usuarios y asignar Roles/Sectores
    for user_data in USERS_DATA:
        if not db.query(User).filter(User.email == user_data["email"]).first():
            roles = db.query(Role).filter(Role.name.in_(user_data["roles"])).all()
            sectors = db.query(Sector).filter(Sector.name.in_(user_data["sectors"])).all()
            
            db_user = User(
                email=user_data["email"],
                name=user_data["name"],
                hashed_password=hash_password(user_data["password"]),
                roles=roles,
                assigned_sectors=sectors
            )
            db.add(db_user)
    db.commit()
    logger.info("Usuarios y asignación de roles/sectores sembrados.")

    logger.info("Siembra de datos para Identidad completada.")
