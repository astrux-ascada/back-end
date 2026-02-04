# /app/core/middlewares/tenant_middleware.py
"""
Middleware de FastAPI para identificar y establecer el contexto del Tenant en cada petición.
"""
import uuid
from typing import Callable # Importar el tipo genérico Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.context import tenant_id_context, user_id_context
from app.identity.models.user import User

class TenantMiddleware(BaseHTTPMiddleware):
    """
    Este middleware se encarga de identificar el tenant del usuario autenticado
    y de inyectarlo en el contexto de la petición (`ContextVar`).
    """
    async def dispatch(
        self, request: Request, call_next: Callable # Usar el tipo genérico Callable
    ) -> Response:
        """
        Procesa la petición para extraer el tenant_id.
        """
        user_id_str = request.scope.get("user", {}).get("id")

        if user_id_str:
            try:
                user_id = uuid.UUID(user_id_str)
                user_id_context.set(user_id)

                db: Session = SessionLocal()
                try:
                    user_tenant = db.query(User.tenant_id).filter(User.id == user_id).first()
                    if user_tenant and user_tenant.tenant_id:
                        tenant_id_context.set(user_tenant.tenant_id)
                finally:
                    db.close()

            except (ValueError, TypeError):
                pass

        response = await call_next(request)
        return response
