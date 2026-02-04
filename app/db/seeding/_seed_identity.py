# /app/db/seeding/_seed_identity.py
"""
Script para sembrar la base de datos con datos iniciales de Identidad (Roles y Usuarios).
"""
import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.identity.models import Role, User
from app.identity.schemas import UserCreate
from app.identity.repository import UserRepository

logger = logging.getLogger(__name__)

def seed_identity(db: Session) -> None:
    """Crea roles y usuarios de ejemplo si no existen."""
    logger.info("Iniciando el sembrado de datos de Identidad...")

    # --- 1. Crear Roles Estandarizados ---
    roles_to_create = {
        "SUPERUSER": "Acceso total a todas las funcionalidades.",
        "ADMINISTRATOR": "Acceso administrativo a la mayoría de funcionalidades.",
        "MAINTENANCE_MANAGER": "Gestiona órdenes de trabajo, planes y técnicos.",
        "TECHNICIAN": "Ejecuta órdenes de trabajo de mantenimiento.",
        "VIEWER": "Acceso de solo lectura a la información operativa."
    }
    
    created_roles = {}
    for role_name, role_desc in roles_to_create.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=role_desc)
            db.add(role)
            logger.info(f"Creando rol: {role_name}")
        created_roles[role_name] = role
    db.commit()
    
    # Refrescar para obtener IDs
    for name, role in created_roles.items():
        if not role.id:
            created_roles[name] = db.query(Role).filter(Role.name == name).first()

    # --- 2. Crear Usuarios de Ejemplo ---
    user_repo = UserRepository(db)
    users_to_create = [
        {
            "email": settings.FIRST_SUPERUSER_EMAIL,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "name": "Super User",
            "role_name": "SUPERUSER"
        },
        {
            "email": "manager@astruxa.com",
            "password": "manager123",
            "name": "Manager de Mantenimiento",
            "role_name": "MAINTENANCE_MANAGER"
        },
        {
            "email": "technician@astruxa.com",
            "password": "tech1234", # CORREGIDO: Contraseña con 8 caracteres
            "name": "Técnico de Campo",
            "role_name": "TECHNICIAN"
        },
        {
            "email": "viewer@astruxa.com",
            "password": "viewer123",
            "name": "Gerente de Planta",
            "role_name": "VIEWER"
        }
    ]

    for user_data in users_to_create:
        if not db.query(User).filter(User.email == user_data["email"]).first():
            role_name = user_data.pop("role_name")
            role = created_roles.get(role_name)
            if role:
                user_in = UserCreate(
                    email=user_data["email"],
                    password=user_data["password"],
                    name=user_data["name"],
                    role_ids=[role.id]
                )
                user_repo.create(user_in=user_in)
                logger.info(f"Creando usuario: {user_data['email']} con rol {role_name}")

    logger.info("Sembrado de datos de Identidad completado.")
