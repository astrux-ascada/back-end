# /app/identity/models/user.py
"""
Modelo de la base de datos para la entidad User.
"""
import uuid

from sqlalchemy import Boolean, Column, String, Integer, func, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """Modelo SQLAlchemy para un Usuario del sistema."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # --- Relación Multi-Tenant ---
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True, comment="Organización a la que pertenece. NULL = Super Admin Global")
    tenant = relationship("Tenant", back_populates="users")

    # --- Relaciones Muchos-a-Muchos ---
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    # La relación `assigned_sectors` se definirá en el __init__.py del módulo para evitar importaciones circulares.

    # --- Campos de Perfil y Autenticación ---
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String(60), nullable=True)
    username = Column(String(25), unique=True, nullable=True)
    phone = Column(String(25), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    position = Column(String(100), nullable=True)
    occupation = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    preferred_language = Column(String(10), default="es", nullable=False)
    employee_id = Column(String(50), unique=True, nullable=True)

    # --- MEJORA: Campos para 2FA ---
    tfa_secret = Column(String(255), nullable=True, comment="Secreto para la autenticación de dos factores (2FA).")
    is_tfa_enabled = Column(Boolean, default=False, nullable=False, comment="Indica si el 2FA está habilitado para el usuario.")

    # --- MEJORA: Seguridad de Sesión (Hardening) ---
    failed_login_attempts = Column(Integer, default=0, nullable=False, comment="Contador de intentos fallidos consecutivos")
    locked_until = Column(TIMESTAMP(timezone=True), nullable=True, comment="Fecha hasta la cual el usuario está bloqueado temporalmente")
    last_login_at = Column(TIMESTAMP(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)

    # --- MEJORA: Trazabilidad Legal (Términos y Condiciones) ---
    terms_accepted_at = Column(TIMESTAMP(timezone=True), nullable=True, comment="Fecha de aceptación de los términos")
    terms_version = Column(String(20), nullable=True, comment="Versión de los términos aceptada (ej: v1.2)")

    # --- Campos de Auditoría ---
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
